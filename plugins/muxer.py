from pyrogram import Client, filters
from helper_func.progress_bar import progress_bar
from helper_func.dbhelper import Database as Db
from helper_func.mux import softmux_vid, hardmux_vid, softremove_vid
from config import Config
import time
import os
from database.adduser import AddUser
db = Db()
from plugins.forcesub import handle_force_subscribe
@Client.on_message(filters.command('softmux') & filters.private)
async def softmux(client, message):
    await AddUser(client, message)
    if Config.UPDATES_CHANNEL:
      fsub = await handle_force_subscribe(client, message)
      if fsub == 400:
        return
    chat_id = message.from_user.id
    og_vid_filename = db.get_vid_filename(chat_id)
    og_sub_filename = db.get_sub_filename(chat_id)
    text = ''
    if not og_vid_filename :
        text += 'First send a Video File\n'
    if not og_sub_filename :
        text += 'Send a Subtitle File!'

    if not (og_sub_filename and og_vid_filename) :
        await client.send_message(chat_id, text)
        return

    text = 'Your File is Being Soft Subbed. This should be done in few seconds!'
    sent_msg = await client.send_message(chat_id, text)

    softmux_filename = await softmux_vid(og_vid_filename, og_sub_filename, sent_msg)
    if not softmux_filename:
        return

    final_filename = db.get_filename(chat_id)
    os.rename(Config.DOWNLOAD_DIR+'/'+softmux_filename,Config.DOWNLOAD_DIR+'/'+final_filename)
    thumbnail_location = f"{Config.DOWNLOAD_LOCATION}/{m.from_user.id}.jpg"
    # if thumbnail not exists checking the database for thumbnail
    if not os.path.exists(thumbnail_location):
        thumb_id = (await get_data(m.from_user.id)).thumb_id

        if thumb_id:
            thumb_msg = await c.get_messages(m.chat.id, thumb_id)
            try:
                thumbnail_location = await thumb_msg.download(file_name=thumbnail_location)
            except:
                thumbnail_location = None
        else:
            try:
                thumbnail_location = await take_screen_shot(new_file_location, os.path.dirname(os.path.abspath(new_file_location)), random.randint(0, duration - 1))
            except Exception as e:
                logger.error(e)
                thumbnail_location = None

    width, height, thumbnail = await fix_thumb(thumbnail_location)
    start_time = time.time()
    try:
        await client.send_document(
                chat_id,
                thumb=thumbnail,
                progress = progress_bar, 
                progress_args = (
                    'Uploading your File!',
                    sent_msg,
                    start_time
                    ), 
                document = os.path.join(Config.DOWNLOAD_DIR, final_filename),
                caption = final_filename
                )
        text = 'File Successfully Uploaded!\nTotal Time taken : {} seconds'.format(round(time.time()-start_time))
        await sent_msg.edit(text)
    except Exception as e:
        print(e)
        await client.send_message(chat_id, 'An error occured while uploading the file!\nCheck logs for details of the error!')

    path = Config.DOWNLOAD_DIR+'/'
    os.remove(path+og_sub_filename)
    os.remove(path+og_vid_filename)
    try :
        os.remove(path+final_filename)
    except :
        pass

    db.erase(chat_id)


@Client.on_message(filters.command('hardmux') & filters.private)
async def hardmux(bot, message, cb=False):
    await AddUser(bot, message)
    if Config.UPDATES_CHANNEL:
      fsub = await handle_force_subscribe(bot, message)
      if fsub == 400:
        return
    me = await bot.get_me()
    
    chat_id = message.from_user.id
    og_vid_filename = db.get_vid_filename(chat_id)
    og_sub_filename = db.get_sub_filename(chat_id)
    text = ''
    if not og_vid_filename :
        text += 'First send a Video File\n'
    if not og_sub_filename :
        text += 'Send a Subtitle File!'
    
    if not (og_sub_filename or og_vid_filename) :
        return await bot.send_message(chat_id, text)
    
    text = 'Your File is Being Hard Subbed. This might take a long time!'
    sent_msg = await bot.send_message(chat_id, text)

    hardmux_filename = await hardmux_vid(og_vid_filename, og_sub_filename, sent_msg)
    
    if not hardmux_filename:
        return
    
    final_filename = db.get_filename(chat_id)
    os.rename(Config.DOWNLOAD_DIR+'/'+hardmux_filename,Config.DOWNLOAD_DIR+'/'+final_filename)
    thumbnail_location = f"{Config.DOWNLOAD_LOCATION}/{m.from_user.id}.jpg"
    # if thumbnail not exists checking the database for thumbnail
    if not os.path.exists(thumbnail_location):
        thumb_id = (await get_data(m.from_user.id)).thumb_id

        if thumb_id:
            thumb_msg = await c.get_messages(m.chat.id, thumb_id)
            try:
                thumbnail_location = await thumb_msg.download(file_name=thumbnail_location)
            except:
                thumbnail_location = None
        else:
            try:
                thumbnail_location = await take_screen_shot(new_file_location, os.path.dirname(os.path.abspath(new_file_location)), random.randint(0, duration - 1))
            except Exception as e:
                logger.error(e)
                thumbnail_location = None

    width, height, thumbnail = await fix_thumb(thumbnail_location)
    start_time = time.time()
    try:
        await bot.send_video(
                chat_id,
                thumb=thumbnail,
                progress = progress_bar, 
                progress_args = (
                    'Uploading your File!',
                    sent_msg,
                    start_time
                    ), 
                video = os.path.join(Config.DOWNLOAD_DIR, final_filename),
                caption = final_filename
                )
        text = 'File Successfully Uploaded!\nTotal Time taken : {} seconds'.format(round(time.time()-start_time))
        await sent_msg.edit(text)
    except Exception as e:
        print(e)
        await client.send_message(chat_id, 'An error occured while uploading the file!\nCheck logs for details of the error!')
    
    path = Config.DOWNLOAD_DIR+'/'
    os.remove(path+og_sub_filename)
    os.remove(path+og_vid_filename)
    try :
        os.remove(path+final_filename)
    except :
        pass
    db.erase(chat_id)



@Client.on_message(filters.command('softremove') & filters.private)
async def softremove(client, message):
    if Config.UPDATES_CHANNEL:
      fsub = await handle_force_subscribe(client, message)
      if fsub == 400:
        return
    chat_id = message.from_user.id
    og_vid_filename = db.get_vid_filename(chat_id)
    og_sub_filename = db.get_sub_filename(chat_id)
    text = ''
    if not og_vid_filename :
        text += 'First send a Video File\n'
    if not og_sub_filename :
        text += 'Send a Subtitle File!'

    if not (og_sub_filename and og_vid_filename) :
        await client.send_message(chat_id, text)
        return

    text = 'Your File is Being Soft Subbed. This should be done in few seconds!'
    sent_msg = await client.send_message(chat_id, text)

    softmux_filename = await softremove_vid(og_vid_filename, og_sub_filename, sent_msg)
    if not softmux_filename:
        return

    final_filename = db.get_filename(chat_id)
    os.rename(Config.DOWNLOAD_DIR+'/'+softmux_filename,Config.DOWNLOAD_DIR+'/'+final_filename)
    thumbnail_location = f"{Config.DOWNLOAD_LOCATION}/{m.from_user.id}.jpg"
    # if thumbnail not exists checking the database for thumbnail
    if not os.path.exists(thumbnail_location):
        thumb_id = (await get_data(m.from_user.id)).thumb_id

        if thumb_id:
            thumb_msg = await c.get_messages(m.chat.id, thumb_id)
            try:
                thumbnail_location = await thumb_msg.download(file_name=thumbnail_location)
            except:
                thumbnail_location = None
        else:
            try:
                thumbnail_location = await take_screen_shot(new_file_location, os.path.dirname(os.path.abspath(new_file_location)), random.randint(0, duration - 1))
            except Exception as e:
                logger.error(e)
                thumbnail_location = None

    width, height, thumbnail = await fix_thumb(thumbnail_location)
    start_time = time.time()
    try:
        await client.send_document(
                thumb=thumbnail,
                chat_id, 
                progress = progress_bar, 
                progress_args = (
                    'Uploading your File!',
                    sent_msg,
                    start_time
                    ), 
                document = os.path.join(Config.DOWNLOAD_DIR, final_filename),
                caption = final_filename
                )
        text = 'File Successfully Uploaded!\nTotal Time taken : {} seconds'.format(round(time.time()-start_time))
        await sent_msg.edit(text)
    except Exception as e:
        print(e)
        await client.send_message(chat_id, 'An error occured while uploading the file!\nCheck logs for details of the error!')

    path = Config.DOWNLOAD_DIR+'/'
    os.remove(path+og_sub_filename)
    os.remove(path+og_vid_filename)
    try :
        os.remove(path+final_filename)
    except :
        pass

    db.erase(chat_id)
