import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        # 加入 --disable-http2 是解決協定錯誤的關鍵
        browser = await p.chromium.launch(
            headless=True, 
            args=["--disable-http2", "--no-sandbox"]
        )
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
        )
        page = await context.new_page()

        try:
            print("開始連線國泰...")
            # 優先嘗試 domcontentloaded
            await page.goto("https://www.cathaypacific.com/cx/zh_HK/book-a-trip/redeem-flights.html", wait_until="domcontentloaded", timeout=60000)
            
            # 等待畫面渲染，國泰網站載入較慢
            await asyncio.sleep(15)
            
            # 嘗試截圖，這張圖會顯示我們是否成功進入了搜尋表單
            await page.screenshot(path="github_result.png", full_page=True)
            print("✅ 截圖完成")
            
        except Exception as e:
            print(f"❌ 出錯: {e}")
            # 失敗也截一張圖看錯誤畫面
            await page.screenshot(path="github_result.png")
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(run())
