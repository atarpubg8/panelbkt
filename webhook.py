import os
import json
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = "8678801609:AAGJRCbWZoypAp-Tj6uVD5vthSYi0bVk8AU"  # ← Telegram'dan aldığın token'ı buraya yapıştır

app = Application.builder().token(TOKEN).build()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📂 Listele", callback_data="list")],
        [InlineKeyboardButton("▶️ Çalıştır", callback_data="run")],
        [InlineKeyboardButton("⏹️ Durdur", callback_data="stop")],
        [InlineKeyboardButton("🗑️ Sil", callback_data="delete")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Merhaba! Butonlardan birini seç:", reply_markup=reply_markup)

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(f"✅ {query.data} butonuna tıkladın!")

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button))

async def webhook(request):
    if request.method == "POST":
        body = await request.body()
        data = json.loads(body)
        update = Update.de_json(data, app.bot)
        await app.process_update(update)
        return {"status": "ok"}, 200
    return {"status": "ready"}, 200

async def handle(request):
    return await webhook(request)
