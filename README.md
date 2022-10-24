# Attendance Bot

The main purpose of this Telegram Bot is to check the attendance by Telegram 'share location' option.

## How it works
Here is the description of how this script works, by mini roadmap, but in order to understand it properly you should look at the script
and check the comments

- Firstly, in **start** command Bot will shortly introduce to user his functions. In addition to this, it's saves users fullname and chatid to database for future reference.
- Then, it gives the user the command **get_location** after pressing this command, the bot asks the user to share the location. 
- When user shares location, script gets users latitude and longitude and measure the distance between office and user's location.
- Finally, it saves all this information to database and through the API you can get all these data(Users attendance in month, ).

## Do not forget

In **telegram_bot.py** write the Bot token to API_TOKEN and change the connection string of your database. 

