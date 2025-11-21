from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto

from .storage import (
   searchs, pagination, subscribes,
   retry_on_flood, igrone_error, check_fsb, queue,
   split_list, chaptersList, get_episode_number, is_auth_query,
)

from bot import Bot, Vars, logger
import random

from Tools.db import ensure_user, get_subs, uts
from Tools.base import Subscribes, TaskCard
import asyncio



@Bot.on_callback_query(filters.regex("^refresh$"))
async def refresh_handler(_, query):
  if not _.FSB or _.FSB == []:
    await retry_on_flood(query.answer)(
      " ✅ Thanks for joining! You can now use the bot. ",
      show_alert=True
    )
    return await retry_on_flood(query.message.delete)()

  channel_button, change_data = await check_fsb(_, query)
  if not channel_button:
    await retry_on_flood(query.answer)(
      " ✅ Thanks for joining! You can now use the bot. ",
      show_alert=True
    )
    
    return await retry_on_flood(query.message.delete)()

  channel_button = split_list(channel_button)
  channel_button.append([InlineKeyboardButton("ʀᴇғʀᴇsʜ ⟳", callback_data="refresh")])

  try:
    await retry_on_flood(query.edit_message_media)(
        media=InputMediaPhoto(random.choice(Vars.PICS),
                              caption=Vars.FORCE_SUB_TEXT),
        reply_markup=InlineKeyboardMarkup(channel_button),
    )
  except:
    await retry_on_flood(query.answer)("You're still not in the channel.")

  if change_data:
    for change_ in change_data:
      _.FSB[change_[0]] = (change_[1], change_[2], change_[3])



@Bot.on_callback_query(filters.regex("^close$"))
async def close_handler(_, query):
  await igrone_error(query.answer)()
  await igrone_error(query.message.reply_to_message.delete)()
  await igrone_error(query.message.delete)()



@Bot.on_callback_query(filters.regex("^kclose$"))
async def kclose_handler(_, query):
  await igrone_error(query.answer)()
  await igrone_error(query.message.reply_to_message.delete)()
  await igrone_error(query.message.delete)()



@Bot.on_callback_query(filters.regex("^premuim$"))
async def premuim_handler(_, query):
  """This Is Premuim Handler Of Callback Data"""
  button = query.message.reply_markup.inline_keyboard
  text = """
<b><blockquote>sʜᴀʀᴇ ʙᴏᴛ ʟɪɴᴋ ᴛᴏ ʏᴏᴜʀ ғʀɪᴇɴᴅs ᴀɴᴅ ɢᴇᴛ ᴘʀᴇᴍɪᴜᴍ ᴀᴄᴄᴏʀᴅɪɴɢ ᴛᴏ ᴀᴠᴀɪʟᴀʙʟᴇ ᴘʟᴀɴs</blockquote>
- ᴀᴠᴀɪʟᴀʙʟᴇ ᴘʟᴀɴs -
- 05 sʜᴀʀᴇ - 1 ᴡᴇᴇᴋ
- 10 sʜᴀʀᴇ - 1 ᴍᴏɴᴛʜs
- 20 sʜᴀʀᴇ - 3 ᴍᴏɴᴛʜs
- 30 sʜᴀʀᴇ - 6 ᴍᴏɴᴛʜs
- 40 sʜᴀʀᴇ - 1 year
<blockquote>ᴘʀᴇᴍɪᴜᴍ ғᴇᴀᴛᴜʀᴇs
○ ɴᴏ ɴᴇᴇᴅ ᴛᴏ ᴠᴇʀɪғʏ
○ ɴᴏ ɴᴇᴇᴅ ᴛᴏ ᴏᴘᴇɴ ʟɪɴᴋ
○ ᴅɪʀᴇᴄᴛ ғɪʟᴇs
○ ᴀᴅ-ғʀᴇᴇ ᴇxᴘᴇʀɪᴇɴᴄᴇ
○ ᴜɴʟɪᴍɪᴛᴇᴅ ᴀʟʟ</blockquote>
<blockquote>‼️ᴀғᴛᴇʀ sʜᴀʀɪɴɢ ᴀ ʀᴇғᴇʀᴇɴᴄᴇ ʟɪɴᴋ ᴘʟᴇᴀsᴇ ɢɪᴠᴇ ᴜs sᴏᴍᴇ ᴛɪᴍᴇ ᴛᴏ ᴀᴅᴅ ʏᴏᴜ ɪɴ ᴛʜᴇ ᴘʀᴇᴍɪᴜᴍ</blockquote>
✨ɪғ ʏᴏᴜ ᴡᴀɴᴛ ʏᴏᴜ ᴄᴀɴ ᴅᴏɴᴀᴛᴇ ᴀɴʏ ᴀᴍᴏᴜɴᴛ @EternalsHelplineBot</b>"""
  try:
    del button[-2]
    await retry_on_flood(query.edit_message_media)(
      media=InputMediaPhoto(random.choice(Vars.PICS), caption=text),
      reply_markup=InlineKeyboardMarkup(button)
    )
  except Exception:
    button = [[InlineKeyboardButton(" Close ", callback_data="kclose")]]
    await retry_on_flood(query.edit_message_media)(
      media=InputMediaPhoto(random.choice(Vars.PICS), caption=text),
      reply_markup=InlineKeyboardMarkup(button)
    )



@Bot.on_callback_query(filters.regex("^chs") & is_auth_query())
async def ch_handler(client, query):
  """This Is Information Handler Of Callback Data"""
  try:
    webs, data = searchs[query.data]
  except:
    return await query.answer(
      "This is an old button, please redo the search",
      show_alert=True
    )

  try:
    bio_list = await webs.get_chapters(data)
  except:
    return await query.answer("No chapters found", show_alert=True)

  if not bio_list:
    return await query.answer("No chapters found", show_alert=True)

  c = f"pg:{webs.sf}:{hash(bio_list['url'])}:"
  pagination[c] = (webs, bio_list, data)

  subs_bool = get_subs(str(query.from_user.id), bio_list['url'], webs.sf)
  
  sdata = Subscribes(
    manga_url=bio_list['url'],
    manga_title=bio_list['title'],
    web=webs.sf,
    lastest_chapter=""
  )
  sc = f"subs:{hash(bio_list['url'])}"
  subscribes[sc] = (webs, sdata)

  rand_pic = bio_list['poster'] if "poster" in bio_list else random.choice(Vars.PICS)
  caption = bio_list['msg'][:1024] if "msg" in bio_list else f"<b>{bio_list['title']}</b>"
  
  if webs.sf == "mf":
    button = [
      [
        InlineKeyboardButton("✘ ᴜɴsᴜʙsᴄʀɪʙᴇ ✘", callback_data=sc) if subs_bool else InlineKeyboardButton("✓ sᴜʙsᴄʀɪʙᴇ ✓", callback_data=sc)
      ],
      [
        InlineKeyboardButton("▸ᴄʜᴀᴘᴛᴇʀs◂", callback_data=f"{c}:1"),
        InlineKeyboardButton("▸ᴠᴏʟᴜᴍᴇ◂", callback_data=f"{c}:v:1")
      ],
      [
        InlineKeyboardButton("⇦ 𝗕𝗔𝗖𝗞", callback_data=f"plugin_{webs.sf}")
      ]
    ]
    
  else:
    button = [
        [
            InlineKeyboardButton("✘ ᴜɴsᴜʙsᴄʀɪʙᴇ ✘", callback_data=sc) if subs_bool else InlineKeyboardButton("✓ sᴜʙsᴄʀɪʙᴇ ✓", callback_data=sc)
        ],
        [
            InlineKeyboardButton("▸ᴄʜᴀᴘᴛᴇʀs◂", callback_data=f"{c}:1"),
            InlineKeyboardButton("⇦ 𝗕𝗔𝗖𝗞", callback_data=f"plugin_{webs.sf}")
        ],
    ]
  
  if webs.sf == "ck":
    button.append([InlineKeyboardButton("▏𝗖𝗟𝗢𝗦𝗘▕", callback_data="kclose")])

  try:
    await retry_on_flood(query.edit_message_media)(
      InputMediaPhoto(rand_pic, caption=caption),
      reply_markup=InlineKeyboardMarkup(button)
    )
  except Exception:
    await retry_on_flood(query.edit_message_media)(
      InputMediaPhoto(Vars.PICS[-1], caption=caption),
      reply_markup=InlineKeyboardMarkup(button)
    )


@Bot.on_callback_query(filters.regex("^pg") & is_auth_query())
async def pg_handler(client, query):
  """This Is Pagination Handler Of Callback Data"""
  call_data = query.data.split(":")
  page = call_data[-1]

  vols = None
  if call_data[-2] == "v":
    vols = True
    call_data = ":".join(call_data[:-2])
  else:
    call_data = ":".join(call_data[:-1])

  call_data = f"{call_data}:"
  if call_data not in pagination:
    call_data = call_data[:-1]

  if call_data in pagination:
    webs, data, rdata = pagination[call_data]
    sf = webs.sf
    subs_bool = get_subs(str(query.from_user.id), rdata['url'], sf)
    if sf == "mf" and vols:
      chapters = await webs.get_chapters(rdata, vol=True, page=int(page))
      if not chapters:
        return await query.answer("No chapters found", show_alert=True)
      if "chapters" in chapters and not chapters['chapters']:
        return await query.answer("No chapters found", show_alert=True)

      try:
        chapters = webs.iter_chapters(chapters, vol=True, page=int(page))
      except:
        return await query.answer("No chapters found", show_alert=True)

    else:
      try:
        chapters = await webs.iter_chapters(data, page=int(page))
      except TypeError:
        chapters = webs.iter_chapters(data, page=int(page))

    if not chapters:
      return await query.answer("No chapters found", show_alert=True)

    if chapters == [] or len(chapters) < 1:
      return await query.answer("No chapters found", show_alert=True)

    button = []
    for chapter in chapters:
      c = f"pic|{hash(chapter['url'])}"
      chaptersList[c] = (webs, chapter)
      button.append(InlineKeyboardButton(chapter['title'], callback_data=c))

    button = split_list(button[:60])
    c = f"pg:{sf}:{hash(chapters[-1]['url'])}:"
    pagination[c] = (webs, data, rdata)

    if int(page) > 0:
      pre_page_ = []
      
      if int(int(page) - 1) > 0 and webs.iter_chapters(data, page=int(int(page) - 1)):
        pre_page_.append(InlineKeyboardButton("<<", callback_data=f"{c}{int(page) - 1}"))
      if int(int(page) - 2) > 0 and webs.iter_chapters(data, page=int(int(page) - 2)):
          pre_page_.append(InlineKeyboardButton("<2x", callback_data=f"{c}{int(page) - 2}"))
      if int(int(page) - 5) > 0 and webs.iter_chapters(data, page=int(int(page) - 5)):
          pre_page_.append(InlineKeyboardButton("<5x", callback_data=f"{c}{int(page) - 5}"))
      if pre_page_:
          button.append(pre_page_)

    
    next_page_ = []
    if webs.iter_chapters(data, page=int(int(page) + 1)):
      next_page_.append(InlineKeyboardButton(">>", callback_data=f"{c}{int(page) + 1}"))
    if webs.iter_chapters(data, page=int(int(page) + 2)):
      next_page_.append(InlineKeyboardButton("2x>", callback_data=f"{c}{int(page) + 2}"))
    if webs.iter_chapters(data, page=int(int(page) + 5)):
      next_page_.append(InlineKeyboardButton("5x>", callback_data=f"{c}{int(page) + 5}"))
    if next_page_:
      button.append(next_page_)

    
    sdata = Subscribes(
      manga_url=rdata['url'],
      manga_title=rdata['title'],
      web=webs.sf,
      lastest_chapter=chapters[0]['title'] if chapters else ""
    )
    c = f"subs:{hash(rdata['url'])}"
    subscribes[c] = (webs, sdata)

    if webs.sf != "dj":
      if subs_bool:
        button.append([InlineKeyboardButton("✘ ᴜɴsᴜʙsᴄʀɪʙᴇ ✘", callback_data=c)])
      else:
        button.append([InlineKeyboardButton("✓ sᴜʙsᴄʀɪʙᴇ ✓", callback_data=c)])

    if sf == "mf":
      callback_data = f"full:{sf}:{hash(chapters[0]['url'])}"
      if int(page) == 1:
        pagination[callback_data] = (chapters[:60], webs)
      else:
        pagination[callback_data] = (chapters, webs)

      button.append(
        [
          InlineKeyboardButton("▸ᴄʜᴀᴘᴛᴇʀs◂", callback_data=f"{call_data}:{page}") if vols else InlineKeyboardButton("📡 Volume 📡", callback_data=f"{call_data}v:{page}"),
          InlineKeyboardButton("⇧ ғᴜʟʟ ᴘᴀɢᴇ ⇧", callback_data=callback_data)
        ]
      )
      button.append([InlineKeyboardButton("⇦ 𝗕𝗔𝗖𝗞", callback_data=f"plugin_{sf}")])

    else:
      callback_data = f"full:{sf}:{hash(chapters[0]['url'])}"
      if int(page) == 1:
        pagination[callback_data] = (chapters[:60], webs)
      else:
        pagination[callback_data] = (chapters, webs)

      button.append([
          InlineKeyboardButton("⇧ ғᴜʟʟ ᴘᴀɢᴇ ⇧", callback_data=callback_data),
          InlineKeyboardButton("⇦ 𝗕𝗔𝗖𝗞", callback_data=f"plugin_{sf}")
      ])

    await retry_on_flood(query.edit_message_reply_markup)(InlineKeyboardMarkup(button))
  else:
    await igrone_error(query.answer)(
      "This is an old button, please redo the search",
      show_alert=True
    )




@Bot.on_callback_query(filters.regex("^full") & is_auth_query())
async def full_handler(client, query):
  """ This Is Full Page Handler Of Callback Data """
  if query.data in pagination:
    chapters, webs = pagination[query.data]
    
    merge_size = uts[str(query.from_user.id)].get('setting', {}).get('megre', None)
    priority = uts[str(query.from_user.id)].get('setting', {}).get("premuim", 1)

    try:
      merge_size = int(merge_size) if merge_size else merge_size
    except:
      merge_size = None

    added_item = {}
    chapters = list(reversed(chapters))

    try:
      if merge_size:
        logger.info(merge_size)
        for i in range(0, len(chapters), merge_size):
          data = chapters[i:i + merge_size]
          for chapter in data:
            episode_num = get_episode_number(data[0]['title'])
            if episode_num not in added_item:
              added_item[episode_num] = data # list object

      else:
        for data in chapters:
          episode_num = get_episode_number(data['title'])
          if episode_num not in added_item:
            added_item[episode_num] = [data]

   
      processing_tasks = [
        webs.get_pictures(url=data['url'], data=data)
        for chapter_data in added_item.values()
        for data in chapter_data
      ]
      picturesList = await asyncio.gather(*processing_tasks)
      #picturesList = [item for sublist in picturesList for item in sublist]

      tasks = [
          queue.put(
              TaskCard(
                data_list=chapter_data,
                picturesList=pictures,
                webs=webs,
                sts=None,
                user_id=query.from_user.id,
                chat_id=query.message.chat.id,
                priority=priority
              ),
          ) for chapter_data, pictures in zip(added_item.values(), picturesList)
      ]
      
      await asyncio.gather(*tasks)

      await igrone_error(query.answer)(
        f"{len(tasks)} Chapter Added To Queue",
        show_alert=True
      )

    except Exception as err:
      logger.exception(err)
      await retry_on_flood(query.message.reply_text)(f"`{err}`")
      await igrone_error(query.answer)()
        

  else:
    await retry_on_flood(query.answer)(
      "This is an old button, please redo the search",
      show_alert=True
    )


@Bot.on_callback_query(filters.regex("^pic") & is_auth_query())
async def pic_handler(client, query):
  """This Is Pictures Handler Of Callback Data"""
  if query.data in chaptersList:
    webs, data = chaptersList[query.data]
    user_id = query.from_user.id
    try:
      pictures = await webs.get_pictures(url=data['url'], data=data)
    except:
      return await query.answer("No pictures found", show_alert=True)

    if not pictures:
      return await query.answer("No pictures found", show_alert=True)

    ensure_user(user_id)
    sts = await retry_on_flood(query.message.reply_text)("<code>Adding...</code>")
    try:
      txt = f"<i>Manga Name: **{data['manga_title']}** Chapter: - **{data['title']}**</i>"
      priority = uts[str(query.from_user.id)].get('setting', {}).get("premuim", 1)
      
      task_id = await queue.put(
        TaskCard(
          data_list=[data.copy()],
          picturesList=pictures,
          webs=webs,
          sts=sts,
          user_id=query.from_user.id,
          chat_id=query.message.chat.id,
          priority=priority
        ),
      )
      
      button = [[InlineKeyboardButton(" Cancel Your Tasks ", callback_data=f"cql:{task_id}")]]
      await retry_on_flood(sts.edit)(txt, reply_markup=InlineKeyboardMarkup(button))
      
      await query.answer(f"Your {task_id} added at queue")
    except Exception as err:
      logger.exception(err)
      await retry_on_flood(sts.edit)(f"`{str(err)}`")
      await igrone_error(query.answer)()
  else:
    await igrone_error(query.answer)("This is an old button, please redo the search", show_alert=True)


@Bot.on_callback_query(filters.regex("^cql"))
async def cl_handler(client, query):
  """This Is Cancel Handler Of Callback Data"""
  task_id = query.data.split(":")[-1]

  if await queue.delete_task(task_id):
    await retry_on_flood(query.message.edit_text)("<i>Your Task Cancelled !</i>")
  else:
    await retry_on_flood(query.answer)(" Task Not Found ", show_alert=True)
    await retry_on_flood(query.message.delete)()
