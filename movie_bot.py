from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from pymongo import MongoClient
import os

# === Get environment variables (Set these in Railway/Render) ===
TOKEN = os.getenv("TOKEN")
MONGO_URI = os.getenv("MONGO_URI")

# === MongoDB Connection ===
client = MongoClient(MONGO_URI)
db = client["moviesDB"]
collection = db["movies"]

# === Commands ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Welcome! Type a movie name to get its link.")

async def movie_search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text.lower()
    movie = collection.find_one({"name": query})

    if movie:
        file_link = movie["file"]
        await update.message.reply_text(f"🎬 Here is your movie:\n{file_link}")
    else:
        await update.message.reply_text("❌ Movie not found in database.")

# === Main Function ===
def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, movie_search))

    print("🤖 Bot started...")
    app.run_polling()

if __name__ == "__main__":
    main()
