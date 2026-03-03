import json
from datetime import datetime

class ToDoList:
    """
    Class quản lý danh sách công việc (To-do List).
    Mỗi công việc là một dict với các trường: ten, mo_ta, uu_tien, hoan_thanh, ngay_tao.
    """
    def __init__(self, file_name="todo_list.json"):
        """Khởi tạo danh sách công việc, tự động tải từ file nếu có."""
        self.file_name = file_name
        self.cong_viec = []  # List chứa các dict công việc
        self.tai_danh_sach()  # Tự động tải khi tạo object

    def __len__(self):  
        """Override __len__ để khi gọi len(todo) → trả về số công việc (len(self.cong_viec))"""
        return len(self.cong_viec)
    
    def __str__(self):
        """in ra ToDoList: 5 công việc (2 chưa hoàn thành, 3 đã hoàn thành)"""
        if not self.cong_viec:
            print("ToDoList: Danh sách trống!")
            return
        else:
            ds = self.cong_viec
            ds = [cv for cv in self.cong_viec if not cv["hoan_thanh"]] # ds: danh sách công việc chưa hoàn thành
            return f"ToDoList: {len(self)} công việc ({len(ds)} chưa hoàn thành, {len(self.cong_viec) - len(ds)} đã hoàn thành)"


    
    def tai_danh_sach(self):
        """Đọc danh sách từ file JSON."""
        try:
            with open(self.file_name, "r", encoding="utf-8") as f:
                self.cong_viec = json.load(f)
            print(f"Đã tải {len(self.cong_viec)} công việc từ file.")
        except FileNotFoundError:
            print("Chưa có file lưu → bắt đầu danh sách mới.")
        except Exception as e:
            print(f"Lỗi khi đọc file: {e}")

    def luu_danh_sach(self):
        """Lưu danh sách vào file JSON."""
        try:
            with open(self.file_name, "w", encoding="utf-8") as f:
                json.dump(self.cong_viec, f, ensure_ascii=False, indent=4)
            print("Đã lưu danh sách công việc.")
        except Exception as e:
            print(f"Lỗi khi lưu file: {e}")

    def them_cong_viec(self, ten, mo_ta="", uu_tien=3):
        """Thêm công việc mới."""
        if not ten.strip():
            print("Tên công việc không được để trống!")
            return

        cv = {
            "ten": ten.strip(),
            "mo_ta": mo_ta.strip(),
            "uu_tien": int(uu_tien) if str(uu_tien).isdigit() and 1 <= int(uu_tien) <= 5 else 3,
            "hoan_thanh": False,
            "ngay_tao": datetime.now().strftime("%Y-%m-%d %H:%M")
        }
        self.cong_viec.append(cv)
        print(f"Đã thêm: {ten}")

    def danh_sach_cong_viec(self, chua_hoan_thanh=False):
        """In danh sách công việc (có thể lọc chỉ việc chưa hoàn thành)."""
        if not self.cong_viec:
            print("Danh sách trống!")
            return

        ds = self.cong_viec
        if chua_hoan_thanh:
            ds = [cv for cv in self.cong_viec if not cv["hoan_thanh"]]

        if not ds:
            print("Không có công việc chưa hoàn thành!")
            return

        # Sắp xếp: ưu tiên giảm dần, ngày tạo tăng dần
        ds_sorted = sorted(ds, key=lambda cv: (-cv["uu_tien"], cv["ngay_tao"]))

        trang_thai = {True: "chưa hoàn thành", False: "tất cả"}
        print(f"\nDanh sách công việc ({trang_thai[chua_hoan_thanh]}):")
        for i, cv in enumerate(ds_sorted, 1):
            trang_thai_cv = "✓ Hoàn thành" if cv["hoan_thanh"] else "☐ Chưa làm"
            print(f"{i}. [{trang_thai_cv}] {cv['ten']} (Ưu tiên: {cv['uu_tien']})")
            if cv["mo_ta"]:
                print(f"   Mô tả: {cv['mo_ta']}")
            print(f"   Ngày tạo: {cv['ngay_tao']}\n")

    def hoan_thanh_cong_viec(self, so_thu_tu):
        """Đánh dấu công việc hoàn thành theo số thứ tự (chỉ việc chưa hoàn thành)."""
        chua_hoan_thanh = [cv for cv in self.cong_viec if not cv["hoan_thanh"]]
        if not chua_hoan_thanh:
            print("Không có công việc chưa hoàn thành!")
            return

        if 1 <= so_thu_tu <= len(chua_hoan_thanh):
            cv = chua_hoan_thanh[so_thu_tu - 1]
            cv["hoan_thanh"] = True
            print(f"Đã đánh dấu hoàn thành: {cv['ten']}")
        else:
            print("Số thứ tự không hợp lệ!")

    # xóa công việc không cần làm
    def xoa_cong_viec(self, so_thu_tu):
        """
        Xóa công việc theo số thứ tự (từ toàn bộ danh sách công việc).
        Args:
        so_thu_tu (int): Số thứ tự công việc cần xóa (bắt đầu từ 1).
        """
        if not self.cong_viec:
            print("Danh sách công việc đang trống!")
            return

        if 1 <= so_thu_tu <= len(self.cong_viec):
            # Lấy công việc trước khi xóa
            cv_xoa = self.cong_viec[so_thu_tu - 1]
            ten_xoa = cv_xoa["ten"]
            self.cong_viec.pop(so_thu_tu - 1)
            print(f"Đã xóa công việc: {ten_xoa}")
            print(f"Còn lại {len(self.cong_viec)} công việc.")
        else:
            print("Số thứ tự không hợp lệ!")

    # tìm kiếm công việc (theo tên hoạc mô tả)
    def normalize(self, text):
        """
        Loại bỏ dấu tiếng Việt và chuyển về chữ thường để tìm kiếm không phân biệt dấu/case.
        """
        if not text:
            return ""
        # Bảng thay thế dấu cơ bản (có thể mở rộng nếu cần)
        import unicodedata
        text = unicodedata.normalize('NFD', text)  # Phân tách dấu
        text = ''.join(c for c in text if unicodedata.category(c) != 'Mn')  # Xóa dấu
        return text.lower()

    def tim_cong_viec(self, tu_khoa):
        """
        Tìm công việc theo từ khóa trong tên hoặc mô tả, không phân biệt dấu/case.
        Args:
        tu_khoa (str): Từ khóa cần tìm.
            Returns:
        list: Danh sách công việc khớp từ khóa.
        """
        if not tu_khoa.strip():
            print("Từ khóa không được để trống!")
            return []

        tu_khoa_norm = self.normalize(tu_khoa)
    
        # List comprehension + lambda để lọc
        ket_qua = [
            cv for cv in self.cong_viec
            if tu_khoa_norm in self.normalize(cv["ten"]) 
            or (cv["mo_ta"] and tu_khoa_norm in self.normalize(cv["mo_ta"]))
            ]
    
        if not ket_qua:
            print(f"Không tìm thấy công việc nào chứa '{tu_khoa}'")
        else:
            print(f"\nKết quả tìm kiếm cho '{tu_khoa}' ({len(ket_qua)} công việc):")
            for i, cv in enumerate(ket_qua, 1):
                trang_thai = "✓ Hoàn thành" if cv["hoan_thanh"] else "☐ Chưa làm"
                print(f"{i}. [{trang_thai}] {cv['ten']} (Ưu tiên: {cv['uu_tien']})")
                if cv["mo_ta"]:
                    print(f"   Mô tả: {cv['mo_ta']}")
                print(f"   Ngày tạo: {cv['ngay_tao']}\n")
    
        return ket_qua
            
    def menu(self):
        """Menu tương tác chính."""
        while True:
            print("\n=== QUẢN LÝ CÔNG VIỆC (To-do List) ===")
            print("1. Thêm công việc mới")
            print("2. Xem tất cả công việc")
            print("3. Xem công việc chưa hoàn thành")
            print("4. Đánh dấu hoàn thành")
            print("5. Xóa công việc")
            print("6. Tìm kiếm công việc")
            print("7. Lưu và thoát")
           
            lua_chon = input("Chọn chức năng (1-7): ").strip()

            if lua_chon == "1":
                ten = input("Nhập tên công việc: ").strip()
                mo_ta = input("Mô tả (nếu có): ").strip()
                uu_tien = input("Ưu tiên (1-5, mặc định 3): ").strip()
                self.them_cong_viec(ten, mo_ta, uu_tien)
            elif lua_chon == "2":
                self.danh_sach_cong_viec()
                print(self)
            elif lua_chon == "3":
                self.danh_sach_cong_viec(chua_hoan_thanh=True)
            elif lua_chon == "4":
                self.danh_sach_cong_viec(chua_hoan_thanh=True)
                try:
                    so = int(input("Nhập số thứ tự công việc đã hoàn thành: "))
                    self.hoan_thanh_cong_viec(so)
                except ValueError:
                    print("Vui lòng nhập số hợp lệ!")
            elif lua_chon == "5":
                self.danh_sach_cong_viec()  # In toàn bộ danh sách để người dùng xem số thứ tự
                try:
                    so = int(input("Nhập số thứ tự công việc muốn xóa: "))
                    self.xoa_cong_viec(so)
                except ValueError:
                    print("Vui lòng nhập số hợp lệ!")

            elif lua_chon == "6":
                tu_khoa = input("Nhập từ khóa cần tìm (tên hoặc mô tả): ").strip()
                self.tim_cong_viec(tu_khoa)
                
            elif lua_chon == "7":
                self.luu_danh_sach()
                print("Tạm biệt! Hẹn gặp lại.")
                break

            else:
                print("Lựa chọn không hợp lệ!")

# Chạy chương trình
if __name__ == "__main__":
    todo = ToDoList()  # Tạo instance của class
    todo.menu()
