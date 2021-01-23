import shutil
import urllib.request
import zipfile
from io import BytesIO

BASE_DIR = "https://msedgedriver.azureedge.net"


def get_and_install_driver(num):
    url = f"{BASE_DIR}/{num}/edgedriver_win64.zip"
    target = f"drivers/{num}.exe"
    with urllib.request.urlopen(url) as f:
        z = zipfile.ZipFile(BytesIO(f.read()))
        driver = z.open("msedgedriver.exe")
        with open(target, "wb") as out:
            shutil.copyfileobj(driver, out)


if __name__ == "__main__":
    numbers = [
        "89.0.749.0",
        "89.0.744.0",
        "89.0.743.0",
        "88.0.705.29",
        "88.0.705.22",
        "88.0.705.18",
        "87.0.669.0",
        "87.0.666.0",
        "87.0.664.66",
    ]
    for number in numbers:
        get_and_install_driver(number)
