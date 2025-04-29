from PIL import Image
import numpy as np
import cv2
import adb_controller
import os

def get_screen(device):
    try:
        image_bytes = device.screencap()
        if not image_bytes:
            print("⚠️ screencap 擷取失敗：資料為空")
            return None
        image_array = np.frombuffer(image_bytes, np.uint8)
        if image_array.size == 0:
            print("⚠️ 擷取資料為空陣列")
            return None
        image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
        if image is None:
            print("⚠️ 圖片解碼失敗")
        return image
    except Exception as e:
        print(f"❌ get_screen 發生錯誤：{e}")
        return None

def match_template_multi(template_path, screen_img, threshold=0.8, min_dist=40):
    try:
        template = cv2.imread(template_path, 0)
        if screen_img is None or template is None:
            print(f"⚠️ 匹配失敗，圖片為 None：{template_path}")
            return None, 0

        screen_gray = cv2.cvtColor(screen_img, cv2.COLOR_BGR2GRAY)
        res = cv2.matchTemplate(screen_gray, template, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= threshold)

        raw_matches = list(zip(*loc[::-1]))  # 初始比對結果
        filtered_matches = []

        for pt in raw_matches:
            too_close = False
            for fpt in filtered_matches:
                dist = np.linalg.norm(np.array(pt) - np.array(fpt))
                if dist < min_dist:
                    too_close = True
                    break
            if not too_close:
                filtered_matches.append(pt)

        first_match = filtered_matches[0] if filtered_matches else None
        return first_match, len(filtered_matches)
    except Exception as e:
        print(f"❌ match_template_multi 發生錯誤：{e}")
        return None, 0

def check_all_templates(screen_img, template_dir="UR", threshold=0.9):
    result = {}
    for filename in os.listdir(template_dir):
        if filename.lower().endswith(".png"):
            path = os.path.join(template_dir, filename)
            targets, count = match_template_multi(path, screen_img, threshold)
            result[filename] = count
    return result

def accumulate_results(old_results, new_results):
    for key, new_count in new_results.items():
        if key in old_results:
            old_results[key] += new_count
        else:
            old_results[key] = new_count
    return old_results

if __name__ == "__main__":
    device = adb_controller.connect()
    image = get_screen(device)

    if image is not None:
        cv2.imshow("screenshot", image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        print("🚫 無法取得螢幕畫面，跳過顯示")
