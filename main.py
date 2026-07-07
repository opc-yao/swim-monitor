from playwright.sync_api import sync_playwright
import smtplib
from email.mime.text import MIMEText
import os

SWIM_URL = "https://top.swim.mlit.go.jp/swim/login"

LOGIN_ID = "aak-opr@aerotoyota.co.jp"
LOGIN_PW = "@1234Dispatch"


def send_mail(subject, body):

    gmail_user = os.environ["GMAIL_USER"]
    gmail_pass = os.environ["GMAIL_APP_PASSWORD"]

    msg = MIMEText(body, "plain", "utf-8")

    msg["Subject"] = subject
    msg["From"] = gmail_user
    msg["To"] = gmail_user

    with smtplib.SMTP_SSL(
        "smtp.gmail.com",
        465
    ) as smtp:

        smtp.login(
            gmail_user,
            gmail_pass
        )

        smtp.send_message(msg)


def run():
    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=True
        )

        page = browser.new_page()

        # ログイン
        page.goto(SWIM_URL)

        page.wait_for_timeout(10000)

        inputs = page.locator("input")

        print("input数:", inputs.count())

        inputs.nth(0).fill(LOGIN_ID)
        inputs.nth(1).fill(LOGIN_PW)

        page.locator("button").first.click()

        page.wait_for_timeout(15000)

        print("現在URL:", page.url)

        # フライトプラン登録サービス
        page.goto(
            "https://web.swim.mlit.go.jp/f1fprg/browse/fia627s010"
        )

        page.wait_for_timeout(10000)

        cards = page.locator("swim-card2")

        print("カード数:", cards.count())

        # 通報一覧
        cards.nth(1).click()

        page.wait_for_timeout(10000)

        pages = page.context.pages

        print("ページ数:", len(pages))

        notification_page = pages[1]

        notification_page.wait_for_timeout(10000)

        print(
            "通報一覧URL:",
            notification_page.url
        )

        content = notification_page.content()

        # HTML保存
        with open(
            "notification_page.html",
            "w",
            encoding="utf-8"
        ) as f:
            f.write(content)

        notification_page.screenshot(
            path="notification_page.png",
            full_page=True
        )

        found = "JA6502" in content

        print("JA6502:", found)

        if found:

            send_mail(
                "SWIM通知",
                "JA6502を検知しました"
            )

            print("メール送信完了")

        else:

            print(
                "JA6502は見つかりませんでした"
            )

        browser.close()


if __name__ == "__main__":
    run()
