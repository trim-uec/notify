# ログファイルの差分から、通知テキストを作成する
# 差分から通知に必要な情報を抽出、(欲しい情報を付加し、)文章として整形して文字列を返す


class LogProcessor:
    def __init__(self):
        pass

    # 必要な行を抽出し、各行を通知用の文章にフォーマットして、結合することで通知文書を作る
    # 差分がない場合、抽出されなかった場合、(除外した結果情報が全て無くなった場合、)...これらについてはNoneを返す
    def process(self, diff):
        if not diff:
            return None
        extracted_lines = self.extract(diff)  # 必要な行
        if not extracted_lines:
            return None  # 抽出されなかったら処理の必要無し
        formatted_lines = []
        for s in extracted_lines:
            formatted_lines.append(self.format(s))
        return ''.join(formatted_lines)

    # 行を受け取って人間に見やすく書き換えた行を返す
    # 例外はそのまま
    def format(self, line):
        # Player connected: -> **** さんがログインしました！
        # Player disconnected: -> **** さんがログアウトしました！
        # そのほか -> そのまま
        if 'Player connected:' in line:
            # コロンで区切って1要素目をカンマで区切って0要素目を取得、綺麗にしたものが名前
            player_name = line.split(':')[1].split(',')[0].strip()
            return ''+player_name+' さんがログインしました！\n'
        elif 'Player disconnected:' in line:
            player_name = line.split(':')[1].split(',')[0].strip()
            return ''+player_name+' さんがログアウトしました！\n'
        elif 'Stopping server' in line:
            return 'サーバーを停止します。\n'
        else:
            return line

        # 文字列のリストdiffを受け取り必要な行のみを抜粋して返す
        # NOTE 想定: プレイヤーのログインとログアウト、サーバーストップ
        # TODO 除外するプレイヤーを指定できるようにする。
    def extract(self, diff):
        if not diff:
            return None  # 差分がないなら結果は無し
        extracted = [s for s in diff if (
            'xuid' in s
            or
            'Stopping server' in s
        )] if diff else None
        if not extracted:
            return None  # 見つからないなら結果は無し
        return extracted
