import smtplib
from email.mime.text import MIMEText
from playwright.sync_api import sync_playwright

# ===== SWIM =====
SWIM_URL = "https://top.swim.mlit.go.jp/swim/login"
LOGIN_ID = "yao-opc@aerotoyota.co.jp"
LOGIN_PW = "@1234Dispatch"

TARGET = "JA6502"

# ===== メール設定 =====
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

EMAIL =  "yao.opc@gmail.com"
PASSWORD =  "cghq khwj rnbj bhms"  # ←ここに貼る

TO_EMAIL =  "yao-opc@aerotoyota.co.jp"



def send_mail(message):
    msg = MIMEText(message)
    msg["Subject"] = "SWIM確認"
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

        page.wait_for_timeout(10000)

        inputs = page.locator("input")

        print("input数:", inputs.count())

        inputs.nth(0).fill(LOGIN_ID)
        inputs.nth(1).fill(LOGIN_PW)

        page.locator("button").first.click()

        page.wait_for_timeout(15000)

        print("現在URL:", page.url)

        # スクリーンショット保存
        page.screenshot(
            path="swim.png",
            full_page=True
        )
        content = page.content()
        print("フライトプラン:", "フライトプラン" in content)
        print("利用サービス:", "利用サービス" in content)
        print("通報一覧:", "通報一覧" in content)
        with open("swim_page.html", "w", encoding="utf-8") as f:
            f.write(page.content())

        print("スクリーンショット保存完了")

        send_mail("✅ SWIMログイン確認成功")

        browser.close()


if __name__ == "__main__":
    run()
