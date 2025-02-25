import requests
from bs4 import BeautifulSoup
import os

# 監視するブログURL（チェックしたいブログのアドレス）
BLOG_URL = "https://blog.goo.ne.jp/shinanren"

# LINE Notify のアクセストークン（GitHub に登録するので、ここは空欄でOK）
LINE_TOKEN = os.getenv("LINE_TOKEN")

def get_latest_article():
    """ 最新記事のタイトルとリンクを取得する """
    response = requests.get(BLOG_URL)
    soup = BeautifulSoup(response.text, "html.parser")

    # 最新記事の取得（ブログのHTML構造に合わせて変更する）
    article = soup.find("div", class_="entrylist").find("a")
    latest_link = article["href"]
    latest_title = article.text.strip()

    return latest_link, latest_title

def send_line_notify(message):
    """ LINEグループに通知を送る """
    url = "https://notify-api.line.me/api/notify"
    headers = {"Authorization": f"Bearer {LINE_TOKEN}"}
    data = {"message": message}
    requests.post(url, headers=headers, data=data)

def check_and_notify():
    """ 記事をチェックして更新があれば通知を送る """
    latest_link, latest_title = get_latest_article()
    send_line_notify(f"🆕 新しい記事が投稿されました！\n📌 {latest_title}\n🔗 {latest_link}")

# スクリプト実行
check_and_notify()
