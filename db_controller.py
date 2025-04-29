import mariadb
import os
from datetime import datetime

def insert_game_result_to_db(ctx, results, file_path, db_config):
    UR_NAME_MAP = {
        "UR_01": "吉姆", "UR_02": "獵魔", "UR_03": "天鵝", "UR_04": "風零",
        "UR_05": "鋼彈Ez8", "UR_06": "海盜", "UR_07": "獨角獸", "UR_08": "初鋼",
        "UR_09": "NT鋼彈", "UR_10": "能天使", "UR_11": "沙薩比", "UR_12": "v鋼",
        "UR_13": "鳳凰", "UR_14": "自由", "UR_15": "布萊德‧諾亞&白色基地", "UR_16": "瑪琉‧拉米亞斯&大天使號",
        "UR_17": "奧爾加‧伊茲卡&漁火", "UR_18": "深村玲&苞型運輸艇", "UR_19": "莉莉娜‧多莉安&皮斯美麗昂",
        "UR_20": "芙勞‧寶&白色基地", "UR_21": "漢肯‧貝克納&拉迪修", "UR_22": "蒂法‧安迪爾&自由號",
        "UR_23": "瑪麗娜‧伊士麥&托勒密號2型", "UR_24": "米奧莉奈‧倫布蘭&學園艦",
        "UR_25": "比查‧奧雷格&新阿伽馬號", "UR_26": "古荻莉亞‧藍那‧伯恩斯坦&漁火",
        "UR_27": "皇‧李‧諾瑞加&托勒密號", "UR_28": "安德魯‧巴爾特菲爾德&永恆號",
        "UR_29": "花園麗&阿伽馬",
    }

    try:
        # 彙總 total
        total = 0
        ur_counts = []
        for key, zh_name in UR_NAME_MAP.items():
            count = 0
            for result_key, val in results.items():
                if result_key.startswith(key):
                    count += val
            total += count
            ur_counts.append((zh_name, count))

        # 若 file 不存在則跳過
        if not os.path.exists(file_path):
            print(f"❌ 找不到檔案：{file_path}")
            return

        with open(file_path, "rb") as f:
            file_data = f.read()

        # 建立資料庫連線
        conn = mariadb.connect(**db_config)
        cursor = conn.cursor()

        # 插入主紀錄（game_records）
        cursor.execute("""
            INSERT INTO game_records (
                host_name, emulator_id, serial_number,
                total_count, saved_filename, file_data, uploaded_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            ctx.host_name, ctx.id, ctx.serial_number,
            total, os.path.basename(file_path), file_data, datetime.now()
        ))

        record_id = cursor.lastrowid  # 取得 auto_increment ID

        # 插入每個角色的 UR 數量
        for ur_name, count in ur_counts:
            cursor.execute("""
                INSERT INTO ur_counts (record_id, ur_name, count)
                VALUES (?, ?, ?)
            """, (record_id, ur_name, count))

        conn.commit()
        cursor.close()
        conn.close()
        print(f"✅ 資料成功寫入資料庫（ID: {record_id}）")

    except Exception as e:
        print(f"❌ 資料寫入失敗：{e}")
