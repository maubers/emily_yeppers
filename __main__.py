#!/usr/bin/env python3
'''
Main file for the bot. This is where the magic happens.
'''
from bot_config import *
from stream_handler import *
import asyncio

async def main():
    reddit = asyncpraw.Reddit(client_id=clientID,
                              client_secret=clientSecret,
                              username=username,
                              password=password,
                              user_agent=userAgent)
    queue = asyncio.Queue()

    streams = await subreddit_streams(reddit, subreddits)
    asyncio.create_task(enqueue_items(streams, queue))
    asyncio.create_task(enqueue_unread_messages(reddit, queue))

    await process_queue(queue, reddit)


if __name__ == "__main__":
    asyncio.run(main())