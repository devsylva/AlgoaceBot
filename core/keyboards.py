from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def get_main_menu():
    keyboard = [
        [
            InlineKeyboardButton("💰 Balance", callback_data="balance"),
            InlineKeyboardButton("📥 Deposit", callback_data="deposit")
        ],
        [
            InlineKeyboardButton("📤 Withdraw", callback_data="withdraw"),
            InlineKeyboardButton("📊 History", callback_data="history")
        ],
        [
            InlineKeyboardButton("👥 Copy Trading", callback_data="copy_trading"),
            InlineKeyboardButton("📈 My Trades", callback_data="my_trades")
        ],
        [
            InlineKeyboardButton("👥 Referral", callback_data="referral"),
            InlineKeyboardButton("❓ FAQ", callback_data="faq")
        ],
        [
            InlineKeyboardButton("📞 Support", callback_data="support")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)


def get_deposit_menu():
    keyboard = [
        [
            InlineKeyboardButton("Bitcoin (BTC)", callback_data="deposit_btc"),
            InlineKeyboardButton("USDT", callback_data="deposit_usdt")
        ],
        [
            InlineKeyboardButton("XRP", callback_data="deposit_xrp"),
            InlineKeyboardButton("Solana (SOL)", callback_data="deposit_sol")
        ],
        [InlineKeyboardButton("↩️ Back to Menu", callback_data="main_menu")]
    ]
    return InlineKeyboardMarkup(keyboard)