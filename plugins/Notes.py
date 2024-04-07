import re, time
from hydrogram import Client, filters, enums
from hydrogram.enums import ChatAction
from db.note import save_url, remove_url, get_all, check_all
from lib.env import config_tool


@Client.on_message(filters.command("add"))
def add_url(c, m):
    m.reply_chat_action(ChatAction.TYPING)
    user_id = m.from_user.id
    filename = f"{user_id}"
    if m.from_user.id == 5665225938:
        filename = "v2ray"
    text = m.text
    if m.reply_to_message:
        text = m.reply_to_message.text
    urls = re.findall(
        r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+",
        text,
    )
    if not urls:
        err = m.reply_text("Vui lòng cung cấp URL")
        time.sleep(10)
        c.delete_messages(m.chat.id, err.id)
        m.delete()
        return
    l = 0
    for url in urls:
        try:
            save_url(filename, url)
            l += 1
        except Exception as e:
            pass
    if l != len(urls):
        x = len(urls) - l
        temp = m.reply(f"{x} URL trùng lặp sẽ không được thêm lại")
        time.sleep(5)
        c.delete_messages(m.chat.id, temp.id)
    done = m.reply_text(f"Đã thêm {l} URL")
    time.sleep(10)
    c.delete_messages(m.chat.id, done.id)
    m.delete()


@Client.on_message(filters.command("delete"))
def delete_url(c, m):
    m.reply_chat_action(ChatAction.TYPING)
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
        err = m.reply_text("Vui lòng cung cấp URL")
        time.sleep(10)
        c.delete_messages(m.chat.id, err.id)
        m.delete()
        return
    for url in urls:
        worked = False
        try:
            remove_url(filename, url)
            worked = True
        except Exception as e:
            err = m.reply_text(f"Error: {e}")
            time.sleep(10)
            c.delete_messages(m.chat.id, err.id)
    if worked == True:
        done = m.reply_text(f"Đã xoá {len(urls)} URL")
        time.sleep(10)
        c.delete_messages(m.chat.id, done.id)
    m.delete()


@Client.on_message(filters.command("checkifunavailable"))
def check_all_urls(c, m):
    m.reply_chat_action(ChatAction.TYPING)
    user_id = m.from_user.id
    filename = f"{user_id}"
    if m.from_user.id == 5665225938:
        filename = "v2ray"
    try:
        removed_urls = check_all(filename)
        if removed_urls:
            removed_urls_str = "\n".join(removed_urls)
            m.reply_text(f" Đã xoá {len(removed_urls)} URL(s):\n{removed_urls_str}")
        else:
            err = m.reply_text("No URLs were removed")
            time.sleep(10)
            c.delete_messages(m.chat.id, err.id)
    except Exception as e:
        err = m.reply_text(f"Error: {e}")
        time.sleep(10)
        c.delete_messages(m.chat.id, err.id)


@Client.on_message(filters.command("getmylist"))
def get_all_urls(c, m):
    m.reply_chat_action(ChatAction.TYPING)
    if m.chat.type != enums.ChatType.PRIVATE:
        m.reply("Vui lòng thực hiện thao tác này ở khu vực riêng tư!", quote=True)
        return
    user_id = m.from_user.id
    filename = f"{user_id}"
    if m.from_user.id == 5665225938:
        filename = "v2ray"
    try:
        urls = get_all(filename)
        if urls:
            urls_str = "\n".join(urls)
            m.reply_text(f"Tìm thấy {len(urls)} URL:\n{urls_str}")
        else:
            err = m.reply_text("No URLs found")
            time.sleep(10)
            c.delete_messages(m.chat.id, err.id)
    except Exception as e:
        err = m.reply_text(f"Error: {e}")
        time.sleep(10)
        c.delete_messages(m.chat.id, err.id)


@Client.on_message(filters.command("get"))
def get_urls(c, m):
    m.reply_chat_action(ChatAction.TYPING)
    user_id = m.from_user.id
    filename = f"{user_id}"
    m.reply(
        f"Đây là liên kết của bạn, được chỉnh sửa bằng lệnh /add và /delete do bạn thực thi:\n__--{config_tool}/get/{filename}--__\n\n**Đây là liên kết chung được thêm bởi lệnh /share, có thể được bổ sung bởi mọi người:\n__--{config_tool}/get/share--__",
        quote=True,
    )
