import sqlite3

DB_FILE = "history.db"

def get_conn():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row      # 让查询结果带上列名（默认是元组）
    return conn

#把数据库所有操作包括sql语句都放在项目里面
def init_db():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        text TEXT,
        score REAL,
        label TEXT,
        pinyin TEXT,
        created_at TEXT
    )
    """)
    #idx是索引，history是表名，created是字段名，created_at是字段名
    cur.execute("CREATE INDEX IF NOT EXISTS idx_history_created ON history(created_at)")
    conn.commit()
    conn.close()



#用？进行参数化查询，防止SQL注入攻击
#用created_at字段,其在main.py中已经使用，保证一致性
def save_record(record):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO history (text, score, label, pinyin, created_at) VALUES (?, ?, ?, ?, ?)",
        [record["text"], record["score"], record["label"], record["pinyin"], record["created_at"]],
    )
    conn.commit()
    conn.close()


def get_history(limit):
    conn = get_conn()
    cur = conn.cursor()
    rows = cur.execute(
        "SELECT * FROM history ORDER BY created_at DESC LIMIT ?",
        [limit],
    ).fetchall()
    conn.close()

    records = []
    for row in rows:
        records.append(dict(row))
    return records

