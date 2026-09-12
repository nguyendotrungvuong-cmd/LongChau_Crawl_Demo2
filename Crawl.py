# export_all_products_fixed.py
import asyncio
import csv
from urllib.parse import quote
from playwright.async_api import async_playwright

async def run_full_pipeline():
    keyword = "canxi"
    encoded_keyword = quote(keyword)
    search_url = f"https://nhathuoclongchau.com.vn/tim-kiem?s={encoded_keyword}"
    
    print(f"🚀 [PIPELINE] Bắt đầu cào toàn bộ sản phẩm cho từ khóa: '{keyword}'...")

    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox",
                "--disable-dev-shm-usage"
            ]
        )
        
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 800}
        )
        
        page = await context.new_page()
        await page.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        extracted_products = {}
        total_expected = None

        async def handle_response(response):
            nonlocal total_expected
            if ("search" in response.url or "product" in response.url) and response.status == 200:
                try:
                    content_type = response.headers.get("content-type", "")
                    if "application/json" in content_type:
                        data = await response.json()
                        
                        if isinstance(data, dict):
                            for total_key in ["total", "totalCount", "count", "total_count"]:
                                if total_key in data and isinstance(data[total_key], int):
                                    total_expected = data[total_key]

                        items = []
                        if isinstance(data, dict):
                            for key in ["products", "data", "items", "result"]:
                                if key in data and isinstance(data[key], list):
                                    items = data[key]
                                    break
                        elif isinstance(data, list):
                            items = data

                        if items:
                            count_added = 0
                            for item in items:
                                if not isinstance(item, dict):
                                    continue
                                sku = item.get("sku", "") or item.get("id", "")
                                if not sku:
                                    continue
                                    
                                web_name = item.get("webName", "") or item.get("name", "")
                                brand = item.get("brand", "")
                                
                                # Cố gắng lấy danh mục từ nhiều nhánh dữ liệu khác nhau của JSON
                                category = item.get("category")
                                category_name = ""
                                if isinstance(category, dict):
                                    category_name = category.get("name", "") or category.get("title", "")
                                elif isinstance(category, str):
                                    category_name = category
                                
                                # Nếu API tìm kiếm không trả về category, tạm gán theo từ khóa tìm kiếm hoặc để trống
                                if not category_name:
                                    category_name = "Thực phẩm chức năng" if "canxi" in keyword.lower() else "Sản phẩm khác"

                                slug = item.get("slug", "")
                                product_url = f"https://nhathuoclongchau.com.vn/{slug}" if slug else ""

                                if sku not in extracted_products:
                                    extracted_products[sku] = {
                                        "SKU": sku,
                                        "Tên sản phẩm": web_name,
                                        "Thương hiệu": brand,
                                        "Danh mục": category_name,
                                        "Đường dẫn": product_url
                                    }
                                    count_added += 1
                                    
                            if count_added > 0:
                                target_str = f" / {total_expected}" if total_expected else ""
                                print(f"🎯 Đã bắt thêm {count_added} sản phẩm | Tổng hiện tại: {len(extracted_products)}{target_str}")
                except Exception:
                    pass

        page.on("response", handle_response)

        try:
            print(f"🌐 Đang truy cập: {search_url}")
            await page.goto(search_url, wait_until="domcontentloaded", timeout=60000)
            await asyncio.sleep(4)
            
            max_attempts = 40  
            no_new_count = 0
            last_count = 0

            for step in range(max_attempts):
                if total_expected and len(extracted_products) >= total_expected:
                    print(f"🎉 Đã cào đủ toàn bộ {total_expected} sản phẩm từ API!")
                    break

                try:
                    load_more_btn = page.locator("button").filter(has_text="Xem thêm")
                    
                    if await load_more_btn.count() > 0 and await load_more_btn.first.is_visible():
                        await load_more_btn.first.scroll_into_view_if_needed()
                        await asyncio.sleep(1)
                        
                        print(f"🔄 Đang bấm nút 'Xem thêm' (Lần {step + 1})...")
                        await load_more_btn.first.click()
                        await asyncio.sleep(3.5)
                    else:
                        print("ℹ️ Không tìm thấy nút 'Xem thêm' nữa. Đang chờ đồng bộ dữ liệu...")
                        await asyncio.sleep(2)
                except Exception as e:
                    print(f"⚠️ Lỗi khi click: {e}")

                current_count = len(extracted_products)
                if current_count == last_count:
                    no_new_count += 1
                    if no_new_count >= 5:
                        print("✅ Đã tải xong toàn bộ danh sách.")
                        break
                else:
                    no_new_count = 0
                    last_count = current_count
                
        except Exception as e:
            print(f"⚠️ Lỗi trong quá trình duyệt trang: {e}")

        await browser.close()

        product_list = list(extracted_products.values())
        if product_list:
            filename = f"longchau_{keyword}_{len(product_list)}sp.csv"
            keys = ["SKU", "Tên sản phẩm", "Thương hiệu", "Danh mục", "Đường dẫn"]
            
            with open(filename, "w", newline="", encoding="utf-8-sig") as f:
                writer = csv.DictWriter(f, fieldnames=keys)
                writer.writeheader()
                writer.writerows(product_list)
                
            print(f"\n✨ [HOÀN TẤT] Đã xuất thành công {len(product_list)} sản phẩm ra file: {filename}")
        else:
            print("\n❌ Không bắt được dữ liệu sản phẩm nào.")

if __name__ == "__main__":
    asyncio.run(run_full_pipeline())