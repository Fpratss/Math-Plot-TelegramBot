import logging
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
)
from bob_telegram_tools.bot import TelegramBot
import numpy as np
import matplotlib.pyplot as plt


    

# Definition a few command handlers. 
def start_command(update,context):
    """Send a message when the command /start is issued."""

    s=""" Hi! my name is fprat and I am a bot created for an academic purpose. I can help you to know if a number is even, odd or prime! 
    Also, I can plot a normal distribution with mu and sigma parameters and give you random numbers. I can be your dice!. Just type /help 
    to see how to play with me!
     """

    update.message.reply_text(s)


def help_command(update,context):
    """Send a message when the command /help is issued."""

    h="""*Commands available*
    /even ->To check wether a number is even or odd. E.G. /even 83
    /prime -> To check wether a number is prime or not.E.G. /prime 73
    /normal -> plot normal distribution with parameters mu and sigma. E.G. /normal 0 1
    /random-> tell me which and how many random values you want! E.G. /random 1 8 3, 3 random numbers between 1 and 8. 
    """

    update.message.reply_text(h)



def prime_command(update, context):
    try:
        n_2 = int(context.args[0])       
        for i in range(2,n_2):
            if(n_2%i)==0:
                return update.message.reply_text(str(n_2)+" Is not prime")
            else:
                return update.message.reply_text(str(n_2)+" Is a prime number")
    except (ValueError):
        update.message.reply_text("Ups! Something went wrong.")

def even_command(update, context):
    try:
     n_1 = int(context.args[0])
     if n_1 % 2 ==0:
         return update.message.reply_text(str(n_1)+" Is even ")
     else:
        return update.message.reply_text(str(n_1)+" Is odd ")


    except (ValueError):
        update.message.reply_text("Use numbers please")



def normal_command(update, context):
    try:
        token = 'Your token'
        user_id = int('chat id')
        bot = TelegramBot(token, user_id)
        mu=int(context.args[0])
        sigma=int(context.args[1])
        s=np.random.normal(mu,sigma,10000)
        
        count, bins, ignored =plt.hist(s, 30, density=True)
        
        plt.plot(bins, 1/(sigma * np.sqrt(2 * np.pi)) *np.exp( - (bins - mu)**2 / (2 * sigma**2) ), linewidth=2, color='r')
        
        bot.send_plot(plt)
# This method delete the generetad image
        bot.clean_tmp_dir()

    except (ValueError):
        update.message.reply_text("Use numbers please")



def random_command(update, context):
    try:
        
        V_1=int(context.args[0])
        V_2=int(context.args[1])
        V_3=int(context.args[2])
        out=np.random.randint(V_1,V_2,V_3)

        update.message.reply_text(" These are your random numbers: "+str(out))

    except (ValueError):
        update.message.reply_text("Ups! Something wrong happened!")


def main():
    #We create updater variable.
    updater = Updater(" Your Token",use_context=True)

    # #We create a dispatcher variable. This variable will dispatch whatever is updated to our telegram bot
    dispatcher = updater.dispatcher

    #Get response on commands
    dispatcher.add_handler(CommandHandler("start", start_command))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("even", even_command))
    dispatcher.add_handler(CommandHandler("prime", prime_command))
    dispatcher.add_handler(CommandHandler("normal", normal_command))
    dispatcher.add_handler(CommandHandler("random", random_command))


    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
