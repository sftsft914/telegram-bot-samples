"""
Menu Bot — demonstrates commands, inline keyboards, and callback query handling.
"""

import logging
import os

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.environ.get("BOT_TOKEN", "PUT-YOUR-TOKEN-HERE")

MAIN_MENU = [
    [InlineKeyboardButton("📋 About", callback_data="about")],
    [InlineKeyboardButton("💰 Pricing", callback_data="pricing")],
    [InlineKeyboardButton("📞 Contact", callback_data="contact")],
]

CONTENT = {
    "about": "This bot was built as a portfolio sample.\n\n"
             "It shows command handling, inline keyboards, and callback "
             "routing — the building blocks of most Telegram bots.",
    "pricing": "💵 Sample pricing tiers:\n\n"
               "• Basic bot — from $150\n"
               "• Bot + database — from $300\n"
               "• Bot + payments/admin panel — from $500\n\n"
               "Final price depends on scope.",
    "contact": "📩 Reach out any time — happy to discuss your bot idea "
               "and give a free estimate.",
}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "👋 Welcome! Choose an option below:",
        reply_markup=InlineKeyboardMarkup(MAIN_MENU),
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Available commands:\n"
        "/start — show the main menu\n"
        "/help — show this message"
    )


async def menu_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    section = query.data
    text = CONTENT.get(section, "Unknown option.")

    back_button = InlineKeyboardMarkup(
        [[InlineKeyboardButton("⬅️ Back to menu", callback_data="back")]]
    )

    if section == "back":
        await query.edit_message_text(
            "👋 Welcome! Choose an option below:",
            reply_markup=InlineKeyboardMarkup(MAIN_MENU),
        )
        return

    await query.edit_message_text(text, reply_markup=back_button)


def main() -> None:
    if BOT_TOKEN == "PUT-YOUR-TOKEN-HERE":
        raise SystemExit("Set BOT_TOKEN env var before running.")

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CallbackQueryHandler(menu_callback))

    logger.info("Bot starting (polling)...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
