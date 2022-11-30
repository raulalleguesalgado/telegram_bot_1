import asyncio
import telegram




async def main():
    myFile = open("/home/raulas/PycharmProjects/token.txt", "r")
    token_raul = myFile.read()
    # Programming
    myFile.close()
    bot = telegram.Bot(token_raul.strip())
    async with bot:
        await bot.send_message(text='Holaaaaa', chat_id=1314421918)


if __name__ == '__main__':
    asyncio.run(main())