import json, subprocess

from pyrogram import Client, filters

from tata import download_catchup, download_playback_catchup

from utils import check_user, get_tplay_data

from config import api_id, api_hash, bot_token, script_developer




print("Installing YT-DLP")
subprocess.run("pip install yt-dlp".split())


data_json = get_tplay_data()

app = Client("RC_tplay_dl_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)




@app.on_message(filters.incoming & filters.text)
def tplay_past_catchup_dl_cmd_handler(app, message):

    auth_user = check_user(message)
    if auth_user is None:
        return
    
    if "/tata" in message.text:
        
        if len(message.text.split()) < 3:
            message.reply_text("<b>Syntax: </b>`/tata [channelName] | [filename]`")
            return
        
        

        cmd = message.text.split("|")
        _, channel = cmd[0].strip().split(" ")

        if channel not in data_json:
            message.reply_text(f"<b>Channel Not in DB</b>")
            return

        download_playback_catchup(channel, cmd[1].strip() , data_json, app, message)

    if not "watch.tataplay.com" in message.text:
        return 
    
    if "coming-soon" in message.text:
        message.reply_text(f"<b>Can't DL something which has not aired yet\nCheck URL and try again...</b>")
        return
    download_catchup(message.text , data_json, app, message)


    

@app.on_message(filters.incoming & filters.command(['start']) & filters.text)
def start_cmd_handler(app, message):

    message.reply_text("<b>A Telegram bot to download from tataPlay</b>\n\n`> >`<b> Made with Love by RC</b>")
    

print(script_developer , "\n")



@app.on_message(filters.private & filters.command(["multirec"]))
def recording_multi_audio(bot, update):


    if update.from_user.id in config.AUTH_USERS:

        if len(update.command) > 1:

            url = config.LINK_JSON
            response = urlopen(url) 
            data_json = json.loads(response.read())


            if update.command[1] in data_json:

                channel = update.command[1]
                channel_json = data_json[channel][0]['title']
                recordingDuration = update.command[2]

                
                if len(update.command) > 2:

                    if '|' in update.command:
                        join = concatenate_list_data(update.command)
                        title = join.split('| ')
                        title = title[1]
                        # multirecNickJunior00:00:10|MashaTest
                    elif recordingDuration.split(':')[2] <= 50:
                        title = "Test"
                    else:
                        title = "No Title"



                    msg = update.reply_text(
                    text = f"<b><i>Recording in Progress...</b></i>",
                    disable_web_page_preview=True,
                    quote=True
                    )
                    print('--------')
                    print(f'[RECORDING] {channel_json} - {recordingDuration}\n[USER] {update.from_user.first_name} - {update.from_user.id}')
                    print('--------')

                    

                    audioList = audioListTitle(data_json[channel][0]['audio'])

                    try:
                        newfile = multi_rip(bot, update , streamUrl = data_json[channel][0]['link'] , channel = data_json[channel][0]['title'] , recordingDuration = recordingDuration , language = audioList , ripType = data_json[channel][0]['ripType'] , ripQuality = data_json[channel][0]['quality'] , fileTitle = title)
                        
                        if os.path.exists(newfile) == True:
                            msg.edit(text = f'<b><i>{channel_json} Recorded Successfully</i></b>' , disable_web_page_preview=True)

                            print('--------')
                            print(f'[RECORDING DONE] {channel_json} - {recordingDuration}\n[USER] {update.from_user.first_name} - {update.from_user.id}')
                            print('--------')




                            print('--------')
                            print(f'[UPLOAD] {newfile}\n[USER] {update.from_user.first_name} - {update.from_user.id}')
                            print('--------')
                            
                            

                            duration = get_duration(newfile)
                            width, height = get_width_height(newfile)

                            bot.send_video(video=newfile, chat_id = update.from_user.id , caption= f"<code>{newfile}</code>")

                                

                            
                            os.remove(newfile)

                            print('--------')
                            print(f'[REMOVE] {newfile}\n[USER] {update.from_user.first_name} - {update.from_user.id}')
                            print('--------')
                                

                                
                                



                        else:
                            msg.edit(text = f'<b><i>Recording Failed</b></i>' , disable_web_page_preview=True)

                    except Exception as e:
                        msg.edit(text = f'<code>{e}</code>' , disable_web_page_preview=True)




                    


                    

                else:

                    update.reply_text(
                    text = f"<b><i>No Duration Supplied for {update.command[1]}</b></i>",
                    disable_web_page_preview=True,
                    quote=True
                    )



                
            
            else:
                update.reply_text(
                text = f"<b><i>Requested Channel not Found in Database!</i></b>",
                disable_web_page_preview=True,
                quote=True
                )


            


            

        else:
            update.reply_text(
            text="<b><i>No Command from User...</i></b>",
            disable_web_page_preview=True,
            quote=True
            )

        

    else:
        update.reply_text(
        text="`You are not Allowed to access this Command`",
        reply_markup=InlineKeyboardMarkup([SITE_BUTTON]),
        disable_web_page_preview=True,
        quote=True
    )


app.run()
