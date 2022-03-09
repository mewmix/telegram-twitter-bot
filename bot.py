#!/usr/bin/env python
# pylint: disable=C0116,W0613
import tweepy
from functools import wraps

import logging
from telegram.ext import Updater, CommandHandler


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

LIST_OF_ADMINS = []



logger = logging.getLogger(__name__)
tgtoken = ""
consumer_key = ""
consumer_secret =""
access_token = ""
access_token_secret = ""

auth = tweepy.OAuth1UserHandler(
   consumer_key, consumer_secret, access_token, access_token_secret
)

api = tweepy.API(auth)

characters = "characters"

def restricted(func):
    @wraps(func)
    def wrapped(update, context, *args, **kwargs):
        user_id = update.effective_user.id
        if user_id not in LIST_OF_ADMINS:
            print("Unauthorized access denied for {}.".format(user_id))
            return
        return func(update, context, *args, **kwargs)
    return wrapped

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

@restricted
def post(update, context):
    try:
        number1 = str(update.message.text.replace('/post', ''))       
        result = number1
        posting = result
        post1 = api.update_status(f"{posting}")
        global posted
        posted = (post1.id)
        globals()['posted']=post1.id

        update.message.reply_text('The post is: '+str(posting))
        update.message.reply_text('The url is https://twitter.com/staysafeco/status/'+str(posted))
        truth = len(result) - 1
        update.message.reply_text('There are '  +str(truth) + (characters)) 
        
    except (IndexError, ValueError):
        update.message.reply_text('There are not enough or too many characters')
    

@restricted
def comment(update, context):
    try:
        number1 = str(update.message.text.replace('/comment', ''))
        result = number1
        posting = result
        comt =  api.update_status(status = posting, in_reply_to_status_id = posted, auto_populate_reply_metadata=True)
        postd = (comt.id)

 
        

        update.message.reply_text('The post is: '+str(posting))
        update.message.reply_text('The url is https://twitter.com/staysafeco/status/'+str(postd))


    except (IndexError, ValueError):
        update.message.reply_text('There are not enough or too many characters')
    


def length(update, context):
    try:
        number1 = str(update.message.text.replace('/length', ''))
        result = number1
        truth = len(result) - 1
        update.message.reply_text('There are '  +str(truth) + (characters))
        update.message.reply_text('The url is https://twitter.com/staysafeco/status/'+str(posted))

    except (IndexError, ValueError):
        update.message.reply_text('There are not enough or too many characters')




def main():
    updater = Updater(tgtoken, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("post", post))
    dp.add_handler(CommandHandler("comment", comment))
    dp.add_handler(CommandHandler("length", length))


    dp.add_error_handler(error)
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
