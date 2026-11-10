
import sqlite3

def init_database():
    # 1. 建立或連接到本地的 SQLite 資料庫檔案 (shop.db)
    conn = sqlite3.connect("shop.db")
    cursor = conn.cursor()

    # 啟用 SQLite 的外來鍵約束
    cursor.execute("PRAGMA foreign_keys = ON;")

    # 2. 建立 orders (訂單主表)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_name TEXT NOT NULL,
            total_amount REAL NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # 3. 建立 order_item (訂單明細表)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS order_item (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            product_name TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            price REAL NOT NULL,
            FOREIGN KEY (order_id) REFERENCES orders (id) ON DELETE CASCADE
        )
    """)

    conn.commit()
    print("成功建立空的 orders 與 order_item 資料表！")

    # 4. 測試關聯性：寫入一筆主表與兩筆明細
    try:
        cursor.execute("INSERT INTO orders (customer_name, total_amount) VALUES (?, ?)", ("王小明", 1250.0))
        order_id = cursor.lastrowid  # 取得剛剛生成的訂單編號

        items = [
            (order_id, "Python 程式設計書", 1, 650.0),
            (order_id, "環保不鏽鋼杯", 2, 300.0)
        ]
        cursor.executemany("INSERT INTO order_item (order_id, product_name, quantity, price) VALUES (?, ?, ?, ?)", items)
        
        conn.commit()
        print(f"測試關聯成功！已成功寫入主表 ID: {order_id} 及其對應的明細。")

    except Exception as e:
        print(f"寫入測試資料失敗：{e}")
        conn.rollback()

    finally:
        conn.close()

if __name__ == "__main__":
    init_database()