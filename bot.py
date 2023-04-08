import discord
import responses
import os

# for K value by reference
class MyInt:
    def __init__(self, value):
        self.value = value

# Send messages
async def send_message(message, user_message, K):
    try:
        response = responses.handle_response(user_message, K)
        if isinstance(response, str):
            await message.channel.send(response)
        else:
            # try to send all images
            for item in response:
                try:
                    await message.channel.send(file=discord.File(item))
                    os.remove(item)
                except:
                    print("not able to send")

    except Exception as e:
        print(e)


def run_discord_bot():
    intents = discord.Intents.default()
    intents.members = True
    intents.message_content = True
    K = MyInt(5)

    TOKEN = '********************'  # <---------------------------------YOUR TOKEN HERE
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print(f'{client.user} is now running!')

    @client.event
    async def on_message(message):
        # Make sure bot doesn't get stuck in an infinite loop
        if message.author == client.user:
            return

        # Get data about the user
        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)

        # check for length of msg
        if len(user_message) < 1:
            return

        # must contain / as header for commands
        if user_message[0] == '/':
            user_message = user_message[1:]  # [1:] Removes the '/'
            await send_message(message, user_message, K)

    # Remember to run your bot with your personal TOKEN
    client.run(TOKEN)
