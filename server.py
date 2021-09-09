import asyncio
import datetime
import sys
import time

from pywizlight import discovery


async def find_bulb():
    bulbs = await discovery.discover_lights('192.168.50.255')
    try:
        bulb = bulbs[0]
        return bulb
    except IndexError:
        return None


async def main(wake_time: str):
    bulb = None
    for i in range(5):
        bulb = await find_bulb()
        if bulb:
            break
        time.sleep(1)
        print("Bulb not found")
    if not bulb:
        print("Could not find bulb, terminating")
        return
    print("Bulb found at %s" % bulb.ip)
    wake_time = wake_time.split(':')
    wake_hour = int(wake_time[0])
    wake_minute = int(wake_time[1])

    while True:
        current_time = datetime.datetime.now().time()
        current_hour = current_time.hour
        current_minute = current_time.minute

        if current_hour == wake_hour and current_minute == wake_minute:
            await bulb.turn_on()
            print("Bulb turned on")

        time.sleep(10)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()

    if len(sys.argv) < 2:
        print("Not enough arguments")
    else:
        loop.run_until_complete(main(sys.argv[1]))
