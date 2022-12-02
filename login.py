import logging

import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    filters,
    MessageHandler,
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    CallbackQueryHandler,
)
from telegram import InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import InlineQueryHandler
from dotenv import load_dotenv
import os

load_dotenv()
token_raul = os.environ.get("bot_token")
token_raul_bello = os.environ.get("raul_bello")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Hola, soy el bot de Racama, si quieres "
        "interactuar conmigo usa los siguientes comandos: /start,/caps y para responder un acertijo usa /quiz\n",
    )


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_chat.id == (int(token_raul_bello)):
        await context.bot.send_message(
            chat_id=update.effective_chat.id, text="Raúl eres bien tonto"
        )
        return

    await context.bot.send_message(
        chat_id=update.effective_chat.id, text=update.message.text
    )


async def caps(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if len(update.effective_message.text.split()) <= 1:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="No has introducido texto, el comando se utiliza de "
            "la siguiente forma: /CAPS 'texto a pasar a mayúsculas'",
        )
        return

    text_caps = " ".join(context.args).upper()
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)


async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Sends a message with three inline buttons attached."""
    keyboard = [
        [
            InlineKeyboardButton("El suelo", callback_data="1"),
            InlineKeyboardButton("El jabón", callback_data="2"),
        ],
        [InlineKeyboardButton("Me da igual", callback_data="3")],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "Si se te cae el jabón al suelo, ¿está el suelo limpio o el jabón sucio?:",
        reply_markup=reply_markup,
    )


async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Sends a message with three inline buttons attached."""
    keyboard = [
        [
            InlineKeyboardButton("Carne", callback_data="4"),
            InlineKeyboardButton("Pescado", callback_data="5"),
        ],
        [InlineKeyboardButton("Cerrar", callback_data="6")],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text("Qué quieres comer?:", reply_markup=reply_markup)


async def menu_carne(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Sends a message with three inline buttons attached."""
    keyboard = [
        [
            InlineKeyboardButton("Cerdo", callback_data="7"),
            InlineKeyboardButton("Pollo", callback_data="8"),
        ],
        [InlineKeyboardButton("Atrás", callback_data="9")],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text("Qué tipo de cane?:", reply_markup=reply_markup)


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    await query.answer()
    if query.data == "1":
        await query.edit_message_text(text=f"Puede ser")
    elif query.data == "2":
        await query.edit_message_text(text=f"Bien pensado")
    elif query.data == "3":
        await query.edit_message_text(text=f"Hay que ser bien maricón")
    elif query.data == "4":
        print("Carne")
    # Display menu_carne

    elif query.data == "5":
        print("Pescado")
        # Display menu_pescado
    elif query.data == "6":
        print("Atras")
        # Goback


async def inline_caps(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.inline_query.query
    if not query:
        return
    results = []
    results.append(
        InlineQueryResultArticle(
            id=query.upper(),
            title="Caps",
            input_message_content=InputTextMessageContent(query.upper()),
        )
    )
    await context.bot.answer_inline_query(update.inline_query.id, results)


async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Sorry, I didn't understand that command.",
    )


if __name__ == "__main__":

    application = ApplicationBuilder().token(token_raul).build()
    # initialize handlers
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
    caps_handler = CommandHandler("caps", caps)
    start_handler = CommandHandler("start", start)
    buttons_handler = CommandHandler("quiz", buttons)
    button_handler = CallbackQueryHandler(button)
    menu_hanlder = CommandHandler("menu", menu)
    # Add handlers to application
    application.add_handler(start_handler)
    application.add_handler(echo_handler)
    application.add_handler(caps_handler)
    application.add_handler(buttons_handler)
    application.add_handler(button_handler)
    application.add_handler(menu_hanlder)

    inline_caps_handler = InlineQueryHandler(inline_caps)
    application.add_handler(inline_caps_handler)
    # Other handlers
    unknown_handler = MessageHandler(filters.COMMAND, unknown)
    application.add_handler(unknown_handler)

    application.run_polling()
