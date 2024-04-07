from hydrogram import Client, filters
from hydrogram.enums import ChatAction
from src.db import NotesDB
import asyncio
import re


@Client.on_message(filters.command("delete"))
async def delete_url(c, m):
    notes = NotesDB()
    await m.reply_chat_action(ChatAction.TYPING)
    user_id = m.from_user.id
    filename = f"{user_id}"
    if user_id == 5665225938:
        filename = "v2ray"
    text = m.text
    if m.reply_to_message:
        text = m.reply_to_message.text
    urls = re.findall(
        r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+",
        text,
    )
    if not urls:
        err = await m.reply_text("Vui lòng cung cấp URL")
        await asyncio.sleep(10)
        await c.delete_messages(m.chat.id, err.id)
        await m.delete()
        return
    worked = None
    for url in urls:
        worked = False
        try:
            notes.remove(filename, url)
            worked = True
        except Exception as e:
            err = await m.reply_text(f"Error: {e}")
            await asyncio.sleep(10)
            await c.delete_messages(m.chat.id, err.id)
    if worked:
        done = await m.reply_text(f"Đã xoá {len(urls)} URL")
        await asyncio.sleep(10)
        await c.delete_messages(m.chat.id, done.id)
    await m.delete()


@Client.on_message(filters.command("removefromsharelist"))
async def delete_share_url(c, m):
    notes = NotesDB()
    await m.reply_chat_action(ChatAction.TYPING)
    text = m.text
    if m.reply_to_message:
        text = m.reply_to_message.text
    urls = re.findall(
        r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+",
        text,
    )
    if not urls:
        err = await m.reply_text("Vui lòng cung cấp URL")
        await asyncio.sleep(10)
        await c.delete_messages(m.chat.id, err.id)
        await m.delete()
        return
    worked = None
    for url in urls:
        worked = False
        try:
            notes.remove("share", url)
            worked = True
        except Exception as e:
            err = await m.reply_text(f"Error: {e}")
            await asyncio.sleep(10)
            await c.delete_messages(m.chat.id, err.id)
    if worked:
        done = await m.reply_text(f"Đã xoá {len(urls)} URL")
        await asyncio.sleep(10)
        await c.delete_messages(m.chat.id, done.id)
    await m.delete()