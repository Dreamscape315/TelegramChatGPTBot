from revChatGPT.V3 import Chatbot
from telegram import Update
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes
import logging
import os
import json

try:
    with open("config/config.json", encoding="utf-8") as f:
        auth = json.loads(f.read())
except FileNotFoundError:
    print(f"Error: config.json does not exist")

try:
    with open("config/Prompts.json", encoding="utf-8") as s:
        prompt = json.loads(s.read())
        DictPrompt = prompt[0]
        promptSet = set(prompt[0])
        PromptFrozenSet = frozenset(promptSet)
except FileNotFoundError:
    print(f"Error: Prompts.json does not exist")

api_key = auth[0]['api_key']
bot_token = auth[0]['token']
grpcommand = auth[0]['groupcommand']
GPT3 = "gpt-3.5-turbo-0613"
GPT4 = "gpt-4-0613"

chatbot = Chatbot(api_key=api_key, engine=GPT3)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


async def Private(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type == "private":
        cons = f'conversations/{update.effective_chat.id}.json'
        if os.path.exists(cons):
            chatbot.load(cons)
            message = chatbot.ask(update.message.text)
            chatbot.save(cons)
            await context.bot.send_message(chat_id=update.effective_chat.id, text=message)
        else:
            open(cons, "w", encoding="utf-8")
            message = chatbot.ask(update.message.text)
            chatbot.save(cons)
            await context.bot.send_message(chat_id=update.effective_chat.id, text=message)


async def GroupChat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type == "group" or update.effective_chat.type == "supergroup":
        cons = f'conversations/{update.effective_chat.id}.json'
        if os.path.exists(cons):
            chatbot.load(cons)
            message = chatbot.ask(update.message.text)
            chatbot.save(cons)
            await context.bot.send_message(chat_id=update.effective_chat.id, text=message)
        else:
            open(cons, "w", encoding="utf-8")
            message = chatbot.ask(update.message.text)
            chatbot.save(cons)
            await context.bot.send_message(chat_id=update.effective_chat.id, text=message)


async def PromptModeChange(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("came in PMC func")
    cons = f'conversations/{update.effective_chat.id}.json'
    global PromptCommand
    global Info
    if update.effective_chat.type == "group" or update.effective_chat.type == "supergroup":
        At = update.message.text.rfind("@")
        PromptCommand = update.message.text[1:At]
    else:
        PromptCommand = update.message.text[1:]
    Info = PromptCommand.capitalize() + ' Mode'
    InitialPrompt = DictPrompt[PromptCommand]
    chatbot.reset(system_prompt=InitialPrompt)
    chatbot.save(cons)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=Info)


async def Help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = "When in private chat, ask questions directly \nWhen in group chat, use '/hiyo questions'"
    await context.bot.send_message(chat_id=update.effective_chat.id, text=message)


async def Deletecons(update: Update, context: ContextTypes.DEFAULT_TYPE):
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

    PrivateChat_Handler = MessageHandler(filters.TEXT & (~filters.COMMAND), Private)
    GroupChat_Handler = CommandHandler(grpcommand, GroupChat)
    PromptModeChange_Handler = CommandHandler(PromptFrozenSet, PromptModeChange)
    Help_Handler = CommandHandler('help', Help)
    Deletecon_Handler = CommandHandler('deletemycons', Deletecons)

    application.add_handler(PrivateChat_Handler)
    application.add_handler(GroupChat_Handler)
    application.add_handler(PromptModeChange_Handler)
    application.add_handler(Help_Handler)
    application.add_handler(Deletecon_Handler)

    application.run_polling()
