import logging
import os
import asyncio
import random
from telegram import Update
from telegram.ext import Application, MessageHandler, ContextTypes, filters
from telegram.error import Forbidden, BadRequest

logging.basicConfig(level=logging.INFO)

TOKEN   = os.environ["MEDIA_BOT_TOKEN"]
ALLOWED = {8034872992, 8793739928}

VIDEOS = [
    "BAACAgQAAxkBAAMDajyM4mBmeFxarFZFWzGfp8GPsGkAAgweAAI4K-BRq0SygxDtGJY8BA",
    "BAACAgQAAxkBAAMEajyM4vRUYDJsK8rVo91t9KjTcM0AAg0eAAI4K-BRRRUpiq6HjlM8BA",
    "BAACAgQAAxkBAAMFajyM4pikBM-AqihilvktT2zTkTAAAg8eAAI4K-BROTuOSt0z_8k8BA",
    "BAACAgQAAxkBAAMGajyM4hytOdu4MWv6gVUa5yqrWOMAAhAeAAI4K-BRkHlu6d0F9ag8BA",
    "BAACAgQAAxkBAAMHajyM4ssn3Wi63PTFCW3EYOqj-lEAAhEeAAI4K-BRVOlQXSXmSRU8BA",
    "BAACAgQAAxkBAAMIajyM4tbQAAGiz8eorcrOsIWpGa2DAAISHgACOCvgUe_uvw5XFpanPAQ",
    "BAACAgQAAxkBAAMJajyM4ntuJhZ5VFwlVN0HOn8vtKgAAhMeAAI4K-BRwOiAkNP-t_08BA",
    "BAACAgQAAxkBAAMKajyM4rI2OoMlwXo4iHFrg2GUctQAAhQeAAI4K-BRSwZ_h4Qk4ko8BA",
    "BAACAgQAAxkBAAMLajyM4h0oFUwW2HJ3W7VkfKavDKsAAhUeAAI4K-BRPCWHVjaK4Vc8BA",
]

sending_chats = {}

async def send_loop(ctx, cid):
    while sending_chats.get(cid):
        video = random.choice(VIDEOS)
        try:
            await ctx.bot.send_video(cid, video)
        except Forbidden:
            logging.warning(f"Forbidden: {cid} — dayandırıldı")
            sending_chats[cid] = False
            break
        except BadRequest as e:
            logging.warning(f"BadRequest: {e} — dayandırıldı")
            sending_chats[cid] = False
            break
        except Exception as e:
            logging.warning(f"Xəta: {e}")
        await asyncio.sleep(1)

async def handle_message(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.effective_user:
        return

    uid  = update.effective_user.id
    text = (update.message.text or "").strip()

    if uid not in ALLOWED:
        return

    cid = update.effective_chat.id

    try:
        member = await ctx.bot.get_chat_member(cid, ctx.bot.id)
        if member.status not in ("member", "administrator"):
            return
    except Exception:
        return

    if text == ".send cp":
        if sending_chats.get(cid):
            return
        sending_chats[cid] = True
        asyncio.create_task(send_loop(ctx, cid))

    elif text.startswith("/dur"):
        sending_chats[cid] = False

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT, handle_message))
    app.add_handler(MessageHandler(filters.COMMAND, handle_message))
    print("Media botu başladı...")
    app.run_polling(drop_pending_updates=True, allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
