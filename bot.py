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
    user = update.effective_user
    name = user.first_name or "Friend"

    keyboard = [
        [
            InlineKeyboardButton("👤 Profile", callback_data="menu_profile"),
            InlineKeyboardButton("📊 Stats", callback_data="menu_stats"),
        ],
        [
            InlineKeyboardButton("📋 Help", callback_data="menu_help"),
            InlineKeyboardButton("ℹ️ About", callback_data="menu_about"),
        ],
        [
            InlineKeyboardButton("📩 Contact Owner", callback_data="menu_contact"),
        ],
    ]

    await send_reply(update, 
        f"👋 Welcome {name}! ❤️\n\n"
        "🤖 Welcome to Shubham Help Bot!\n\n"
        "💬 Aap mujhse normally baat kar sakte hain.\n"
        "📋 Neeche menu se koi bhi option choose kijiye. ✨",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton("👤 Profile", callback_data="menu_profile"),
            InlineKeyboardButton("📊 Stats", callback_data="menu_stats"),
        ],
        [
            InlineKeyboardButton("📋 Commands", callback_data="menu_commands"),
            InlineKeyboardButton("📩 Contact Owner", callback_data="menu_contact"),
        ],
    ]

    await send_reply(update, 
        "🤖 Help Menu\n\n"
        "Neeche se option choose kijiye ❤️",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_reply(update, 
        "ℹ️ About Shubham Help Bot\n\n"
        "🤖 Name: Shubham Help Bot\n"
        "✨ Version: 2.0\n\n"
        "🚀 Features:\n"
        "• Smart & natural replies 💬\n"
        "• Custom personality 😎\n"
        "• Conversation context 🧠\n"
        "• User profiles 👤\n"
        "• Message notifications 🔔\n"
        "• Owner reply system ↩️\n"
        "• Broadcast 📢\n"
        "• User management 🔒\n"
        "• Interactive menu 📋\n\n"
        "👤 Owner: @MR_ALONE141\n\n"
        "❤️ Made with Python & Telegram"
    )

async def contact_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_reply(update, 
        "📩 Contact\n\n"
        "Aap yahin message bhejkar help le sakte hain. 😊",
        reply_markup=back_button(),
    )

async def owner_reply_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if update.effective_user.id != 6222405805:
        return

    if query.data.startswith("reply_"):
        user_id = int(query.data.split("_", 1)[1])
        context.user_data["reply_to_user"] = user_id

        await query.message.reply_text(
            "✍️ Ab apna reply message bhejiye.\n"
            "Main use selected user ko send kar dunga."
        )


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "menu_help":
        await query.message.reply_text(
            "📋 Help\n\n"
            "/start - Main menu\n"
            "/help - Help menu\n"
            "/profile - Your profile\n"
            "/about - About bot"
        )
        return

    if query.data == "menu_about":
        await query.message.reply_text(
            "ℹ️ Shubham Help Bot\n\n"
            "✨ Version: 2.0\n"
            "👤 Owner: @MR_ALONE141\n\n"
            "❤️ Made with Python & Telegram"
        )
        return

    if query.data == "menu_profile":
        profiles = context.application.bot_data.setdefault("profiles", {})
        user = update.effective_user
        profile = profiles.get(user.id)

        if not profile:
            profile = {
                "name": user.full_name,
                "username": user.username,
                "messages": 0,
            }
            profiles[user.id] = profile

        username = (
            f"@{profile['username']}"
            if profile.get("username")
            else "No username"
        )

        await query.message.reply_text(
            "👤 Your Profile\n\n"
            f"📝 Name: {profile['name']}\n"
            f"📱 Username: {username}\n"
            f"📝 Bio: {profile.get('bio', 'No bio set')}\n"
            f"🆔 ID: {user.id}\n"
            f"📩 Messages: {profile.get('messages', 0)}"
        )
        return

    if query.data == "menu_stats":
        stats = context.application.bot_data.get(
            "stats", {"messages": 0, "users": set()}
        )
        await query.message.reply_text(
            "📊 Bot Statistics\n\n"
            f"📩 Total Messages: {stats['messages']}\n"
            f"👥 Unique Users: {len(stats['users'])}\n"
            "🟢 Status: Online"
        )
        return

    if query.data == "menu_commands":
        await query.message.reply_text(
            "📋 Commands\n\n"
            "/start - Start bot\n"
            "/help - Open menu\n"
            "/menu - Open menu\n"
            "/profile - Your profile"
        )
        return

    if query.data == "menu_contact":
        await query.message.reply_text(
            "📩 Contact Owner\n\n"
            "👤 Owner: @MR_ALONE141\n"
            "💬 Aap owner ko Telegram par contact kar sakte hain."
        )
        return


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

async def owner_message_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != 6222405805:
        return False

    target = context.user_data.get("reply_to_user")
    if not target:
        return False

    try:
        await context.bot.send_message(
            chat_id=target,
            text=update.message.text
        )
        await send_reply(update, "✅ Reply send ho gaya.")
        context.user_data.pop("reply_to_user", None)
    except Exception as e:
        await send_reply(update, f"❌ Reply send nahi ho paya: {e}")

    return True


async def send_reply(update: Update, text: str, delay: float = 0.7, **kwargs):
    try:
        await update.message.chat.send_action("typing")
    except Exception:
        pass

    if delay > 0:
        import asyncio
        await asyncio.sleep(delay)

    await update.message.reply_text(text, **kwargs)

async def auto_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    import random

    if not update.message or not update.message.text:
        return

    text = update.message.text.lower().strip()
    name = context.user_data.get("name")

    # Naam save karna
    if text.startswith("mera naam ") and text.endswith(" hai") and text not in ("mera naam kya hai",):
        name = text[9:-4].strip().title()
        if name:
            context.user_data["name"] = name
            await send_reply(update, f"Achha {name} 😊❤️ Aapse milkar achha laga!")
            return

    if text.startswith("my name is "):
        name = text[11:].strip().title()
        if name:
            context.user_data["name"] = name
            await send_reply(update, f"Nice to meet you, {name} 😊❤️")
            return

    # Naam poochna
    name = context.user_data.get("name")
    if text in ("mera naam kya hai", "what is my name", "whats my name"):
        if name:
            await send_reply(update, f"Aapka naam {name} hai 😊❤️")
        else:
            await send_reply(update, "Aapne abhi mujhe apna naam nahi bataya 😊")
        return


    if text in ("tum mere dost ho", "aap mere dost ho"):
        await send_reply(update, "Bilkul 🤝❤️ Main aapka dost hoon!")
        return

    if text in ("mujhe ek joke sunao", "joke sunao", "joke batao"):
        await send_reply(update, random.choice([
            "Teacher: Batao sabse zyada nasha kis cheez mein hota hai? Student: Padhai mein 😂📚",
            "Main dieting par hoon... bas khane ko ye baat nahi pata 😂",
            "Phone ki battery aur insaan ka patience, dono 1% par aa jayein to tension hoti hai 😂🔋"
        ]))
        return

    if text in ("mujhe motivate karo", "motivate me", "motivation do"):
        await send_reply(update, "Haar mat maano 💪❤️ Dheere-dheere har cheez possible hai!")
        return

    if text in ("tum mujhe yaad karte ho", "mujhe yaad karte ho", "mujhe yaad krte ho"):
        await send_reply(update, "Haan 😊❤️ Bilkul yaad karta hoon!")
        return

    if text in ("aaj kya naya hai", "aaj kya hua", "kya naya hai"):
        await send_reply(update, random.choice([
            "Filhaal to aapse baat karna hi naya hai 😄❤️",
            "Kuch khaas nahi 😊 Aap batao, aaj kya naya hua?",
            "Sab mast hai 😎❤️ Aapke paas koi nayi baat hai?"
        ]))
        return

    # Greeting
    if text in ("hello", "hi", "hii", "hey", "hlo", "helo", "namaste", "नमस्ते"):
        await send_reply(update, random.choice([
            "Hello 😊❤️ Kaise ho?",
            "Hii 😄❤️ Kya haal hai?",
            "Hey 😊❤️ Main yahin hoon!"
        ]))
        return

    # Kaise ho
    if text in ("kaise ho", "kaisa ho", "kese ho", "how are you", "how r u"):
        await send_reply(update, random.choice([
            "Main bilkul badhiya hoon 😊❤️ Aap kaise ho?",
            "Sab badhiya 😄❤️ Aap batao?",
            "Main ekdum theek hoon 🤖❤️"
        ]))
        return

    # Kya haal
    if text in ("kya haal hai", "haal chaal", "haal chal"):
        await send_reply(update, "Bilkul badhiya 😊❤️ Aap batao?")
        return

    # Kya kar rahe ho
    if text in (
        "kya kar rahe ho", "kya kr rahe ho", "kya kar rhe ho",
        "kya kr rhe ho", "what are you doing", "what r u doing"
    ):
        reply = (
            f"Bas {name} se baat kar raha hoon 😄❤️"
            if name else
            "Bas aapse baat kar raha hoon 😄❤️"
        )
        await send_reply(update, reply)
        return

    # Kahan ho
    if text in ("tum kahan ho", "tum kaha ho", "aap kahan ho", "aap kaha ho", "where are you"):
        await send_reply(update, "Main yahin hoon 😊❤️")
        return

    # Naam bot ka
    if text in ("tumhara naam kya hai", "aapka naam kya hai", "what is your name"):
        await send_reply(update, "Mera naam Shubham Help Bot hai 🤖❤️")
        return

    if text in ("tum kaun ho", "aap kaun ho", "who are you"):
        await send_reply(update, "Main Shubham Help Bot hoon 🤖😊❤️")
        return

    # Weather
    if any(x in text for x in (
        "mausam", "weather", "garmi", "thand",
        "baarish", "barish", "dhoop"
    )):
        await send_reply(update, random.choice([
            "Haan 😊 Aaj mausam kaafi achha lag raha hai! ❤️",
            "Bilkul 😄 Mausam achha ho to mood bhi achha ho jata hai.",
            "Haan ji 😊 Aaj weather kaafi nice hai!"
        ]))
        return

    # Food
    if any(x in text for x in (
        "khana", "khaana", "bhook", "lunch",
        "dinner", "breakfast"
    )):
        await send_reply(update, random.choice([
            "Achha 😊 Kuch tasty kha lo ❤️",
            "Haan 😄 Khana time par kha lena.",
            "Bhook lagi hai to kuch achha sa kha lo 😊❤️"
        ]))
        return

    # Sleep / tired
    if any(x in text for x in (
        "neend", "so raha", "sona hai",
        "thak gaya", "thak gya"
    )):
        await send_reply(update, random.choice([
            "Toh thoda rest kar lo 😴❤️",
            "Haan 😊 Aaram bhi zaroori hai.",
            "Thak gaye ho to thoda relax kar lo ❤️"
        ]))
        return

    # Mood
    if any(x in text for x in ("mood off", "mood kharab", "sad", "dukhi", "udaas", "lonely", "akela")):
        await send_reply(update, random.choice([
            "Kya hua? 😊 Main yahin hoon, batao ❤️",
            "Aap mujhse baat kar sakte ho ❤️",
            "Thoda halka feel karne ke liye baat karte hain 😊"
        ]))
        return

    # Happy
    if any(x in text for x in ("khush hoon", "happy hoon", "achha din", "accha din", "mast din", "mood bahut achha hai", "mood achha hai")):
        await send_reply(update, random.choice([
            "Ye sunkar mujhe bhi achha laga 😊❤️ Aise hi khush raho!",
            "Wah 😄 Aap khush ho to mood automatically achha ho jata hai ❤️",
            "Bahut badhiya 😊❤️ Aaj ka din enjoy karo!"
        ]))
        return

    # Thank you
    if any(x in text for x in ("thank you", "thanks", "thx", "shukriya", "dhanyawad")):
        await send_reply(update, random.choice([
            "You're welcome 😊❤️",
            "Koi baat nahi 😄❤️",
            "Hamesha 😊❤️"
        ]))
        return

    # Miss you
    if any(x in text for x in ("miss you", "miss u", "miss youu", "missuu")):
        await send_reply(update, "Aww 😊❤️ Main yahin hoon!")
        return

    # Funny
    if text in ("haha", "hahaha", "lol", "hehe", "hehehe"):
        await send_reply(update, random.choice([
            "Haha 😄😂",
            "😂😂 Bahut funny!",
            "Hehe 😄❤️"
        ]))
        return

    # Bye
    if text in ("bye", "goodbye", "see you"):
        await send_reply(update, random.choice([
            "Bye 😊❤️ Phir milte hain!",
            "Okay 😄 Take care!",
            "See you soon 🤖❤️"
        ]))
        return

    # Good morning / night
    if "good morning" in text or text in ("gm", "suprabhat"):
        await send_reply(update, "Good Morning 🌅😊❤️ Aapka din bahut achha rahe!")
        return

    if "good night" in text or text in ("gn", "shubh ratri"):
        await send_reply(update, "Good Night 🌙😴❤️ Sweet dreams!")
        return

    # Radhe Radhe
    if text in ("radhe radhe", "radhey radhey", "radhe"):
        await send_reply(update, "🙏 Radhe Radhe ❤️🌸")
        return

    if text in ("jai shree krishna", "jai shri krishna", "jai krishna", "krishna"):
        await send_reply(update, "🦚🙏 जय श्री कृष्ण ❤️")
        return

    # Simple conversation
    if text in ("achha", "acha", "accha"):
        await send_reply(update, "Haan ji 😊❤️")
        return

    if text in ("sach me", "sach mein"):
        await send_reply(update, "Haan bilkul 😄❤️")
        return

    if text in ("kyu", "kyun", "kyon"):
        await send_reply(update, "Bas aise hi 😊❤️")
        return

    # Going home
    if any(x in text for x in ("ghar ja raha hoon", "ghar jaa raha hoon", "ghar ja raha", "ghar jaa raha")):
        await send_reply(update, random.choice([
            "Achha 😊 Dhyan se ghar jana ❤️",
            "Theek hai 😄 Ghar pahunchkar batana!",
            "Achha ji 😊 Safe journey, ghar pahunchkar aaram karna ❤️"
        ]))
        return

    # Together / support
    if text in ("kya tum mere saath ho", "kya tum mere sath ho", "tum mere saath ho", "tum mere sath ho"):
        await send_reply(update, random.choice([
            "Haan 😊❤️ Main yahin hoon, aapke saath.",
            "Bilkul 🤝❤️ Jab bhi baat karni ho, main yahin hoon.",
            "Haan ji 😊❤️ Aapse baat karne ke liye main yahin hoon."
        ]))
        return

    # Natural reply for unknown/random messages
    if any(x in text for x in ("aaj", "din", "hua", "raha", "gaya", "gayi")):
        replies = [
            "Achha 😊❤️ Phir kya hua?",
            "Ohh 😄 Accha! Aage batao.",
            "Wah 😊 Iske baare mein aur batao.",
            "Achha ji ❤️ Phir kaisa raha?"
        ]
    elif any(x in text for x in ("main", "mujhe", "mera", "meri")):
        replies = [
            "Achha 😊❤️ Aapke baare mein aur batao.",
            "Hmm 😄 Samajh raha hoon, phir kya hua?",
            "Ohh 😊 Accha! Aage bataiye.",
            "Haan ji ❤️ Main sun raha hoon."
        ]
    elif "bahut" in text or "zyada" in text:
        replies = [
            "Ohh 😯 Itna zyada? Aage batao.",
            "Achha 😊❤️ Phir kya hua?",
            "Wah 😄 Ye interesting hai!",
            "Haan ji 😊 Main sun raha hoon."
        ]
    else:
        replies = [
            "Achha 😊❤️ Iske baare mein aur batao.",
            "Hmm 😄 Samajh raha hoon, phir kya hua?",
            "Ohh 😯 Accha! Aage batao.",
            "Haan ji 😊 Main sun raha hoon.",
            "Interesting 😎❤️ Aur bataiye.",
            "Achha ji 😊 Phir batao."
        ]

    await send_reply(update, random.choice(replies))

async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != 6222405805:
        await send_reply(update, "⛔ Ye command sirf bot owner ke liye hai.")
        return

    stats = context.application.bot_data.get(
        "stats", {"messages": 0, "users": set()}
    )

    await send_reply(update, 
        "📊 Bot Statistics\n\n"
        f"📩 Total Messages: {stats['messages']}\n"
        f"👥 Unique Users: {len(stats['users'])}\n"
        "🟢 Status: Online"
    )


async def broadcast_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != 6222405805:
        await send_reply(update, "⛔ Ye command sirf bot owner ke liye hai.")
        return

    if not context.args:
        await send_reply(update, 
            "📢 Broadcast message likhiye.\n\n"
            "Example:\n/broadcast Hello everyone ❤️"
        )
        return

    message = " ".join(context.args)

    stats = context.application.bot_data.get(
        "stats", {"messages": 0, "users": set()}
    )

    users = list(stats.get("users", set()))

    if not users:
        await send_reply(update, 
            "📭 Abhi koi saved user nahi mila."
        )
        return

    sent = 0
    failed = 0

    for user_id in users:
        try:
            await context.bot.send_message(
                chat_id=user_id,
                text=message
            )
            sent += 1
        except Exception as e:
            failed += 1
            print(f"Broadcast error for {user_id}: {e}")

    await send_reply(update, 
        "📢 Broadcast complete!\n\n"
        f"✅ Sent: {sent}\n"
        f"❌ Failed: {failed}"
    )


async def block_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != 6222405805:
        await send_reply(update, "⛔ Ye command sirf bot owner ke liye hai.")
        return

    if not context.args:
        await send_reply(update, 
            "🔒 User ID dijiye.\nExample: /block 123456789"
        )
        return

    try:
        user_id = int(context.args[0])
        blocked = context.application.bot_data.setdefault("blocked_users", set())
        blocked.add(user_id)
        await send_reply(update, 
            f"🔒 User {user_id} successfully blocked."
        )
    except ValueError:
        await send_reply(update, "❌ Invalid Telegram ID.")


async def unblock_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != 6222405805:
        await send_reply(update, "⛔ Ye command sirf bot owner ke liye hai.")
        return

    if not context.args:
        await send_reply(update, 
            "🔓 User ID dijiye.\nExample: /unblock 123456789"
        )
        return

    try:
        user_id = int(context.args[0])
        blocked = context.application.bot_data.setdefault("blocked_users", set())

        if user_id in blocked:
            blocked.remove(user_id)
            await send_reply(update, 
                f"🔓 User {user_id} successfully unblocked."
            )
        else:
            await send_reply(update, 
                f"ℹ️ User {user_id} blocked list mein nahi hai."
            )
    except ValueError:
        await send_reply(update, "❌ Invalid Telegram ID.")


async def blocked_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != 6222405805:
        await send_reply(update, "⛔ Ye command sirf bot owner ke liye hai.")
        return

    blocked = context.application.bot_data.setdefault("blocked_users", set())

    if not blocked:
        await send_reply(update, "🔓 Blocked users: None")
        return

    users = "\n".join(f"• {user_id}" for user_id in sorted(blocked))
    await send_reply(update, 
        f"🔒 Blocked Users ({len(blocked)}):\n\n{users}"
    )


async def profile_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    profiles = context.application.bot_data.setdefault("profiles", {})

    profile = profiles.get(user.id)

    if not profile:
        await send_reply(update, 
            "👤 Profile abhi create nahi hua."
        )
        return

    username = (
        f"@{profile['username']}"
        if profile["username"]
        else "No username"
    )

    await send_reply(update, 
        "👤 Your Profile\n\n"
        f"📝 Name: {profile['name']}\n"
        f"📱 Username: {username}\n"
        f"🆔 ID: {user.id}\n"
        f"📩 Messages: {profile['messages']}"
    )


async def reset_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    # Clear conversation-related data while keeping profile/stats.
    for key in (
        "conversation",
        "conversation_history",
        "chat_history",
        "context_history",
        "reply_to_user",
    ):
        context.user_data.pop(key, None)

    await send_reply(
        update,
        "🔄 Conversation reset ho gayi!\n\n"
        "✨ Ab hum fresh start karte hain. 😊❤️"
    )


async def remind_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 2:
        await send_reply(
            update,
            "⏰ Reminder format:\n\n"
            "/remind 10m पानी पीना\n"
            "/remind 1h खाना खाना"
        )
        return

    time_text = context.args[0].lower()
    reminder_text = " ".join(context.args[1:])

    import re
    match = re.fullmatch(r"(\d+)(s|m|h)", time_text)

    if not match:
        await send_reply(
            update,
            "❌ Time format गलत है.\n"
            "Example: /remind 10m पानी पीना"
        )
        return

    amount = int(match.group(1))
    unit = match.group(2)

    if unit == "s":
        delay = amount
    elif unit == "m":
        delay = amount * 60
    else:
        delay = amount * 3600

    if delay > 86400:
        await send_reply(
            update,
            "⚠️ Maximum reminder time 24 hours है."
        )
        return

    import asyncio

    await send_reply(
        update,
        f"⏰ Reminder set!\n\n"
        f"📝 {reminder_text}\n"
        f"⌛ {time_text} बाद याद दिलाऊँगा. ❤️"
    )

    async def reminder_task():
        await asyncio.sleep(delay)
        try:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=(
                    "🔔 Reminder!\n\n"
                    f"📝 {reminder_text}\n\n"
                    "❤️ आपका reminder आ गया!"
                )
            )
        except Exception as e:
            print(f"Reminder error: {e}")

    asyncio.create_task(reminder_task())


async def ping_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    import time

    start_time = time.perf_counter()

    await update.message.chat.send_action("typing")

    elapsed = (time.perf_counter() - start_time) * 1000

    await update.message.reply_text(
        "🏓 Pong!\n\n"
        "🟢 Bot is online\n"
        f"⚡ Response: {elapsed:.0f} ms"
    )


async def commands_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_reply(
        update,
        "📋 Available Commands\n\n"
        "/start - Main menu 👋\n"
        "/help - Help menu 📖\n"
        "/profile - Your profile 👤\n"
        "/id - User information 🆔\n"
        "/ping - Check bot status 🏓\n"
        "/joke - Random joke 😂\n"
        "/quote - Random quote ✨\n"
        "/remind - Set a reminder ⏰\n"
        "/reset - Reset conversation 🔄\n"
        "/about - About bot ℹ️\n"
        "/contact - Contact owner 📩\n\n"
        "❤️ Shubham Help Bot"
    )


async def setname_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    profiles = context.application.bot_data.setdefault("profiles", {})

    if not context.args:
        await send_reply(
            update,
            "✏️ Apna new name likhiye.\n\n"
            "Example:\n"
            "/setname Shubham"
        )
        return

    new_name = " ".join(context.args).strip()

    if len(new_name) > 50:
        await send_reply(
            update,
            "❌ Name maximum 50 characters ka ho sakta hai."
        )
        return

    profile = profiles.setdefault(
        user.id,
        {
            "name": user.full_name,
            "username": user.username,
            "messages": 0,
        }
    )

    profile["name"] = new_name

    await send_reply(
        update,
        f"✅ Profile name update ho gaya!\n\n"
        f"👤 New Name: {new_name}"
    )


async def setbio_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    profiles = context.application.bot_data.setdefault("profiles", {})

    if not context.args:
        await send_reply(
            update,
            "✏️ Apna bio likhiye.\n\n"
            "Example:\n"
            "/setbio Always positive ❤️"
        )
        return

    new_bio = " ".join(context.args).strip()

    if len(new_bio) > 150:
        await send_reply(
            update,
            "❌ Bio maximum 150 characters ka ho sakta hai."
        )
        return

    profile = profiles.setdefault(
        user.id,
        {
            "name": user.full_name,
            "username": user.username,
            "messages": 0,
        }
    )

    profile["bio"] = new_bio

    await send_reply(
        update,
        f"✅ Bio update ho gaya!\n\n"
        f"📝 Bio: {new_bio}"
    )


async def mystats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    profiles = context.application.bot_data.setdefault("profiles", {})
    profile = profiles.get(user.id)

    if not profile:
        profile = {
            "name": user.full_name,
            "username": user.username,
            "messages": 0,
            "bio": "",
        }
        profiles[user.id] = profile

    username = (
        f"@{profile.get('username')}"
        if profile.get("username")
        else "No username"
    )

    await send_reply(
        update,
        "📊 My Stats\n\n"
        f"👤 Name: {profile.get('name', user.full_name)}\n"
        f"📱 Username: {username}\n"
        f"🆔 ID: {user.id}\n"
        f"📩 Messages: {profile.get('messages', 0)}\n"
        "🤖 Status: Active ✅"
    )


async def guess_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    import random

    user = update.effective_user
    games = context.application.bot_data.setdefault("guess_games", {})

    if not context.args:
        games[user.id] = random.randint(1, 10)

        await send_reply(
            update,
            "🎯 Guess Game Started!\n\n"
            "Maine 1 se 10 ke beech ek number choose kiya hai. 🤫\n"
            "Ab guess kijiye:\n\n"
            "/guess 7\n\n"
            "🍀 Good luck!"
        )
        return

    try:
        guess = int(context.args[0])
    except ValueError:
        await send_reply(
            update,
            "❌ Sirf number likhiye. Example: /guess 7"
        )
        return

    if guess < 1 or guess > 10:
        await send_reply(
            update,
            "⚠️ Number 1 se 10 ke beech hona chahiye."
        )
        return

    if user.id not in games:
        games[user.id] = random.randint(1, 10)

    secret = games[user.id]

    if guess == secret:
        del games[user.id]
        await send_reply(
            update,
            f"🎉 Correct! Number {secret} tha! ❤️\n"
            "🏆 You won!\n\n"
            "Naya game ke liye /guess bhejiye."
        )
    elif guess < secret:
        await send_reply(
            update,
            "📈 Thoda bada number try kijiye! 😎"
        )
    else:
        await send_reply(
            update,
            "📉 Thoda chhota number try kijiye! 😎"
        )


def main():
    app = Application.builder().token(os.environ["BOT_TOKEN"]).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("about", about_command))
    app.add_handler(CommandHandler("contact", contact_command))

    async def info_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await send_reply(update, 
            "🤖 Shubham Help Bot\n\n"
            "✨ Features:\n"
            "• Smart replies 💬\n"
            "• Funny replies 😂\n"
            "• Friendly conversation ❤️\n"
            "• Radhe Radhe replies 🙏\n"
            "• Useful commands ⚡\n\n"
            "🟢 Status: Online\n"
            "❤️ Made with Python"
        )


    async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await send_reply(update, 
            "🤖 Bot Status: Online ✅\n"
            "⚡ Shubham Help Bot is running smoothly! ❤️"
        )

    async def id_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
        user = update.effective_user

        username = (
            f"@{user.username}"
            if user.username
            else "No username"
        )

        await send_reply(
            update,
            "👤 User Information\n\n"
            f"📝 Name: {user.full_name}\n"
            f"📱 Username: {username}\n"
            f"🆔 Telegram ID: {user.id}"
        )


    async def joke_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
        import random

        category = " ".join(context.args).lower().strip()

        jokes = {
            "funny": [
                "😂 Teacher: Homework kahan hai? Student: Sir, WiFi nahi tha!",
                "🤣 Phone bola: Battery low. Maine bola: Same bro!",
                "😂 Monday aur mera mood—dono kabhi ready nahi hote!"
            ],
            "love": [
                "❤️ Pyaar mein sab smart hote hain, bas reply aate hi nervous ho jaate hain. 😂",
                "😂 Crush ka 'Hi' aaya aur dil ne 5G speed pakad li! ❤️",
                "❤️ Love ka rule simple hai: Seen ka wait aur reply ki hope. 😂"
            ],
            "friend": [
                "😂 Dost wahi jo problem mein saath de... aur photo mein tag bhi kare!",
                "🤣 Best friend: 'Bhai secret hai.' 5 minute baad poori duniya ko pata!",
                "😂 Dost ke saath argument ka result: Dono galat, friendship right!"
            ],
            "default": [
                "😂 Teacher: Homework kahan hai? Student: Sir, WiFi nahi tha!",
                "🤣 Mera phone bhi mujhe ignore karta hai—battery 1% pe chala jata hai!",
                "😂 Life short hai, isliye jokes long rakho!",
                "🤣 Main diet par hoon... bas khana dekhte hi diet mujhe chhod deti hai!"
            ]
        }

        reply = random.choice(jokes.get(category, jokes["default"]))
        await send_reply(update, reply)

    async def quote_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await send_reply(update, 
            random.choice([
                "✨ Khud par bharosa rakho, waqt zaroor badlega.",
                "💪 Chhoti progress bhi progress hoti hai.",
                "🌟 Har din ek nayi opportunity hai."
            ])
        )

    async def love_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await send_reply(update, "❤️😊 Aapke liye ek special smile!")

    async def radhe_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await send_reply(update, "🙏 Radhe Radhe ❤️🌸")

    async def menu_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await send_reply(update, 
            "🤖 Shubham Help Bot\n\n"
            "📋 Available Commands\n\n"
            "/start - 🏠 Main Menu\n"
            "/help - 🤖 Help Menu\n"
            "/about - ℹ️ About Bot\n"
            "/contact - 📩 Contact\n"
            "/joke - 😂 Random Joke\n"
            "/quote - ✨ Motivational Quote\n"
            "/love - ❤️ Special Reply\n"
            "/radhe - 🙏 Radhe Radhe\n"
            "/status - 🟢 Bot Status\n"
            "/id - 🆔 Your Telegram ID\n"
            "/menu - 📋 Commands List\n\n"
            "💬 Aap normal messages bhi bhej sakte hain!"
        )



    app.add_handler(CommandHandler("joke", joke_command))
    app.add_handler(CommandHandler("quote", quote_command))
    app.add_handler(CommandHandler("love", love_command))
    app.add_handler(CommandHandler("radhe", radhe_command))
    app.add_handler(CommandHandler("menu", menu_command))


    app.add_handler(CommandHandler("status", status_command))
    app.add_handler(CommandHandler("id", id_command))

    app.add_handler(CommandHandler("info", info_command))
    app.add_handler(
        CallbackQueryHandler(owner_reply_handler, pattern=r"^reply_")
    )
    app.add_handler(CommandHandler("stats", stats_command))
    app.add_handler(CommandHandler("broadcast", broadcast_command))
    app.add_handler(CommandHandler("profile", profile_command))
    app.add_handler(CommandHandler("guess", guess_command))
    app.add_handler(CommandHandler("mystats", mystats_command))
    app.add_handler(CommandHandler("setbio", setbio_command))
    app.add_handler(CommandHandler("setname", setname_command))
    app.add_handler(CommandHandler("commands", commands_command))
    app.add_handler(CommandHandler("ping", ping_command))
    app.add_handler(CommandHandler("remind", remind_command))
    app.add_handler(CommandHandler("reset", reset_command))
    app.add_handler(CommandHandler("block", block_command))
    app.add_handler(CommandHandler("unblock", unblock_command))
    app.add_handler(CommandHandler("blocked", blocked_command))

    app.add_handler(CallbackQueryHandler(button_handler))


    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, auto_reply)
    )
    print("Bot started...")
    app.run_polling()

if __name__ == "__main__":
    main()
