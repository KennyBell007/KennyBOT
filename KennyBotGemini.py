from dotenv import load_dotenv
import discord
import os
import google.generativeai as genai # Import Google Generative AI library

# Load environment variables from .env file
load_dotenv()
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY') # Changed to GOOGLE_API_KEY
DISCORD_TOKEN = os.getenv('TOKEN')

# Configure the Gemini client
genai.configure(api_key=GOOGLE_API_KEY)

def call_gemini(question): # Renamed function to call_gemini
    model = genai.GenerativeModel('gemini-pro') # Specify the Gemini model
    completion = model.generate_content(
        f"Respond like a pirate to the following question:  {question}"
    )
    # Print the response
    response = completion.text # Access the text content from Gemini's response
    print(response)
    return response


# Set up discord
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

    if message.content.startswith('$question'):
        print(f"Message: {message.content}")
        message_content = message.content.split("$question")[1]
        print(f"Question: {message_content}")
        response = call_gemini(message_content) # Changed to call_gemini
        print(f"Assistant: {response}")
        print("---")
        await message.channel.send(response)

client.run(DISCORD_TOKEN)
