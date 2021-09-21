from pyrogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton

gerador = ReplyKeyboardMarkup([['♻️ Gerar Sinais', '🟢 Sinais 24h', '✅ Check Sinais'],
                               ['🏄🏼‍♂️ Tendência', '🧙🏼‍♂️ Perfil', '🧹 Limpar Sinais']], resize_keyboard = True)

menu_ativos = ReplyKeyboardMarkup(
    [['🚀 Normal', '⚔️ OTC'],
     ['🏠 Menu']], 
    resize_keyboard = True, one_time_keyboard = True)

info = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton('📖 Info', callback_data='InfoVIP')
        ]
    ])

comunidade = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton('⚙️ Configurações', callback_data='configs')
        ]
    ])

sub_configs = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton('⬅️ Voltar', callback_data='back-configs'),
            InlineKeyboardButton('📣 Notícias', callback_data='noticias-configs')
        ]
    ])

volatividade = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton('⭐️', callback_data='volat-1-configs'),
            InlineKeyboardButton('⭐️⭐️', callback_data='volat-2-configs'),
            InlineKeyboardButton('⭐️⭐️⭐️', callback_data='volat-3-configs')
        ]
    ])

dif_noticia = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton('3 min', callback_data='3-min-configs'),
            InlineKeyboardButton('5 min', callback_data='5-min-configs'),
            InlineKeyboardButton('10 min', callback_data='10-min-configs')
        ],
        [
            InlineKeyboardButton('15 min', callback_data='15-min-configs'),
            InlineKeyboardButton('30 min', callback_data='30-min-configs'),
        ]
    ])


choose_moeda = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton('1ª moeda', callback_data='moeda-1-configs'),
            InlineKeyboardButton('2ª moeda', callback_data='moeda-2-configs')
        ]
    ])


OFF = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton('🚫 Desligar', callback_data='ao_vivo_OFF')
        ]
    ])

ON = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton('✅ Ligar', callback_data='ao_vivo_ON')
        ]
    ])

timeframe_menu = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton('M1', callback_data='tf-1'),
            InlineKeyboardButton('M5', callback_data='tf-5')
        ],
        [
            InlineKeyboardButton('M15', callback_data='tf-15'),
            InlineKeyboardButton('M30', callback_data='tf-30')
        ]
    ])

payout_menu = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton('70%', callback_data='pay-70'),
            InlineKeyboardButton('80%', callback_data='pay-80')
        ],
        [
            InlineKeyboardButton('90%', callback_data='pay-90'),
            InlineKeyboardButton('100%', callback_data='pay-100')
        ],
        [
            InlineKeyboardButton('100% ~ 100%', callback_data='pay-200')
        ]
    ])

m1_ON = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton('✅ M1', callback_data='m1_vivo_ON'),
            InlineKeyboardButton('M5', callback_data='m5_vivo_ON')
        ],
        [
            InlineKeyboardButton('Desativado', callback_data='ao_vivo_OFF')
        ]
    ])

m5_ON = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton('M1', callback_data='m1_vivo_ON'),
            InlineKeyboardButton('✅ M5', callback_data='m5_vivo_ON')
        ],
        [
            InlineKeyboardButton('Desativado', callback_data='ao_vivo_OFF')
        ]
    ])
      
ao_vivo_OFF = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton('M1', callback_data='m1_vivo_ON'),
            InlineKeyboardButton('M5', callback_data='m5_vivo_ON')
        ],
        [
            InlineKeyboardButton('✅ Desativado', callback_data='ao_vivo_OFF')
        ]
    ])

analise_menu = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton('Parcial', callback_data='#parcial'),
            InlineKeyboardButton('Completa', callback_data='#completa'),
            InlineKeyboardButton('Lista G1', callback_data='#lista')
        ]
    ])

direcao_menu = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton('CALL', callback_data='alta='),
            InlineKeyboardButton('PUT', callback_data='baixa=')
        ]
    ])

cont_dias = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton('1 dia', callback_data='1-d'),
            InlineKeyboardButton('2 dias', callback_data='2-d'),
            InlineKeyboardButton('3 dias', callback_data='3-d'),
            InlineKeyboardButton('4 dias', callback_data='4-d'),
            InlineKeyboardButton('5 dias', callback_data='5-d')
        ],
        [
            InlineKeyboardButton('6 dias', callback_data='6-d'),
            InlineKeyboardButton('7 dias', callback_data='7-d'),
            InlineKeyboardButton('8 dias', callback_data='8-d'),
            InlineKeyboardButton('9 dias', callback_data='9-d'),
            InlineKeyboardButton('10 dias', callback_data='10-d')
        ],
        [
        
            InlineKeyboardButton('Padrão', callback_data='default-d')
        ]
    ])

horario_menu = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton('0-1h', callback_data='0'),
            InlineKeyboardButton('1-2h', callback_data='1'),
            InlineKeyboardButton('2-3h', callback_data='2'),
            InlineKeyboardButton('3-4h', callback_data='3'),
            InlineKeyboardButton('4-5h', callback_data='4')
        ],
        
        [
            InlineKeyboardButton('5-6h', callback_data='5'),
            InlineKeyboardButton('6-7h', callback_data='6'),
            InlineKeyboardButton('7-8h', callback_data='7'),
            InlineKeyboardButton('8-9h', callback_data='8'),
            InlineKeyboardButton('9-10h', callback_data='9')
        ],
        
        [
            InlineKeyboardButton('11-12h', callback_data='11'),
            InlineKeyboardButton('12-13h', callback_data='12'),
            InlineKeyboardButton('13-14h', callback_data='13'),
            InlineKeyboardButton('14-15h', callback_data='14'),
            InlineKeyboardButton('15-16h', callback_data='15')
        ],
        [
            InlineKeyboardButton('16-17h', callback_data='16'),
            InlineKeyboardButton('17-18h', callback_data='17'),
            InlineKeyboardButton('18-19h', callback_data='18'),
            InlineKeyboardButton('19-20h', callback_data='19'),
            InlineKeyboardButton('20-21h', callback_data='20')
        ],
        [
            InlineKeyboardButton('21-22h', callback_data='21'),
            InlineKeyboardButton('22-23h', callback_data='22'),
            InlineKeyboardButton('23-0h', callback_data='23')
        ]
    ])

inline_OTC = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton('EUR/USD (OTC)', callback_data='EURUSD-OTC'),
            InlineKeyboardButton('EUR/GBP (OTC)', callback_data='EURGBP-OTC'),
        ],
        
        [
            InlineKeyboardButton('USD/CHF (OTC)', callback_data='USDCHF-OTC'),
            InlineKeyboardButton('GBP/USD (OTC)', callback_data='GBPUSD-OTC')
        ],
        
        [
            InlineKeyboardButton('GBP/JPY (OTC)', callback_data='GBPJPY-OTC'),
            InlineKeyboardButton('AUD/CAD (OTC)', callback_data='AUDCAD-OTC')
        ],
        
        [
            InlineKeyboardButton('EUR/JPY (OTC)', callback_data='EURJPY-OTC'),
            InlineKeyboardButton('NZD/USD (OTC)', callback_data='NZDUSD-OTC')
        ],
        
        [
            InlineKeyboardButton('USD/JPY (OTC)', callback_data='USDJPY-OTC')
        ]
    ])

inline_NORMAL = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton('EUR/USD', callback_data='EURUSD'),
            InlineKeyboardButton('EUR/GBP', callback_data='EURGBP'),
            InlineKeyboardButton('EUR/AUD', callback_data='EURAUD'),
            InlineKeyboardButton('AUD/NZD', callback_data='AUDNZD'),
            InlineKeyboardButton('USD/NOK', callback_data='USDNOK')
        ],
        
        [
            InlineKeyboardButton('USD/CHF', callback_data='USDCHF'),
            InlineKeyboardButton('GBP/USD', callback_data='GBPUSD'),
            InlineKeyboardButton('AUD/USD', callback_data='AUDUSD'),
            InlineKeyboardButton('USD/CAD', callback_data='USDCAD'),
            InlineKeyboardButton('EUR/CAD', callback_data='EURCAD')
        ],
        
        [
            InlineKeyboardButton('GBP/JPY', callback_data='GBPJPY'),
            InlineKeyboardButton('AUD/CAD', callback_data='AUDCAD'),
            InlineKeyboardButton('EUR/NZD', callback_data='EURNZD'),
            InlineKeyboardButton('GBP/NZD', callback_data='GBPNZD'),
            InlineKeyboardButton('GBP/CAD', callback_data='GBPCAD')
        ],
        
        [
            InlineKeyboardButton('EUR/JPY', callback_data='EURJPY'),
            InlineKeyboardButton('NZD/USD', callback_data='NZDUSD'),
            InlineKeyboardButton('AUD/JPY', callback_data='AUDJPY'),
            InlineKeyboardButton('GBP/CHF', callback_data='GBPCHF'),
            InlineKeyboardButton('CAD/JPY', callback_data='CADJPY')
        ],
        
        [
            InlineKeyboardButton('USD/JPY', callback_data='USDJPY'),
            InlineKeyboardButton('AUD/CHF', callback_data='AUDCHF'),
            InlineKeyboardButton('CAD/CHF', callback_data='CADCHF'),
            InlineKeyboardButton('GBP/AUD', callback_data='GBPAUD'),
            InlineKeyboardButton('CHF/JPY', callback_data='CHFJPY')
        ]
    ])



inline_TENDENCIA = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton('EUR/USD', callback_data='+EURUSD'),
            InlineKeyboardButton('EUR/GBP', callback_data='+EURGBP'),
            InlineKeyboardButton('EUR/AUD', callback_data='+EURAUD'),
            InlineKeyboardButton('AUD/NZD', callback_data='+AUDNZD'),
            InlineKeyboardButton('USD/NOK', callback_data='+USDNOK')
        ],
        
        [
            InlineKeyboardButton('USD/CHF', callback_data='+USDCHF'),
            InlineKeyboardButton('GBP/USD', callback_data='+GBPUSD'),
            InlineKeyboardButton('AUD/USD', callback_data='+AUDUSD'),
            InlineKeyboardButton('USD/CAD', callback_data='+USDCAD'),
            InlineKeyboardButton('EUR/CAD', callback_data='+EURCAD')
        ],
        
        [
            InlineKeyboardButton('GBP/JPY', callback_data='+GBPJPY'),
            InlineKeyboardButton('AUD/CAD', callback_data='+AUDCAD'),
            InlineKeyboardButton('EUR/NZD', callback_data='+EURNZD'),
            InlineKeyboardButton('GBP/NZD', callback_data='+GBPNZD'),
            InlineKeyboardButton('GBP/CAD', callback_data='+GBPCAD')
        ],
        
        [
            InlineKeyboardButton('EUR/JPY', callback_data='+EURJPY'),
            InlineKeyboardButton('NZD/USD', callback_data='+NZDUSD'),
            InlineKeyboardButton('AUD/JPY', callback_data='+AUDJPY'),
            InlineKeyboardButton('GBP/CHF', callback_data='+GBPCHF'),
            InlineKeyboardButton('CAD/JPY', callback_data='+CADJPY')
        ],
        
        [
            InlineKeyboardButton('USD/JPY', callback_data='+USDJPY'),
            InlineKeyboardButton('AUD/CHF', callback_data='+AUDCHF'),
            InlineKeyboardButton('CAD/CHF', callback_data='+CADCHF'),
            InlineKeyboardButton('GBP/AUD', callback_data='+GBPAUD'),
            InlineKeyboardButton('CHF/JPY', callback_data='+CHFJPY')
        ]
    ])

