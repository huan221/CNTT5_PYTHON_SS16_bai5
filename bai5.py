er_patients = [
    "ER01|Nguyen Van Quan|HR:115|TEMP:39.5",
    "ER02|Tran Thi Binh|HR:80|TEMP:37.0",
    "ER03|Le Van Cuong|HR:130|TEMP:38.2"
]

def find_patient_index(patients, er_id):
    for i in range(len(patients)):
        if patients[i].startswith(er_id + "|"):
            return i
    return -1


def extract_vital_value(vital_string):
    try:
        return float(vital_string.split(":")[1])
    except:
        return None

def display_dashboard(patients):
    if not patients:
        print("Khoa cấp cứu hiện đang trống.")
        return

    print("--- BẢNG THEO DÕI CA CẤP CỨU ------------------------------------")

    for i, p in enumerate(patients, 1):
        parts = p.split("|")
        er_id = parts[0]
        name = parts[1]
        hr = extract_vital_value(parts[2])
        temp = extract_vital_value(parts[3])

        print(f"{i}. [{er_id}] {name:<20} | Nhịp tim: {int(hr)} bpm | Nhiệt độ: {temp} °C")

    print("-----------------------------------------------------------------")

def admit_patient(patients):
    print("\n--- TIẾP NHẬN CA CẤP CỨU MỚI ---")

    er_id = input("Nhập mã ER: ").strip().upper()
    if not er_id:
        print("Mã ER không được để trống!")
        return

    if find_patient_index(patients, er_id) != -1:
        print("Mã ca cấp cứu đã tồn tại!")
        return

    name = input("Nhập tên bệnh nhân: ").strip().title()
    if not name:
        print("Tên bệnh nhân không được để trống!")
        return

    # nhập HR
    while True:
        hr_input = input("Nhập nhịp tim HR: ").strip()
        if hr_input.replace(".", "").isdigit():
            hr = float(hr_input)
            if hr > 0:
                break
        print("Sinh hiệu không hợp lệ, vui lòng nhập số lớn hơn 0!")

    # nhập TEMP
    while True:
        temp_input = input("Nhập nhiệt độ TEMP: ").strip()
        if temp_input.replace(".", "").isdigit():
            temp = float(temp_input)
            if temp >= 36.5:
                break
        print("Sinh hiệu không hợp lệ, vui lòng nhập số lớn hơn hoặc bằng 36.5!")

    new_patient = f"{er_id}|{name}|HR:{int(hr)}|TEMP:{temp}"
    patients.append(new_patient)

    print("\nTiếp nhận ca cấp cứu mới thành công!")
    print("Dữ liệu:", new_patient)

def update_vitals(patients):
    print("\n--- CẬP NHẬT LẠI SINH HIỆU ---")

    er_id = input("Nhập mã ER cần cập nhật: ").strip().upper()
    index = find_patient_index(patients, er_id)

    if index == -1:
        print("Không tìm thấy bệnh nhân. Vui lòng kiểm tra lại mã ER!")
        return

    parts = patients[index].split("|")
    print(f"Tìm thấy bệnh nhân: {parts[1]}")
    print(f"Sinh hiệu hiện tại: {parts[2]} | {parts[3]}")

    print("1. Nhịp tim HR")
    print("2. Nhiệt độ TEMP")
    choice = input("Chọn loại sinh hiệu: ")

    if choice not in ["1", "2"]:
        print("Lựa chọn không hợp lệ. Vui lòng chọn 1 hoặc 2!")
        return

    while True:
        value_input = input("Nhập giá trị mới: ").strip()
        if value_input.replace(".", "").isdigit():
            value = float(value_input)
            if value > 0:
                break
        print("Sinh hiệu không hợp lệ, vui lòng nhập số lớn hơn 0!")

    if choice == "1":
        parts[2] = f"HR:{int(value)}"
        print("Cập nhật nhịp tim thành công!")
    else:
        parts[3] = f"TEMP:{value}"
        print("Cập nhật nhiệt độ thành công!")

    patients[index] = "|".join(parts)

def trigger_red_alert(patients):
    if not patients:
        print("Khoa cấp cứu hiện đang trống.")
        return

    critical = []

    for p in patients:
        parts = p.split("|")
        hr = extract_vital_value(parts[2])
        temp = extract_vital_value(parts[3])

        if hr > 100 or temp >= 39.0:
            critical.append(parts)

    if not critical:
        print("--- KIỂM TRA BÁO ĐỘNG ĐỎ ---")
        print("Không có bệnh nhân nguy kịch tại thời điểm hiện tại.")
        return

    print("\n!!! BÁO ĐỘNG ĐỎ - DANH SÁCH BỆNH NHÂN NGUY KỊCH !!!")

    for i, p in enumerate(critical, 1):
        print(f"{i}. [{p[0]}] {p[1]} | HR: {p[2].split(':')[1]} bpm | TEMP: {p[3].split(':')[1]} °C | CẦN XỬ LÝ KHẨN CẤP")

    print("-----------------------------------------------------")
    print(f"Tổng số ca nguy kịch: {len(critical)}")

def discharge_patient(patients):
    print("\n--- XUẤT VIỆN / CHUYỂN KHOA ---")

    er_id = input("Nhập mã ER cần xóa khỏi hệ thống: ").strip().upper()
    if not er_id:
        print("Mã ER không được để trống!")
        return

    index = find_patient_index(patients, er_id)

    if index == -1:
        print("Không tìm thấy bệnh nhân. Vui lòng kiểm tra lại mã ER!")
        return

    name = patients[index].split("|")[1]
    patients.pop(index)

    print(f"Đã chuyển khoa thành công cho bệnh nhân {name}!")

def main():
    while True:
        print("\n===== HỆ THỐNG QUẢN LÝ CẤP CỨU RIKKEI ER =====")
        print("1. Bảng theo dõi bệnh nhân")
        print("2. Tiếp nhận ca cấp cứu mới")
        print("3. Cập nhật lại sinh hiệu")
        print("4. BÁO ĐỘNG ĐỎ")
        print("5. Xuất viện / Chuyển khoa")
        print("6. Thoát chương trình")
        print("=================================================")

        choice = input("Chọn chức năng (1-6): ")

        if choice == "1":
            display_dashboard(er_patients)
        elif choice == "2":
            admit_patient(er_patients)
        elif choice == "3":
            update_vitals(er_patients)
        elif choice == "4":
            trigger_red_alert(er_patients)
        elif choice == "5":
            discharge_patient(er_patients)
        elif choice == "6":
            print("Kết thúc ca trực. Tạm biệt!")
            break
        else:
            print("Lựa chọn không hợp lệ!")


main()