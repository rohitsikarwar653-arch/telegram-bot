import random
import os
import threading
from flask import Flask

web_app = Flask(__name__)

@web_app.route("/")
def home():
    return "Telegram Bot is running!"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    web_app.run(host="0.0.0.0", port=port)
from telegram import Update
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

def main_menu():
    keyboard = [
        [
            InlineKeyboardButton("🤖 Help", callback_data="help"),
            InlineKeyboardButton("ℹ️ About", callback_data="about"),
        ],
        [
            InlineKeyboardButton("📩 Contact", callback_data="contact"),
            InlineKeyboardButton("🙏 Radhe Radhe", callback_data="radhe"),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)

def back_button():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🏠 Main Menu", callback_data="main_menu")]
    ])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🙏 Namaste!\n\n"
        "Main Shubham Help Bot hoon. 🤖\n"
        "Neeche menu se option choose kijiye 👇",
        reply_markup=main_menu(),
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 Help Menu\n\n"
        "/start - Main menu\n"
        "/help - Help menu\n"
        "/about - Bot ke baare mein\n"
        "/contact - Contact information",
        reply_markup=back_button(),
    )

async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "ℹ️ About\n\n"
        "Ye Shubham Help Bot hai. 🤖❤️\n"
        "Aap menu buttons ya commands ka use kar sakte hain.",
        reply_markup=back_button(),
    )

async def contact_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📩 Contact\n\n"
        "Aap yahin message bhejkar help le sakte hain. 😊",
        reply_markup=back_button(),
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "main_menu":
        await query.edit_message_text(
            "🙏 Main Menu\n\n"
            "Neeche se option choose kijiye 👇",
            reply_markup=main_menu(),
        )

    elif query.data == "help":
        await query.edit_message_text(
            "🤖 Help Menu\n\n"
            "/start - Main menu\n"
            "/help - Help menu\n"
            "/about - About\n"
            "/contact - Contact",
            reply_markup=back_button(),
        )

    elif query.data == "about":
        await query.edit_message_text(
            "ℹ️ About\n\n"
            "Ye Shubham Help Bot hai. 🤖❤️",
            reply_markup=back_button(),
        )

    elif query.data == "contact":
        await query.edit_message_text(
            "📩 Contact\n\n"
            "Aap yahin message bhejkar help le sakte hain. 😊",
            reply_markup=back_button(),
        )

    elif query.data == "radhe":
        await query.edit_message_text(
            "🙏 Radhe Radhe ❤️",
            reply_markup=back_button(),
        )

async def auto_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower().strip()
    if text.startswith("mera naam ") and text.endswith(" hai") and text not in ("mera naam kya hai", "mera naam kya hai?"):
        name = text[9:-4].strip().title()
        if name:
            context.user_data["name"] = name
            await update.message.reply_text(
                f"Achha {name} 😊❤️ Ab mujhe aapka naam yaad rahega!"
            )
            return

    if text in ("hi", "hello", "hey"):
        replies = [
            "Hey 😊❤️ Kaise ho?",
            "Hello 👋😄 Kya haal hai?",
            "Hi 😊 Main yahin hoon.",
            "Heyy 😎❤️ Batao kya chal raha hai?",
            "Hello ji 😊 Aapse baat karke achha laga ❤️"
        ]
        await update.message.reply_text(random.choice(replies))

    elif text in ("namaste", "namaskar"):
        await update.message.reply_text(
            "🙏 Namaste!\nShubham Help Bot me aapka swagat hai."
        )

    elif text in ("radhe radhe", "radhey radhey"):
        await update.message.reply_text("Radhe Radhe 🙏❤️")

    elif any(x in text for x in ("kya kar rahe ho", "kya kr rahe ho", "kya kar rhe ho")):
        replies = [
            "Bas aapse baat kar raha hoon 😄❤️",
            "Kuch khaas nahi, aapka message dekh raha hoon 😊",
            "Bas yahin hoon, aapse chatting kar raha hoon ❤️",
            "Aapka reply dene mein busy hoon 🤖❤️",
            "Bas aaram se hoon 😄 Aap batao?",
            "Aapse baat karna hi sabse achha kaam hai 😊❤️"
        ]
        await update.message.reply_text(random.choice(replies))

    elif "kaise ho" in text:
        name = context.user_data.get("name")
        if name:
            replies = [
                f"Main bilkul badhiya hoon 😊❤️ Aap batao, {name}?",
                f"Ekदम mast hoon 😄 {name}, aap kaise ho?",
                f"Bilkul fine! 😎 Aapka kya haal hai, {name}?",
                f"Main badhiya hoon ❤️ Aapse baat karke aur bhi achha lag raha hai, {name}.",
                f"Mast chal raha hai 😄 Aap sunao, {name}?"
            ]
        else:
            replies = [
                "Main bilkul badhiya hoon 😊 Aap batao?",
                "Ekदम mast hoon 😄❤️ Aap kaise ho?",
                "Bilkul fine! 😎 Aapka kya haal hai?"
            ]
        await update.message.reply_text(random.choice(replies))

    elif "kahan ho" in text:
        await update.message.reply_text("Yahin hoon 😎 Aapse baat kar raha hoon.")
    elif text in ("haan", "ha", "yes", "ok", "okay"):
        replies = [
            "Haan ji 😊❤️",
            "Bilkul 😄",
            "Okay 👍❤️",
            "Ji haan 😎"
        ]
        await update.message.reply_text(random.choice(replies))

    elif text in ("nahi", "na", "no"):
        replies = [
            "Achha 😄",
            "Koi baat nahi ❤️",
            "Theek hai 😊",
            "Okay, samajh gaya 👍"
        ]
        await update.message.reply_text(random.choice(replies))

    elif text in ("lol", "haha", "hahaha"):
        replies = [
            "😂😂 Hahaha!",
            "Haha 😄❤️",
            "Aap bhi na 😂"
        ]
        await update.message.reply_text(random.choice(replies))

    elif text in ("ok", "okay"):
        await update.message.reply_text("Okay 😊👍")
        await update.message.reply_text(
            "Yahin hoon 😎 Aapse baat kar raha hoon."
        )

    elif "good morning" in text:
        replies = [
            "Good Morning 🌅❤️ Aapka din bahut achha ho!",
            "Good Morning 😊🌸 Hope aapka din shandaar rahe!",
            "Good Morning ☀️❤️ Aaj ka din aapke liye special ho!",
            "Suprabhat 🌅😊 Hamesha khush rahiye!",
            "Good Morning 😄❤️ Aaj kya plan hai?"
        ]
        await update.message.reply_text(random.choice(replies))

    elif "good night" in text:
        replies = [
            "Good Night 🌙❤️ Sweet dreams!",
            "Good Night 😊🌙 Achhi neend aaye!",
            "Shubh Ratri 🌙❤️ Kal ka din aur bhi achha ho!",
            "Good Night 😴✨ Take care and sleep well!",
            "Sweet dreams 🌙😊 Kal phir baat karenge!"
        ]
        await update.message.reply_text(random.choice(replies))

    elif text in ("bye", "goodbye"):
        await update.message.reply_text(
            "Bye 👋❤️ Phir milte hain!"
        )
    elif "thank" in text or "thanks" in text:
        await update.message.reply_text(
            "You're most welcome 😊❤️"
        )

    elif "kya haal hai" in text:
        await update.message.reply_text(
            "Bilkul badhiya 😄 Aapka kya haal hai?"
        )

    elif "kya chal raha hai" in text:
        await update.message.reply_text(
            "Bas sab badhiya chal raha hai 😎❤️"
        )

    elif "mera naam kya hai" in text or "mujhe mera naam batao" in text:
        name = context.user_data.get("name")
        if name:
            await update.message.reply_text(f"Aapka naam {name} hai 😊❤️")
        else:
            await update.message.reply_text("Aapne abhi mujhe apna naam nahi bataya 😊")

    elif "tumhara naam kya hai" in text or "aapka naam kya hai" in text:
        await update.message.reply_text(
            "Mera naam Shubham Help Bot hai 🤖❤️"
        )

    elif "tum kaun ho" in text or "aap kaun ho" in text:
        await update.message.reply_text(
            "Main Shubham Help Bot hoon 🤖😊"
        )

    elif "miss you" in text:
        await update.message.reply_text(
            "Aww 😊❤️ Main yahin hoon!"
        )
    elif any(x in text for x in ("khana kha liya", "khana khaya", "khaana kha liya", "khaana khaya")):
        await update.message.reply_text(random.choice(["Haan ji 😄 Aapne kha liya?", "Haan 😊 Khana kha liya. Aapne?", "Ji haan ❤️ Aapne khana khaya?"]))

    elif any(x in text for x in ("shubham kaha hai", "shubham kahan hai", "shubham kaha par hai", "shubham kahan par hai")):
        await update.message.reply_text(random.choice(["Shubham yahin hai 😊", "Shubham abhi yahin hai 😄", "Yahin hai ❤️ Aapse baat kar raha hai."]))

    elif any(x in text for x in ("kya hua", "kya hua hai")):
        await update.message.reply_text(random.choice(["Kuch nahi 😊 Sab badhiya hai.", "Kuch khaas nahi 😄", "Sab theek hai ❤️"]))

    elif any(x in text for x in ("kahan ja rahe ho", "kaha ja rahe ho")):
        await update.message.reply_text(random.choice(["Abhi kahin nahi 😄", "Bas thoda bahar ja raha hoon 😊", "Abhi yahin hoon ❤️"]))

    else:
        replies = [
            "Hmm 😊 Iske baare mein thoda aur batao.",
            "Achha 😄 Phir aage batao...",
            "Samajh raha hoon 😊",
            "Ohh 😎 Interesting!",
            "Haha 😄 Aapki baat interesting hai ❤️"
        ]
        await update.message.reply_text(random.choice(replies))
def main():
    app = Application.builder().token(os.environ["BOT_TOKEN"]).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("about", about_command))
    app.add_handler(CommandHandler("contact", contact_command))

    app.add_handler(CallbackQueryHandler(button_handler))

    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, auto_reply)
    )
    
    threading.Thread(target=run_web, daemon=True).start()
    print("Bot started...")
    app.run_polling()

if __name__ == "__main__":
    main()
