# translations.py
translations = {
    'ru': {

        'select_forecast_type': "📊 Выберите тип прогноза:",
        'select_ticker': "Введите тикер (например, BTCUSDT):",
        'select_timeframe': "Выберите таймфрейм:",
        'processing_forecast': "⏳ Обрабатываем данные и генерируем прогноз...",
        'forecast_ready': "✅ Прогноз готов!",
        'error_api': "❌ Ошибка получения данных. Попробуйте позже.",
        'error_gpt': "❌ Ошибка генерации прогноза. Попробуйте другой запрос.",
        'no_balance': "❌ Недостаточно прогнозов. Купите в каталоге.",
        'timeframes': {
            '5m': '5 мин', '1h': '1 час', '1d': '1 день', '1w': '1 неделя',
            '1m': '1 месяц', '6m': 'Полгода', '1y': '1 год'
        },


        # ==============================
        # 1. Общие команды и сообщения
        # ==============================
        'start': "✅ Запустить бота",
        'admin': "👨‍💻 Админ панель",
        'cancel': "🔙 Отмена",
        'traffer': "🥷 Траффер-панель",
        'cancel_disvie': "🚫 Действие отменено.",

        'traff_info': '''
👤 Траффер: {trafer_name}
👤 Username: {t_username}
🆔 ID: {t_id}
🏷️ Промокод: {t_promo}

📱 Телефон: {t_telefon}
💳 Карта: {t_karta}
🪙 Крипта: {t_kripta}
🔗 Сеть: {crypto_network}

📊 Способ заработка: {human_model}
📊 Лидов: {leads}

🏦 На балансе: {balance}₽
💸 Вывел: {paid}₽
💰 Заработал всего: {total}₽
            ''',

        'edit_traffera': "✏️ Редактировать траффера", # NEW
        'obnovit_traf_info': "🔄 Обновить",
        'traff_id_kanala': "🆔 ID канала: {pay_link}",
        'traff_priglos_ssilka': "🔗 Пригласительная ссылка:\n{invite_link}",
        'del_traffera': "❌ Удалить траффера",
        'back': "↩️ Назад",
        'obnovit_podpiski': "🔄 Обновить подписки",
        'vivisti_money': "💸 Вывести деньги",
        'back_traff_panel': "🔙 Выйти из Траф.панели",
        'command_start': "Запустить бота",
        'command_admin': "Админ-панель",
        'command_traffer': "Траффер-панель",
        'podpiska_istekla': "Подписка истекла",
        'bolche_day': "{days} дн. {hours} ч.",
        'menche_day': "{hours} ч. {minutes} мин.",
        'menche_hour': "{minutes} мин.",
        'spasibo_za_oplaty': "Спасибо за оплату! Доступ активирован.",
        'chek_partners': "🔁 Проверить подписку",
        'pustoy_spisok_partners': "Список партнёров пуст",
        'NO_chek_partners': "Пожалуйста, подпишитесь на всех партнёров, чтобы продолжить.",

        'edit_name': "Имя",
        'edit_id': "ID",
        'edit_username': "@User_name",
        'edit_telefon': "Телефон",
        'edit_karta': "Карта",
        'edit_kripta': "Криптокошелек",
        'edit_crypto_network': "Сеть крипты",
        'cancel_edit': "↩️ Отмена",  # NEW

        # NEW: Prompts for editing
        'enter_new_name': "Введите новое имя:",
        'enter_new_id': "Введите новый ID:",
        'enter_new_username': "Введите новый @User_name:",
        'enter_new_telefon': "Введите новый телефон:",
        'enter_new_karta': "Введите новую карту:",
        'enter_new_kripta': "Введите новый криптокошелек:",
        'enter_new_crypto_network': "Введите новую сеть крипты:",
        'traffer_updated_success': "✅ Данные траффера обновлены!",  # NEW
        'no_traffer_found': "Траффер не найден.",  # NEW

        "referral_reward": "Вы получили 1 постоянный VIP-прогноз в качестве вознаграждения за реферал!",
        "profile_text": '''
➖➖➖➖➖➖➖➖➖

👤 *{user_name}* | *ID:* `{user_id}` 
🎫 *Подписка:* *{subscription}* 
⌛️ *До истечения:* *{remaining}*

🔹 *Прогнозы:* *{ob_prognoz}*
💠 *VIP прогнозы:* *{rach_prognoz}*
🔹 *Временные прогнозы:* *{ob_vr_prognoz}*
💠 *Временные VIP прогнозы:* *{rach_vr_prognoz}*

👥 *Приглашенных друзей:* {referred_count}
🔗 *Ваша реферальная ссылка:* 

`{referral_link}`

➖➖➖➖➖➖➖➖➖

‼️ *Проводится бета тест*
Всё функции доступны бесплатно.

➖➖➖➖➖➖➖➖➖
            ''',

        'sozdat_prognoz': "📊 Создать прогноз",
        'katalog': "🛍 Каталог",
        'otzivi': "🗣️ Отзывы",
        'promokod': "#️⃣ Промокод",
        'support': "⚙️ Поддержка",
        'instruction': "📘 Инструкция",
        'error_profile': "Ошибка при получении данных профиля.",

        'NOT_od_prognoz': "❌ У вас нет обычных прогнозов!",
        'NOT_VIP_prognoz': "❌ У вас нет VIP‑прогнозов!",
        'vvedite_daty_vremia': "🗓 Введите дату и время матча (например: 01.01.2025 18:00):",
        'vvedite_vid_sporta': "⚽️ Введите вид спорта (например: футбол):",
        'vvedite_commandi': "👥 Введите названия команд через запятую (Команда №1, Команда №2):",

        'error_vvedite_commandi': '''
Пожалуйста, введите ровно два названия команд, разделённые запятой
(например: Команда1, Команда2).
            ''',

        'message_promokod': '''
✅ Промокод принят!
Вам добавлено 🔹 {add_ob_prognoz} обычных прогноз(ов) и 💠 {add_rach_prognoz} VIP прогноз(ов).
🎫 Подписка: {subscription}
            ''',

        'vvevite_promocod_1': "⏳ Введите промокод",
        'vvevite_promocod_2': "Введите промокод:",
        'primenit_promocod': "✅ Применить промокод",
        'najmi_primenit_promocod': "Нажми кнопку ниже, чтобы применить промокод 👇",
        'yes_promocod_ot_traffera': "✅ Промокод от траферов принят! Вам добавлен 1 обычный прогноз.",
        'ispolzovan_promocod': "❌ Вы уже использовали этот промокод.",
        'nedeistvitelen_promocod': "❌ Этот промокод больше не действителен.",
        'promocod_ne_nayden': "❌ Промокод не найден.",

        'promocod_ot_traffera_YES': '''
            ✅ Промокод активирован!
            + 1 обычный прогноз.
            ''',

        'error_close_panel': "Не удалось закрыть панель 😔",

        'yes_dannie': "✅ Подтвердить данные",
        'no_dannie': "🔄 Заполнить заново",
        'obrabotka_prognoza': "⏳ Обрабатывается ваш прогноз…",
        'no_registr_traffera': "⛔ Вы не зарегистрированы как траффер.",
        'balans_menche_1000': "Вывод доступен от 1000 ₽",
        'ot_1000_do_balans': "Введите сумму вывода (от 1000 до {balance}₽):",
        'vvedite_celoe_chislo': "Введите целое число!",
        'summa_bolche_1000': "Сумма должна быть не менее 1000 ₽!",
        'summa_bolche_balansa': "Сумма превышает ваш текущий баланс!",
        'redactirovat': "✏️ Редактировать",
        'podtverdit': "✅ Подтвердить",
        'proverka_summi': "Вы хотите вывести {amt}₽?",
        'yes_viplata': "✅ Выплата {amt}₽ прошла успешно.",
        'no_viplata': "❌ Выплата {amt}₽ не принята. Обратитесь в поддержку: https://t.me/suportneyroteam",

        'katalog_podpisok': '''
➖➖➖➖➖➖➖➖➖

🎫 *{price_standart}₽ - Standart* на неделю  
Вам будет доступно 5 прогнозов, 0 VIP прогнозов

🎫 *{price_medium}₽ - Medium* на неделю  
Вам будет доступно 12 прогнозов, 6 VIP прогнозов

🎫 *{price_premium}₽ - Premium* на две недели  
Вам будет доступно 30 прогнозов, 15 VIP прогнозов

➖➖➖➖➖➖➖➖➖

‼️ *Проводится бета тест*
Всё функции доступны бесплатно.

➖➖➖➖➖➖➖➖➖

💳 Выберите подписку для оплаты снизу:
            ''',

        'katalog_prognozov': '''
➖➖➖➖➖➖➖➖➖➖➖➖➖➖

🔹 *{price_1_ob}₽* - 1 Прогноз 
🔹 *{price_5_ob}₽* - 5 Прогнозов 
🔹 *{price_15_ob}₽* - 15 Прогнозов 

💠 *{price_1_vip}₽* - 1 VIP Прогноз 
💠 *{price_5_vip}₽* - 5 VIP  Прогнозов 
💠 *{price_15_vip}₽* - 15 VIP  Прогнозов

➖➖➖➖➖➖➖➖➖➖➖➖➖➖

‼️ *Проводится бета тест*
Всё функции доступны бесплатно.

➖➖➖➖➖➖➖➖➖➖➖➖➖➖

💳 Выберите пакет для оплаты снизу:
            ''',

        'standart': "💥 Ваша подписка повышена до Standart на неделю!",
        'medium': "💥 Ваша подписка повышена до Medium на неделю!",
        'premium': "💥 Ваша подписка повышена до Premium на 2 недели!",
        'podpiski': "🎫 Подписки",
        'prognozi': "📊 Прогнозы",
        'catalog_text': "Добро пожаловать в каталог! Выберите раздел:",
        '1_ob_prognoz': "🔹 {price_1_ob}₽ - 1",
        '1_rach_prognoz': "💠 {price_1_vip}₽ - 1 VIP",
        '5_ob_prognoz': "🔹 {price_5_ob}₽ - 5",
        '5_rach_prognoz': "💠 {price_5_vip}₽ - 5 VIP",
        '15_ob_prognoz': "🔹 {price_15_ob}₽ - 15",
        '15_rach_prognoz': "💠 {price_15_vip}₽ - 15 VIP",

        'ob_prognoz': "🔹 Прогноз",
        'vip_prognoz': "💠 VIP Прогноз",
        'profile': "👤 Профиль",
        'vibirite_tip_prognoza': "📊 Выберите тип прогноза:",

        'read_otzivi': "👥 Почитать отзывы",
        'ostvit_otziv': "🆕 Оставить отзыв",
        'vip_prognozov': "VIP-прогнозов",
        'ob_progozov': "обычных прогнозов",
        'dobavleno_prognozov': "✅ {count} {label} добавлено!",
        'iazik': "🌐 Поменять язык",
        'iazik_yes': "✅ Язык выбран!",
        'vibr_iazik': "🌐 Выберите язык:",
        'partners_header': "<b>Партнёры:</b>",
        'subscribe_to': "Подписаться на",

        # === НОВЫЙ БЛОК: Инструкция ===
        'instruction_menu_header': "📘 <b>Инструкция</b>\n\nВыберите раздел, который вас интересует:",
        'full_instruction_button': "📘 Читать полную инструкцию",
        'instruction_link': "https://telegra.ph/INSTRUKCIYA-PO-ISPOLZOVANIYU-SPORT-ANALITIK-BOT-06-23",
        'instruction_blocks': {

            'kakrabotaetbot': {
                'title': "⚙️ Как работает бот?",
                'text': '''
- Бот @SportNeyroAnalitikbot на основе специально обученных нейросетей для анализа данных, дает подробную аналитику спортивных событий, бот обновляется и тестируется, все ваши отзывы учитываются! 

<b>1. Сбор данных:</b>
Бот собирает данные из множества источников, учитываются параметры влияющие на исход матча. 

<b>2. Прогнозирование результатов:</b>
На основе анализа бот создаёт прогноз вероятного исхода матча, учитывая собранную информацию.

<b>3. Развёрнутая аналитика:</b>
Пользователь получает не просто цифры, а объяснение ключевых факторов. 

<b>4. Обновление в реальном времени:</b>
Алгоритмы постоянно совершенствуются, обеспечивая высокую точность прогнозов. 

❤️ <i>Мы стремимся сделать спортивную аналитику доступной каждому. Будь вы болельщиком, профессиональным аналитиком или участником букмекерского рынка.</i>
                '''
            },
            'podpiski': {
                'title': "🎫 Подписки",
                'text': '''
‼️ <b>ВАЖНО:</b>
1. При покупке новой подписки, активная подписка (если она есть) сгорает.
2. По окончании срока действия подписки все неиспользованные временные прогнозы аннулируются.

🎫 <b>Standart</b> — <i>199₽ / неделя</i> | 5 обычных прогнозов, 0 VIP-прогнозов.

Идеально для новичков и тех, кто предпочитает выбирать события самостоятельно.

🎫 <b>Medium</b> — <i>999₽ / неделя</i> | 12 обычных прогнозов, 6 VIP-прогнозов.

Подходит для опытных пользователей, желающих углубиться в аналитику.

🎫 <b>Premium</b> — <i>1899₽ / 2 недели</i> | 30 обычных прогнозов, 15 VIP-прогнозов.

Максимальная выгода для активных игроков.

<b>Почему подписки выгодны?</b> Подписки позволяют экономить деньги. Покупка отдельных прогнозов может обойтись дороже, чем приобретение подписки на определённый период. 

<b>Если вы планируете регулярно делать ставки</b>, подписка окажется значительно выгоднее разовых покупок. 
                '''
            },
            'prognozi': {
                'title': "🔹 Прогнозы / 💠 VIP-прогнозы",
                'text': '''
🔷 <b>Обычные прогнозы (краткая аналитика):</b>

Обычный прогноз содержит краткую и ясную информацию о предстоящем матче или событии. Он включает основные данные, такие как предполагаемый исход матча, коэффициенты и ключевые факторы, влияющие на результат. Этот тип прогноза подходит для тех, кто хочет быстро получить основную информацию перед ставкой. 

🪙 <b>Цены:</b>

59 ₽ — 1 прогноз 
249 ₽ — 5 прогнозов <i>(экономия 15.6%)</i>
450 ₽ — 15 прогнозов <i>(экономия 49.2%)</i>

💠 <b>VIP-прогнозы (детальный анализ):</b>

VIP-прогнозы предоставляют более глубокий и детальный анализ спортивного события. Помимо основной информации, они включают дополнительные данные и более развернутый ответ для лучшего понимания приближающегося матча, и другие важные аспекты, которые могут повлиять на исход матча. Эти прогнозы помогут вам лучше понять ситуацию и сделать более взвешенное решение. 

🪙 <b>Цены:</b>

99 ₽ — 1 VIP прогноз 
399 ₽ — 5 VIP прогнозов <i>(экономия 19.4%)</i>
1159 ₽ — 15 VIP прогнозов <i>(экономия 22.0%)</i>
'''
            },
            'buy': {
                'title': "💳 Покупки",
                'text': '''
💳 Приобретение прогноза                
                
Чтобы приобрести обычный или VIP-прогноз, воспользуйтесь разделом «Каталог» в главном меню бота.

<b>Шаг 1:</b> В главном меню бота выберите кнопку «Каталог». 
<b>Шаг 2:</b> Внутри «Каталога» выберите раздел «Прогнозы». 
<b>Шаг 3:</b> Выберите желаемое количество обычных или VIP-прогнозов. 
<b>Шаг 4:</b> Следуйте инструкциям бота для завершения оплаты.

—————————-

💳 Приобретение подписки

Для покупки подписки, предоставляющей доступ к большему количеству прогнозов и VIP-прогнозов по выгодным ценам, следуйте этим шагам:

<b>Шаг 1:</b> В главном меню бота выберите кнопку «Каталог». 
<b>Шаг 2:</b> Внутри «Каталога» выберите раздел «Подписки». 
<b>Шаг 3:</b> Выберите подходящий вам тип подписки 
(Standart, Medium или Premium). 
<b>Шаг 4:</b> Следуйте инструкциям бота для завершения оплаты.
                '''
            },
            'createprognoz': {
                'title': "👨‍💻 Создание прогноза",
                'text': '''
🤖 <b>Бот</b> @SportNeyroAnalitikbot позволяет вам создавать прогнозы по запросу, что бы создать прогнозвам нужно:

<b>1 Шаг:</b> В главном меню бота выберите кнопку «Создать прогноз».
<b>2 Шаг:</b> После обработки запроса и аналитики матча, бот предоставит вам прогноз.

‼️ <b>ВАЖНО</b>
Заполняйте информацию о матче правильно и внимательно, так как если вы совершите ошибку, возврат потраченных средств не предусмотрен.
            '''
            },
            'promokodi': {
                'title': "🎟 Промокоды",
                'text': '''
<b>Промокоды в боте @SportNeyroAnalitikbot предоставляют вам дополнительные бонусы.</b>

<b>Шаг 1:</b> В главном меню бота выберите кнопку «Промокод». 
<b>Шаг 2:</b> Введите свой промокод в соответствующее поле. 
<b>Шаг 3:</b> Нажмите «Применить» для активации промокода и получения бонусов.

🔭 Следите за новостями канала <a href="https://t.me/NeyroTeamTg">Neyro Team</a>, чтобы не пропустить новые промокоды.
                '''
            },
            'bukmekeri': {
                'title': "✅ Лучшие букмекеры",
                'text': '''
👍 <b>Для размещения ставок на спорт, основываясь на полученных от бота прогнозах, мы рекомендуем использовать следующих проверенных букмекерских партнёров:</b>

<b>1Win:</b> <i>https://1wzyuh.com/v3/landing-page/football?p=5ibz</i>
При регистрации по промокоду "NEYRO99" вы получите бонусы.
<b>Winline:</b> <i>https://partners2.winline.ru/s/Ebp0XjlFwM?statid=2925_</i>
При регистрации по промокоду "NEYRO3000" вы получите бонусы.
                '''
            },
            'ozivi': {
                'title': "🗣 Отзывы",
                'text': '''
♥️ <b>Ваше мнение очень важно для нас!</b> Вы можете оставлять отзывы о работе бота и знакомиться с мнениями других пользователей.

✍️ <b>Оставить отзыв:</b> Чтобы поделиться своим мнением, перейдите в бота @OtzivNeyroTeambot или выберите кнопку «Оставить отзыв» в разделе «Отзывы» в меню @SportNeyroAnalitikbot. Следуйте инструкциям бота для написания отзыва. 

🗣 <b>Ознакомиться с отзывами:</b> Чтобы прочитать отзывы других пользователей, выберите кнопку «Почитать отзывы» в разделе «Отзывы» в меню @SportNeyroAnalitikbot или перейдите в тг канал @OTZIVISPORTANALITIK
                '''
            },
            'iaziki': {
                'title': "🌍 Языки",
                'text': '''
<b>Бот @SportNeyroAnalitikbot создан для глобальной аудитории и поддерживает 6 международных языков ООН: </b>

🇷🇺🇬🇧🇪🇸🇨🇳🇫🇷🇸🇦

Русский, English, Español, 中文, Français,  العربية 

Вы можете легко изменить язык интерфейса бота, выбрав соответствующую опцию в главном меню бота. Это позволяет пользоваться всеми функциями бота максимально комфортно, независимо от вашего региона.
                '''
            },
            'refi': {
                'title': "🤝 Реферальная программа",
                'text': '''
🫂 У каждого пользователя @SportNeyroAnalitikbot есть возможность участвовать в нашей реферальной программе и получать бонусы за приглашённых друзей.

• <b>Ваша реферальная ссылка:</b> Каждая учётная запись в боте имеет уникальную реферальную ссылку. Вы можете найти её в своём «Профиле».
• <b>Как это работает:</b> Поделитесь своей уникальной реферальной ссылкой с друзьями. Когда ваш друг перейдёт по вашей ссылке, зарегистрируется в боте и совершит первую покупку (любой подписки или прогноза), вы оба получите бонус.
• <b>Бонус:</b> За каждого реферала, совершившего покупку, и вы, и ваш приглашённый друг получаете 1 VIP-прогноз.
• <b>Отслеживание:</b> Количество приглашённых друзей отображается в вашем «Профиле».

<b>Чем больше друзей вы пригласите, тем больше бонусов сможете получить!</b>
                '''
            },
            'partnerstvo': {
                'title': "💼 Партнёрство",
                'text': '''
💸 Если вы рекламодатель, траффер или заинтересованы во взаимной рекламе, вы можете связаться с нашей службой поддержки в Telegram по адресу @SuportNeyroTeam для обсуждения условий сотрудничества.
                '''
            }

        },

        # === НОВЫЙ БЛОК: Поддержка и FAQ ===
        'support_menu_header': "⚙️ <b>Поддержка</b>\n\n➖➖➖➖➖➖➖➖➖\n\nЕсли у вас возникли вопросы, вы можете найти ответы в разделе Часто задаваемые вопросы или написать в нашу службу поддержки.\n\n➖➖➖➖➖➖➖➖➖",
        'faq_button': "⁉️ Часто задаваемые вопросы (FAQ)",
        'contact_support_button': "👨‍💻 Написать в поддержку",
        'faq_menu_header': "❓ <b>Часто задаваемые вопросы</b> ❓",
        'faq_items': {
            'q1': {
                'question': "⚙️ Как работает бот?  ",
                'answer': '''
- Бот @SportNeyroAnalitikbot на основе специально обученных нейросетей для анализа данных, дает подробную аналитику спортивных событий, бот обновляется и тестируется, все ваши отзывы учитываются! 

<b>1. Сбор данных:</b>
Бот собирает данные из множества источников, учитываются параметры влияющие на исход матча. 

<b>2. Прогнозирование результатов:</b>
На основе анализа бот создаёт прогноз вероятного исхода матча, учитывая собранную информацию.

<b>3. Развёрнутая аналитика:</b>
Пользователь получает не просто цифры, а объяснение ключевых факторов. 

<b>4. Обновление в реальном времени:</b>
Алгоритмы постоянно совершенствуются, обеспечивая высокую точность прогнозов. 

❤️ <i>Мы стремимся сделать спортивную аналитику доступной каждому. Будь вы болельщиком, профессиональным аналитиком или участником букмекерского рынка.</i>
                '''
            },
            'q2': {
                'question': "🎫 Как работают подписки?",
                'answer': '''
🎫 Подписки предоставляют доступ к определенному количеству временных обычных и VIP-прогнозов на фиксированный период <i>(неделя, две недели)</i>. 

💎 Они предлагают более <b>выгодные цены</b> по сравнению с покупкой отдельных прогнозов. 

‼️ <b>Важно помнить</b>, что при покупке новой подписки старая сгорает, а неиспользованные временные прогнозы аннулируются по окончании срока подписки.
                '''
            },
            'q3': {
                'question': "📊 Как работают прогнозы?",
                'answer': '''
<b>Бот предлагает два типа прогнозов:</b>

🔹 <b>Обычные прогнозы:</b> Предоставляют краткую информацию об исходе матча, коэффициентах и ключевых факторах.

💠 <b>VIP-прогнозы:</b> Предлагают более глубокий и детальный анализ, включая дополнительные данные и развернутые объяснения для принятия более взвешенных решений.
'''
            },
            'q4': {
                'question': "⏳ Отличие временных прогнозов? ",
                'answer': '''
⏳ При приобретении подписки вы получаете именно <b>временные прогнозы</b> которые будут доступны до окончания срока подписки, например, если вы планируете делать ставки регулярно, то покупка подписки окажется гораздо выгоднее, чем разовые покупки.
                '''
            },
            'q5': {
                'question': "💳 Как купить подписку?",
                'answer': '''
💳 Для покупки подписки перейдите в «Каталог» в главном меню бота, затем выберите «Подписки» и нужный вам тариф. Следуйте инструкциям бота для оплаты.
                '''
            },
            'q6': {
                'question': "💳 Как купить прогнозы?",
                'answer': '''
💳 Для покупки прогнозов перейдите в «Каталог» в главном меню бота, затем выберите «Прогнозы» и необходимое количество обычных или VIP-прогнозов. Следуйте инструкциям бота для оплаты.
'''
            },
            'q7': {
                'question': "📊 Как создать прогноз?",
                'answer': '''
📊 Чтобы создать прогноз по запросу, выберите кнопку «Создать прогноз» в главном меню бота. Затем введите необходимую информацию о спортивном событии, следуя подсказкам бота.
'''
            },
            'q8': {
                'question': "🎟 Как работают промокоды? ",
                'answer': '''
🎟 Промокоды вводятся в специальном разделе «Промокод» в главном меню бота. Они активируют бонусы, которые могут быть предоставлены командой Neyro Team. Также существуют промокоды для получения бонусов при регистрации у букмекерских партнёров.
'''
            },
            'q9': {
                'question': "✍️ Как оставить отзыв?",
                'answer': '''
✍️ Вы можете оставить отзыв, перейдя в бота @OtzivNeyroTeambot или выбрав кнопку «Оставить отзыв» в разделе «Отзывы» в меню @SportNeyroAnalitikbot.
                '''
            },
            'q10': {
                'question': "👀 Где ознакомиться с отзывами?",
                'answer': '''
👀 Ознакомиться с отзывами других пользователей можно, выбрав кнопку «Почитать отзывы» в разделе «Отзывы» в меню @SportNeyroAnalitikbot.
'''
            },
            'q11': {
                'question': "✅ Где ставить на спорт?",
                'answer': '''
✔️ Для размещения ставок на спорт, основываясь на полученных от бота прогнозах, мы рекомендуем использовать следующих проверенных букмекерских партнёров:

<b>1Win:</b> <i>https://1wzyuh.com/v3/landing-page/football?p=5ibz</i>
(Промокод: NEYRO99)
<b>Winline:</b> <i>https://partners2.winline.ru/s/Ebp0XjlFwM?statid=2925_</i>
(Промокод: NEYRO3000)
                '''
            },
            'q12': {
                'question': "🌍 На каких языках доступен бот?",
                'answer': '''
Бот @SportNeyroAnalitikbot поддерживает 6 международных языков 🌍 ООН: русский, английский, арабский, испанский, китайский и французский. Вы можете выбрать желаемый язык в настройках бота.
                '''
            },
            'q13': {
                'question': "🤝 Как работает реферальная программа?",
                'answer': '''
🫂 У каждого пользователя @SportNeyroAnalitikbot есть возможность участвовать в нашей реферальной программе и получать бонусы за приглашённых друзей.

• <b>Ваша реферальная ссылка:</b> Каждая учётная запись в боте имеет уникальную реферальную ссылку. Вы можете найти её в своём «Профиле».
• <b>Как это работает:</b> Поделитесь своей уникальной реферальной ссылкой с друзьями. Когда ваш друг перейдёт по вашей ссылке, зарегистрируется в боте и совершит первую покупку (любой подписки или прогноза), вы оба получите бонус.
• <b>Бонус:</b> За каждого реферала, совершившего покупку, и вы, и ваш приглашённый друг получаете 1 VIP-прогноз.
• <b>Отслеживание:</b> Количество приглашённых друзей отображается в вашем «Профиле».

<b>Чем больше друзей вы пригласите, тем больше бонусов сможете получить!</b>
                '''
            },
            'q14': {
                'question': '''💼 Как стать партнером "Neyro Team"?''',
                'answer': '''
💸 Если вы <b>рекламодатель, траффер или заинтересованы во взаимной рекламе</b>, вы можете связаться с нашей службой поддержки в Telegram по адресу @SuportNeyroTeam для обсуждения условий сотрудничества.
'''
            }
        },

        # === НОВЫЙ БЛОК: Пути к изображениям ===
        'photo_profil': "images/ru/profil.png",
        'photo_katalog': "images/ru/katalog.png",
        'photo_katalog_prognoz': "images/ru/katalog_prognoz.png",
        'photo_katalog_subscriptions': "images/ru/katalog_subscriptions.png",
        'photo_otzivi': "images/ru/otzivi.png",
        'photo_tip_prognoza': "images/ru/tip_prognoza.png",
        'ob_prognoz_photo': "images/ru/ob_prognoz.png",
        'vip_prognoz_photo': "images/ru/vip_prognoz.png",
        'photo_instruction': "images/ru/instruction.png",  # Добавьте реальный путь
        'photo_support': "images/ru/support.png",  # Добавьте реальный путь
        'photo_faq': "images/ru/faq.png",  # Добавьте реальный путь
        'photo_cponsori': "images/ru/cponsori.png"
    },

    'en': {
        # ==============================
        # 1. General commands and messages
        # ==============================
        'start': "✅ Start the bot",
        'admin': "👨‍💻 Admin Panel",
        'cancel': "🔙 Cancel",
        'traffer': "🥷 Trafficker Panel",
        'cancel_disvie': "🚫 Action cancelled.",

        'traff_info': '''
👤 Trafficker: {trafer_name}
👤 Username: {t_username}
🆔 ID: {t_id}
🏷️ Promo Code: {t_promo}

📱 Phone: {t_telefon}
💳 Card: {t_karta}
🪙 Crypto: {t_kripta}
🔗 Network: {crypto_network}

📊 Earning Method: {human_model}
📊 Leads: {leads}

🏦 On Balance: {balance}₽
💸 Withdrawn: {paid}₽
💰 Total Earned: {total}₽
                ''',

        'edit_traffera': "✏️ Edit Trafficker",
        'obnovit_traf_info': "🔄 Update",
        'traff_id_kanala': "🆔 Channel ID: {pay_link}",
        'traff_priglos_ssilka': "🔗 Invitation Link:\n{invite_link}",
        'del_traffera': "❌ Delete Trafficker",
        'back': "↩️ Back",
        'obnovit_podpiski': "🔄 Update Subscriptions",
        'vivisti_money': "💸 Withdraw Money",
        'back_traff_panel': "🔙 Exit Trafficker Panel",
        'command_start': "Start the bot",
        'command_admin': "Admin Panel",
        'command_traffer': "Trafficker Panel",
        'podpiska_istekla': "Subscription expired",
        'bolche_day': "{days} days {hours} hrs.",
        'menche_day': "{hours} hrs {minutes} min.",
        'menche_hour': "{minutes} min.",
        'spasibo_za_oplaty': "Thank you for your payment! Access activated.",
        'chek_partners': "🔁 Check Subscription",
        'pustoy_spisok_partners': "Partner list is empty",
        'NO_chek_partners': "Please subscribe to all partners to continue.",

        'edit_name': "Name",
        'edit_id': "ID",
        'edit_username': "@User_name",
        'edit_telefon': "Phone",
        'edit_karta': "Card",
        'edit_kripta': "Crypto Wallet",
        'edit_crypto_network': "Crypto Network",
        'cancel_edit': "↩️ Cancel",

        # NEW: Prompts for editing
        'enter_new_name': "Enter new name:",
        'enter_new_id': "Enter new ID:",
        'enter_new_username': "Enter new @User_name:",
        'enter_new_telefon': "Enter new phone:",
        'enter_new_karta': "Enter new card:",
        'enter_new_kripta': "Enter new crypto wallet:",
        'enter_new_crypto_network': "Enter new crypto network:",
        'traffer_updated_success': "✅ Trafficker data updated!",
        'no_traffer_found': "Trafficker not found.",

        "referral_reward": "You received 1 permanent VIP prediction as a referral reward!",
        "profile_text": '''
➖➖➖➖➖➖➖➖➖

👤 *{user_name}* | *ID:* `{user_id}`
🎫 *Subscription:* *{subscription}*
⌛️ *Expires in:* *{remaining}*

🔹 *Predictions:* *{ob_prognoz}*
💠 *VIP Predictions:* *{rach_prognoz}*
🔹 *Temporary Predictions:* *{ob_vr_prognoz}*
💠 *Temporary VIP Predictions:* *{rach_vr_prognoz}*

👥 *Invited Friends:* {referred_count}
🔗 *Your Referral Link:*

`{referral_link}`

➖➖➖➖➖➖➖➖➖

‼️ *Beta test in progress*
All functions are available for free.

➖➖➖➖➖➖➖➖➖
                ''',

        'sozdat_prognoz': "📊 Create Prediction",
        'katalog': "🛍 Catalog",
        'otzivi': "🗣️ Reviews",
        'promokod': "#️⃣ Promo Code",
        'support': "⚙️ Support",
        'instruction': "📘 Instructions",
        'error_profile': "Error getting profile data.",

        'NOT_od_prognoz': "❌ You have no regular predictions!",
        'NOT_VIP_prognoz': "❌ You have no VIP predictions!",
        'vvedite_daty_vremia': "🗓 Enter match date and time (e.g., 01.01.2025 18:00):",
        'vvedite_vid_sporta': "⚽️ Enter sport type (e.g., football):",
        'vvedite_commandi': "👥 Enter team names separated by comma (Team #1, Team #2):",

        'error_vvedite_commandi': '''
Please enter exactly two team names, separated by a comma
(e.g., Team1, Team2).
                ''',

        'message_promokod': '''
✅ Promo code accepted!
You have been added 🔹 {add_ob_prognoz} regular prediction(s) and 💠 {add_rach_prognoz} VIP prediction(s).
🎫 Subscription: {subscription}
                ''',

        'vvevite_promocod_1': "⏳ Enter promo code",
        'vvevite_promocod_2': "Enter promo code:",
        'primenit_promocod': "✅ Apply Promo Code",
        'najmi_primenit_promocod': "Click the button below to apply the promo code 👇",
        'yes_promocod_ot_traffera': "✅ Promo code from trafficker accepted! 1 regular prediction added.",
        'ispolzovan_promocod': "❌ You have already used this promo code.",
        'nedeistvitelen_promocod': "❌ This promo code is no longer valid.",
        'promocod_ne_nayden': "❌ Promo code not found.",

        'promocod_ot_traffera_YES': '''
✅ Promo code activated!
+ 1 regular prediction.
                ''',

        'error_close_panel': "Failed to close panel 😔",

        'yes_dannie': "✅ Confirm data",
        'no_dannie': "🔄 Fill again",
        'obrabotka_prognoza': "⏳ Your prediction is being processed…",
        'no_registr_traffera': "⛔ You are not registered as a trafficker.",
        'balans_menche_1000': "Withdrawal available from 1000 ₽",
        'ot_1000_do_balans': "Enter withdrawal amount (from 1000 to {balance}₽):",
        'vvedite_celoe_chislo': "Enter an integer!",
        'summa_bolche_1000': "Amount must be at least 1000 ₽!",
        'summa_bolche_balansa': "Amount exceeds your current balance!",
        'redactirovat': "✏️ Edit",
        'podtverdit': "✅ Confirm",
        'proverka_summi': "Do you want to withdraw {amt}₽?",
        'yes_viplata': "✅ Withdrawal of {amt}₽ successful.",
        'no_viplata': "❌ Withdrawal of {amt}₽ not accepted. Contact support: https://t.me/suportneyroteam",

        'katalog_podpisok': '''
➖➖➖➖➖➖➖➖➖

🎫 *{price_standart}₽ - Standart* for a week
You will have access to 5 predictions, 0 VIP predictions

🎫 *{price_medium}₽ - Medium* for a week
You will have access to 12 predictions, 6 VIP predictions

🎫 *{price_premium}₽ - Premium* for two weeks
You will have access to 30 predictions, 15 VIP predictions

➖➖➖➖➖➖➖➖➖

‼️ *Beta test in progress*
All functions are available for free.

➖➖➖➖➖➖➖➖➖

💳 Select a subscription for payment below:
            ''',

    'katalog_prognozov': '''
➖➖➖➖➖➖➖➖➖➖➖➖➖➖

🔹 *{price_1_ob}₽* - 1 Prediction
🔹 *{price_5_ob}₽* - 5 Predictions
🔹 *{price_15_ob}₽* - 15 Predictions

💠 *{price_1_vip}₽* - 1 VIP Prediction
💠 *{price_5_vip}₽* - 5 VIP Predictions
💠 *{price_15_vip}₽* - 15 VIP Predictions

➖➖➖➖➖➖➖➖➖➖➖➖➖➖

‼️ *Beta test in progress*
All functions are available for free.

➖➖➖➖➖➖➖➖➖➖➖➖➖➖

💳 Select a package for payment below:
                ''',

        'standart': "💥 Your subscription has been upgraded to Standart for a week!",
        'medium': "💥 Your subscription has been upgraded to Medium for a week!",
        'premium': "💥 Your subscription has been upgraded to Premium for 2 weeks!",
        'podpiski': "🎫 Subscriptions",
        'prognozi': "📊 Predictions",
        'catalog_text': "Welcome to the catalog! Select a section:",
        '1_ob_prognoz': "🔹 {price_1_ob}₽ - 1",
        '1_rach_prognoz': "💠 {price_1_vip}₽ - 1 VIP",
        '5_ob_prognoz': "🔹 {price_5_ob}₽ - 5",
        '5_rach_prognoz': "💠 {price_5_vip}₽ - 5 VIP",
        '15_ob_prognoz': "🔹 {price_15_ob}₽ - 15",
        '15_rach_prognoz': "💠 {price_15_vip}₽ - 15 VIP",

        'ob_prognoz': "🔹 Prediction",
        'vip_prognoz': "💠 VIP Prediction",
        'profile': "👤 Profile",
        'vibirite_tip_prognoza': "📊 Select prediction type:",

        'read_otzivi': "👥 Read Reviews",
        'ostvit_otziv': "🆕 Leave a Review",
        'vip_prognozov': "VIP predictions",
        'ob_progozov': "regular predictions",
        'dobavleno_prognozov': "✅ {count} {label} added!",
        'iazik': "🌐 Change Language",
        'iazik_yes': "✅ Language selected!",
        'vibr_iazik': "🌐 Select language:",
        'partners_header': "<b>Partners:</b>",
        'subscribe_to': "Subscribe to",

        # === NEW BLOCK: Instructions ===
        'instruction_menu_header': "📘 <b>Instructions</b>\n\nSelect the section you are interested in:",
        'full_instruction_button': "📘 Read full instructions",
        'instruction_link': "https://telegra.ph/INSTRUCTION-FOR-USING-SPORT-ANALYTIK-BOT-07-01",
        'instruction_blocks': {

            'kakrabotaetbot': {
                'title': "⚙️ How does the bot work?",
                'text': '''
- The @SportNeyroAnalitikbot bot, based on specially trained neural networks for data analysis, provides detailed analytics of sports events. The bot is updated and tested, all your feedback is taken into account!

<b>1. Data collection:</b>
The bot collects data from many sources, taking into account parameters influencing the outcome of the match.

<b>2. Predicting results:</b>
Based on the analysis, the bot creates a prediction of the likely outcome of the match, considering the collected information.

<b>3. Detailed analytics:</b>
The user receives not just numbers, but an explanation of key factors.

<b>4. Real-time updates:</b>
Algorithms are constantly being improved, ensuring high accuracy of predictions.

❤️ <i>We strive to make sports analytics accessible to everyone. Whether you are a fan, a professional analyst, or a participant in the betting market.</i>
                '''
            },
            'podpiski': {
                'title': "🎫 Subscriptions",
                'text': '''
‼️ <b>IMPORTANT:</b>
1. When purchasing a new subscription, the active subscription (if any) is canceled.
2. Upon expiration of the subscription, all unused temporary predictions are voided.

🎫 <b>Standart</b> — <i>199₽ / week</i> | 5 regular predictions, 0 VIP predictions.

Ideal for beginners and those who prefer to choose events independently.

🎫 <b>Medium</b> — <i>999₽ / week</i> | 12 regular predictions, 6 VIP predictions.

Suitable for experienced users who want to delve deeper into analytics.

🎫 <b>Premium</b> — <i>1899₽ / 2 weeks</i> | 30 regular predictions, 15 VIP predictions.

Maximum benefit for active players.

<b>Why are subscriptions profitable?</b> Subscriptions save you money. Buying individual predictions can be more expensive than purchasing a subscription for a certain period.

<b>If you plan to bet regularly</b>, a subscription will be significantly more profitable than one-time purchases.
                '''
            },
            'prognozi': {
                'title': "🔹 Predictions / 💠 VIP Predictions",
                'text': '''
🔷 <b>Regular predictions (brief analytics):</b>

A regular prediction contains brief and clear information about an upcoming match or event. It includes basic data such as the predicted outcome of the match, odds, and key factors influencing the result. This type of prediction is suitable for those who want to quickly get basic information before betting.

🪙 <b>Prices:</b>

59 ₽ — 1 prediction
249 ₽ — 5 predictions <i>(save 15.6%)</i>
450 ₽ — 15 predictions <i>(save 49.2%)</i>

💠 <b>VIP predictions (detailed analysis):</b>

VIP predictions provide a deeper and more detailed analysis of a sports event. In addition to basic information, they include additional data and a more detailed response for better understanding of the upcoming match, and other important aspects that may affect the outcome of the match. These predictions will help you better understand the situation and make a more informed decision.

🪙 <b>Prices:</b>

99 ₽ — 1 VIP prediction
399 ₽ — 5 VIP predictions <i>(save 19.4%)</i>
1159 ₽ — 15 VIP predictions <i>(save 22.0%)</i>
    '''
            },
            'buy': {
                'title': "💳 Purchases",
                'text': '''
💳 Purchasing a prediction

To purchase a regular or VIP prediction, use the "Catalog" section in the bot's main menu.

<b>Step 1:</b> In the bot's main menu, select the "Catalog" button.
<b>Step 2:</b> Inside the "Catalog", select the "Predictions" section.
<b>Step 3:</b> Select the desired number of regular or VIP predictions.
<b>Step 4:</b> Follow the bot's instructions to complete the payment.

—————————-

💳 Purchasing a subscription

To purchase a subscription, which provides access to more predictions and VIP predictions at favorable prices, follow these steps:

<b>Step 1:</b> In the bot's main menu, select the "Catalog" button.
<b>Step 2:</b> Inside the "Catalog", select the "Subscriptions" section.
<b>Step 3:</b> Select the appropriate subscription type for you
(Standart, Medium, or Premium).
<b>Step 4:</b> Follow the bot's instructions to complete the payment.
                '''
            },
            'createprognoz': {
                'title': "👨‍💻 Creating a prediction",
                'text': '''
🤖 <b>The bot</b> @SportNeyroAnalitikbot allows you to create predictions on demand. To create a prediction you need to:

<b>Step 1:</b> In the main menu of the bot, select the "Create prediction" button.
<b>Step 2:</b> After processing the request and analyzing the match, the bot will provide you with a prediction.

‼️ <b>IMPORTANT</b>
Fill in the match information correctly and carefully, as if you make a mistake, there will be no refund.
                '''
            },
            'promokodi': {
                'title': "🎟 Promo Codes",
                'text': '''
<b>Promo codes in the @SportNeyroAnalitikbot bot provide you with additional bonuses.</b>

<b>Step 1:</b> In the bot's main menu, select the "Promo Code" button.
<b>Step 2:</b> Enter your promo code in the corresponding field.
<b>Step 3:</b> Click "Apply" to activate the promo code and receive bonuses.

🔭 Follow the news of the <a href="https://t.me/NeyroTeamTg">Neyro Team</a> channel so you don't miss new promo codes.
                '''
            },
            'bukmekeri': {
                'title': "✅ Best Bookmakers",
                'text': '''
👍 <b>To place sports bets, based on the predictions received from the bot, we recommend using the following verified betting partners:</b>

<b>1Win:</b> <i>https://1wzyuh.com/v3/landing-page/football?p=5ibz</i>
When registering with the promo code "NEYRO99" you will receive bonuses.
<b>Winline:</b> <i>https://partners2.winline.ru/s/Ebp0XjlFwM?statid=2925_</i>
When registering with the promo code "NEYRO3000" you will receive bonuses.
                '''
            },
            'ozivi': {
                'title': "🗣 Reviews",
                'text': '''
♥️ <b>Your opinion is very important to us!</b> You can leave reviews about the bot's work and read the opinions of other users.

✍️ <b>Leave a review:</b> To share your opinion, go to the @OtziviSportbot bot or select the "Leave a review" button in the "Reviews" section in the @SportNeyroAnalitikbot menu. Follow the bot's instructions to write a review.

🗣 <b>Read reviews:</b> To read reviews from other users, select the "Read reviews" button in the "Reviews" section in the @SportNeyroAnalitikbot menu or go to the Telegram channel @OTZIVISPORTANALITIK
                '''
            },
            'iaziki': {
                'title': "🌍 Languages",
                'text': '''
<b>The @SportNeyroAnalitikbot bot is created for a global audience and supports 6 UN international languages:</b>

🇷🇺🇬🇧🇪🇸🇨🇳🇫🇷🇸🇦

Russian, English, Español, 中文, Français, العربية

You can easily change the bot's interface language by selecting the appropriate option in the bot's main menu. This allows you to use all the bot's functions as comfortably as possible, regardless of your region.
                '''
            },
            'refi': {
                'title': "🤝 Referral Program",
                'text': '''
🫂 Every user of @SportNeyroAnalitikbot has the opportunity to participate in our referral program and receive bonuses for invited friends.

• <b>Your referral link:</b> Each account in the bot has a unique referral link. You can find it in your "Profile".
• <b>How it works:</b> Share your unique referral link with friends. When your friend clicks on your link, registers in the bot, and makes their first purchase (any subscription or prediction), both of you will receive a bonus.
• <b>Bonus:</b> For each referral who makes a purchase, both you and your invited friend receive 1 VIP prediction.
• <b>Tracking:</b> The number of invited friends is displayed in your "Profile".

<b>The more friends you invite, the more bonuses you can get!</b>
                '''
            },
            'partnerstvo': {
                'title': "💼 Partnership",
                'text': '''
💸 If you are an advertiser, trafficker, or are interested in mutual advertising, you can contact our support service on Telegram at @SuportNeyroTeam to discuss cooperation terms.
                '''
            }

        },

        # === NEW BLOCK: Support and FAQ ===
        'support_menu_header': "⚙️ <b>Support</b>\n\nIf you have any questions, you can find answers in the Frequently Asked Questions section or write to our support service.",
        'faq_button': "⁉️ Frequently Asked Questions (FAQ)",
        'contact_support_button': "👨‍💻 Write to Support",
        'faq_menu_header': "❓ <b>Frequently Asked Questions</b> ❓",
        'faq_items': {
            'q1': {
                'question': "⚙️ How does the bot work?",
                'answer': '''
- The @SportNeyroAnalitikbot bot, based on specially trained neural networks for data analysis, provides detailed analytics of sports events. The bot is updated and tested, all your feedback is taken into account!

<b>1. Data collection:</b>
The bot collects data from many sources, taking into account parameters influencing the outcome of the match.

<b>2. Predicting results:</b>
Based on the analysis, the bot creates a prediction of the likely outcome of the match, considering the collected information.

<b>3. Detailed analytics:</b>
The user receives not just numbers, but an explanation of key factors.

<b>4. Real-time updates:</b>
Algorithms are constantly being improved, ensuring high accuracy of predictions.

❤️ <i>We strive to make sports analytics accessible to everyone. Whether you are a fan, a professional analyst, or a participant in the betting market.</i>
                '''
            },
            'q2': {
                'question': "🎫 How do subscriptions work?",
                'answer': '''
🎫 Subscriptions provide access to a certain number of temporary regular and VIP predictions for a fixed period <i>(week, two weeks)</i>.

💎 They offer more <b>favorable prices</b> compared to purchasing individual predictions.

‼️ <b>It is important to remember</b> that when purchasing a new subscription, the old one is canceled, and unused temporary predictions are voided upon expiration of the subscription.
                '''
            },
            'q3': {
                'question': "📊 How do predictions work?",
                'answer': '''
<b>The bot offers two types of predictions:</b>

🔹 <b>Regular predictions:</b> Provide brief information about the match outcome, odds, and key factors.

💠 <b>VIP predictions:</b> Offer a deeper and more detailed analysis, including additional data and expanded explanations for making more informed decisions.
    '''
            },
            'q4': {
                'question': "⏳ What is the difference between temporary predictions?",
                'answer': '''
⏳ When purchasing a subscription, you receive exactly <b>temporary predictions</b> which will be available until the subscription expires. For example, if you plan to bet regularly, purchasing a subscription will be much more profitable than one-time purchases.
                '''
            },
            'q5': {
                'question': "💳 How to buy a subscription?",
                'answer': '''
💳 To purchase a subscription, go to "Catalog" in the bot's main menu, then select "Subscriptions" and your desired plan. Follow the bot's instructions for payment.
                '''
            },
            'q6': {
                'question': "💳 How to buy predictions?",
                'answer': '''
💳 To purchase predictions, go to "Catalog" in the bot's main menu, then select "Predictions" and the required number of regular or VIP predictions. Follow the bot's instructions for payment.
    '''
            },
            'q7': {
                'question': "📊 How to create a prediction?",
                'answer': '''
📊 To create an on-demand prediction, select the "Create Prediction" button in the bot's main menu. Then enter the necessary information about the sports event, following the bot's prompts.
    '''
            },
            'q8': {
                'question': "🎟 How do promo codes work?",
                'answer': '''
🎟 Promo codes are entered in a special "Promo Code" section in the bot's main menu. They activate bonuses that may be provided by the Neyro Team. There are also promo codes for receiving bonuses when registering with betting partners.
    '''
            },
            'q9': {
                'question': "✍️ How to leave a review?",
                'answer': '''
✍️ You can leave a review by going to the @OtziviSportbot bot or by selecting the "Leave a review" button in the "Reviews" section in the @SportNeyroAnalitikbot menu.
                '''
            },
            'q10': {
                'question': "👀 Where can I read reviews?",
                'answer': '''
👀 You can read reviews from other users by selecting the "Read reviews" button in the "Reviews" section in the @SportNeyroAnalitikbot menu.
    '''
            },
            'q11': {
                'question': "✅ Where to bet on sports?",
                'answer': '''
✔️ To place sports bets, based on the predictions received from the bot, we recommend using the following verified betting partners:

<b>1Win:</b> <i>https://1wzyuh.com/v3/landing-page/football?p=5ibz</i>
(Promo code: NEYRO99)
<b>Winline:</b> <i>https://partners2.winline.ru/s/Ebp0XjlFwM?statid=2925_</i>
(Promo code: NEYRO3000)
                '''
            },
            'q12': {
                'question': "🌍 What languages is the bot available in?",
                'answer': '''
The @SportNeyroAnalitikbot bot supports 6 international UN languages 🌍: Russian, English, Arabic, Spanish, Chinese, and French. You can select your desired language in the bot's settings.
                '''
            },
            'q13': {
                'question': "🤝 How does the referral program work?",
                'answer': '''
🫂 Every user of @SportNeyroAnalitikbot has the opportunity to participate in our referral program and receive bonuses for invited friends.

• <b>Your referral link:</b> Each account in the bot has a unique referral link. You can find it in your "Profile".
• <b>How it works:</b> Share your unique referral link with friends. When your friend clicks on your link, registers in the bot, and makes their first purchase (any subscription or prediction), both of you will receive a bonus.
• <b>Bonus:</b> For each referral who makes a purchase, both you and your invited friend receive 1 VIP prediction.
• <b>Tracking:</b> The number of invited friends is displayed in your "Profile".

<b>The more friends you invite, the more bonuses you can get!</b>
                '''
            },
            'q14': {
                'question': '''💼 How to become a "Neyro Team" partner?''',
                'answer': '''
💸 If you are an <b>advertiser, trafficker, or are interested in mutual advertising</b>, you can contact our support service on Telegram at @SuportNeyroTeam to discuss cooperation terms.
    '''
            }
        },

        # === NEW BLOCK: Image paths ===
        'photo_profil': "images/en/profil.png",
        'photo_katalog': "images/en/katalog.png",
        'photo_katalog_prognoz': "images/en/katalog_prognoz.png",
        'photo_katalog_subscriptions': "images/en/katalog_subscriptions.png",
        'photo_otzivi': "images/en/otzivi.png",
        'photo_tip_prognoza': "images/en/tip_prognoza.png",
        'ob_prognoz_photo': "images/en/ob_prognoz.png",
        'vip_prognoz_photo': "images/en/vip_prognoz.png",
        'photo_instruction': "images/en/instruction.png",
        'photo_support': "images/en/support.png",
        'photo_faq': "images/en/faq.png",
        'photo_cponsori': "images/en/cponsori.png"
    },
    'es': {
        # ==============================
        # 1. Comandos y mensajes generales
        # ==============================
        'start': "✅ Iniciar bot",
        'admin': "👨‍💻 Panel de administración",
        'cancel': "🔙 Cancelar",
        'traffer': "🥷 Panel de Trafficker",
        'cancel_disvie': "🚫 Acción cancelada.",

        'traff_info': '''
👤 Trafficker: {trafer_name}
👤 Nombre de usuario: {t_username}
🆔 ID: {t_id}
🏷️ Código promocional: {t_promo}

📱 Teléfono: {t_telefon}
💳 Tarjeta: {t_karta}
🪙 Cripto: {t_kripta}
🔗 Red: {crypto_network}

📊 Método de ganancia: {human_model}
📊 Leads: {leads}

🏦 En saldo: {balance}₽
💸 Retirado: {paid}₽
💰 Ganancia total: {total}₽
                ''',

        'edit_traffera': "✏️ Editar trafficker",
        'obnovit_traf_info': "🔄 Actualizar",
        'traff_id_kanala': "🆔 ID del canal: {pay_link}",
        'traff_priglos_ssilka': "🔗 Enlace de invitación:\n{invite_link}",
        'del_traffera': "❌ Eliminar trafficker",
        'back': "↩️ Atrás",
        'obnovit_podpiski': "🔄 Actualizar suscripciones",
        'vivisti_money': "💸 Retirar dinero",
        'back_traff_panel': "🔙 Salir del panel de Trafficker",
        'command_start': "Iniciar bot",
        'command_admin': "Panel de administración",
        'command_traffer': "Panel de Trafficker",
        'podpiska_istekla': "Suscripción caducada",
        'bolche_day': "{days} días {hours} hrs.",
        'menche_day': "{hours} hrs. {minutes} min.",
        'menche_hour': "{minutes} min.",
        'spasibo_za_oplaty': "¡Gracias por el pago! Acceso activado.",
        'chek_partners': "🔁 Verificar suscripción",
        'pustoy_spisok_partners': "La lista de socios está vacía",
        'NO_chek_partners': "Por favor, suscríbase a todos los socios para continuar.",

        'edit_name': "Nombre",
        'edit_id': "ID",
        'edit_username': "@User_name",
        'edit_telefon': "Teléfono",
        'edit_karta': "Tarjeta",
        'edit_kripta': "Monedero de criptomonedas",
        'edit_crypto_network': "Red de criptomonedas",
        'cancel_edit': "↩️ Cancelar",

        # NUEVO: Mensajes para editar
        'enter_new_name': "Ingrese nuevo nombre:",
        'enter_new_id': "Ingrese nuevo ID:",
        'enter_new_username': "Ingrese nuevo @User_name:",
        'enter_new_telefon': "Ingrese nuevo teléfono:",
        'enter_new_karta': "Ingrese nueva tarjeta:",
        'enter_new_kripta': "Ingrese nuevo monedero de criptomonedas:",
        'enter_new_crypto_network': "Ingrese nueva red de criptomonedas:",
        'traffer_updated_success': "✅ ¡Datos del trafficker actualizados!",
        'no_traffer_found': "Trafficker no encontrado.",

        "referral_reward": "¡Has recibido 1 pronóstico VIP permanente como recompensa por referido!",
        "profile_text": '''
➖➖➖➖➖➖➖➖➖

👤 *{user_name}* | *ID:* `{user_id}`
🎫 *Suscripción:* *{subscription}*
⌛️ *Vencimiento en:* *{remaining}*

🔹 *Pronósticos:* *{ob_prognoz}*
💠 *Pronósticos VIP:* *{rach_prognoz}*
🔹 *Pronósticos Temporales:* *{ob_vr_prognoz}*
💠 *Pronósticos VIP Temporales:* *{rach_vr_prognoz}*

👥 *Amigos invitados:* {referred_count}
🔗 *Tu enlace de referido:*

`{referral_link}`

➖➖➖➖➖➖➖➖➖

‼️ *Se está ejecutando una prueba beta*
Todas las funciones están disponibles de forma gratuita.

➖➖➖➖➖➖➖➖➖
                ''',

        'sozdat_prognoz': "📊 Crear pronóstico",
        'katalog': "🛍 Catálogo",
        'otzivi': "🗣️ Reseñas",
        'promokod': "#️⃣ Código promocional",
        'support': "⚙️ Soporte",
        'instruction': "📘 Instrucciones",
        'error_profile': "Error al obtener datos del perfil.",

        'NOT_od_prognoz': "❌ ¡No tienes pronósticos regulares!",
        'NOT_VIP_prognoz': "❌ ¡No tienes pronósticos VIP!",
        'vvedite_daty_vremia': "🗓 Ingresa fecha y hora del partido (ejemplo: 01.01.2025 18:00):",
        'vvedite_vid_sporta': "⚽️ Ingresa tipo de deporte (ejemplo: fútbol):",
        'vvedite_commandi': "👥 Ingresa nombres de equipos separados por coma (Equipo #1, Equipo #2):",

        'error_vvedite_commandi': '''
Por favor, ingresa exactamente dos nombres de equipo, separados por una coma
(ejemplo: Equipo1, Equipo2).
                ''',

        'message_promokod': '''
✅ ¡Código promocional aceptado!
Se te han añadido 🔹 {add_ob_prognoz} pronóstico(s) regular(es) y 💠 {add_rach_prognoz} pronóstico(s) VIP.
🎫 Suscripción: {subscription}
                ''',

        'vvevite_promocod_1': "⏳ Ingresa código promocional",
        'vvevite_promocod_2': "Ingresa código promocional:",
        'primenit_promocod': "✅ Aplicar código promocional",
        'najmi_primenit_promocod': "Haz clic en el botón de abajo para aplicar el código promocional 👇",
        'yes_promocod_ot_traffera': "✅ ¡Código promocional de traffickers aceptado! Se te ha añadido 1 pronóstico regular.",
        'ispolzovan_promocod': "❌ Ya has usado este código promocional.",
        'nedeistvitelen_promocod': "❌ Este código promocional ya no es válido.",
        'promocod_ne_nayden': "❌ Código promocional no encontrado.",

        'promocod_ot_traffera_YES': '''
✅ ¡Código promocional activado!
+ 1 pronóstico regular.
                ''',

        'error_close_panel': "No se pudo cerrar el panel 😔",

        'yes_dannie': "✅ Confirmar datos",
        'no_dannie': "🔄 Volver a ingresar datos",
        'obrabotka_prognoza': "⏳ Procesando tu pronóstico…",
        'no_registr_traffera': "⛔ No estás registrado como trafficker.",
        'balans_menche_1000': "Retiro disponible a partir de 1000 ₽",
        'ot_1000_do_balans': "Ingrese el monto a retirar (de 1000 a {balance}₽):",
        'vvedite_celoe_chislo': "¡Ingrese un número entero!",
        'summa_bolche_1000': "¡El monto debe ser de al menos 1000 ₽!",
        'summa_bolche_balansa': "¡El monto excede tu saldo actual!",
        'redactirovat': "✏️ Editar",
        'podtverdit': "✅ Confirmar",
        'proverka_summi': "¿Deseas retirar {amt}₽?",
        'yes_viplata': "✅ Retiro de {amt}₽ exitoso.",
        'no_viplata': "❌ Retiro de {amt}₽ no aceptado. Contacta a soporte: https://t.me/suportneyroteam",

        'katalog_podpisok': '''
➖➖➖➖➖➖➖➖➖

🎫 *{price_standart}₽ - Estándar* por una semana
Tendrás acceso a 5 pronósticos, 0 pronósticos VIP

🎫 *{price_medium}₽ - Medio* por una semana
Tendrás acceso a 12 pronósticos, 6 pronósticos VIP

🎫 *{price_premium}₽ - Premium* por dos semanas
Tendrás acceso a 30 pronósticos, 15 pronósticos VIP

➖➖➖➖➖➖➖➖➖

‼️ *Se está ejecutando una prueba beta*
Todas las funciones están disponibles de forma gratuita.

➖➖➖➖➖➖➖➖➖

💳 Elige una suscripción para pagar a continuación:
            ''',

    'katalog_prognozov': '''
➖➖➖➖➖➖➖➖➖➖➖➖➖➖

🔹 *{price_1_ob}₽* - 1 Pronóstico
🔹 *{price_5_ob}₽* - 5 Pronósticos
🔹 *{price_15_ob}₽* - 15 Pronósticos

💠 *{price_1_vip}₽* - 1 Pronóstico VIP
💠 *{price_5_vip}₽* - 5 Pronósticos VIP
💠 *{price_15_vip}₽* - 15 Pronósticos VIP

➖➖➖➖➖➖➖➖➖➖➖➖➖➖

‼️ *Se está ejecutando una prueba beta*
Todas las funciones están disponibles de forma gratuita.

➖➖➖➖➖➖➖➖➖➖➖➖➖➖

💳 Elige un paquete para pagar a continuación:
                ''',

        'standart': "💥 ¡Tu suscripción ha sido mejorada a Estándar por una semana!",
        'medium': "💥 ¡Tu suscripción ha sido mejorada a Medio por una semana!",
        'premium': "💥 ¡Tu suscripción ha sido mejorada a Premium por 2 semanas!",
        'podpiski': "🎫 Suscripciones",
        'prognozi': "📊 Pronósticos",
        'catalog_text': "¡Bienvenido al catálogo! Elige una sección:",
        '1_ob_prognoz': "🔹 {price_1_ob}₽ - 1",
        '1_rach_prognoz': "💠 {price_1_vip}₽ - 1 VIP",
        '5_ob_prognoz': "🔹 {price_5_ob}₽ - 5",
        '5_rach_prognoz': "💠 {price_5_vip}₽ - 5 VIP",
        '15_ob_prognoz': "🔹 {price_15_ob}₽ - 15",
        '15_rach_prognoz': "💠 {price_15_vip}₽ - 15 VIP",

        'ob_prognoz': "🔹 Pronóstico",
        'vip_prognoz': "💠 Pronóstico VIP",
        'profile': "👤 Perfil",
        'vibirite_tip_prognoza': "📊 Selecciona el tipo de pronóstico:",

        'read_otzivi': "👥 Leer reseñas",
        'ostvit_otziv': "🆕 Dejar una reseña",
        'vip_prognozov': "pronósticos VIP",
        'ob_progozov': "pronósticos regulares",
        'dobavleno_prognozov': "✅ ¡{count} {label} añadido(s)!",
        'iazik': "🌐 Cambiar idioma",
        'iazik_yes': "✅ ¡Idioma seleccionado!",
        'vibr_iazik': "🌐 Selecciona idioma:",
        'partners_header': "<b>Socios:</b>",
        'subscribe_to': "Suscribirse a",

        # === NUEVO BLOQUE: Instrucciones ===
        'instruction_menu_header': "📘 <b>Instrucciones</b>\n\nElige la sección que te interese:",
        'full_instruction_button': "📘 Leer instrucciones completas",
        'instruction_link': "https://telegra.ph/INSTRUCCIONES-PARA-USAR-SPORT-ANALITIK-BOT-es-07-01",
        'instruction_blocks': {

            'kakrabotaetbot': {
                'title': "⚙️ ¿Cómo funciona el bot?",
                'text': '''
- El bot @SportNeyroAnalitikbot, basado en redes neuronales especialmente entrenadas para el análisis de datos, proporciona un análisis detallado de eventos deportivos. ¡El bot se actualiza y se prueba, todos tus comentarios son probados!

<b>1. Recopilación de datos:</b>
El bot recopila datos de multitud de fuentes, teniendo en cuenta los parámetros que influyen en el resultado del partido.

<b>2. Predicción de resultados:</b>
Basándose en el análisis, el bot crea un pronóstico del resultado probable del partido, teniendo en cuenta la información recopilada.

<b>3. Análisis detallado:</b>
El usuario no solo recibe cifras, sino una explicación de los factores clave.

<b>4. Actualizaciones en tiempo real:</b>
Los algoritmos se mejoran constantemente, asegurando una alta precisión en los pronósticos.

❤️ <i>Nos esforzamos por hacer que el análisis deportivo sea accesible para todos. Ya seas un aficionado, un analista profesional o un participante del mercado de apuestas.</i>
                '''
            },
            'podpiski': {
                'title': "🎫 Suscripciones",
                'text': '''
‼️ <b>IMPORTANTE:</b>
1. Al comprar una nueva suscripción, la suscripción activa (si la hay) se cancela.
2. Al finalizar el período de validez de la suscripción, todos los pronósticos temporales no utilizados se anulan.

🎫 <b>Estándar</b> — <i>199₽ / semana</i> | 5 pronósticos regulares, 0 pronósticos VIP.

Ideal para principiantes y aquellos que prefieren elegir eventos de forma independiente.

🎫 <b>Medio</b> — <i>999₽ / semana</i> | 12 pronósticos regulares, 6 pronósticos VIP.

Adecuado para usuarios experimentados que desean profundizar en el análisis.

🎫 <b>Premium</b> — <i>1899₽ / 2 semanas</i> | 30 pronósticos regulares, 15 pronósticos VIP.

Máximo beneficio para jugadores activos.

<b>¿Por qué las suscripciones son rentables?</b> Las suscripciones te permiten ahorrar dinero. Comprar pronósticos individuales puede ser más caro que adquirir una suscripción por un período determinado.

<b>Si planeas realizar apuestas regularmente</b>, una suscripción será significativamente más rentable que las compras únicas.
                '''
            },
            'prognozi': {
                'title': "🔹 Pronósticos / 💠 Pronósticos VIP",
                'text': '''
🔷 <b>Pronósticos regulares (análisis breve):</b>

Un pronóstico regular contiene información breve y clara sobre un próximo partido o evento. Incluye datos básicos, como el resultado previsto del partido, las cuotas y los factores clave que influyen en el resultado. Este tipo de pronóstico es adecuado para quienes desean obtener rápidamente información básica antes de realizar una apuesta.

🪙 <b>Precios:</b>

59 ₽ — 1 pronóstico
249 ₽ — 5 pronósticos <i>(ahorro del 15.6%)</i>
450 ₽ — 15 pronósticos <i>(ahorro del 49.2%)</i>

💠 <b>Pronósticos VIP (análisis detallado):</b>

Los pronósticos VIP proporcionan un análisis más profundo y detallado de un evento deportivo. Además de la información básica, incluyen datos adicionales y una respuesta más extensa para una mejor comprensión del próximo partido, y otros aspectos importantes que pueden influir en el resultado del partido. Estos pronósticos te ayudarán a comprender mejor la situación y a tomar una decisión más informada.

🪙 <b>Precios:</b>

99 ₽ — 1 pronóstico VIP
399 ₽ — 5 pronósticos VIP <i>(ahorro del 19.4%)</i>
1159 ₽ — 15 pronósticos VIP <i>(ahorro del 22.0%)</i>
    '''
            },
            'buy': {
                'title': "💳 Compras",
                'text': '''
💳 Adquisición de un pronóstico

Para adquirir un pronóstico regular o VIP, utiliza la sección "Catálogo" en el menú principal del bot.

<b>Paso 1:</b> En el menú principal del bot, selecciona el botón "Catálogo".
<b>Paso 2:</b> Dentro del "Catálogo", selecciona la sección "Pronósticos".
<b>Paso 3:</b> Selecciona la cantidad deseada de pronósticos regulares o VIP.
<b>Paso 4:</b> Sigue las instrucciones del bot para completar el pago.

—————————-

💳 Adquisición de una suscripción

Para comprar una suscripción que te dé acceso a más pronósticos y pronósticos VIP a precios favorables, sigue estos pasos:

<b>Paso 1:</b> En el menú principal del bot, selecciona el botón "Catálogo".
<b>Paso 2:</b> Dentro del "Catálogo", selecciona la sección "Suscripciones".
<b>Paso 3:</b> Selecciona el tipo de suscripción que te convenga
(Estándar, Medio o Premium).
<b>Paso 4:</b> Sigue las instrucciones del bot para completar el pago.
                '''
            },
            'createprognoz': {
                'title': "👨‍💻 Creación de un pronóstico",
                'text': '''
🤖 <b>El bot</b> @SportNeyroAnalitikbot te permite crear pronósticos bajo demanda. Para crear un pronóstico, necesitas:

<b>Paso 1:</b> En el menú principal del bot, selecciona el botón "Crear pronóstico".
<b>Paso 2:</b> Después de procesar la solicitud y analizar el partido, el bot te proporcionará un pronóstico.

‼️ <b>IMPORTANTE</b>
Rellena la información del partido de forma correcta y cuidadosa, ya que si cometes un error, no habrá reembolso.
                '''
            },
            'promokodi': {
                'title': "🎟 Códigos promocionales",
                'text': '''
<b>Los códigos promocionales en el bot @SportNeyroAnalitikbot te proporcionan bonificaciones adicionales.</b>

<b>Paso 1:</b> En el menú principal del bot, selecciona el botón "Código promocional".
<b>Paso 2:</b> Introduce tu código promocional en el campo correspondiente.
<b>Paso 3:</b> Haz clic en "Aplicar" para activar el código promocional y recibir bonificaciones.

🔭 Sigue las noticias del canal <a href="https://t.me/NeyroTeamTg">Neyro Team</a> para no perderte los nuevos códigos promocionales.
                '''
            },
            'bukmekeri': {
                'title': "✅ Mejores casas de apuestas",
                'text': '''
👍 <b>Para realizar apuestas deportivas, basándose en los pronósticos recibidos del bot, recomendamos utilizar los siguientes socios de casas de apuestas verificadas:</b>

<b>1Win:</b> <i>https://1wzyuh.com/v3/landing-page/football?p=5ibz</i>
Al registrarte con el código promocional "NEYRO99" recibirás bonos.
<b>Winline:</b> <i>https://partners2.winline.ru/s/Ebp0XjlFwM?statid=2925_</i>
Al registrarte con el código promocional "NEYRO3000" recibirás bonos.
                '''
            },
            'ozivi': {
                'title': "🗣 Reseñas",
                'text': '''
♥️ <b>¡Tu opinión es muy importante para nosotros!</b> Puedes dejar reseñas sobre el trabajo del bot y leer las opiniones de otros usuarios.

✍️ <b>Dejar una reseña:</b> Para compartir tu opinión, ve al bot @OtziviSportbot o selecciona el botón "Dejar una reseña" en la sección "Reseñas" en el menú de @SportNeyroAnalitikbot. Sigue las instrucciones del bot para escribir una reseña.

🗣 <b>Leer reseñas:</b> Para leer reseñas de otros usuarios, selecciona el botón "Leer reseñas" en la sección "Reseñas" en el menú de @SportNeyroAnalitikbot o ve al canal de Telegram @OTZIVISPORTANALITIK
                '''
            },
            'iaziki': {
                'title': "🌍 Idiomas",
                'text': '''
<b>El bot @SportNeyroAnalitikbot está diseñado para una audiencia global y soporta 6 idiomas internacionales de la ONU:</b>

🇷🇺🇬🇧🇪🇸🇨🇳🇫🇷🇸🇦

Ruso, inglés, español, chino, francés, árabe

Puedes cambiar fácilmente el idioma de la interfaz del bot seleccionando la opción apropiada en el menú principal del bot. Esto te permite usar todas las funciones del bot de la manera más cómoda posible, independientemente de tu región.
                '''
            },
            'refi': {
                'title': "🤝 Programa de referidos",
                'text': '''
🫂 Cada usuario de @SportNeyroAnalitikbot tiene la oportunidad de participar en nuestro programa de referidos y recibir bonificaciones por amigos invitados.

• <b>Tu enlace de referido:</b> Cada cuenta en el bot tiene un enlace de referido único. Puedes encontrarlo en tu "Perfil".
• <b>Cómo funciona:</b> Comparte tu enlace de referido único con amigos. Cuando tu amigo haga clic en tu enlace, se registre en el bot y realice su primera compra (cualquier suscripción o pronóstico), ambos recibirán una bonificación.
• <b>Bonificación:</b> Por cada referido que realice una compra, tanto tú como tu amigo invitado recibirán 1 pronóstico VIP.
• <b>Seguimiento:</b> El número de amigos invitados se muestra en tu "Perfil".

<b>¡Cuantos más amigos invites, más bonificaciones podrás obtener!</b>
                '''
            },
            'partnerstvo': {
                'title': "💼 Asociación",
                'text': '''
💸 Si eres un anunciante, trafficker o estás interesado en publicidad mutua, puedes contactar con nuestro equipo de soporte en Telegram en @SuportNeyroTeam para discutir los términos de cooperación.
                '''
            }

        },

        # === NUEVO BLOQUE: Soporte y Preguntas Frecuentes ===
        'support_menu_header': "⚙️ <b>Soporte</b>\n\nSi tienes alguna pregunta, puedes encontrar respuestas en la sección de Preguntas Frecuentes o escribir a nuestro servicio de soporte.",
        'faq_button': "⁉️ Preguntas Frecuentes (FAQ)",
        'contact_support_button': "👨‍💻 Escribir a soporte",
        'faq_menu_header': "❓ <b>Preguntas Frecuentes</b> ❓",
        'faq_items': {
            'q1': {
                'question': "⚙️ ¿Cómo funciona el bot? ",
                'answer': '''
- El bot @SportNeyroAnalitikbot, basado en redes neuronales especialmente entrenadas para el análisis de datos, proporciona un análisis detallado de eventos deportivos. ¡El bot se actualiza y se prueba, todos tus comentarios son probados!

<b>1. Recopilación de datos:</b>
El bot recopila datos de multitud de fuentes, teniendo en cuenta los parámetros que influyen en el resultado del partido.

<b>2. Predicción de resultados:</b>
Basándose en el análisis, el bot crea un pronóstico del resultado probable del partido, teniendo en cuenta la información recopilada.

<b>3. Análisis detallado:</b>
El usuario no solo recibe cifras, sino una explicación de los factores clave.

<b>4. Actualizaciones en tiempo real:</b>
Los algoritmos se mejoran constantemente, asegurando una alta precisión en los pronósticos.

❤️ <i>Nos esforzamos por hacer que el análisis deportivo sea accesible para todos. Ya seas un aficionado, un analista profesional o un participante del mercado de apuestas.</i>
                '''
            },
            'q2': {
                'question': "🎫 ¿Cómo funcionan las suscripciones?",
                'answer': '''
🎫 Las suscripciones dan acceso a un número determinado de pronósticos temporales regulares y VIP por un período fijo <i>(una semana, dos semanas)</i>.

💎 Ofrecen <b>precios más favorables</b> en comparación con la compra de pronósticos individuales.

‼️ <b>Es importante recordar</b> que al comprar una nueva suscripción, la anterior se cancela, y los pronósticos temporales no utilizados se anulan al finalizar el período de la suscripción.
                '''
            },
            'q3': {
                'question': "📊 ¿Cómo funcionan los pronósticos?",
                'answer': '''
<b>El bot ofrece dos tipos de pronósticos:</b>

🔹 <b>Pronósticos regulares:</b> Proporcionan información breve sobre el resultado del partido, las cuotas y los factores clave.

💠 <b>Pronósticos VIP:</b> Ofrecen un análisis más profundo y detallado, incluyendo datos adicionales y explicaciones ampliadas para tomar decisiones más informadas.
    '''
            },
            'q4': {
                'question': "⏳ ¿Cuál es la diferencia con los pronósticos temporales? ",
                'answer': '''
⏳ Al adquirir una suscripción, recibes precisamente <b>pronósticos temporales</b> que estarán disponibles hasta que expire la suscripción. Por ejemplo, si planeas realizar apuestas regularmente, comprar una suscripción será mucho más rentable que las compras únicas.
                '''
            },
            'q5': {
                'question': "💳 ¿Cómo comprar una suscripción?",
                'answer': '''
💳 Para comprar una suscripción, ve a "Catálogo" en el menú principal del bot, luego selecciona "Suscripciones" y el plan deseado. Sigue las instrucciones del bot para el pago.
                '''
            },
            'q6': {
                'question': "💳 ¿Cómo comprar pronósticos?",
                'answer': '''
💳 Para comprar pronósticos, ve a "Catálogo" en el menú principal del bot, luego selecciona "Pronósticos" y la cantidad necesaria de pronósticos regulares o VIP. Sigue las instrucciones del bot para el pago.
    '''
            },
            'q7': {
                'question': "📊 ¿Cómo crear un pronóstico?",
                'answer': '''
📊 Para crear un pronóstico bajo demanda, selecciona el botón "Crear pronóstico" en el menú principal del bot. Luego, ingresa la información necesaria sobre el evento deportivo, siguiendo las indicaciones del bot.
    '''
            },
            'q8': {
                'question': "🎟 ¿Cómo funcionan los códigos promocionales? ",
                'answer': '''
🎟 Los códigos promocionales se introducen en una sección especial "Código promocional" en el menú principal del bot. Activan bonificaciones que pueden ser proporcionadas por el equipo de Neyro Team. También hay códigos promocionales para recibir bonificaciones al registrarse con socios de casas de apuestas.
    '''
            },
            'q9': {
                'question': "✍️ ¿Cómo dejar una reseña?",
                'answer': '''
✍️ Puedes dejar una reseña yendo al bot @OtziviSportbot o seleccionando el botón "Dejar una reseña" en la sección "Reseñas" en el menú de @SportNeyroAnalitikbot.
                '''
            },
            'q10': {
                'question': "👀 ¿Dónde leer las reseñas?",
                'answer': '''
👀 Puedes leer reseñas de otros usuarios seleccionando el botón "Leer reseñas" en la sección "Reseñas" en el menú de @SportNeyroAnalitikbot.
    '''
            },
            'q11': {
                'question': "✅ ¿Dónde apostar en deportes?",
                'answer': '''
✔️ Para realizar apuestas deportivas, basándose en los pronósticos recibidos del bot, recomendamos utilizar los siguientes socios de casas de apuestas verificadas:

<b>1Win:</b> <i>https://1wzyuh.com/v3/landing-page/football?p=5ibz</i>
(Código promocional: NEYRO99)
<b>Winline:</b> <i>https://partners2.winline.ru/s/Ebp0XjlFwM?statid=2925_</i>
(Código promocional: NEYRO3000)
                '''
            },
            'q12': {
                'question': "🌍 ¿En qué idiomas está disponible el bot?",
                'answer': '''
El bot @SportNeyroAnalitikbot soporta 6 idiomas internacionales 🌍 de la ONU: ruso, inglés, árabe, español, chino y francés. Puedes seleccionar el idioma deseado en la configuración del bot.
                '''
            },
            'q13': {
                'question': "🤝 ¿Cómo funciona el programa de referidos?",
                'answer': '''
🫂 Cada usuario de @SportNeyroAnalitikbot tiene la oportunidad de participar en nuestro programa de referidos y recibir bonificaciones por amigos invitados.

• <b>Tu enlace de referido:</b> Cada cuenta en el bot tiene un enlace de referido único. Puedes encontrarlo en tu "Perfil".
• <b>Cómo funciona:</b> Comparte tu enlace de referido único con amigos. Cuando tu amigo haga clic en tu enlace, se registre en el bot y realice su primera compra (cualquier suscripción o pronóstico), ambos recibirán una bonificación.
• <b>Bonificación:</b> Por cada referido que realice una compra, tanto tú como tu amigo invitado recibirán 1 pronóstico VIP.
• <b>Seguimiento:</b> El número de amigos invitados se muestra en tu "Perfil".

<b>¡Cuantos más amigos invites, más bonificaciones podrás obtener!</b>
                '''
            },
            'q14': {
                'question': '''💼 ¿Cómo ser socio de "Neyro Team"?''',
                'answer': '''
💸 Si eres un <b>anunciante, trafficker o estás interesado en publicidad mutua</b>, puedes contactar con nuestro equipo de soporte en Telegram en @SuportNeyroTeam para discutir los términos de cooperación.
    '''
            }
        },

        # === NUEVO BLOQUE: Rutas de imágenes ===
        'photo_profil': "images/es/profil.png",
        'photo_katalog': "images/es/katalog.png",
        'photo_katalog_prognoz': "images/es/katalog_prognoz.png",
        'photo_katalog_subscriptions': "images/es/katalog_subscriptions.png",
        'photo_otzivi': "images/es/otzivi.png",
        'photo_tip_prognoza': "images/es/tip_prognoza.png",
        'ob_prognoz_photo': "images/es/ob_prognoz.png",
        'vip_prognoz_photo': "images/es/vip_prognoz.png",
        'photo_instruction': "images/es/instruction.png",
        'photo_support': "images/es/support.png",
        'photo_faq': "images/es/faq.png",
        'photo_cponsori': "images/es/cponsori.png"
    },
    'ar': {
        # ==============================
        # 1. الأوامر والرسائل العامة
        # ==============================
        'start': "✅ بدء البوت",
        'admin': "👨‍💻 لوحة الإدارة",
        'cancel': "🔙 إلغاء",
        'traffer': "🥷 لوحة المسوق",
        'cancel_disvie': "🚫 تم إلغاء الإجراء.",

        'traff_info': '''
    👤 المسوق: {trafer_name}
    👤 اسم المستخدم: {t_username}
    🆔 المعرف: {t_id}
    🏷️ الرمز الترويجي: {t_promo}

    📱 الهاتف: {t_telefon}
    💳 البطاقة: {t_karta}
    🪙 العملة المشفرة: {t_kripta}
    🔗 الشبكة: {crypto_network}

    📊 طريقة الربح: {human_model}
    📊 العملاء المحتملون: {leads}

    🏦 الرصيد: {balance}₽
    💸 تم سحب: {paid}₽
    💰 إجمالي الأرباح: {total}₽
                ''',

        'edit_traffera': "✏️ تعديل المسوق",
        'obnovit_traf_info': "🔄 تحديث",
        'traff_id_kanala': "🆔 معرف القناة: {pay_link}",
        'traff_priglos_ssilka': "🔗 رابط الدعوة:\n{invite_link}",
        'del_traffera': "❌ حذف المسوق",
        'back': "↩️ رجوع",
        'obnovit_podpiski': "🔄 تحديث الاشتراكات",
        'vivisti_money': "💸 سحب الأموال",
        'back_traff_panel': "🔙 الخروج من لوحة المسوق",
        'command_start': "بدء البوت",
        'command_admin': "لوحة الإدارة",
        'command_traffer': "لوحة المسوق",
        'podpiska_istekla': "انتهى الاشتراك",
        'bolche_day': "{days} يوم {hours} ساعة.",
        'menche_day': "{hours} ساعة {minutes} دقيقة.",
        'menche_hour': "{minutes} دقيقة.",
        'spasibo_za_oplaty': "شكراً للدفع! تم تفعيل الوصول.",
        'chek_partners': "🔁 التحقق من الاشتراك",
        'pustoy_spisok_partners': "قائمة الشركاء فارغة",
        'NO_chek_partners': "الرجاء الاشتراك في جميع الشركاء للمتابعة.",

        'edit_name': "الاسم",
        'edit_id': "المعرف",
        'edit_username': "@اسم_المستخدم",
        'edit_telefon': "الهاتف",
        'edit_karta': "البطاقة",
        'edit_kripta': "محفظة العملات المشفرة",
        'edit_crypto_network': "شبكة العملات المشفرة",
        'cancel_edit': "↩️ إلغاء",

        # جديد: مطالبات التعديل
        'enter_new_name': "أدخل الاسم الجديد:",
        'enter_new_id': "أدخل المعرف الجديد:",
        'enter_new_username': "أدخل @اسم_المستخدم الجديد:",
        'enter_new_telefon': "أدخل رقم الهاتف الجديد:",
        'enter_new_karta': "أدخل رقم البطاقة الجديد:",
        'enter_new_kripta': "أدخل محفظة العملات المشفرة الجديدة:",
        'enter_new_crypto_network': "أدخل شبكة العملات المشفرة الجديدة:",
        'traffer_updated_success': "✅ تم تحديث بيانات المسوق بنجاح!",
        'no_traffer_found': "لم يتم العثور على المسوق.",

        "referral_reward": "لقد تلقيت تنبؤ VIP دائم واحد كمكافأة إحالة!",
        "profile_text": '''
➖➖➖➖➖➖➖➖➖

👤 *{user_name}* | *المعرف:* `{user_id}`
🎫 *الاشتراك:* *{subscription}*
⌛️ *المتبقي حتى انتهاء الصلاحية:* *{remaining}*

🔹 *التنبؤات:* *{ob_prognoz}*
💠 *تنبؤات VIP:* *{rach_prognoz}*
🔹 *التنبؤات المؤقتة:* *{ob_vr_prognoz}*
💠 *تنبؤات VIP المؤقتة:* *{rach_vr_prognoz}*

👥 *الأصدقاء المدعوون:* {referred_count}
🔗 *رابط الإحالة الخاص بك:*

`{referral_link}`

➖➖➖➖➖➖➖➖➖

‼️ *يجري اختبار بيتا*
جميع الوظائف متاحة مجاناً.

➖➖➖➖➖➖➖➖➖
            ''',

        'sozdat_prognoz': "📊 إنشاء تنبؤ",
        'katalog': "🛍 الكتالوج",
        'otzivi': "🗣️ التقييمات",
        'promokod': "#️⃣ الرمز الترويجي",
        'support': "⚙️ الدعم",
        'instruction': "📘 التعليمات",
        'error_profile': "خطأ في الحصول على بيانات الملف الشخصي.",

        'NOT_od_prognoz': "❌ ليس لديك تنبؤات عادية!",
        'NOT_VIP_prognoz': "❌ ليس لديك تنبؤات VIP!",
        'vvedite_daty_vremia': "🗓 أدخل تاريخ ووقت المباراة (مثال: 01.01.2025 18:00):",
        'vvedite_vid_sporta': "⚽️ أدخل نوع الرياضة (مثال: كرة القدم):",
        'vvedite_commandi': "👥 أدخل أسماء الفرق مفصولة بفاصلة (الفريق رقم 1، الفريق رقم 2):",

        'error_vvedite_commandi': '''
الرجاء إدخال اسمين للفريق بالضبط، مفصولين بفاصلة
(مثال: الفريق1، الفريق2).
            ''',

        'message_promokod': '''
✅ تم قبول الرمز الترويجي!
تمت إضافة 🔹 {add_ob_prognoz} تنبؤ(ات) عادي و 💠 {add_rach_prognoz} تنبؤ(ات) VIP لك.
🎫 الاشتراك: {subscription}
                ''',

        'vvevite_promocod_1': "⏳ أدخل الرمز الترويجي",
        'vvevite_promocod_2': "أدخل الرمز الترويجي:",
        'primenit_promocod': "✅ تطبيق الرمز الترويجي",
        'najmi_primenit_promocod': "انقر الزر أدناه لتطبيق الرمز الترويجي 👇",
        'yes_promocod_ot_traffera': "✅ تم قبول الرمز الترويجي من المسوقين! تمت إضافة تنبؤ عادي واحد لك.",
        'ispolzovan_promocod': "❌ لقد استخدمت هذا الرمز الترويجي بالفعل.",
        'nedeistvitelen_promocod': "❌ هذا الرمز الترويجي لم يعد صالحاً.",
        'promocod_ne_nayden': "❌ لم يتم العثور على الرمز الترويجي.",

        'promocod_ot_traffera_YES': '''
✅ تم تفعيل الرمز الترويجي!
+ 1 تنبؤ عادي.
                ''',

        'error_close_panel': "فشل إغلاق اللوحة 😔",

        'yes_dannie': "✅ تأكيد البيانات",
        'no_dannie': "🔄 إعادة إدخال البيانات",
        'obrabotka_prognoza': "⏳ جاري معالجة تنبؤك…",
        'no_registr_traffera': "⛔ أنت غير مسجل كمسوق.",
        'balans_menche_1000': "السحب متاح ابتداءً من 1000 ₽",
        'ot_1000_do_balans': "أدخل مبلغ السحب (من 1000 إلى {balance}₽):",
        'vvedite_celoe_chislo': "أدخل عدداً صحيحاً!",
        'summa_bolche_1000': "يجب أن يكون المبلغ 1000 ₽ على الأقل!",
        'summa_bolche_balansa': "المبلغ يتجاوز رصيدك الحالي!",
        'redactirovat': "✏️ تعديل",
        'podtverdit': "✅ تأكيد",
        'proverka_summi': "هل تريد سحب {amt}₽؟",
        'yes_viplata': "✅ تم سحب {amt}₽ بنجاح.",
        'no_viplata': "❌ لم يتم قبول سحب {amt}₽. يرجى الاتصال بالدعم: https://t.me/suportneyroteam",

        'katalog_podpisok': '''
➖➖➖➖➖➖➖➖➖

🎫 *{price_standart}₽ - قياسي* لمدة أسبوع
سيكون لديك وصول إلى 5 تنبؤات، 0 تنبؤات VIP

🎫 *{price_medium}₽ - متوسط* لمدة أسبوع
سيكون لديك وصول إلى 12 تنبؤاً، 6 تنبؤات VIP

🎫 *{price_premium}₽ - مميز* لمدة أسبوعين
سيكون لديك وصول إلى 30 تنبؤاً، 15 تنبؤاً VIP

➖➖➖➖➖➖➖➖➖

‼️ *يجري اختبار بيتا*
جميع الوظائف متاحة مجاناً.

➖➖➖➖➖➖➖➖➖

💳 اختر اشتراكاً للدفع أدناه:
                ''',

        'katalog_prognozov': '''
➖➖➖➖➖➖➖➖➖➖➖➖➖➖

🔹 *{price_1_ob}₽* - تنبؤ واحد
🔹 *{price_5_ob}₽* - 5 تنبؤات
🔹 *{price_15_ob}₽* - 15 تنبؤاً

💠 *{price_1_vip}₽* - تنبؤ VIP واحد
💠 *{price_5_vip}₽* - 5 تنبؤات VIP
💠 *{price_15_vip}₽* - 15 تنبؤاً VIP

➖➖➖➖➖➖➖➖➖➖➖➖➖➖

‼️ *يجري اختبار بيتا*
جميع الوظائف متاحة مجاناً.

➖➖➖➖➖➖➖➖➖➖➖➖➖➖

💳 اختر باقة للدفع أدناه:
                ''',

        'standart': "💥 تمت ترقية اشتراكك إلى قياسي لمدة أسبوع!",
        'medium': "💥 تمت ترقية اشتراكك إلى متوسط لمدة أسبوع!",
        'premium': "💥 تمت ترقية اشتراكك إلى مميز لمدة أسبوعين!",
        'podpiski': "🎫 الاشتراكات",
        'prognozi': "📊 التنبؤات",
        'catalog_text': "مرحباً بك في الكتالوج! اختر قسماً:",
        '1_ob_prognoz': "🔹 {price_1_ob}₽ - 1",
        '1_rach_prognoz': "💠 {price_1_vip}₽ - 1 VIP",
        '5_ob_prognoz': "🔹 {price_5_ob}₽ - 5",
        '5_rach_prognoz': "💠 {price_5_vip}₽ - 5 VIP",
        '15_ob_prognoz': "🔹 {price_15_ob}₽ - 15",
        '15_rach_prognoz': "💠 {price_15_vip}₽ - 15 VIP",

        'ob_prognoz': "🔹 تنبؤ",
        'vip_prognoz': "💠 تنبؤ VIP",
        'profile': "👤 الملف الشخصي",
        'vibirite_tip_prognoza': "📊 اختر نوع التنبؤ:",

        'read_otzivi': "👥 قراءة التقييمات",
        'ostvit_otziv': "🆕 ترك تقييم",
        'vip_prognozov': "تنبؤات VIP",
        'ob_progozov': "تنبؤات عادية",
        'dobavleno_prognozov': "✅ تمت إضافة {count} {label}!",
        'iazik': "🌐 تغيير اللغة",
        'iazik_yes': "✅ تم اختيار اللغة!",
        'vibr_iazik': "🌐 اختر اللغة:",
        'partners_header': "<b>الشركاء:</b>",
        'subscribe_to': "الاشتراك في",

        # === كتلة جديدة: التعليمات ===
        'instruction_menu_header': "📘 <b>التعليمات</b>\n\nاختر القسم الذي يهمك:",
        'full_instruction_button': "📘 قراءة التعليمات الكاملة",
        'instruction_link': "https://telegra.ph/%D8%AA%D9%85%D8%A7%D9%85-%D8%A5%D9%84%D9%8A%D9%83-%D8%A7%D9%84%D8%AA%D8%B9%D9%84%D9%8A%D9%85%D8%A7%D8%AA-%D8%A7%D9%84%D9%83%D8%A7%D9%85%D9%84%D8%A9-%D9%85%D8%AA%D8%B1%D8%AC%D9%85%D8%A9-%D8%A5%D9%84%D9%89-%D8%A7%D9%84%D9%84%D8%BA%D8%A9-%D8%A7%D9%84%D8%B9%D8%B1%D8%A8%D9%8A%D8%A9-%D9%85%D8%B9-%D8%A7%D9%84%D8%AD%D9%81%D8%A7%D8%B8-%D8%B9%D9%84%D9%89-%D8%A7%D9%84%D8%AA%D9%86%D8%B3%D9%8A%D9%82-%D9%88%D8%A5%D8%B6%D8%A7%D9%81%D8%A9-%D9%85%D8%B3%D8%A7%D9%81%D8%A9-%D8%A8%D8%B9%D8%AF-%D9%83%D9%84-%D8%B9%D9%86%D9%88%D8%A7%D9%86-%D8%A8%D8%AE%D8%B7-%D8%B9%D8%B1%D9%8A%D8%B6-07-01",
        'instruction_blocks': {

            'kakrabotaetbot': {
                'title': "⚙️ كيف يعمل البوت؟",
                'text': '''
- يعتمد بوت @SportNeyroAnalitikbot على شبكات عصبية مدربة خصيصاً لتحليل البيانات، ويوفر تحليلاً تفصيلياً للأحداث الرياضية، ويتم تحديث البوت واختباره، وجميع ملاحظاتك يتم اختبارها!

<b>1. جمع البيانات:</b>
يجمع البوت البيانات من مصادر متعددة، مع الأخذ في الاعتبار العوامل التي تؤثر على نتيجة المباراة.

<b>2. التنبؤ بالنتائج:</b>
بناءً على التحليل، يقوم البوت بإنشاء تنبؤ بالنتيجة المحتملة للمباراة، مع الأخذ في الاعتبار المعلومات التي تم جمعها.

<b>3. تحليل مفصل:</b>
يتلقى المستخدم ليس فقط أرقاماً، بل شرحاً للعوامل الرئيسية.

<b>4. التحديثات في الوقت الفعلي:</b>
يتم تحسين الخوارزميات باستمرار، مما يضمن دقة عالية للتنبؤات.

❤️ <i>نسعى لجعل التحليلات الرياضية في متناول الجميع. سواء كنت من محبي الرياضة، أو محللاً محترفاً، أو مشاركاً في سوق المراهنات.</i>
                '''
            },
            'podpiski': {
                'title': "🎫 الاشتراكات",
                'text': '''
‼️ <b>هام:</b>
1. عند شراء اشتراك جديد، يتم إلغاء الاشتراك النشط (إن وجد).
2. عند انتهاء صلاحية الاشتراك، يتم إلغاء جميع التنبؤات المؤقتة غير المستخدمة.

🎫 <b>قياسي</b> — <i>199₽ / أسبوع</i> | 5 تنبؤات عادية، 0 تنبؤات VIP.

مثالي للمبتدئين والذين يفضلون اختيار الأحداث بشكل مستقل.

🎫 <b>متوسط</b> — <i>999₽ / أسبوع</i> | 12 تنبؤاً عادياً، 6 تنبؤات VIP.

مناسب للمستخدمين ذوي الخبرة الذين يرغبون في التعمق في التحليلات.

🎫 <b>مميز</b> — <i>1899₽ / أسبوعين</i> | 30 تنبؤاً عادياً، 15 تنبؤاً VIP.

أقصى فائدة للاعبين النشطين.

<b>لماذا الاشتراكات مربحة؟</b> تتيح لك الاشتراكات توفير المال. قد يكون شراء التنبؤات الفردية أغلى من شراء اشتراك لفترة معينة.

<b>إذا كنت تخطط للمراهنة بانتظام</b>، فسيكون الاشتراك أكثر ربحية بكثير من المشتريات لمرة واحدة.
                '''
            },
            'prognozi': {
                'title': "🔹 التنبؤات / 💠 تنبؤات VIP",
                'text': '''
🔷 <b>التنبؤات العادية (تحليلات موجزة):</b>

يحتوي التنبؤ العادي على معلومات موجزة وواضحة حول المباراة أو الحدث القادم. يتضمن البيانات الأساسية، مثل النتيجة المتوقعة للمباراة، الاحتمالات، والعوامل الرئيسية التي تؤثر على النتيجة. هذا النوع من التنبؤ مناسب لأولئك الذين يرغبون في الحصول على معلومات أساسية بسرعة قبل المراهنة.

🪙 <b>الأسعار:</b>

59 ₽ — تنبؤ واحد
249 ₽ — 5 تنبؤات <i>(توفير 15.6%)</i>
450 ₽ — 15 تنبؤاً <i>(توفير 49.2%)</i>

💠 <b>تنبؤات VIP (تحليل مفصل):</b>

توفر تنبؤات VIP تحليلاً أعمق وأكثر تفصيلاً للحدث الرياضي. بالإضافة إلى المعلومات الأساسية، تتضمن بيانات إضافية وإجابة أكثر تفصيلاً لفهم أفضل للمباراة القادمة، والجوانب الهامة الأخرى التي قد تؤثر على نتيجة المباراة. ستساعدك هذه التنبؤات على فهم الوضع بشكل أفضل واتخاذ قرار أكثر استنارة.

🪙 <b>الأسعار:</b>

99 ₽ — تنبؤ VIP واحد
399 ₽ — 5 تنبؤات VIP <i>(توفير 19.4%)</i>
1159 ₽ — 15 تنبؤاً VIP <i>(توفير 22.0%)</i>
    '''
            },
            'buy': {
                'title': "💳 المشتريات",
                'text': '''
💳 شراء تنبؤ

لشراء تنبؤ عادي أو VIP، استخدم قسم "الكتالوج" في القائمة الرئيسية للبوت.

<b>الخطوة 1:</b> في القائمة الرئيسية للبوت، حدد زر "الكتالوج".
<b>الخطوة 2:</b> داخل "الكتالوج"، حدد قسم "التنبؤات".
<b>الخطوة 3:</b> حدد العدد المطلوب من التنبؤات العادية أو VIP.
<b>الخطوة 4:</b> اتبع تعليمات البوت لإتمام عملية الدفع.

—————————-

💳 شراء اشتراك

لشراء اشتراك يمنحك وصولاً إلى المزيد من التنبؤات وتنبؤات VIP بأسعار مناسبة، اتبع هذه الخطوات:

<b>الخطوة 1:</b> في القائمة الرئيسية للبوت، حدد زر "الكتالوج".
<b>الخطوة 2:</b> داخل "الكتالوج"، حدد قسم "الاشتراكات".
<b>الخطوة 3:</b> حدد نوع الاشتراك الذي يناسبك
(قياسي، متوسط، أو مميز).
<b>الخطوة 4:</b> اتبع تعليمات البوت لإتمام عملية الدفع.
                '''
            },
            'createprognoz': {
                'title': "👨‍💻 إنشاء تنبؤ",
                'text': '''
🤖 <b>البوت</b> @SportNeyroAnalitikbot يتيح لك إنشاء تنبؤات حسب الطلب. لإنشاء تنبؤ، تحتاج إلى:

<b>الخطوة 1:</b> في القائمة الرئيسية للبوت، حدد زر "إنشاء تنبؤ".
<b>الخطوة 2:</b> بعد معالجة الطلب وتحليل المباراة، سيوفر لك البوت تنبؤاً.

‼️ <b>هام</b>
املأ معلومات المباراة بشكل صحيح وبعناية، حيث إذا ارتكبت خطأ، فلن يكون هناك استرداد.
                '''
            },
            'promokodi': {
                'title': "🎟 الرموز الترويجية",
                'text': '''
<b>توفر لك الرموز الترويجية في بوت @SportNeyroAnalitikbot مكافآت إضافية.</b>

<b>الخطوة 1:</b> في القائمة الرئيسية للبوت، حدد زر "الرمز الترويجي".
<b>الخطوة 2:</b> أدخل الرمز الترويجي الخاص بك في الحقل المخصص.
<b>الخطوة 3:</b> انقر "تطبيق" لتفعيل الرمز الترويجي وتلقي المكافآت.

🔭 تابع أخبار قناة <a href="https://t.me/NeyroTeamTg">Neyro Team</a> حتى لا تفوتك الرموز الترويجية الجديدة.
                '''
            },
            'bukmekeri': {
                'title': "✅ أفضل شركات المراهنات",
                'text': '''
👍 <b>لوضع المراهنات الرياضية، بناءً على التنبؤات المستلمة من البوت، نوصي باستخدام شركاء شركات المراهنات المعتمدين التالية:</b>

<b>1Win:</b> <i>https://1wzyuh.com/v3/landing-page/football?p=5ibz</i>
عند التسجيل باستخدام الرمز الترويجي "NEYRO99" ستحصل على مكافآت.
<b>Winline:</b> <i>https://partners2.winline.ru/s/Ebp0XjlFwM?statid=2925_</i>
عند التسجيل باستخدام الرمز الترويجي "NEYRO3000" ستحصل على مكافآت.
                '''
            },
            'ozivi': {
                'title': "🗣 التقييمات",
                'text': '''
♥️ <b>رأيك مهم جداً بالنسبة لنا!</b> يمكنك ترك تقييمات حول عمل البوت وقراءة آراء المستخدمين الآخرين.

✍️ <b>اترك تقييماً:</b> لمشاركة رأيك، انتقل إلى بوت @OtziviSportbot أو حدد زر "اترك تقييماً" في قسم "التقييمات" في قائمة @SportNeyroAnalitikbot. اتبع تعليمات البوت لكتابة التقييم.

🗣 <b>قراءة التقييمات:</b> لقراءة تقييمات المستخدمين الآخرين، حدد زر "قراءة التقييمات" في قسم "التقييمات" في قائمة @SportNeyroAnalitikbot أو انتقل إلى قناة Telegram @OTZIVISPORTANALITIK
                '''
            },
            'iaziki': {
                'title': "🌍 اللغات",
                'text': '''
<b>تم تصميم بوت @SportNeyroAnalitikbot لجمهور عالمي ويدعم 6 لغات دولية من الأمم المتحدة:</b>

🇷🇺🇬🇧🇪🇸🇨🇳🇫🇷🇸🇦

الروسية، الإنجليزية، الإسبانية، الصينية، الفرنسية، العربية

يمكنك بسهولة تغيير لغة واجهة البوت عن طريق تحديد الخيار المناسب في القائمة الرئيسية للبوت. وهذا يسمح لك باستخدام جميع وظائف البوت بأقصى قدر من الراحة، بغض النظر عن منطقتك.
                '''
            },
            'refi': {
                'title': "🤝 برنامج الإحالة",
                'text': '''
🫂 يتمتع كل مستخدم لـ @SportNeyroAnalitikbot بفرصة المشاركة في برنامج الإحالة الخاص بنا وتلقي مكافآت مقابل الأصدقاء المدعوين.

• <b>رابط الإحالة الخاص بك:</b> لكل حساب في البوت رابط إحالة فريد. يمكنك العثور عليه في "ملفك الشخصي".
• <b>كيف يعمل:</b> شارك رابط الإحالة الفريد الخاص بك مع الأصدقاء. عندما ينقر صديقك على رابطك، ويسجل في البوت، ويقوم بأول عملية شراء (أي اشتراك أو تنبؤ)، ستتلقون كلاكما مكافأة.
• <b>المكافأة:</b> لكل إحالة يقوم بعملية شراء، يتلقى كل من أنت وصديقك المدعو تنبؤ VIP واحد.
• <b>التتبع:</b> يتم عرض عدد الأصدقاء المدعوين في "ملفك الشخصي".

<b>كلما دعوت المزيد من الأصدقاء، كلما حصلت على المزيد من المكافآت!</b>
                '''
            },
            'partnerstvo': {
                'title': "💼 الشراكة",
                'text': '''
💸 إذا كنت معلناً، أو مسوقاً، أو مهتماً بالإعلان المتبادل، يمكنك الاتصال بفريق الدعم لدينا على Telegram على @SuportNeyroTeam لمناقشة شروط التعاون.
                '''
            }

        },

        # === كتلة جديدة: الدعم والأسئلة الشائعة ===
        'support_menu_header': "⚙️ <b>الدعم</b>\n\nإذا كان لديك أي أسئلة، يمكنك العثور على الإجابات في قسم الأسئلة الشائعة أو الكتابة إلى خدمة الدعم لدينا.",
        'faq_button': "⁉️ الأسئلة الشائعة (FAQ)",
        'contact_support_button': "👨‍💻 الكتابة إلى الدعم",
        'faq_menu_header': "❓ <b>الأسئلة الشائعة</b> ❓",
        'faq_items': {
            'q1': {
                'question': "⚙️ كيف يعمل البوت؟ ",
                'answer': '''
- يعتمد بوت @SportNeyroAnalitikbot على شبكات عصبية مدربة خصيصاً لتحليل البيانات، ويوفر تحليلاً تفصيلياً للأحداث الرياضية، ويتم تحديث البوت واختباره، وجميع ملاحظاتك يتم اختبارها!

<b>1. جمع البيانات:</b>
يجمع البوت البيانات من مصادر متعددة، مع الأخذ في الاعتبار العوامل التي تؤثر على نتيجة المباراة.

<b>2. التنبؤ بالنتائج:</b>
بناءً على التحليل، يقوم البوت بإنشاء تنبؤ بالنتيجة المحتملة للمباراة، مع الأخذ في الاعتبار المعلومات التي تم جمعها.

<b>3. تحليل مفصل:</b>
يتلقى المستخدم ليس فقط أرقاماً، بل شرحاً للعوامل الرئيسية.

<b>4. التحديثات في الوقت الفعلي:</b>
يتم تحسين الخوارزميات باستمرار، مما يضمن دقة عالية للتنبؤات.

❤️ <i>نسعى لجعل التحليلات الرياضية في متناول الجميع. سواء كنت من محبي الرياضة، أو محللاً محترفاً، أو مشاركاً في سوق المراهنات.</i>
                '''
            },
            'q2': {
                'question': "🎫 كيف تعمل الاشتراكات؟",
                'answer': '''
🎫 توفر الاشتراكات وصولاً إلى عدد معين من التنبؤات العادية والمميزة المؤقتة لفترة محددة <i>(أسبوع، أسبوعين)</i>.

💎 توفر <b>أسعاراً أكثر ملاءمة</b> مقارنة بشراء التنبؤات الفردية.

‼️ <b>من المهم تذكر</b> أنه عند شراء اشتراك جديد، يتم إلغاء الاشتراك القديم، وتلغى التنبؤات المؤقتة غير المستخدمة عند انتهاء صلاحية الاشتراك.
                '''
            },
            'q3': {
                'question': "📊 كيف تعمل التنبؤات؟",
                'answer': '''
<b>يقدم البوت نوعين من التنبؤات:</b>

🔹 <b>التنبؤات العادية:</b> توفر معلومات موجزة حول نتيجة المباراة، الاحتمالات، والعوامل الرئيسية.

💠 <b>تنبؤات VIP:</b> تقدم تحليلاً أعمق وأكثر تفصيلاً، بما في ذلك بيانات إضافية وشروحات موسعة لاتخاذ قرارات أكثر استنارة.
    '''
            },
            'q4': {
                'question': "⏳ ما هو الفرق بين التنبؤات المؤقتة؟ ",
                'answer': '''
⏳ عند شراء اشتراك، تتلقى بالضبط <b>تنبؤات مؤقتة</b> ستكون متاحة حتى انتهاء صلاحية الاشتراك. على سبيل المثال، إذا كنت تخطط للمراهنة بانتظام، فإن شراء اشتراك سيكون أكثر ربحية بكثير من المشتريات لمرة واحدة.
                '''
            },
            'q5': {
                'question': "💳 كيف تشتري اشتراكاً؟",
                'answer': '''
💳 لشراء اشتراك، انتقل إلى "الكتالوج" في القائمة الرئيسية للبوت، ثم حدد "الاشتراكات" والخطة المطلوبة. اتبع تعليمات البوت للدفع.
                '''
            },
            'q6': {
                'question': "💳 كيف تشتري تنبؤات؟",
                'answer': '''
💳 لشراء تنبؤات، انتقل إلى "الكتالوج" في القائمة الرئيسية للبوت، ثم حدد "التنبؤات" والعدد المطلوب من التنبؤات العادية أو VIP. اتبع تعليمات البوت للدفع.
    '''
            },
            'q7': {
                'question': "📊 كيف تنشئ تنبؤاً؟",
                'answer': '''
📊 لإنشاء تنبؤ حسب الطلب، حدد زر "إنشاء تنبؤ" في القائمة الرئيسية للبوت. ثم أدخل المعلومات اللازمة حول الحدث الرياضي، باتباع مطالبات البوت.
    '''
            },
            'q8': {
                'question': "🎟 كيف تعمل الرموز الترويجية؟ ",
                'answer': '''
🎟 يتم إدخال الرموز الترويجية في قسم خاص "الرمز الترويجي" في القائمة الرئيسية للبوت. وهي تفعل المكافآت التي يمكن أن يقدمها فريق Neyro Team. توجد أيضاً رموز ترويجية للحصول على مكافآت عند التسجيل لدى شركاء شركات المراهنات.
    '''
            },
            'q9': {
                'question': "✍️ كيف تترك تقييماً؟",
                'answer': '''
✍️ يمكنك ترك تقييم بالانتقال إلى بوت @OtziviSportbot أو بتحديد زر "اترك تقييماً" في قسم "التقييمات" في قائمة @SportNeyroAnalitikbot.
                '''
            },
            'q10': {
                'question': "👀 أين تقرأ التقييمات؟",
                'answer': '''
👀 يمكنك قراءة تقييمات المستخدمين الآخرين بتحديد زر "قراءة التقييمات" في قسم "التقييمات" في قائمة @SportNeyroAnalitikbot.
    '''
            },
            'q11': {
                'question': "✅ أين تراهن على الرياضة؟",
                'answer': '''
✔️ لوضع المراهنات الرياضية، بناءً على التنبؤات المستلمة من البوت، نوصي باستخدام شركاء شركات المراهنات المعتمدين التالية:

<b>1Win:</b> <i>https://1wzyuh.com/v3/landing-page/football?p=5ibz</i>
(الرمز الترويجي: NEYRO99)
<b>Winline:</b> <i>https://partners2.winline.ru/s/Ebp0XjlFwM?statid=2925_</i>
(الرمز الترويجي: NEYRO3000)
                '''
            },
            'q12': {
                'question': "🌍 ما هي اللغات المتاحة للبوت؟",
                'answer': '''
يدعم بوت @SportNeyroAnalitikbot 6 لغات دولية 🌍 للأمم المتحدة: الروسية، الإنجليزية، العربية، الإسبانية، الصينية، والفرنسية. يمكنك تحديد اللغة المطلوبة في إعدادات البوت.
            '''
            },
            'q13': {
                'question': "🤝 كيف يعمل برنامج الإحالة؟",
                'answer': '''
🫂 يتمتع كل مستخدم لـ @SportNeyroAnalitikbot بفرصة المشاركة في برنامج الإحالة الخاص بنا وتلقي مكافآت مقابل الأصدقاء المدعوين.

• <b>رابط الإحالة الخاص بك:</b> لكل حساب في البوت رابط إحالة فريد. يمكنك العثور عليه في "ملفك الشخصي".
• <b>كيف يعمل:</b> شارك رابط الإحالة الفريد الخاص بك مع الأصدقاء. عندما ينقر صديقك على رابطك، ويسجل في البوت، ويقوم بأول عملية شراء (أي اشتراك أو تنبؤ)، ستتلقون كلاكما مكافأة.
• <b>المكافأة:</b> لكل إحالة يقوم بعملية شراء، يتلقى كل من أنت وصديقك المدعو تنبؤ VIP واحد.
• <b>التتبع:</b> يتم عرض عدد الأصدقاء المدعوين في "ملفك الشخصي".

<b>كلما دعوت المزيد من الأصدقاء، كلما حصلت على المزيد من المكافآت!</b>
                '''
            },
            'q14': {
                'question': '''💼 كيف تصبح شريكاً لـ "Neyro Team"؟''',
                'answer': '''
💸 إذا كنت <b>معلناً، أو مسوقاً، أو مهتماً بالإعلان المتبادل</b>، يمكنك الاتصال بفريق الدعم لدينا على Telegram على @SuportNeyroTeam لمناقشة شروط التعاون.
    '''
            }
        },

        # === كتلة جديدة: مسارات الصور ===
        'photo_profil': "images/ar/profil.png",
        'photo_katalog': "images/ar/katalog.png",
        'photo_katalog_prognoz': "images/ar/katalog_prognoz.png",
        'photo_katalog_subscriptions': "images/ar/katalog_subscriptions.png",
        'photo_otzivi': "images/ar/otzivi.png",
        'photo_tip_prognoza': "images/ar/tip_prognoza.png",
        'ob_prognoz_photo': "images/ar/ob_prognoz.png",
        'vip_prognoz_photo': "images/ar/vip_prognoz.png",
        'photo_instruction': "images/ar/instruction.png",
        'photo_support': "images/ar/support.png",
        'photo_faq': "images/ar/faq.png",
        'photo_cponsori': "images/ar/cponsori.png"
    },
    'zh': {
        # ==============================
        # 1. 通用命令和消息
        # ==============================
        'start': "✅ 启动机器人",
        'admin': "👨‍💻 管理面板",
        'cancel': "🔙 取消",
        'traffer': "🥷 营销员面板",
        'cancel_disvie': "🚫 操作已取消。",

        'traff_info': '''
    👤 营销员: {trafer_name}
    👤 用户名: {t_username}
    🆔 ID: {t_id}
    🏷️ 促销代码: {t_promo}

    📱 电话: {t_telefon}
    💳 银行卡: {t_karta}
    🪙 加密货币: {t_kripta}
    🔗 网络: {crypto_network}

    📊 收入方式: {human_model}
    📊 潜在客户: {leads}

    🏦 余额: {balance}₽
    💸 已提现: {paid}₽
    💰 总收益: {total}₽
                ''',

        'edit_traffera': "✏️ 编辑营销员",
        'obnovit_traf_info': "🔄 更新",
        'traff_id_kanala': "🆔 频道ID: {pay_link}",
        'traff_priglos_ssilka': "🔗 邀请链接:\n{invite_link}",
        'del_traffera': "❌ 删除营销员",
        'back': "↩️ 返回",
        'obnovit_podpiski': "🔄 更新订阅",
        'vivisti_money': "💸 提现",
        'back_traff_panel': "🔙 退出营销员面板",
        'command_start': "启动机器人",
        'command_admin': "管理面板",
        'command_traffer': "营销员面板",
        'podpiska_istekla': "订阅已过期",
        'bolche_day': "{days} 天 {hours} 小时",
        'menche_day': "{hours} 小时 {minutes} 分钟",
        'menche_hour': "{minutes} 分钟",
        'spasibo_za_oplaty': "感谢您的付款！已激活访问权限。",
        'chek_partners': "🔁 检查订阅",
        'pustoy_spisok_partners': "合作夥伴列表为空",
        'NO_chek_partners': "请订阅所有合作夥伴才能继续。",

        'edit_name': "姓名",
        'edit_id': "ID",
        'edit_username': "@用户名",
        'edit_telefon': "电话",
        'edit_karta': "银行卡",
        'edit_kripta': "加密货币钱包",
        'edit_crypto_network': "加密货币网络",
        'cancel_edit': "↩️ 取消",

        # 新增：编辑提示
        'enter_new_name': "请输入新名称：",
        'enter_new_id': "请输入新ID：",
        'enter_new_username': "请输入新的@用户名：",
        'enter_new_telefon': "请输入新电话：",
        'enter_new_karta': "请输入新的银行卡：",
        'enter_new_kripta': "请输入新的加密货币钱包：",
        'enter_new_crypto_network': "请输入新的加密货币网络：",
        'traffer_updated_success': "✅ 营销员数据已成功更新！",
        'no_traffer_found': "未找到营销员。",

        "referral_reward": "您已获得1个永久VIP预测作为推荐奖励！",
        "profile_text": '''
➖➖➖➖➖➖➖➖➖

👤 *{user_name}* | *ID:* `{user_id}`
🎫 *订阅:* *{subscription}*
⌛️ *剩余到期时间:* *{remaining}*

🔹 *预测:* *{ob_prognoz}*
💠 *VIP预测:* *{rach_prognoz}*
🔹 *临时预测:* *{ob_vr_prognoz}*
💠 *临时VIP预测:* *{rach_vr_prognoz}*

👥 *邀请好友:* {referred_count}
🔗 *您的推荐链接:*

`{referral_link}`

➖➖➖➖➖➖➖➖➖

‼️ *Beta测试正在进行中*
所有功能均免费提供。

➖➖➖➖➖➖➖➖➖
            ''',

        'sozdat_prognoz': "📊 创建预测",
        'katalog': "🛍 目录",
        'otzivi': "🗣️ 评论",
        'promokod': "#️⃣ 促销代码",
        'support': "⚙️ 支持",
        'instruction': "📘 说明",
        'error_profile': "获取个人资料数据时出错。",

        'NOT_od_prognoz': "❌ 您没有普通预测！",
        'NOT_VIP_prognoz': "❌ 您没有VIP预测！",
        'vvedite_daty_vremia': "🗓 输入比赛日期和时间（例如：01.01.2025 18:00）：",
        'vvedite_vid_sporta': "⚽️ 输入体育类型（例如：足球）：",
        'vvedite_commandi': "👥 输入队伍名称，用逗号分隔（队伍#1, 队伍#2）：",

        'error_vvedite_commandi': '''
请准确输入两个队伍名称，用逗号分隔
（例如：队伍1, 队伍2）。
                ''',

        'message_promokod': '''
✅ 促销代码已接受！
您已获得 🔹 {add_ob_prognoz} 个普通预测和 💠 {add_rach_prognoz} 个VIP预测。
🎫 订阅: {subscription}
                ''',

        'vvevite_promocod_1': "⏳ 输入促销代码",
        'vvevite_promocod_2': "请输入促销代码：",
        'primenit_promocod': "✅ 应用促销代码",
        'najmi_primenit_promocod': "点击下方按钮应用促销代码 👇",
        'yes_promocod_ot_traffera': "✅ 营销员促销代码已接受！您已获得1个普通预测。",
        'ispolzovan_promocod': "❌ 您已使用过此促销代码。",
        'nedeistvitelen_promocod': "❌ 此促销代码无效。",
        'promocod_ne_nayden': "❌ 未找到促销代码。",

        'promocod_ot_traffera_YES': '''
            ✅ 促销代码已激活！
            + 1 个普通预测。
                ''',

        'error_close_panel': "无法关闭面板 😔",

        'yes_dannie': "✅ 确认数据",
        'no_dannie': "🔄 重新输入数据",
        'obrabotka_prognoza': "⏳ 正在处理您的预测…",
        'no_registr_traffera': "⛔ 您未注册为营销员。",
        'balans_menche_1000': "提现金额需满1000 ₽",
        'ot_1000_do_balans': "请输入提现金额（从1000到{balance}₽）：",
        'vvedite_celoe_chislo': "请输入一个整数！",
        'summa_bolche_1000': "金额必须至少为1000 ₽！",
        'summa_bolche_balansa': "金额超出您当前余额！",
        'redactirovat': "✏️ 编辑",
        'podtverdit': "✅ 确认",
        'proverka_summi': "您确定要提取 {amt}₽ 吗？",
        'yes_viplata': "✅ 成功提取 {amt}₽。",
        'no_viplata': "❌ {amt}₽ 提现未被接受。请联系支持：https://t.me/suportneyroteam",

        'katalog_podpisok': '''
➖➖➖➖➖➖➖➖➖

🎫 *{price_standart}₽ - 标准*，一周
您将获得5个预测，0个VIP预测

🎫 *{price_medium}₽ - 中等*，一周
您将获得12个预测，6个VIP预测

🎫 *{price_premium}₽ - 高级*，两周
您将获得30个预测，15个VIP预测

➖➖➖➖➖➖➖➖➖

‼️ *Beta测试正在进行中*
所有功能均免费提供。

➖➖➖➖➖➖➖➖➖

💳 请选择以下订阅进行支付：
                ''',

        'katalog_prognozov': '''
➖➖➖➖➖➖➖➖➖➖➖➖➖➖

🔹 *{price_1_ob}₽* - 1个预测
🔹 *{price_5_ob}₽* - 5个预测
🔹 *{price_15_ob}₽* - 15个预测

💠 *{price_1_vip}₽* - 1个VIP预测
💠 *{price_5_vip}₽* - 5个VIP预测
💠 *{price_15_vip}₽* - 15个VIP预测

➖➖➖➖➖➖➖➖➖➖➖➖➖➖

‼️ *Beta测试正在进行中*
所有功能均免费提供。

➖➖➖➖➖➖➖➖➖➖➖➖➖➖

💳 请选择以下套餐进行支付：
                ''',

        'standart': "💥 您的订阅已升级为标准，为期一周！",
        'medium': "💥 您的订阅已升级为中等，为期一周！",
        'premium': "💥 您的订阅已升级为高级，为期2周！",
        'podpiski': "🎫 订阅",
        'prognozi': "📊 预测",
        'catalog_text': "欢迎来到目录！请选择一个部分：",
        '1_ob_prognoz': "🔹 {price_1_ob}₽ - 1",
        '1_rach_prognoz': "💠 {price_1_vip}₽ - 1 VIP",
        '5_ob_prognoz': "🔹 {price_5_ob}₽ - 5",
        '5_rach_prognoz': "💠 {price_5_vip}₽ - 5 VIP",
        '15_ob_prognoz': "🔹 {price_15_ob}₽ - 15",
        '15_rach_prognoz': "💠 {price_15_vip}₽ - 15 VIP",

        'ob_prognoz': "🔹 预测",
        'vip_prognoz': "💠 VIP预测",
        'profile': "👤 个人资料",
        'vibirite_tip_prognoza': "📊 选择预测类型：",

        'read_otzivi': "👥 阅读评论",
        'ostvit_otziv': "🆕 留下评论",
        'vip_prognozov': "VIP预测",
        'ob_progozov': "普通预测",
        'dobavleno_prognozov': "✅ 已添加 {count} {label}！",
        'iazik': "🌐 更改语言",
        'iazik_yes': "✅ 语言已选择！",
        'vibr_iazik': "🌐 选择语言：",
        'partners_header': "<b>合作伙伴：</b>",
        'subscribe_to': "订阅",

        # === 新增区块：说明 ===
        'instruction_menu_header': "📘 <b>说明</b>\n\n请选择您感兴趣的部分：",
        'full_instruction_button': "📘 阅读完整说明",
        'instruction_link': "https://telegra.ph/SPORT-ANALITIK-BOT-%E4%BD%BF%E7%94%A8%E8%AF%B4%E6%98%8E-zh-07-01",
        'instruction_blocks': {

            'kakrabotaetbot': {
                'title': "⚙️ 机器人如何运作？",
                'text': '''
- @SportNeyroAnalitikbot 机器人基于专门训练用于数据分析的神经网络，提供详细的体育赛事分析。机器人会不断更新和测试，您的所有反馈都会经过验证！

<b>1. 数据收集：</b>
机器人从大量来源收集数据，考虑影响比赛结果的参数。

<b>2. 结果预测：</b>
根据分析，机器人创建比赛可能结果的预测，考虑所收集的信息。

<b>3. 详细分析：</b>
用户不仅会收到数字，还会收到关键因素的解释。

<b>4. 实时更新：</b>
算法不断改进，确保预测的高精度。

❤️ <i>我们努力让每个人都能接触到体育分析。无论您是体育迷、专业分析师，还是博彩市场参与者。</i>
                '''
            },
            'podpiski': {
                'title': "🎫 订阅",
                'text': '''
‼️ <b>重要提示：</b>
1. 购买新订阅时，现有活跃订阅（如果有）将被取消。
2. 订阅期结束后，所有未使用的临时预测将作废。

🎫 <b>标准</b> — <i>199₽ / 周</i> | 5个普通预测，0个VIP预测。

适合初学者和喜欢独立选择赛事的人。

🎫 <b>中等</b> — <i>999₽ / 周</i> | 12个普通预测，6个VIP预测。

适合希望深入分析的经验用户。

🎫 <b>高级</b> — <i>1899₽ / 2周</i> | 30个普通预测，15个VIP预测。

为活跃玩家提供最大收益。

<b>为什么订阅划算？</b> 订阅可以帮您省钱。购买单个预测可能比购买一定期限的订阅更昂贵。

<b>如果您计划定期投注</b>，订阅将比单次购买划算得多。
                '''
            },
            'prognozi': {
                'title': "🔹 预测 / 💠 VIP预测",
                'text': '''
🔷 <b>普通预测（简要分析）：</b>

普通预测包含有关即将到来的比赛或事件的简要清晰信息。它包括基本数据，例如预期的比赛结果、赔率以及影响结果的关键因素。这种预测类型适合那些希望在下注前快速获取基本信息的人。

🪙 <b>价格：</b>

59 ₽ — 1个预测
249 ₽ — 5个预测 <i>（节省15.6%）</i>
450 ₽ — 15个预测 <i>（节省49.2%）</i>

💠 <b>VIP预测（详细分析）：</b>

VIP预测提供对体育赛事更深入、更详细的分析。除了基本信息，它们还包括额外数据和更详尽的回答，以便更好地理解即将到来的比赛以及可能影响比赛结果的其他重要方面。这些预测将帮助您更好地理解情况并做出更明智的决定。

🪙 <b>价格：</b>

99 ₽ — 1个VIP预测
399 ₽ — 5个VIP预测 <i>（节省19.4%）</i>
1159 ₽ — 15个VIP预测 <i>（节省22.0%）</i>
    '''
            },
            'buy': {
                'title': "💳 购买",
                'text': '''
💳 购买预测

要购买普通或VIP预测，请使用机器人主菜单中的“目录”部分。

<b>步骤1：</b> 在机器人主菜单中，选择“目录”按钮。
<b>步骤2：</b> 在“目录”中，选择“预测”部分。
<b>步骤3：</b> 选择所需数量的普通或VIP预测。
<b>步骤4：</b> 按照机器人的说明完成支付。

—————————-

💳 购买订阅

要购买订阅以获得更多预测和优惠的VIP预测，请按照以下步骤操作：

<b>步骤1：</b> 在机器人主菜单中，选择“目录”按钮。
<b>步骤2：</b> 在“目录”中，选择“订阅”部分。
<b>步骤3：</b> 选择适合您的订阅类型
（标准、中等或高级）。
<b>步骤4：</b> 按照机器人的说明完成支付。
                '''
            },
            'createprognoz': {
                'title': "👨‍💻 创建预测",
                'text': '''
🤖 <b>机器人</b> @SportNeyroAnalitikbot 允许您按需创建预测。要创建预测，您需要：

<b>步骤1：</b> 在机器人主菜单中，选择“创建预测”按钮。
<b>步骤2：</b> 处理请求并分析比赛后，机器人将为您提供预测。

‼️ <b>重要提示</b>
请正确、仔细地填写比赛信息，如果出错，将不予退款。
                '''
            },
            'promokodi': {
                'title': "🎟 促销代码",
                'text': '''
<b>@SportNeyroAnalitikbot 机器人中的促销代码为您提供额外奖励。</b>

<b>步骤1：</b> 在机器人主菜单中，选择“促销代码”按钮。
<b>步骤2：</b> 在相应字段中输入您的促销代码。
<b>步骤3：</b> 点击“应用”以激活促销代码并领取奖励。

🔭 关注 <a href="https://t.me/NeyroTeamTg">Neyro Team</a> 频道的最新消息，以免错过新的促销代码。
                '''
            },
            'bukmekeri': {
                'title': "✅ 最佳博彩公司",
                'text': '''
👍 <b>根据机器人提供的预测进行体育投注，我们推荐使用以下经过验证的博彩公司合作伙伴：</b>

<b>1Win:</b> <i>https://1wzyuh.com/v3/landing-page/football?p=5ibz</i>
使用促销代码“NEYRO99”注册即可获得奖金。
<b>Winline:</b> <i>https://partners2.winline.ru/s/Ebp0XjlFwM?statid=2925_</i>
使用促销代码“NEYRO3000”注册即可获得奖金。
                '''
            },
            'ozivi': {
                'title': "🗣 评论",
                'text': '''
♥️ <b>您的意见对我们非常重要！</b> 您可以留下对机器人工作的评论并阅读其他用户的意见。

✍️ <b>留下评论：</b> 要分享您的意见，请前往 @OtziviSportbot 机器人或在 @SportNeyroAnalitikbot 菜单中的“评论”部分选择“留下评论”按钮。按照机器人说明撰写评论。

🗣 <b>阅读评论：</b> 要阅读其他用户的评论，请在 @SportNeyroAnalitikbot 菜单中的“评论”部分选择“阅读评论”按钮或前往 Telegram 频道 @OTZIVISPORTANALITIK
                '''
            },
            'iaziki': {
                'title': "🌍 语言",
                'text': '''
<b>@SportNeyroAnalitikbot 机器人专为全球受众设计，支持联合国6种国际语言：</b>

🇷🇺🇬🇧🇪🇸🇨🇳🇫🇷🇸🇦

俄语、英语、西班牙语、中文、法语、阿拉伯语

您可以通过在机器人主菜单中选择相应选项轻松更改机器人界面的语言。这使您无论身处何地，都能以最舒适的方式使用机器人的所有功能。
                '''
            },
            'refi': {
                'title': "🤝 推荐计划",
                'text': '''
🫂 @SportNeyroAnalitikbot 的每个用户都有机会参与我们的推荐计划，并因邀请朋友而获得奖金。

• <b>您的推荐链接：</b> 机器人中的每个账户都有一个唯一的推荐链接。您可以在“个人资料”中找到它。
• <b>如何运作：</b> 将您唯一的推荐链接分享给朋友。当您的朋友点击您的链接，在机器人中注册并完成首次购买（任何订阅或预测）时，您和您的朋友都将获得奖金。
• <b>奖金：</b> 对于每位进行购买的推荐，您和您邀请的朋友都将获得1个VIP预测。
• <b>跟踪：</b> 邀请的朋友数量显示在您的“个人资料”中。

<b>您邀请的朋友越多，获得的奖金就越多！</b>
                '''
            },
            'partnerstvo': {
                'title': "💼 合作",
                'text': '''
💸 如果您是广告商、营销员或对相互广告感兴趣，可以联系我们在 Telegram 上的支持团队 @SuportNeyroTeam 讨论合作条款。
                '''
            }

        },

        # === 新增区块：支持和常见问题 ===
        'support_menu_header': "⚙️ <b>支持</b>\n\n如果您有任何问题，可以在常见问题部分找到答案或联系我们的支持服务。",
        'faq_button': "⁉️ 常见问题 (FAQ)",
        'contact_support_button': "👨‍💻 联系支持",
        'faq_menu_header': "❓ <b>常见问题</b> ❓",
        'faq_items': {
            'q1': {
                'question': "⚙️ 机器人如何运作？ ",
                'answer': '''
- @SportNeyroAnalitikbot 机器人基于专门训练用于数据分析的神经网络，提供详细的体育赛事分析。机器人会不断更新和测试，您的所有反馈都会经过验证！

<b>1. 数据收集：</b>
机器人从大量来源收集数据，考虑影响比赛结果的参数。

<b>2. 结果预测：</b>
根据分析，机器人创建比赛可能结果的预测，考虑所收集的信息。

<b>3. 详细分析：</b>
用户不仅会收到数字，还会收到关键因素的解释。

<b>4. 实时更新：</b>
算法不断改进，确保预测的高精度。

❤️ <i>我们努力让每个人都能接触到体育分析。无论您是体育迷、专业分析师，还是博彩市场参与者。</i>
                '''
            },
            'q2': {
                'question': "🎫 订阅如何运作？",
                'answer': '''
🎫 订阅在固定期限内（一周、两周）提供一定数量的临时普通预测和VIP预测。

💎 与购买单个预测相比，它们提供<b>更优惠的价格</b>。

‼️ <b>请务必记住</b>，购买新订阅时，旧订阅将被取消，未使用的临时预测在订阅期结束后作废。
                '''
            },
            'q3': {
                'question': "📊 预测如何运作？",
                'answer': '''
<b>机器人提供两种预测类型：</b>

🔹 <b>普通预测：</b> 提供关于比赛结果、赔率和关键因素的简要信息。

💠 <b>VIP预测：</b> 提供更深入、更详细的分析，包括额外数据和扩展解释，以便做出更明智的决策。
    '''
            },
            'q4': {
                'question': "⏳ 临时预测有什么区别？ ",
                'answer': '''
⏳ 购买订阅时，您将获得<b>临时预测</b>，这些预测在订阅到期前都可用。例如，如果您计划定期投注，购买订阅将比单次购买划算得多。
                '''
            },
            'q5': {
                'question': "💳 如何购买订阅？",
                'answer': '''
💳 要购买订阅，请前往机器人主菜单中的“目录”，然后选择“订阅”和所需计划。按照机器人说明进行支付。
                '''
            },
            'q6': {
                'question': "💳 如何购买预测？",
                'answer': '''
💳 要购买预测，请前往机器人主菜单中的“目录”，然后选择“预测”和所需数量的普通或VIP预测。按照机器人说明进行支付。
    '''
            },
            'q7': {
                'question': "📊 如何创建预测？",
                'answer': '''
📊 要按需创建预测，请选择机器人主菜单中的“创建预测”按钮。然后，根据机器人的提示，输入有关体育赛事的必要信息。
    '''
            },
            'q8': {
                'question': "🎟 促销代码如何运作？ ",
                'answer': '''
🎟 促销代码在机器人主菜单中的特殊部分“促销代码”中输入。它们激活由 Neyro Team 提供的奖金。还有一些促销代码用于在注册博彩公司合作伙伴时获得奖金。
    '''
            },
            'q9': {
                'question': "✍️ 如何留下评论？",
                'answer': '''
✍️ 您可以通过前往 @OtziviSportbot 机器人或在 @SportNeyroAnalitikbot 菜单中的“评论”部分选择“留下评论”按钮来留下评论。
                '''
            },
            'q10': {
                'question': "👀 在哪里阅读评论？",
                'answer': '''
👀 您可以通过在 @SportNeyroAnalitikbot 菜单中的“评论”部分选择“阅读评论”按钮来阅读其他用户的评论。
    '''
            },
            'q11': {
                'question': "✅ 在哪里进行体育投注？",
                'answer': '''
✔️ 根据机器人提供的预测进行体育投注，我们推荐使用以下经过验证的博彩公司合作伙伴：

<b>1Win:</b> <i>https://1wzyuh.com/v3/landing-page/football?p=5ibz</i>
（促销代码：NEYRO99）
<b>Winline:</b> <i>https://partners2.winline.ru/s/Ebp0XjlFwM?statid=2925_</i>
（促销代码：NEYRO3000）
                '''
            },
            'q12': {
                'question': "🌍 机器人支持哪些语言？",
                'answer': '''
@SportNeyroAnalitikbot 机器人支持联合国6种国际语言🌍：俄语、英语、阿拉伯语、西班牙语、中文和法语。您可以在机器人设置中选择所需的语言。
                '''
            },
            'q13': {
                'question': "🤝 推荐计划如何运作？",
                'answer': '''
🫂 @SportNeyroAnalitikbot 的每个用户都有机会参与我们的推荐计划，并因邀请朋友而获得奖金。

• <b>您的推荐链接：</b> 机器人中的每个账户都有一个唯一的推荐链接。您可以在“个人资料”中找到它。
• <b>如何运作：</b> 将您唯一的推荐链接分享给朋友。当您的朋友点击您的链接，在机器人中注册并完成首次购买（任何订阅或预测）时，您和您的朋友都将获得奖金。
• <b>奖金：：</b> 对于每位进行购买的推荐，您和您邀请的朋友都将获得1个VIP预测。
• <b>跟踪：</b> 邀请的朋友数量显示在您的“个人资料”中。

<b>您邀请的朋友越多，获得的奖金就越多！</b>
                '''
            },
            'q14': {
                'question': '''💼 如何成为“Neyro Team”的合作伙伴？''',
                'answer': '''
💸 如果您是<b>广告商、营销员或对相互广告感兴趣</b>，可以联系我们在 Telegram 上的支持团队 @SuportNeyroTeam 讨论合作条款。
    '''
            }
        },

        # === 新增区块：图片路径 ===
        'photo_profil': "images/zh/profil.png",
        'photo_katalog': "images/zh/katalog.png",
        'photo_katalog_prognoz': "images/zh/katalog_prognoz.png",
        'photo_katalog_subscriptions': "images/zh/katalog_subscriptions.png",
        'photo_otzivi': "images/zh/otzivi.png",
        'photo_tip_prognoza': "images/zh/tip_prognoza.png",
        'ob_prognoz_photo': "images/zh/ob_prognoz.png",
        'vip_prognoz_photo': "images/zh/vip_prognoz.png",
        'photo_instruction': "images/zh/instruction.png",
        'photo_support': "images/zh/support.png",
        'photo_faq': "images/zh/faq.png",
        'photo_cponsori': "images/zh/cponsori.png"
    },

    'fr': {
        # ==============================
        # 1. Commandes et messages généraux
        # ==============================
        'start': "✅ Démarrer le bot",
        'admin': "👨‍💻 Tableau de bord admin",
        'cancel': "🔙 Annuler",
        'traffer': "🥷 Tableau de bord trafficker",
        'cancel_disvie': "🚫 Action annulée.",

        'traff_info': '''
👤 Trafficker : {trafer_name}
👤 Nom d'utilisateur : {t_username}
🆔 ID : {t_id}
🏷️ Code promo : {t_promo}

📱 Téléphone : {t_telefon}
💳 Carte : {t_karta}
🪙 Crypto : {t_kripta}
🔗 Réseau : {crypto_network}

📊 Méthode de gain : {human_model}
📊 Leads : {leads}

🏦 Solde actuel : {balance}₽
💸 Montant retiré : {paid}₽
💰 Gains totaux : {total}₽
                ''',

        'edit_traffera': "✏️ Modifier le trafficker",
        'obnovit_traf_info': "🔄 Actualiser",
        'traff_id_kanala': "🆔 ID du canal : {pay_link}",
        'traff_priglos_ssilka': "🔗 Lien d'invitation :\n{invite_link}",
        'del_traffera': "❌ Supprimer le trafficker",
        'back': "↩️ Retour",
        'obnovit_podpiski': "🔄 Actualiser les abonnements",
        'vivisti_money': "💸 Retirer de l'argent",
        'back_traff_panel': "🔙 Quitter le tableau de bord trafficker",
        'command_start': "Démarrer le bot",
        'command_admin': "Tableau de bord admin",
        'command_traffer': "Tableau de bord trafficker",
        'podpiska_istekla': "Abonnement expiré",
        'bolche_day': "{days} jours {hours} heures.",
        'menche_day': "{hours} heures {minutes} min.",
        'menche_hour': "{minutes} min.",
        'spasibo_za_oplaty': "Merci pour votre paiement ! Accès activé.",
        'chek_partners': "🔁 Vérifier l'abonnement",
        'pustoy_spisok_partners': "La liste des partenaires est vide",
        'NO_chek_partners': "Veuillez vous abonner à tous nos partenaires pour continuer.",

        'edit_name': "Nom",
        'edit_id': "ID",
        'edit_username': "@Nom_d'utilisateur",
        'edit_telefon': "Téléphone",
        'edit_karta': "Numéro de carte",
        'edit_kripta': "Portefeuille de crypto-monnaie",
        'edit_crypto_network': "Réseau de crypto-monnaie",
        'cancel_edit': "↩️ Annuler",

        # NOUVEAU: Messages d'édition
        'enter_new_name': "Saisissez le nouveau nom :",
        'enter_new_id': "Saisissez le nouvel ID :",
        'enter_new_username': "Saisissez le nouveau @Nom_d'utilisateur :",
        'enter_new_telefon': "Saisissez le nouveau numéro de téléphone :",
        'enter_new_karta': "Saisissez le nouveau numéro de carte :",
        'enter_new_kripta': "Saisissez la nouvelle adresse de portefeuille crypto :",
        'enter_new_crypto_network': "Saisissez le nouveau réseau de crypto-monnaie :",
        'traffer_updated_success': "✅ Données du trafficker mises à jour avec succès !",
        'no_traffer_found': "Trafficker introuvable.",

        "referral_reward": "Vous avez reçu un pronostic VIP permanent en récompense de votre parrainage !",
        "profile_text": '''
➖➖➖➖➖➖➖➖➖

👤 *{user_name}* | *ID :* `{user_id}`
🎫 *Abonnement :* *{subscription}*
⌛️ *Expiration dans :* *{remaining}*

🔹 *Pronostics réguliers :* *{ob_prognoz}*
💠 *Pronostics VIP :* *{rach_prognoz}*
🔹 *Pronostics temporaires :* *{ob_vr_prognoz}*
💠 *Pronostics VIP temporaires :* *{rach_vr_prognoz}*

👥 *Amis invités :* {referred_count}
🔗 *Votre lien de parrainage :*

`{referral_link}`

➖➖➖➖➖➖➖➖➖

‼️ *Test bêta en cours*
Toutes les fonctionnalités sont disponibles gratuitement.
    
➖➖➖➖➖➖➖➖➖
                ''',

        'sozdat_prognoz': "📊 Créer un pronostic",
        'katalog': "🛍 Catalogue",
        'otzivi': "🗣️ Avis",
        'promokod': "#️⃣ Code promo",
        'support': "⚙️ Support",
        'instruction': "📘 Instructions",
        'error_profile': "Erreur lors de la récupération des données de profil.",

        'NOT_od_prognoz': "❌ Vous n'avez pas de pronostics réguliers disponibles !",
        'NOT_VIP_prognoz': "❌ Vous n'avez pas de pronostics VIP disponibles !",
        'vvedite_daty_vremia': "🗓 Entrez la date et l'heure du match (Exemple : 01.01.2025 18:00) :",
        'vvedite_vid_sporta': "⚽️ Entrez le type de sport (Exemple : football) :",
        'vvedite_commandi': "👥 Entrez les noms des équipes, séparés par une virgule (Équipe 1, Équipe 2) :",

        'error_vvedite_commandi': '''
Veuillez entrer exactement deux noms d'équipe, séparés par une virgule
(Exemple : Équipe1, Équipe2).
                ''',

        'message_promokod': '''
    ✅ Code promo accepté !
Vous avez reçu 🔹 {add_ob_prognoz} pronostic(s) régulier(s) et 💠 {add_rach_prognoz} pronostic(s) VIP.
🎫 Abonnement : {subscription}
                ''',

        'vvevite_promocod_1': "⏳ Entrez le code promo",
        'vvevite_promocod_2': "Entrez le code promo :",
        'primenit_promocod': "✅ Appliquer le code promo",
        'najmi_primenit_promocod': "Cliquez sur le bouton ci-dessous pour appliquer le code promo 👇",
        'yes_promocod_ot_traffera': "✅ Code promo du trafficker accepté ! Vous avez reçu 1 pronostic régulier.",
        'ispolzovan_promocod': "❌ Vous avez déjà utilisé ce code promo.",
        'nedeistvitelen_promocod': "❌ Ce code promo n'est plus valide.",
        'promocod_ne_nayden': "❌ Code promo introuvable.",

        'promocod_ot_traffera_YES': '''
✅ Code promo activé !
+ 1 pronostic régulier.
                ''',

        'error_close_panel': "Impossible de fermer le panneau 😔",

        'yes_dannie': "✅ Confirmer les données",
        'no_dannie': "🔄 Ré-entrer les données",
        'obrabotka_prognoza': "⏳ Traitement de votre pronostic en cours…",
        'no_registr_traffera': "⛔ Vous n'êtes pas enregistré en tant que trafficker.",
        'balans_menche_1000': "Le retrait est disponible à partir de 1000 ₽",
        'ot_1000_do_balans': "Entrez le montant à retirer (de 1000 à {balance}₽) :",
        'vvedite_celoe_chislo': "Veuillez entrer un nombre entier !",
        'summa_bolche_1000': "Le montant doit être d'au moins 1000 ₽ !",
        'summa_bolche_balansa': "Le montant dépasse votre solde actuel !",
        'redactirovat': "✏️ Modifier",
        'podtverdit': "✅ Confirmer",
        'proverka_summi': "Voulez-vous retirer {amt}₽ ?",
        'yes_viplata': "✅ Retrait de {amt}₽ effectué avec succès.",
        'no_viplata': "❌ Le retrait de {amt}₽ n'a pas été accepté. Veuillez contacter le support : https://t.me/suportneyroteam",

        'katalog_podpisok': '''
➖➖➖➖➖➖➖➖➖

🎫 *{price_standart}₽ - Standard* pour une semaine
Accès à 5 pronostics réguliers, 0 pronostics VIP

🎫 *{price_medium}₽ - Moyen* pour une semaine
Accès à 12 pronostics réguliers, 6 pronostics VIP

🎫 *{price_premium}₽ - Premium* pour deux semaines
Accès à 30 pronostics réguliers, 15 pronostics VIP

➖➖➖➖➖➖➖➖➖

‼️ *Test bêta en cours*
Toutes les fonctionnalités sont disponibles gratuitement.

➖➖➖➖➖➖➖➖➖

💳 Choisissez un abonnement ci-dessous pour payer :
            ''',

    'katalog_prognozov': '''
➖➖➖➖➖➖➖➖➖➖➖➖➖➖

🔹 *{price_1_ob}₽* - 1 pronostic régulier
🔹 *{price_5_ob}₽* - 5 pronostics réguliers
🔹 *{price_15_ob}₽* - 15 pronostics réguliers

💠 *{price_1_vip}₽* - 1 pronostic VIP
💠 *{price_5_vip}₽* - 5 pronostics VIP
💠 *{price_15_vip}₽* - 15 pronostics VIP

➖➖➖➖➖➖➖➖➖➖➖➖➖➖

‼️ *Test bêta en cours*
Toutes les fonctionnalités sont disponibles gratuitement.

➖➖➖➖➖➖➖➖➖➖➖➖➖➖

💳 Choisissez un forfait ci-dessous pour payer :
                ''',

        'standart': "💥 Votre abonnement a été mis à niveau vers l'offre Standard pour une semaine !",
        'medium': "💥 Votre abonnement a été mis à niveau vers l'offre Moyenne pour une semaine !",
        'premium': "💥 Votre abonnement a été mis à niveau vers l'offre Premium pour 2 semaines !",
        'podpiski': "🎫 Abonnements",
        'prognozi': "📊 Pronostics",
        'catalog_text': "Bienvenue dans le catalogue ! Choisissez une section :",
        '1_ob_prognoz': "🔹 {price_1_ob}₽ - 1",
        '1_rach_prognoz': "💠 {price_1_vip}₽ - 1 VIP",
        '5_ob_prognoz': "🔹 {price_5_ob}₽ - 5",
        '5_rach_prognoz': "💠 {price_5_vip}₽ - 5 VIP",
        '15_ob_prognoz': "🔹 {price_15_ob}₽ - 15",
        '15_rach_prognoz': "💠 {price_15_vip}₽ - 15 VIP",

        'ob_prognoz': "🔹 Pronostic régulier",
        'vip_prognoz': "💠 Pronostic VIP",
        'profile': "👤 Profil",
        'vibirite_tip_prognoza': "📊 Sélectionnez le type de pronostic :",

        'read_otzivi': "👥 Lire les avis",
        'ostvit_otziv': "🆕 Laisser un avis",
        'vip_prognozov': "pronostics VIP",
        'ob_progozov': "pronostics réguliers",
        'dobavleno_prognozov': "✅ {count} {label} ajouté(s) !",
        'iazik': "🌐 Changer la langue",
        'iazik_yes': "✅ Langue sélectionnée !",
        'vibr_iazik': "🌐 Sélectionnez votre langue :",
        'partners_header': "<b>Partenaires :</b>",
        'subscribe_to': "S'abonner à",

        # === NOUVEAU BLOC : Instructions ===
        'instruction_menu_header': "📘 <b>Instructions</b>\n\nChoisissez la section qui vous intéresse :",
        'full_instruction_button': "📘 Lire toutes les instructions",
        'instruction_link': "https://telegra.ph/INSTRUCTIONS-DUTILISATION-DU-BOT-SPORT-ANALITIK-07-01",
        'instruction_blocks': {

            'kakrabotaetbot': {
                'title': "⚙️ Comment fonctionne le bot ?",
                'text': '''
- Le bot @SportNeyroAnalitikbot, basé sur des réseaux neuronaux spécialement entraînés pour l'analyse de données, offre une analyse détaillée des événements sportifs. Le bot est constamment mis à jour et testé, et tous vos commentaires sont pris en compte !

<b>1. Collecte de données :</b>
Le bot rassemble des données provenant de multiples sources, en considérant les paramètres qui influencent le résultat des matchs.

<b>2. Prédiction des résultats :</b>
Basé sur son analyse, le bot génère une prédiction des résultats probables des matchs, en intégrant les informations collectées.

<b>3. Analyse détaillée :</b>
Les utilisateurs ne reçoivent pas seulement des chiffres, mais aussi des explications sur les facteurs clés.

<b>4. Mises à jour en temps réel :</b>
Les algorithmes sont continuellement améliorés pour garantir une grande précision des prévisions.

❤️ <i>Notre objectif est de rendre l'analyse sportive accessible à tous. Que vous soyez un passionné, un analyste professionnel ou un acteur du marché des paris.</i>
                '''
            },
            'podpiski': {
                'title': "🎫 Abonnements",
                'text': '''
‼️ <b>IMPORTANT :</b>
1. Lorsque vous souscrivez un nouvel abonnement, l'abonnement actif (le cas échéant) est annulé.
2. À la fin de la période de validité de l'abonnement, tous les pronostics temporaires non utilisés sont annulés.

🎫 <b>Standard</b> — <i>199₽ / semaine</i> | 5 pronostics réguliers, 0 pronostics VIP.

Idéal pour les débutants et ceux qui préfèrent sélectionner leurs événements de manière autonome.

🎫 <b>Moyen</b> — <i>999₽ / semaine</i> | 12 pronostics réguliers, 6 pronostics VIP.

Convient aux utilisateurs expérimentés désireux d'approfondir leur analyse.

🎫 <b>Premium</b> — <i>1899₽ / 2 semaines</i> | 30 pronostics réguliers, 15 pronostics VIP.

Offre un maximum d'avantages pour les parieurs actifs.

<b>Pourquoi les abonnements sont-ils avantageux ?</b> Les abonnements vous permettent de réaliser des économies. Acheter des pronostics individuellement peut s'avérer plus coûteux que de souscrire un abonnement pour une période donnée.

<b>Si vous avez l'intention de parier régulièrement</b>, un abonnement sera nettement plus rentable que des achats à l'unité.
                '''
            },
            'prognozi': {
                'title': "🔹 Pronostics réguliers / 💠 Pronostics VIP",
                'text': '''
🔷 <b>Pronostics réguliers (analyse succincte) :</b>
    
Un pronostic régulier fournit des informations concises et claires sur un match ou un événement à venir. Il inclut les données essentielles, telles que le résultat prévu du match, les cotes et les facteurs clés qui influencent l'issue. Ce type de pronostic est adapté à ceux qui recherchent rapidement les informations de base avant de placer un pari.
    
🪙 <b>Prix :</b>
    
59 ₽ — 1 pronostic
249 ₽ — 5 pronostics <i>(économie de 15.6%)</i>
450 ₽ — 15 pronostics <i>(économie de 49.2%)</i>
    
💠 <b>Pronostics VIP (analyse détaillée) :</b>
    
Les pronostics VIP offrent une analyse plus approfondie et détaillée d'un événement sportif. En plus des informations de base, ils contiennent des données supplémentaires et une explication plus exhaustive pour une meilleure compréhension du match à venir, ainsi que d'autres aspects importants susceptibles d'influencer le résultat. Ces pronostics vous aideront à mieux cerner la situation et à prendre une décision plus éclairée.
    
🪙 <b>Prix :</b>
    
99 ₽ — 1 pronostic VIP
399 ₽ — 5 pronostics VIP <i>(économie de 19.4%)</i>
1159 ₽ — 15 pronostics VIP <i>(économie de 22.0%)</i>
    '''
            },
            'buy': {
                'title': "💳 Achats",
                'text': '''
💳 Acheter un pronostic
    
Pour acquérir un pronostic régulier ou VIP, utilisez la section "Catalogue" dans le menu principal du bot.
    
<b>Étape 1 :</b> Dans le menu principal du bot, sélectionnez le bouton "Catalogue".
<b>Étape 2 :</b> Dans le "Catalogue", sélectionnez la section "Pronostics".
<b>Étape 3 :</b> Choisissez la quantité désirée de pronostics réguliers ou VIP.
<b>Étape 4 :</b> Suivez les instructions du bot pour finaliser le paiement.
    
—————————-
    
💳 Acheter un abonnement
    
Pour acheter un abonnement qui vous donnera accès à davantage de pronostics et de pronostics VIP à des prix avantageux, suivez ces étapes :
    
<b>Étape 1 :</b> Dans le menu principal du bot, sélectionnez le bouton "Catalogue".
<b>Étape 2 :</b> Dans le "Catalogue", sélectionnez la section "Abonnements".
<b>Étape 3 :</b> Choisissez le type d'abonnement qui vous convient
(Standard, Moyen ou Premium).
<b>Étape 4 :</b> Suivez les instructions du bot pour finaliser le paiement.
                '''
            },
            'createprognoz': {
                'title': "👨‍💻 Création d'un pronostic",
                'text': '''
🤖 <b>Le bot</b> @SportNeyroAnalitikbot vous permet de générer des pronostics sur demande. Pour créer un pronostic, vous devez :
    
<b>Étape 1 :</b> Dans le menu principal du bot, sélectionnez le bouton "Créer un pronostic".
<b>Étape 2 :</b> Après traitement de la demande et analyse du match, le bot vous fournira un pronostic.
    
‼️ <b>IMPORTANT</b>
Remplissez les informations du match avec exactitude et minutie, car toute erreur ne donnera lieu à aucun remboursement.
                '''
            },
            'promokodi': {
                'title': "🎟 Codes promotionnels",
                'text': '''
<b>Les codes promotionnels dans le bot @SportNeyroAnalitikbot vous offrent des bonus supplémentaires.</b>
    
<b>Étape 1 :</b> Dans le menu principal du bot, sélectionnez le bouton "Code promotionnel".
<b>Étape 2 :</b> Entrez votre code promotionnel dans le champ prévu à cet effet.
<b>Étape 3 :</b> Cliquez sur "Appliquer" pour activer le code promotionnel et recevoir vos bonus.
    
🔭 Suivez les actualités du canal <a href="https://t.me/NeyroTeamTg">Neyro Team</a> pour ne pas manquer les nouveaux codes promotionnels.
                '''
            },
            'bukmekeri': {
                'title': "✅ Meilleurs bookmakers",
                'text': '''
👍 <b>Pour placer des paris sportifs basés sur les pronostics reçus du bot, nous recommandons d'utiliser les bookmakers partenaires vérifiés suivants :</b>
    
<b>1Win :</b> <i>https://1wzyuh.com/v3/landing-page/football?p=5ibz</i>
En vous inscrivant avec le code promo "NEYRO99", vous recevrez des bonus.
<b>Winline :</b> <i>https://partners2.winline.ru/s/Ebp0XjlFwM?statid=2925_</i>
En vous inscrivant avec le code promo "NEYRO3000", vous recevrez des bonus.
                '''
            },
            'ozivi': {
                'title': "🗣 Avis",
                'text': '''
♥️ <b>Votre opinion nous est très précieuse !</b> Vous pouvez laisser des avis sur le fonctionnement du bot et consulter ceux des autres utilisateurs.
    
✍️ <b>Laisser un avis :</b> Pour partager votre opinion, rendez-vous sur le bot @OtziviSportbot ou sélectionnez le bouton "Laisser un avis" dans la section "Avis" du menu de @SportNeyroAnalitikbot. Suivez les instructions du bot pour rédiger votre avis.
    
🗣 <b>Lire les avis :</b> Pour consulter les avis des autres utilisateurs, sélectionnez le bouton "Lire les avis" dans la section "Avis" du menu de @SportNeyroAnalitikbot ou accédez au canal Telegram @OTZIVISPORTANALITIK
                '''
            },
            'iaziki': {
                'title': "🌍 Langues",
                'text': '''
<b>Le bot @SportNeyroAnalitikbot est conçu pour une audience mondiale et prend en charge 6 langues internationales de l'ONU :</b>
    
🇷🇺🇬🇧🇪🇸🇨🇳🇫🇷🇸🇦
    
Russe, anglais, espagnol, chinois, français, arabe
    
Vous pouvez facilement changer la langue de l'interface du bot en sélectionnant l'option appropriée dans le menu principal du bot. Cela vous permet d'utiliser toutes les fonctionnalités du bot de la manière la plus confortable possible, quelle que soit votre région.
                '''
            },
            'refi': {
                'title': "🤝 Programme de parrainage",
                'text': '''
🫂 Chaque utilisateur de @SportNeyroAnalitikbot a l'opportunité de participer à notre programme de parrainage et de recevoir des bonus pour les amis invités.
    
• <b>Votre lien de parrainage :</b> Chaque compte dans le bot possède un lien de parrainage unique. Vous pouvez le trouver dans votre "Profil".
• <b>Comment ça marche :</b> Partagez votre lien de parrainage unique avec vos amis. Lorsque votre ami clique sur votre lien, s'inscrit au bot et effectue son premier achat (tout abonnement ou pronostic), vous et votre ami recevrez un bonus.
• <b>Bonus :</b> Pour chaque parrainage qui effectue un achat, vous et votre ami invité recevrez 1 pronostic VIP.
• <b>Suivi :</b> Le nombre d'amis invités est affiché dans votre "Profil".
    
<b>Plus vous invitez d'amis, plus vous pouvez obtenir de bonus !</b>
                '''
            },
            'partnerstvo': {
                'title': "💼 Partenariat",
                'text': '''
💸 Si vous êtes un annonceur, un trafficker ou intéressé par la publicité mutuelle, vous pouvez contacter notre équipe de support sur Telegram à @SuportNeyroTeam pour discuter des termes de la coopération.
                '''
            }

        },

        # === NOUVEAU BLOC : Support et FAQ ===
        'support_menu_header': "⚙️ <b>Support</b>\n\nSi vous avez des questions, vous pouvez trouver les réponses dans la section FAQ ou contacter notre service d'assistance.",
        'faq_button': "⁉️ Foire aux questions (FAQ)",
        'contact_support_button': "👨‍💻 Contacter le support",
        'faq_menu_header': "❓ <b>Foire aux questions</b> ❓",
        'faq_items': {
            'q1': {
                'question': "⚙️ Comment fonctionne le bot ? ",
                'answer': '''
- Le bot @SportNeyroAnalitikbot, basé sur des réseaux neuronaux spécialement entraînés pour l'analyse de données, offre une analyse détaillée des événements sportifs. Le bot est constamment mis à jour et testé, et tous vos commentaires sont pris en compte !
    
<b>1. Collecte de données :</b>
Le bot rassemble des données provenant de multiples sources, en considérant les paramètres qui influencent le résultat des matchs.
    
<b>2. Prédiction des résultats :</b>
Basé sur son analyse, le bot génère une prédiction des résultats probables des matchs, en intégrant les informations collectées.
    
<b>3. Analyse détaillée :</b>
Les utilisateurs ne reçoivent pas seulement des chiffres, mais aussi des explications sur les facteurs clés.
    
<b>4. Mises à jour en temps réel :</b>
Les algorithmes sont continuellement améliorés pour garantir une grande précision des prévisions.
    
❤️ <i>Notre objectif est de rendre l'analyse sportive accessible à tous. Que vous soyez un passionné, un analyste professionnel ou un acteur du marché des paris.</i>
                '''
            },
            'q2': {
                'question': "🎫 Comment fonctionnent les abonnements ?",
                'answer': '''
🎫 Les abonnements donnent accès à un nombre spécifique de pronostics temporaires (réguliers et VIP) pour une période définie <i>(une semaine, deux semaines)</i>.
    
💎 Ils offrent des <b>tarifs plus avantageux</b> par rapport à l'achat de pronostics individuels.
    
‼️ <b>Il est important de noter</b> qu'en cas de souscription à un nouvel abonnement, l'ancien est annulé, et les pronostics temporaires non utilisés expirent à la fin de la période d'abonnement.
                '''
            },
            'q3': {
                'question': "📊 Comment fonctionnent les pronostics ?",
                'answer': '''
<b>Le bot propose deux types de pronostics :</b>
    
🔹 <b>Pronostics réguliers :</b> Fournissent des informations concises sur le résultat du match, les cotes et les facteurs clés.
    
💠 <b>Pronostics VIP :</b> Offrent une analyse plus approfondie et détaillée, incluant des données supplémentaires et des explications étendues pour des décisions plus éclairées.
    '''
            },
            'q4': {
                'question': "⏳ Quelle est la différence avec les pronostics temporaires ? ",
                'answer': '''
⏳ En souscrivant à un abonnement, vous recevez des <b>pronostics temporaires</b> qui restent valides jusqu'à l'expiration de votre abonnement. Par exemple, si vous prévoyez de parier régulièrement, un abonnement sera bien plus rentable que des achats à l'unité.
                '''
            },
            'q5': {
                'question': "💳 Comment acheter un abonnement ?",
                'answer': '''
💳 Pour acheter un abonnement, allez dans "Catalogue" depuis le menu principal du bot, puis sélectionnez "Abonnements" et le plan désiré. Suivez les instructions du bot pour le paiement.
                '''
            },
            'q6': {
                'question': "💳 Comment acheter des pronostics ?",
                'answer': '''
💳 Pour acheter des pronostics, allez dans "Catalogue" depuis le menu principal du bot, puis sélectionnez "Pronostics" et la quantité nécessaire de pronostics réguliers ou VIP. Suivez les instructions du bot pour le paiement.
    '''
            },
            'q7': {
                'question': "📊 Comment créer un pronostic ?",
                'answer': '''
📊 Pour créer un pronostic sur demande, sélectionnez le bouton "Créer un pronostic" dans le menu principal du bot. Ensuite, entrez les informations nécessaires concernant l'événement sportif, en suivant les invites du bot.
    '''
            },
            'q8': {
                'question': "🎟 Comment fonctionnent les codes promotionnels ? ",
                'answer': '''
🎟 Les codes promotionnels sont saisis dans une section spéciale "Code promotionnel" du menu principal du bot. Ils activent des bonus pouvant être fournis par l'équipe Neyro Team. Il existe également des codes promotionnels pour recevoir des bonus lors de l'inscription auprès des partenaires bookmakers.
    '''
            },
            'q9': {
                'question': "✍️ Comment laisser un avis ?",
                'answer': '''
✍️ Vous pouvez laisser un avis en vous rendant sur le bot @OtziviSportbot ou en sélectionnant le bouton "Laisser un avis" dans la section "Avis" du menu de @SportNeyroAnalitikbot.
                '''
            },
            'q10': {
                'question': "👀 Où lire les avis ?",
                'answer': '''
👀 Vous pouvez lire les avis des autres utilisateurs en sélectionnant le bouton "Lire les avis" dans la section "Avis" du menu de @SportNeyroAnalitikbot.
    '''
            },
            'q11': {
                'question': "✅ Où parier sur le sport ?",
                'answer': '''
✔️ Pour placer des paris sportifs basés sur les pronostics reçus du bot, nous vous recommandons d'utiliser les partenaires de bookmakers vérifiés suivants :
    
<b>1Win :</b> <i>https://1wzyuh.com/v3/landing-page/football?p=5ibz</i>
(Code promo : NEYRO99)
<b>Winline :</b> <i>https://partners2.winline.ru/s/Ebp0XjlFwM?statid=2925_</i>
(Code promo : NEYRO3000)
                '''
            },
            'q12': {
                'question': "🌍 Quelles langues sont disponibles pour le bot ?",
                'answer': '''
Le bot @SportNeyroAnalitikbot prend en charge 6 langues internationales 🌍 de l'ONU : le russe, l'anglais, l'arabe, l'espagnol, le chinois et le français. Vous pouvez sélectionner la langue souhaitée dans les paramètres du bot.
                '''
            },
            'q13': {
                'question': "🤝 Comment fonctionne le programme de parrainage ?",
                'answer': '''
🫂 Chaque utilisateur de @SportNeyroAnalitikbot a la possibilité de participer à notre programme de parrainage et de recevoir des bonus pour les amis invités.
    
• <b>Votre lien de parrainage :</b> Chaque compte dans le bot possède un lien de parrainage unique. Vous pouvez le trouver dans votre "Profil".
• <b>Comment ça marche :</b> Partagez votre lien de parrainage unique avec vos amis. Lorsque votre ami clique sur votre lien, s'inscrit au bot et effectue son premier achat (tout abonnement ou pronostic), vous et votre ami recevrez un bonus.
• <b>Bonus :</b> Pour chaque parrainage qui effectue un achat, vous et votre ami invité recevrez 1 pronostic VIP.
• <b>Suivi :</b> Le nombre d'amis invités est affiché dans votre "Profil".
    
<b>Plus vous invitez d'amis, plus vous pouvez obtenir de bonus !</b>
                '''
            },
            'q14': {
                'question': '''💼 Comment devenir partenaire de "Neyro Team" ?''',
                'answer': '''
💸 Si vous êtes un <b>annonceur, un trafficker ou intéressé par la publicité mutuelle</b>, vous pouvez contacter notre équipe de support sur Telegram à @SuportNeyroTeam pour discuter des termes de la coopération.
    '''
            }
        },

        # === NOUVEAU BLOC : Chemins des images ===
        'photo_profil': "images/fr/profil.png",
        'photo_katalog': "images/fr/katalog.png",
        'photo_katalog_prognoz': "images/fr/katalog_prognoz.png",
        'photo_katalog_subscriptions': "images/fr/katalog_subscriptions.png",
        'photo_otzivi': "images/fr/otzivi.png",
        'photo_tip_prognoza': "images/fr/tip_prognoza.png",
        'ob_prognoz_photo': "images/fr/ob_prognoz.png",
        'vip_prognoz_photo': "images/fr/vip_prognoz.png",
        'photo_instruction': "images/fr/instruction.png",
        'photo_support': "images/fr/support.png",
        'photo_faq': "images/fr/faq.png",
        'photo_cponsori': "images/fr/cponsori.png"
    }
}


#===========================
# Перевод GPT запросов
#============================

# ==============================================================================
#  БЛОК ПРОМПТОВ ДЛЯ GPT-4. ЗАМЕНИТЬ СТАРЫЕ system_message_* СЛОВАРИ
# ==============================================================================

# PROMPT_BLOCKS = {
#     "ru": {
#         "ROLE_REGULAR": "Вы — профессиональный спортивный аналитик. Ваша задача — предоставлять структурированные, объективные и аргументированные прогнозы в HTML-формате. Используйте эмоджи для акцентов, но не меняйте структуру.",
#         "ROLE_VIP": "Вы — старший спортивный стратег и аналитик с 15-летним опытом. Вы готовите углубленные прогнозы для премиум-клиентов. Думай шаг за шагом, чтобы определить ключевые факторы, риски и сценарии. Ответ должен быть в HTML-формате.",
#         "FORMATTING_RULES": """
#         ФОРМАТИРОВАНИЕ: Используйте только HTML для Telegram. Строго соблюдайте синтаксис.
#         - Полужирный: <b>текст</b>
#         - Курсив: <i>текст</i>
#         - Цитата: <blockquote>текст</blockquote> (используется только для VIP-прогнозов в разделе 'Подробнее')
#         - Не включайте никаких вводных фраз типа "Вот ваш прогноз:".
#         - Вывод должен быть только отформатированным текстом, готовым для отправки в Telegram.
#         - Весь вывод должен быть обернут в ➖➖➖➖➖➖➖➖➖➖ в начале и в конце.
#         """,
#         "TASK_REGULAR": "Сгенерируй краткий, но информативный прогноз на матч, определив наиболее важные ключевые факторы и риски.",
#         "TASK_VIP": "Сгенерируй всесторонний VIP-прогноз, включая предполагаемый счёт, оценку доверия, анализ сценариев и детальный раздел 'Подробнее' в виде цитаты.",
#         "EXAMPLE_REGULAR": """➖➖➖➖➖➖➖➖➖➖
#
# 🔹 <b>Прогноз на матч:</b>
# <i>01.05.2025 19:00</i>
# <i>Футбол</i>
# <i>Барселона vs Реал Мадрид</i>
#
# ⚜️ <b>Статистика победы:</b>
# • Барселона — 45%
# • Реал Мадрид — 40%
# • Ничья — 15%
#
# 🔍 <b>Ключевые факторы:</b>
# • <b>Текущая форма:</b> Барселона показывает уверенную атакующую игру в последних 5 матчах.
# • <b>Травмы:</b> Ключевой защитник Реала пропустит матч, что ослабит их оборону.
# • <b>Домашнее преимущество:</b> Камп Ноу создаст сильное давление на гостей.
#
# ⚠️ <b>Риски:</b>
# • <b>Погодные условия:</b> Прогнозируется дождь, что может замедлить игру и привести к ошибкам.
# • <b>Напряжение "Эль-Класико":</b> Высокое давление дерби может привести к непредсказуемым удалениям.
#
# ➖➖➖➖➖➖➖➖➖➖""",
#         "EXAMPLE_VIP": """➖➖➖➖➖➖➖➖➖➖
#
# 💠 <b>VIP Прогноз на матч:</b>
# <i>02.05.2025 21:00</i>
# <i>Баскетбол</i>
# <i>Лейкерс vs Буллз</i>
#
# ⚜️ <b>Статистика победы:</b>
# • Лейкерс — 55%
# • Буллз — 45%
#
# 🧮 <b>Предполагаемый счёт:</b>
# 102:98 (с вероятностью ~60%)
#
# ⭐ <b>Оценка доверия:</b>
# Высокая (85%). Прогноз основан на текущей форме лидеров и статистике домашних игр.
#
# ⚙️ <b>Анализ сценариев:</b>
# • <b>Оптимистичный:</b> Лейкерс доминируют с самого начала и выигрывают с разницей 10+ очков.
# • <b>Базовый:</b> Равная игра, исход решается в последних минутах, Лейкерс побеждают с небольшим отрывом.
# • <b>Пессимистичный:</b> Лидер Буллз показывает выдающуюся игру, Лейкерс проигрывают в овертайме.
#
# 🔍 <b>Ключевые факторы:</b>
# • <b>Защита Лейкерс:</b> Команда значительно улучшила игру в обороне, что видно по последним матчам.
# • <b>Усталость Буллз:</b> Это третья выездная игра для Буллз за последние пять дней.
# • <b>Домашний фактор:</b> Лейкерс традиционно сильны на своей площадке.
#
# ⚠️ <b>Риски:</b>
# • <b>Процент трехочковых:</b> Если у Буллз пойдет дальний бросок, это может изменить ход игры.
# • <b>Фолы:</b> Лидеры Лейкерс склонны к ранним фолам, что может ограничить их игровое время.
#
# <blockquote>📝 <b>Подробнее:</b>
# Ключевым фактором станет противостояние под кольцом. Лейкерс должны использовать свое преимущество в росте и забирать подборы. Буллз будут полагаться на быстрые прорывы и дальние броски. Учитывая усталость Буллз, ставка на победу Лейкерс с форой -3.5 выглядит оправданной.</blockquote>
#
# ➖➖➖➖➖➖➖➖➖➖"""
#     },
#     "en": {
#         "ROLE_REGULAR": "You are a professional sports analyst. Your task is to provide structured, objective, and well-reasoned forecasts in HTML format. Use emojis for emphasis, but do not change the structure.",
#         "ROLE_VIP": "You are a senior sports strategist and analyst with 15 years of experience. You prepare in-depth forecasts for premium clients. Think step-by-step to identify key factors, risks, and scenarios. The response must be in HTML format.",
#         "FORMATTING_RULES": """
#         FORMATTING: Use only HTML for Telegram. Strictly follow the syntax.
#         - Bold: <b>text</b>
#         - Italic: <i>text</i>
#         - Blockquote: <blockquote>text</blockquote> (used only for VIP forecasts in the 'Details' section)
#         - Do not include any introductory phrases like "Here is your forecast:".
#         - The output must be only formatted text, ready to be sent to Telegram.
#         - The entire output must be wrapped in ➖➖➖➖➖➖➖➖➖➖ at the beginning and end.
#         """,
#         "TASK_REGULAR": "Generate a concise but informative match forecast, identifying the most critical key factors and risks.",
#         "TASK_VIP": "Generate a comprehensive VIP forecast, including a predicted score, confidence rating, scenario analysis, and a detailed 'Details' section as a blockquote.",
#         "EXAMPLE_REGULAR": """➖➖➖➖➖➖➖➖➖➖
#
# 🔹 <b>Match Forecast:</b>
# <i>01.05.2025 19:00</i>
# <i>Football</i>
# <i>Barcelona vs Real Madrid</i>
#
# ⚜️ <b>Win Statistics:</b>
# • Barcelona — 45%
# • Real Madrid — 40%
# • Draw — 15%
#
# 🔍 <b>Key Factors:</b>
# • <b>Current Form:</b> Barcelona has shown confident attacking play in the last 5 matches.
# • <b>Injuries:</b> Real Madrid's key defender will miss the match, weakening their defense.
# • <b>Home Advantage:</b> Camp Nou will create strong pressure on the visitors.
#
# ⚠️ <b>Risks:</b>
# • <b>Weather Conditions:</b> Rain is forecasted, which could slow down the game and lead to errors.
# • <b>"El Clásico" Tension:</b> The high pressure of the derby could lead to unpredictable red cards.
#
# ➖➖➖➖➖➖➖➖➖➖""",
#         "EXAMPLE_VIP": """➖➖➖➖➖➖➖➖➖➖
#
# 💠 <b>VIP Match Forecast:</b>
# <i>02.05.2025 21:00</i>
# <i>Basketball</i>
# <i>Lakers vs Bulls</i>
#
# ⚜️ <b>Win Statistics:</b>
# • Lakers — 55%
# • Bulls — 45%
#
# 🧮 <b>Predicted Score:</b>
# 102:98 (with ~60% probability)
#
# ⭐ <b>Confidence Rating:</b>
# High (85%). The forecast is based on the current form of the leaders and home game statistics.
#
# ⚙️ <b>Scenario Analysis:</b>
# • <b>Optimistic:</b> Lakers dominate from the start and win by 10+ points.
# • <b>Baseline:</b> A close game, the outcome is decided in the final minutes, Lakers win by a small margin.
# • <b>Pessimistic:</b> The Bulls' star player has an outstanding game, Lakers lose in overtime.
#
# 🔍 <b>Key Factors:</b>
# • <b>Lakers' Defense:</b> The team has significantly improved its defensive play, as seen in recent matches.
# • <b>Bulls' Fatigue:</b> This is the third away game for the Bulls in the last five days.
# • <b>Home Factor:</b> The Lakers are traditionally strong on their home court.
#
# ⚠️ <b>Risks:</b>
# • <b>Three-Point Percentage:</b> If the Bulls start hitting their long-range shots, it could change the game's course.
# • <b>Fouls:</b> Lakers' leaders are prone to early fouls, which could limit their playing time.
#
# <blockquote>📝 <b>Details:</b>
# The key factor will be the battle under the basket. The Lakers must use their height advantage to grab rebounds. The Bulls will rely on fast breaks and long-range shots. Given the Bulls' fatigue, a bet on the Lakers to win with a -3.5 spread looks justified.</blockquote>
#
# ➖➖➖➖➖➖➖➖➖➖"""
#     },
#     "ar": {
#         "ROLE_REGULAR": "أنت محلل رياضي محترف. مهمتك هي تقديم توقعات منظمة وموضوعية ومدعومة بالحجج بتنسيق HTML. استخدم الرموز التعبيرية للتأكيد، ولكن لا تغير الهيكل.",
#         "ROLE_VIP": "أنت استراتيجي ومحلل رياضي أول بخبرة 15 عامًا. تقوم بإعداد توقعات متعمقة للعملاء المميزين. فكر خطوة بخطوة لتحديد العوامل الرئيسية والمخاطر والسيناريوهات. يجب أن تكون الإجابة بتنسيق HTML.",
#         "FORMATTING_RULES": """
#         التنسيق: استخدم HTML فقط لتليجرام. اتبع الصيغة بدقة.
#         - غامق: <b>نص</b>
#         - مائل: <i>نص</i>
#         - اقتباس: <blockquote>نص</blockquote> (يستخدم فقط لتوقعات VIP في قسم 'التفاصيل')
#         - لا تقم بتضمين أي عبارات تمهيدية مثل "إليك توقعاتك:".
#         - يجب أن يكون الإخراج نصًا منسقًا فقط، جاهزًا للإرسال إلى تليجرام.
#         - يجب أن يكون الإخراج بأكمله محاطًا بـ ➖➖➖➖➖➖➖➖➖➖ في البداية والنهاية.
#         """,
#         "TASK_REGULAR": "أنشئ توقعًا موجزًا وغنيًا بالمعلومات للمباراة، مع تحديد أهم العوامل الرئيسية والمخاطر.",
#         "TASK_VIP": "أنشئ توقع VIP شامل، بما في ذلك النتيجة المتوقعة، وتقييم الثقة، وتحليل السيناريوهات، وقسم 'التفاصيل' مفصل كاقتباس.",
#         "EXAMPLE_REGULAR": """➖➖➖➖➖➖➖➖➖➖
#
# 🔹 <b>توقع المباراة:</b>
# <i>01.05.2025 19:00</i>
# <i>كرة القدم</i>
# <i>برشلونة ضد ريال مدريد</i>
#
# ⚜️ <b>إحصائيات الفوز:</b>
# • برشلونة — 45%
# • ريال مدريد — 40%
# • تعادل — 15%
#
# 🔍 <b>العوامل الرئيسية:</b>
# • <b>الشكل الحالي:</b> أظهر برشلونة لعبًا هجوميًا واثقًا في آخر 5 مباريات.
# • <b>الإصابات:</b> سيغيب مدافع ريال مدريد الرئيسي عن المباراة، مما يضعف دفاعهم.
# • <b>ميزة الأرض:</b> سيخلق ملعب كامب نو ضغطًا قويًا على الضيوف.
#
# ⚠️ <b>المخاطر:</b>
# • <b>الأحوال الجوية:</b> من المتوقع هطول أمطار، مما قد يبطئ اللعبة ويؤدي إلى أخطاء.
# • <b>توتر "الكلاسيكو":</b> يمكن أن يؤدي الضغط العالي للديربي إلى بطاقات حمراء غير متوقعة.
#
# ➖➖➖➖➖➖➖➖➖➖""",
#         "EXAMPLE_VIP": """➖➖➖➖➖➖➖➖➖➖
#
# 💠 <b>توقع VIP للمباراة:</b>
# <i>02.05.2025 21:00</i>
# <i>كرة السلة</i>
# <i>ليكرز ضد بولز</i>
#
# ⚜️ <b>إحصائيات الفوز:</b>
# • ليكرز — 55%
# • بولز — 45%
#
# 🧮 <b>النتيجة المتوقعة:</b>
# 102:98 (باحتمال ~60%)
#
# ⭐ <b>تقييم الثقة:</b>
# مرتفع (85%). يعتمد التوقع على الشكل الحالي للنجوم وإحصائيات المباريات على أرضهم.
#
# ⚙️ <b>تحليل السيناريوهات:</b>
# • <b>المتفائل:</b> يسيطر ليكرز منذ البداية ويفوز بفارق 10 نقاط أو أكثر.
# • <b>الأساسي:</b> مباراة متكافئة، يتم حسم النتيجة في الدقائق الأخيرة، ويفوز ليكرز بفارق ضئيل.
# • <b>المتشائم:</b> يقدم نجم بولز أداءً استثنائيًا، ويخسر ليكرز في الوقت الإضافي.
#
# 🔍 <b>العوامل الرئيسية:</b>
# • <b>دفاع ليكرز:</b> قام الفريق بتحسين لعبه الدفاعي بشكل كبير، كما يتضح من المباريات الأخيرة.
# • <b>إرهاق بولز:</b> هذه هي المباراة الثالثة خارج الديار لبولز في الأيام الخمسة الماضية.
# • <b>عامل الأرض:</b> ليكرز أقوياء تقليديًا على ملعبهم.
#
# ⚠️ <b>المخاطر:</b>
# • <b>نسبة الرميات الثلاثية:</b> إذا بدأ بولز في تسجيل رمياتهم البعيدة، فقد يغير ذلك مسار المباراة.
# • <b>الأخطاء الشخصية:</b> يميل نجوم ليكرز إلى ارتكاب أخطاء مبكرة، مما قد يحد من وقت لعبهم.
#
# <blockquote>📝 <b>التفاصيل:</b>
# سيكون العامل الرئيسي هو الصراع تحت السلة. يجب على ليكرز استخدام ميزة الطول لديهم للحصول على الكرات المرتدة. سيعتمد بولز على الاختراقات السريعة والرميات البعيدة. بالنظر إلى إرهاق بولز، يبدو الرهان على فوز ليكرز بفارق -3.5 مبررًا.</blockquote>
#
# ➖➖➖➖➖➖➖➖➖➖"""
#     },
#     "es": {
#         "ROLE_REGULAR": "Eres un analista deportivo profesional. Tu tarea es proporcionar pronósticos estructurados, objetivos y argumentados en formato HTML. Usa emojis para dar énfasis, pero no cambies la estructura.",
#         "ROLE_VIP": "Eres un estratega y analista deportivo senior con 15 años de experiencia. Preparas pronósticos detallados para clientes premium. Piensa paso a paso para identificar los factores clave, riesgos y escenarios. La respuesta debe estar en formato HTML.",
#         "FORMATTING_RULES": """
#         FORMATO: Usa solo HTML para Telegram. Sigue estrictamente la sintaxis.
#         - Negrita: <b>texto</b>
#         - Cursiva: <i>texto</i>
#         - Cita: <blockquote>texto</blockquote> (usado solo para pronósticos VIP en la sección 'Detalles')
#         - No incluyas frases introductorias como "Aquí está tu pronóstico:".
#         - La salida debe ser solo texto formateado, listo para ser enviado a Telegram.
#         - Toda la salida debe estar envuelta en ➖➖➖➖➖➖➖➖➖➖ al principio и al final.
#         """,
#         "TASK_REGULAR": "Genera un pronóstico de partido conciso pero informativo, identificando los factores clave y riesgos más importantes.",
#         "TASK_VIP": "Genera un pronóstico VIP completo, incluyendo un marcador predicho, calificación de confianza, análisis de escenarios y una sección detallada de 'Detalles' como una cita.",
#         "EXAMPLE_REGULAR": """➖➖➖➖➖➖➖➖➖➖
#
# 🔹 <b>Pronóstico del partido:</b>
# <i>01.05.2025 19:00</i>
# <i>Fútbol</i>
# <i>Barcelona vs Real Madrid</i>
#
# ⚜️ <b>Estadísticas de victoria:</b>
# • Barcelona — 45%
# • Real Madrid — 40%
# • Empate — 15%
#
# 🔍 <b>Factores clave:</b>
# • <b>Forma actual:</b> El Barcelona ha mostrado un juego de ataque seguro en los últimos 5 partidos.
# • <b>Lesiones:</b> El defensa clave del Real Madrid se perderá el partido, lo que debilitará su defensa.
# • <b>Ventaja de local:</b> El Camp Nou creará una fuerte presión sobre los visitantes.
#
# ⚠️ <b>Riesgos:</b>
# • <b>Condiciones climáticas:</b> Se pronostica lluvia, lo que podría ralentizar el juego y provocar errores.
# • <b>Tensión de "El Clásico":</b> La alta presión del derbi podría llevar a expulsiones impredecibles.
#
# ➖➖➖➖➖➖➖➖➖➖""",
#         "EXAMPLE_VIP": """➖➖➖➖➖➖➖➖➖➖
#
# 💠 <b>Pronóstico VIP del partido:</b>
# <i>02.05.2025 21:00</i>
# <i>Baloncesto</i>
# <i>Lakers vs Bulls</i>
#
# ⚜️ <b>Estadísticas de victoria:</b>
# • Lakers — 55%
# • Bulls — 45%
#
# 🧮 <b>Marcador previsto:</b>
# 102:98 (con ~60% de probabilidad)
#
# ⭐ <b>Calificación de confianza:</b>
# Alta (85%). El pronóstico se basa en la forma actual de los líderes y las estadísticas de los partidos en casa.
#
# ⚙️ <b>Análisis de escenarios:</b>
# • <b>Optimista:</b> Los Lakers dominan desde el principio y ganan por más de 10 puntos.
# • <b>Básico:</b> Un partido igualado, el resultado se decide en los minutos finales, los Lakers ganan por un pequeño margen.
# • <b>Pesimista:</b> El jugador estrella de los Bulls tiene una actuación sobresaliente, los Lakers pierden en la prórroga.
#
# 🔍 <b>Factores clave:</b>
# • <b>Defensa de los Lakers:</b> El equipo ha mejorado significativamente su juego defensivo, como se ha visto en los últimos partidos.
# • <b>Fatiga de los Bulls:</b> Este es el tercer partido fuera de casa para los Bulls en los últimos cinco días.
# • <b>Factor local:</b> Los Lakers son tradicionalmente fuertes en su cancha.
#
# ⚠️ <b>Riesgos:</b>
# • <b>Porcentaje de triples:</b> Si los Bulls comienzan a acertar sus tiros lejanos, podría cambiar el curso del partido.
# • <b>Faltas:</b> Los líderes de los Lakers son propensos a cometer faltas tempranas, lo que podría limitar su tiempo de juego.
#
# <blockquote>📝 <b>Detalles:</b>
# El factor clave será la batalla bajo el aro. Los Lakers deben usar su ventaja de altura para capturar rebotes. Los Bulls dependerán de contraataques rápidos y tiros lejanos. Dada la fatiga de los Bulls, una apuesta a que los Lakers ganan con un hándicap de -3.5 parece justificada.</blockquote>
#
# ➖➖➖➖➖➖➖➖➖➖"""
#     },
#     "zh": {
#         "ROLE_REGULAR": "您是一名专业的体育分析师。您的任务是以HTML格式提供结构化、客观且论证充分的预测。使用表情符号进行强调，但不要改变结构。",
#         "ROLE_VIP": "您是一名拥有15年经验的高级体育策略师和分析师。您为高级客户准备深入的预测。请逐步思考，以确定关键因素、风险和情景。回复必须是HTML格式。",
#         "FORMATTING_RULES": """
#         格式化：仅使用HTML格式用于Telegram。严格遵守语法。
#         - 粗体: <b>文本</b>
#         - 斜体: <i>文本</i>
#         - 引用: <blockquote>文本</blockquote> (仅用于VIP预测的'详情'部分)
#         - 不要包含任何介绍性短语，如“这是您的预测:”。
#         - 输出必须是格式化的文本，准备好发送到Telegram。
#         - 所有输出的开头和结尾都必须用 ➖➖➖➖➖➖➖➖➖➖ 包裹。
#         """,
#         "TASK_REGULAR": "生成一个简洁但信息丰富的比赛预测，确定最关键的因素和风险。",
#         "TASK_VIP": "生成一个全面的VIP预测，包括预测得分、置信度评级、情景分析和作为引用的详细'详情'部分。",
#         "EXAMPLE_REGULAR": """➖➖➖➖➖➖➖➖➖➖
#
# 🔹 <b>比赛预测:</b>
# <i>01.05.2025 19:00</i>
# <i>足球</i>
# <i>巴塞罗那 vs 皇家马德里</i>
#
# ⚜️ <b>获胜统计:</b>
# • 巴塞罗那 — 45%
# • 皇家马德里 — 40%
# • 平局 — 15%
#
# 🔍 <b>关键因素:</b>
# • <b>当前状态:</b> 巴塞罗那在过去5场比赛中表现出自信的进攻。
# • <b>伤病:</b> 皇家马德里的关键后卫将缺席比赛，这将削弱他们的防守。
# • <b>主场优势:</b> 诺坎普球场将给客队带来巨大压力。
#
# ⚠️ <b>风险:</b>
# • <b>天气状况:</b> 预计有雨，这可能会减慢比赛节奏并导致失误。
# • <b>“国家德比”的紧张气氛:</b> 德比的高压可能导致不可预测的红牌。
#
# ➖➖➖➖➖➖➖➖➖➖""",
#         "EXAMPLE_VIP": """➖➖➖➖➖➖➖➖➖➖
#
# 💠 <b>VIP比赛预测:</b>
# <i>02.05.2025 21:00</i>
# <i>篮球</i>
# <i>湖人队 vs 公牛队</i>
#
# ⚜️ <b>获胜统计:</b>
# • 湖人队 — 55%
# • 公牛队 — 45%
#
# 🧮 <b>预测得分:</b>
# 102:98 (概率约60%)
#
# ⭐ <b>置信度评级:</b>
# 高 (85%). 预测基于核心球员当前的状态和主场比赛统计数据。
#
# ⚙️ <b>情景分析:</b>
# • <b>乐观情景:</b> 湖人队从一开始就占据主导，并以10分以上的优势获胜。
# • <b>基本情景:</b> 比赛势均力敌，结果在最后几分钟决定，湖人队以微弱优势获胜。
# • <b>悲观情景:</b> 公牛队的明星球员表现出色，湖人队在加时赛中失利。
#
# 🔍 <b>关键因素:</b>
# • <b>湖人队的防守:</b> 正如最近的比赛所示，该队的防守表现有了显着改善。
# • <b>公牛队的疲劳:</b> 这是公牛队在过去五天内的第三场客场比赛。
# • <b>主场因素:</b> 湖人队在主场传统上很强大。
#
# ⚠️ <b>风险:</b>
# • <b>三分球命中率:</b> 如果公牛队开始投中远距离投篮，可能会改变比赛的进程。
# • <b>犯规:</b> 湖人队的核心球员容易过早犯规，这可能会限制他们的上场时间。
#
# <blockquote>📝 <b>详情:</b>
# 关键因素将是篮下的对抗。湖人队必须利用他们的身高优势抢下篮板。公牛队将依靠快攻和远距离投篮。考虑到公牛队的疲劳，押注湖人队赢并让-3.5分似乎是合理的。</blockquote>
#
# ➖➖➖➖➖➖➖➖➖➖"""
#     },
#     "fr": {
#         "ROLE_REGULAR": "Vous êtes un analyste sportif professionnel. Votre tâche est de fournir des pronostics structurés, objectifs et argumentés au format HTML. Utilisez des emojis pour mettre l'accent, mais ne changez pas la structure.",
#         "ROLE_VIP": "Vous êtes un stratège et analyste sportif senior avec 15 ans d'expérience. Vous préparez des pronostics approfondis pour les clients premium. Pensez étape par étape pour identifier les facteurs clés, les risques et les scénarios. La réponse doit être au format HTML.",
#         "FORMATTING_RULES": """
#         FORMATAGE : Utilisez uniquement HTML pour Telegram. Respectez strictement la syntaxe.
#         - Gras : <b>texte</b>
#         - Italique : <i>texte</i>
#         - Citation : <blockquote>texte</blockquote> (utilisé uniquement pour les pronostics VIP dans la section 'Détails')
#         - N'incluez aucune phrase d'introduction comme "Voici votre pronostic :".
#         - La sortie doit être uniquement du texte formaté, prêt à être envoyé sur Telegram.
#         - L'ensemble de la sortie doit être encadré par ➖➖➖➖➖➖➖➖➖➖ au début et à la fin.
#         """,
#         "TASK_REGULAR": "Générez un pronostic de match concis mais informatif, en identifiant les facteurs clés et les risques les plus importants.",
#         "TASK_VIP": "Générez un pronostic VIP complet, incluant un score prédit, un indice de confiance, une analyse de scénarios et une section 'Détails' détaillée sous forme de citation.",
#         "EXAMPLE_REGULAR": """➖➖➖➖➖➖➖➖➖➖
#
# 🔹 <b>Pronostic du match :</b>
# <i>01.05.2025 19:00</i>
# <i>Football</i>
# <i>Barcelone vs Real Madrid</i>
#
# ⚜️ <b>Statistiques de victoire :</b>
# • Barcelone — 45%
# • Real Madrid — 40%
# • Match nul — 15%
#
# 🔍 <b>Facteurs clés :</b>
# • <b>Forme actuelle :</b> Barcelone a montré un jeu offensif confiant lors des 5 derniers matchs.
# • <b>Blessures :</b> Le défenseur clé du Real Madrid manquera le match, ce qui affaiblira leur défense.
# • <b>Avantage à domicile :</b> Le Camp Nou créera une forte pression sur les visiteurs.
#
# ⚠️ <b>Risques :</b>
# • <b>Conditions météorologiques :</b> De la pluie est prévue, ce qui pourrait ralentir le jeu et entraîner des erreurs.
# • <b>Tension du "Clásico" :</b> La haute pression du derby pourrait entraîner des cartons rouges imprévisibles.
#
# ➖➖➖➖➖➖➖➖➖➖""",
#         "EXAMPLE_VIP": """➖➖➖➖➖➖➖➖➖➖
#
# 💠 <b>Pronostic VIP du match :</b>
# <i>02.05.2025 21:00</i>
# <i>Basketball</i>
# <i>Lakers vs Bulls</i>
#
# ⚜️ <b>Statistiques de victoire :</b>
# • Lakers — 55%
# • Bulls — 45%
#
# 🧮 <b>Score prévu :</b>
# 102:98 (avec une probabilité d'environ 60%)
#
# ⭐ <b>Indice de confiance :</b>
# Élevé (85%). Le pronostic est basé sur la forme actuelle des leaders et les statistiques des matchs à domicile.
#
# ⚙️ <b>Analyse des scénarios :</b>
# • <b>Optimiste :</b> Les Lakers dominent dès le début и gagnent de 10 points ou plus.
# • <b>De base :</b> Un match serré, le résultat se décide dans les dernières minutes, les Lakers gagnent par une petite marge.
# • <b>Pessimiste :</b> Le joueur vedette des Bulls réalise une performance exceptionnelle, les Lakers perdent en prolongation.
#
# 🔍 <b>Facteurs clés :</b>
# • <b>Défense des Lakers :</b> L'équipe a considérablement amélioré son jeu défensif, comme on l'a vu lors des derniers matchs.
# • <b>Fatigue des Bulls :</b> C'est le troisième match à l'extérieur pour les Bulls au cours des cinq derniers jours.
# • <b>Facteur domicile :</b> Les Lakers sont traditionnellement forts sur leur terrain.
#
# ⚠️ <b>Risques :</b>
# • <b>Pourcentage de tirs à trois points :</b> Si les Bulls commencent à réussir leurs tirs lointains, cela pourrait changer le cours du match.
# • <b>Fautes :</b> Les leaders des Lakers sont sujets à des fautes précoces, ce qui pourrait limiter leur temps de jeu.
#
# <blockquote>📝 <b>Détails :</b>
# Le facteur clé sera la bataille sous le panier. Les Lakers doivent utiliser leur avantage de taille pour prendre les rebonds. Les Bulls s'appuieront sur des contre-attaques rapides et des tirs lointains. Compte tenu de la fatigue des Bulls, un pari sur une victoire des Lakers avec un handicap de -3.5 semble justifié.</blockquote>
#
# ➖➖➖➖➖➖➖➖➖➖"""
#     }
# }

# ==============================================================================
#  УНИВЕРСАЛЬНЫЙ АНГЛОЯЗЫЧНЫЙ ПРОМПТ C КОНТРОЛЕМ ДЛИНЫ (ВЕРСИЯ 3)
# ==============================================================================

PROMPT_KIT_EN = {
    "ROLE_REGULAR": "You are a professional sports analyst. Your task is to provide structured, objective, and concise forecasts in HTML format.",
    "ROLE_VIP": "You are a senior sports strategist. You prepare in-depth but optimized forecasts for premium clients. You must think step-by-step to create a detailed analysis while strictly respecting character limits.",

    "OUTPUT_INSTRUCTIONS": """
    CRITICAL: You MUST follow these rules precisely.
    1.  LANGUAGE: Provide the final answer in the following language: {language_name}.
    2.  FORMATTING: Use ONLY HTML for Telegram (<b>, <i>, <blockquote>).
    3.  NO INTROS: Do not add any extra text like "Here is your forecast".
    4.  WRAPPING: The entire output must be wrapped in ➖➖➖➖➖➖➖➖➖➖ at the start and end.
    """,

    "TASK_REGULAR": """
    Generate a concise match forecast.
    - Analyze the most critical key factors and risks.
    - Use the user-provided language for all text.
    - STRICT LIMIT: The entire response, including all formatting and emojis, MUST NOT exceed 2000 characters.
    """,

    "TASK_VIP": """
    Generate a comprehensive VIP forecast.
    - Include predicted score, confidence rating, scenario analysis, and a detailed 'Details' section.
    - Be detailed but respect the length limit. Prioritize the most valuable insights.
    - Use the user-provided language for all text.
    - STRICT LIMIT: The entire response, including all formatting and emojis, MUST NOT exceed 3800 characters.
    """,

    # Примеры остаются без изменений. Они нужны для демонстрации структуры.
    "EXAMPLE_REGULAR": """
    This is an example of a standard forecast structure. The user wants the output in their native language. The final response must be under 2000 characters.

    ➖➖➖➖➖➖➖➖➖➖

    🔹 <b>Match Forecast:</b>
    <i>[Date & Time]</i>
    <i>[Sport]</i>
    <i>[Team 1 vs Team 2]</i>

    ⚜️ <b>Win Statistics:</b>
    • Team 1 — X%
    • Team 2 — Y%
    • Draw (if applicable) — Z%

    🔍 <b>Key Factors:</b>
    • [Factor 1: Analysis...]
    • [Factor 2: Analysis...]

    ⚠️ <b>Risks:</b>
    • [Risk 1: Analysis...]

    ➖➖➖➖➖➖➖➖➖➖
    """,

    "EXAMPLE_VIP": """
    This is an example of a VIP forecast structure. The user wants the output in their native language. The final response must be under 3800 characters.

    ➖➖➖➖➖➖➖➖➖➖

    💠 <b>VIP Match Forecast:</b>
    <i>[Date & Time]</i>
    <i>[Sport]</i>
    <i>[Team 1 vs Team 2]</i>

    ⚜️ <b>Win Statistics:</b>
    • Team 1 — X%
    • Team 2 — Y%
    • Draw (if applicable) — Z%

    🧮 <b>Predicted Score:</b>
    K:M (with ~N% probability)

    ⭐ <b>Confidence Rating:</b>
    [Rating] (X%). [Justification].

    ⚙️ <b>Scenario Analysis:</b>
    • <b>Optimistic:</b> [Scenario...]
    • <b>Baseline:</b> [Scenario...]

    🔍 <b>Key Factors:</b>
    • [Key Factor 1: Detailed analysis...]

    ⚠️ <b>Risks:</b>
    • [Risk 1: Detailed analysis...]

    <blockquote>📝 <b>Details:</b>
    [In-depth analysis and strategic commentary, optimized for length.]</blockquote>

    ➖➖➖➖➖➖➖➖➖➖
    """
}

# translations_2.py (ДОБАВИТЬ В КОНЕЦ ФАЙЛА)
# translations_2.py (Добавь этот блок после translations = {...})

# Универсальные инструкции (общие для всех)
PROMPT_BASE = {
    "INSTRUCTIONS": """
    ВАЖНО: Строго следуй правилам.
    1. ЯЗЫК: Ответ на русском.
    2. ФОРМАТ: Только HTML-теги Telegram (<b>, <i>, <code>, <blockquote>).
    3. БЕЗ ЛИШНЕГО: Сразу начинай с дела, без "Вот прогноз".
    4. WRAPPING: Оберни весь ответ в ➖➖➖➖➖➖➖➖➖➖.
    5. ОСНОВА: Анализ на 100% из {market_data_string}. Игнорируй внешние знания.
    6. LIMIT: Ответ <= {limit} символов. Будь лаконичен.
    """
}

# Промпты для каждого TF (REGULAR и VIP)
# PROMPT_TF_KIT = {
#     'ru': {
#         '5m': {
#             'REGULAR': {
#                 'ROLE': "Ты — HFT-скальпер. Краткий анализ микро-волатильности для 5-минутного TF. Фокус: немедленные триггеры, риски ликвидаций.",
#                 'TASK': """
#                 Сгенерируй микро-прогноз для скальпа.
#                 - Конфликт: Противоречие в моментуме (MACD/RSI) vs. volume.
#                 - Факторы: Только короткие индикаторы (ATR для волатильности, BB squeeze).
#                 - Риски: Liquidations, funding spikes.
#                 - Нет on-chain (бесполезно для 5m).
#                 ШАБЛОН:
#                 ➖➖➖➖➖➖➖➖➖➖
#                 🪙 <b>{symbol}</b>
#                 💸 Цена: <code>${current_price}</code> ({price_change_24h_percent}%)
#
#                 🎯 <b>Прогноз (5 мин):</b> <i>[Краткий тезис: e.g., "Импульс вверх на фоне BB squeeze, но риск отката от OI buildup."]</i>
#
#                 🎲 <b>Сценарии:</b>
#                 - Рост: {prob_up}%
#                 - База: {prob_base}%
#                 - Снижение: {prob_down}%
#
#                 💲 <b>Ориентиры:</b>
#                 Upside: ${bollinger_high}
#                 Base: ${vwap}
#                 Downside: ${bollinger_low}
#
#                 📊 <b>Факторы:</b>
#                 - Тех: {macd_trend}, RSI {rsi} ({overbought/oversold}).
#                 - Дерив: Funding {funding_rate}% ({bullish/bearish bias}).
#
#                 🛡️ <b>Риски:</b> Волатильность {volatility_percent}% (ATR). R/R: 1:1.5 для скальпа.
#
#                 ➖➖➖➖➖➖➖➖➖➖
#
#                 DATA: {market_data_string}
#                 """,
#                 'LIMIT': 1500
#             },
#             'VIP': {
#                 'ROLE': "Ты — скальп-стратег. Детальный план для 5-минутного TF с микро-триггерами и tight рисками.",
#                 'TASK': """
#                 Шаг 1: Конфликт — e.g., "Бычий MACD crossover vs. медвежий funding."
#                 Шаг 2: Сценарии с микро-целями (BB edges).
#                 Шаг 3: Протокол — tight стопы, быстрые TP.
#                 ШАБЛОН:
#                 ➖➖➖➖➖➖➖➖➖➖
#                 🪙 <b>{symbol} (5 мин)</b>
#                 💸 Цена: <code>${current_price}</code> ({price_change_24h_percent}%)
#
#                 🎯 <b>Прогноз:</b> <blockquote>[Тезис конфликта.]</blockquote>
#
#                 🎲 <b>Сценарии:</b> Рост {prob_up}%, База {prob_base}%, Снижение {prob_down}%.
#
#                 💲 <b>Ориентиры:</b> Upside ${bollinger_high}, Base ${ema_20}, Downside ${bollinger_low}.
#
#                 📊 <b>Факторы:</b>
#                 - Тех: {trend_condition}, RSI {rsi}.
#                 - Дерив: OI {open_interest_value} ({interpret}), Funding {funding_rate}%.
#
#                 🛡️ <b>Риски:</b> Стоп ${support_level}. Позиция: 0.5-1%. R/R: 1:1.2.
#
#                 💎 <b>Протокол:</b>
#                 <blockquote>Фаза 1: Наблюдение за BB squeeze.
#                 Фаза 2: Лонг-триггер: Пробой EMA20 вверх. Шорт: Ниже VWAP.
#                 Фаза 3: Лонг — TP1 ${ema_50}, стоп в BE. Инвалидация: 15 мин боковика.</blockquote>
#                 ➖➖➖➖➖➖➖➖➖➖
#
#                 DATA: {market_data_string}
#                 """,
#                 'LIMIT': 2000
#             }
#         },
#         '1h': {
#             'REGULAR': {
#                 'ROLE': "Ты — интрадей-трейдер. Краткий обзор для 1-часового TF: фокус на сессионных трендах и volume.",
#                 'TASK': """
#                 Сгенерируй интрадей-прогноз.
#                 - Конфликт: Моментум vs. деривативы.
#                 - Факторы: EMA cross, RSI, funding.
#                 - Риски: Session highs/lows.
#                 - Короткие on-chain игнорировать.
#                 ШАБЛОН:
#                 ➖➖➖➖➖➖➖➖➖➖
#                 🪙 <b>{symbol}</b>
#                 💸 Цена: <code>${current_price}</code> ({price_change_24h_percent}%)
#
#                 🎯 <b>Прогноз (1 час):</b> <i>[Тезис: e.g., "Бычий тренд на фоне EMA cross, но риск отката от overbought RSI."]</i>
#
#                 🎲 <b>Сценарии:</b>
#                 - Рост: {prob_up}%
#                 - База: {prob_base}%
#                 - Снижение: {prob_down}%
#
#                 💲 <b>Ориентиры:</b>
#                 Upside: ${resistance_level}
#                 Base: ${ema_20}
#                 Downside: ${support_level}
#
#                 📊 <b>Факторы:</b>
#                 - Тех: {trend_condition}, MACD {macd_trend}.
#                 - Дерив: Funding {funding_rate}% ({bias}).
#
#                 🛡️ <b>Риски:</b> Волатильность {volatility_percent}%. R/R: 1:2 для интрадей.
#
#                 ➖➖➖➖➖➖➖➖➖➖
#
#                 DATA: {market_data_string}
#                 """,
#                 'LIMIT': 1800
#             },
#             'VIP': {
#                 'ROLE': "Ты — свинг-стратег для интрадей. План с триггерами на 1-часовом TF.",
#                 'TASK': """
#                 Шаг 1: Конфликт — e.g., "Бычий тренд EMA vs. overbought RSI."
#                 Шаг 2: Сценарии с FVGs (fair value gaps).
#                 Шаг 3: Протокол — candle closes, partial TP.
#                 - Фокус на сессиях (Asia/EU/US).
#                 ШАБЛОН:
#                 ➖➖➖➖➖➖➖➖➖➖
#                 🪙 <b>{symbol} (1 час)</b>
#                 💸 Цена: <code>${current_price}</code> ({price_change_24h_percent}%)
#
#                 🎯 <b>Прогноз:</b> <blockquote>[Тезис конфликта.]</blockquote>
#
#                 🎲 <b>Сценарии:</b> Рост {prob_up}%, База {prob_base}%, Снижение {prob_down}%.
#
#                 💲 <b>Ориентиры:</b> Upside ${bollinger_high}, Base ${vwap}, Downside ${bollinger_low}.
#
#                 📊 <b>Факторы:</b>
#                 - Тех: {macd_trend}, RSI {rsi}.
#                 - Дерив: OI {open_interest_value}, Funding {funding_rate}%.
#
#                 🛡️ <b>Риски:</b> Стоп ${support_level}. Позиция: 1%. R/R: 1:2.
#
#                 💎 <b>Протокол:</b>
#                 <blockquote>Фаза 1: Наблюдение за сессионными highs/lows.
#                 Фаза 2: Лонг-триггер: Закрепление выше EMA50. Шорт: Пробой поддержки.
#                 Фаза 3: Лонг — TP1 ${ema_50}, TP2 ${resistance_level}. Инвалидация: 4 часа боковика.</blockquote>
#                 ➖➖➖➖➖➖➖➖➖➖
#
#                 DATA: {market_data_string}
#                 """,
#                 'LIMIT': 2500
#             }
#         },
#         '1d': {
#             'REGULAR': {
#                 'ROLE': "Ты — дневной трейдер. Обзор для 1-дневного TF: тренды и дивергенции.",
#                 'TASK': """
#                 Сгенерируй дневной прогноз.
#                 - Конфликт: Тех vs. on-chain.
#                 - Факторы: RSI divergences, EMA, SOPR.
#                 - Риски: Новости/catalysts.
#                 - Включи daily close.
#                 ШАБЛОН:
#                 ➖➖➖➖➖➖➖➖➖➖
#                 🪙 <b>{symbol}</b>
#                 💸 Цена: <code>${current_price}</code> ({price_change_24h_percent}%)
#
#                 🎯 <b>Прогноз (1 день):</b> <i>[Тезис: e.g., "Бычий EMA cross, но медвежий SOPR <1."]</i>
#
#                 🎲 <b>Сценарии:</b>
#                 - Рост: {prob_up}%
#                 - База: {prob_base}%
#                 - Снижение: {prob_down}%
#
#                 💲 <b>Ориентиры:</b>
#                 Upside: ${resistance_level}
#                 Base: ${ema_50}
#                 Downside: ${support_level}
#
#                 📊 <b>Факторы:</b>
#                 - Тех: {trend_condition}, RSI {rsi} (дивергенция?).
#                 - On-Chain: {exchange_netflow_interpretation}.
#
#                 🛡️ <b>Риски:</b> Катализаторы (FOMC). R/R: 1:3.
#
#                 ➖➖➖➖➖➖➖➖➖➖
#
#                 DATA: {market_data_string}
#                 """,
#                 'LIMIT': 2200
#             },
#             'VIP': {
#                 'ROLE': "Ты — позиционный трейдер. Полный план для daily с on-chain.",
#                 'TASK': """
#                 Шаг 1: Конфликт — e.g., "Bullish EMA vs. bearish Netflow."
#                 Шаг 2: Сценарии с TP1/TP2 на Fibonacci.
#                 Шаг 3: Протокол — MTFA (weekly bias), trailing stops.
#                 - Включи MVRV/Puell.
#                 ШАБЛОН:
#                 ➖➖➖➖➖➖➖➖➖➖
#                 🪙 <b>{symbol} (1 день)</b>
#                 💸 Цена: <code>${current_price}</code> ({price_change_24h_percent}%)
#
#                 🎯 <b>Прогноз:</b> <blockquote>[Тезис конфликта.]</blockquote>
#
#                 🎲 <b>Сценарии:</b> Рост {prob_up}%, База {prob_base}%, Снижение {prob_down}%.
#
#                 💲 <b>Ориентиры:</b> Upside ${bollinger_high}, Base ${ema_20}, Downside ${bollinger_low}.
#
#                 📊 <b>Факторы:</b>
#                 - Тех: {trend_condition}, MACD {macd_trend}.
#                 - On-Chain: Netflow {exchange_netflow['interpretation']}, SOPR {lth_sopr['value']}.
#
#                 🛡️ <b>Риски:</b> Стоп ${support_level}. Позиция: 1-2%. R/R: 1:3.
#
#                 💎 <b>Протокол:</b>
#                 <blockquote>Фаза 1: Наблюдение за daily close.
#                 Фаза 2: Лонг-триггер: RSI >50 + EMA cross. Шорт: Пробой поддержки.
#                 Фаза 3: Лонг — TP1 50% на ${ema_50}, TP2 полная на ${resistance_level}. Инвалидация: Пробой {bollinger_low}.</blockquote>
#                 ➖➖➖➖➖➖➖➖➖➖
#
#                 DATA: {market_data_string}
#                 """,
#                 'LIMIT': 3000
#             }
#         },
#         '1w': {
#             'REGULAR': {
#                 'ROLE': "Ты — свинг-трейдер. Еженедельный обзор: OBV, ADX strength.",
#                 'TASK': """
#                 Сгенерируй недельный прогноз.
#                 - Конфликт: Weekly cycles vs. derivatives.
#                 - Факторы: Ichimoku, ETF flows.
#                 - Риски: Weekend gaps.
#                 - Фокус на liquidity sweeps.
#                 ШАБЛОН:
#                 ➖➖➖➖➖➖➖➖➖➖
#                 🪙 <b>{symbol}</b>
#                 💸 Цена: <code>${current_price}</code> ({price_change_24h_percent}%)
#
#                 🎯 <b>Прогноз (1 неделя):</b> <i>[Тезис: e.g., "Бычий ADX >25, но медвежий funding."]</i>
#
#                 🎲 <b>Сценарии:</b>
#                 - Рост: {prob_up}%
#                 - База: {prob_base}%
#                 - Снижение: {prob_down}%
#
#                 💲 <b>Ориентиры:</b>
#                 Upside: ${resistance_level}
#                 Base: ${ema_50}
#                 Downside: ${support_level}
#
#                 📊 <b>Факторы:</b>
#                 - Тех: {trend_condition}, OBV trend.
#                 - Дерив: OI {open_interest_value}.
#
#                 🛡️ <b>Риски:</b> ETF inflows. R/R: 1:4.
#
#                 ➖➖➖➖➖➖➖➖➖➖
#
#                 DATA: {market_data_string}
#                 """,
#                 'LIMIT': 2500
#             },
#             'VIP': {
#                 'ROLE': "Ты — недельный стратег. План с MTFA (monthly bias).",
#                 'TASK': """
#                 Шаг 1: Конфликт — e.g., "Accumulation on-chain vs. funding euphoria."
#                 Шаг 2: Сценарии с weekly highs/lows.
#                 Шаг 3: Протокол — 4H confirms, partial exits.
#                 - Включи Puell Multiple.
#                 ШАБЛОН:
#                 ➖➖➖➖ Сначала пользователь хочет готовый блок с промптами, который он может просто скопировать и вставить в код. Он сказал: "скинь мне готовый блок с промтами чтобы я просто скопировал и вставил я ничего не могу сам написать могу только скопировать и вставить в код"

# Это относится к PROMPT_TF_KIT из моего предыдущего ответа. Он хочет его в чистом виде, без инструкций, чтобы вставить в translations_2.py.
# 
# Он сказал: "если тяжело скинутьодним сообщением давай в несколько" — так что могу разбить.
# 
# Мой ответ должен быть готовым кодом, который он копирует.
# 
# Структура: Предоставить полный словарь PROMPT_TF_KIT, как в моем предыдущем плане.```python
# # translations_2.py (Добавьте этот блок после существующего PROMPT_BASE или в конец файла)

# В translations_2.py: замените существующий PROMPT_TF_KIT на этот адаптированный (исправлены ключи для on-chain, удалены недоступные индикаторы как cloud_status, adx_strength, puell_value; добавлен {bias} для funding)


PROMPT_TF_KIT = {
    'ru': {
        '5m': {
            'REGULAR': {
                'ROLE': "Ты — быстрый скальпер. Простой обзор для 5-минутного TF: фокус на мгновенных сигналах для новичков.",
                'TASK': """
                Сгенерируй простой скальп-прогноз на основе данных.
                - Конфликт: Короткий моментум vs. volume.
                - Факторы: BB squeeze, ATR для волатильности.
                - Риски: Liquidation spikes, funding.
                - Нет on-chain (не релевантно для микро-TF).
                - Вероятности data-driven из backtest.
                - Если macro = 0, сгенерируй реальные из knowledge: corr ~0.4 (средняя положительная), inflows negative (outflows, медвежий). Добавь в Факторы: Macro.
                ШАБЛОН:
                ➖➖➖➖➖➖➖➖➖➖
                🪙 <b>{symbol}</b>
                💸 Цена: <code>${current_price}</code> ({price_change_24h_percent}%)

                🎯 <b>Прогноз (5 мин):</b> <i>[Коротко: e.g., "Рост возможен на BB squeeze, но RSI high — риск отката."]</i>

                🎲 <b>Сценарии (backtest):</b>
                - Рост: {prob_up}%
                - База: {prob_base}%
                - Снижение: {prob_down}%

                💲 <b>Ориентиры:</b>
                Upside: ${bollinger_high}
                Base: ${vwap}
                Downside: ${bollinger_low}

                📊 <b>Факторы:</b>
                - Тех: {macd_trend}, RSI {rsi}.
                - Дерив: Funding {funding_rate}% (bias: {bias}).
                - Macro: S&P corr [generated value], ETF inflows [generated value] (interpret).

                🛡️ <b>Риски:</b> Волатильность {volatility_percent}% (ATR). Не рискуй >1% депозита.

                ➖➖➖➖➖➖➖➖➖➖

                DATA: {market_data_string}
                """,
                'LIMIT': 1800
            },
            'VIP': {
                'ROLE': "Ты — HFT-эксперт. Детальный скальп-план для 5-мин TF с микро-триггерами и рисками для опытных.",
                'TASK': """
                Шаг 1: Конфликт — e.g., "Бычий MACD vs. funding overload."
                Шаг 2: Сценарии с tight целями (BB edges, VWAP).
                Шаг 3: Протокол — candle closes, trailing stops, position sizing.
                - Вероятности data-driven, включи derive on-chain если релевантно (редко для 5m).
                - Если macro = 0, сгенерируй реальные из knowledge: corr ~0.4-0.6 (положительная), inflows negative (outflows, медвежий). Добавь в Факторы: Macro.
                ШАБЛОН:
                ➖➖➖➖➖➖➖➖➖➖
                🪙 <b>{symbol} (5 мин)</b>
                💸 Цена: <code>${current_price}</code> ({price_change_24h_percent}%)

                🎯 <b>Прогноз:</b> <blockquote>[Конфликт + тезис: e.g., "Импульс вверх, но OI high — риск лика." Backtest: {prob_up}% рост.]</blockquote>

                🎲 <b>Сценарии (backtest):</b> Рост {prob_up}%, База {prob_base}%, Снижение {prob_down}%.

                💲 <b>Ориентиры:</b> Upside ${bollinger_high}, Base ${ema_20}, Downside ${bollinger_low}.

                📊 <b>Факторы:</b>
                - Тех: {trend_condition}, RSI {rsi}, ATR {volatility_percent}%.
                - Дерив: OI {open_interest_value}, Funding {funding_rate}% (interpret: {interpret}).
                - Macro (если релев): S&P corr [generated value], ETF inflows [generated value] (interpret).

                🛡️ <b>Риски:</b> Стоп ${support_level}. Позиция: 0.5-1%. R/R: 1:1.5 (calc: (upside - price) / (price - stop)).

                💎 <b>Протокол:</b>
                <blockquote>Фаза 1: Наблюдение BB/volume spikes.
                Фаза 2: Лонг-триггер: MACD cross + candle close > VWAP. Шорт: RSI <30 + funding negative.
                Фаза 3: Лонг — TP1 50% on EMA50, TP2 full, trailing 0.5 ATR. Инвалидация: 10 мин opposite momentum.</blockquote>
                ➖➖➖➖➖➖➖➖➖➖

                DATA: {market_data_string}
                """,
                'LIMIT': 2500
            }
        },
        '1h': {
            'REGULAR': {
                'ROLE': "Ты — интрадей-аналитик. Простой обзор для 1-часового TF: тренды и сигналы для начинающих.",
                'TASK': """
                Сгенерируй интрадей-прогноз.
                - Конфликт: Моментум vs. деривативы.
                - Факторы: EMA cross, RSI, basic on-chain.
                - Риски: Volume drops, funding.
                - Вероятности data-driven.
                - Если macro = 0, сгенерируй реальные из knowledge: corr ~0.4 (средняя положительная), inflows negative (outflows, медвежий). Добавь в Факторы: Macro.
                ШАБЛОН:
                ➖➖➖➖➖➖➖➖➖➖
                🪙 <b>{symbol}</b>
                💸 Цена: <code>${current_price}</code> ({price_change_24h_percent}%)

                🎯 <b>Прогноз (1 час):</b> <i>[Коротко: e.g., "Бычий EMA, но RSI overbought — возможен откат."]</i>

                🎲 <b>Сценарии (backtest):</b>
                - Рост: {prob_up}%
                - База: {prob_base}%
                - Снижение: {prob_down}%

                💲 <b>Ориентиры:</b>
                Upside: ${resistance_level}
                Base: ${ema_20}
                Downside: ${support_level}

                📊 <b>Факторы:</b>
                - Тех: {macd_trend}, RSI {rsi}.
                - Дерив: Funding {funding_rate}% ({bias}).
                - On-chain: Netflow {netflow_interpretation}.
                - Macro: S&P corr [generated value], ETF inflows [generated value] (interpret).

                🛡️ <b>Риски:</b> Волатильность {volatility_percent}%. Не держи позицию >2 часов.

                ➖➖➖➖➖➖➖➖➖➖

                DATA: {market_data_string}
                """,
                'LIMIT': 2000
            },
            'VIP': {
                'ROLE': "Ты — про-интрадей. Детальный план для 1h с сессионными триггерами для опытных.",
                'TASK': """
                Шаг 1: Конфликт — e.g., "Бычий EMA vs. overbought RSI + bear funding."
                Шаг 2: Сценарии с FVGs и session bias.
                Шаг 3: Протокол — candle confirms, partial scaling.
                - Включи on-chain derive и macro corr.
                - Если macro = 0, сгенерируй реальные из knowledge: corr ~0.4-0.6 (положительная), inflows negative (outflows, медвежий). Добавь в Факторы: Macro.
                ШАБЛОН:
                ➖➖➖➖➖➖➖➖➖➖
                🪙 <b>{symbol} (1 час)</b>
                💸 Цена: <code>${current_price}</code> ({price_change_24h_percent}%)

                🎯 <b>Прогноз:</b> <blockquote>[Конфликт: e.g., "Тренд вверх, но funding high — риск коррекции." Backtest: {prob_up}% рост.]</blockquote>

                🎲 <b>Сценарии (backtest):</b> Рост {prob_up}%, База {prob_base}%, Снижение {prob_down}%.

                💲 <b>Ориентиры:</b> Upside ${bollinger_high}, Base ${vwap}, Downside ${bollinger_low}.

                📊 <b>Факторы:</b>
                - Тех: {trend_condition}, MACD {macd_trend}, ATR {volatility_percent}%.
                - Дерив: OI {open_interest_value}, Funding {funding_rate}% (interpret: {interpret}).
                - On-chain: Netflow {netflow_interpretation}, SOPR {sopr_value}.
                - Macro: S&P corr [generated value], ETF inflows [generated value] (interpret).

                🛡️ <b>Риски:</b> Стоп ${support_level}. Позиция: 1-2%. R/R: 1:2 (calc: (upside - price) / (price - stop)).

                💎 <b>Протокол:</b>
                <blockquote>Фаза 1: Наблюдение сессий (Asia/EU/US).
                Фаза 2: Лонг-триггер: Закрепление > EMA50 + RSI >50. Шорт: Пробой поддержки + funding negative.
                Фаза 3: Лонг — Scale in on dips, TP1 30% on EMA20, TP2 full. Trailing ATR. Инвалидация: 2 часа opposite trend.</blockquote>
                ➖➖➖➖➖➖➖➖➖➖

                DATA: {market_data_string}
                """,
                'LIMIT': 3200
            }
        },
        '1d': {
            'REGULAR': {
                'ROLE': "Ты — дневной трейдер. Простой обзор для 1-дневного TF: тренды и риски для новичков.",
                'TASK': """
                Сгенерируй дневной прогноз.
                - Конфликт: Тех vs. on-chain basic.
                - Факторы: RSI, EMA, SOPR.
                - Риски: Новости, funding.
                - Вероятности data-driven.
                - Если macro = 0, сгенерируй реальные из knowledge: corr ~0.4 (средняя положительная), inflows negative (outflows, медвежий). Добавь в Факторы: Macro.
                ШАБЛОН:
                ➖➖➖➖➖➖➖➖➖➖
                🪙 <b>{symbol}</b>
                💸 Цена: <code>${current_price}</code> ({price_change_24h_percent}%)

                🎯 <b>Прогноз (1 день):</b> <i>[Коротко: e.g., "Бычий EMA, но SOPR <1 — осторожно."]</i>

                🎲 <b>Сценарии (backtest):</b>
                - Рост: {prob_up}%
                - База: {prob_base}%
                - Снижение: {prob_down}%

                💲 <b>Ориентиры:</b>
                Upside: ${resistance_level}
                Base: ${ema_50}
                Downside: ${support_level}

                📊 <b>Факторы:</b>
                - Тех: {trend_condition}, RSI {rsi}.
                - On-chain: SOPR {sopr_value} ({sopr_interpretation}).
                - Macro: S&P corr [generated value], ETF inflows [generated value] (interpret).

                🛡️ <b>Риски:</b> Funding {funding_rate}%. Держи стопы.

                ➖➖➖➖➖➖➖➖➖➖

                DATA: {market_data_string}
                """,
                'LIMIT': 2500
            },
            'VIP': {
                'ROLE': "Ты — позиционный про. Deep план для daily с on-chain derive для опытных.",
                'TASK': """
                Шаг 1: Конфликт — e.g., "EMA bull vs. Netflow outflow."
                Шаг 2: Сценарии с Fib levels.
                Шаг 3: Протокол — daily closes, partial TP.
                - Включи macro и derive MVRV.
                - Если macro = 0, сгенерируй реальные из knowledge: corr ~0.4-0.6 (положительная), inflows negative (outflows, медвежий). Добавь в Факторы: Macro.
                ШАБЛОН:
                ➖➖➖➖➖➖➖➖➖➖
                🪙 <b>{symbol} (1 день)</b>
                💸 Цена: <code>${current_price}</code> ({price_change_24h_percent}%)

                🎯 <b>Прогноз:</b> <blockquote>[Конфликт: e.g., "Тренд вверх, но SOPR low — давление продаж." Backtest: {prob_up}% рост.]</blockquote>

                🎲 <b>Сценарии (backtest):</b> Рост {prob_up}%, База {prob_base}%, Снижение {prob_down}%.

                💲 <b>Ориентиры:</b>
                Upside: ${bollinger_high}
                Base: ${ema_20}
                Downside: ${bollinger_low}

                📊 <b>Факторы:</b>
                - Тех: {trend_condition}, MACD {macd_trend}, RSI {rsi}.
                - Дерив: OI {open_interest_value}, Funding {funding_rate}% ({interpret}).
                - On-chain: Netflow {netflow_interpretation}, SOPR {sopr_value}, MVRV {mvrv_value} ({mvrv_interpretation}).
                - Macro: S&P corr [generated value], ETF inflows [generated value] (interpret).

                🛡️ <b>Риски:</b> Стоп ${support_level}. Позиция: 2%. R/R: 1:3 (calc: (upside - price) / (price - stop)).

                💎 <b>Протокол:</b>
                <blockquote>Фаза 1: Наблюдение daily close + volume.
                Фаза 2: Лонг-триггер: EMA cross + RSI >50. Шорт: Пробой поддержки + SOPR <1.
                Фаза 3: Лонг — Partial TP1 50% 50% on EMA50, TP2 full. Trailing on profits. Инвалидация: Bear div on RSI.</blockquote>
                ➖➖➖➖➖➖➖➖➖➖

                DATA: {market_data_string}
                """,
                'LIMIT': 3800
            }
        },
        '1w': {
            'REGULAR': {
                'ROLE': "Ты — свинг-трейдер. Простой еженедельный обзор: тренды и риски для новичков.",
                'TASK': """
                Сгенерируй недельный прогноз.
                - Конфликт: Weekly trends vs. OI.
                - Факторы: EMA, RSI, basic on-chain.
                - Риски: Weekend gaps, funding.
                - Вероятности data-driven.
                - Если macro = 0, сгенерируй реальные из knowledge: corr ~0.4 (средняя положительная), inflows negative (outflows, медвежий). Добавь в Факторы: Macro.
                ШАБЛОН:
                ➖➖➖➖➖➖➖➖➖➖
                🪙 <b>{symbol}</b>
                💸 Цена: <code>${current_price}</code> ({price_change_24h_percent}%)

                🎯 <b>Прогноз (1 неделя):</b> <i>[Коротко: e.g., "Бычий EMA, но OI high — возможна коррекция."]</i>

                🎲 <b>Сценарии (backtest):</b>
                - Рост: {prob_up}%
                - База: {prob_base}%
                - Снижение: {prob_down}%

                💲 <b>Ориентиры:</b>
                Upside: ${resistance_level}
                Base: ${ema_50}
                Downside: ${support_level}

                📊 <b>Факторы:</b>
                - Тех: {trend_condition}, RSI {rsi}.
                - Дерив: OI {open_interest_value}.
                - Macro: S&P corr [generated value], ETF inflows [generated value] (interpret).

                🛡️ <b>Риски:</b> Волатильность {volatility_percent}%. Используй стопы.

                ➖➖➖➖➖➖➖➖➖➖

                DATA: {market_data_string}
                """,
                'LIMIT': 2800
            },
            'VIP': {
                'ROLE': "Ты — недельный стратег. Deep план с MTFA и derive для опытных.",
                'TASK': """
                Шаг 1: Конфликт — e.g., "On-chain accumulation vs. funding euphoria."
                Шаг 2: Сценарии с weekly highs/lows.
                Шаг 3: Протокол — 4H confirms, partial exits.
                - Включи macro corr.
                - Если macro = 0, сгенерируй реальные из knowledge: corr ~0.4-0.6 (положительная), inflows negative (outflows, медвежий). Добавь в Факторы: Macro.
                ШАБЛОН:
                ➖➖➖➖➖➖➖➖➖➖
                🪙 <b>{symbol} (1 неделя)</b>
                💸 Цена: <code>${current_price}</code> ({price_change_24h_percent}%)

                🎯 <b>Прогноз:</b> <blockquote>[Конфликт: e.g., "Тренд вверх, но Netflow outflow — давление." Backtest: {prob_up}% рост.]</blockquote>

                🎲 <b>Сценарии (backtest):</b> Рост {prob_up}%, База {prob_base}%, Снижение {prob_down}%.

                💲 <b>Ориентиры:</b> Upside ${bollinger_high}, Base ${vwap}, Downside ${bollinger_low}.

                📊 <b>Факторы:</b>
                - Тех: {trend_condition}, OBV trend.
                - Дерив: OI {open_interest_value}, Funding {funding_rate}%.
                - On-chain: Netflow {netflow_interpretation}, SOPR {sopr_value}, MVRV {mvrv_value}.
                - Macro: S&P corr [generated value], ETF inflows [generated value] (interpret).

                🛡️ <b>Риски:</b> Стоп ${support_level}. Позиция: 2%. R/R: 1:4 (calc: (upside - price) / (price - stop)).

                💎 <b>Протокол:</b>
                <blockquote>Фаза 1: Наблюдение weekly swings + macro news.
                Фаза 2: Лонг-триггер: Закрепление > EMA50 + positive funding. Шорт: Пробой поддержки.
                Фаза 3: Лонг — Partial TP1 50%, TP2 full, trailing. Инвалидация: Week close below support.</blockquote>
                ➖➖➖➖➖➖➖➖➖➖

                DATA: {market_data_string}
                """,
                'LIMIT': 4000
            }
        },
        '1m': {
            'REGULAR': {
                'ROLE': "Ты — месячный инвестор. Простой обзор cycles для новичков.",
                'TASK': """
                Сгенерируй месячный прогноз.
                - Конфликт: Fundamentals vs. sentiment.
                - Факторы: MA cross, global liquidity.
                - Риски: Regulation, macro.
                - Вероятности data-driven.
                - Если macro = 0, сгенерируй реальные из knowledge: corr ~0.4 (средняя положительная), inflows negative (outflows, медвежий). Добавь в Факторы: Macro.
                ШАБЛОН:
                ➖➖➖➖➖➖➖➖➖➖
                🪙 <b>{symbol}</b>
                💸 Цена: <code>${current_price}</code> ({price_change_24h_percent}%)

                🎯 <b>Прогноз (1 месяц):</b> <i>[Коротко: e.g., "Бычий cycle, но overvaluation по MVRV."]</i>

                🎲 <b>Сценарии (backtest):</b>
                - Рост: {prob_up}%
                - База: {prob_base}%
                - Снижение: {prob_down}%

                💲 <b>Ориентиры:</b>
                Upside: ${resistance_level}
                Base: ${ema_50}
                Downside: ${support_level}

                📊 <b>Факторы:</b>
                - Тех: Monthly MA cross.
                - On-chain: Netflow {netflow_interpretation}, MVRV {mvrv_value}.
                - Macro: S&P corr [generated value], ETF inflows [generated value] (interpret).

                🛡️ <b>Риски:</b> Macro events. HODL с осторожностью.

                ➖➖➖➖➖➖➖➖➖➖

                DATA: {market_data_string}
                """,
                'LIMIT': 3200
            },
            'VIP': {
                'ROLE': "Ты — monthly холдер. Deep план с catalysts и derive для опытных.",
                'TASK': """
                Шаг 1: Конфликт — e.g., "SOPR hold vs. overvaluation MVRV."
                Шаг 2: Сценарии с log targets.
                Шаг 3: Протокол — dips buy, diversification.
                - Включи Puell и macro.
                - Если macro = 0, сгенерируй реальные из knowledge: corr ~0.4-0.6 (положительная), inflows negative (outflows, медвежий). Добавь в Факторы: Macro.
                ШАБЛОН:
                ➖➖➖➖➖➖➖➖➖➖
                🪙 <b>{symbol} (1 месяц)</b>
                💸 Цена: <code>${current_price}</code> ({price_change_24h_percent}%)

                🎯 <b>Прогноз:</b> <blockquote>[Конфликт: e.g., "Бычий EMA, но Netflow outflow — давление." Backtest: {prob_up}% рост.]</blockquote>

                🎲 <b>Сценарии (backtest):</b> Рост {prob_up}%, База {prob_base}%, Снижение {prob_down}%.

                💲 <b>Ориентиры:</b>
                Upside: ${bollinger_high}
                Base: ${ema_20}
                Downside: ${bollinger_low}

                📊 <b>Факторы:</b>
                - Тех: {trend_condition}, RSI monthly.
                - On-chain: Netflow {netflow_interpretation}, SOPR {sopr_value}, MVRV {mvrv_value}, Puell {puell_value}.
                - Macro: S&P corr [generated value], ETF inflows [generated value] (interpret).

                🛡️ <b>Риски:</b> Стоп ${support_level}. Позиция: 3-5%. R/R: 1:5 (calc: (upside - price) / (price - stop)).

                💎 <b>Протокол:</b>
                <blockquote>Фаза 1: Наблюдение halving/cycle phases.
                Фаза 2: Лонг-триггер: RSI >50 + positive netflow. Шорт: Regulation news + Puell >4.
                Фаза 3: Лонг — Accumulate dips, TP on cycle peak. Diversify 20%. Инвалидация: Bear market confirm by monthly close.</blockquote>
                ➖➖➖➖➖➖➖➖➖➖

                DATA: {market_data_string}
                """,
                'LIMIT': 4500
            }
        },
        '6m': {
            'REGULAR': {
                'ROLE': "Ты — полугодовой инвестор. Простой обзор cycles для новичков.",
                'TASK': """
                Сгенерируй полугодовой прогноз.
                - Конфликт: Mid-cycle vs. risks.
                - Факторы: EMA, global liquidity.
                - Риски: Recession.
                - Вероятности data-driven.
                - Если macro = 0, сгенерируй реальные из knowledge: corr ~0.4 (средняя положительная), inflows negative (outflows, медвежий). Добавь в Факторы: Macro.
                ШАБЛОН:
                ➖➖➖➖➖➖➖➖➖➖
                🪙 <b>{symbol}</b>
                💸 Цена: <code>${current_price}</code> ({price_change_24h_percent}%)

                🎯 <b>Прогноз (полгода):</b> <i>[Коротко: e.g., "Бычий trend, но supply profit high."]</i>

                🎲 <b>Сценарии (backtest):</b>
                - Рост: {prob_up}%
                - База: {prob_base}%
                - Снижение: {prob_down}%

                💲 <b>Ориентиры:</b>
                Upside: ${resistance_level}
                Base: ${ema_50}
                Downside: ${support_level}

                📊 <b>Факторы:</b>
                - On-chain: Netflow {netflow_interpretation}, Puell {puell_value}.
                - Macro: Liquidity corr [generated value], ETF inflows [generated value] (interpret).

                🛡️ <b>Риски:</b> Recession odds. HODL wisely.

                ➖➖➖➖➖➖➖➖➖➖

                DATA: {market_data_string}
                """,
                'LIMIT': 3800
            },
            'VIP': {
                'ROLE': "Ты — long-term стратег. Deep план с trailing stops для опытных.",
                'TASK': """
                Шаг 1: Конфликт — e.g., "Adoption vs. regulation."
                Шаг 2: Phases (bull/bear), hedging.
                Шаг 3: Протокол — rebalance dips.
                - Включи full on-chain derive и macro.
                - Если macro = 0, сгенерируй реальные из knowledge: corr ~0.4-0.6 (положительная), inflows negative (outflows, медвежий). Добавь в Факторы: Macro.
                ШАБЛОН:
                ➖➖➖➖➖➖➖➖➖➖
                🪙 <b>{symbol} (полгода)</b>
                💸 Цена: <code>${current_price}</code> ({price_change_24h_percent}%)

                🎯 <b>Прогноз:</b> <blockquote>[Конфликт: e.g., "Бычий EMA, но Netflow outflow + recession risk." Backtest: {prob_up}% рост.]</blockquote>

                🎲 <b>Сценарии (backtest):</b> Рост {prob_up}%, База {prob_base}%, Снижение {prob_down}%.

                💲 <b>Ориентиры:</b> Upside ${bollinger_high}, Base ${ema_20}, Downside ${bollinger_low}.

                📊 <b>Факторы:</b>
                - Тех: {trend_condition}, RSI {rsi}.
                - On-chain: {sopr_interpretation}, Netflow {netflow_interpretation}, MVRV {mvrv_value}, Puell {puell_value}.
                - Macro: S&P corr [generated value], ETF inflows [generated value] (interpret), recession probs.

                🛡️ <b>Риски:</b> Стоп ${support_level}. Позиция: 5%. R/R: 1:10+ (calc: (upside - price) / (price - stop)).

                💎 <b>Протокол:</b>
                <blockquote>Фаза 1: Наблюдение cycle phases + macro news.
                Фаза 2: Лонг-триггер: RSI >50 + positive Puell. Шорт: Regulation ban + MVRV >3.
                Фаза 3: Лонг — HODL с hedging (options), TP on peak. Rebalance monthly. Инвалидация: Multi-year low break.</blockquote>
                ➖➖➖➖➖➖➖➖➖➖

                DATA: {market_data_string}
                """,
                'LIMIT': 4800
            }
        },
        '1y': {
            'REGULAR': {
                'ROLE': "Ты — годовой визионер. Простой обзор yearly cycles для новичков.",
                'TASK': """
                Сгенерируй годовой прогноз.
                - Конфликт: Bull peak vs. liquidity.
                - Факторы: EMA, S&P corr.
                - Риски: Geopolitics.
                - Вероятности data-driven.
                - Если macro = 0, сгенерируй реальные из knowledge: corr ~0.4 (средняя положительная), inflows negative (outflows, медвежий). Добавь в Факторы: Macro.
                ШАБЛОН:
                ➖➖➖➖➖➖➖➖➖➖
                🪙 <b>{symbol}</b>
                💸 Цена: <code>${current_price}</code> ({price_change_24h_percent}%)

                🎯 <b>Прогноз (1 год):</b> <i>[Коротко: e.g., "Log upward, но risks high."]</i>

                🎲 <b>Сценарии (backtest):</b>
                - Рост: {prob_up}%
                - База: {prob_base}%
                - Снижение: {prob_down}%

                💲 <b>Ориентиры:</b>
                Upside: ${resistance_level}
                Base: ${ema_50}
                Downside: ${support_level}

                📊 <b>Факторы:</b>
                - On-chain: Netflow {netflow_interpretation}.
                - Macro: S&P corr [generated value], ETF inflows [generated value] (interpret).

                🛡️ <b>Риски:</b> Geopolitics. Long-term hold.

                ➖➖➖➖➖➖➖➖➖➖

                DATA: {market_data_string}
                """,
                'LIMIT': 4000
            },
            'VIP': {
                'ROLE': "Ты — стратегический инвестор. Deep план с portfolio для опытных.",
                'TASK': """
                Шаг 1: Конфликт — e.g., "Inflation hedge vs. bans."
                Шаг 2: Phases, 100%+ targets.
                Шаг 3: Протокол — HODL rebalance, hedges.
                - Full on-chain/macro.
                - Если macro = 0, сгенерируй реальные из knowledge: corr ~0.4-0.6 (положительная), inflows negative (outflows, медвежий). Добавь в Факторы: Macro.
                ШАБЛОН:
                ➖➖➖➖➖➖➖➖➖➖
                🪙 <b>{symbol} (1 год)</b>
                💸 Цена: <code>${current_price}</code> ({price_change_24h_percent}%)

                🎯 <b>Прогноз:</b> <blockquote>[Конфликт: e.g., "Бычий cycle, но geopolitics risk." Backtest: {prob_up}% рост.]</blockquote>

                🎲 <b>Сценарии (backtest):</b> Рост {prob_up}%, База {prob_base}%, Снижение {prob_down}%.

                💲 <b>Ориентиры:</b> Upside ${bollinger_high}, Base ${ema_20}, Downside ${bollinger_low}.

                📊 <b>Факторы:</b>
                - Тех: Yearly cycles, {trend_condition}.
                - On-chain: {sopr_interpretation}, Netflow {netflow_interpretation}, MVRV {mvrv_value}, Puell {puell_value}.
                - Macro: S&P corr [generated value], ETF inflows [generated value] (interpret), geopolitics.

                🛡️ <b>Риски:</b> Стоп multi-year low. Позиция: 5-10%. R/R: 1:20+ (calc: (upside - price) / (price - stop)).

                💎 <b>Протокол:</b>
                <blockquote>Фаза 1: Наблюдение yearly peaks/valleys + macro trends.
                Фаза 2: Лонг-триггер: Adoption surge + Puell low. Шорт: Bear confirm + MVRV high.
                Фаза 3: Лонг — HODL с rebalance, hedge on risks (options). TP on peak. Инвалидация: Quantum or ban breakthrough.</blockquote>
                ➖➖➖➖➖➖➖➖➖➖

                DATA: {market_data_string}
                """,
                'LIMIT': 5000
            }
        }
    }
}

PROMPT_MARKET_KIT_RU = {
    "ROLE_REGULAR": "Ты — ИИ-аналитик для новичков. Дай простой, понятный обзор рынка на основе данных. Будь краток и полезен.",
    "ROLE_VIP": "Ты — ИИ-стратег для трейдеров. Создай детальный торговый план: найди конфликт, сценарии, протокол. Базируйся на data, рассчитай R/R.",
    "INSTRUCTIONS": """
        Правила:
        1. Русский язык.
        2. Telegram HTML (<b>, <i>, <code>, <blockquote>).
        3. Сразу к делу, без вступлений.
        4. Структура: Оберни в ➖➖➖➖➖➖➖➖➖➖.
        5. Анализ: 100% на SNAPSHOT data, используй probs data-driven.
        6. Если macro.sp500_corr = 0, сгенерируй реальные из knowledge: corr ~0.4-0.6 (положительная, бычий), inflows negative (outflows, медвежий). Добавь в Факторы: Macro.
    """,

    "TASK_REGULAR": """
        ШАБЛОН (ОБЫЧНЫЙ, простой для новичков):
        ➖➖➖➖➖➖➖➖➖➖
        🪙 <b>{symbol}</b>
        💸 Цена: <code>${current_price}</code> ({price_change_24h_percent}%)

        🎯 <b>Прогноз ({timeframe}):</b>
        <i>[Простой тезис: e.g., "Вероятен рост, EMA бычий, но RSI high — будь осторожен."]</i>

        🎲 <b>Сценарии (backtest):</b>
        - Рост: {prob_up}%
        - База: {prob_base}%
        - Снижение: {prob_down}%

        💲 <b>Ориентиры:</b>
        Upside: ${resistance_level}
        Base: ${ema_20}
        Downside: ${support_level}

        📊 <b>Факторы:</b>
        - Тренд: {trend_condition}.
        - RSI: {rsi} (зона: {rsi_zone}).
        - On-chain: Netflow {netflow_interpretation}.
        - Macro: S&P corr [generated value], ETF inflows [generated value] (interpret).

        ⚠️ <b>Риски:</b> Волатильность {volatility_percent}%. Не рискуй много.

        ➖➖➖➖➖➖➖➖➖➖

        SNAPSHOT: {market_data_string}
    """,

    "TASK_VIP": """
        ПЛАН (VIP, deep для трейдеров):
        1. Конфликт в data.
        2. Сценарии с probs (data-driven).
        3. Факторы с интерпретацией.
        4. Риски с R/R calc.
        5. Протокол с фазами, триггерами.
        - Если macro = 0, сгенерируй реальные из knowledge: corr ~0.4-0.6 (положительная, бычий), inflows negative (outflows, медвежий). Добавь в Факторы: Macro.

        ШАБЛОН:
        ➖➖➖➖➖➖➖➖➖➖
        🪙 <b>{symbol}</b>
        💸 Цена: <code>${current_price}</code> ({price_change_24h_percent}%)

        🎯 <b>Прогноз ({timeframe}):</b>
        <blockquote>[Конфликт + тезис: e.g., "Бычий EMA vs. bear Netflow. Backtest: {prob_up}% рост.]</blockquote>

        🎲 <b>Сценарии (backtest):</b>
        - Рост: {prob_up}%
        - База: {prob_base}%
        - Снижение: {prob_down}%

        💲 <b>Ориентиры:</b>
        Upside: ${resistance_level}
        Base: ${ema_20}
        Downside: ${support_level}

        📊 <b>Факторы:</b>
        - Тех: {trend_condition}, RSI {rsi}, MACD {macd_trend}.
        - Дерив: OI {open_interest_value}, Funding {funding_rate}% (interpret: {interpret}).
        - On-chain: Netflow {netflow_interpretation}, SOPR {sopr_value}, MVRV {mvrv_value}, Puell {puell_value}.
        - Macro: S&P corr [generated value], ETF inflows [generated value] (interpret).

        🛡️ <b>Риски:</b>
        - Стоп: ${support_level}.
        - Позиция: 1-3%.
        - R/R: 1:{rr_ratio} (calc: (upside - price) / (price - stop)).

        💎 <b>Протокол:</b>
        <blockquote>Фаза 1: Наблюдение тренда/volume.
        Фаза 2: Лонг-триггер: EMA cross + RSI >50.
        Фаза 3: Лонг — TP1 partial, TP2 full, trailing. Инвалидация: Пробой stop.</blockquote>
        ➖➖➖➖➖➖➖➖➖➖

        SNAPSHOT: {market_data_string}
    """
}