
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler,Filters, CallbackQueryHandler
from telegram import ParseMode, MessageEntity,ChatMember
from telegram import ReplyKeyboardMarkup
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import os

if os.name == 'nt':
    databasepath = "D:\\udemy\\Messages.txt"
else:
    databasepath = "Messages.txt"

token = Updater("*****************", use_context=True)


def pleasejoinchannel(update, context):
    channel_link = 'https://t.me/developersubtitle'  # لینک کانال شما
    join_button = InlineKeyboardButton("✅ عضویت در کانال ما", url=channel_link)
    confirm_button = InlineKeyboardButton("تایید عضویت", callback_data='confirm_join')
    keyboard = [[join_button], [confirm_button]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    if update.message != None: # /start
        context.bot.send_message(
            chat_id=update.message.chat_id,
            text="سلام {}! برای دریافت ویدیو ها در کانال ما عضو شوید.".format(update.message.from_user.first_name),
            reply_markup=reply_markup
        )
    else:  # dokme
        context.bot.send_message(
            chat_id=update.callback_query.message.chat_id,
            text="سلام ! برای دریافت ویدیو ها در کانال ما عضو شوید.",
            reply_markup=reply_markup
        )


Manager = 399327386

def chooselanguage(id, context):
    python = InlineKeyboardButton("پایتون", callback_data='پایتون')
    java_script = InlineKeyboardButton("جاوا اسکریپت", callback_data='جاوا اسکریپت')
    react = InlineKeyboardButton(" ری اکت ", callback_data='ری اکت')
    nodejs = InlineKeyboardButton("نود جی اس ", callback_data='mynodejs')
    keyboard = [[java_script], [python],[react],[nodejs]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    context.bot.send_message(
        chat_id=id,
        text="دوره مد نظر خود را انتخاب کنید",
        reply_markup=reply_markup
    )

# 1001671023573
def file_handler(update, context):
    id_of_udemy_channel = -1001882212866
    # aliId = 399327386
    if update.effective_message != None:

        if update.effective_message.chat_id == id_of_udemy_channel:
            ChannelID = "@" + update.effective_chat.username
            Caption = update.effective_message.caption
            MsgID = update.effective_message.message_id
            if "جاوا" in Caption.split("#")[1]:
                Language = "JS"
            elif "پایتون" in Caption.split("#")[1]:
                Language = "PY"
            elif "ری_اکت" in Caption.split("#")[1]:
                Language = "RE"
            elif "نود_جی_اس" in Caption.split("#")[1]:
                Language = "NJ"
            Fasl = Caption.split("#")[2].replace("#", "").replace("\n", "")
            with open(databasepath, "a", encoding="utf-8") as myfile:
                myfile.write("{0}*{1}*{2}*{3}---\n".format(Language, Fasl , MsgID, ChannelID))
            context.bot.send_message(chat_id = id_of_udemy_channel , text="فایل به دیتابیس اضافه شد ✅", reply_to_message_id= MsgID)
        
def checkuser(user_id, context):
        try:
            result = context.bot.get_chat_member("@developersubtitle", user_id)
            if result.status == "member" or result.status == "creator" or result.status == "administrator" or result.status == "restricted":
                return True
            else: # kicked , left
                return False
        except Exception as e:# never start the bot
            return False




def button_callback(update, context):
    query = update.callback_query
    if not checkuser(query.message.chat_id, context):
        pleasejoinchannel(update, context)
        return
    if query.data == 'confirm_join':
        chooselanguage(query.message.chat_id, context)
    if query.data == 'پایتون':
           keyboard = []
           with open(databasepath, "r", encoding="utf-8") as myfile:
            data = myfile.read().split("---\n")        
            for item in data:
                leasson_item = item.split("*")
                Language = leasson_item[0]
                if Language == "PY":
                    Fasl = leasson_item[1]

                    if query.message.chat_id == Manager:
                        button = [InlineKeyboardButton(Fasl, callback_data = "py" + Fasl), InlineKeyboardButton("🗑️", callback_data = "delpy" + Fasl)]
                    else:
                        button = [InlineKeyboardButton(Fasl, callback_data = "py" + Fasl)]
                    keyboard.append(button)

            reply_markup = InlineKeyboardMarkup(keyboard)
            context.bot.send_message(
            chat_id=query.from_user.id,
            text="📖 فصل را انتخاب کنید",
            reply_markup=reply_markup
        )

    elif query.data.startswith("py"):
        fasl = query.data.replace("py","")
        with open(databasepath, "r", encoding="utf-8") as myfile:
            data = myfile.read().split("---\n")        
            for item in data:
                leasson_item = item.split("*")
                Language = leasson_item[0]
                Fasl = leasson_item[1]
                msgId = leasson_item[2]
                channeld = leasson_item[3]
                if Language == "PY" and fasl in Fasl:
                    
                    returntomenu = InlineKeyboardButton("بازگشت به منوی اصلی", callback_data='menu')
                    keyboard = [[returntomenu]]
                    reply_markup = InlineKeyboardMarkup(keyboard)
                    context.bot.copy_message(query.message.chat_id, channeld, msgId, reply_markup=reply_markup)
                    break
    elif query.data.startswith("delpy"):
        if query.message.chat_id != Manager:
            return
        fasl = query.data.replace("delpy","")
        with open(databasepath, "r", encoding="utf-8") as myfile:
            lines = myfile.readlines()
        with open(databasepath, "w", encoding="utf-8") as myfile:
            for line in lines:
                if fasl not in line:
                    myfile.write(line)
        context.bot.send_message(
            chat_id=Manager,
            text="فصل مورد نظر پاک شد ✅"
        )
        
    elif query.data == 'menu':
        chooselanguage(query.message.chat_id, context)  

    elif query.data == 'mynodejs':
           keyboard = []
           with open(databasepath, "r", encoding="utf-8") as myfile:
            data = myfile.read().split("---\n")        
            for item in data:
                leasson_item = item.split("*")
                Language = leasson_item[0]
                if Language == "NJ":
                    Fasl = leasson_item[1]

                    if query.message.chat_id == Manager:
                        button = [InlineKeyboardButton(Fasl, callback_data = "nj" + Fasl), InlineKeyboardButton("🗑️", callback_data = "delnj" + Fasl)]
                    else:
                        button = [InlineKeyboardButton(Fasl, callback_data = "nj" + Fasl)]
                    keyboard.append(button)

            reply_markup = InlineKeyboardMarkup(keyboard)
            context.bot.send_message(
            chat_id=query.from_user.id,
            text="📖فصل را انتخاب کنید",
            reply_markup=reply_markup
        )

    elif query.data.startswith("nj"):
        fasl = query.data.replace("nj","")
        with open(databasepath, "r", encoding="utf-8") as myfile:
            data = myfile.read().split("---\n")        
            for item in data:
                leasson_item = item.split("*")
                Language = leasson_item[0]
                Fasl = leasson_item[1]
                msgId = leasson_item[2]
                channeld = leasson_item[3]
                if Language == "NJ" and fasl in Fasl:
                    
                    returntomenu = InlineKeyboardButton("بازگشت به منوی اصلی", callback_data='menu')
                    keyboard = [[returntomenu]]
                    reply_markup = InlineKeyboardMarkup(keyboard)
                    context.bot.copy_message(query.message.chat_id, channeld, msgId, reply_markup=reply_markup)
                    break
    elif query.data.startswith("delnj"):
        if query.message.chat_id != Manager:
            return
        fasl = query.data.replace("delnj","")
        with open(databasepath, "r", encoding="utf-8") as myfile:
            lines = myfile.readlines()
        with open(databasepath, "w", encoding="utf-8") as myfile:
            for line in lines:
                if fasl not in line:
                    myfile.write(line)
        context.bot.send_message(
            chat_id=Manager,
            text="فصل مورد نظر پاک شد ✅"
        )
        
    elif query.data == 'ری اکت':
           keyboard = []
           with open(databasepath, "r", encoding="utf-8") as myfile:
            data = myfile.read().split("---\n")        
            for item in data:
                leasson_item = item.split("*")
                Language = leasson_item[0]
                if Language == "RE":
                    Fasl = leasson_item[1]

                    if query.message.chat_id == Manager:
                        button = [InlineKeyboardButton(Fasl, callback_data = "re" + Fasl), InlineKeyboardButton("🗑️", callback_data = "delre" + Fasl)]
                    else:
                        button = [InlineKeyboardButton(Fasl, callback_data = "re" + Fasl)]
                    keyboard.append(button)

            reply_markup = InlineKeyboardMarkup(keyboard)
            context.bot.send_message(
            chat_id=query.from_user.id,
            text="📖فصل را انتخاب کنید",
            reply_markup=reply_markup
        )

    elif query.data.startswith("re"):
        fasl = query.data.replace("re","")
        with open(databasepath, "r", encoding="utf-8") as myfile:
            data = myfile.read().split("---\n")        
            for item in data:
                leasson_item = item.split("*")
                Language = leasson_item[0]
                Fasl = leasson_item[1]
                msgId = leasson_item[2]
                channeld = leasson_item[3]
                if Language == "RE" and fasl in Fasl:
                    
                    returntomenu = InlineKeyboardButton("بازگشت به منوی اصلی", callback_data='menu')
                    keyboard = [[returntomenu]]
                    reply_markup = InlineKeyboardMarkup(keyboard)
                    context.bot.copy_message(query.message.chat_id, channeld, msgId, reply_markup=reply_markup)
                    break
    elif query.data.startswith("delre"):
        if query.message.chat_id != Manager:
            return
        fasl = query.data.replace("delre","")
        with open(databasepath, "r", encoding="utf-8") as myfile:
            lines = myfile.readlines()
        with open(databasepath, "w", encoding="utf-8") as myfile:
            for line in lines:
                if fasl not in line:
                    myfile.write(line)
        context.bot.send_message(
            chat_id=Manager,
            text="فصل مورد نظر پاک شد ✅"
        )


    elif query.data == "جاوا اسکریپت":
        keyboard = []
        with open(databasepath, "r", encoding="utf-8") as myfile:
            data = myfile.read().split("---\n")        
            for item in data:
                leasson_item = item.split("*")
                Language = leasson_item[0]
                if Language == "JS":
                    Fasl = leasson_item[1]
                   
                   
                   
                    if query.message.chat_id == Manager:
                        button = [InlineKeyboardButton(Fasl, callback_data = "js" + Fasl), InlineKeyboardButton("🗑️", callback_data = "deljs" + Fasl)]
                    else:
                        button = [InlineKeyboardButton(Fasl, callback_data = "js" + Fasl)]
                    keyboard.append(button)

             
        reply_markup = InlineKeyboardMarkup(keyboard)
        context.bot.send_message(
            chat_id=query.from_user.id,
            text="📖فصل را انتخاب کنید",
            reply_markup=reply_markup
        )

        
        
    elif query.data.startswith("js"):
        fasl = query.data.replace("js","")
        with open(databasepath, "r", encoding="utf-8") as myfile:
            data = myfile.read().split("---\n")        
            for item in data:
                leasson_item = item.split("*")
                Language = leasson_item[0]
                Fasl = leasson_item[1]
                msgId = leasson_item[2]
                channeld = leasson_item[3]
                if Language == "JS" and fasl in Fasl:
                    
                    returntomenu = InlineKeyboardButton("بازگشت به منوی اصلی", callback_data='menu')
                    keyboard = [[returntomenu]]
                    reply_markup = InlineKeyboardMarkup(keyboard)
                    context.bot.copy_message(query.message.chat_id, channeld, msgId, reply_markup=reply_markup)
                    break
    elif query.data.startswith("deljs"):
        if query.message.chat_id != Manager:
            return
        fasl = query.data.replace("deljs","")
        with open(databasepath, "r", encoding="utf-8") as myfile:
            lines = myfile.readlines()
        with open(databasepath, "w", encoding="utf-8") as myfile:
            for line in lines:
                if fasl not in line:
                    myfile.write(line)
        context.bot.send_message(
            chat_id=Manager,
            text="فصل مورد نظر پاک شد ✅"
        )
        

def help1(update , context):
    context.bot.send_message(chat_id = update.message.chat_id , text= 'برای ارتباط با ادمین در بیو ایدی ادمین درج شده همچنان برای اطلاعات بیشتر میتوانید صفحه اینستاگرام ما را نیز دنبال کنید . \n  برای عضویت در کانال ماروی دستور /start کلیک نمایید.')


token.dispatcher.add_handler(CommandHandler('start', pleasejoinchannel))
token.dispatcher.add_handler(CommandHandler('help', help1))
# token.dispatcher.add_handler(CommandHandler('info', info))
# token.dispatcher.add_handler(CallbackQueryHandler(contact_buttons))
token.dispatcher.add_handler(CallbackQueryHandler(button_callback))
# token.dispatcher.add_handler(MessageHandler(Filters.text, send))
token.dispatcher.add_handler(MessageHandler(Filters.attachment, file_handler))





token.start_polling()
token.idle()