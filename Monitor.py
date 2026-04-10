# main.py
import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        # 使用 commit 參數模擬真實瀏覽器啟動
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        # 設置過大的超時是沒用的，我們改用分段等待
        try:
            print("啟動國泰監控...")
            # 只等待 DOM 加載
            await page.goto("https://www.cathaypacific.com/cx/zh_HK.html", wait_until="commit")
            await asyncio.sleep(5)
            
            # 嘗試直接跳轉到搜尋結果 API (如果能分析出規律)
            # 或者執行你的輸入邏輯...
            
            await page.screenshot(path="github_result.png")
            print("監控完成")
        except Exception as e:
            print(f"錯誤: {e}")
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(run())
