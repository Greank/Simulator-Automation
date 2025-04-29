from pathlib import Path

def load_images(folder_name="images"):
    """自動載入指定資料夾內的所有圖片，並回傳相對於專案根目錄的路徑"""
    base_dir = Path(__file__).parent  # 取得當前腳本所在目錄
    picture_dir = base_dir / folder_name  # 設定圖片資料夾路徑

    # 掃描資料夾內所有 PNG 檔案，回傳相對路徑
    image_paths = {file.stem: file.relative_to(base_dir) for file in picture_dir.glob("*.png")}

    return image_paths

# 測試執行
if __name__ == "__main__":
    images = load_images()
    print("載入的圖片：", images)  # 應該顯示相對路徑，例如 'picture/Home.png'
    print(images["01"])
