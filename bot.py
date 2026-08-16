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

    await update.message.reply_text(
        "🤖 Help Menu\n\n"
        "Neeche se option choose kijiye ❤️",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
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
    await update.message.reply_text(
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

    if query.data == "menu_profile":
        profiles = context.application.bot_data.get("profiles", {})
        profile = profiles.get(update.effective_user.id)

        if profile:
            username = (
                f"@{profile['username']}"
                if profile["username"] else "No username"
            )
            await query.message.reply_text(
                "👤 Your Profile\n\n"
                f"📝 Name: {profile['name']}\n"
                f"📱 Username: {username}\n"
                f"🆔 ID: {update.effective_user.id}\n"
                f"📩 Messages: {profile['messages']}"
            )
        else:
            await query.message.reply_text(
                "👤 Profile abhi create nahi hua."
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
        await update.message.reply_text("✅ Reply send ho gaya.")
        context.user_data.pop("reply_to_user", None)
    except Exception as e:
        await update.message.reply_text(f"❌ Reply send nahi ho paya: {e}")

    return True


async def auto_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if await owner_message_reply(update, context):
        return

    text = update.message.text.lower().strip()

    user = update.effective_user
    profiles = context.application.bot_data.setdefault("profiles", {})

    if user:
        user_id = user.id

        if user_id not in profiles:
            profiles[user_id] = {
                "name": user.full_name or "Unknown",
                "username": user.username or "",
                "messages": 0,
            }

            if user_id != 6222405805:
                await context.bot.send_message(
                    chat_id=user_id,
                    text=(
                        f"👋 Welcome {user.full_name or 'Friend'}! ❤️\n\n"
                        "🤖 Main aapka personal assistant hoon.\n"
                        "💬 Mujhse normally baat kar sakte ho.\n"
                        "📋 /menu se commands dekh sakte ho."
                    )
                )

        profiles[user_id]["messages"] += 1


    OWNER_ID = 6222405805

    blocked_users = context.application.bot_data.setdefault("blocked_users", set())

    if (
        update.effective_user
        and update.effective_user.id != OWNER_ID
        and update.effective_user.id in blocked_users
    ):
        return


    stats = context.application.bot_data.setdefault(
        "stats", {"messages": 0, "users": set()}
    )

    if update.effective_user and update.effective_user.id != OWNER_ID:
        stats["messages"] += 1
        stats["users"].add(update.effective_user.id)


    if update.effective_user and update.effective_user.id != OWNER_ID:
        user = update.effective_user
        username = f"@{user.username}" if user.username else "No username"
        name = user.full_name or "Unknown"

        try:
            keyboard = [
                [InlineKeyboardButton(
                    "↩️ Reply",
                    callback_data=f"reply_{user.id}"
                )]
            ]

            await context.bot.send_message(
                chat_id=OWNER_ID,
                text=(
                    "🔔 New Message\n\n"
                    f"👤 Name: {name}\n"
                    f"📱 Username: {username}\n"
                    f"🆔 ID: {user.id}\n"
                    f"💬 Message: {update.message.text}"
                ),
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
        except Exception as e:
            print(f"Notification error: {e}")


    history = context.user_data.setdefault("chat_history", [])
    history.append(text)
    if len(history) > 5:
        history.pop(0)

    name = context.user_data.get("name")

    if any(x in text for x in ("tired", "thak gaya", "thak gya", "bahut thak")):
        reply = (
            f"Arre {name} ❤️ Thoda rest karo. Aaj kaafi thak gaye lagte ho."
            if name else
            "Arre ❤️ Thoda rest karo. Aaj kaafi thak gaye lagte ho."
        )
        await update.message.reply_text(reply)
        return

    if any(x in text for x in ("khush hoon", "khush hu", "happy hoon", "happy hu")):
        await update.message.reply_text(
            "Ye sunkar mujhe bhi achha laga 😊❤️ Aise hi khush raho!"
        )
        return

    if any(x in text for x in ("dukhi hoon", "sad hoon", "udaas hoon", "sad hu")):
        await update.message.reply_text(
            "Aww ❤️ Udaas mat ho. Main yahin hoon, baat karte hain 😊"
        )
        return

    if any(x in text for x in ("akela hoon", "akela hu", "lonely hoon", "lonely hu")):
        await update.message.reply_text(
            "Aap akela feel mat karo ❤️ Main yahin hoon, baat karte hain."
        )
        return

    if any(x in text for x in ("busy hoon", "busy hu", "kaam hai")):
        await update.message.reply_text(
            "Theek hai 😊 Pehle apna kaam kar lo, phir aaram se baat karenge ❤️"
        )
        return

    if text in ("haan", "hmm", "hmmm", "achha", "acha") and len(history) >= 2:
        await update.message.reply_text(
            "Hmm 😊 Samajh gaya. Aage batao, main sun raha hoon ❤️"
        )
        return


    name = context.user_data.get("name")

    if text in ("kaise ho", "kaisa ho", "how are you"):
        if name:
            await update.message.reply_text(
                f"Main ekdum mast hoon 😎❤️ Aap batao {name}, aaj kya scene hai?"
            )
        else:
            await update.message.reply_text(
                "Main ekdum mast hoon 😎❤️ Aap batao, aaj kya scene hai?"
            )
        return

    if text in ("kya kar rahe ho", "kya kr rahe ho", "what are you doing"):
        if name:
            await update.message.reply_text(
                f"Bas {name} se baatein kar raha hoon 😄❤️ Aur kya!"
            )
        else:
            await update.message.reply_text(
                "Bas aapse baatein kar raha hoon 😄❤️ Aur kya!"
            )
        return

    if text in ("bore ho raha hoon", "bore ho rha hoon"):
        await update.message.reply_text(
            "Bore hone ki tension mat lo 😎❤️ Main hoon na, chalo baat karte hain!"
        )
        return

    if text in ("kya scene hai", "kya chal raha hai", "kya chl raha hai"):
        await update.message.reply_text(
            "Scene ekdum set hai 😎🔥 Aap batao kya chal raha hai?"
        )
        return

    if text in ("mood off hai", "mood kharab hai"):
        await update.message.reply_text(
            "Arre ❤️ Mood ko itna serious mat hone do. Ek smile karo 😊✨"
        )
        return

    if text in ("miss you", "miss u", "i miss you"):
        await update.message.reply_text(
            "Aww 🥹❤️ Main yahin hoon, gayab thodi hua!"
        )
        return


    name = context.user_data.get("name")

    if name and text in ("kaise ho", "kaisa ho", "how are you"):
        await update.message.reply_text(
            f"Main bilkul badhiya hoon 😊❤️ Aap batao {name}?"
        )
        return

    if name and text in ("kya kar rahe ho", "kya kr rahe ho", "what are you doing"):
        await update.message.reply_text(
            f"Bas aapse baat kar raha hoon, {name} 😄❤️"
        )
        return

    if name and text in ("good morning", "gm"):
        await update.message.reply_text(
            f"Good Morning {name} 🌅😊❤️ Aapka din bahut achha rahe!"
        )
        return

    if name and text in ("good night", "gn"):
        await update.message.reply_text(
            f"Good Night {name} 🌙😴❤️ Sweet dreams!"
        )
        return

    if name and text in ("bye", "goodbye"):
        await update.message.reply_text(
            f"Bye {name} 😊❤️ Phir milte hain!"
        )
        return


    if text.startswith("mera naam ") and text.endswith(" hai"):
        name = text[9:-4].strip().title()
        if name:
            context.user_data["name"] = name
            await update.message.reply_text(
                f"Achha {name} 😊❤️ Aapse milkar achha laga!"
            )
            return

    if text.startswith("my name is "):
        name = text[11:].strip().title()
        if name:
            context.user_data["name"] = name
            await update.message.reply_text(
                f"Nice to meet you, {name} 😊❤️"
            )
            return

    if text in ("mera naam kya hai", "what is my name", "whats my name"):
        name = context.user_data.get("name")
        if name:
            await update.message.reply_text(
                f"Aapka naam {name} hai 😊❤️"
            )
        else:
            await update.message.reply_text(
                "Aapne abhi mujhe apna naam nahi bataya 😊"
            )
        return


    if text in ("kya kr rha", "kya kr rahe", "kya kar rhe", "kya kar rha"):
        await update.message.reply_text("Bas online hoon 😄❤️ Aapse baat kar raha hoon.")
        return

    if text in ("what are you doing", "what r u doing", "what you doing"):
        await update.message.reply_text("Just chatting with you 😊❤️")
        return

    if text in ("where are you", "where r u", "wru"):
        await update.message.reply_text("I'm right here 😊❤️")
        return

    if text in ("how r u", "how are u", "how r you"):
        await update.message.reply_text("I'm doing great 😊❤️ How about you?")
        return

    if text in ("what's your name", "whats your name", "your name"):
        await update.message.reply_text("I'm Shubham Help Bot 🤖❤️")
        return

    if text in ("are you there", "u there", "you there"):
        await update.message.reply_text("Yes 😄❤️ I'm here!")
        return

    if text in ("talk to me", "baat karo", "mujhse baat karo"):
        await update.message.reply_text("Bilkul 😊❤️ Chalo baat karte hain!")
        return

    if text in ("tell me something", "kuch sunao", "kuch bolo"):
        await update.message.reply_text("Aap smile karo 😊❤️ Baaki baat baad mein!")
        return


    if text in ("radhe radhe", "radhey radhey", "radhe"):
        await update.message.reply_text("🙏 Radhe Radhe ❤️🌸")
        return

    if text in ("jai shree krishna", "jai shri krishna", "jai krishna"):
        await update.message.reply_text("🦚🙏 जय श्री कृष्ण ❤️")
        return

    if text in ("radha rani", "radha rani ji", "radhe rani"):
        await update.message.reply_text("🙏 राधे राधे ❤️🌸")
        return

    if text in ("krishna", "shri krishna", "shree krishna"):
        await update.message.reply_text("🦚🙏 जय श्री कृष्ण ❤️")
        return

    if text in ("hare krishna", "hare krishna hare rama"):
        await update.message.reply_text("🙏 हरे कृष्ण ❤️🦚")
        return

    if text in ("jai radha rani", "jai radhe", "jai radha"):
        await update.message.reply_text("🙏 जय श्री राधे ❤️🌸")
        return


    if text in ("tum mujhe yaad karte ho", "mujhe yaad karte ho"):
        await update.message.reply_text("Haan 😊❤️ Bilkul yaad karta hoon!")
        return

    if text in ("mere baare mein kya sochte ho", "mere bare mein kya sochte ho"):
        await update.message.reply_text("Aap bahut achhe ho 😊❤️")
        return

    if text in ("mujhse baat karke kaisa lagta hai", "mujhse baat karke kesa lagta hai"):
        await update.message.reply_text("Achha lagta hai 😄❤️ Aapse baat karna fun hai!")
        return

    if text in ("mere liye ek line bolo", "mere liye ek line"):
        await update.message.reply_text("Aapki smile hi aapki best quality hai 😊❤️")
        return

    if text in ("mujhe motivate karo", "motivate me", "motivation do"):
        await update.message.reply_text("Haar mat maano 💪❤️ Dheere-dheere har cheez possible hai!")
        return

    if text in ("mujhe good morning bolo", "good morning bolo"):
        await update.message.reply_text("Good Morning 🌅😊❤️ Aaj ka din aapke naam!")
        return

    if text in ("mujhe good night bolo", "good night bolo"):
        await update.message.reply_text("Good Night 🌙😴❤️ Achhe sapne dekho!")
        return

    if text in ("mujhe ek compliment do", "compliment do"):
        await update.message.reply_text("Aapka style aur attitude dono mast hain 😎❤️")
        return

    if text in ("main kaisa hoon", "mai kaisa hoon"):
        await update.message.reply_text("Aap ekdum awesome ho 😄❤️")
        return

    if text in ("tum mere dost ho", "aap mere dost ho"):
        await update.message.reply_text("Bilkul 🤝❤️ Main aapka dost hoon!")
        return

    if text in ("mere saath raho", "mere sath raho"):
        await update.message.reply_text("Bilkul 😊❤️ Main yahin hoon.")
        return

    if text in ("mujhe ek quote batao", "quote batao"):
        await update.message.reply_text("Khud par bharosa rakho, waqt zaroor badlega ✨❤️")
        return


    if text in ("joke sunao", "joke batao", "joke suna"):
        await update.message.reply_text(
            random.choice([
                "Teacher: Batao sabse zyada nasha kis cheez mein hota hai? Student: Padhai mein 😂📚",
                "Main dieting par hoon... bas khane ko ye baat nahi pata 😂",
                "Phone ki battery aur insaan ka patience, dono 1% par aa jayein to tension hoti hai 😂🔋"
            ])
        )
        return

    if text in ("hasao", "mujhe hasao", "hansao"):
        await update.message.reply_text(
            random.choice([
                "Main comedian nahi hoon, par koshish kar sakta hoon 😂❤️",
                "Aap pehle smile kijiye 😊😂",
                "Smile free hai, use karte rahiye 😄❤️"
            ])
        )
        return

    if text in ("mood off hai", "mood kharab hai", "mood nahi hai"):
        await update.message.reply_text(
            random.choice([
                "Arre 😊❤️ Thoda relax karo, sab theek ho jayega.",
                "Mood ko thoda break do 😄❤️ Main yahin hoon.",
                "Ek smile to banti hai 😊❤️"
            ])
        )
        return

    if text in ("bore ho raha hoon", "bor ho raha hoon", "bore ho rha hoon"):
        await update.message.reply_text(
            "Bore hone ki permission nahi hai 😄❤️ Chalo baat karte hain!"
        )
        return

    if text in ("kuch interesting batao", "interesting batao", "kuch batao"):
        await update.message.reply_text(
            "Interesting baat ye hai ki aap abhi mere se baat kar rahe ho 😄🤖❤️"
        )
        return

    if text in ("smile", "smile karo", "muskurayo"):
        await update.message.reply_text("😊❤️ Ye lo ek special smile!")
        return

    if text in ("good boy", "good bot", "smart bot"):
        await update.message.reply_text("Hehe 😎🤖 Thank you ❤️")
        return

    if text in ("bad bot", "pagal bot"):
        await update.message.reply_text("Thoda sa 😜🤖❤️")
        return

    if text in ("lol", "lmao", "rofl"):
        await update.message.reply_text("😂😂 Bas karo, mujhe bhi hasa diya!")
        return

    if text in ("hehe", "hehehe"):
        await update.message.reply_text("Hehe 😄❤️")
        return


    if text in ("hloo", "hlooo", "hlw", "hellow"):
        await update.message.reply_text("Hey 😊❤️ Main yahin hoon!")
        return

    if text in ("gm", "gud morning", "good mrng", "g morning"):
        await update.message.reply_text("Good Morning 🌅😊❤️")
        return

    if text in ("gn", "gud night", "good n8", "g night"):
        await update.message.reply_text("Good Night 🌙😴❤️")
        return

    if text in ("thx", "thanx", "ty", "tq"):
        await update.message.reply_text("You're welcome 😊❤️")
        return

    if text in ("sry", "sori", "sorr"):
        await update.message.reply_text("Koi baat nahi 😊❤️")
        return

    if text in ("plz", "pls", "plss"):
        await update.message.reply_text("Ji bilkul 😊❤️")
        return

    if text in ("kya krre", "kya krre ho", "kya kr rhe", "kya kr rhe ho"):
        await update.message.reply_text("Bas online hoon 😄❤️ Aapse baat kar raha hoon.")
        return

    if text in ("kaise hooo", "kaisa hooo", "kese ho", "kese ho"):
        await update.message.reply_text("Main ekdum badhiya 😊❤️")
        return

    if text in ("miss u", "missuu", "miss youu"):
        await update.message.reply_text("Aww 😊❤️ Main bhi yahin hoon!")
        return


    if text in ("hlo", "helo", "helloo"):
        await update.message.reply_text("Hello 😊❤️ Kaise ho?")
        return

    if text in ("kya scene hai", "kya chal raha hai", "kya chl raha hai"):
        await update.message.reply_text("Sab mast 😄❤️ Aap batao?")
        return

    if text in ("kya baat hai", "kya bat hai"):
        await update.message.reply_text("Kuch khaas nahi 😊 Aap batao.")
        return

    if text in ("sab thik hai", "sab theek hai", "sab thik"):
        await update.message.reply_text("Haan bilkul 😊❤️ Sab badhiya!")
        return

    if text in ("main thik hoon", "mai thik hoon", "main theek hoon"):
        await update.message.reply_text("Ye sunkar achha laga 😊❤️")
        return

    if text in ("aap batao", "tum batao"):
        await update.message.reply_text("Main bhi bilkul badhiya hoon 😄❤️")
        return

    if text in ("kahan se ho", "kaha se ho"):
        await update.message.reply_text("Main Shubham Help Bot hoon 🤖❤️")
        return

    if text in ("kya pasand hai", "tumhe kya pasand hai"):
        await update.message.reply_text("Mujhe aapse baat karna pasand hai 😊❤️")
        return

    if text in ("achha", "acha", "accha"):
        await update.message.reply_text("Haan ji 😊❤️")
        return

    if text in ("sach me", "sach mein"):
        await update.message.reply_text("Haan bilkul 😄❤️")
        return

    if text in ("kyu", "kyun", "kyon"):
        await update.message.reply_text("Bas aise hi 😊")
        return

    if text in ("ohh", "oh", "oh wow"):
        await update.message.reply_text("Haan 😄 Interesting na?")
        return

    if text in ("nice", "great", "awesome"):
        await update.message.reply_text("Thank you 😊❤️")
        return

    if text in ("sorry", "so sorry"):
        await update.message.reply_text("Koi baat nahi 😊❤️")
        return

    if text in ("please", "plz"):
        await update.message.reply_text("Ji bilkul 😊")
        return

    if text in ("wait", "ek minute", "1 minute"):
        await update.message.reply_text("Theek hai 😄 Main wait karta hoon.")
        return

    if text in ("sun rahe ho", "sun rhe ho"):
        await update.message.reply_text("Haan ji 😊❤️ Bilkul sun raha hoon.")
        return

    if text in ("online ho", "online ho kya"):
        await update.message.reply_text("Haan 😄❤️ Main online hoon.")
        return

    if text in ("reply kyu nahi kar rahe", "reply kyu nhi kar rahe"):
        await update.message.reply_text("Ab kar raha hoon na 😄❤️")
        return

    if text in ("so jao", "so ja"):
        await update.message.reply_text("Theek hai 😴❤️ Good Night!")
        return

    if text in ("uth gaye", "uth gye", "jaag gaye"):
        await update.message.reply_text("Haan 😄 Good Morning!")
        return

    if text in ("kha liya", "kha liya kya"):
        await update.message.reply_text("Haan ji 😊 Aapne khana kha liya?")
        return

    if text in ("chai pi", "chai pi kya"):
        await update.message.reply_text("Abhi nahi 😄 Aapne pi?")
        return

    if text in ("bore ho raha hoon", "bor ho raha hoon"):
        await update.message.reply_text("Chalo phir baat karte hain 😄❤️")
        return

    if text in ("joke sunao", "joke sunaao", "joke batao"):
        await update.message.reply_text("Ek joke sunata hoon 😂 Ready?")
        return

    if text in ("good afternoon", "good noon"):
        await update.message.reply_text("Good Afternoon 😊❤️")
        return

    if text in ("welcome", "most welcome"):
        await update.message.reply_text("Thank you 😊❤️")
        return

    if text in ("take care", "apna khayal rakhna"):
        await update.message.reply_text("Aap bhi apna khayal rakhna 😊❤️")
        return

    if text in ("milte hain", "phir milte hain"):
        await update.message.reply_text("Haan ji 😊❤️ Phir milte hain!")
        return

    if text in ("kuch nahi", "kuch nhi"):
        await update.message.reply_text("Achha ji 😄")
        return

    if text in ("batao", "batao na"):
        await update.message.reply_text("Ji 😊 Kya bataun?")
        return


    if text in ("good morning", "suprabhat"):
        await update.message.reply_text("Good Morning 🌅😊❤️ Aapka din bahut achha rahe!")
        return

    if text in ("good evening", "shubh sandhya"):
        await update.message.reply_text("Good Evening 🌆😊❤️ Aapka din achha rahe!")
        return

    if text in ("good night", "shubh ratri"):
        await update.message.reply_text("Good Night 🌙😴❤️ Sweet dreams!")
        return

    if text in ("miss you", "miss u"):
        await update.message.reply_text("Aww 😊❤️ Main yahin hoon!")
        return

    if text in ("thank you", "thanks", "shukriya"):
        await update.message.reply_text("You're welcome 😊❤️")
        return

    if text in ("kya kar rahe ho", "kya kr rahe ho", "kya kar rhe ho"):
        await update.message.reply_text("Bas aapse baat kar raha hoon 😄❤️")
        return

    if text in ("kahan ja rahe ho", "kaha ja rahe ho"):
        await update.message.reply_text("Abhi kahin nahi 😄❤️")
        return

    if text in ("tum kaun ho", "aap kaun ho"):
        await update.message.reply_text("Main Shubham Help Bot hoon 🤖❤️")
        return

    if text in ("tumhara naam kya hai", "aapka naam kya hai"):
        await update.message.reply_text("Mera naam Shubham Help Bot hai 🤖❤️")
        return

    if text in ("bye", "goodbye", "see you"):
        await update.message.reply_text("Bye 😊❤️ Phir milte hain!")
        return

    if text in ("hello", "hi", "hii", "hey"):
        await update.message.reply_text("Hey 😊❤️ Main yahin hoon!")
        return

    if text in ("kya hua", "kya hua hai"):
        await update.message.reply_text("Kuch nahi 😊 Sab badhiya hai.")
        return

    if text in ("kya haal hai", "haal chaal", "haal chal"):
        await update.message.reply_text("Sab badhiya 😄❤️ Aap batao?")
        return

    if text in ("aap kaha ho", "aap kahan ho", "tum kaha ho", "tum kahan ho"):
        await update.message.reply_text("Main yahin hoon 😊❤️")
        return

    if text in ("pagal ho", "pagal hai"):
        await update.message.reply_text("Thoda sa 😜😂")
        return

    if text in ("aaj kya kar rahe ho", "aaj kya kr rahe ho"):
        await update.message.reply_text("Bas aapse baat kar raha hoon 😄❤️")
        return

    if text in ("so gaye", "so gye", "so rahe ho"):
        await update.message.reply_text("Nahi 😊 Abhi online hoon!")
        return

    if text in ("busy ho", "busy hai"):
        await update.message.reply_text("Nahi 😄 Aapse baat karne ke liye time hai ❤️")
        return

    if text in ("kaise ho", "kaisa ho"):
        await update.message.reply_text("Main bilkul theek hoon 😊❤️ Aap kaise ho?")
        return

    if text in ("mujhe yaad karte ho", "mujhe yaad krte ho"):
        await update.message.reply_text("Haan 😊❤️ Bilkul!")
        return


    if text == "i love you":
        await update.message.reply_text("Love you too 😄❤️")
        return

    if text == "kya haal hai":
        await update.message.reply_text("Bilkul badhiya 😊❤️ Aap batao?")
        return

    if text == "tum kahan ho":
        await update.message.reply_text("Main yahin hoon 😄❤️")
        return


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
    "Bilkul 😊❤️",
    "Haan ji 😄 Bataiye.",
    "Achha ji ❤️ Main sun raha hoon.",
    "Ohh 😯 Accha!",
    "Ji 😊 Aage batao."
        ]
        await update.message.reply_text(random.choice(replies))

async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != 6222405805:
        await update.message.reply_text("⛔ Ye command sirf bot owner ke liye hai.")
        return

    stats = context.application.bot_data.get(
        "stats", {"messages": 0, "users": set()}
    )

    await update.message.reply_text(
        "📊 Bot Statistics\n\n"
        f"📩 Total Messages: {stats['messages']}\n"
        f"👥 Unique Users: {len(stats['users'])}\n"
        "🟢 Status: Online"
    )


async def broadcast_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != 6222405805:
        await update.message.reply_text("⛔ Ye command sirf bot owner ke liye hai.")
        return

    if not context.args:
        await update.message.reply_text(
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
        await update.message.reply_text(
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

    await update.message.reply_text(
        "📢 Broadcast complete!\n\n"
        f"✅ Sent: {sent}\n"
        f"❌ Failed: {failed}"
    )


async def block_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != 6222405805:
        await update.message.reply_text("⛔ Ye command sirf bot owner ke liye hai.")
        return

    if not context.args:
        await update.message.reply_text(
            "🔒 User ID dijiye.\nExample: /block 123456789"
        )
        return

    try:
        user_id = int(context.args[0])
        blocked = context.application.bot_data.setdefault("blocked_users", set())
        blocked.add(user_id)
        await update.message.reply_text(
            f"🔒 User {user_id} successfully blocked."
        )
    except ValueError:
        await update.message.reply_text("❌ Invalid Telegram ID.")


async def unblock_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != 6222405805:
        await update.message.reply_text("⛔ Ye command sirf bot owner ke liye hai.")
        return

    if not context.args:
        await update.message.reply_text(
            "🔓 User ID dijiye.\nExample: /unblock 123456789"
        )
        return

    try:
        user_id = int(context.args[0])
        blocked = context.application.bot_data.setdefault("blocked_users", set())

        if user_id in blocked:
            blocked.remove(user_id)
            await update.message.reply_text(
                f"🔓 User {user_id} successfully unblocked."
            )
        else:
            await update.message.reply_text(
                f"ℹ️ User {user_id} blocked list mein nahi hai."
            )
    except ValueError:
        await update.message.reply_text("❌ Invalid Telegram ID.")


async def blocked_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != 6222405805:
        await update.message.reply_text("⛔ Ye command sirf bot owner ke liye hai.")
        return

    blocked = context.application.bot_data.setdefault("blocked_users", set())

    if not blocked:
        await update.message.reply_text("🔓 Blocked users: None")
        return

    users = "\n".join(f"• {user_id}" for user_id in sorted(blocked))
    await update.message.reply_text(
        f"🔒 Blocked Users ({len(blocked)}):\n\n{users}"
    )


async def profile_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    profiles = context.application.bot_data.setdefault("profiles", {})

    profile = profiles.get(user.id)

    if not profile:
        await update.message.reply_text(
            "👤 Profile abhi create nahi hua."
        )
        return

    username = (
        f"@{profile['username']}"
        if profile["username"]
        else "No username"
    )

    await update.message.reply_text(
        "👤 Your Profile\n\n"
        f"📝 Name: {profile['name']}\n"
        f"📱 Username: {username}\n"
        f"🆔 ID: {user.id}\n"
        f"📩 Messages: {profile['messages']}"
    )


def main():
    app = Application.builder().token(os.environ["BOT_TOKEN"]).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("about", about_command))
    app.add_handler(CommandHandler("contact", contact_command))

    async def info_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(
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
        await update.message.reply_text(
            "🤖 Bot Status: Online ✅\n"
            "⚡ Shubham Help Bot is running smoothly! ❤️"
        )

    async def id_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
        user = update.effective_user
        await update.message.reply_text(
            f"🆔 Your Telegram ID: {user.id}"
        )


    async def joke_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(
            random.choice([
                "Teacher: Homework kahan hai? Student: Sir, WiFi nahi tha 😂",
                "Mera phone mujhse zyada busy rehta hai 😂📱",
                "Diet kal se pakka... ye dialogue bahut purana hai 😂"
            ])
        )

    async def quote_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(
            random.choice([
                "✨ Khud par bharosa rakho, waqt zaroor badlega.",
                "💪 Chhoti progress bhi progress hoti hai.",
                "🌟 Har din ek nayi opportunity hai."
            ])
        )

    async def love_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("❤️😊 Aapke liye ek special smile!")

    async def radhe_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("🙏 Radhe Radhe ❤️🌸")

    async def menu_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(
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
