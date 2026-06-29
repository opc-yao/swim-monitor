import smtplib
from email.mime.text import MIMEText
from playwright.sync_api import sync_playwright

# ===== SWIM =====
SWIM_URL = "https://top.swim.mlit.go.jp/swim"
LOGIN_ID = "yao-opc@aerotoyota.co.jp"
LOGIN_PW = "@1234Dispatch"

TARGET = "JA6502"

# ===== メール設定 =====
SMTP_SERVER = "smtp.office365.com"
SMTP_PORT = 587

EMAIL =  "yutazaki0506@outlook.jp"
PASSWORD =  "rcnljhvguyuzvrtg"  # ←ここに貼る

TO_EMAIL =  "yao-opc@aerotoyota.co.jp"


def send_mail(message):
    msg = MIMEText(message)
    msg["Subject"] = "SWIM検知通知"
    msg["From"] = EMAIL
    msg["To"] = TO_EMAIL

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL, PASSWORD)
        server.send_message(msg)


def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto(SWIM_URL)

        page.fill("input[type='text']", LOGIN_ID)
        page.fill("input[type='password']", LOGIN_PW)
        page.click("button")

        page.wait_for_timeout(5000)

        page.click("text=利用サービス一覧")
        page.click("text=フライトプラン登録サービス")
        page.click("text=通報一覧")

        page.wait_for_timeout(5000)

        content = page.content()

        if TARGET in content:
            send_mail(f"✈️ {TARGET} が検知されました")

        browser.close()


if __name__ == "__main__":
    run()
