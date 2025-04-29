import adb_controller
import screen_capture
import image_loader
import time
import write_excel
import simulator
import threading
from pathlib import Path
import db_controller

class BotContext:
    def __init__(self, device, images, serial_number, id, index):
        self.device = device
        self.images = images
        self.serial_number = serial_number
        self.number_of_runs = 0
        self.id = id
        self.index = index
        self.host_name = "PC-1"

#覆蓋使用者資料
def user(ctx):

    start_time = time.time()  # ← 在這裡記錄開始時間

    #迴圈綁定
    while_store = 1

    while True:

        #畫面截圖
        screenshot = screen_capture.get_screen(ctx.device)

        #畫面核對
        targets, count = screen_capture.match_template_multi(ctx.images["01"], screenshot)  # 偵測圖案

        if targets :
            print("點擊檔案總管")
            x, y = targets
            adb_controller.tap(ctx.device, x + 10, y + 10)  # 點擊目標（稍微偏移中心）
            time.sleep(1)
            while_store = 1
        
        #畫面核對
        targets, count = screen_capture.match_template_multi(ctx.images["02"], screenshot, threshold=0.99)  # 偵測圖案

        if targets and while_store == 1:
            print("點擊0檔案夾")
            x, y = targets
            adb_controller.tap(ctx.device, x + 10, y + 10)  # 點擊目標（稍微偏移中心）
            while_store = 2
            time.sleep(1)

        #畫面核對
        targets, count = screen_capture.match_template_multi(ctx.images["03"], screenshot)  # 偵測圖案

        if targets and while_store == 2:
            print("點擊選單")
            x, y = targets
            adb_controller.tap(ctx.device, x + 10, y + 10)  # 點擊目標（稍微偏移中心）
            while_store = 3
            time.sleep(1)

        #畫面核對
        targets, count = screen_capture.match_template_multi(ctx.images["04"], screenshot)  # 偵測圖案

        if targets and while_store == 3:
            print("點擊全選")
            x, y = targets
            adb_controller.tap(ctx.device, x + 10, y + 10)  # 點擊目標（稍微偏移中心）
            while_store = 4
            time.sleep(1)

        #畫面核對
        targets, count = screen_capture.match_template_multi(ctx.images["05"], screenshot)  # 偵測圖案

        if targets and while_store == 4:
            print("點擊上層目錄")
            x, y = targets
            adb_controller.tap(ctx.device, x + 10, y + 10)  # 點擊目標（稍微偏移中心）
            while_store = 5
            time.sleep(1)
        
        #畫面核對
        targets, count = screen_capture.match_template_multi(ctx.images["06"], screenshot)  # 偵測圖案

        if targets and while_store == 5:
            print("點擊選單")
            x, y = targets
            adb_controller.tap(ctx.device, x + 10, y + 10)  # 點擊目標（稍微偏移中心）
            while_store = 6
            time.sleep(1)

        #畫面核對
        targets, count = screen_capture.match_template_multi(ctx.images["07"], screenshot)  # 偵測圖案

        if targets and while_store == 6:
            print("點擊貼上選取的項目")
            x, y = targets
            adb_controller.tap(ctx.device, x + 10, y + 10)  # 點擊目標（稍微偏移中心）
            while_store = 7
            time.sleep(1)

        #畫面核對
        targets, count = screen_capture.match_template_multi(ctx.images["07_01"], screenshot, threshold=0.95)  # 偵測圖案

        if targets and while_store == 7:
            print("點擊覆蓋")
            x, y = targets
            adb_controller.tap(ctx.device, x + 10, y + 10)  # 點擊目標（稍微偏移中心）
            while_store = 8

            time.sleep(1)

            print("點擊HOME")
            adb_controller.keyevent(ctx.device, "HOME")

            game_01(ctx)
            

        time.sleep(0.5)

        # --- 這裡檢查是否已經超過 5 分鐘（200秒） ---
        elapsed = time.time() - start_time
        print(f"編號:{ctx.id} 運行經過時間:{elapsed}秒")
        if elapsed > 200:
            print(f"⚠️ [{ctx.id}] 跑超過 5 分鐘，自動執行 end_03() 重啟模擬器")
            end_03(ctx)
            start_time = time.time()  # ✅ 重設開始時間（讓它繼續計下一輪）

#開啟遊戲-資料設定
def game_01(ctx):

    start_time = time.time()  # ← 在這裡記錄開始時間

    #迴圈綁定
    while_store = 1

    while True:

        #畫面截圖
        screenshot = screen_capture.get_screen(ctx.device)

        #畫面核對
        targets, count = screen_capture.match_template_multi(ctx.images["08"], screenshot)  # 偵測圖案

        if targets :
            print("點擊S世代 永恆")
            x, y = targets
            adb_controller.tap(ctx.device, x + 10, y + 10)  # 點擊目標（稍微偏移中心）
            time.sleep(1)
            while_store = 1

        #畫面核對
        targets, count = screen_capture.match_template_multi(ctx.images["09"], screenshot)  # 偵測圖案

        if targets and while_store == 1:
            print("點擊選單")
            x, y = targets
            adb_controller.tap(ctx.device, x + 10, y + 10)  # 點擊目標（稍微偏移中心）
            while_store = 2
            time.sleep(1)

        #畫面核對
        targets, count = screen_capture.match_template_multi(ctx.images["10"], screenshot)  # 偵測圖案

        if targets and while_store == 2:
            print("點擊刪除使用者資料")
            x, y = targets
            adb_controller.tap(ctx.device, x + 10, y + 10)  # 點擊目標（稍微偏移中心）
            while_store = 3
            time.sleep(1)

        #畫面核對
        targets, count = screen_capture.match_template_multi(ctx.images["11"], screenshot)  # 偵測圖案

        if targets and while_store == 3:
            print("點擊打勾")
            x, y = targets
            adb_controller.tap(ctx.device, x + 10, y + 10)  # 點擊目標（稍微偏移中心）
            while_store = 4
            time.sleep(1)

        #畫面核對
        targets, count = screen_capture.match_template_multi(ctx.images["12"], screenshot)  # 偵測圖案

        if targets and while_store == 4:
            print("點擊刪除")
            x, y = targets
            adb_controller.tap(ctx.device, x + 10, y + 10)  # 點擊目標（稍微偏移中心）
            while_store = 5
            time.sleep(1)

        #畫面核對
        targets, count = screen_capture.match_template_multi(ctx.images["13"], screenshot)  # 偵測圖案

        if targets and while_store == 5:
            print("點擊關閉")
            x, y = targets
            adb_controller.tap(ctx.device, x + 10, y + 10)  # 點擊目標（稍微偏移中心）
            while_store = 6
            time.sleep(1)

        #畫面核對
        targets, count = screen_capture.match_template_multi(ctx.images["14"], screenshot)  # 偵測圖案

        if targets and while_store == 6:
            print("點擊TAP TO START")
            x, y = targets
            adb_controller.tap(ctx.device, x + 10, y + 10)  # 點擊目標（稍微偏移中心）
            while_store = 7
            time.sleep(1)

        #畫面核對
        targets, count = screen_capture.match_template_multi(ctx.images["15"], screenshot, threshold=0.95)  # 偵測圖案

        if targets and while_store == 7:
            print("點擊同意")
            x, y = targets
            adb_controller.tap(ctx.device, x + 10, y + 10)  # 點擊目標（稍微偏移中心）
            while_store = 8
            time.sleep(1)

        #畫面核對
        targets, count = screen_capture.match_template_multi(ctx.images["16"], screenshot, threshold=0.95)  # 偵測圖案

        if targets and while_store == 8:
            print("點擊全部接受")
            x, y = targets
            adb_controller.tap(ctx.device, x + 10, y + 10)  # 點擊目標（稍微偏移中心）
            while_store = 9
            time.sleep(1)

        #畫面核對
        targets, count = screen_capture.match_template_multi(ctx.images["17"], screenshot, threshold=0.95)  # 偵測圖案

        if targets and while_store == 9:
            print("點擊略過")
            x, y = targets
            adb_controller.tap(ctx.device, x + 10, y + 10)  # 點擊目標（稍微偏移中心）
            while_store = 10
            time.sleep(1)

        #畫面核對
        targets, count = screen_capture.match_template_multi(ctx.images["18"], screenshot, threshold=0.95)  # 偵測圖案

        if targets and while_store == 10:
            print("點擊輸入玩家名稱")
            x, y = targets
            adb_controller.tap(ctx.device, x + 10, y + 10)  # 點擊目標（稍微偏移中心）
            while_store = 11
            time.sleep(1)
            adb_controller.text(ctx.device, "Master")
            time.sleep(1)

        #畫面核對
        targets, count = screen_capture.match_template_multi(ctx.images["19"], screenshot)  # 偵測圖案

        if targets and while_store == 11:
            print("點擊執行")
            x, y = targets
            adb_controller.tap(ctx.device, x + 10, y + 10)  # 點擊目標（稍微偏移中心）
            while_store = 12
            time.sleep(1)

        #畫面核對
        targets, count = screen_capture.match_template_multi(ctx.images["20"], screenshot)  # 偵測圖案

        if targets and while_store == 12:
            print("點擊是")
            x, y = targets
            adb_controller.tap(ctx.device, x + 10, y + 10)  # 點擊目標（稍微偏移中心）
            while_store = 13
            time.sleep(1)
            game_02(ctx)

        #畫面核對
        targets, count = screen_capture.match_template_multi(ctx.images["56"], screenshot)  # 偵測圖案

        if targets :
            print("出現連線忙碌中，回到初始刷取")
            end_02(ctx)

        time.sleep(0.5)

        # --- 這裡檢查是否已經超過 5 分鐘（200秒） ---
        elapsed = time.time() - start_time
        print(f"編號:{ctx.id} 運行經過時間:{elapsed}秒")
        if elapsed > 200:
            print(f"⚠️ [{ctx.id}] 跑超過 5 分鐘，自動執行 end_03() 重啟模擬器")
            end_03(ctx)
            start_time = time.time()  # ✅ 重設開始時間（讓它繼續計下一輪）

#開啟遊戲-新手教學完成
def game_02(ctx):

    start_time = time.time()  # ← 在這裡記錄開始時間

    #迴圈綁定
    while_store = 0

    while True:
        
        #畫面截圖
        screenshot = screen_capture.get_screen(ctx.device)

        #畫面核對
        targets, count = screen_capture.match_template_multi(ctx.images["21"], screenshot)  # 偵測圖案

        if targets and while_store == 0:
            print("點擊略過")
            x, y = targets
            adb_controller.tap(ctx.device, x + 10, y + 10)  # 點擊目標（稍微偏移中心）
            while_store = 1
            time.sleep(1)
            adb_controller.tap(ctx.device, x + 10, y + 10)  # 點擊目標（稍微偏移中心）
            time.sleep(1)

        #畫面核對
        targets, count = screen_capture.match_template_multi(ctx.images["22"], screenshot)  # 偵測圖案

        if targets and while_store == 1:
            print("點擊略過")
            x, y = targets
            adb_controller.tap(ctx.device, x + 10, y + 10)  # 點擊目標（稍微偏移中心）
            while_store = 2
            time.sleep(1)
            adb_controller.tap(ctx.device, x + 10, y + 10)  # 點擊目標（稍微偏移中心）
            time.sleep(1)

        #畫面核對
        targets, count = screen_capture.match_template_multi(ctx.images["23"], screenshot)  # 偵測圖案

        if targets and while_store == 2:
            print("點擊關閉")
            x, y = targets
            adb_controller.tap(ctx.device, x + 10, y + 10)  # 點擊目標（稍微偏移中心）
            while_store = 3
            time.sleep(1)

        #畫面核對
        targets, count = screen_capture.match_template_multi(ctx.images["24"], screenshot)  # 偵測圖案

        if targets and while_store == 3:
            print("點擊初學者使命")
            x, y = targets
            adb_controller.tap(ctx.device, x + 10, y + 10)  # 點擊目標（稍微偏移中心）
            while_store = 4
            time.sleep(1)
            adb_controller.tap(ctx.device, x + 10, y + 10)  # 點擊目標（稍微偏移中心）
            time.sleep(1)
            adb_controller.tap(ctx.device, x + 10, y + 10)  # 點擊目標（稍微偏移中心）
            time.sleep(1)
            adb_controller.tap(ctx.device, x + 10, y + 10)  # 點擊目標（稍微偏移中心）
            time.sleep(1)
            adb_controller.tap(ctx.device, x + 10, y + 10)  # 點擊目標（稍微偏移中心）
            time.sleep(1)
            adb_controller.tap(ctx.device, x + 10, y + 10)  # 點擊目標（稍微偏移中心）
            time.sleep(1)
            adb_controller.tap(ctx.device, x + 10, y + 10)  # 點擊目標（稍微偏移中心）
            time.sleep(1)
            

        #畫面核對
        targets, count = screen_capture.match_template_multi(ctx.images["25"], screenshot)  # 偵測圖案

        if targets and while_store == 4:
            print("點擊OK")
            x, y = targets
            adb_controller.tap(ctx.device, x + 10, y + 10)  # 點擊目標（稍微偏移中心）
            while_store = 5
            time.sleep(1)

        #畫面核對
        targets, count = screen_capture.match_template_multi(ctx.images["28"], screenshot)  # 偵測圖案

        if targets and while_store == 5:
            print("點擊禮物")
            x, y = targets
            adb_controller.tap(ctx.device, x + 10, y + 10)  # 點擊目標（稍微偏移中心）
            while_store = 6
            time.sleep(1)

        #畫面核對
        targets, count = screen_capture.match_template_multi(ctx.images["29"], screenshot)  # 偵測圖案

        if targets and while_store == 6:
            print("點擊全部領取")
            x, y = targets
            adb_controller.tap(ctx.device, x + 10, y + 10)  # 點擊目標（稍微偏移中心）
            while_store = 7
            time.sleep(5)
            adb_controller.tap(ctx.device, x + 10, y + 10)  # 點擊目標（稍微偏移中心
            time.sleep(1)

        #畫面核對
        targets, count = screen_capture.match_template_multi(ctx.images["30"], screenshot)  # 偵測圖案

        if targets and while_store == 7:
            print("點擊OK")
            x, y = targets
            adb_controller.tap(ctx.device, x + 10, y + 10)  # 點擊目標（稍微偏移中心）
            while_store = 8
            time.sleep(1)
        
        #畫面核對
        targets, count = screen_capture.match_template_multi(ctx.images["32"], screenshot)  # 偵測圖案

        if targets and while_store == 8:
            print("點擊機體補給")
            x, y = targets
            adb_controller.tap(ctx.device, x + 10, y + 10)  # 點擊目標（稍微偏移中心）
            while_store = 9
            time.sleep(1)
            game_03(ctx)


        #畫面核對-沒有順序述
        targets, count = screen_capture.match_template_multi(ctx.images["27"], screenshot, threshold=0.9)  # 偵測圖案

        if targets:
            print("點擊關閉")
            x, y = targets
            adb_controller.tap(ctx.device, x + 10, y + 10)  # 點擊目標（稍微偏移中心）
            time.sleep(2)

        #畫面核對
        targets, count = screen_capture.match_template_multi(ctx.images["56"], screenshot)  # 偵測圖案

        if targets :
            print("出現連線忙碌中，回到初始刷取")
            end_02(ctx)
        
        time.sleep(0.5)

        # --- 這裡檢查是否已經超過 5 分鐘（200秒） ---
        elapsed = time.time() - start_time
        print(f"編號:{ctx.id} 運行經過時間:{elapsed}秒")
        if elapsed > 200:
            print(f"⚠️ [{ctx.id}] 跑超過 5 分鐘，自動執行 end_03() 重啟模擬器")
            end_03(ctx)
            start_time = time.time()  # ✅ 重設開始時間（讓它繼續計下一輪）

#開啟遊戲-進入抽取
def game_03(ctx):

    start_time = time.time()  # ← 在這裡記錄開始時間

    #迴圈綁定
    while_store = 0

    while True:
        
        #畫面截圖
        screenshot = screen_capture.get_screen(ctx.device)

        #畫面核對
        targets, count = screen_capture.match_template_multi(ctx.images["33"], screenshot)  # 偵測圖案

        if targets and while_store == 0:
            print("點擊高級機體補給")
            x, y = targets
            adb_controller.tap(ctx.device, x + 10, y + 10)  # 點擊目標（稍微偏移中心）
            while_store = 1
            time.sleep(1)

        #畫面核對
        targets, count = screen_capture.match_template_multi(ctx.images["34"], screenshot)  # 偵測圖案

        if targets and while_store == 1:
            print("點擊補給10次")
            x, y = targets
            adb_controller.tap(ctx.device, x + 10, y + 10)  # 點擊目標（稍微偏移中心）
            while_store = 2
            time.sleep(1)

        #畫面核對
        targets, count = screen_capture.match_template_multi(ctx.images["35"], screenshot, threshold=0.9)  # 偵測圖案

        if targets and while_store == 2:
            print("點擊機體補給")
            x, y = targets
            adb_controller.tap(ctx.device, x + 10, y + 10)  # 點擊目標（稍微偏移中心）
            while_store = 3
            time.sleep(1)
            game_04(ctx)

        #畫面核對
        targets, count = screen_capture.match_template_multi(ctx.images["56"], screenshot)  # 偵測圖案

        if targets :
            print("出現連線忙碌中，回到初始刷取")
            end_02(ctx)

        time.sleep(0.5)

        # --- 這裡檢查是否已經超過 5 分鐘（200秒） ---
        elapsed = time.time() - start_time
        print(f"編號:{ctx.id} 運行經過時間:{elapsed}秒")
        if elapsed > 200:
            print(f"⚠️ [{ctx.id}] 跑超過 5 分鐘，自動執行 end_03() 重啟模擬器")
            end_03(ctx)
            start_time = time.time()  # ✅ 重設開始時間（讓它繼續計下一輪）

#開啟遊戲-刷10連抽並記錄
def game_04(ctx):

    start_time = time.time()  # ← 在這裡記錄開始時間

    #迴圈綁定
    while_store = 0

    while_01 = 2

    results = {} 

    while True:
        
        #畫面截圖
        screenshot = screen_capture.get_screen(ctx.device)

        #畫面核對-沒有順序述
        targets, count = screen_capture.match_template_multi(ctx.images["36"], screenshot, threshold=0.9)  # 偵測圖案

        if targets:
            print("點擊略過")
            x, y = targets
            adb_controller.tap(ctx.device, x + 10, y + 10)  # 點擊目標（稍微偏移中心）
            time.sleep(1)
            while_01 += 0.5

        #畫面核對
        targets, count = screen_capture.match_template_multi(ctx.images["54"], screenshot)  # 偵測圖案

        if targets and while_store == 0:
            print("機體補給結果")
            time.sleep(while_01)
            while_01 = 2

            #畫面截圖
            screenshot = screen_capture.get_screen(ctx.device)
            new_results = screen_capture.check_all_templates(screenshot)  # 偵測圖案
            results = screen_capture.accumulate_results(results, new_results)

            # 印出累積結果
            for name, count in results.items():
                print(f"{name} 累積出現 {count} 次")

            # 計算總次數
            total_count = sum(results.values())
            print(f"所有圖案累積出現次數總和：{total_count}")

            #畫面核對
            targets, count = screen_capture.match_template_multi(ctx.images["30"], screenshot)  # 偵測圖案

            if targets and total_count >= 3:
                write_excel.write_custom_excel(results, ctx.serial_number, ctx.id)
                ctx.number_of_runs += 1
                end_01(ctx, results)
            elif targets and total_count < 3:
                ctx.number_of_runs += 1
                if ctx.number_of_runs >= 10:
                    end_03(ctx)
                else:
                    end_02(ctx)

            time.sleep(1)

            while_store = 1

        #畫面核對
        targets, count = screen_capture.match_template_multi(ctx.images["37"], screenshot)  # 偵測圖案

        if targets and while_store == 1:
            print("點擊在補給1次")
            x, y = targets
            adb_controller.tap(ctx.device, x + 10, y + 10)  # 點擊目標（稍微偏移中心）
            while_store = 2
            time.sleep(1)
        
        #畫面核對
        targets, count = screen_capture.match_template_multi(ctx.images["38"], screenshot)  # 偵測圖案

        if targets and while_store == 2:
            print("點擊機體補給")
            x, y = targets
            adb_controller.tap(ctx.device, x + 10, y + 10)  # 點擊目標（稍微偏移中心）
            while_store = 0
            time.sleep(3)

        #畫面核對
        targets, count = screen_capture.match_template_multi(ctx.images["56"], screenshot)  # 偵測圖案

        if targets :
            print("出現連線忙碌中，回到初始刷取")
            end_02(ctx)
        
        time.sleep(0.5)

        # --- 這裡檢查是否已經超過 5 分鐘（200秒） ---
        elapsed = time.time() - start_time
        print(f"編號:{ctx.id} 運行經過時間:{elapsed}秒")
        if elapsed > 200:
            print(f"⚠️ [{ctx.id}] 跑超過 5 分鐘，自動執行 end_03() 重啟模擬器")
            end_03(ctx)
            start_time = time.time()  # ✅ 重設開始時間（讓它繼續計下一輪）

#刷到指定數量 儲存檔案並記錄
def end_01(ctx, results):

    start_time = time.time()  # ← 在這裡記錄開始時間

    adb_controller.keyevent(ctx.device, "APP_SWITCH")

    #迴圈綁定
    while_store = 0

    while True:
        
        #畫面截圖
        screenshot = screen_capture.get_screen(ctx.device)

        #畫面核對-沒有順序述
        targets, count = screen_capture.match_template_multi(ctx.images["46"], screenshot)  # 偵測圖案

        if targets and while_store == 0 :
            print("點擊全部清除")
            x, y = targets
            adb_controller.tap(ctx.device, x + 10, y + 10)  # 點擊目標（稍微偏移中心）
            time.sleep(1)
            while_store = 1

        # 推送檔案到模擬器
        # adb_controller.push_file(ctx.device, "C:/Users/user/Desktop/test.txt", "/data/media/0/Android/data/com.bandainamcoent.gget_WW/files/gamedata")

        # folder = Path("C:/Users/user/Desktop/SD鋼彈/saved")

        if while_store == 1 :

            # 要備份的模擬器內資料路徑（GameData）
            remote_path = "/data/media/0/Android/data/com.bandainamcoent.gget_WW/files/GameData"
            # 要儲存到本地的壓縮檔位置
            local_path = f"C:/Users/user/Desktop/SD鋼彈/saved/{ctx.id}_{ctx.serial_number}/gamedata.tar"

            # 備份
            adb_controller.backup_gamedata(ctx.device, remote_game_path=remote_path, local_tar_path=local_path)
            # 資料庫備份
            db_controller.insert_game_result_to_db(
                ctx = ctx,
                results = results,
                file_path = local_path ,
                db_config = {
                    "host": "localhost",
                    "user": "root",
                    "password": "sad69412",
                    "database": "game_db"
                }
            )

            ctx.serial_number += 1
            write_excel.update_config_value(ctx.id, ctx.serial_number)
            game_01(ctx)

        # --- 這裡檢查是否已經超過 5 分鐘（200秒） ---
        elapsed = time.time() - start_time
        print(f"編號:{ctx.id} 運行經過時間:{elapsed}秒")
        if elapsed > 20:
            print(f"⚠️ [{ctx.id}] 跑超過 5 分鐘，自動執行 end_03() 重啟模擬器")
            end_03(ctx)
            start_time = time.time()  # ✅ 重設開始時間（讓它繼續計下一輪）        

#沒刷到指定數量 回到user
def end_02(ctx):

    start_time = time.time()  # ← 在這裡記錄開始時間

    adb_controller.keyevent(ctx.device, "APP_SWITCH")

    #迴圈綁定
    while_store = 0

    while True:
        
        #畫面截圖
        screenshot = screen_capture.get_screen(ctx.device)

        #畫面核對-沒有順序述
        targets, count = screen_capture.match_template_multi(ctx.images["46"], screenshot)  # 偵測圖案

        if targets and while_store == 0 :
            print("點擊全部清除")
            x, y = targets
            adb_controller.tap(ctx.device, x + 10, y + 10)  # 點擊目標（稍微偏移中心）
            time.sleep(1)
            while_store = 1
            game_01(ctx)

        # --- 這裡檢查是否已經超過 5 分鐘（200秒） ---
        elapsed = time.time() - start_time
        print(f"編號:{ctx.id} 運行經過時間:{elapsed}秒")
        if elapsed > 20:
            print(f"⚠️ [{ctx.id}] 跑超過 5 分鐘，自動執行 end_03() 重啟模擬器")
            end_03(ctx)
            start_time = time.time()  # ✅ 重設開始時間（讓它繼續計下一輪） 

#沒刷到指定數量 到達運行指定次數
def end_03(ctx):
    simulator.restart_ldplayer(ctx.index)
    time.sleep(30)
    ctx.number_of_runs = 0
    game_01(ctx)

#檔案還原
def restore(ctx):
    # 要還原的檔案位置
    local_path_restore = "C:/Users/user/Desktop/SD鋼彈/saved/gamedata.tar"
    # 還原
    adb_controller.restore_gamedata(ctx.device, local_tar_path=local_path_restore)

def run_bot(device_id, sn, index):
    device = adb_controller.connect(device_id)
    images = image_loader.load_images()
    ctx = BotContext(device, images, serial_number=sn, id=device_id, index=index)
    game_01(ctx)

if __name__ == "__main__":
    
    device_map = {
        "emulator-5554": [91,'0'],
        # "emulator-5556": [65,'1'],
        # "emulator-5558": [11,'2']
    }

    write_excel.load_config_to_device_map(device_map)

    print(device_map)

    threads = []
    for device_id, sn in device_map.items():
        t = threading.Thread(target=run_bot, args=(device_id, sn[0], sn[1]))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

# if __name__ == "__main__":

#     serial_number = 13

#     number_of_runs = 0

#     device_id = {"emulator-5554":13,"emulator-5556":11}

#     # 載入圖片
#     images = image_loader.load_images()

#     #Adb裝置連結
#     device = adb_controller.connect(device_id=device_id[0])

#     user()