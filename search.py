import sys
import mariadb
import os
import image_loader
import adb_controller
import screen_capture
import time
from PIL import Image
import cv2

def download_gamedata(db_config, record_id, SAVE_DIR):

    try:
        conn = mariadb.connect(**db_config)
        cursor = conn.cursor()

        cursor.execute("SELECT saved_filename, file_data FROM game_records WHERE id = ?", (record_id,))
        result = cursor.fetchone()

        if result:
            saved_filename, file_data = result
            if not saved_filename:
                saved_filename = "gamedata.tar"

            save_path = os.path.join(SAVE_DIR, saved_filename)

            with open(save_path, "wb") as f:
                f.write(file_data)
            print(f"✅ 已下載並儲存至：{save_path}")
        else:
            print(f"❌ 找不到 ID 為 {record_id} 的資料")

        cursor.close()
        conn.close()

    except Exception as e:
        print(f"❌ 發生錯誤：{e}")

#檔案還原
def restore(device):
    # 要還原的檔案位置
    local_path_restore = "C:/Users/user/Desktop/SD鋼彈/saved/gamedata.tar"
    # 還原
    adb_controller.restore_gamedata(device, local_tar_path=local_path_restore)

#開啟遊戲-資料設定
def game_01(device):

    start_time = time.time()  # ← 在這裡記錄開始時間

    #迴圈綁定
    while_store = 1

    while True:

        #畫面截圖
        screenshot = screen_capture.get_screen(device)

        #畫面核對
        targets, count = screen_capture.match_template_multi(images["08"], screenshot)  # 偵測圖案

        if targets :
            print("點擊S世代 永恆")
            x, y = targets
            adb_controller.tap(device, x + 10, y + 10)  # 點擊目標（稍微偏移中心）
            time.sleep(1)


        #畫面核對
        targets, count = screen_capture.match_template_multi(images["14"], screenshot)  # 偵測圖案

        if targets :
            print("點擊TAP TO START")
            x, y = targets
            adb_controller.tap(device, x + 10, y + 10)  # 點擊目標（稍微偏移中心）
            time.sleep(1)

        #畫面核對
        targets, count = screen_capture.match_template_multi(images["57"], screenshot, threshold=0.9)  # 偵測圖案

        if targets :
            print("點擊強化")
            x, y = targets
            adb_controller.tap(device, x + 10, y + 10)  # 點擊目標（稍微偏移中心）
            time.sleep(5)
            while_store = 2

        #畫面核對
        targets, count = screen_capture.match_template_multi(images["58"], screenshot, threshold=0.9)  # 偵測圖案

        if targets and while_store == 2:
            print("點擊繼續")
            x, y = targets
            adb_controller.tap(device, x + 10, y + 10)  # 點擊目標（稍微偏移中心）
            time.sleep(1)

        #畫面核對
        targets, count = screen_capture.match_template_multi(images["25"], screenshot, threshold=0.9)  # 偵測圖案

        if targets and while_store == 2:
            print("點擊OK")
            x, y = targets
            adb_controller.tap(device, x + 10, y + 10)  # 點擊目標（稍微偏移中心）
            time.sleep(1)

        #畫面核對 -有無再強化頁面
        targets, count = screen_capture.match_template_multi(images["59"], screenshot)  # 偵測圖案

        if targets and while_store == 2:
            screenshot = screen_capture.get_screen(device)  # numpy 陣列格式（OpenCV）
            screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGR2RGB)  # OpenCV 是 BGR，轉成 RGB
            img = Image.fromarray(screenshot)  # 轉成 PIL 圖片物件
            img.save("templates/images/img1.png")  # ✅ 儲存為 PNG
            time.sleep(1)
            while_store = 3

        #畫面核對
        targets, count = screen_capture.match_template_multi(images["60"], screenshot)  # 偵測圖案

        if targets and while_store == 3:
            print("點擊支援人員")
            x, y = targets
            adb_controller.tap(device, x + 10, y + 10)  # 點擊目標（稍微偏移中心）
            time.sleep(1)
            screenshot = screen_capture.get_screen(device)  # numpy 陣列格式（OpenCV）
            screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGR2RGB)  # OpenCV 是 BGR，轉成 RGB
            img = Image.fromarray(screenshot)  # 轉成 PIL 圖片物件
            img.save("templates/images/img2.png")  # ✅ 儲存為 PNG
            time.sleep(1)
            end_02(device)
            break


        #畫面核對-沒有順序述
        targets, count = screen_capture.match_template_multi(images["36"], screenshot, threshold=0.9)  # 偵測圖案

        if targets:
            print("點擊略過")
            x, y = targets
            adb_controller.tap(device, x + 10, y + 10)  # 點擊目標（稍微偏移中心）
            time.sleep(1)
            adb_controller.tap(device, x + 10, y + 10)  # 點擊目標（稍微偏移中心）
            time.sleep(1)

        #畫面核對-沒有順序述
        targets, count = screen_capture.match_template_multi(images["27"], screenshot, threshold=0.9)  # 偵測圖案

        if targets:
            print("點擊關閉")
            x, y = targets
            adb_controller.tap(device, x + 10, y + 10)  # 點擊目標（稍微偏移中心）
            time.sleep(2)

        time.sleep(0.5)

        # --- 這裡檢查是否已經超過 5 分鐘（300秒） ---
        elapsed = time.time() - start_time
        # print(f"編號:{device} 運行經過時間:{elapsed}秒")
        if elapsed > 400:
            # print(f"⚠️ [{device}] 跑超過 5 分鐘，自動執行 end_03() 重啟模擬器")
            end_03(device)
            start_time = time.time()  # ✅ 重設開始時間（讓它繼續計下一輪） 

def end_02(device):

    adb_controller.keyevent(device, "APP_SWITCH")

    #迴圈綁定
    while_store = 0

    while True:
        
        #畫面截圖
        screenshot = screen_capture.get_screen(device)

        #畫面核對-沒有順序述
        targets, count = screen_capture.match_template_multi(images["46"], screenshot)  # 偵測圖案

        if targets and while_store == 0 :
            print("點擊全部清除")
            x, y = targets
            adb_controller.tap(device, x + 10, y + 10)  # 點擊目標（稍微偏移中心）
            time.sleep(1)
            while_store = 1
            break

def end_03(device):

    adb_controller.keyevent(device, "APP_SWITCH")

    #迴圈綁定
    while_store = 0

    while True:
        
        #畫面截圖
        screenshot = screen_capture.get_screen(device)

        #畫面核對-沒有順序述
        targets, count = screen_capture.match_template_multi(images["46"], screenshot)  # 偵測圖案

        if targets and while_store == 0 :
            print("點擊全部清除")
            x, y = targets
            adb_controller.tap(device, x + 10, y + 10)  # 點擊目標（稍微偏移中心）
            time.sleep(1)
            while_store = 1
            game_01(device)


if __name__ == "__main__":

    # ✅ 固定儲存資料夾（你可以修改）
    SAVE_DIR = "C:/Users/user/Desktop/SD鋼彈/saved"

    # 資料庫設定
    db_config = {
        "host": "localhost",
        "port": 3306,
        "user": "root",
        "password": "sad69412",
        "database": "game_db"
    }

    # ✅ 取得傳入的 record_id
    if len(sys.argv) < 2:
        print("❗請輸入 record_id，例如：python search.py 12")
        sys.exit(1)

    record_id = sys.argv[1]

    # 確保儲存路徑存在
    os.makedirs(SAVE_DIR, exist_ok=True)

    download_gamedata(db_config, record_id, SAVE_DIR)

    device_id = "emulator-5556"

    # 載入圖片
    images = image_loader.load_images()

    #Adb裝置連結
    device = adb_controller.connect(device_id=device_id)

    restore(device)

    game_01(device)



# img = Image.new("RGB", (300, 200), color="lightblue")
# draw = ImageDraw.Draw(img)
# draw.text((10, 90), f"ID: {id}", fill="black")
# img.save("templates/images/img1.png")
# img.save("templates/images/img2.png")
