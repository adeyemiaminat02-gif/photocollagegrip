import os
import io
import logging
from collections import defaultdict
from PIL import Image
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Setup logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Temporary store for user photos: {chat_id: [BytesIO, BytesIO, ...]}
USER_PHOTOS = defaultdict(list)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome! Send me up to 4 photos, then type /collage to create your grid."
    )

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    
    # Get the highest resolution photo version
    photo_file = await update.message.photo[-1].get_file()
    
    # Download photo into memory
    photo_bytes = io.BytesIO()
    await photo_file.download_to_memory(photo_bytes)
    photo_bytes.seek(0)
    
    USER_PHOTOS[chat_id].append(photo_bytes)
    count = len(USER_PHOTOS[chat_id])
    
    await update.message.reply_text(f"📸 Photo received! ({count}/4)")

async def make_collage(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    photos = USER_PHOTOS[chat_id]
    
    if not photos:
        await update.message.reply_text("❌ You haven't sent any photos yet!")
        return
        
    await update.message.reply_text("⏳ Generating your collage grid...")
    
    # Open images with Pillow
    images = [Image.open(p) for p in photos[:4]]
    
    # Target size for each grid item (e.g., 500x500 pixels)
    thumb_size = (500, 500)
    resized_images = [img.resize(thumb_size) for img in images]
    
    # Determine grid size (2x2 max)
    collage_width = thumb_size[0] * 2
    collage_height = thumb_size[1] * 2
    
    # Create blank canvas
    collage = Image.new("RGB", (collage_width, collage_height), color="white")
    
    # Paste images into grid positions
    positions = [
        (0, 0),                  # Top Left
        (thumb_size[0], 0),      # Top Right
        (0, thumb_size[1]),      # Bottom Left
        (thumb_size[0], thumb_size[1]) # Bottom Right
    ]
    
    for idx, img in enumerate(resized_images):
        collage.paste(img, positions[idx])
        
    # Save final collage to memory buffer
    output_buffer = io.BytesIO()
    collage.save(output_buffer, format="JPEG")
    output_buffer.seek(0)
    
    # Clear user store after generating
    USER_PHOTOS[chat_id].clear()
    
    # Send back to Telegram
    await update.message.reply_photo(photo=output_buffer, caption="🎉 Here is your collage grid!")

def main():
    # Token pulled from environment variable
    TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    if not TOKEN:
        logger.error("No TELEGRAM_BOT_TOKEN found in environment variables!")
        return

    # Build the application
    app = Application.builder().token(TOKEN).build()

    # Handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("collage", make_collage))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))

    # Start long polling
    logger.getLogger().info("Bot started via Long Polling...")
    app.run_polling()

if __name__ == '__main__':
    main()
