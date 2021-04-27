# ToolBox

- contextmanagerを用いて，実験ログを保存するためのライブラリ
- logファイルへの保存だけでなく，slackへの通知も可能

# How to use

1. 環境変数に `export SLACK_URL=<Slack AppのチャンネルURL>`を追加
  - 該当するSlack Appにメッセージ投稿権限を与えること
2. コード例
```
from ToolBox.utils import start_logging,timer,do_job

LOGGER = start_logging(filename=WORK_DIR+"log/0_sample.log")

if __name__ == '__main__':
    LOGGER.info('')
    LOGGER.info('logging start')
    
    with do_job('read',LOGGER): #コードブロックが始まるタイミングと終わるタイミングで，logファイルの記録+終わるタイミングでslack通知
      df = pd.read_pickle(...)
    
    with timer('edit',LOGGER): #コードブロックが始まるタイミングと終わるタイミングで,logファイルは記録されるがslack通知は行わない
      x = y + z
```
3. ログ例(0_sample.log)
```
2020-09-23 03:45:48,516:30:INFO:
2020-09-23 03:45:48,516:31:INFO:logging start
2020-09-23 03:45:48,516:53:INFO:start [read]
2020-09-23 03:55:21,960:57:INFO:[read] done in 573 s
2020-09-23 03:55:22,123:60:INFO:start [edit]
2020-09-23 03:57:32,717:65:INFO:failed edit
Traceback (most recent call last):
  File "/home/t-miura/notebooks/2020_complexnetwork/execution/core/utils.py", line 57, in do_job
    yield
  File "core/0_extract_citation.py", line 40, in <module>
    x = y + z
NameError: name 'y' is not defined
```
