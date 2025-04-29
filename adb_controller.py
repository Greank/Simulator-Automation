from ppadb.client import Client as AdbClient
import os

# Adb 裝置連結
def connect(device_id="emulator-5554"):
    try:
        client = AdbClient(host="127.0.0.1", port=5037)
        devices = client.devices()
        print("已連接裝置：", [d.serial for d in devices])

        if not devices:
            raise RuntimeError("找不到任何 ADB 裝置")

        return client.device(device_id)
    except Exception as e:
        print(f"❌ ADB 裝置連接失敗：{e}")
        return None

# 點擊位置
def tap(device, x, y):
    try:
        if device:
            device.shell(f"input tap {x} {y}")
        else:
            print("⚠️ 無有效裝置，tap 指令跳過")
    except Exception as e:
        print(f"❌ tap 執行失敗：{e}")

# 文字輸入（支援空白與特殊符號轉義）
def text(device, text):
    try:
        if device:
            # 先轉換空白為 %s（input text 的特殊表示方式）
            safe_text = text.replace(" ", "%s")

            # 特殊字元轉義對照表
            special_chars = {
                "$": "\\$",
                "&": "\\&",
                "|": "\\|",
                ";": "\\;",
                "<": "\\<",
                ">": "\\>"
            }


            # 替換所有特殊字元
            for char, escaped in special_chars.items():
                safe_text = safe_text.replace(char, escaped)

            # 輸出執行的實際指令（方便 debug）
            print(f" input text 傳送：{safe_text}")

            device.shell(f'input text "{safe_text}"')
        else:
            print(" 無有效裝置，text 指令跳過")
    except Exception as e:
        print(f" text 輸入失敗：{e}")

# 按鍵事件（支援任意 keyevent 代碼）
def keyevent(device, keyevent):
    """
    //模拟电源按键
    adb shell input keyevent 26
    //解锁滑屏
    adb shell input keyevent  82
    //在屏幕上做划屏操作，前四个数为坐标点，后面是滑动的时间（单位毫秒）
    adb shell input swipe 50 250 500 250 200
    //主屏按键回到桌面
    adb shell input keyevent  3
    //物理返回键
    adb shell input keyevent  4
    //打电话界面
    adb shell input keyevent  5
    //关闭屏幕
    adb shell input keyevent  6
    //声音上
    adb shell input keyevent  KEYCODE_VOLUME_UP
    //声音下
    adb shell input keyevent  KEYCODE_VOLUME_DOWN
    //上
    adb shell input keyevent  KEYCODE_DPAD_UP
    //下
    adb shell input keyevent  KEYCODE_DPAD_DOWN
    //左
    adb shell input keyevent  KEYCODE_DPAD_LEFT
    //右
    adb shell input keyevent  KEYCODE_DPAD_RIGHT
    //进去选中程序命令
    adb shell input keyevent  KEYCODE_DPAD_CENTER
    //拍照键
    adb shell input keyevent  KEYCODE_CAMERA
    //多媒体播放按钮
    adb shell input keyevent  KEYCODE_MEDIA_PLAY
    //多媒体键 停止
    adb shell input keyevent  KEYCODE_MEDIA_STOP
    //多媒体键 暂停
    adb shell input keyevent  KEYCODE_MEDIA_PAUSE
    //多媒体键 播放/暂停
    adb shell input keyevent  KEYCODE_MEDIA_PLAY_PAUSE
    //多媒体键 快进
    adb shell input keyevent  KEYCODE_MEDIA_FAST_FORWARD
    //多媒体键 快退
    adb shell input keyevent  KEYCODE_MEDIA_REWIND
    //多媒体键 下一首
    adb shell input keyevent  KEYCODE_MEDIA_NEXT
    //媒体键 上一首
    adb shell input keyevent  KEYCODE_MEDIA_PREVIOUS多
    //所有任务窗口
    adb shell input keyevent  KEYCODE_APP_SWITCH
    打电话功能
    adb shell am start -a android.intent.action.CALL tel:18611290021
    关机功能
    adb shell reboot -p
    //获取手机上层的activity
    adb shell dumpsys activity | findstr "mResumedActivity"
    //选择浏览器打开地址
    adb shell am start -a android.intent.action.VIEW -d  www.baidu.cn/
    //打开一个应用程序
    adb shell am start -a -n com.android.mediacenter/.PageActivity
    //下拉显示命令行
    adb shell service call statusbar 1
    //收缩状态栏
    adb shell service call statusbar 2
    //设置窗口大小的命令
    adb shell wm size 540x960
    //恢复窗口设置
    adb shell wm size reset
    //关闭wifi
    adb shell svc wifi disable
    //打开wifi
    adb shell svc wifi enable
    //adb 发送广播
    adb shell am broadcast -n com.ztemt.test.basic/.receiver.FlashLightBroadcastReceiver -a cn.programmer.CUSTOM_INTENT --ez enable true

    """
    try:
        if device:
            device.shell(f"input keyevent KEYCODE_{keyevent}")
        else:
            print("⚠️ 無有效裝置，keyevent 指令跳過")
    except Exception as e:
        print(f"❌ keyevent 執行失敗：{e}")

def backup_gamedata(device, remote_game_path, local_tar_path, temp_tar_name="gamedata.tar"):
    """
    從模擬器備份資料夾並拉回電腦。
    :param ctx: BotContext（包含 device）
    :param remote_game_path: 模擬器要打包的資料夾（例：/data/media/0/...）
    :param local_tar_path: 要儲存在本地的 tar 檔案完整路徑
    :param temp_tar_name: 模擬器暫存檔名（預設 gamedata.tar）
    """
    try:
        # 1️⃣ 自動建立目錄
        local_dir = os.path.dirname(local_tar_path)
        os.makedirs(local_dir, exist_ok=True)

        # 2️⃣ 壓縮與拉取
        print(f"📦 備份開始：{remote_game_path}")
        device.shell(f"su -c 'tar -cf /sdcard/{temp_tar_name} {remote_game_path}'")
        device.pull(f"/sdcard/{temp_tar_name}", local_tar_path)
        print(f"✅ 備份完成 → {local_tar_path}")
    except Exception as e:
        print(f"❌ 備份失敗：{e}")


def restore_gamedata(device, local_tar_path, temp_tar_name="gamedata.tar"):
    """
    將本地壓縮檔推回模擬器並還原。
    :param device: BotContext
    :param local_tar_path: 本地壓縮檔完整路徑
    :param temp_tar_name: 模擬器內的暫存檔名（預設 gamedata.tar）
    """
    try:
        print(f"📦 開始還原：{local_tar_path}")
        device.push(local_tar_path, f"/sdcard/{temp_tar_name}")
        device.shell(f"su -c 'tar -xf /sdcard/{temp_tar_name} -C /'")
        print(f"✅ 還原完成 → 解壓至根目錄 /")
    except Exception as e:
        print(f"❌ 還原失敗：{e}")


# 連線測試用
if __name__ == "__main__":
    device = connect()
    tap(device, 270, 278)

    # 要備份的模擬器內資料路徑（GameData）
    remote_path = "/data/media/0/Android/data/com.bandainamcoent.gget_WW/files/GameData"
    # 要儲存到本地的壓縮檔位置
    local_path = "C:/Users/user/Desktop/gamedata.tar"

    # 備份
    backup_gamedata(device, remote_game_path=remote_path, local_tar_path=local_path)

    # 還原
    restore_gamedata(device, local_tar_path=local_path)
