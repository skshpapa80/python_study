from datetime import datetime

date_string = "2025:01:17 10:39:10"

dt = datetime.strptime(
    date_string,
    "%Y:%m:%d %H:%M:%S"
)

folder_name = dt.strftime("%Y-%m-%d")

print(folder_name)