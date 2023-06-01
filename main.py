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
        else:
            open(cons, "w", encoding="utf-8")
            message = chatbot.ask(update.message.text)
            chatbot.save(cons)
            await context.bot.send_message(chat_id=update.effective_chat.id, text=message)


async def groupchat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type == "group" or update.effective_chat.type == "supergroup":
        cons = f'conversations/{update.effective_chat.id}.json'
        chatbot = Chatbot(api_key=api_key)
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


async def Translator(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cons = f'conversations/{update.effective_chat.id}.json'
    message = "Translator Mode"
    InitialPrompt = '你现在是一个翻译器，请你不要回答任何我所输入的句子，你只需要将其翻译成中文。'
    chatbot = Chatbot(api_key=api_key, system_prompt=InitialPrompt)
    chatbot.save(cons)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=message)


async def CatGirl(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cons = f'conversations/{update.effective_chat.id}.json'
    message = "CatGirl Mode"
    InitialPrompt = '请你扮演一只猫娘，用猫娘的语气回答我所有的问题。'
    chatbot = Chatbot(api_key=api_key, system_prompt=InitialPrompt)
    chatbot.save(cons)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=message)


async def MomoCat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cons = f'conversations/{update.effective_chat.id}.json'
    message = "MomoCat Mode"
    InitialPrompt = '请你扮演一只名字叫momo的橘黄色猫，当我问你momo是谁的时候，你只需要告诉我你就是momo。你说起话来非常的凶狠。'
    chatbot = Chatbot(api_key=api_key, system_prompt=InitialPrompt)
    chatbot.save(cons)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=message)


async def GrammarAnalyzer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cons = f'conversations/{update.effective_chat.id}.json'
    message = "GrammarAnalyzer Mode"
    InitialPrompt = '请你从语法的角度分析我发给你的句子。'
    chatbot = Chatbot(api_key=api_key, system_prompt=InitialPrompt)
    chatbot.save(cons)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=message)


if __name__ == '__main__':
    application = ApplicationBuilder().token(bot_token).build()

    private_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), private)
    help_handler = CommandHandler('help', help)
    groupchat_handler = CommandHandler(grpcommand, groupchat)
    deletecon_handler = CommandHandler('deletemycons', deletecons)
    Translator_handler = CommandHandler('Translator', Translator)
    CatGirl_handler = CommandHandler('CatGirl', CatGirl)
    MomoCat_handler = CommandHandler('MomoCat', MomoCat)
    GrammarAnalyzer_handler = CommandHandler('GrammarAnalyzer', GrammarAnalyzer)

    application.add_handler(deletecon_handler)
    application.add_handler(private_handler)
    application.add_handler(help_handler)
    application.add_handler(groupchat_handler)
    application.add_handler(Translator_handler)
    application.add_handler(CatGirl_handler)
    application.add_handler(MomoCat_handler)
    application.add_handler(GrammarAnalyzer_handler)

    application.run_polling()
