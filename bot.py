import random
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.environ["BOT_TOKEN"]
ADMIN_ID =6222405805

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Namaste! 👋 Main Shubham Help Bot hoon."
    )
async def myid(update: Update, context):
    await update.message.reply_text(f"Your Chat ID is: {update.effective_chat.id}")
  

async def manual_reply(update: Update, context):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("⛔ Ye command sirf admin ke liye hai.")
        return

    if len(context.args) < 2:
        await update.message.reply_text(
            "Use: /reply USER_ID message"
        )
        return

    try:
        user_id = int(context.args[0])
        text = " ".join(context.args[1:])

        await context.bot.send_message(
            chat_id=user_id,
            text=text
        )

        await update.message.reply_text("✅ Reply send ho gaya.")

    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")

async def help_command(update: Update, context):
    await update.message.reply_text(
        "Commands:\n"
        "/start - Bot start kare\n"
        "/help - Help dekhein"
    )


async def auto_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
            return
    msg = update.message.text.lower()

    if "hello" in msg or "hi" in msg:
        reply = "Namaste! 👋 Kaise hain aap?"
    elif "kaise ho" in msg or "kese ho" in msg or "kya haal hai" in msg or "how are you" in msg:
        reply = random.choice([
    "Main bilkul badhiya hoon 😊",
    "Ekdam mast 😄 Aap batao?",
    "Sab badhiya ❤️ Aap kaise ho?",
    "Main theek hoon 😊 Aap sunaiye?"
])
   
    elif (
    "shubham kaha hai" in msg
    or "shubham kahan hai" in msg
    or "shubham kaha par hai" in msg
    or "shubham kahan par hai "in msg
):   
        reply = "Shubham abhi busy hai 😊"
    elif "naam" in msg:
        reply = "Mera naam Shubham Help Bot hai 🤖"
    elif "help" in msg:
        reply = "Ji 😊 Bataiye, main aapki kya help karun?"
    elif "thank" in msg:
        reply = "Aapka swagat hai ❤️"
    elif (
    "kya kar rahe ho" in msg
    or "kya kr rahe ho" in msg
    or "kya kar rhe ho" in msg
    or "kya kr rhe ho" in msg
    ):
            reply = random.choice([
        "Bas aapse baat kar raha hoon 😊",
        "Kuch khaas nahi 😄 Aap kya kar rahe ho?",
        "Aapke message ka wait kar raha tha 😁",
        "Bas time pass 😎 Aap sunao?"
    ])

   
    elif "aur batao" in msg or "kya chal raha hai" in msg or "what's up" in msg or "whats up" in msg:
           reply = random.choice([
        "Bas badhiya 😊 Aap batao?",
        "Sab mast chal raha hai 😄 Aap sunaiye?",
        "Kuch khaas nahi 😊 Aapse baat kar raha hoon.",
        "Sab first class 😎 Aapke kya haal hain?"
    ])
    elif "good morning" in msg:
        reply = "Good morning ☀️ Aapka din shubh ho 😊"
        

    elif "good night" in msg:
        reply = "Good night 🌙 Sweet dreams!"

    elif "kahan ho" in msg:
        reply = "Main yahin hoon, aapke Telegram bot mein 🤖"

    elif "khana kha liya" in msg:
        reply = "Haan 😊 Aapne khana kha liya?"

    elif "kya hua" in msg:
        reply = "Kuch nahi 😊 Aap bataiye kya hua?"

    elif "busy ho" in msg:
        reply = "Nahi 😊 Aapke liye available hoon."

    elif "good afternoon" in msg:
        reply = "Good afternoon ☀️ Aapka din accha ja raha ho!"

    elif "good evening" in msg:
        reply = "Good evening 🌆 Kaise hain aap?"


    elif "dost banoge" in msg or "dost bnoge" in msg or "dost banoge kya" in msg:
        reply = "Bilkul 😊 Hum dost hain."

    elif "miss you" in msg:
        reply = "Aww 😊 Main yahin hoon."

    elif "sorry" in msg:
        reply = "Koi baat nahi 😊"

    elif "kaun ho" in msg:
        reply = "Main Shubham Help Bot hoon 🤖"

    elif "kya haal hai" in msg:
        reply = "Sab badhiya hai 😊 Aap bataiye?"

    elif "love you" in msg:
        reply = "Aap bahut sweet hain 😊❤️"
    elif "bye" in msg:
        reply = "Bye 👋 Phir milte hain!"
    elif "kon ho" in msg:
      reply = "Main Shubham Help Bot hoon 🤖"

    elif "thank" in msg or "thanks" in msg:
        reply = "Aapka swagat hai 😊❤️"

    elif "good morning" in msg:
        reply = "Good morning! ☀️ Aapka din shubh ho 😊"

    elif "good night" in msg:
        reply = "Good night! 🌙 Sweet dreams 😊"
   

    elif "kya kar rahe ho" in msg:
        reply = "Bas aapse baat kar raha hoon 😊"

    elif "naam kya hai" in msg or "aapka naam" in msg:
        reply = "Mera naam Shubham Help Bot hai 🤖"

    elif "kaise ho" in msg:
        reply = "Main bilkul badhiya hoon 😊 Aap kaise hain?"

    elif "welcome" in msg:
        reply = "Thank you 😊❤️"

    elif "ok" in msg or "okay" in msg:
        reply = "Ji bilkul 😊"
    elif "radhe radhe" in msg:
        reply = "Radhe Radhe 🙏❤️"

    elif "good afternoon" in msg:
        reply = "Good afternoon ☀️ Kaise hain aap?"

    elif "good evening" in msg:
        reply = "Good evening 🌆 Aapka din kaisa raha?"

    elif "kaha ho" in msg or "kahan ho" in msg:
        reply = "Main yahin hoon 😊"

    elif "kya hua" in msg:
        reply = "Kuch nahi 😊 Aap bataiye kya hua?"
    elif "busy ho" in msg:
        reply = "Nahi 😊 Aap bataiye."

    elif "khana kha liya" in msg or "khana khaya" in msg:
        reply = "Haan 😊 Aapne khana kha liya?"

    elif "miss you" in msg:
        reply = "Aww 😊 Main yahin hoon."

    elif "dost banoge" in msg or "friend banoge" in msg:
        reply = "Bilkul 😊 Hum dost hain."

    elif "sorry" in msg:
        reply = "Koi baat nahi 😊"
    else:
        reply = "Hmm 😊 Main is message ko abhi samajh nahi paya. Aap thoda simple likhiye."

    await update.message.reply_text(reply)
    user = update.effective_user

    if user.id != ADMIN_ID:
        username = f"@{user.username}" if user.username else "No username"

        notify_text = (
            f"📩 New message\n"
            f"Name: {user.full_name}\n"
            f"User ID: {user.id}\n"
            f"Username: {username}\n"
            f"Message: {update.message.text}\n"
            f"Bot reply: {reply}"
        )

        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=notify_text
        )

app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help_command))
app.add_handler(CommandHandler("myid", myid))
app.add_handler(CommandHandler("reply", manual_reply))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, auto_reply))

print("Bot started...")
app.run_polling()
