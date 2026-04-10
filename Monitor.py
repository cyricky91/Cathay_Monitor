import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        # 使用一組更像真人的啟動參數
        browser = await p.chromium.launch(
            headless=True,
            args=[
                "--disable-http2", 
                "--disable-blink-features=AutomationControlled",
                "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
            ]
        )
        
        # 設定香港當地的語言和時區
        context = await browser.new_context(
            locale="zh-HK",
            timezone_id="Asia/Hong_Kong",
            viewport={'width': 1920, 'height': 1080}
        )
        
        page = await context.new_page()

        try:
            print("嘗試低延遲連線...")
            # 移除 wait_until，只要連上就開始截圖
            await page.goto(url, timeout=90000) 
    
            # 手動給予足夠的固定等待時間，而不是等待網路閒置
            await asyncio.sleep(20) 
    
            await page.screenshot(path="github_result.png")
            print("✅ 截圖完成")

            # 如果截圖顯示有內容，我們就可以在此加入 fill("HKG") 等邏輯
            
        except Exception as e:
            print(f"❌ 依然發生錯誤: {e}")
            try:
                await page.screenshot(path="github_result.png")
            except:
                pass
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(run())
