import asyncio
import os
from playwright.async_api import async_playwright

# --- 設定區域 ---
TELEGRAM_TOKEN = "你的_BOT_TOKEN"
CHAT_ID = "你的_CHAT_ID"
CHECK_INTERVAL = 300  # 每 5 分鐘檢查一次 (秒)

async def send_telegram_msg(message):
    import requests
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    requests.post(url, json=payload)

async def check_flights():
    async with async_playwright() as p:
        # 本地運行時建議 headless=False，你可以親眼看到它操作
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
        )
        page = await context.new_page()

        try:
            print("正在開啟國泰官網...")
            await page.goto("https://www.cathaypacific.com/cx/zh_HK/book-a-trip/redeem-flights.html", timeout=60000)
            
            # 等待畫面載入完成
            await asyncio.sleep(10)
            
            # --- 填表邏輯 ---
            # 這裡需要根據現場頁面元素進行填寫 (HKG, NRT, 2026-12-24)
            # 範例 (具體 selector 視官網更新而定):
            # await page.fill('input[name="origin"]', 'HKG')
            # await page.fill('input[name="destination"]', 'NRT')
            
            print("✅ 頁面加載成功！")
            await page.screenshot(path="local_check.png")
            
            # 如果邏輯判斷有位子：
            # await send_telegram_msg("🚨 發現 2026-12-24 有位子了！快去搶！")

        except Exception as e:
            print(f"❌ 運行錯誤: {e}")
        finally:
            await browser.close()

if __name__ == "__main__":
    # 在本地你可以寫一個無限循環
    while True:
        asyncio.run(check_flights())
        print(f"等待 {CHECK_INTERVAL} 秒後再次檢查...")
        time.sleep(CHECK_INTERVAL)
