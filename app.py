from flask import Flask, jsonify, render_template ,request, send_file
import mariadb
import os
from io import BytesIO
import subprocess
import time

# ✅ 指定圖片路徑：將 templates/images 當作 static_url_path=/images 使用
app = Flask(
    __name__,
    static_url_path="/images",                # 網頁上的路徑
    static_folder="templates/images",         # 實際檔案位置
    template_folder="templates"               # HTML 放哪裡
)

# 資料庫設定
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "sad69412",
    "database": "game_db"
}

# 密碼（你可改成環境變數更安全）
INTERNAL_PASSWORD = "sad69412"

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        password = request.form.get("password")
        if password == INTERNAL_PASSWORD:
            return render_template("index.html")
        else:
            return "❌ 密碼錯誤", 403
    return '''
        <form method="post">
            <h3>🔐 請輸入密碼進入內部系統</h3>
            <input type="password" name="password" />
            <button type="submit">進入</button>
        </form>
    '''

@app.route("/client")
def client():
    return render_template("client.html")  # 客戶用（公開）


@app.route("/id_check", methods=["GET", "POST"])
def id_check():
    if request.method == "POST":
        password = request.form.get("password")
        if password == INTERNAL_PASSWORD:
            return render_template("id_check.html")
        else:
            return "❌ 密碼錯誤", 403

    return '''
        <form method="post">
            <h3>🔐 請輸入密碼進入帳號查驗</h3>
            <input type="password" name="password" />
            <button type="submit">進入</button>
        </form>
    '''

@app.route("/api/records")
def get_records():
    try:
        conn = mariadb.connect(**db_config)
        cursor = conn.cursor(dictionary=True)

        # 1. 先抓主表
        cursor.execute("""
            SELECT id, host_name, emulator_id, serial_number, total_count, uploaded_at
            FROM game_records
            ORDER BY uploaded_at DESC
        """)
        records = cursor.fetchall()

        # 2. 一筆筆查對應的 ur_counts
        for record in records:
            cursor.execute("""
                SELECT ur_name AS name, count
                FROM ur_counts
                WHERE record_id = ?
            """, (record['id'],))
            record['ur_counts'] = cursor.fetchall()

        cursor.close()
        conn.close()
        return jsonify(records)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    
@app.route("/api/filter", methods=["POST"])
def filter_records():
    try:
        filters = request.json  # e.g., {"吉姆": 1, "海盜": 2}
        if not filters:
            return jsonify({"error": "無搜尋條件"}), 400

        conn = mariadb.connect(**db_config)
        cursor = conn.cursor(dictionary=True)

        # 1. 找出所有符合條件的紀錄
        placeholders = []
        for ur_name, count in filters.items():
            placeholders.append(f"""
                (SELECT count FROM ur_counts
                 WHERE record_id = gr.id AND ur_name = '{ur_name}') >= {count}
            """)
        where_clause = " AND ".join(placeholders)

        sql = f"""
            SELECT gr.id, gr.host_name, gr.emulator_id, gr.serial_number,
                   gr.total_count, gr.uploaded_at
            FROM game_records gr
            WHERE {where_clause}
            ORDER BY uploaded_at DESC
        """

        cursor.execute(sql)
        records = cursor.fetchall()

        # 2. 每筆補上 ur_counts 陣列
        for record in records:
            cursor.execute("""
                SELECT ur_name AS name, count
                FROM ur_counts
                WHERE record_id = ?
            """, (record['id'],))
            record['ur_counts'] = cursor.fetchall()

        cursor.close()
        conn.close()
        return jsonify(records)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    
@app.route("/api/download/<int:record_id>")
def download_file(record_id):
    try:
        conn = mariadb.connect(**db_config)
        cursor = conn.cursor()

        cursor.execute("SELECT saved_filename, file_data FROM game_records WHERE id = ?", (record_id,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()

        if not row:
            return "找不到資料", 404

        filename, data = row
        return send_file(BytesIO(data), download_name=filename, as_attachment=True)

    except Exception as e:
        return str(e), 500


@app.route("/api/run_search", methods=["POST"])
def run_search():
    user_id = request.json.get("user_id")

    try:
        subprocess.run(["python", "search.py", user_id], check=True)

        # 等待圖片出現
        img1_path = "templates/images/img1.png"
        img2_path = "templates/images/img2.png"
        timeout = 15  # 最多等 15 秒
        waited = 0
        while not (os.path.exists(img1_path) and os.path.exists(img2_path)):
            time.sleep(0.5)
            waited += 0.5
            if waited > timeout:
                return jsonify({"error": "圖片產生逾時"}), 500

        return jsonify({
            "img1": "/images/img1.png",
            "img2": "/images/img2.png"
        })

    except subprocess.CalledProcessError as e:
        return jsonify({"error": f"執行失敗：{e}"}), 500


from flask import Response, stream_with_context
import subprocess

@app.route("/api/submit_stream")
def submit_stream():
    account = request.args.get("account")
    password = request.args.get("password")

    def generate():
        try:
            process = subprocess.Popen(
                ["python", "-u", "final_submit.py", account, password],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1
            )


            # 即時逐行讀出輸出
            for line in process.stdout:
                yield f"data: {line.strip()}\n\n"

            process.stdout.close()
            process.wait()
            yield f"data: ✅ 執行完成\n\n"

        except Exception as e:
            yield f"data: ❌ 發生錯誤：{str(e)}\n\n"

    return Response(stream_with_context(generate()), mimetype='text/event-stream')





if __name__ == "__main__":
    app.run(debug=True)
