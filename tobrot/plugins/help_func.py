#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) 5MysterySD | Anasty17 [MLTB]
#
# Copyright 2022 - TeamTele-LeechX
# 
# This is Part of < https://github.com/5MysterySD/Tele-LeechX >
# All Right Reserved

from asyncio import sleep as asleep
from os import path as opath, remove as oremove
from time import time
from telegraph import upload_file
from subprocess import check_output
from psutil import disk_usage, cpu_percent, swap_memory, cpu_count, virtual_memory, net_io_counters, boot_time
from pyrogram import enums, Client
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, InputMediaPhoto, Message

from tobrot import *
from tobrot.helper_funcs.display_progress import humanbytes, TimeFormatter
from tobrot.bot_theme.themes import BotTheme
from tobrot.plugins import getUserOrChaDetails

TGH_LIMIT = 5242880*2

async def stats(client: Client, message: Message):
    user_id, _ = getUserOrChaDetails(message)
    stats = (BotTheme(user_id)).STATS_MSG_1
    if opath.exists('.git'):
        last_commit = check_output(["git log -1 --date=format:'%I:%M:%S %p %d %B, %Y' --pretty=format:'%cr ( %cd )'"], shell=True).decode()
    else:
        LOGGER.info("Stats : No UPSTREAM_REPO")
        last_commit = ''
    if last_commit:
        stats += ((BotTheme(user_id)).STATS_MSG_2).format(
        lc = last_commit
    )
    currentTime = TimeFormatter((time() - BOT_START_TIME)*1000)
    osUptime = TimeFormatter((time() - boot_time())*1000)
    total, used, free, disk= disk_usage('/')
    total = humanbytes(total)
    used = humanbytes(used)
    free = humanbytes(free)
    sent = humanbytes(net_io_counters().bytes_sent)
    recv = humanbytes(net_io_counters().bytes_recv)
    cpuUsage = cpu_percent(interval=0.5)
    p_core = cpu_count(logical=False)
    t_core = cpu_count(logical=True)
    swap = swap_memory()
    swap_p = swap.percent
    swap_t = humanbytes(swap.total)
    memory = virtual_memory()
    mem_p = memory.percent
    mem_t = humanbytes(memory.total)
    mem_a = humanbytes(memory.available)
    mem_u = humanbytes(memory.used)
    stats += ((BotTheme(user_id)).STATS_MSG_3).format(
        ct = currentTime,
        osUp = osUptime,
        t = total,
        u = used,
        f = free,
        s = sent,
        r = recv,
        cpu = cpuUsage,
        mem = mem_p,
        di = disk,
        p_co = p_core,
        t_co = t_core,
        swap_t = swap_t,
        swap_p = swap_p,
        mem_t = mem_t,
        mem_a = mem_a,
        mem_u = mem_u,
        UPDATES_CHANNEL = UPDATES_CHANNEL
    )
    await message.reply_text(text = stats,
        parse_mode = enums.ParseMode.HTML,
        disable_web_page_preview=True
    )

async def help_message_f(client: Client, message: Message):
    user_id, _ = getUserOrChaDetails(message)
    reply_markup = InlineKeyboardMarkup(
        [[InlineKeyboardButton("🆘️ Open Help 🆘️", callback_data = "openHelp_pg1")]]
    )
    await message.reply_text(
        text = ((BotTheme(user_id)).HELP_MSG).format(
        UPDATES_CHANNEL = UPDATES_CHANNEL
    ),
        reply_markup = reply_markup,
        parse_mode = enums.ParseMode.HTML,
        disable_web_page_preview=True
    )

async def user_settings(client: Client, message: Message):

    uid, _ = getUserOrChaDetails(message)
    to_edit = await message.reply_text('Fetching your Details . . .')
    __theme = USER_THEMES.get(uid, 'Default Bot Theme')
    __prefix = PRE_DICT.get(uid, "-")
    __caption = CAP_DICT.get(uid, "-")
    __template = IMDB_TEMPLATE.get(uid, "Default Template")
    __toggle = user_specific_config.get(uid, False)
    toggle_ = 'Document' if __toggle else 'Video'
    __text = f'''┏━ 𝙐𝙨𝙚𝙧 𝘾𝙪𝙧𝙧𝙚𝙣𝙩 𝙎𝙚𝙩𝙩𝙞𝙣𝙜𝙨 ━━╻
┃
┣ <b>User Prefix :</b> <code>{__prefix}</code>
┣ <b>User Bot Theme :</b> <code>{__theme}</code>
┣ <b>User Caption :</b> <code>{__caption}</code>
┣ <b>User IMDB Template :</b> 
<code>{__template}</code>
┣ <b>User Toggle :</b> <code>{toggle_}</code>
┃
┗━━━━━━━━━━━━━━━━━━╹

'''
    btn = InlineKeyboardMarkup(
        [[InlineKeyboardButton("🖼 Show Thumb 🖼", callback_data = f"showthumb {uid}")]]
    )
    await to_edit.delete()
    await message.reply_photo(photo = 'https://te.legra.ph/file/a3dea655deb2a6f213813.jpg', caption=__text, parse_mode=enums.ParseMode.HTML, reply_markup=btn)

async def settings_callback(client, query: CallbackQuery):
    if query.data.startswith("showthumb"):
        getData = (query.data).split(" ")
        thumb_path = f'{DOWNLOAD_LOCATION}/thumbnails/{getData[1]}.jpg'
        if not opath.exists(thumb_path):
            _text = '''┏━ 𝙐𝙨𝙚𝙧 𝘾𝙪𝙧𝙧𝙚𝙣𝙩 𝙎𝙚𝙩𝙩𝙞𝙣𝙜𝙨 ━━╻
┃
┣ <b>User Thumbnail :</b> <code>Not Set Yet !</code>
┃
┗━━━━━━━━━━━━━━━━━━╹'''

            await query.edit_message_caption(caption=_text)
        else:
            _text = '''┏━ 𝙐𝙨𝙚𝙧 𝘾𝙪𝙧𝙧𝙚𝙣𝙩 𝙎𝙚𝙩𝙩𝙞𝙣𝙜𝙨 ━━╻
┃
┣ <b>User Thumbnail :</b> <code>Already have A Custom Thumbnail !</code>
┃
┗━━━━━━━━━━━━━━━━━━╹'''

            await query.edit_message_media(media=InputMediaPhoto(media=thumb_path, caption=_text))

async def picture_add(client: Client, message: Message):
    '''/addpic command'''
    editable = await message.reply_text("Checking Input ...")
    resm = message.reply_to_message
    msg_text = resm.text
    if msg_text:
        if msg_text.startswith("http"):
            pic_add = msg_text.strip()
            await editable.edit("Adding your Link ...")
    elif resm.photo:
        if not ((resm.photo and resm.photo.file_size <= TGH_LIMIT)):
            await editable.edit("This Media is Not Supported! Only Send Photos !!")
            return
        await editable.edit("Uploading to te.legra.ph Server ...")
        df = await client.download_media(
            message=resm,
            file_name=f'{DOWNLOAD_LOCATION}/thumbnails'
        )
        await editable.edit("`Uploading to te.legra.ph Please Wait....`")
        try:
            tgh_post = upload_file(df)
            pic_add = f'https://te.legra.ph{tgh_post[0]}'
        except Exception as err:
            await editable.edit(err)
        finally:
            oremove(df)
    else:
        await editable.edit("Provide Some Photos!! Bruh Photo or DDL Links.")
    PICS_LIST.append(pic_add)
    asleep(1.5)
    await editable.edit("Added to Existing Random Pictures Status List!")

async def pictures(client: Client, message: Message):
    '''/pics command'''
    if not PICS_LIST:
        await message.reply_text("Add Some Photos OR use API to Let me Show you !!")
    else:
        to_edit = await message.reply_text("Generating Grid of your Images...")
        btn = [
            [InlineKeyboardButton("<<", callback_data=f"pic -1"),
            InlineKeyboardButton(">>", callback_data="pic 1")],
            [InlineKeyboardButton("Remove Photo", callback_data="picsremove 0")]
        ]
        await to_edit.delete()
        await message.reply_photo(photo=PICS_LIST[0], caption=f'• Picture No. : 1 / {len(PICS_LIST)}', reply_markup=InlineKeyboardMarkup(btn))

async def pics_callback(client: Client, query: CallbackQuery):
    if query.data.startswith("pic"):
        if query.data.startswith("picsremove"):
            getData = (query.data).split()
            index = int(getData[1])
            PICS_LIST.pop(index)
            await query.edit_message_media(media=InputMediaPhoto(media="https://te.legra.ph/file/06dbd8fb0628b8ba4ab45.png", caption="Removed from Existing Random Pictures Status List !!"))
            return
        getData = (query.data).split()
        ind = int(getData[1])
        no = len(PICS_LIST) - abs(ind+1) if ind < 0 else ind + 1
        pic_info = f'🌄 <b>Picture No. : {no} / {len(PICS_LIST)}</b>'
        btns = [
            [InlineKeyboardButton("<<", callback_data=f"pic {ind-1}"),
            InlineKeyboardButton(">>", callback_data=f"pic {ind+1}")],
            [InlineKeyboardButton("Remove Photo", callback_data=f"picsremove {ind}")]
        ]
        await query.edit_message_media(media=InputMediaPhoto(media=PICS_LIST[ind], caption=pic_info), reply_markup=InlineKeyboardMarkup(btns))
