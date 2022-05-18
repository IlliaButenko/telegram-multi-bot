from pyrogram import Client

api_id = 16444352
api_hash = '85f0a6a4881b0f4122724d25ffc0de8a'
app = Client("gen",
             api_id=api_id,
             api_hash=api_hash)
async def main():
    async with app:
        await app.send_message("@TalentedBlockchainDeveloper", "Hi!")
app.run(main())
