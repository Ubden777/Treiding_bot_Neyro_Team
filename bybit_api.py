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




load_dotenv()

cg = CoinGeckoAPI()

# URL для API Bybit v5
BASE_URL = "https://api.bybit.com"

# Простой кэш (словарь в памяти)
data_cache = {}
CACHE_TTL = 3600  # 1 час в секундах

# Логи (чтобы отслеживать запросы)
logging.basicConfig(level=logging.INFO)


# Функция для скачивания/обновления списка монет (раз в день)
def load_coins_list(force_update=False):
    file = 'coins.json'
    if os.path.exists(file) and not force_update:
        with open(file, 'r') as f:
            data = json.load(f)
        if time.time() - data.get('timestamp', 0) < 86400:  # 24 часа
            logging.info("Список монет из кэша")
            return data['coins']

    try:
        time.sleep(1)  # Задержка для лимита
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}  # Чтобы избежать блоков
        response = requests.get("https://api.coingecko.com/api/v3/coins/list", headers=headers)
        response.raise_for_status()
        coins = response.json()
        if not coins:
            logging.warning("Пустой список от CoinGecko, возможно лимит")
            return []
        with open(file, 'w') as f:
            json.dump({'coins': coins, 'timestamp': time.time()}, f)
        logging.info("Список монет обновлён, загружено {len(coins)} монет")
        return coins
    except Exception as e:
        logging.error(f"Ошибка загрузки списка монет: {e}")
        return []


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
async def get_kline_data(session, symbol: str, interval: str, limit: int = 100) -> list | None:
    cache_key = f"kline_{symbol}_{interval}"
    if cache_key in data_cache and time.time() - data_cache[cache_key]['time'] < CACHE_TTL:
        logging.info(f"Использую кэш для {symbol}")
        return data_cache[cache_key]['data']

    time.sleep(1)  # Задержка 1 сек, чтобы не превысить лимит

    interval_map = {'5m': '5', '1h': '60', '1d': 'D', '1w': 'W', '1m': 'M', '6m': 'M', '1y': 'M'}
    api_interval = interval_map.get(interval, 'D')
    params = {"category": "linear", "symbol": symbol, "interval": api_interval, "limit": limit}

    try:
        response = await session.get(f"{BASE_URL}/v5/market/kline", params=params)
        response.raise_for_status()
        data = response.json()
        if data.get("retCode") == 0 and data["result"]["list"]:
            kline = sorted(data["result"]["list"], key=lambda x: int(x[0]))
            if interval in ['6m', '1y']:
                agg_period = 6 if interval == '6m' else 12
                kline = aggregate_kline(kline, period=agg_period, freq='M')

            # Сохраняем в кэш
            data_cache[cache_key] = {'data': kline, 'time': time.time()}
            logging.info(f"Запрос к Bybit для {symbol}, кэш обновлён")
            return kline
        return None
    except Exception as e:
        logging.error(f"Ошибка Bybit kline: {e}")
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
def get_macro_data(symbol: str):
    try:
        api_key = os.getenv('ALPHA_VANTAGE_API_KEY')
        # BTC
        url_btc = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=BTCUSD&outputsize=full&apikey={api_key}"
        response_btc = requests.get(url_btc)
        data_btc = response_btc.json()['Time Series (Daily)']
        df_btc = pd.DataFrame.from_dict(data_btc, orient='index')
        df_btc = df_btc.sort_index()
        df_btc['close'] = df_btc['4. close'].astype(float)
        # S&P
        url_sp = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=^GSPC&outputsize=full&apikey={api_key}"
        response_sp = requests.get(url_sp)
        data_sp = response_sp.json()['Time Series (Daily)']
        df_sp = pd.DataFrame.from_dict(data_sp, orient='index')
        df_sp = df_sp.sort_index()
        df_sp['close'] = df_sp['4. close'].astype(float)
        # Align dates
        common_dates = df_btc.index.intersection(df_sp.index)
        df_btc = df_btc.loc[common_dates]
        df_sp = df_sp.loc[common_dates]
        corr = df_btc['close'].corr(df_sp['close'])
        corr = 0 if pd.isna(corr) else corr
        # ETF inflows (GBTC)
        url_etf = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=GBTC&outputsize=compact&apikey={api_key}"
        response_etf = requests.get(url_etf)
        data_etf = response_etf.json()['Time Series (Daily)']
        df_etf = pd.DataFrame.from_dict(data_etf, orient='index')
        df_etf = df_etf.sort_index()
        df_etf['volume'] = df_etf['5. volume'].astype(float)
        etf_inflows = df_etf['volume'].sum() if not df_etf.empty else 0
        interpretation = "Бычий" if corr > 0.5 else "Медвежий"
        return {"sp500_corr": corr, "etf_inflows": etf_inflows, "interpretation": interpretation}
    except Exception as e:
        logging.error(f"Ошибка macro: {e}")
        return {"sp500_corr": 0, "etf_inflows": 0, "interpretation": "N/A"}

# Пропущенная функция backtest_probabilities (простой backtest на kline)
def backtest_probabilities(symbol: str, timeframe: str):
    try:
        session = httpx.Client()
        params = {"category": "linear", "symbol": symbol, "interval": timeframe, "limit": 200}
        response = session.get(f"{BASE_URL}/v5/market/kline", params=params)
        data = response.json()
        if data.get("retCode") == 0:
            kline = sorted(data["result"]["list"], key=lambda x: int(x[0]))
        else:
            return {"up": 50, "base": 30, "down": 20}
        if not kline or len(kline) < 14:
            logging.warning("Kline short for backtest")
            return {"up": 50, "base": 30, "down": 20}
        df = pd.DataFrame(kline, columns=["timestamp", "open", "high", "low", "close", "volume"])
        df = df.astype(float)
        df['ema20'] = ta.ema(df['close'], length=20)
        df['ema50'] = ta.ema(df['close'], length=50)
        df['rsi'] = ta.rsi(df['close'], length=14)
        df['trend_bull'] = (df['ema20'] > df['ema50']).astype(int)
        df['rsi_bull'] = (df['rsi'] > 35).astype(int)  # Relax
        df['return'] = df['close'].pct_change().shift(-1)
        df['outcome'] = 1  # Рост
        df.loc[df['return'] < -0.01, 'outcome'] = -1  # Снижение
        df.loc[abs(df['return']) <= 0.01, 'outcome'] = 0  # База
        bull_cases = df[(df['trend_bull'] == 1) & (df['rsi_bull'] == 1)]
        logging.info(f"Bull cases len: {len(bull_cases)}")
        prob_up = (bull_cases['outcome'] == 1).mean() * 100 if not bull_cases.empty else 50
        prob_down = (bull_cases['outcome'] == -1).mean() * 100 if not bull_cases.empty else 20
        prob_base = 100 - prob_up - prob_down
        return {"up": round(prob_up, 1), "base": round(prob_base, 1), "down": round(prob_down, 1)}
    except Exception as e:
        logging.error(f"Ошибка backtest: {e}")
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


# Функция для получения данных (с derive)
async def get_market_data(symbol: str, timeframe: str, limit: int = 365, is_vip: bool = False, category: str = 'linear'):
    try:
        # Kline
        session = httpx.AsyncClient()
        params = {"category": category, "symbol": symbol, "interval": timeframe, "limit": limit}
        response = await session.get(f"{BASE_URL}/v5/market/kline", params=params)
        data = response.json()
        if data.get("retCode") != 0:
            logging.error(f"Kline error for {symbol} in {category}: {data.get('retMsg')}")
            return None
        kline = sorted(data["result"]["list"], key=lambda x: int(x[0]))
        if not kline:
            logging.warning(f"Empty kline for {symbol} in {category}")
            return None
        # Tickers
        params_ticker = {"category": category, "symbol": symbol}
        response_ticker = await session.get(f"{BASE_URL}/v5/market/tickers", params=params_ticker)
        data_ticker = response_ticker.json()
        if data_ticker.get("retCode") != 0:
            logging.error(f"Ticker error for {symbol}: {data_ticker.get('retMsg')}")
            return None
        ticker = data_ticker["result"]["list"][0] if data_ticker["result"]["list"] else {}
        current_price = float(ticker.get('lastPrice', 0))
        price_change_24h_percent = float(ticker.get('price24hPChg', 0)) * 100
        open_interest_value = float(ticker.get('openInterestValue', 0)) if 'openInterestValue' in ticker else 0
        funding_rate = float(ticker.get('fundingRate', 0)) * 100 if 'fundingRate' in ticker else 0
        # Onchain (use base symbol like 'btc' for Glassnode)
        base_symbol = symbol.rstrip(network) if 'network' in locals() else symbol  # Assume network from symbol
        onchain = get_onchain_data(base_symbol.lower())
        macro = get_macro_data(base_symbol.lower())
        backtest_probs = backtest_probabilities(symbol, timeframe)
        tech_metrics = calculate_advanced_metrics(kline)
        market_data = {
            'symbol': symbol,
            'current_price': current_price,
            'price_change_24h_percent': price_change_24h_percent,
            'open_interest_value': open_interest_value,
            'funding_rate': funding_rate,
            'kline_data': kline,
            'timeframe': timeframe,
            'onchain': onchain,
            'macro': macro,
            'backtest_probs': backtest_probs,
            **tech_metrics
        }
        return market_data
    except Exception as e:
        logging.error(f"Ошибка get_market_data: {e}")
        return None


def aggregate_kline(kline: list, period: int, freq: str) -> list:
    """Агрегирует свечи для длинных TF (e.g., monthly to 6M)."""
    if not kline:
        logging.warning("No kline data to aggregate.")
        return []

    try:
        # Определяем количество столбцов
        num_cols = len(kline[0]) if kline else 0
        if num_cols == 6:
            columns = ["timestamp", "open", "high", "low", "close", "volume"]
        elif num_cols == 7:
            columns = ["timestamp", "open", "high", "low", "close", "volume", "turnover"]
        else:
            raise ValueError(f"Unexpected number of columns in kline_data: {num_cols}")

        df = pd.DataFrame(kline, columns=columns)
        df['timestamp'] = df['timestamp'].astype('int64')
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        df.set_index('timestamp', inplace=True)
        df = df.astype(float)

        agg = {'open': 'first', 'high': 'max', 'low': 'min', 'close': 'last', 'volume': 'sum'}
        if 'turnover' in df.columns:
            agg['turnover'] = 'sum'

        df_resampled = df.resample('ME').agg(agg)  # Use 'ME' for month end

        if not isinstance(df_resampled.index, pd.DatetimeIndex):
            logging.error("Index after resample is not DatetimeIndex.")
            return []

        grouper = pd.Grouper(freq=f'{period}ME')  # Изменено на 'ME' (e.g., '6ME' for 6 months end)
        df_grouped = df_resampled.groupby(grouper).agg(agg)

        df_grouped.reset_index(inplace=True)
        df_grouped['timestamp'] = df_grouped['timestamp'].astype('int64') // 10**6
        df_grouped['timestamp'] = df_grouped['timestamp'].astype(int)

        if period == 1:
            df_resampled.reset_index(inplace=True)
            df_resampled['timestamp'] = df_resampled['timestamp'].astype('int64') // 10 ** 6
            df_resampled['timestamp'] = df_resampled['timestamp'].astype(int)
            return df_resampled[columns].values.tolist()

        # Возвращаем в формате list of lists с теми же столбцами
        return df_grouped[columns].values.tolist()
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
        "vwap": vwap
    }


# async def get_market_data(symbol: str, timeframe: str = '1d', limit: int = 100) -> dict | None:
#     symbol = symbol.upper()
#     if not symbol.endswith('USDT'):
#         symbol = f"{symbol}USDT"
#     async with httpx.AsyncClient() as session:
#         derivatives_task = get_derivatives_info(session, symbol)
#         kline_task = get_kline_data(session, symbol, interval=timeframe, limit=limit)
#         netflow_task = get_exchange_netflow(symbol)
#         lth_sopr_task = get_lth_sopr(symbol)
#         derivatives_info, kline_data, netflow_info, lth_sopr_info = await asyncio.gather(
#             derivatives_task, kline_task, netflow_task, lth_sopr_task
#         )
#         if not derivatives_info or not kline_data:
#             logging.error(f"No data for {symbol} on {timeframe}")
#             return None
#         tech_metrics = calculate_advanced_metrics(kline_data)
#         market_data = {
#             "symbol": symbol,
#             "current_price": derivatives_info["last_price"],
#             "price_change_24h_percent": derivatives_info["price_24h_pcnt"],
#             "open_interest_value": derivatives_info["open_interest_value"],
#             "funding_rate": derivatives_info["funding_rate"],
#             "kline_data": kline_data,
#             "timeframe": timeframe
#         }
#         market_data.update(tech_metrics)
#         market_data["exchange_netflow"] = netflow_info
#         market_data["lth_sopr"] = lth_sopr_info
#         return market_data


# bybit_api.py (БЛОК: plot_chart - добавить сортировку df)
def plot_chart(market_data: dict, timeframe: str, is_vip: bool = False):
    kline_data = market_data['kline_data']
    if not kline_data:
        return None
    df = pd.DataFrame(kline_data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'turnover'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df.set_index('timestamp', inplace=True)
    df = df.astype(float)
    df = df.sort_index()  # Ensure datetime order

    # Aggregation for long TF
    if timeframe in ['1m', '6m', '1y']:
        freq = 'M' if timeframe == '1m' else '6M' if timeframe == '6m' else 'Y'
        df = df.resample(freq).agg({'open': 'first', 'high': 'max', 'low': 'min', 'close': 'last', 'volume': 'sum'})

    # Индикаторы
    min_len = len(df) - 1
    ema_20 = ta.ema(df['close'], length=min(20, min_len)) if min_len >= 1 else None
    ema_50 = ta.ema(df['close'], length=min(50, min_len)) if min_len >= 1 else None
    bb = ta.bbands(df['close'], length=min(20, min_len), std=2) if min_len >= 1 else None
    rsi = ta.rsi(df['close'], length=min(14, min_len)) if min_len >= 1 else None

    # Фигура
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 8), sharex=True, gridspec_kw={'height_ratios': [3, 1, 1]})
    fig.suptitle(f"{market_data.get('symbol', 'Asset')} ({timeframe})", fontsize=14, color='black')

    # OHLC Candles
    width_map = {'5m': 0.0005, '1h': 0.001, '1d': 0.3, '1w': 0.6, '1m': 1.0, '6m': 2.0, '1y': 4.0}
    width = width_map.get(timeframe, 0.3)

    date_fmt = '%H:%M' if timeframe in ['5m', '1h'] else '%Y-%m-%d' if timeframe in ['1d', '1w'] else '%Y-%m'
    ax1.xaxis.set_major_formatter(mdates.DateFormatter(date_fmt))

    for i in range(len(df)):
        o, h, l, c = df.iloc[i][['open', 'high', 'low', 'close']]
        color = 'green' if c >= o else 'red'
        ax1.plot([df.index[i], df.index[i]], [l, h], color=color, linewidth=1)  # Wick
        ax1.bar(df.index[i], abs(c - o), width, bottom=min(o, c), color=color, alpha=0.8)  # Body

    # EMAs & BB
    if ema_20 is not None:
        ax1.plot(df.index, ema_20, label='EMA20', color='blue', linewidth=1.5)
    if ema_50 is not None:
        ax1.plot(df.index, ema_50, label='EMA50', color='orange', linewidth=1.5)
    if bb is not None:
        ax1.fill_between(df.index, bb['BBL_20_2.0'], bb['BBU_20_2.0'], color='gray', alpha=0.2, label='Bollinger')

    if is_vip:
        support = market_data.get('support_level', 0)
        resistance = market_data.get('resistance_level', 0)
        ax1.axhline(support, color='green', linestyle='--', label='Support', linewidth=1.2)
        ax1.axhline(resistance, color='red', linestyle='--', label='Resistance', linewidth=1.2)
        last_close = df['close'].iloc[-1]
        ax1.annotate(f"Price: {last_close:.2f}", xy=(df.index[-1], last_close), xytext=(10, 10),
                     textcoords='offset points', arrowprops=dict(arrowstyle="->", color='black'), fontsize=10, color='black')
        if rsi is not None:
            last_rsi = rsi.iloc[-1]
            if last_rsi > 70:
                ax2.annotate("Overbought", xy=(df.index[-1], last_rsi), xytext=(10, -10),
                             textcoords='offset points', arrowprops=dict(arrowstyle="->", color='red'), color='red', fontsize=10)
            elif last_rsi < 30:
                ax2.annotate("Oversold", xy=(df.index[-1], last_rsi), xytext=(10, 10),
                             textcoords='offset points', arrowprops=dict(arrowstyle="->", color='green'), color='green', fontsize=10)

    ax1.legend(loc='upper left', fontsize=8)
    ax1.tick_params(axis='x', rotation=45, labelsize=8)
    ax1.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f'{x:.0f}'))  # Целые цены

    # RSI
    if rsi is not None:
        ax2.plot(df.index, rsi, label='RSI', color='purple', linewidth=1.5)
        ax2.axhline(70, color='red', linestyle='--', alpha=0.7)
        ax2.axhline(50, color='black', linestyle=':', alpha=0.5)
        ax2.axhline(30, color='green', linestyle='--', alpha=0.7)
        ax2.set_ylim(0, 100)
        ax2.legend(loc='upper left', fontsize=8)

    # Volume
    colors = ['green' if df['close'].iloc[i] >= df['open'].iloc[i] else 'red' for i in range(len(df))]
    ax3.bar(df.index, df['volume'], color=colors, alpha=0.6, width=width)
    ax3.set_ylabel('Volume', fontsize=8)

    plt.tight_layout(pad=1.0)
    buf = BytesIO()
    fig.savefig(buf, format='png', dpi=150, bbox_inches='tight')
    buf.seek(0)
    plt.close(fig)
    return buf