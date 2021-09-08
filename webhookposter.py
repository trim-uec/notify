import requests

# LogMonitorを用いて差分を取得、そのデータを何らかの方法で整形したうえで、所定の手段で通知を行う。
# 暫定的にwebhookを用いたものとする


class WebhookPoster:

    # webhook_url
    def __init__(self, webhook_url):
        self.webhook_url = webhook_url

    def post_onlytext(self, text):
        if not text:
            return None
        main_content = {
            'content': text  # NOTE contentは2000文字を超えると送信不可になるため注意
        }
        requests.post(self.webhook_url, main_content)
        # print('Notification sent.')  # TODO ログ表示の見直し
        return True
