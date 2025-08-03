import asyncio
from utils import get_filtered_coins
from web import app as web_app
from fastapi import FastAPI
import uvicorn
import os
from license import check_license
from dotenv import load_dotenv
from telegram import Bot

load_dotenv()

bot_token = os.getenv("BOT_TOKEN")
channel_id = os.getenv("CHANNEL_ID")

if not check_license():
    print("❌ License verification failed.")
    exit()

bot = Bot(token=bot_token)
sent_symbols = set()

async def notify():
    global sent_symbols
    coins = await get_filtered_coins()
    for coin in coins:
        if coin["symbol"] not in sent_symbols:
            message = f"""
🚨 فرصة تداول جديدة 🚨

📌 العملة: {coin['symbol']}
💰 السعر الحالي: {coin['price']}$
🎯 الهدف الأول: {coin['target']}$
🛑 وقف الخسارة: {coin['stop_loss']}$
📊 حجم التداول: {coin['volume']}$ 
📈 التغير 24h: {coin['change']}%
📉 RSI: {coin['rsi']}

#MEXC #Crypto
"""
            await bot.send_message(chat_id=channel_id, text=message)
            sent_symbols.add(coin["symbol"])

async def start_bot():
    while True:
        await notify()
        await asyncio.sleep(600)  # كل 10 دقائق

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(start_bot())

# ✅ Health Check Endpoint
@app.get("/")
async def root():
    return {"status": "Bot is running on Render"}

# ✅ Mount واجهة الويب الخاصة بك
app.mount("/web", web_app)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
