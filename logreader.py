import datetime as dt
import os

# ログファイル差分チェッカー
# ファイル名を受け取り、update()実行ごとに差分を返す
# 更新実行時の時間をもつ
# 更新にかかった総所要時間の計測はせず、上のレイヤーに任せる
# 監視対象のファイルは行を追加する形で情報が増えていくものとする


class LogReader:

    # filename, last_update, tail_ix
    def __init__(self, filename):
        self.filename = filename
        self.last_update = dt.datetime.now()
        assert os.path.isfile(filename), '存在しないファイルを指定しました'
        with open(self.filename, 'r') as f:
            lines = f.readlines()
        self.tail_ix = len(lines)  # 末尾の行数(1から数えた場合の) = 次回更新でこの行数から読み込む
        # TODO ファイルの存在をassertできるともっと良い(import osでexists?)
        # TODO ログ出力はこれでよいのか？Viewクラス使ったほうがよいのでは？
        # self.__printlog('初期化成功。'+self.filename+'を監視します。')

    # 同期。last_updateを更新し、差分を取得し、tail_ixを更新。差分(文字列のリスト)を返す。無ければ空のリスト。
    def added_lines(self):
        self.last_update = dt.datetime.now()
        with open(self.filename, 'r') as f:
            all_lines = f.readlines()
        added_lines = all_lines[self.tail_ix:]
        self.tail_ix = len(all_lines)
        return added_lines

    # def __printlog(self, mes):
    #     print('['+str(dt.datetime.now())[:-7]+']', mes)
