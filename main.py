from revChatGPT.V3 import Chatbot
from telegram import Update
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes
import logging
import os
import json

try:
    with open("config.json", encoding="utf-8") as f:
        auth = json.loads(f.read())
except FileNotFoundError:
    print(f"Error: config.json does not exist")

print(auth[0]['api_key'])

api_key = auth[0]['api_key']
bot_token = auth[0]['token']
grpcommand = auth[0]['groupcommand']

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


async def private(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type == "private":
        cons = f'conversations/{update.effective_chat.id}.json'
        chatbot = Chatbot(api_key=api_key)
        if os.path.exists(cons):
            chatbot.load(cons)
            message = chatbot.ask(update.message.text)

            chatbot.save(cons)
            await context.bot.send_message(chat_id=update.effective_chat.id, text=message)
            #chatbot.reset()
        else:
            open(cons, "w", encoding="utf-8")
            message = chatbot.ask(update.message.text)
            chatbot.save(cons)
            await context.bot.send_message(chat_id=update.effective_chat.id, text=message)
            #chatbot.reset()


async def groupchat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type == "group" or update.effective_chat.type == "supergroup":
        cons = f'conversations/{update.effective_chat.id}.json'
        chatbot = Chatbot(api_key=api_key)
        if os.path.exists(cons):
            chatbot.load(cons)
            message = chatbot.ask(update.message.text)
            chatbot.save(cons)
            await context.bot.send_message(chat_id=update.effective_chat.id, text=message)
            chatbot.reset()
        else:
            open(cons, "w", encoding="utf-8")
            message = chatbot.ask(update.message.text)
            chatbot.save(cons)
            await context.bot.send_message(chat_id=update.effective_chat.id, text=message)
            chatbot.reset()


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = "When in private chat, ask questions directly \nWhen in group chat, use '/hiyo questions'"
    await context.bot.send_message(chat_id=update.effective_chat.id, text=message)


async def deletecons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cons = f'conversations/{update.effective_chat.id}.json'
    if os.path.exists(cons):
        os.remove(cons)
        message = "Conversation deleted"
        await context.bot.send_message(chat_id=update.effective_chat.id, text=message)
    else:
        message = "No conversations"
        await context.bot.send_message(chat_id=update.effective_chat.id, text=message)


if __name__ == '__main__':

    application = ApplicationBuilder().token(bot_token).build()

    private_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), private)
    help_handler = CommandHandler('help', help)
    groupchat_handler = CommandHandler(grpcommand, groupchat)
    deletecon_handler = CommandHandler('deletemycons', deletecons)

    application.add_handler(deletecon_handler)
    application.add_handler(private_handler)
    application.add_handler(help_handler)
    application.add_handler(groupchat_handler)

    application.run_polling()
