import random
import os
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

    if any(x in text for x in ("hello", "hi", "hii", "hey", "namaste", "नमस्ते")):
        await update.message.reply_text(
            random.choice([
                "Hello 😊❤️ Kaise ho?",
                "Hii 😄❤️ Kya haal hai?",
                "Hey 😊 Main yahin hoon!"
            ])
        )

    elif "kaise ho" in text or "kaisa ho" in text:
        await update.message.reply_text(
            random.choice([
                "Main bilkul badhiya hoon 😊❤️ Aap kaise ho?",
                "Sab badhiya 😄 Aap batao?",
                "Main theek hoon 🤖❤️"
            ])
        )

    elif any(x in text for x in ("kya kar rahe ho", "kya kr rahe ho", "kya kar rhe ho")):
        await update.message.reply_text(
            random.choice([
                "Bas aapse baat kar raha hoon 😄❤️",
                "Abhi yahin hoon 😊 Aapse chat kar raha hoon.",
                "Bas online hoon 🤖😎"
            ])
        )

    elif "tumhara naam kya hai" in text or "aapka naam kya hai" in text:
        await update.message.reply_text(
            "Mera naam Shubham Help Bot hai 🤖❤️"
        )

    elif "tum kaun ho" in text or "aap kaun ho" in text:
        await update.message.reply_text(
            "Main Shubham Help Bot hoon 🤖😊"
        )

    elif "miss you" in text or "miss u" in text:
        await update.message.reply_text(
            "Aww 😊❤️ Main yahin hoon!"
        )

    elif any(x in text for x in (
        "khana kha liya", "khana khaya",
        "khaana kha liya", "khaana khaya"
    )):
        await update.message.reply_text(
            random.choice([
                "Haan ji 😄 Aapne kha liya?",
                "Haan 😊 Khana kha liya. Aapne?",
                "Ji haan ❤️ Aapne khana khaya?"
            ])
        )

    elif any(x in text for x in (
        "shubham kaha hai", "shubham kahan hai",
        "shubham kaha par hai", "shubham kahan par hai"
    )):
        await update.message.reply_text(
            random.choice([
                "Shubham yahin hai 😊",
                "Shubham abhi yahin hai 😄",
                "Yahin hai ❤️ Aapse baat kar raha hai."
            ])
        )

    elif "kya hua" in text or "kya hua hai" in text:
        await update.message.reply_text(
            random.choice([
                "Kuch nahi 😊 Sab badhiya hai.",
                "Kuch khaas nahi 😄",
                "Sab theek hai ❤️"
            ])
        )

    elif "kahan ja rahe ho" in text or "kaha ja rahe ho" in text:
        await update.message.reply_text(
            random.choice([
                "Abhi kahin nahi 😄",
                "Bas thoda bahar ja raha hoon 😊",
                "Abhi yahin hoon ❤️"
            ])
        )

    elif any(x in text for x in ("thank you", "thanks", "dhanyawad", "shukriya")):
        await update.message.reply_text(
            random.choice([
                "You're welcome 😊❤️",
                "Koi baat nahi 😄",
                "Hamesha 😊❤️"
            ])
        )

    elif "good morning" in text or "suprabhat" in text:
        await update.message.reply_text(
            "Good Morning 🌅😊❤️ Aapka din bahut achha rahe!"
        )

    elif "good night" in text or "shubh ratri" in text:
        await update.message.reply_text(
            "Good Night 🌙😴❤️ Sweet dreams!"
        )

    elif any(x in text for x in ("haha", "hahaha", "lol")):
        await update.message.reply_text(
            random.choice([
                "Haha 😄😂",
                "😂😂 Bahut funny!",
                "Hehe 😄❤️"
            ])
        )

    elif any(x in text for x in ("bye", "goodbye", "see you")):
        await update.message.reply_text(
            random.choice([
                "Bye 😊❤️ Phir milte hain!",
                "Okay 😄 Take care!",
                "See you soon 🤖❤️"
            ])
        )

    else:
        replies = [
            "Achha 😊 Phir batao...",
            "Hmm 😄 Samajh raha hoon.",
            "Ohh 😎 Interesting!",
            "Achha ji ❤️ Aage batao.",
            "Haan 😊 Main sun raha hoon."
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
    print("Bot started...")
    app.run_polling()

if __name__ == "__main__":
    main()
