import httpx
import asyncio
import statistics
from datetime import datetime, timedelta
import pandas as pd
import pandas_ta as ta
import random
import matplotlib.pyplot as plt
from io import BytesIO
import matplotlib.dates as mdates
from matplotlib.ticker import FuncFormatter
import yfinance as yf
import logging
from pycoingecko import CoinGeckoAPI
from dotenv import load_dotenv
import os
import time  # Для задержек и кэша
import json
import requests
import mplfinance as mpf
import matplotlib.pyplot as plt
import traceback
import numpy as np
import logging
from io import BytesIO
from typing import List, Tuple, Optional, Dict, Any

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib import gridspec
import re
import io

load_dotenv()

cg = CoinGeckoAPI()

# URL для API Bybit v5
BASE_URL = "https://api.bybit.com"

# Простой кэш (словарь в памяти)
data_cache = {}
CACHE_TTL = 3600  # 1 час в секундах

# Логи (чтобы отслеживать запросы)
logging.basicConfig(level=logging.INFO)

BYBIT_TIMEFRAMES = {
    '5m': '5',    # 5 минут
    '1h': '60',   # 1 час (60 минут)
    '1d': 'D',    # 1 день
    '1w': 'W',    # 1 неделя
    '1M': 'M',    # <-- ДОБАВЛЕНО: Прямой запрос месячных свечей
    '6M': 'D',    # <-- ВНИМАНИЕ: Для 6 месяцев запрашиваем дневные (D) для последующей агрегации
    '1Y': 'D',    # <-- ВНИМАНИЕ: Для 1 года также запрашиваем дневные (D)
}

# normalize timeframe keys for case-insensitive lookups
BYBIT_TIMEFRAMES = {k.upper(): v for k, v in BYBIT_TIMEFRAMES.items()}






async def get_bybit_symbols(category='linear'):
    for attempt in range(3):
        try:
            async with httpx.AsyncClient() as session:
                params = {"category": category}
                response = await session.get(f"{BASE_URL}/v5/market/instruments-info", params=params)
                response.raise_for_status()
                data = response.json()
                if data.get("retCode") == 0:
                    symbols = []
                    for item in data['result']['list']:
                        symbol_name = item['symbol']
                        # 1. Проверяем, что символ заканчивается на USDT
                        # 2. Проверяем, что символ не начинается с цифр
                        if symbol_name.endswith('USDT') and not symbol_name[0].isdigit():
                            symbols.append({
                                "symbol": symbol_name,
                                "name": item['baseCoin']
                            })
                    return symbols
                else:
                    logging.error(f"Bybit API error: {data.get('retMsg')}")
        except httpx.RequestError as e:
            logging.error(f"HTTP request failed: {e}")
        except Exception as e:
            logging.error(f"An error occurred: {e}")
    return None

# Функция для скачивания/обновления списка монет (раз в день, с retries и fallback)
def load_coins_list(force_update=False, max_retries=3, min_expected_coins=10000):
    file = 'coins.json'

    if os.path.exists(file) and not force_update:
        with open(file, 'r') as f:
            data = json.load(f)
        if time.time() - data.get('timestamp', 0) < 86400:
            logging.info("Список монет из кэша")
            return data  # dict {'coins': list}

    for attempt in range(1, max_retries + 1):
        try:
            time.sleep(1 + random.uniform(0, 1))
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
            response = requests.get("https://api.coingecko.com/api/v3/coins/list", headers=headers, timeout=10)
            response.raise_for_status()
            coins = response.json()
            if len(coins) < min_expected_coins:
                raise ValueError("Incomplete list")
            save_data = {'coins': coins, 'timestamp': time.time()}
            with open(file, 'w') as f:
                json.dump(save_data, f)
            logging.info(f"Список монет обновлён: {len(coins)} монет")
            return save_data
        except Exception as e:
            logging.error(f"Ошибка на попытке {attempt}: {e}")
            if attempt < max_retries:
                backoff = 2 ** (attempt - 1)
                if response.status_code == 429 if 'response' in locals() else False:
                    backoff += 60
                time.sleep(backoff)
            else:
                if os.path.exists(file):
                    with open(file, 'r') as f:
                        data = json.load(f)
                    logging.warning("Fallback на старый кэш")
                    return data
                return {'coins': []}
    return {'coins': []}

# Функция для поиска coin_id по symbol (e.g., 'ton' -> 'the-open-network')
def get_coin_id(symbol: str):
    coins = load_coins_list()
    symbol_lower = symbol.lower().replace('usdt', '')
    for coin in coins:
        if coin['symbol'] == symbol_lower:
            return coin['id']
    logging.warning(f"Монета {symbol_lower} не найдена в списке")
    return None


# В get_stock_data: аналогично, для '1m' no aggregation, '6m' aggregate 6, '1y' aggregate 12
def get_stock_data(symbol: str, interval: str, limit: int):
    period_map = {'5m': '1d', '1h': '5d', '1d': '1mo', '1w': '3mo', '1m': '6mo', '6m': '1y', '1y': '2y'}
    yf_interval_map = {'5m': '5m', '1h': '1h', '1d': '1d', '1w': '1wk', '1m': '1mo', '6m': '1mo', '1y': '1mo'}
    period = period_map.get(interval, "1mo")
    yf_interval = yf_interval_map.get(interval, "1d")
    df = yf.download(symbol, period=period, interval=yf_interval)
    if df.empty:
        raise ValueError(f"No data from yfinance for {symbol}")
    df.reset_index(inplace=True)
    df['timestamp'] = (df['Date'].astype('int64') // 10**6).astype(int)  # ms
    kline_data = df[['timestamp', 'Open', 'High', 'Low', 'Close', 'Volume']].values.tolist()[-limit:]  # 6 columns
    # Aggregation for long TF
    if interval in ['1m', '6m', '1y']:
        agg_period = 1 if interval == '1m' else 6 if interval == '6m' else 12
        kline_data = aggregate_kline(kline_data, period=agg_period, freq='M')
    tech_metrics = calculate_advanced_metrics(kline_data)
    market_data = {
        "kline_data": kline_data,
        "symbol": symbol,
        "current_price": kline_data[-1][4] if kline_data else 0,
        "price_change_24h_percent": tech_metrics.get('price_change_24h_percent', 0),
        "open_interest_value": tech_metrics.get('open_interest_value', 0),
        "funding_rate": tech_metrics.get('funding_rate', 0),
        "timeframe": interval,
        "onchain": tech_metrics.get('onchain', {}),
        "macro": tech_metrics.get('macro', {}),
        "backtest_probs": tech_metrics.get('backtest_probs', {}),
        "atr": tech_metrics.get('atr', 0),
        "volatility_percent": tech_metrics.get('volatility_percent', 0),
        "ema_20": tech_metrics.get('ema_20', 0),
        "ema_50": tech_metrics.get('ema_50', 0),
        "trend_condition": tech_metrics.get('trend_condition', 'Нейтральный'),
        "rsi": tech_metrics.get('rsi', 50),
        "bollinger_high": tech_metrics.get('bollinger_high', 0),
        "bollinger_low": tech_metrics.get('bollinger_low', 0),
        "support_level": tech_metrics.get('support_level', 0),
        "resistance_level": tech_metrics.get('resistance_level', 0),
        "macd_line": tech_metrics.get('macd_line', 0),
        "signal_line": tech_metrics.get('signal_line', 0),
        "macd_trend": tech_metrics.get('macd_trend', 'Нейтральный'),
        "vwap": tech_metrics.get('vwap', 0)
    }
    return market_data

# Функция для получения клайн данных (с кэшем и задержкой)
# async def get_kline_data(symbol, timeframe, limit=500):
#
#     url = f"{BASE_URL}/v5/market/kline"
#     bybit_timeframe = BYBIT_TIMEFRAMES.get(str(timeframe).upper(), None)
#
#     if bybit_timeframe is None:
#         logging.error(f"Invalid timeframe: {timeframe}")
#         return None
#
#     params = {
#         "category": "linear",
#         "symbol": symbol,
#         "interval": bybit_timeframe,
#         "limit": limit
#     }
#
#     for attempt in range(3):
#         try:
#             async with httpx.AsyncClient() as session:
#                 response = await session.get(url, params=params)
#                 response.raise_for_status()
#                 data = response.json()
#
#                 if data.get("retCode") == 0 and data['result']['list']:
#                     return data['result']['list']
#                 else:
#                     logging.warning(f"Empty kline for {symbol} in linear. Attempt {attempt + 1}.")
#                     time.sleep(1)
#         except httpx.RequestError as e:
#             logging.error(f"HTTP request failed: {e}")
#             time.sleep(1)
#         except Exception as e:
#             logging.error(f"An error occurred: {e}")
#             time.sleep(1)
#
#     logging.error(f"Failed to get kline data for {symbol} after 3 attempts.")
#     return None

async def get_kline_data(symbol, timeframe, limit=500):
    url = f"{BASE_URL}/v5/market/kline"
    bybit_timeframe = BYBIT_TIMEFRAMES.get(str(timeframe).upper(), None)

    if bybit_timeframe is None:
        logging.error(f"Invalid timeframe: {timeframe}")
        return None

    params = {
        "category": "linear",
        "symbol": symbol,
        "interval": bybit_timeframe,
        "limit": limit
    }

    for attempt in range(3):
        try:
            async with httpx.AsyncClient() as session:
                response = await session.get(url, params=params)
                response.raise_for_status()
                data = response.json()

                if data.get("retCode") == 0 and data['result'].get('list'):
                    raw_list = data['result']['list']
                    normalized = []
                    for item in raw_list:
                        # If API already returned list-of-values (rare), keep it
                        if isinstance(item, (list, tuple)):
                            normalized.append(item)
                            continue

                        # Bybit usually returns dict like {'start': 1672531200, 'open': '...', ...}
                        ts = item.get('start') or item.get('t') or item.get('open_time') or item.get('timestamp')
                        if ts is None:
                            continue
                        try:
                            ts = int(float(ts))
                        except:
                            continue
                        # convert seconds -> ms if needed
                        ts_ms = ts if ts > 1_000_000_000_000 else ts * 1000

                        o = float(item.get('open', item.get('open_price', 0) or 0))
                        h = float(item.get('high', 0) or 0)
                        l = float(item.get('low', 0) or 0)
                        c = float(item.get('close', 0) or 0)
                        v = float(item.get('volume', item.get('turnover', 0) or 0))

                        row = [ts_ms, o, h, l, c, v]
                        # optional turnover if present
                        if 'turnover' in item:
                            try:
                                row.append(float(item.get('turnover', 0) or 0))
                            except:
                                pass
                        normalized.append(row)

                    return normalized
                else:
                    logging.warning(f"Empty kline for {symbol} in linear. Attempt {attempt + 1}.")
                    time.sleep(1)
        except httpx.RequestError as e:
            logging.error(f"HTTP request failed: {e}")
            time.sleep(1)
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            time.sleep(1)

    logging.error(f"Failed to get kline data for {symbol} after 3 attempts.")
    logging.info(
        f"Fetched {len(normalized)} candles for {symbol} {bybit_timeframe}: {pd.to_datetime(normalized[0][0], unit='ms')} - {pd.to_datetime(normalized[-1][0], unit='ms')}")
    return None


# Функция для расчёта MVRV (derive из CoinGecko)
def derive_mvrv(symbol: str):
    try:
        coin_id = get_coin_id(symbol)
        if not coin_id:
            return {"value": 1, "interpretation": "N/A"}
        data = cg.get_coin_by_id(coin_id)
        market_cap = data.get('market_data', {}).get('market_cap', {}).get('usd', 0)
        supply = data.get('market_data', {}).get('circulating_supply', 0)
        hist = cg.get_coin_market_chart_by_id(coin_id, 'usd', '365')
        avg_price = sum(p[1] for p in hist.get('prices', [])) / len(hist['prices']) if hist.get('prices') else 1
        realized_cap = supply * avg_price
        mvrv = market_cap / realized_cap if realized_cap else 1
        interpretation = "Бычий" if mvrv < 1 else "Медвежий"
        return {"value": mvrv, "interpretation": interpretation}
    except Exception as e:
        logging.error(f"Ошибка derive MVRV: {e}")
        return {"value": 1, "interpretation": "N/A"}


# Функция для расчёта Puell (derive из CoinGecko)
def derive_puell(symbol: str):
    try:
        coin_id = get_coin_id(symbol)
        if not coin_id:
            return {"value": 1, "interpretation": "N/A"}
        hist = cg.get_coin_market_chart_by_id(coin_id, 'usd', '365')
        prices = [p[1] for p in hist.get('prices', [])]
        daily_issuance = 450  # BTC; for TON 0
        ma_price = sum(prices) / len(prices) if prices else 1
        ma_issuance = ma_price * daily_issuance
        current_issuance = prices[-1] * daily_issuance if prices else 1
        puell = current_issuance / ma_issuance if ma_issuance else 1
        interpretation = "Бычий" if puell < 0.5 else "Медвежий"
        return {"value": puell, "interpretation": interpretation}
    except Exception as e:
        logging.error(f"Ошибка derive Puell: {e}")
        return {"value": 1, "interpretation": "N/A"}

# Пропущенная функция get_macro_data (для макро из yfinance)
# def get_macro_data(symbol: str):
#     try:
#         api_key = os.getenv('ALPHA_VANTAGE_API_KEY')
#         # BTC
#         url_btc = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=BTCUSD&outputsize=full&apikey={api_key}"
#         response_btc = requests.get(url_btc)
#         data_btc = response_btc.json()['Time Series (Daily)']
#         df_btc = pd.DataFrame.from_dict(data_btc, orient='index')
#         df_btc = df_btc.sort_index()
#         df_btc['close'] = df_btc['4. close'].astype(float)
#         # S&P
#         url_sp = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=^GSPC&outputsize=full&apikey={api_key}"
#         response_sp = requests.get(url_sp)
#         data_sp = response_sp.json()['Time Series (Daily)']
#         df_sp = pd.DataFrame.from_dict(data_sp, orient='index')
#         df_sp = df_sp.sort_index()
#         df_sp['close'] = df_sp['4. close'].astype(float)
#         # Align dates
#         common_dates = df_btc.index.intersection(df_sp.index)
#         df_btc = df_btc.loc[common_dates]
#         df_sp = df_sp.loc[common_dates]
#         corr = df_btc['close'].corr(df_sp['close'])
#         corr = 0 if pd.isna(corr) else corr
#         # ETF inflows (GBTC)
#         url_etf = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=GBTC&outputsize=compact&apikey={api_key}"
#         response_etf = requests.get(url_etf)
#         data_etf = response_etf.json()['Time Series (Daily)']
#         df_etf = pd.DataFrame.from_dict(data_etf, orient='index')
#         df_etf = df_etf.sort_index()
#         df_etf['volume'] = df_etf['5. volume'].astype(float)
#         etf_inflows = df_etf['volume'].sum() if not df_etf.empty else 0
#         interpretation = "Бычий" if corr > 0.5 else "Медвежий"
#         return {"sp500_corr": corr, "etf_inflows": etf_inflows, "interpretation": interpretation}
#     except Exception as e:
#         logging.error(f"Ошибка macro: {e}")
#         return {"sp500_corr": 0, "etf_inflows": 0, "interpretation": "N/A"}

def get_macro_data(symbol: str):
    try:
        # Получаем данные S&P 500
        sp500_ticker = yf.Ticker('^GSPC')
        sp500_df_raw = sp500_ticker.history(period='2y')
        if sp500_df_raw.empty:
            logging.error("Failed to get S&P 500 data from yfinance.")
            return {"sp500_corr": 0, "etf_inflows": 0, "interpretation": "N/A"}
        sp500_df = sp500_df_raw['Close'].resample('D').mean().ffill()

        # Получаем данные BTC
        btc_ticker = yf.Ticker('BTC-USD')
        btc_df_raw = btc_ticker.history(period='2y')
        if btc_df_raw.empty:
            logging.error("Failed to get BTC data from yfinance.")
            return {"sp500_corr": 0, "etf_inflows": 0, "interpretation": "N/A"}
        btc_df = btc_df_raw['Close'].resample('D').mean().ffill()

        # ✅ Используем join, чтобы объединить DataFrame по общим датам
        combined_df = btc_df.to_frame(name='btc_close').join(sp500_df.to_frame(name='sp500_close'), how='inner')

        if combined_df.empty:
            logging.warning("No common dates for correlation analysis after joining on index.")
            return {"sp500_corr": 0, "etf_inflows": 0, "interpretation": "N/A"}

        corr = combined_df['btc_close'].corr(combined_df['sp500_close'])
        corr = 0 if pd.isna(corr) else corr


        # Получаем данные по ETF GBTC
        gbtc_ticker = yf.Ticker('GBTC')
        gbtc_df = gbtc_ticker.history(period='30d')  # Короткий период для объемов

        etf_inflows = gbtc_df['Volume'].sum() if not gbtc_df.empty else 0

        interpretation = "Бычий" if corr > 0.5 else "Медвежий"

        return {"sp500_corr": corr, "etf_inflows": etf_inflows, "interpretation": interpretation}

    except Exception as e:
        logging.error(f"Ошибка macro: {e}")
        return {"sp500_corr": 0, "etf_inflows": 0, "interpretation": "N/A"}


# Пропущенная функция backtest_probabilities (простой backtest на kline)
# Замените существующую функцию backtest_probabilities на этот вариант
async def backtest_probabilities(kline: list, symbol: str, timeframe: str):
    try:
        default = {"up": 50, "base": 30, "down": 20}

        # Быстрые проверки
        if not kline or len(kline) < 3:
            logging.warning("Bybit API returned no/insufficient data for backtest.")
            return default

        # --- Нормализация входа (поддержка dicts и lists) ---
        # Если элементы - dict, приводим к list-of-lists: [ts_ms, o, h, l, c, v]
        if isinstance(kline[0], dict):
            normalized = []
            for it in kline:
                ts = it.get('start') or it.get('t') or it.get('timestamp') or it.get('open_time')
                if ts is None:
                    continue
                try:
                    ts = int(float(ts))
                except:
                    continue
                # convert seconds->ms if needed
                if ts < 1_000_000_000_000:
                    ts = ts * 1000
                o = float(it.get('open', it.get('open_price', 0) or 0))
                h = float(it.get('high', 0) or 0)
                l = float(it.get('low', 0) or 0)
                c = float(it.get('close', it.get('close_price', 0) or 0))
                v = float(it.get('volume', 0) or 0)
                normalized.append([ts, o, h, l, c, v])
            kline = normalized

        # Ensure structure width >=6
        if not kline or len(kline[0]) < 6:
            logging.warning("Kline format unexpected for backtest.")
            return default

        # Создаём DataFrame гибко (если есть turnover — включаем)
        num_cols = len(kline[0])
        cols = ['timestamp', 'open', 'high', 'low', 'close', 'volume']
        if num_cols >= 7:
            cols.append('turnover')
        df = pd.DataFrame(kline, columns=cols[:num_cols])
        # timestamps
        df['timestamp'] = pd.to_numeric(df['timestamp'], errors='coerce')
        df = df.dropna(subset=['timestamp'])
        # convert seconds->ms if needed
        if df['timestamp'].max() < 1_000_000_000_000:
            df['timestamp'] = df['timestamp'] * 1000
        df['timestamp'] = pd.to_datetime(df['timestamp'].astype('int64'), unit='ms')
        df.set_index('timestamp', inplace=True)
        df = df.sort_index()
        # numeric cast
        for c in ['open', 'high', 'low', 'close', 'volume']:
            if c in df.columns:
                df[c] = pd.to_numeric(df[c], errors='coerce')

        df = df.dropna(subset=['close'])
        if df.empty or len(df) < 3:
            logging.warning("Not enough valid close prices for backtest.")
            return default

        # --- Индикаторы с fallback (min_periods=1) ---
        # EMA через pandas.ewm чтобы не было NaN при короткой истории
        df['ema20'] = df['close'].ewm(span=20, adjust=False, min_periods=1).mean()
        df['ema50'] = df['close'].ewm(span=50, adjust=False, min_periods=1).mean()

        # Надёжная реализация RSI (EWMA based), работает при коротких сериях
        def rsi_series(series: pd.Series, length: int = 14) -> pd.Series:
            delta = series.diff()
            up = delta.clip(lower=0)
            down = -delta.clip(upper=0)
            # Wilder smoothing approx via ewm with alpha=1/length
            ma_up = up.ewm(alpha=1/length, adjust=False, min_periods=1).mean()
            ma_down = down.ewm(alpha=1/length, adjust=False, min_periods=1).mean()
            rs = ma_up / ma_down.replace(0, 1e-9)
            rsi = 100 - (100 / (1 + rs))
            return rsi

        df['rsi'] = rsi_series(df['close'], length=14)

        # Trend bull: prefer EMA cross, но если короткая серия - fallback на положительный средний рост
        df['price_slope_3'] = df['close'].pct_change().rolling(3, min_periods=1).mean()
        df['trend_bull'] = ((df['ema20'] > df['ema50']) | (df['price_slope_3'] > 0)).astype(int)

        # RSI filter (relaxed threshold as у вас было 35)
        df['rsi_bull'] = (df['rsi'] > 35).astype(int)

        # Forward return (следующий бар)
        df['return'] = df['close'].pct_change().shift(-1)
        # outcome: up/down/base (порог 1% можно варьировать)
        df['outcome'] = 0
        df.loc[df['return'] > 0.01, 'outcome'] = 1
        df.loc[df['return'] < -0.01, 'outcome'] = -1

        # --- Логирование перед фильтрацией ---
        logging.info(f"Backtest total candles: {len(df)}; date range: {df.index.min()} - {df.index.max()}")

        # Основная фильтрация: сначала строгий вариант
        bull_cases = df[(df['trend_bull'] == 1) & (df['rsi_bull'] == 1)]
        logging.info(f"After trend & rsi filter: {len(bull_cases)}")

        # Если пусто — progressive relaxation
        if bull_cases.empty:
            # 1) Только тренд
            bull_cases = df[df['trend_bull'] == 1]
            logging.info(f"Relax 1 (trend only): {len(bull_cases)}")

        if bull_cases.empty:
            # 2) Только RSI
            bull_cases = df[df['rsi_bull'] == 1]
            logging.info(f"Relax 2 (rsi only): {len(bull_cases)}")

        if bull_cases.empty:
            # 3) Убираем пороги outcome (используем все свечи)
            bull_cases = df
            logging.info("Relax 3: using all candles for probabilities (no filters)")

        # Вычисляем вероятности
        prob_up = (bull_cases['outcome'] == 1).mean() * 100 if not bull_cases.empty else default['up']
        prob_down = (bull_cases['outcome'] == -1).mean() * 100 if not bull_cases.empty else default['down']
        prob_base = max(0, 100 - prob_up - prob_down)

        return {"up": round(prob_up, 1), "base": round(prob_base, 1), "down": round(prob_down, 1)}

    except Exception as e:
        logging.error(f"Ошибка backtest: {e}\n{traceback.format_exc()}")
        return {"up": 50, "base": 30, "down": 20}


def get_onchain_data(symbol: str):
    try:
        api_key = os.getenv('GLASSNODE_API_KEY')
        if not api_key:
            logging.warning("No Glassnode API key, default onchain")
            return {
                'netflow': {'value': 0, 'interpretation': 'N/A'},
                'sopr': {'value': 1.0, 'interpretation': 'N/A'},
                'mvrv': {'value': 0, 'interpretation': 'N/A'},
                'puell': {'value': 0, 'interpretation': 'N/A'}
            }
        symbol_lower = symbol.lower()
        url_netflow = f"https://api.glassnode.com/v1/metrics/transactions/transfers_volume_to_exchanges_mean?api_key={api_key}&a={symbol_lower}&s=365"
        url_sopr = f"https://api.glassnode.com/v1/metrics/indicators/sopr?api_key={api_key}&a={symbol_lower}"
        url_mvrv = f"https://api.glassnode.com/v1/metrics/market/mvrv?api_key={api_key}&a={symbol_lower}"
        url_puell = f"https://api.glassnode.com/v1/metrics/mining/puell_multiple?api_key={api_key}&a={symbol_lower}"

        # Netflow
        resp_netflow = requests.get(url_netflow).json()
        netflow_value = resp_netflow[-1]['v'] if resp_netflow else 0
        netflow_interp = 'Приток (медвежий сигнал)' if netflow_value > 0 else 'Отток (бычий сигнал)' if netflow_value < 0 else 'Нейтральный'

        # SOPR
        resp_sopr = requests.get(url_sopr).json()
        sopr_value = resp_sopr[-1]['v'] if resp_sopr else 1.0
        sopr_interp = 'Вера в рост (бычий сигнал)' if sopr_value > 1 else 'Паника (медвежий сигнал)' if sopr_value < 1 else 'Нейтральный'

        # MVRV
        resp_mvrv = requests.get(url_mvrv).json()
        mvrv_value = resp_mvrv[-1]['v'] if resp_mvrv else 0
        mvrv_interp = 'Бычий' if mvrv_value < 1 else 'Медвежий' if mvrv_value > 3.5 else 'Нейтральный'

        # Puell
        resp_puell = requests.get(url_puell).json()
        puell_value = resp_puell[-1]['v'] if resp_puell else 0
        puell_interp = 'Бычий' if puell_value < 0.5 else 'Медвежий' if puell_value > 4 else 'Нейтральный'

        return {
            'netflow': {'value': netflow_value, 'interpretation': netflow_interp},
            'sopr': {'value': sopr_value, 'interpretation': sopr_interp},
            'mvrv': {'value': mvrv_value, 'interpretation': mvrv_interp},
            'puell': {'value': puell_value, 'interpretation': puell_interp}
        }
    except Exception as e:
        logging.error(f"Ошибка onchain: {e}")
        return {
            'netflow': {'value': 0, 'interpretation': 'N/A'},
            'sopr': {'value': 1.0, 'interpretation': 'N/A'},
            'mvrv': {'value': 0, 'interpretation': 'N/A'},
            'puell': {'value': 0, 'interpretation': 'N/A'}
        }

def merge_metrics(computed: dict, llm_metrics: dict) -> dict:
    """
    Возвращает словарь метрик: приоритет — computed (локальные вычисления).
    Если у computed нет значения (None / nan / missing), но есть в llm_metrics — берем из llm_metrics.
    Работает рекурсивно для вложенных структур (например vip_metrics with series).
    """
    import math
    def is_missing(v):
        if v is None: return True
        if isinstance(v, float) and (math.isnan(v) or math.isinf(v)): return True
        return False

    result = {}
    keys = set()
    if isinstance(computed, dict): keys.update(computed.keys())
    if isinstance(llm_metrics, dict): keys.update(llm_metrics.keys())

    for k in keys:
        cv = computed.get(k) if isinstance(computed, dict) else None
        lv = llm_metrics.get(k) if isinstance(llm_metrics, dict) else None
        if isinstance(cv, dict) and isinstance(lv, dict):
            result[k] = merge_metrics(cv, lv)
        else:
            if not is_missing(cv):
                result[k] = cv
            else:
                result[k] = lv
    return result

# Функция для получения данных (с derive)

# --------------------------
#  Помощник: парсинг JSON из текста LLM
# --------------------------
def parse_llm_json_from_text(text: str) -> dict:
    """
    Ищет блок ```JSON ... ``` или ```json ... ``` в тексте и возвращает Python dict.
    Если такого блока нет — пытается распарсить всю строку как JSON.
    Возвращает {} при ошибке парсинга.
    """
    if not text:
        return {}
    # ищем ```JSON ... ```
    m = re.search(r"```(?:JSON|json)\s*(\{.*?\})\s*```", text, flags=re.S)
    if not m:
        # возможно LLM вернул json без ``` — постараемся найти первый { ... } большой блок
        m2 = re.search(r"(\{[\s\S]*\})", text, flags=re.S)
        block = m2.group(1) if m2 else text.strip()
    else:
        block = m.group(1)
    try:
        parsed = json.loads(block)
        return parsed if isinstance(parsed, dict) else {}
    except Exception as e:
        logging.warning(f"parse_llm_json_from_text: json.loads failed: {e}. Trying fallback len(block)={len(block)}")
        # fallback: попытаемся исправить одинарные кавычки -> двойные, убрать комментарии и т.д.
        try:
            cleaned = re.sub(r"//.*?$", "", block, flags=re.M)  # remove //comments
            cleaned = re.sub(r"/\*[\s\S]*?\*/", "", cleaned)  # remove /* ... */
            cleaned = cleaned.replace("'", '"')
            parsed = json.loads(cleaned)
            return parsed if isinstance(parsed, dict) else {}
        except Exception as e2:
            logging.error(f"parse_llm_json_from_text fallback failed: {e2}")
            return {}

# --------------------------
#  Помощник: нормализация kline -> pandas.DataFrame
# --------------------------
def normalize_kline_to_df(kline):
    """
    kline: list-of-lists [[ts_ms, o,h,l,c,v], ...] or DataFrame
    Returns DataFrame with columns ['dt','open','high','low','close','volume'] and dt as datetime
    """
    if kline is None:
        return None
    if isinstance(kline, pd.DataFrame):
        df = kline.copy()
        # try to normalize column names
        if 'ts' in df.columns:
            df['dt'] = pd.to_datetime(df['ts'], unit='ms')
        elif 'dt' not in df.columns and 'timestamp' in df.columns:
            df['dt'] = pd.to_datetime(df['timestamp'], unit='ms')
        elif 'dt' not in df.columns and 'time' in df.columns:
            df['dt'] = pd.to_datetime(df['time'], unit='ms')
        elif 'dt' not in df.columns:
            # if index is datetime-like
            try:
                df['dt'] = pd.to_datetime(df.index)
            except Exception:
                pass
        # ensure numeric columns exist
        for c in ['open','high','low','close','volume']:
            if c not in df.columns:
                # try common alternatives
                if c == 'volume' and 'vol' in df.columns:
                    df['volume'] = df['vol']
                else:
                    df[c] = np.nan
        df = df[['dt','open','high','low','close','volume']].copy()
        df = df.dropna(subset=['dt']).sort_values('dt').reset_index(drop=True)
        return df
    # assume list of rows
    try:
        # support rows either 6-length [ts,o,h,l,c,v] or dict
        if len(kline) == 0:
            return None
        first = kline[0]
        if isinstance(first, dict):
            # try mapping keys
            records = []
            for r in kline:
                ts = r.get('ts') or r.get('time') or r.get('timestamp') or r.get('t')
                records.append({
                    'dt': pd.to_datetime(int(ts), unit='ms') if ts is not None else None,
                    'open': float(r.get('open', np.nan)),
                    'high': float(r.get('high', np.nan)),
                    'low': float(r.get('low', np.nan)),
                    'close': float(r.get('close', np.nan)),
                    'volume': float(r.get('volume', r.get('vol', np.nan)))
                })
            df = pd.DataFrame(records).dropna(subset=['dt']).sort_values('dt').reset_index(drop=True)
            return df
        else:
            # list-of-lists
            records = []
            for row in kline:
                if len(row) >= 6:
                    ts = int(row[0])
                    o,h,l,c,v = float(row[1]),float(row[2]),float(row[3]),float(row[4]),float(row[5])
                    records.append({'dt': pd.to_datetime(ts, unit='ms'), 'open': o, 'high': h, 'low': l, 'close': c, 'volume': v})
                elif len(row) == 2:
                    ts = int(row[0]); c = float(row[1])
                    records.append({'dt': pd.to_datetime(ts, unit='ms'), 'open': c, 'high': c, 'low': c, 'close': c, 'volume': 0.0})
                else:
                    # unknown shape -> skip
                    continue
            df = pd.DataFrame(records).dropna(subset=['dt']).sort_values('dt').reset_index(drop=True)
            return df
    except Exception as e:
        # fallback
        return None


def _safe_extract_metric_series(metric_obj):
    """Возвращает список float значений из vip_metrics[...] или None."""
    if not isinstance(metric_obj, dict):
        return None
    # try common keys in order
    candidates = []
    for key in ('series','line','hist','values','data'):
        v = metric_obj.get(key)
        if v is not None:
            candidates = v
            break
    if not candidates:
        # single numeric value fallback
        if metric_obj.get('value') is not None:
            try:
                val = float(metric_obj.get('value') or 0.0)
                return list(np.linspace(0, val if val != 0 else 1, 40))
            except Exception:
                return None
        return None
    # now normalize candidates to list of floats
    try:
        # if list of pairs [[ts,val],...]
        if isinstance(candidates, (list, tuple)) and len(candidates) and isinstance(candidates[0], (list, tuple)):
            out = []
            for row in candidates:
                if len(row) >= 2:
                    try:
                        out.append(float(row[1]))
                    except Exception:
                        out.append(np.nan)
                else:
                    try:
                        out.append(float(row[0]))
                    except Exception:
                        out.append(np.nan)
            return out
        # if list of scalars
        if isinstance(candidates, (list, tuple)):
            return [float(x) if x is not None else np.nan for x in candidates]
    except Exception:
        return None
    return None

def compute_vwap(df):
    """Compute VWAP series on history df (returns series aligned with df.index)."""
    if df is None or df.empty or 'volume' not in df.columns or 'close' not in df.columns:
        return None
    vol = df['volume'].astype(float).replace(0, np.nan).fillna(0)
    pv = (df['close'].astype(float) * vol)
    cum_pv = pv.cumsum()
    cum_vol = vol.cumsum().replace(0, np.nan)
    vwap = (cum_pv / cum_vol).fillna(method='ffill').fillna(df['close'])
    return vwap

def compute_rsi(series, period=14):
    """Simple RSI calc returning same-length series (pandas Series)."""
    s = pd.Series(series).astype(float)
    delta = s.diff()
    up = delta.clip(lower=0)
    down = -delta.clip(upper=0)
    ma_up = up.ewm(alpha=1/period, adjust=False).mean()
    ma_down = down.ewm(alpha=1/period, adjust=False).mean().replace(0, 1e-9)
    rs = ma_up / ma_down
    rsi = 100 - (100 / (1 + rs))
    rsi = rsi.fillna(50)
    rsi.index = s.index
    return rsi

def compute_macd(series, fast=12, slow=26, signal=9):
    s = pd.Series(series).astype(float)
    ema_fast = s.ewm(span=fast, adjust=False).mean()
    ema_slow = s.ewm(span=slow, adjust=False).mean()
    macd = ema_fast - ema_slow
    signal_line = macd.ewm(span=signal, adjust=False).mean()
    hist = macd - signal_line
    return macd, signal_line, hist





def parse_forecast_payload(payload, history_df=None, horizon=None):
    """
    Универсальный парсер payload (может быть LLM JSON или market_data).
    Возвращает dict:
      - forecast_df (pd.DataFrame with dt/open/high/low/close/volume)
      - trade_idea (dict)
      - vip_metrics (dict)
      - metrics_to_show (list)
      - x_axis (dict or None)
      - forecast_horizon (dict or None)
      - raw (original payload)
    """
    out = {
        "forecast_df": None,
        "trade_idea": {},
        "vip_metrics": {},
        "metrics_to_show": [],
        "x_axis": None,
        "forecast_horizon": None,
        "raw": payload
    }

    if payload is None:
        # fallback: build forecast from history_df if given
        if history_df is not None:
            last_dt = pd.to_datetime(history_df["dt"].iloc[-1])
            last_price = float(history_df["close"].iloc[-1])
            steps = HORIZON_STEPS.get(horizon, 12)
            # infer freq
            if horizon and horizon.endswith("m"):
                freq = f"{int(horizon[:-1])}min"
            elif horizon and horizon.endswith("h"):
                freq = f"{int(horizon[:-1])}h"
            elif horizon and horizon.endswith("d"):
                freq = "1D"
            else:
                freq = "1D"
            f_times = pd.date_range(start=last_dt + pd.Timedelta(minutes=1), periods=steps, freq=freq)
            rows = [[t, last_price*0.995, last_price*1.005, last_price*0.993, last_price, 0.0] for t in f_times]
            out["forecast_df"] = pd.DataFrame(rows, columns=["dt","open","high","low","close","volume"])
        return out

    # If payload is already a dict (LLM JSON or market_data)
    if isinstance(payload, dict):
        # copy straightforward fields
        out["trade_idea"] = payload.get("trade_idea", {}) or {}
        out["vip_metrics"] = payload.get("vip_metrics", {}) or {}
        mts = payload.get("metrics_to_show", []) or []
        if isinstance(mts, str):
            mts = [mts]
        out["metrics_to_show"] = list(mts)
        out["x_axis"] = payload.get("x_axis", None)
        out["forecast_horizon"] = payload.get("forecast_horizon", None)

        # 1) try payload['forecast']
        fc = payload.get("forecast") or payload.get("forecast_series") or payload.get("forecast_data")
        if fc is not None:
            # if fc is dict {'type':..., 'data':...}
            if isinstance(fc, dict) and fc.get("type") and fc.get("data"):
                ftype = fc.get("type")
                data = fc.get("data", [])
                # OHLCV
                if ftype == "ohlcv":
                    try:
                        rows = []
                        for r in data:
                            ts = int(r[0]); dt = pd.to_datetime(ts, unit='ms')
                            o = float(r[1]); h = float(r[2]); l = float(r[3]); c = float(r[4])
                            v = float(r[5]) if len(r) > 5 else 0.0
                            rows.append([dt,o,h,l,c,v])
                        if rows:
                            out["forecast_df"] = pd.DataFrame(rows, columns=["dt","open","high","low","close","volume"])
                            return out
                    except Exception:
                        pass
                # close_series
                if ftype == "close_series":
                    try:
                        rows = []
                        for r in data:
                            ts = int(r[0]); dt = pd.to_datetime(ts, unit='ms'); c = float(r[1])
                            rows.append([dt,c])
                        if rows:
                            df = pd.DataFrame(rows, columns=["dt","close"])
                            df["open"] = df["close"].shift(1).fillna(df["close"]*0.995)
                            df["high"] = df[["open","close"]].max(axis=1) * 1.001
                            df["low"] = df[["open","close"]].min(axis=1) * 0.999
                            df["volume"] = 0.0
                            out["forecast_df"] = df[["dt","open","high","low","close","volume"]]
                            return out
                    except Exception:
                        pass
            # if fc is list-of-lists
            if isinstance(fc, list) and len(fc) and isinstance(fc[0], (list,tuple)):
                # decide by length of inner lists
                if len(fc[0]) >= 6:
                    try:
                        rows = []
                        for r in fc:
                            ts = int(r[0]); dt = pd.to_datetime(ts, unit='ms')
                            o = float(r[1]); h = float(r[2]); l = float(r[3]); c = float(r[4]); v = float(r[5])
                            rows.append([dt,o,h,l,c,v])
                        out["forecast_df"] = pd.DataFrame(rows, columns=["dt","open","high","low","close","volume"])
                        return out
                    except Exception:
                        pass
                else:
                    try:
                        rows = []
                        for r in fc:
                            ts = int(r[0]); dt = pd.to_datetime(ts, unit='ms'); c = float(r[1])
                            rows.append([dt,c])
                        df = pd.DataFrame(rows, columns=["dt","close"])
                        df["open"] = df["close"].shift(1).fillna(df["close"]*0.995)
                        df["high"] = df[["open","close"]].max(axis=1) * 1.001
                        df["low"] = df[["open","close"]].min(axis=1) * 0.999
                        df["volume"] = 0.0
                        out["forecast_df"] = df[["dt","open","high","low","close","volume"]]
                        return out
                    except Exception:
                        pass

        # 2) if no forecast, try to create forecast from payload.kline_data (if present)
        if out["forecast_df"] is None:
            kd = payload.get("kline_data") or payload.get("history") or payload.get("ohlcv")
            if kd is not None:
                hist_df = normalize_kline_to_df(kd)
                if hist_df is not None and len(hist_df) >= 1:
                    # create a simple flat close_series forecast from last price
                    last_dt = hist_df["dt"].iloc[-1]
                    last_price = float(hist_df["close"].iloc[-1])
                    steps = HORIZON_STEPS.get(horizon, 12)
                    # infer freq from payload forecast_horizon if exists
                    freq = "1D"
                    f_times = pd.date_range(start=last_dt + pd.Timedelta(minutes=1), periods=steps, freq=freq)
                    rows = [[t, last_price*0.995, last_price*1.005, last_price*0.993, last_price, 0.0] for t in f_times]
                    out["forecast_df"] = pd.DataFrame(rows, columns=["dt","open","high","low","close","volume"])
                    return out

        # 3) If still none, fallback to history_df if provided
        if out["forecast_df"] is None and history_df is not None:
            hist_df = history_df.copy()
            if "dt" not in hist_df.columns:
                # try ts
                if "ts" in hist_df.columns:
                    hist_df["dt"] = pd.to_datetime(hist_df["ts"], unit='ms')
            if "dt" in hist_df.columns:
                last_dt = hist_df["dt"].iloc[-1]
                last_price = float(hist_df["close"].iloc[-1])
                steps = HORIZON_STEPS.get(horizon, 12)
                if horizon and horizon.endswith("m"):
                    freq = f"{int(horizon[:-1])}min"
                elif horizon and horizon.endswith("h"):
                    freq = f"{int(horizon[:-1])}h"
                elif horizon and horizon.endswith("d"):
                    freq = "1D"
                else:
                    freq = "1D"
                f_times = pd.date_range(start=last_dt + pd.Timedelta(minutes=1), periods=steps, freq=freq)
                rows = [[t, last_price*0.995, last_price*1.005, last_price*0.993, last_price, 0.0] for t in f_times]
                out["forecast_df"] = pd.DataFrame(rows, columns=["dt","open","high","low","close","volume"])
                return out

    # if nothing found, return out with forecast_df None
    return out

def _shorten_text_words(text, max_words=7):
    if not text:
        return ""
    words = str(text).split()
    if len(words) <= max_words:
        return " ".join(words)
    return " ".join(words[:max_words]).rstrip(".,;:") + "..."

# --------------------------
#  Обновлённая get_market_data (копипаст-автономная версия для вставки)
# --------------------------
async def get_market_data(
    symbol: str,
    timeframe: str,
    limit: int = 365,
    is_vip: bool = False,
    category: str = 'linear'
) -> dict | None:
    """
    Возвращает: {
      'symbol', 'current_price', 'price_change_24h_percent', 'open_interest_value',
      'funding_rate', 'kline_data' (DataFrame), 'timeframe', 'onchain', 'macro',
      'backtest_probs', ... (raw technical metrics),
      'vip_metrics' (normalized), 'metrics_to_show' (list)
    }
    Использует: get_kline_data, backtest_probabilities, calculate_advanced_metrics, get_onchain_data, get_macro_data
    """
    try:
        raw_kline = await get_kline_data(symbol, timeframe, limit)
        if not raw_kline:
            logging.warning(f"Incomplete or insufficient market data for {symbol} / {timeframe}")
            return None

        df = normalize_kline_to_df(raw_kline)

        # --- ticker (robust) ---
        async with httpx.AsyncClient(timeout=20.0) as session:
            try:
                params_ticker = {"category": category, "symbol": symbol}
                response_ticker = await session.get(f"{BASE_URL}/v5/market/tickers", params=params_ticker)
                data_ticker = response_ticker.json()
            except Exception as e:
                logging.warning(f"Ticker fetch failed for {symbol}: {e}")
                data_ticker = {}

        ticker = data_ticker.get("result", {}).get("list", [{}])[0] if data_ticker else {}
        try:
            current_price = float(ticker.get('lastPrice', df['close'].iloc[-1]))
        except Exception:
            current_price = float(df['close'].iloc[-1]) if not df.empty else 0.0

        raw_pct = None
        for key in ('price24hPcnt', 'price24hPChg', 'price24hPcnt', 'price_24h_pcnt', 'price24hPcnt'):
            if key in ticker and ticker.get(key) not in (None, ""):
                raw_pct = ticker.get(key)
                break
        if raw_pct is None:
            price_change_24h_percent = 0.0
        else:
            try:
                price_change_24h_percent = float(raw_pct) * 100
            except Exception:
                try:
                    price_change_24h_percent = float(str(raw_pct).strip().strip('%'))
                except:
                    price_change_24h_percent = 0.0

        open_interest_value = float(ticker.get('openInterestValue', 0)) if 'openInterestValue' in ticker else 0.0
        funding_rate = float(ticker.get('fundingRate', 0)) * 100 if 'fundingRate' in ticker else 0.0

        base_symbol = symbol.rstrip("USDT").rstrip("USDC").lower() if symbol.endswith(("USDT", "USDC")) else symbol.lower()
        onchain = get_onchain_data(base_symbol) if 'get_onchain_data' in globals() else {}
        macro = get_macro_data(base_symbol) if 'get_macro_data' in globals() else {}

        # backtest & advanced metrics (use raw_kline/list for compatibility with existing functions)
        backtest = await backtest_probabilities(raw_kline, symbol, timeframe) if 'backtest_probabilities' in globals() else None
        tech_metrics = calculate_advanced_metrics(raw_kline) if 'calculate_advanced_metrics' in globals() else {}

        # --- normalize local vip_metrics in LLM-friendly shape ---
        local_vip = {}
        # rsi, macd, vwap, atr, ema_20, ema_50, volatility_percent, open_interest, funding_rate
        if 'rsi' in tech_metrics:
            r = tech_metrics['rsi']
            if isinstance(r, (int, float)):
                local_vip['rsi'] = {'value': float(r)}
            elif isinstance(r, dict):
                local_vip['rsi'] = r
        if 'macd' in tech_metrics:
            local_vip['macd'] = tech_metrics['macd']
        for key in ('vwap','atr','ema_20','ema_50','volatility_percent','open_interest','funding_rate'):
            if key in tech_metrics and tech_metrics[key] is not None:
                local_vip[key] = tech_metrics[key]
        if backtest is not None:
            if isinstance(backtest, dict):
                val = backtest.get('win_rate', backtest.get('value', None))
                try:
                    local_vip['backtest_probs'] = {'value': float(val)}
                except:
                    local_vip['backtest_probs'] = {'value': None}
                if 'series' in backtest:
                    local_vip['backtest_probs']['series'] = backtest['series']
            else:
                try:
                    local_vip['backtest_probs'] = {'value': float(backtest)}
                except:
                    pass

        metrics_list = list(local_vip.keys())[:6]

        market_data = {
            'symbol': symbol,
            'current_price': current_price,
            'price_change_24h_percent': price_change_24h_percent,
            'open_interest_value': open_interest_value,
            'funding_rate': funding_rate,
            'kline_data': df,
            'timeframe': timeframe,
            'onchain': onchain,
            'macro': macro,
            'backtest_probs': backtest,
            **tech_metrics,
            'vip_metrics': local_vip,
            'metrics_to_show': metrics_list,
        }
        return market_data

    except Exception as e:
        logging.exception(f"get_market_data error for {symbol}:{timeframe} -> {e}")
        return None


# --------------------------
#  apply_x_format (принимает cfg из LLM x_axis при наличии)
# --------------------------
def apply_x_format(ax, horizon_label, forecast_start_dt=None, x_axis_cfg=None):
    """
    Formats x-axis of ax. Accepts x_axis_cfg from LLM or fallback based on horizon_label.
    x_axis_cfg example: {"hist_format":"%H:%M","forecast_format":"%H:%M","tick_interval":{"unit":"minutes","value":5}}
    """
    # Default formats per horizon
    default = {
        "5m": ("%H:%M", "%H:%M"),
        "1h": ("%d %b\n%H:%M", "%d %b\n%H:%M"),
        "1d": ("%d %b\n%Y", "%d %b\n%Y"),
        "1w": ("%d %b\n%Y","%d %b\n%Y"),
        "1m": ("%d %b\n%Y","%d %b\n%Y"),
        "6m": ("%b %Y","%b %Y"),
        "1y": ("%b %Y","%b %Y")
    }
    try:
        if x_axis_cfg and isinstance(x_axis_cfg, dict):
            fmt = x_axis_cfg.get('hist_format') or default.get(horizon_label, default["1d"])[0]
        else:
            fmt = default.get(horizon_label, default["1d"])[0]
    except Exception:
        fmt = default["1d"][0]
    ax.xaxis.set_major_formatter(mdates.DateFormatter(fmt))
    # auto rotate
    for label in ax.get_xticklabels():
        label.set_rotation(0)
        label.set_color(COLORS["secondary_text"])

def rounded_title(ax, text, fontsize=11):
    """Динамическая pill-заголовок (размер под текст)."""
    trans = ax.transAxes
    # width proportional to len, but limited
    width = max(0.15, min(0.6, 0.03 * len(text)))
    height = 0.065
    bbox = FancyBboxPatch((0.01, 0.92), width, height, transform=trans,
                         boxstyle="round,pad=0.02", facecolor='#0b1220', edgecolor='none', alpha=0.95, zorder=6)
    ax.add_patch(bbox)
    ax.text(0.02, 0.92 + 0.01, text, transform=trans, color=COLORS["text"], fontsize=fontsize, va='top', zorder=7)

def draw_rounded_title(ax, text, fontsize=11, pad_y=0.02):
    """
    Draws rounded rectangle behind text (inside axis coords).
    Width is adaptive by text length.
    """
    trans = ax.transAxes
    # approximate width by characters
    width = min(0.64, max(0.14, 0.02 * len(text)))
    height = 0.065
    x0 = 0.01
    y0 = 1 - height - pad_y
    bbox = FancyBboxPatch((x0, y0), width, height, transform=trans, boxstyle="round,pad=0.02",
                          linewidth=0, facecolor="#0b1220", alpha=0.95, zorder=8)
    ax.add_patch(bbox)
    ax.text(x0 + 0.01, y0 + 0.01, text, transform=trans, color="#E6F0FF", fontsize=fontsize, va='top', zorder=9)


def aggregate_kline(kline: list, period: int, freq: str = 'M') -> list:
    """
    Aggregate kline to period-month bars.
    kline: list of [timestamp_ms, open, high, low, close, volume(, turnover)]
    period: number of months to aggregate (1 => monthly, 6 => 6M, 12 => yearly-ish)
    freq: 'M' expected for month-based aggregation
    """
    if not kline:
        logging.warning("No kline data to aggregate.")
        return []

    try:
        num_cols = len(kline[0])
        if num_cols >= 6:
            cols = ["timestamp", "open", "high", "low", "close", "volume"]
        else:
            raise ValueError("Unexpected kline width")

        df = pd.DataFrame(kline, columns=cols + (["turnover"] if num_cols >= 7 else []))
        df['timestamp'] = pd.to_datetime(df['timestamp'].astype(int), unit='ms')
        df.set_index('timestamp', inplace=True)
        df = df.astype(float)

        # monthly resample, then group every `period` months
        monthly = df.resample('ME').agg({'open':'first','high':'max','low':'min','close':'last','volume':'sum'})
        if period > 1:
            grouped = monthly.groupby(pd.Grouper(freq=f'{period}M')).agg({'open':'first','high':'max','low':'min','close':'last','volume':'sum'})
        else:
            grouped = monthly

        grouped = grouped.dropna(how='all')
        grouped = grouped.reset_index()
        grouped['timestamp'] = (grouped['timestamp'].astype('int64') // 10**6).astype(int)
        return grouped[['timestamp','open','high','low','close','volume']].values.tolist()
    except Exception as e:
        logging.error(f"Aggregate kline error: {e}")
        return []

async def get_derivatives_info(session, symbol: str) -> dict | None:
    """Получает данные по открытому интересу и ставке финансирования."""
    try:
        response = await session.get(
            f"{BASE_URL}/v5/market/tickers",
            params={"category": "linear", "symbol": symbol}
        )
        response.raise_for_status()
        data = response.json()
        if data.get("retCode") == 0 and data["result"]["list"]:
            derivatives_data = data["result"]["list"][0]
            return {
                "open_interest_value": float(derivatives_data.get("openInterestValue", 0)),
                "funding_rate": float(derivatives_data.get("fundingRate", 0)) * 100,
                "last_price": float(derivatives_data.get("lastPrice", 0)),
                "price_24h_pcnt": float(derivatives_data.get("price24hPcnt", 0)) * 100
            }
        return None
    except httpx.HTTPStatusError as e:
        print(f"Bybit API error (derivatives): {e.response.status_code} - {e.response.text}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred in get_derivatives_info: {e}")
        return None

# --- НОВЫЕ ФУНКЦИИ-СИМУЛЯТОРЫ ON-CHAIN ДАННЫХ ---
# bybit_api.py (БЛОК: get_exchange_netflow и get_lth_sopr - заменить полностью)
# bybit_api.py (БЛОК: get_exchange_netflow и get_lth_sopr - заменить полностью)
symbol_to_id = {
    'BTC': 'bitcoin',
    'ETH': 'ethereum',
    'SOL': 'solana',
    'BTS': 'bitshares',  # Добавлено для BitShares
    'XRP': 'ripple',
    'ADA': 'cardano',
    'BNB': 'binancecoin',
    'DOT': 'polkadot',
    'DOGE': 'dogecoin',
    'LTC': 'litecoin',
    'LINK': 'chainlink',
    'AVAX': 'avalanche-2',
    'MATIC': 'matic-network',
    'SHIB': 'shiba-inu',
    'UNI': 'uniswap',
    'TRX': 'tron',
    'ATOM': 'cosmos',
    'XLM': 'stellar',
    'NEAR': 'near',
    'FIL': 'filecoin',
    'VET': 'vechain',
    'ICP': 'internet-computer',
    'EOS': 'eos',
    'THETA': 'theta-token',
    'AAVE': 'aave',
    'MKR': 'maker',
    'COMP': 'compound-coin',
    'ALGO': 'algorand',
    'XTZ': 'tezos',
    'KSM': 'kusama',
    'EGLD': 'elrond-erd-2',
    'AXS': 'axie-infinity',
    'GRT': 'the-graph',
    'STX': 'stacks',
    'HBAR': 'hedera-hashgraph',
    'QNT': 'quant-network',
    'RNDR': 'render-token',
    'FTM': 'fantom',
    'SAND': 'the-sandbox',
    'MANA': 'decentraland',
    'APE': 'apecoin',
    'CHZ': 'chiliz',
    'CRV': 'curve-dao-token',
    'DYDX': 'dydx',
    '1INCH': '1inch',
    'ENJ': 'enjincoin',
    'SNX': 'havven',
    'BAT': 'basic-attention-token',
    'ZRX': '0x',
    'YFI': 'yearn-finance',
    'BAL': 'balancer',
    'UMA': 'uma',
    'KNC': 'kyber-network-crystal',
    'BAND': 'band-protocol',
    'STORJ': 'storj',
    'REN': 'republic-protocol',
    'LRC': 'loopring',
    'OCEAN': 'ocean-protocol',
    'NMR': 'numeraire',
    'ANKR': 'ankr',
    'RSR': 'reserve-rights-token',
    'SKL': 'skale',
    'CELR': 'celer-network',
    'HOT': 'holotoken',
    'CHR': 'chromaway',
    'DENT': 'dent',
    'REEF': 'reef-finance',
    'MTL': 'metal',
    'STMX': 'storm',
    'OGN': 'origin-protocol',
    'FET': 'fetch-ai',
    'CVC': 'civic',
    'SFP': 'safepal',
    'ALPHA': 'alpha-finance',
    'ZEN': 'horizen',
    'NKN': 'nkn',
    'CTK': 'certik',
    'ALICE': 'my-neighbor-alice',
    'FLM': 'flamingo-finance',
    'DODO': 'dodo',
    'BADGER': 'badger-dao',
    'OM': 'mantra-dao',
    'ORN': 'orion-protocol',
    'UTK': 'utrust',
    'ACM': 'actinium',
    'PHA': 'phala-network',
    'BOND': 'barnbridge',
    'FIS': 'stafi',
    'POLS': 'polkastarter',
    'FARM': 'harvest-finance',
    'MLN': 'enzyme',
    'GHST': 'aavegotchi',
    'BURGER': 'burger-swap',
    'JUV': 'juventus-fan-token',
    'PSG': 'paris-saint-germain-fan-token',
    'ASR': 'as-roma-fan-token',
    'ATM': 'atletico-madrid-fan-token',
    'BAR': 'fc-barcelona-fan-token',
    'CITY': 'manchester-city-fan-token',
    'GAL': 'galatasaray-fan-token',
    'ACM': 'ac-milan-fan-token',
    # Добавьте больше популярных монет по необходимости
}

async def get_exchange_netflow(symbol: str) -> dict:
    try:
        coin_id = get_coin_id(symbol)
        if not coin_id:
            return {"value": 0, "interpretation": "N/A"}
        data = cg.get_coin_by_id(coin_id)
        total_volume_usd = data.get('market_data', {}).get('total_volume', {}).get('usd', 0)
        circulating_supply = data.get('market_data', {}).get('circulating_supply', 0)
        flow = total_volume_usd - circulating_supply
        interpretation = "Приток (медвежий сигнал)" if flow > 0 else "Отток (бычий сигнал)"
        return {"value": flow, "interpretation": interpretation}
    except Exception as e:
        logging.error(f"Netflow error: {e}")
        return {"value": 0, "interpretation": "N/A"}

async def get_lth_sopr(symbol: str) -> dict:
    try:
        coin_id = get_coin_id(symbol)
        if not coin_id:
            return {"value": 1.0, "interpretation": "N/A"}
        data = cg.get_coin_market_chart_by_id(id=coin_id, vs_currency='usd', days=30)
        prices = data.get('prices', [])
        if prices:
            avg_price = sum(p[1] for p in prices) / len(prices)
            sopr = avg_price / prices[-1][1]
            interpretation = "Фиксация прибыли (давление продаж)" if sopr > 1.02 else "Вера в рост (бычий сигнал)"
            return {"value": sopr, "interpretation": interpretation}
        return {"value": 1.0, "interpretation": "N/A"}
    except Exception as e:
        logging.error(f"SOPR error: {e}")
        return {"value": 1.0, "interpretation": "N/A"}

# --- КОНЕЦ НОВЫХ ФУНКЦИЙ ---


def calculate_advanced_metrics(kline_data: list) -> dict:
    if not kline_data or len(kline_data) < 2:
        return {
            "atr": 0,
            "volatility_percent": 0,
            "ema_20": 0,
            "ema_50": 0,
            "trend_condition": "Нейтральный",
            "rsi": 50,
            "bollinger_high": 0,
            "bollinger_low": 0,
            "support_level": 0,
            "resistance_level": 0,
            "macd_line": 0,
            "signal_line": 0,
            "macd_trend": "Нейтральный (недостаточно данных)",
            "vwap": 0
        }

    df = pd.DataFrame(kline_data, columns=["timestamp", "open", "high", "low", "close", "volume", "turnover"])
    df['timestamp'] = pd.to_numeric(df['timestamp'], errors='coerce')
    df = df.dropna(subset=['timestamp'])
    df['timestamp'] = pd.to_numeric(df['timestamp'], errors='coerce')
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df.set_index('timestamp', inplace=True)
    df = df.astype(float).sort_index()
    df = df.dropna(subset=['high', 'low', 'close', 'volume'])

    if len(df) < 2:
        return {
            "atr": 0,
            "volatility_percent": 0,
            "ema_20": df['close'].iloc[-1] if not df.empty else 0,
            "ema_50": df['close'].iloc[-1] if not df.empty else 0,
            "trend_condition": "Нейтральный",
            "rsi": 50,
            "bollinger_high": df['close'].iloc[-1] if not df.empty else 0,
            "bollinger_low": df['close'].iloc[-1] if not df.empty else 0,
            "support_level": df['low'].min() if not df.empty else 0,
            "resistance_level": df['high'].max() if not df.empty else 0,
            "macd_line": 0,
            "signal_line": 0,
            "macd_trend": "Нейтральный (недостаточно данных)",
            "vwap": df['close'].iloc[-1] if not df.empty else 0
        }

    len_df = len(df)
    last_price = df['close'].iloc[-1]

    # Ensure lengths <= len_df
    atr_length = max(1, min(14, len_df))
    atr = ta.atr(high=df['high'], low=df['low'], close=df['close'], length=atr_length)
    atr_last = atr.iloc[-1] if atr is not None and not atr.empty else 0
    volatility_pct = (atr_last / last_price) * 100 if last_price != 0 else 0

    ema20_length = max(1, min(20, len_df))
    ema_20 = ta.ema(close=df['close'], length=ema20_length).iloc[-1] if ema20_length >= 1 else last_price

    ema50_length = max(1, min(50, len_df))
    ema_50 = ta.ema(close=df['close'], length=ema50_length).iloc[-1] if ema50_length >= 1 else last_price

    trend_condition = "Бычий" if ema_20 > ema_50 else "Медвежий"

    rsi_length = max(1, min(14, len_df))
    rsi = ta.rsi(close=df['close'], length=rsi_length).iloc[-1] if rsi_length >= 1 else 50

    bb_length = max(1, min(20, len_df))
    bb_std = 2.0  # Fixed
    bb = ta.bbands(close=df['close'], length=bb_length, std=bb_std)
    if bb is not None and not bb.empty:
        bb_upper_col = f'BBU_{bb_length}_{bb_std}'
        bb_lower_col = f'BBL_{bb_length}_{bb_std}'
        bb_high = bb[bb_upper_col].iloc[-1] if bb_upper_col in bb else last_price
        bb_low = bb[bb_lower_col].iloc[-1] if bb_lower_col in bb else last_price
    else:
        bb_high = last_price
        bb_low = last_price

    macd_fast = max(1, min(12, len_df))
    macd_slow = max(macd_fast + 1, min(26, len_df))  # Ensure slow > fast and <= len_df
    macd_signal = max(1, min(9, len_df))
    macd = ta.macd(close=df['close'], fast=macd_fast, slow=macd_slow, signal=macd_signal)
    if macd is not None and not macd.empty:
        macd_col = f'MACD_{macd_fast}_{macd_slow}_{macd_signal}'
        signal_col = f'MACDs_{macd_fast}_{macd_slow}_{macd_signal}'
        macd_line = macd[macd_col].iloc[-1] if macd_col in macd else 0
        signal_line = macd[signal_col].iloc[-1] if signal_col in macd else 0
    else:
        macd_line = 0
        signal_line = 0
    macd_trend = "Бычий (MACD > Signal)" if macd_line > signal_line else "Медвежий (MACD < Signal)"

    vwap_length = max(1, min(14, len_df))
    try:
        vwap = ta.vwap(high=df['high'], low=df['low'], close=df['close'], volume=df['volume'], length=vwap_length).iloc[-1]
    except Exception as e:
        logging.error(f"VWAP calculation error: {e}")
        vwap = last_price

    recent_period = df.tail(min(30, len_df))
    support = recent_period['low'].min() if not recent_period.empty else 0
    resistance = recent_period['high'].max() if not recent_period.empty else 0

    last_candle_open = df['open'].iloc[-1]
    last_candle_close = df['close'].iloc[-1]
    last_candle_change_percent = 0
    if last_candle_open != 0:
        last_candle_change_percent = ((last_candle_close - last_candle_open) / last_candle_open) * 100

    return {
        "atr": atr_last,
        "volatility_percent": volatility_pct,
        "ema_20": ema_20,
        "ema_50": ema_50,
        "trend_condition": trend_condition,
        "rsi": rsi,
        "bollinger_high": bb_high,
        "bollinger_low": bb_low,
        "support_level": support,
        "resistance_level": resistance,
        "macd_line": macd_line,
        "signal_line": signal_line,
        "macd_trend": macd_trend,
        "vwap": vwap,
        "last_candle_change_percent": last_candle_change_percent,  # <-- ДОБАВЬ ЭТУ СТРОКУ В СЛОВАРЬ
        "price_change_24h_percent": last_candle_change_percent
    }



# plot_chart module
# Версия: 1.0 (финальная версия по ТЗ)
# Дата: 2025-09-24
#
# Функция plot_chart рисует прогнозный блок (свечи) + историю + RSI + VIP-карточки метрик,
# и в верхнем правом углу показывает компактную Action-карточку с торговой идеей.
# Формат входных данных: JSON (LLM) + исторический DataFrame (OHLCV).


from typing import Dict, Any, Optional, List, Tuple, Union
import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.patches import FancyBboxPatch, Rectangle
from matplotlib.ticker import FuncFormatter
from datetime import datetime, timedelta, timezone

# ---------------------------------------------------------------------
#  Конфигурация палитр / размеры / горизонты (взято из варианта 6)
# ---------------------------------------------------------------------

# Цвета и константы (адаптируйте под ваш файл COLORS / FIGSIZE)
COLORS = {
    "bg": "#0f172a",
    "panel_bg": "#0b1220",  # чуть светлее для панелей
    "text": "#E6F0FF",
    "secondary_text": "#9CA3AF",
    "forecast": "#60A5FA",
    "bull": "#22C55E",
    "bear": "#EF4444",
    "vip_accent": "#86EFAC",
    "ema20": "#3B82F6",
    "ema50": "#F97316",
    "profit": "#10B981",
    "neutral": "#6B7280",
    "risk": "#EF4444",
    "grid": "#1f2937"
}


# horizon settings (main guidance from ТЗ)
HORIZON_SETTINGS = {
    "5m":  {"hist_periods": 48,  "forecast_periods": 12, "rsi_period": 7,  "nf": 0.12, "x_fmt_hist": "%H:%M",            "x_fmt_fore": "%H:%M"},
    "1h":  {"hist_periods": 72,  "forecast_periods": 24, "rsi_period": 7,  "nf": 0.18, "x_fmt_hist": "%d %b\n%H:%M",     "x_fmt_fore": "%H:%M\n%d %b"},
    "1d":  {"hist_periods": 180, "forecast_periods": 14, "rsi_period": 14, "nf": 0.28, "x_fmt_hist": "%d %b",           "x_fmt_fore": "%d %b"},
    "1w":  {"hist_periods": 156, "forecast_periods": 12, "rsi_period": 14, "nf": 0.33, "x_fmt_hist": "%d %b\n%Y",      "x_fmt_fore": "%d %b\n%Y"},
    "1m":  {"hist_periods": 200, "forecast_periods": 30, "rsi_period": 14, "nf": 0.33, "x_fmt_hist": "%d %b\n%Y",      "x_fmt_fore": "%d %b\n%Y"},
    "6m":  {"hist_periods": 260, "forecast_periods": 26, "rsi_period": 14, "nf": 0.40, "x_fmt_hist": "%b %Y",         "x_fmt_fore": "%b %Y"},
    "1y":  {"hist_periods": 240, "forecast_periods": 12, "rsi_period": 14, "nf": 0.45, "x_fmt_hist": "%b %Y",         "x_fmt_fore": "%b %Y"},
}

HORIZON_STEPS = {"5m": 12, "1h": 24, "1d": 14, "1w": 12, "1m": 30, "6m": 26, "1y": 12}

# default figure sizes
FIGSIZE_STD = (14, 9)
FIGSIZE_VIP = (20, 11)

try:
    COLORS
except NameError:
    COLORS = {
        "bg": "#0f172a",
        "text": "#E6F0FF",
        "secondary_text": "#9CA3AF",
        "forecast": "#60A5FA",
        "bull": "#22C55E",
        "bear": "#EF4444",
        "vip_accent": "#86EFAC",
        "ema20": "#3B82F6",
        "ema50": "#F97316",
        "profit": "#10B981",
        "neutral": "#6B7280",
        "risk": "#EF4444",
        "grid": "#1f2937"
    }

FIGSIZE_STD = (14, 9)
FIGSIZE_VIP = (20, 11)
# ---------------------------------------------------------------------
#  JSON contract validator / parser (expects LLM output in agreed shape)
# ---------------------------------------------------------------------
def parse_forecast_json(raw_json):
    """
    raw_json: dict parsed from LLM (already python dict).
    Normalizes forecast part into DataFrame and returns a dict with keys:
      'forecast_df' (ohlc df),
      'trade_idea',
      'vip_metrics',
      'metrics_to_show',
      'x_axis' and 'forecast_horizon' etc.
    """
    out = {}
    if not isinstance(raw_json, dict):
        return out
    # metrics
    out['trade_idea'] = raw_json.get('trade_idea', {}) or {}
    out['vip_metrics'] = raw_json.get('vip_metrics', {}) or {}
    out['metrics_to_show'] = raw_json.get('metrics_to_show', []) or []
    out['x_axis'] = raw_json.get('x_axis', None)
    out['forecast_horizon'] = raw_json.get('forecast_horizon', None)

    # forecast normalization
    fc = raw_json.get('forecast')
    if not fc:
        out['forecast_df'] = None
        return out
    try:
        if isinstance(fc, dict) and fc.get('type') == 'ohlcv' and isinstance(fc.get('data'), list):
            rows = fc['data']
            recs = []
            for r in rows:
                if len(r) >= 6:
                    ts,o,h,l,c,v = int(r[0]), float(r[1]), float(r[2]), float(r[3]), float(r[4]), float(r[5])
                    recs.append({'dt': pd.to_datetime(ts, unit='ms'), 'open': o, 'high': h, 'low': l, 'close': c, 'volume': v})
                elif len(r) == 2:
                    ts,c = int(r[0]), float(r[1])
                    recs.append({'dt': pd.to_datetime(ts, unit='ms'), 'open': c, 'high': c, 'low': c, 'close': c, 'volume': 0.0})
            out['forecast_df'] = pd.DataFrame(recs).dropna(subset=['dt']).sort_values('dt').reset_index(drop=True)
        elif isinstance(fc, list):
            # legacy: list of [ts, close]
            recs = []
            for r in fc:
                if len(r) >= 2:
                    ts,c = int(r[0]), float(r[1])
                    recs.append({'dt': pd.to_datetime(ts, unit='ms'), 'open': c, 'high': c, 'low': c, 'close': c, 'volume': 0.0})
            out['forecast_df'] = pd.DataFrame(recs).dropna(subset=['dt']).sort_values('dt').reset_index(drop=True)
        elif isinstance(fc, dict) and fc.get('type') == 'close_series' and isinstance(fc.get('data'), list):
            recs = []
            for r in fc['data']:
                ts,c = int(r[0]), float(r[1])
                recs.append({'dt': pd.to_datetime(ts, unit='ms'), 'open': c, 'high': c, 'low': c, 'close': c, 'volume': 0.0})
            out['forecast_df'] = pd.DataFrame(recs).dropna(subset=['dt']).sort_values('dt').reset_index(drop=True)
        else:
            out['forecast_df'] = None
    except Exception:
        out['forecast_df'] = None
    return out


def clamp_rect(left, bottom, width, height):
    """Clamp rectangle to valid 0..1 coords and min sizes."""
    left = max(0.0, min(0.98, float(left)))
    bottom = max(0.0, min(0.98, float(bottom)))
    width = float(width)
    height = float(height)
    # minimal reasonable sizes (in fractions of figure)
    min_w, min_h = 0.04, 0.06
    if width < min_w:
        width = min_w
    if height < min_h:
        height = min_h
    # ensure it fits in [0,1]
    if left + width > 1.0:
        left = max(0.0, 1.0 - width)
    if bottom + height > 1.0:
        bottom = max(0.0, 1.0 - height)
    return left, bottom, width, height

# ---------------------------------------------------------------------
#  Helper plotting utilities
# ---------------------------------------------------------------------
def draw_candles(ax, df, width_factor=0.6, zorder=3, color_up=None, color_down=None):
    """
    Рисует свечи по df с колонками dt, open, high, low, close.
    width_factor — относительная ширина к медианному шагу по времени.
    """
    if df is None or len(df) == 0:
        return
    times = pd.to_datetime(df['dt'])
    x = mdates.date2num(times)
    # compute dx median
    if len(x) > 1:
        dx = np.median(np.diff(x))
    else:
        dx = 0.02
    w = dx * width_factor
    for xi, o, h, l, c in zip(x, df['open'], df['high'], df['low'], df['close']):
        up = (c >= o)
        col = color_up if up else color_down
        # wick
        ax.vlines(xi, l, h, color=col, linewidth=1, zorder=zorder-1)
        # body
        left = xi - w/2
        bottom = min(o, c)
        height = max(abs(c - o), 1e-9)
        rect = Rectangle((left, bottom), w, height, facecolor=col, edgecolor=col, linewidth=0.5, zorder=zorder)
        ax.add_patch(rect)
    # set x-limits nicely
    ax.set_xlim(min(x) - dx, max(x) + dx)


# def clip_label_inside(ax, xdt, yval, text, bgcolor="#0b1220", fontsize=10):
#     """
#     Рисует boxed label у координаты (xdt, yval), автоматически поднимает подпись внутрь холста
#     если она выходит за пределы по Y (чтобы TP/SL не выходили за холст).
#     """
#     ymin, ymax = ax.get_ylim()
#     # clamp y to [ymin + margin, ymax - margin]
#     margin = (ymax - ymin) * 0.02
#     yinside = min(max(yval, ymin + margin), ymax - margin)
#     ax.text(xdt, yinside, f" {text} ", color=COLORS["text"], fontsize=fontsize, va='center', ha='left',
#             bbox=dict(facecolor=bgcolor, alpha=0.92, boxstyle="round,pad=0.12"), zorder=9, clip_on=True)


# ---------------------------------------------------------------------
#  Основная функция plot_chart
# ---------------------------------------------------------------------
# ВСТАВЬТЕ В ВЕРХ ФАЙЛА (импорты)
import io
import textwrap
from datetime import datetime, timezone, timedelta
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyBboxPatch
import matplotlib.dates as mdates

# Цвета и константы (адаптируйте под ваш файл COLORS / FIGSIZE)
COLORS = {
    "bg": "#0f172a",
    "panel_bg": "#111827",          # немного светлее общего фона
    "panel_grid": "#1f2937",
    "text": "#E6F0FF",
    "secondary_text": "#9CA3AF",
    "forecast": "#60A5FA",
    "bull": "#22C55E",
    "bear": "#EF4444",
    "vip_accent": "#86EFAC",
    "ema20": "#3B82F6",
    "ema50": "#F97316",
    "profit": "#10B981",
    "neutral": "#6B7280",
    "risk": "#EF4444",
}
FIGSIZE_STD = (14, 9)
FIGSIZE_VIP = (20, 11)

# --- ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ---

def normalize_kline_to_df(kline):
    """
    Привести kline в DataFrame с колонками ['ts','open','high','low','close','volume','dt'].
    Принимает: list-of-lists, list-of-dicts или pd.DataFrame.
    """
    if kline is None:
        return None
    if isinstance(kline, pd.DataFrame):
        df = kline.copy()
        # нормализуем имена колонок
        for c in ['timestamp','time','ts']:
            if c in df.columns and 'ts' not in df.columns:
                df.rename(columns={c:'ts'}, inplace=True)
        if 'dt' not in df.columns:
            if 'ts' in df.columns:
                df['dt'] = pd.to_datetime(df['ts'], unit='ms', utc=True).dt.tz_convert(None)
            elif 'time' in df.columns:
                df['dt'] = pd.to_datetime(df['time']).dt.tz_convert(None)
        return df
    # list-of-dicts
    if isinstance(kline, (list, tuple)) and len(kline) > 0 and isinstance(kline[0], dict):
        rows = []
        for r in kline:
            ts = None
            if 'ts' in r:
                ts = int(r['ts'])
            elif 'time' in r and isinstance(r['time'], (int, float)):
                ts = int(r['time'])
            elif 'timestamp' in r:
                ts = int(r['timestamp'])
            # OHLCV fields
            o = r.get('open') or r.get('o') or None
            h = r.get('high') or r.get('h') or None
            l = r.get('low') or r.get('l') or None
            c = r.get('close') or r.get('c') or None
            v = r.get('volume') or r.get('v') or 0
            rows.append([ts, o, h, l, c, v])
        df = pd.DataFrame(rows, columns=['ts','open','high','low','close','volume'])
        df['dt'] = pd.to_datetime(df['ts'], unit='ms', utc=True).dt.tz_convert(None)
        return df
    # list-of-lists: [[ts,o,h,l,c,v], ...]
    if isinstance(kline, (list, tuple)) and len(kline) > 0 and isinstance(kline[0], (list, tuple)):
        arr = []
        for row in kline:
            # expect first value timestamp_ms
            try:
                ts = int(row[0])
            except Exception:
                ts = None
            o = float(row[1]) if len(row) > 1 and row[1] is not None else np.nan
            h = float(row[2]) if len(row) > 2 and row[2] is not None else np.nan
            l = float(row[3]) if len(row) > 3 and row[3] is not None else np.nan
            c = float(row[4]) if len(row) > 4 and row[4] is not None else np.nan
            v = float(row[5]) if len(row) > 5 and row[5] is not None else 0.0
            arr.append([ts, o, h, l, c, v])
        df = pd.DataFrame(arr, columns=['ts','open','high','low','close','volume'])
        df['dt'] = pd.to_datetime(df['ts'], unit='ms', utc=True).dt.tz_convert(None)
        return df
    return None

def _safe_extract_metric_series(metric_obj):
    """Возвращает список float значений из vip_metrics[...] или None."""
    if not isinstance(metric_obj, dict):
        return None
    # try common keys in order
    candidates = []
    for key in ('series','line','hist','values','data'):
        v = metric_obj.get(key)
        if v is not None:
            candidates = v
            break
    if not candidates:
        # single numeric value fallback
        if metric_obj.get('value') is not None:
            try:
                val = float(metric_obj.get('value') or 0.0)
                return list(np.linspace(0, val if val != 0 else 1, 40))
            except Exception:
                return None
        return None
    # now normalize candidates to list of floats
    try:
        # if list of pairs [[ts,val],...]
        if isinstance(candidates, (list, tuple)) and len(candidates) and isinstance(candidates[0], (list, tuple)):
            out = []
            for row in candidates:
                if len(row) >= 2:
                    try:
                        out.append(float(row[1]))
                    except Exception:
                        out.append(np.nan)
                else:
                    try:
                        out.append(float(row[0]))
                    except Exception:
                        out.append(np.nan)
            return out
        # if list of scalars
        if isinstance(candidates, (list, tuple)):
            return [float(x) if x is not None else np.nan for x in candidates]
    except Exception:
        return None
    return None

def apply_x_format(ax, horizon, start_dt, x_axis_cfg=None):
    """
    Универсальное форматирование оси X.
    x_axis_cfg: {'hist_format','forecast_format','tick_interval':{'unit','value'}} от LLM, опционально.
    """
    # choose default formatter based on horizon
    if x_axis_cfg and isinstance(x_axis_cfg, dict):
        fmt_hist = x_axis_cfg.get('hist_format')
        fmt_fc = x_axis_cfg.get('forecast_format')
    else:
        fmt_hist = None; fmt_fc = None

    # choose reasonable format per horizon
    mapping = {
        '5m': "%H:%M",
        '1h': "%H:%M\n%d %b",
        '1d': "%d %b %Y",
        '1w': "%d %b %Y",
        '1m': "%d %b %Y",
        '6m': "%b %Y",
        '1y': "%b %Y"
    }
    chosen = mapping.get(horizon, "%d %b")
    fmt_use = fmt_fc or fmt_hist or chosen
    locator = mdates.AutoDateLocator()
    ax.xaxis.set_major_locator(locator)
    ax.xaxis.set_major_formatter(mdates.DateFormatter(fmt_use))
    # rotate slightly
    for label in ax.get_xticklabels():
        label.set_rotation(0)
        label.set_ha('center')

def draw_candles(ax, df, width_factor=0.6, zorder=3, color_up=None, color_down=None):
    """
    Рисует свечи по df с колонками dt, open, high, low, close.
    width_factor — относительная ширина к медианному шагу по времени.
    """
    if df is None or len(df) == 0:
        return
    times = pd.to_datetime(df['dt'])
    x = mdates.date2num(times)
    # compute dx median
    if len(x) > 1:
        dx = np.median(np.diff(x))
    else:
        dx = 0.02
    w = dx * width_factor
    for xi, o, h, l, c in zip(x, df['open'], df['high'], df['low'], df['close']):
        up = (c >= o)
        col = color_up if up else color_down
        # wick
        ax.vlines(xi, l, h, color=col, linewidth=1, zorder=zorder-1)
        # body
        left = xi - w/2
        bottom = min(o, c)
        height = max(abs(c - o), 1e-9)
        rect = Rectangle((left, bottom), w, height, facecolor=col, edgecolor=col, linewidth=0.5, zorder=zorder)
        ax.add_patch(rect)
    # set x-limits nicely
    ax.set_xlim(min(x) - dx, max(x) + dx)

def rounded_title(ax, text, fontsize=11):
    """Динамическая pill-заголовок (размер под текст)."""
    trans = ax.transAxes
    # width proportional to len, but limited
    width = max(0.15, min(0.6, 0.03 * len(text)))
    height = 0.065
    bbox = FancyBboxPatch((0.01, 0.92), width, height, transform=trans,
                         boxstyle="round,pad=0.02", facecolor='#0b1220', edgecolor='none', alpha=0.95, zorder=6)
    ax.add_patch(bbox)
    ax.text(0.02, 0.92 + 0.01, text, transform=trans, color=COLORS["text"], fontsize=fontsize, va='top', zorder=7)

def draw_metric_card(fig, rect, title, series, ylabel="", fontsize=10, vip_box_alpha=0.015):
    """
    rect = (left, bottom, width, height) in figure fraction.
    series = iterable of floats
    """
    left, bottom, width, height = rect
    # background rounded card
    fig.patches.append(FancyBboxPatch((left + 0.004, bottom + 0.004), width - 0.008, height - 0.008,
                                     transform=fig.transFigure, facecolor='#ffffff', alpha=vip_box_alpha,
                                     boxstyle="round,pad=0.02", edgecolor='#222831', linewidth=0.5, zorder=0))
    # create inset axes
    ax = fig.add_axes([left + 0.01, bottom + 0.04, width - 0.03, height - 0.12], facecolor='none', zorder=5)
    # mini title box
    ax.text(0.0, 1.02, title, transform=ax.transAxes, fontsize=fontsize, color=COLORS["text"], va='bottom')
    ax.plot(np.linspace(0,1,len(series)), series, linewidth=1.6, zorder=6)
    ax.set_xticks([])
    # y ticks small
    ax.tick_params(colors=COLORS["secondary_text"], labelsize=9)
    # optionally annotate last value
    try:
        lv = series[-1]
        ax.text(0.98, 0.1, (f"{lv:.2f}" if abs(lv) >= 1e-6 else "0.00") + ("" if not ylabel else f" {ylabel}"),
                transform=ax.transAxes, fontsize=9, color=COLORS["text"], ha='right', va='bottom')
    except Exception:
        pass

def _truncate_explain(text, max_words=7):
    """Возвращает укороченную версию тезиса (max_words) и переносы."""
    if not text:
        return ""
    words = text.strip().split()
    if len(words) <= max_words:
        return textwrap.fill(text, width=28)
    short = " ".join(words[:max_words])
    # add ellipsis
    return textwrap.fill(short + " …", width=28)

def draw_action_card(ax, trade_idea: dict, vip_metrics: dict, max_words=7, fontsize=10):
    """
    Рисует компактную карточку в правом-нижнем углу ax (action box).
    Ставит тезис (укороченный), вход/цель/стоп и ключевые сигналы.
    """
    # build lines
    idea = trade_idea.get('type', 'LONG') if isinstance(trade_idea, dict) else 'LONG'
    conf = trade_idea.get('confidence', '') if isinstance(trade_idea, dict) else ''
    explain = trade_idea.get('explain_short', '') if isinstance(trade_idea, dict) else ''
    entry = trade_idea.get('entry_price', None)
    tp = trade_idea.get('take_profit_price', None)
    sl = trade_idea.get('stop_loss_price', None)
    signals = trade_idea.get('signals', []) if isinstance(trade_idea, dict) else []

    # truncate explain
    explain_short = _truncate_explain(explain, max_words)

    # place box relative to axes bbox
    bbox = ax.get_position()
    # we'll place inside axes area: compute in axes fraction
    tx = 0.98; ty = 0.02  # lower-right inside
    # transform to axes coords: but easier add as annotation in axes coordinates
    text_lines = []
    text_lines.append(f"Idea: {idea} {'|' + str(conf) if conf else ''}")
    if explain_short:
        text_lines.append(f"Thesis: {explain_short}")
    if entry is not None:
        text_lines.append(f"Entry: ≈{entry:.4f}")
    if tp is not None or sl is not None:
        text_lines.append(f"TP: {tp if tp is not None else '—'} | SL: {sl if sl is not None else '—'}")
    if signals:
        text_lines.append("Signals: " + ", ".join(signals[:3]))

    card_txt = "\n".join(text_lines)
    # draw pill background inside ax (axes fraction coords)
    ax.text(0.98, 0.02, card_txt, transform=ax.transAxes,
            fontsize=fontsize, color=COLORS["text"], va='bottom', ha='right',
            bbox=dict(facecolor='#0b1220', alpha=0.92, boxstyle='round,pad=0.4'))

# -------------------------
# ГЛАВНАЯ ФУНКЦИЯ plot_chart_v4
# -------------------------
def plot_chart_v4(
    forecast_json: dict,
    history_df: pd.DataFrame = None,
    horizon: str = "1h",
    mode: str = "standard",   # "standard" | "vip"
    output_path: str = None,
    asset_name: str = None,
    created_at: datetime = None,
    show: bool = False
) -> bytes:
    """
    Robust plotting function designed to be a drop-in replacement.
    forecast_json: LLM JSON (see TЗ) — must include 'forecast' (ohlcv or close_series).
    history_df: DataFrame or list-of-lists; will be normalized.
    horizon: timeframe string (5m,1h,1d,1w,1m,6m,1y)
    mode: 'standard' or 'vip'
    Returns PNG bytes.
    """
    # --- basic validation & normalization ---
    if created_at is None:
        created_at = datetime.now(timezone.utc)
    # ensure forecast key exists
    if not isinstance(forecast_json, dict) or 'forecast' not in forecast_json:
        raise ValueError("forecast_json must contain 'forecast' key")

    # normalize history
    if history_df is None:
        # try to synth fallback from forecast leftmost part — but prefer history_df
        history_df = None
    else:
        if not isinstance(history_df, pd.DataFrame):
            history_df = normalize_kline_to_df(history_df)
    if history_df is None:
        raise ValueError("history_df is required (history context for plotting)")

    history_df = history_df.sort_values('dt').reset_index(drop=True)
    # compute RSI on history (14 default)
    rsi_period = 14
    close = history_df['close'].astype(float)
    delta = close.diff().fillna(0)
    up = delta.clip(lower=0)
    down = -delta.clip(upper=0)
    ma_up = up.rolling(window=rsi_period, min_periods=1).mean()
    ma_down = down.rolling(window=rsi_period, min_periods=1).mean().replace(0, 1e-9)
    rsi = 100 - (100 / (1 + ma_up / ma_down))

    # parse forecast
    fc = forecast_json.get('forecast')
    fc_type = fc.get('type') if isinstance(fc, dict) else None
    fc_data = fc.get('data') if isinstance(fc, dict) else fc
    if not fc_type:
        # try to infer
        if isinstance(fc_data, list) and len(fc_data) and len(fc_data[0]) >= 6:
            fc_type = 'ohlcv'
        elif isinstance(fc_data, list) and len(fc_data) and len(fc_data[0]) >= 2:
            fc_type = 'close_series'
        else:
            raise ValueError("Cannot infer forecast.type")

    # build forecast_df with dt, open, high, low, close, volume
    if fc_type == 'ohlcv':
        # rows [ts_ms,open,high,low,close,volume]
        fdf_rows = []
        for row in fc_data:
            ts = int(row[0])
            o = float(row[1]); h = float(row[2]); l = float(row[3]); c = float(row[4])
            v = float(row[5]) if len(row) > 5 else 0.0
            fdf_rows.append([ts, o, h, l, c, v])
        fdf = pd.DataFrame(fdf_rows, columns=['ts','open','high','low','close','volume'])
        fdf['dt'] = pd.to_datetime(fdf['ts'], unit='ms', utc=True).dt.tz_convert(None)
    elif fc_type == 'close_series':
        fdf_rows = []
        for row in fc_data:
            ts = int(row[0])
            c = float(row[1])
            fdf_rows.append([ts, np.nan, np.nan, np.nan, c, 0.0])
        fdf = pd.DataFrame(fdf_rows, columns=['ts','open','high','low','close','volume'])
        fdf['dt'] = pd.to_datetime(fdf['ts'], unit='ms', utc=True).dt.tz_convert(None)
        # synth OHLC around close using small wiggle (based on recent ATR)
        hist_atr = (history_df['high'] - history_df['low']).rolling(14).mean().iloc[-1]
        hist_atr = hist_atr if not np.isnan(hist_atr) and hist_atr > 0 else (history_df['close'].iloc[-1] * 0.01)
        opens = []
        highs = []
        lows = []
        for c in fdf['close'].values:
            o = c * (1 - 0.002)  # small offset
            wig = abs(hist_atr) * 0.6
            h = max(o, c) + wig * (0.6 + np.random.rand() * 0.4)
            l = min(o, c) - wig * (0.6 + np.random.rand() * 0.4)
            opens.append(o); highs.append(h); lows.append(l)
        fdf['open'] = opens; fdf['high'] = highs; fdf['low'] = lows

    # set time window: context from history (last N) then forecast starting from created_at (or fdf dt)
    # Ensure forecast times are placed to the right of the last historical dt.
    last_hist_dt = history_df['dt'].iloc[-1]
    # If forecast timestamps are earlier than last_hist_dt, shift forecast to start after last_hist_dt
    if fdf['dt'].iloc[0] <= last_hist_dt:
        # compute step (use median diff in forecast df if >1 else use horizon duration)
        if len(fdf) > 1:
            step = fdf['dt'].iloc[1] - fdf['dt'].iloc[0]
        else:
            # map horizon to timedelta
            if horizon.endswith('m'):
                step = timedelta(minutes=int(horizon[:-1]))
            elif horizon.endswith('h'):
                step = timedelta(hours=int(horizon[:-1]))
            elif horizon.endswith('d'):
                step = timedelta(days=int(horizon[:-1]))
            elif horizon.endswith('w'):
                step = timedelta(weeks=int(horizon[:-1].rstrip('w')))
            else:
                step = timedelta(hours=1)
        # rebase forecast to start at last_hist_dt + step
        shift_base = last_hist_dt + step
        new_dts = [shift_base + i * step for i in range(len(fdf))]
        fdf['dt'] = new_dts
        fdf['ts'] = (fdf['dt'].astype('datetime64[ms]').astype(np.int64)).astype(int)

    # now prepare figure and axes
    figsize = FIGSIZE_VIP if mode == "vip" else FIGSIZE_STD
    fig = plt.figure(figsize=figsize, dpi=120)
    fig.patch.set_facecolor(COLORS["bg"])
    if mode == "vip":
        gs = fig.add_gridspec(4,3, width_ratios=[3,3,1], height_ratios=[3,2,0.9,0.45], wspace=0.12, hspace=0.12)
        ax_fore = fig.add_subplot(gs[0,0:2]); ax_hist = fig.add_subplot(gs[1,0:2]); ax_rsi = fig.add_subplot(gs[2,0:2]); ax_footer = fig.add_subplot(gs[3,0:2])
        metric_slots = [fig.add_subplot(gs[i,2]) for i in range(3)]
    else:
        gs = fig.add_gridspec(4,1, height_ratios=[3,2,0.9,0.45], hspace=0.12)
        ax_fore = fig.add_subplot(gs[0]); ax_hist = fig.add_subplot(gs[1]); ax_rsi = fig.add_subplot(gs[2]); ax_footer = fig.add_subplot(gs[3])
        metric_slots = []

    # panel backgrounds: slightly lighter than global bg, with fine dashed border
    for ax in (ax_fore, ax_hist, ax_rsi):
        ax.set_facecolor(COLORS["panel_bg"])
        # add thin dashed rectangle border (in axes coords)
        bb = ax.get_position()
        rect = Rectangle((bb.x0, bb.y0), bb.width, bb.height, transform=fig.transFigure,
                         fill=False, edgecolor=COLORS["panel_grid"], linewidth=0.6, linestyle=(0, (2,3)), zorder=0)
        fig.patches.append(rect)

    # Plot history on ax_hist
    draw_candles(ax_hist, history_df.iloc[-min(len(history_df), 240):], width_factor=0.6,
                 color_up=COLORS["bull"], color_down=COLORS["bear"])
    # EMAs
    ax_hist.plot(history_df['dt'], history_df['close'].ewm(span=20, adjust=False).mean(), color=COLORS["ema20"], linewidth=1.2, zorder=6)
    ax_hist.plot(history_df['dt'], history_df['close'].ewm(span=50, adjust=False).mean(), color=COLORS["ema50"], linewidth=1.2, zorder=6)
    rounded_title(ax_hist, "History", fontsize=11)
    # show final Price label
    final_price = history_df['close'].iloc[-1]
    ax_hist.annotate(f"Price: {final_price:.2f}", xy=(history_df['dt'].iloc[-1], final_price),
                     xytext=(history_df['dt'].iloc[-1], final_price * (1 + 0.02)),
                     color=COLORS["text"],
                     bbox=dict(facecolor='#0b1220', alpha=0.8, boxstyle='round,pad=0.2'),
                     arrowprops=dict(arrowstyle="->", color=COLORS["secondary_text"]))

    # Plot forecast: combine last N context from history + forecast on ax_fore
    ctx_n = min(12, len(history_df))
    ctx_df = history_df.iloc[-ctx_n:].copy().reset_index(drop=True)
    draw_candles(ax_fore, ctx_df, width_factor=0.6, color_up=COLORS["bull"], color_down=COLORS["bear"])
    draw_candles(ax_fore, fdf, width_factor=0.9, color_up=COLORS["bull"], color_down=COLORS["bear"])
    rounded_title(ax_fore, f"Forecast — {horizon.upper()}", fontsize=12)

    # zones: neutral/profit/risk relative to entry_price (center neutral)
    trade_idea = forecast_json.get('trade_idea', {}) or {}
    entry_price = trade_idea.get('entry_price', float(history_df['close'].iloc[-1]))
    y_min = min(ctx_df['low'].min(), fdf['low'].min())
    y_max = max(ctx_df['high'].max(), fdf['high'].max())
    y_range = y_max - y_min if y_max != y_min else y_max * 0.02
    nf = 0.30
    neutral_half = y_range * nf / 2.0
    neutral_bottom = entry_price - neutral_half
    neutral_top = entry_price + neutral_half
    # draw clipped spans
    def clip_span(a,b,color,alpha=0.06):
        lo = max(min(a,b), y_min); hi = min(max(a,b), y_max)
        if lo < hi:
            ax_fore.axhspan(lo, hi, color=color, alpha=alpha, zorder=1, clip_on=True)
    clip_span(y_max, neutral_top, COLORS["profit"])
    clip_span(neutral_bottom, neutral_top, COLORS["neutral"])
    clip_span(y_min, neutral_bottom, COLORS["risk"])

    # draw ENTRY/SL/TP lines inside axes with boxed labels
    sl_price = trade_idea.get('stop_loss_price', entry_price * 0.99)
    tp_price = trade_idea.get('take_profit_price', entry_price * 1.03)
    def boxed_label(ax, x_dt, y_val, label, color, emphasize=True):
        lw = 1.6 if emphasize else 0.9
        ls = '--' if emphasize else ':'
        ax.axhline(y_val, color=color, linestyle=ls, linewidth=lw, zorder=6)
        # position label near right edge of forecast
        x_pos = fdf['dt'].iloc[-1] + (fdf['dt'].iloc[1] - fdf['dt'].iloc[0]) * 0.5 if len(fdf)>1 else fdf['dt'].iloc[-1]
        # clamp y within visible
        ymin2, ymax2 = ax.get_ylim()
        y_plot = min(max(y_val, ymin2 + 0.01*(ymax2-ymin2)), ymax2 - 0.01*(ymax2-ymin2))
        ax.text(x_pos, y_plot, f" {label} ", color=COLORS["text"], fontsize=10,
                bbox=dict(facecolor='#0b1220', alpha=0.9, boxstyle='round,pad=0.2'), zorder=10)

    boxed_label(ax_fore, fdf['dt'].iloc[-1], entry_price, "ENTRY", COLORS["vip_accent"], emphasize=True)
    boxed_label(ax_fore, fdf['dt'].iloc[-1], sl_price, "SL", COLORS["bear"], emphasize=True)
    if mode == "vip":
        boxed_label(ax_fore, fdf['dt'].iloc[-1], tp_price, "TP", COLORS["forecast"], emphasize=False)

    # single best buy/sell markers
    if len(fdf) > 0:
        buy_dt = fdf['dt'].iloc[0]; buy_price = float(fdf['close'].iloc[0])
        sell_dt = fdf['dt'].iloc[-1]; sell_price = float(fdf['close'].iloc[-1])
        ax_fore.scatter([mdates.date2num(buy_dt)], [buy_price], marker="o", s=120, color=COLORS["bear"], edgecolor=COLORS["text"], zorder=9)
        ax_fore.text(buy_dt, buy_price, f"  B {buy_price:.4f}", color=COLORS["text"], fontsize=9, va="center", ha="left",
                     bbox=dict(facecolor="#0b1220", alpha=0.85, boxstyle="round,pad=0.12"), zorder=10)
        ax_fore.scatter([mdates.date2num(sell_dt)], [sell_price], marker="v", s=140, color=COLORS["bull"], edgecolor=COLORS["text"], zorder=9)
        ax_fore.text(sell_dt, sell_price, f"  S {sell_price:.4f}", color=COLORS["text"], fontsize=9, va="center", ha="left",
                     bbox=dict(facecolor="#0b1220", alpha=0.85, boxstyle="round,pad=0.12"), zorder=10)

    # X axis formatting
    apply_x_format(ax_fore, horizon, fdf['dt'].iloc[0], x_axis_cfg=forecast_json.get('x_axis'))
    ax_fore.tick_params(colors=COLORS["secondary_text"], labelsize=10)
    ax_fore.set_ylabel("", color=COLORS["secondary_text"])
    ax_fore.set_xlabel("")

    # Draw action card (right-bottom inside forecast axes)
    draw_action_card(ax_fore, trade_idea, forecast_json.get('vip_metrics', {}), max_words=7, fontsize=10)

    # RSI plot
    ax_rsi.plot(history_df['dt'], rsi, color=COLORS["forecast"], linewidth=1.6)
    ax_rsi.fill_between(history_df['dt'], 70, 100, where=(rsi >= 70), color=COLORS["bear"], alpha=0.06)
    ax_rsi.fill_between(history_df['dt'], 0, 30, where=(rsi <= 30), color=COLORS["profit"], alpha=0.04)
    ax_rsi.axhline(70, linestyle="--", color=COLORS["secondary_text"], alpha=0.6)
    ax_rsi.axhline(30, linestyle="--", color=COLORS["secondary_text"], alpha=0.6)
    ax_rsi.set_ylim(0, 100)
    rounded_title(ax_rsi, "RSI", fontsize=11)

    # Footer legend
    ax_footer.axis("off")
    ax_footer.add_patch(Rectangle((0.01, 0.56), 0.06, 0.2, transform=ax_footer.transAxes, facecolor=COLORS["profit"], alpha=0.9))
    ax_footer.text(0.08, 0.64, "PROFIT zone", transform=ax_footer.transAxes, color=COLORS["secondary_text"], fontsize=10)
    ax_footer.add_patch(Rectangle((0.42, 0.56), 0.06, 0.2, transform=ax_footer.transAxes, facecolor=COLORS["neutral"], alpha=0.9))
    ax_footer.text(0.49, 0.64, "WAIT zone", transform=ax_footer.transAxes, color=COLORS["secondary_text"], fontsize=10)
    ax_footer.add_patch(Rectangle((0.75, 0.56), 0.06, 0.2, transform=ax_footer.transAxes, facecolor=COLORS["risk"], alpha=0.9))
    ax_footer.text(0.82, 0.64, "RISK zone", transform=ax_footer.transAxes, color=COLORS["secondary_text"], fontsize=10)

    # VIP metric cards (right column)
    vip_metrics = forecast_json.get('vip_metrics', {}) or {}
    metrics_to_show = forecast_json.get('metrics_to_show') or list(vip_metrics.keys())[:3] or []
    if mode == "vip" and metric_slots:
        # layout rects from figure coordinates (better consistent)
        left = 0.73; width = 0.255; top = 0.66; card_h = 0.105; gap = 0.02
        for i, slot_ax in enumerate(metric_slots):
            # we use draw_metric_card with its own inset axes
            bottom = top - i * (card_h + gap)
            rect = (left, bottom, width, card_h)
            m = metrics_to_show[i] if i < len(metrics_to_show) else (list(vip_metrics.keys())[i] if i < len(vip_metrics) else f"metric_{i}")
            series = _safe_extract_metric_series(vip_metrics.get(m)) or []
            # fallback: if empty, create small synthetic
            if not series:
                series = list(np.clip(0.45 + 0.12 * np.sin(np.linspace(0, 3.14, 40) + i) + 0.02 * np.random.randn(40), 0, None))
            ylabel = "%" if "prob" in m.lower() or "backtest" in m.lower() else ""
            draw_metric_card(fig, rect, m.replace("_"," ").title(), series, ylabel=ylabel, fontsize=10, vip_box_alpha=0.015)

    # final polish
    for ax in (ax_fore, ax_hist, ax_rsi):
        for spine in ax.spines.values():
            spine.set_visible(False)
        ax.tick_params(colors=COLORS["secondary_text"], labelsize=10)

    fig.canvas.draw()
    buf = io.BytesIO()
    plt.savefig(buf, bbox_inches='tight', facecolor=fig.get_facecolor(), dpi=150)
    if output_path:
        plt.savefig(output_path, bbox_inches='tight', facecolor=fig.get_facecolor(), dpi=150)
    if show:
        plt.show()
    plt.close(fig)
    buf.seek(0)
    return buf.getvalue()
