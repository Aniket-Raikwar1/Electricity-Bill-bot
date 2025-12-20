import logging
import os
import threading
from flask import Flask
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

# Import our merged scraper
from scraper_up import BillScraper

# Load Token
load_dotenv()
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

import logging
import os
import threading
from flask import Flask
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

# Import our merged scraper
from scraper_up import BillScraper

# Load Token
load_dotenv()
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# --- PART 1: The Web Server Setup ---
app = Flask(__name__)

@app.route('/')
def health_check():
    return "MP Electricity Bot is Running! ⚡"

def run_web_server():
    # Render assigns a port automatically. We must read it from the environment.
    port = int(os.environ.get("PORT", 10000))
    # host='0.0.0.0' makes the server accessible to Render
    app.run(host="0.0.0.0", port=port)

# --- PART 2: Your Bot Handlers ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.effective_user.first_name
    await update.message.reply_text(
        f"👋 Hi {user_name}!\n\n"
        "I am the MP Electricity Bot. \n"
        "Send me your **IVRS Number** and I will download your latest bill."
    )

async def handle_ivrs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ivrs_number = update.message.text.strip().upper() # Clean up the input
    
    # Basic validation
    if len(ivrs_number) < 5:
        await update.message.reply_text("❌ That doesn't look like a valid IVRS number. Please try again.")
        return

    await update.message.reply_text(f"🔍 Searching for IVRS: {ivrs_number}...\nPlease wait up to 30 seconds.")

    # Initialize Scraper
    scraper = BillScraper()
    
    # Run the scraping task
    pdf_path = scraper.fetch_bill(ivrs_number)

    if pdf_path and os.path.exists(pdf_path):
        await update.message.reply_text("✅ Bill found! Uploading now...")
        
        # Send the file
        with open(pdf_path, 'rb') as doc:
            await update.message.reply_document(document=doc, filename=os.path.basename(pdf_path))
    else:
        await update.message.reply_text(
            "❌ Could not download the bill.\n"
            "Possible reasons:\n"
            "1. IVRS Number is wrong.\n"
            "2. The website is slow/down.\n"
            "3. No bill generated for this month yet."
        )

# --- PART 3: Main Execution ---
if __name__ == '__main__':
    if not TOKEN:
        print("⚠️ Error: Please put your TELEGRAM_BOT_TOKEN in the .env file")
    else:
        # 1. Start the dummy web server in a separate thread
        # This allows the Flask server and the Telegram bot to run at the same time
        print("Starting dummy web server...")
        threading.Thread(target=run_web_server).start()

        # 2. Start the Bot
        print("Starting bot...")
        application = ApplicationBuilder().token(TOKEN).build()
        application.add_handler(CommandHandler('start', start))
        application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_ivrs))
        
        application.run_polling()