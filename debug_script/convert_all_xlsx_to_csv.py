import os
import pandas as pd

xlsx_dir = "/media/ntlong/Disk22/CVE_Tools/flask_project/data/tpcn/xlsx"
csv_dir = "/media/ntlong/Disk22/CVE_Tools/flask_project/data/tpcn/csv"

if not os.path.exists(csv_dir):
    os.makedirs(csv_dir)

for filename in os.listdir(xlsx_dir):
    if filename.endswith(".xlsx"):
        xlsx_path = os.path.join(xlsx_dir, filename)
        csv_path = os.path.join(csv_dir, filename.replace(".xlsx", ".csv"))
        try:
            df = pd.read_excel(xlsx_path)
            df.to_csv(csv_path, index=False, encoding="utf-8")
            print(f"Đã chuyển {filename} thành {os.path.basename(csv_path)}")
        except Exception as e:
            print(f"Lỗi với file {filename}: {e}")