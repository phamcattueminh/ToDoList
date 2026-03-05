import json
from datetime import datetime

class CongViec:
    """Class cơ bản đại diện cho một công việc."""
    def __init__(self, ten, mo_ta=""):
        self.ten = ten.strip()
        self.mo_ta = mo_ta.strip()
        self.hoan_thanh = False
        self.ngay_tao = datetime.now().strftime("%Y-%m-%d %H:%M")

    def danh_dau_hoan_thanh(self):
        """Đánh dấu công việc hoàn thành."""
        self.hoan_thanh = True
        print(f"Đã hoàn thành: {self.ten}")

    def __str__(self):
        trang_thai = "✓ Hoàn thành" if self.hoan_thanh else "☐ Chưa làm"
        return f"[{trang_thai}] {self.ten}\n   Ngày tạo: {self.ngay_tao}"

    def to_dict(self):
        """Chuyển object thành dict để lưu JSON."""
        return {
            "loai": "CongViec",
            "ten": self.ten,
            "mo_ta": self.mo_ta,
            "hoan_thanh": self.hoan_thanh,
            "ngay_tao": self.ngay_tao
        }


class CongViecUuTien(CongViec):
    """Công việc có ưu tiên (kế thừa từ CongViec)."""
    def __init__(self, ten, uu_tien=3, mo_ta=""):
        super().__init__(ten, mo_ta)
        self.uu_tien = max(1, min(5, int(uu_tien)))  # Giới hạn 1-5

    def __str__(self):
        return f"{super().__str__()}\n   Ưu tiên: {self.uu_tien}"

    def to_dict(self):
        data = super().to_dict()
        data["loai"] = "CongViecUuTien"
        data["uu_tien"] = self.uu_tien
        return data


class CongViecCoDeadline(CongViec):
    """Công việc có hạn chót (kế thừa từ CongViec)."""
    def __init__(self, ten, deadline, mo_ta=""):
        super().__init__(ten, mo_ta)
        self.deadline = deadline.strip()  # Format: YYYY-MM-DD

    def kiem_tra_qua_han(self):
        """Kiểm tra xem công việc đã quá hạn chưa."""
        if self.hoan_thanh:
            return False
        try:
            ngay_deadline = datetime.strptime(self.deadline, "%Y-%m-%d")
            return datetime.now() > ngay_deadline
        except ValueError:
            return False

    def __str__(self):
        qua_han = " (QUÁ HẠN!)" if self.kiem_tra_qua_han() else ""
        return f"{super().__str__()}\n   Hạn chót: {self.deadline}{qua_han}"

    def to_dict(self):
        data = super().to_dict()
        data["loai"] = "CongViecCoDeadline"
        data["deadline"] = self.deadline
        return data


class ToDoList:
    """Class quản lý danh sách các công việc (dùng các object CongViec)."""
    def __init__(self, file_name="todo_list.json"):
        self.file_name = file_name
        self.cong_viec = []  # List chứa các object CongViec (hoặc con)
        self.tai_danh_sach()

    def tai_danh_sach(self):
        """Đọc từ file JSON và chuyển thành object."""
        try:
            with open(self.file_name, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.cong_viec = []
            for item in data:
                loai = item.get("loai", "CongViec")
                if loai == "CongViecUuTien":
                    cv = CongViecUuTien(item["ten"], item.get("uu_tien", 3), item.get("mo_ta", ""))
                elif loai == "CongViecCoDeadline":
                    cv = CongViecCoDeadline(item["ten"], item["deadline"], item.get("mo_ta", ""))
                else:
                    cv = CongViec(item["ten"], item.get("mo_ta", ""))
                cv.hoan_thanh = item["hoan_thanh"]
                cv.ngay_tao = item["ngay_tao"]
                self.cong_viec.append(cv)
            print(f"Đã tải {len(self.cong_viec)} công việc từ file.")
        except FileNotFoundError:
            print("Chưa có file → bắt đầu mới.")
        except Exception as e:
            print(f"Lỗi đọc file: {e}")

    def luu_danh_sach(self):
        """Lưu tất cả công việc dưới dạng JSON."""
        data = [cv.to_dict() for cv in self.cong_viec]
        try:
            with open(self.file_name, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            print("Đã lưu danh sách.")
        except Exception as e:
            print(f"Lỗi lưu file: {e}")

    def them_cong_viec(self, ten, loai="thuong", **kwargs):
        """Thêm công việc với loại (thuong, uu_tien, co_deadline)."""
        if not ten.strip():
            print("Tên không được để trống!")
            return

        if loai == "uu_tien":
            cv = CongViecUuTien(ten, **kwargs)
        elif loai == "co_deadline":
            cv = CongViecCoDeadline(ten, **kwargs)
        else:
            cv = CongViec(ten, **kwargs)

        self.cong_viec.append(cv)
        print(f"Đã thêm: {ten}")

    def danh_sach_cong_viec(self):
        """In tất cả công việc."""
        if not self.cong_viec:
            print("Danh sách trống!")
            return

        print("\nDanh sách công việc:")
        for i, cv in enumerate(self.cong_viec, 1):
            print(f"{i}. {cv}")

    def menu(self):
        while True:
            print("\n=== QUẢN LÝ CÔNG VIỆC (OOP) ===")
            print("1. Thêm công việc thường")
            print("2. Thêm công việc ưu tiên")
            print("3. Thêm công việc có deadline")
            print("4. Xem danh sách")
            print("5. Lưu và thoát")
            chon = input("Chọn (1-5): ").strip()

            if chon == "1":
                ten = input("Tên: ")
                mo_ta = input("Mô tả: ")
                self.them_cong_viec(ten, mo_ta=mo_ta)
            elif chon == "2":
                ten = input("Tên: ")
                uu_tien = input("Ưu tiên (1-5): ")
                self.them_cong_viec(ten, loai="uu_tien", uu_tien=uu_tien)
            elif chon == "3":
                ten = input("Tên: ")
                deadline = input("Deadline (YYYY-MM-DD): ")
                self.them_cong_viec(ten, loai="co_deadline", deadline=deadline)
            elif chon == "4":
                self.danh_sach_cong_viec()
            elif chon == "5":
                self.luu_danh_sach()
                break

if __name__ == "__main__":
    todo = ToDoList()
    todo.menu()
