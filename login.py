import logging
from telegram import Update
from telegram.ext import (
    filters,
    MessageHandler,
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)
from telegram import InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import InlineQueryHandler

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Hola, soy el bot de Racama, si quieres "
        "interactuar conmigo usa los siguientes comandos: /start,/caps\n",
    )


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    myFile = open("/home/raulas/PycharmProjects/token.txt", "r")
    token_raul_bello = myFile.read().split("\n")[1]

    myFile.close()
    if update.effective_chat.id.__eq__(token_raul_bello):
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
    myFile = open("/home/raulas/PycharmProjects/token.txt", "r")
    token_raul = myFile.read().split("\n")[0]

    myFile.close()
    application = ApplicationBuilder().token(token_raul.strip()).build()
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
    caps_handler = CommandHandler("caps", caps)
    start_handler = CommandHandler("start", start)
    application.add_handler(start_handler)
    application.add_handler(echo_handler)
    application.add_handler(caps_handler)
    inline_caps_handler = InlineQueryHandler(inline_caps)
    application.add_handler(inline_caps_handler)
    # Other handlers
    unknown_handler = MessageHandler(filters.COMMAND, unknown)
    application.add_handler(unknown_handler)

    application.run_polling()
