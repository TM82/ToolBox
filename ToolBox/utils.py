import os
import time
import json
import logging
import requests
from contextlib import contextmanager

SLACK_URL = os.getenv("SLACK_URL", "")

# # プロキシの設定
# proxies = {
#   'http': 'http://192.168.100.2:58888/',
#   'https': 'http://192.168.100.2:58888/'
# }

def start_logging(filename="job.log"):
    '''
    loggerを起動させる
    '''
    LOGGER = logging.getLogger('Logging')
    LOGGER.setLevel('INFO')
    fh = logging.FileHandler(filename)
    LOGGER.addHandler(fh)
    formatter = logging.Formatter('%(asctime)s:%(lineno)d:%(levelname)s:%(message)s')
    fh.setFormatter(formatter)
    return LOGGER

def progress_reporter(text, slack_url=SLACK_URL):
    '''
    該当slackチャンネルにメッセージを送信する
    slack urlが""の時は送らない
    '''
    if slack_url != "":
        data = json.dumps({"text": text, "username": 'progress_report'})
        # requests.post(slack_url, data=data, proxies=proxies)
        requests.post(slack_url, data=data)
    return

@contextmanager
def timer(name, LOGGER):
    '''
    with文で処理にかかる時間を測る
    '''
    LOGGER.info(f"start [{name}]")
    start = time.time()
    yield
    LOGGER.info(f'[{name}] done in {time.time() - start:.0f} s')

@contextmanager
def do_job(name, LOGGER):
    '''
    with文で処理にかかる時間を測りながらslackに通知
    '''
    LOGGER.info(f"start [{name}]")
    start = time.time()
    try:
        yield
        LOGGER.info(f'[{name}] done in {time.time() - start:.0f} s')
        progress_reporter(f'[{name}] done in {time.time() - start:.0f} s')
    except:
        import traceback, sys
        exc_type, exc_value, exc_traceback = sys.exc_info()
        exc_lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
        msg = f"failed {name} \n"
        msg += ''.join('' + line for line in exc_lines)
        LOGGER.info(msg)
        progress_reporter(msg)