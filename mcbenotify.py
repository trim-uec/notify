from webhookposter import WebhookPoster
from configfilereader import ConfigFileReader
from logreader import LogReader
from logprocessor import LogProcessor
import glob
import time
import datetime as dt


def find_latest_log():
    logfiles = glob.glob('*.log')
    assert logfiles, 'ログファイルが見つかりませんでした。'
    return sorted(logfiles)[-1]  # ソートして最も新しいものを選ぶ


def printlog(mes):
    print('['+str(dt.datetime.now())[:-7]+']', mes)


# config
configfilereader = ConfigFileReader()
UPDATE_INTERVAL = configfilereader.read_int('UpdateInterval')
IGNORE_PLAYERS = configfilereader.read_str_list('IgnorePlayers')
WEBHOOK_URL = configfilereader.read_str('WebhookURL')

# メイン処理に必要なオブジェクト作成
logprocessor = LogProcessor()
LOGFILENAME = find_latest_log()
webhookposter = WebhookPoster(WEBHOOK_URL)
logreader = LogReader(LOGFILENAME)

printlog(''+LOGFILENAME+'を監視します。')

while True:
    time.sleep(UPDATE_INTERVAL)
    diff = logreader.added_lines()
    text = logprocessor.process(diff)
    has_posted = webhookposter.post_onlytext(text)
    if has_posted:
        printlog('Notification sent.')
    printlog('Updated. Time needed: '+str(
        (dt.datetime.now() - logreader.last_update).total_seconds()))
