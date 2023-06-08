
'''
This file contains the main logic for the bot. It handles all the streams, queues, and processing of items.
'''
from bot_config import *
from response_handler import generate_response
import asyncio
import asyncpraw
import logging
import re
import traceback


# Handles all subreddits specified to stream new content from
async def subreddit_streams(reddit, subreddits):

    streams = []

    for subreddit_name in subreddits:
        subreddit = await reddit.subreddit(subreddit_name)
        comment_stream = subreddit.stream.comments(skip_existing=True)
        submission_stream = subreddit.stream.submissions(skip_existing=True)
        streams.extend([comment_stream, submission_stream])

    return streams


# Adds all items to the queue for processing
async def enqueue_items(streams, queue):
    async def enqueue_stream(stream):
        async for item in stream:
            await queue.put(item)

    tasks = [asyncio.create_task(enqueue_stream(stream)) for stream in streams]
    await asyncio.gather(*tasks)


# Adds messages to the queue for processing
async def enqueue_unread_messages(reddit, queue):
    while True:
        unread_messages = reddit.inbox.unread(limit=None)
        async for message in unread_messages:
            await queue.put(message)
            await message.mark_read()
        await asyncio.sleep(30)  # Check for unread messages every half minute


# Iterates through the queue
async def process_queue(queue, reddit):
    processed_items = set()

    while True:
        item = await queue.get()

        if item.id not in processed_items:
            isValidItem = await itemIsValid(item, reddit)
            print('\n')
            if isValidItem:
                print("Item is valid. Running handle_bot_reply...")
                await handle_bot_reply(item)
                processed_items.add(item.id)


# Checks if item is valid for a response
async def itemIsValid(item, reddit):
    print("Checking item", item)

    try:
        if (item.author.name.lower() == username.lower()):
            print("Bot is the author. Returning false.")
            return False

        else:
            if isinstance(item, asyncpraw.models.Comment):
                print("Comment detected")
                print(f'Contents: {item.body}')

                parent_id = item.parent_id
                bot_in_comment_chain = False

                
                while parent_id.startswith("t1_"):
                    parent_comment = await reddit.comment(parent_id[3:])  # Remove the 't1_' prefix
                    await parent_comment.load()

                    if parent_comment.author.name.lower() == username.lower():
                        bot_in_comment_chain = True
                        break

                    parent_id = parent_comment.parent_id

                if re.search(shutup_mention, item.body, flags=re.IGNORECASE):
                    print(f'Stopping bot from replying - user told it to shut up')
                    return False
                
                elif bot_in_comment_chain:
                    print(f'Replying to item - bot in comment chain')
                    return True


                elif re.search(bot_mention, item.body, flags=re.IGNORECASE):
                    print(f'Replying to item - bot mention')
                    return True

                else:
                    for phrase in TARGET_PHRASES:
                        if trigger_regex.search(item.body.lower()):
                            print(f'Replying to item - target phrase in body.')
                            return True

            elif isinstance(item, asyncpraw.models.Submission):
                print("Submission Detected")
                print(f'Contents: {item.selftext}')
                
                for phrase in TARGET_PHRASES:
                    if trigger_regex.search(item.title.lower()):
                        print(f'Replying to item - target phrase in title')
                        return True

                    elif trigger_regex.search(item.selftext.lower()):
                        print(f'Replying to item - target phrase in body.')
                        return True
                        
                print(f'Finished checking other submission checks. Now checking for a bot mention in {item.selftext}')
                
                if re.search(bot_mention, item.selftext, flags=re.IGNORECASE):
                        print(f'Replying to item - bot mention')

                        return True
    except Exception as e:
        print("An error occurred: ", e)
        traceback.print_exc()

    print("Item is not valid")
    return False


async def handle_bot_reply(item):
    try:
        author = item.author.name.lower()

        if isinstance(item, asyncpraw.models.Comment):
            text = item.body
        elif isinstance(item, asyncpraw.models.Submission):
            text = item.title + "." + item.selftext
        else:
            text = item.body  # For mentions and replies (Message instances)

        response_text = generate_response(text, author)
        reply = await item.reply(response_text)
        print("Successfully posted reply")
        await asyncio.sleep(30)  # Add a delay before refreshing the comment
        await reply.refresh()


    except Exception as e:
        logging.error(f"Error while handling target phrase: {e}")
