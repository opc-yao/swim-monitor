import smtplib
from email.mime.text import MIMEText
from playwright.sync_api import sync_playwright

# ===== SWIM =====
SWIM_URL = "https://top.swim.mlit.go.jp/swim/login"
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
# ✅ 十分待つ
        page.wait_for_timeout(15000)
# ✅ 全入力欄を取得
        inputs = page.locator("input")
# ✅ 数確認（デバッグ）
        print("input数:", inputs.count())
# ✅ 上から順に試す（強引だけど確実）
        inputs.nth(0).fill(LOGIN_ID)
        inputs.nth(1).fill(LOGIN_PW)
# ✅ ボタン押す
        page.locator("button").first.click()
# ✅ 遷移待ち
        page.wait_for_timeout(10000)


        content = page.content()

        if TARGET in content:
            send_mail(f"✈️ {TARGET} が検知されました")

        browser.close()


if __name__ == "__main__":
    run()
