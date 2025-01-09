from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, Bot
from telegram.ext import Application, CommandHandler, CallbackContext, CallbackQueryHandler, MessageHandler, filters, ContextTypes
from core.models import TelegramUser
import json
from .keyboards import get_main_menu, get_deposit_menu
from django.http import HttpResponse
from asgiref.sync import sync_to_async
from .utils import getDepositAddress

# Create your views here.
def landingPage(request):
    return render(request, 'landingpage.html')

# Create a single bot instance
bot = Bot(token=settings.TELEGRAM_TOKEN)

@sync_to_async
def create_or_update_user(user_id, username, first_name, last_name):
    """Async wrapper for database operations"""
    telegram_user, created = TelegramUser.objects.get_or_create(
        telegram_id=user_id,
        defaults={
            'username': username,
            'first_name': first_name,
            'last_name': last_name
        }
    )
    if not created:
        telegram_user.username = username
        telegram_user.first_name = first_name
        telegram_user.last_name = last_name
        telegram_user.save()
    return telegram_user

async def register_user(update: Update):
    """Register or update user"""
    user = update.effective_user
    return await create_or_update_user(
        user.id,
        user.username,
        user.first_name,
        user.last_name
    )

@sync_to_async
def get_user_balance(telegram_user):
    """Async wrapper for getting user balance"""
    # Refresh from database to get latest balance
    telegram_user.refresh_from_db()
    return telegram_user.balance

async def start(update: Update):
    try:
        # register user
        telegram_user = await register_user(update)

        welcome_text = (
            f"🌟 *Welcome to AlgoAce Trading Bot!* 🌟\n\n"
            f"Hello {update.effective_user.first_name}!\n\n"
            "🚀 *Your Gateway to Smart Crypto Trading* 🚀\n\n"
            "Choose from the options below to:\n"
            "• Check your balance\n"
            "• Make deposits/withdrawals\n"
            "• View transaction history\n"
            "• Start copy trading\n"
            "• Get support\n"
            "• Earn with referrals\n\n"
            f"Your Referral Code: `{telegram_user.referral_code}`\n\n"
            "🔐 *Safe & Secure Trading*\n"
            "📊 *Real-time Updates*\n"
            "💯 *24/7 Support*\n"
        )

        await update.message.reply_text(
            text=welcome_text,
            parse_mode='Markdown',
            reply_markup=get_main_menu()
        )
    except Exception as e:
        print(f"Error in start command: {e}")
        raise


async def handle_callback(update: Update):
    """Handle callback queries from inline keyboard"""
    query = update.callback_query
    await query.answer()  # Answer the callback query to remove loading state

    try:
        # Get or register user
        telegram_user = await register_user(update)

        if query.data == "balance":
            balance = await get_user_balance(telegram_user)
            text = f"💰 *Your Current Balance*\n\nAvailable: ${balance:.2f} USDT"
            await query.message.reply_text(text, parse_mode='Markdown')
        
        elif query.data == "deposit":
            # Add your deposit logic here
            text = "📥 *Deposit Methods*\n\nChoose your preferred deposit method:"
            # deposit_keyboard = [
            #     [InlineKeyboardButton("BTC", callback_data="deposit_btc"),
            #      InlineKeyboardButton("ETH", callback_data="deposit_eth")],
            #     [InlineKeyboardButton("USDT", callback_data="deposit_usdt"),
            #      InlineKeyboardButton("Back to Menu", callback_data="main_menu")]
            # ]
            await query.message.reply_text(
                text,
                parse_mode='Markdown',
                reply_markup=get_deposit_menu()
            )

        elif query.data == "main_menu":
            # Handle return to main menu
            await query.message.reply_text(
                "Main Menu",
                reply_markup=get_main_menu()
            )

        elif query.data == 'deposit_':
            crypto = query.data.split('_')[1]
            address_info = await getDepositAddress(crypto)

            if address_info:
                memo_text = f"\n📝 *Memo/Tag:* `{address_info['memo']}`" if address_info['memo'] else ""
                
                text = (
                    f"🏦 *Deposit {crypto}*\n\n"
                    f"💳 *Deposit Address:*\n`{address_info['address']}`"
                    f"{memo_text}\n\n"
                    f"🔄 *Network:* {address_info['network']}\n\n"
                    "⚠️ *Important Notes:*\n"
                    f"• Send only {crypto} to this address\n"
                    "• Deposits will be credited after confirmations\n"
                    "• Include memo/tag if provided\n\n"
                    "Need help? Contact support."
                )
                
                keyboard = [
                    [InlineKeyboardButton("↩️ Back to Deposit Options", callback_data="deposit")],
                    [InlineKeyboardButton("📞 Contact Support", callback_data="support")]
                ]
                
                await query.message.reply_text(
                    text,
                    parse_mode='Markdown',
                    reply_markup=InlineKeyboardMarkup(keyboard)
                )


            else:
                await query.message.reply_text(
                    "Sorry, deposit address not available. Please contact support.",
                    parse_mode='Markdown',
                    reply_markup=get_main_menu()
                )

        

    except Exception as e:
        print(f"Error in callback: {e}")
        await query.message.reply_text("Sorry, an error occurred. Please try again.")




@csrf_exempt
async def telegram_webhook(request):
    if request.method == 'POST':
        try:
            print("Received webhook request")  # Debug log
            update_data = json.loads(request.body.decode('utf-8'))
            print(f"Update data: {update_data}")  # Debug log
            
            # Create update object
            update = Update.de_json(update_data, bot)
            
            # Handle the update based on type
            if update.message and update.message.text == '/start':
                await start(update)
            elif update.callback_query:
                await handle_callback(update)
                
            return HttpResponse('OK')
        except Exception as e:
            print(f"Error processing update: {e}")
            return HttpResponse('Error processing update', status=500)
    return HttpResponse('Only POST requests are allowed')