import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        # 強制偽裝與禁用自動化標記
        browser = await p.chromium.launch(
            headless=True,
            args=[
                "--disable-http2", 
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox"
            ]
        )
        
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
            locale="zh-HK",
            viewport={'width': 1280, 'height': 800}
        )
        
        page = await context.new_page()
        # 定義漏掉的 url 變數
        target_url = "https://www.cathaypacific.com/cx/zh_HK/book-a-trip/redeem-flights.html"

        try:
            print("嘗試低延遲連線至國泰官網...")
            # 移除 wait_until 限制，只要連上就開始計時，避免 60s 超時
            await page.goto(target_url, timeout=90000) 
            
            print("連線成功，等待頁面渲染 (20秒)...")
            await asyncio.sleep(20) 
            
            # 截圖確認畫面
            await page.screenshot(path="github_result.png", full_page=True)
            print("✅ 截圖完成，請檢查 Artifacts。")
            
        except Exception as e:
            print(f"❌ 依然發生錯誤: {e}")
            # 發生錯誤時也嘗試截圖，幫助分析是在哪一關被擋
            try:
                await page.screenshot(path="github_result.png")
            except:
                pass
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(run())
