import time
import traceback
from threading import Timer

import praw
import prawcore
import yaml


def lock_submission(*args, **kwargs):
    """
    When the timer expires, locks the submissions and leaves a comment
    :param args:
    :param kwargs:
    """
    submission = args[0]
    submission.mod.lock()
    response = f"{kwargs['reply']}\n\n^(This action was performed by a bot, please contact the mods for any questions.)"
    submission.reply(response)

    timers = args[1]
    del timers[submission.id]


def main():
    global failed_attempt

    with open('config.yaml') as stream:
        bot_config = yaml.safe_load(stream)

    # Logging into Reddit
    reddit = praw.Reddit(client_id=bot_config['reddit_credentials']['client_id'],
                         client_secret=bot_config['reddit_credentials']['client_secret'],
                         username=bot_config['reddit_credentials']['username'],
                         password=bot_config['reddit_credentials']['password'],
                         user_agent=bot_config['reddit_credentials']['user_agent'])
    subreddit = reddit.subreddit(bot_config['subreddit'])

    print("Bot is now live!", time.strftime('%I:%M %p %Z'))
    timers = {}

    # Gets 100 historical submission
    submission_stream = subreddit.stream.submissions(pause_after=-1, skip_existing=True)
    while True:
        try:
            for submission in submission_stream:
                if submission is None:
                    break
                submission_flair = submission.link_flair_text.lower()
                timer_value = -1
                try:
                    if 'min' in submission_flair:
                        timer_value = int(submission.link_flair_text.lower().split()[0]) * 60
                    elif 'hour' in submission_flair:
                        timer_value = int(submission.link_flair_text.lower().split()[0]) * 60 * 60
                except ValueError:
                    print(f"The submission https://www.reddit.com/{submission.permalink} skipped because the timer"
                          f"value could not be understood.")

                if timer_value > 0:
                    t = Timer(timer_value, lock_submission, args=(submission, timers),
                              kwargs={'reply': bot_config['comment'].replace('{{author}}', submission.author.name)})
                    t.start()
                    timers[submission.id] = t

                failed_attempt = 1
        except KeyboardInterrupt:
            # Cancel all the timers before quitting the program
            for key, value in timers.items():
                value.cancel()
            print("Bot has stopped!", time.strftime('%I:%M %p %Z'))
            quit(0)

        except Exception as exp:
            tb = traceback.format_exc()
            print(tb)
            # In case of server error pause for multiple of 5 minutes
            if isinstance(exp, (prawcore.exceptions.ServerError, prawcore.exceptions.RequestException)):
                print(f"Waiting {(300 * failed_attempt) / 60} minutes...")
                time.sleep(300 * failed_attempt)
                failed_attempt += 1


if __name__ == '__main__':
    failed_attempt = 1
    main()
