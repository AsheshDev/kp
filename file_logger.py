import asyncio

async def log_to_file(message_queue):
    with open("keystroke_log.txt", "a") as file:
        while True:
            message = await message_queue.get()
            if message is None:
                break
            file.write(message)
            message_queue.task_done()
