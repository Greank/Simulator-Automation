import sys
import image_loader
import adb_controller
import time
import screen_capture
from PIL import Image
import cv2

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
        targets, count = screen_capture.match_template_multi(images["61"], screenshot, threshold=0.9)  # 偵測圖案

        if targets :
            print("點擊選單")
            x, y = targets
            adb_controller.tap(device, x + 10, y + 10)  # 點擊目標（稍微偏移中心）
            time.sleep(1)
            while_store = 2

        #畫面核對
        targets, count = screen_capture.match_template_multi(images["62"], screenshot, threshold=0.9)  # 偵測圖案

        if targets and while_store == 2:
            print("點擊資料同步")
            x, y = targets
            adb_controller.tap(device, x + 10, y + 10)  # 點擊目標（稍微偏移中心）
            time.sleep(1)
            while_store = 3

        #畫面核對
        targets, count = screen_capture.match_template_multi(images["63"], screenshot, threshold=0.9)  # 偵測圖案

        if targets and while_store == 3:
            print("點擊同步")
            x, y = targets
            adb_controller.tap(device, x + 10, y + 10)  # 點擊目標（稍微偏移中心）
            time.sleep(1)
            while_store = 4

        #畫面核對
        targets, count = screen_capture.match_template_multi(images["64"], screenshot)  # 偵測圖案

        if targets and while_store == 4:
            print("點擊電子郵件信箱")
            x, y = targets
            adb_controller.tap(device, x + 10, y + 10)  # 點擊目標（稍微偏移中心）
            time.sleep(1)
            while_store = 5
            adb_controller.text(device, account)
            time.sleep(1)

        #畫面核對
        targets, count = screen_capture.match_template_multi(images["65"], screenshot)  # 偵測圖案

        if targets and while_store == 5:
            print("點擊密碼")
            x, y = targets
            adb_controller.tap(device, x + 10, y + 10)  # 點擊目標（稍微偏移中心）
            time.sleep(1)
            while_store = 6
            adb_controller.text(device, password)
            time.sleep(1)
            adb_controller.keyevent(device, "DPAD_DOWN")
            time.sleep(0.5)
            adb_controller.keyevent(device, "DPAD_DOWN")
            time.sleep(0.5)
            adb_controller.keyevent(device, "DPAD_DOWN")
            time.sleep(0.5)
            adb_controller.keyevent(device, "DPAD_DOWN")
            time.sleep(1)

        #畫面核對
        targets, count = screen_capture.match_template_multi(images["66"], screenshot)  # 偵測圖案

        if targets and while_store == 6:
            print("點擊登入")
            x, y = targets
            adb_controller.tap(device, x + 10, y + 10)  # 點擊目標（稍微偏移中心）
            time.sleep(5)
            while_store = 7
            adb_controller.keyevent(device, "DPAD_DOWN")
            time.sleep(0.5)
            adb_controller.keyevent(device, "DPAD_DOWN")
            time.sleep(0.5)
            adb_controller.keyevent(device, "DPAD_DOWN")
            time.sleep(0.5)
            adb_controller.keyevent(device, "DPAD_DOWN")
            time.sleep(0.5)
            adb_controller.keyevent(device, "DPAD_DOWN")
            time.sleep(0.5)
            adb_controller.keyevent(device, "DPAD_DOWN")
            time.sleep(0.5)
            adb_controller.keyevent(device, "DPAD_DOWN")
            time.sleep(0.5)
            adb_controller.keyevent(device, "DPAD_DOWN")
            time.sleep(1)

        #畫面核對
        targets, count = screen_capture.match_template_multi(images["67"], screenshot)  # 偵測圖案

        if targets and while_store == 7:
            print("勾選同意內容")
            x, y = targets
            adb_controller.tap(device, x + 10, y + 10)  # 點擊目標（稍微偏移中心）
            time.sleep(1)
            while_store = 8

        #畫面核對
        targets, count = screen_capture.match_template_multi(images["68"], screenshot)  # 偵測圖案

        if targets and while_store == 8:
            print("點擊同意")
            x, y = targets
            adb_controller.tap(device, x + 10, y + 10)  # 點擊目標（稍微偏移中心）
            time.sleep(1)
            while_store = 9

        #畫面核對
        targets, count = screen_capture.match_template_multi(images["25"], screenshot, threshold=0.9)  # 偵測圖案

        if targets and while_store >= 7:
            screenshot = screen_capture.get_screen(device)  # numpy 陣列格式（OpenCV）
            screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGR2RGB)  # OpenCV 是 BGR，轉成 RGB
            img = Image.fromarray(screenshot)  # 轉成 PIL 圖片物件
            img.save("templates/images/img3.png")  # ✅ 儲存為 PNG
            print("點擊OK")
            x, y = targets
            adb_controller.tap(device, x + 10, y + 10)  # 點擊目標（稍微偏移中心）
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

        if targets and while_store <= 1:
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

    device_id = "emulator-5556"

    # 載入圖片
    images = image_loader.load_images()

    #Adb裝置連結
    device = adb_controller.connect(device_id=device_id)

    account = sys.argv[1]
    password = sys.argv[2]

    print(f"[OK] 成功收到帳號：{account}，密碼：{password}")

    time.sleep(1)

    print("等待帳號綁定中....")

    game_01(device)



# 你可以在這裡做真正的提交、登入、模擬點擊等操作