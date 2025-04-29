import subprocess
import time



def restart_ldplayer(index):

    ld_path = "E:/LDPlayer/LDPlayer9/dnconsole.exe"  # 你的 dnconsole.exe 路徑

    # 關閉模擬器
    subprocess.run([ld_path, "quit", "--index", index])
    print("✅ 模擬器已關閉，等待 5 秒再重啟")
    time.sleep(5)
    # 重啟模擬器
    subprocess.run([ld_path, "launch", "--index", index])
    print("✅ 模擬器已重啟")
