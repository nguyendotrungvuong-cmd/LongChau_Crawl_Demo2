# 🛒 Long Chau Scraper (Playwright & Network Interception)

Công cụ cào dữ liệu (Scraper) tự động sử dụng **Python** và **Playwright** để trích xuất toàn bộ danh sách sản phẩm từ trang web Nhà thuốc FPT Long Châu thông qua việc bắt các gói tin API ngầm (Network Interception).

## ✨ Tính năng nổi bật
* **Nhập từ khóa tùy ý**: Hỗ trợ nhập bất kỳ từ khóa nào từ bàn phím khi chạy chương trình (ví dụ: *canxi, sữa tắm, vitamin...*) để tìm kiếm và cào dữ liệu động.
* **Vượt rào bảo mật & Chống Bot**: Tích hợp các cấu hình ẩn danh tính tự động (`navigator.webdriver`, User-Agent) giúp né tránh các cơ chế phòng thủ.
* **Bắt API trực tiếp**: Thu thập trực tiếp dữ liệu JSON từ các gói tin phản hồi ngầm, đảm bảo tốc độ cực nhanh và đầy đủ trường thông tin.
* **Tự động bấm "Xem thêm"**: Tự động nhận diện nút "Xem thêm" theo thời gian thực, cuộn màn hình và click liên tục cho đến khi vét sạch 100% danh sách sản phẩm.
* **Lọc trùng lặp & Xuất file sạch**: Tự động gom nhóm dựa trên `SKU` để loại bỏ sản phẩm trùng và xuất ra file `.csv` chuẩn định dạng UTF-8-sig hiển thị tiếng Việt hoàn hảo trên Excel.

---

## 🛠️ Yêu cầu hệ thống
* Python 3.8 trở lên.
* Thư viện `playwright`.

---

## ⚙️ Hướng dẫn cài đặt và Chạy

### 1. Cài đặt thư viện
Chạy lệnh sau trong Terminal / Command Prompt để cài đặt Playwright:
```
pip install playwright
playwright install
```
## Có sử dụng và tham khảo GEMINI AI
⚠️ Cam kết sử dụng: Mã nguồn và công cụ này chỉ được tạo ra và chia sẻ hoàn toàn với mục đích học tập và nghiên cứu kỹ thuật (Educational & Research purposes).
