import json
from datetime import datetime

# File lưu danh sách công việc
FILE_NAME = "todo_list.json"

# Danh sách công việc (list chứa dict)
# Mỗi công việc là một dict: {"ten": "...", "mo_ta": "...", "uu_tien": 1-5, "hoan_thanh": False, "ngay_tao": "..."}
cong_viec = []

def tai_danh_sach():
    """Đọc danh sách từ file JSON"""
    global cong_viec
    try:
        with open(FILE_NAME, "r", encoding="utf-8") as f:
            cong_viec = json.load(f)
        print(f"Đã tải {len(cong_viec)} công việc từ file.")
    except FileNotFoundError:
        print("Chưa có file lưu → bắt đầu danh sách mới.")
    except Exception as e:
        print(f"Lỗi khi đọc file: {e}")

def luu_danh_sach():
    """Lưu danh sách vào file JSON"""
    try:
        with open(FILE_NAME, "w", encoding="utf-8") as f:
            json.dump(cong_viec, f, ensure_ascii=False, indent=4)
        print("Đã lưu danh sách công việc.")
    except Exception as e:
        print(f"Lỗi khi lưu file: {e}")

def them_cong_viec():
    """Thêm công việc mới"""
    ten = input("Nhập tên công việc: ").strip()
    if not ten:
        print("Tên không được để trống!")
        return

    mo_ta = input("Mô tả (nếu có): ").strip()
    uu_tien = input("Ưu tiên (1-5, mặc định 3): ").strip()
    uu_tien = int(uu_tien) if uu_tien.isdigit() and 1 <= int(uu_tien) <= 5 else 3

    cv = {
        "ten": ten,
        "mo_ta": mo_ta,
        "uu_tien": uu_tien,
        "hoan_thanh": False,
        "ngay_tao": datetime.now().strftime("%Y-%m-%d %H:%M")
    }
    cong_viec.append(cv)
    print(f"Đã thêm: {ten}")

def danh_sach_cong_viec(chua_hoan_thanh=False):
    """In danh sách công việc (có thể lọc chỉ việc chưa hoàn thành)"""
    if not cong_viec:
        print("Danh sách trống!")
        return

    # Dùng list comprehension + lambda để lọc và sắp xếp
    ds = cong_viec
    if chua_hoan_thanh:
        ds = [cv for cv in cong_viec if not cv["hoan_thanh"]]

    # Sắp xếp theo ưu tiên giảm dần (cao trước), rồi theo ngày tạo
    ds_sorted = sorted(ds, key=lambda cv: (-cv["uu_tien"], cv["ngay_tao"]))

    print(f"\nDanh sách công việc ({'chưa hoàn thành' if chua_hoan_thanh else 'tất cả'}):")
    for i, cv in enumerate(ds_sorted, 1):
        trang_thai = "✓ Hoàn thành" if cv["hoan_thanh"] else "☐ Chưa làm"
        print(f"{i}. [{trang_thai}] {cv['ten']} (Ưu tiên: {cv['uu_tien']})")
        if cv["mo_ta"]:
            print(f"   Mô tả: {cv['mo_ta']}")
        print(f"   Ngày tạo: {cv['ngay_tao']}\n")

def hoan_thanh_cong_viec():
    """Đánh dấu công việc hoàn thành"""
    danh_sach_cong_viec(chua_hoan_thanh=True)
    if not any(not cv["hoan_thanh"] for cv in cong_viec):
        print("Không có công việc chưa hoàn thành!")
        return

    try:
        so_thu_tu = int(input("Nhập số thứ tự công việc đã hoàn thành: "))
        # Tìm công việc chưa hoàn thành (dùng enumerate + filter)
        chua_hoan_thanh = [cv for cv in cong_viec if not cv["hoan_thanh"]]
        if 1 <= so_thu_tu <= len(chua_hoan_thanh):
            cv = chua_hoan_thanh[so_thu_tu - 1]
            cv["hoan_thanh"] = True
            print(f"Đã đánh dấu hoàn thành: {cv['ten']}")
        else:
            print("Số thứ tự không hợp lệ!")
    except ValueError:
        print("Vui lòng nhập số hợp lệ!")

def menu():
    tai_danh_sach()  # Tải khi bắt đầu
    while True:
        print("\n=== QUẢN LÝ CÔNG VIỆC (To-do List) ===")
        print("1. Thêm công việc mới")
        print("2. Xem tất cả công việc")
        print("3. Xem công việc chưa hoàn thành")
        print("4. Đánh dấu hoàn thành")
        print("5. Lưu và thoát")
        lua_chon = input("Chọn chức năng (1-5): ").strip()

        if lua_chon == "1":
            them_cong_viec()
        elif lua_chon == "2":
            danh_sach_cong_viec()
        elif lua_chon == "3":
            danh_sach_cong_viec(chua_hoan_thanh=True)
        elif lua_chon == "4":
            hoan_thanh_cong_viec()
        elif lua_chon == "5":
            luu_danh_sach()
            print("Tạm biệt! Hẹn gặp lại.")
            break
        else:
            print("Lựa chọn không hợp lệ!")

# Chạy chương trình
if __name__ == "__main__":
    menu()
