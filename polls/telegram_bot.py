from telegram import Bot
# Replace with your bot token and chat 
TELEGRAM_BOT_TOKEN = "7868091454:AAFCbhl9pf_81aZjWFGa4vENnF89pZL2MTo"
CHAT_ID = "8052136381"

async def send_order_notification(order):
    """
    Sends a notification to Telegram when a new order is created.
    """
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    message = (
        f"📦 *New Order Received!*\n\n"
        f"👤 Customer: {order.details}\n"
        f"📞 Phone: {order.phone_number}\n"
        f"🏠 Address: {order.address}\n"
        f"🛒 Items: {order.product}\n"
        f"📅 Date: {order.created_at.strftime('%Y-%m-%d %H:%M:%S')}"
    )

    try:
        bot.send_message(chat_id=CHAT_ID, text=message, parse_mode="Markdown")
    except Exception as e:
        print(f"Error sending Telegram message: {e}")
