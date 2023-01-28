import faust

app = faust.App('member-marks',broker='kafka://', store='rocksdb://')



channel = app.channel(value_type=str)
@app.agent(channel)
async def greet(greetings):
    async for greeting in greetings:
        print(greeting)

@app.timer(1.0)
async def populate():
    await channel.send("akshay")


