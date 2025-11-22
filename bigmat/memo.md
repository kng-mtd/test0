```bash
cd ~/venv0
. bin/activate

echo "alias py='python3'" >> ~/.bashrc
source ~/.bashrc

pip install pandas numpy polars pyarrow
```

## 1. Apache Arrow

- **概要**：メモリ上の列指向データフォーマット
- **特徴**：

  - 列単位アクセスで高速
  - メモリ上で直接操作可能（コピーなしで別プロセスへ渡せる）
  - SIMD / マルチスレッド計算に適している

- **用途**：

  - 巨大データのメモリ内操作
  - Polars や NumPy などに変換して処理

---

## 2. Arrow IPC

- **概要**：Arrow Table を保存・転送するバイナリ形式
- **特徴**：

  - ファイルに保存しても Arrow Table と互換
  - 軽量圧縮で高速 I/O
  - 別プロセスへの受け渡しに便利

- **用途**：

  - データの永続化
  - プロセス間通信や部分読み込み

- **Arrow との関係**：

  - Arrow = メモリ上データ表
  - Arrow IPC = Arrow をファイル化 / 他プロセスに渡す形式

---

## 3. Parquet

- **概要**：列指向の永続化フォーマット
- **特徴**：

  - 圧縮率が高くディスク節約に有効
  - 列単位で読み込み可能 → I/O 高速
  - Arrow Table と互換

- **用途**：

  - ディスク保存して必要な列だけ読み込みたい場合
  - 巨大データのタイル化保存（2D chunk）に最適

---

## 4. Polars

- **概要**：高速 DataFrame ライブラリ
- **特徴**：

  - Arrow Table / Arrow IPC / Parquet と相性が良い
  - LazyFrame による部分読み込み・遅延評価
  - Rust 実装で SIMD / マルチスレッド計算
  - 統計・集計・join・filter に強い

- **用途**：

  - Arrow / Parquet / Arrow IPC のデータ操作
  - 計算の前処理や部分抽出

---

Polars で **CSV、Parquet、ArrowIPC** を読み込む

## 1. CSV

| 方法         | コード                                                   | 説明                                             |
| ------------ | -------------------------------------------------------- | ------------------------------------------------ |
| 通常読み込み | `df = pl.read_csv("data.csv", has_header=True, sep=",")` | 全体を DataFrame として読み込む                  |
| 遅延読み込み | `lf = pl.scan_csv("data.csv", has_header=True, sep=",")` | LazyFrame、巨大 CSV 向け。必要なチャンクだけ処理 |

---

## 2. Parquet

| 方法         | コード                                 | 説明                                           |
| ------------ | -------------------------------------- | ---------------------------------------------- |
| 通常読み込み | `df = pl.read_parquet("data.parquet")` | 全体を DataFrame として読み込む                |
| 遅延読み込み | `lf = pl.scan_parquet("data.parquet")` | LazyFrame、巨大 Parquet 向け。メモリ効率が良い |

---

## 3. ArrowIPC / Feather

| 方法         | コード                           | 説明                                                                                                |
| ------------ | -------------------------------- | --------------------------------------------------------------------------------------------------- |
| 通常読み込み | `df = pl.read_ipc("data.arrow")` | ArrowIPC / Feather を DataFrame として読み込む                                                      |
| 遅延読み込み | **サポートなし**                 | LazyFrame での直接読み込みは現在非対応。巨大データの場合は Parquet に変換して `scan_parquet` で読む |

---

## 1. CSV → Parquet

```python
import polars as pl

def csv_to_parquet(csv_path, parquet_path, chunksize=10**6):
    """
    CSV を Parquet に変換（巨大ファイル対応）
    """
    # 遅延読み込みでチャンク処理
    lf = pl.scan_csv(csv_path, has_header=False, sep=",")

    # 一度に collect して書き出す場合（中規模ファイル向き）
    df = lf.collect()
    df.write_parquet(parquet_path)

# 使用例
csv_to_parquet("data.csv", "data.parquet")
```

---

## 2. ArrowIPC → Parquet

```python
import polars as pl

def arrowipc_to_parquet(ipc_path, parquet_path):
    """
    ArrowIPC / Feather を Parquet に変換
    """
    # ArrowIPC を DataFrame として読み込む
    df = pl.read_ipc(ipc_path)
    # Parquet に書き出す
    df.write_parquet(parquet_path)

# 使用例
arrowipc_to_parquet("data.arrow", "data.parquet")
```

---

Arrow を用いた **ELT（Extract, Load, Transform）** 。Arrow は **メモリ上で列指向データを扱える** ので、特に巨大データの ELT で高速化に強みがあります。整理すると次のようになります。

---

## 1. Arrow を使う ELT の基本フロー

```
Extract → Load → Transform
```

- **Extract（抽出）**

  - データベースやファイル（CSV/Parquet）から Arrow Table に読み込む
  - 例: DuckDB, PostgreSQL, S3, Parquet など
  - 巨大データでもバッチ/ストリーム処理可能

- **Load（格納）**

  - Arrow Table を中間ストレージやデータウェアハウスにロード
  - DuckDB、SQLite、Parquet ファイル、S3 など
  - ゼロコピー可能な場合はそのまま渡す

- **Transform（変換/集計）**

  - Arrow Table 上で直接集計やフィルタリング
  - Polars, PyArrow compute, DuckDB などで SQL/列指向操作可能
  - DataFrame に変換せずに高速処理

---

## 2. Arrow を使うメリット

| 項目     | Arrow 使用時の利点                                       |
| -------- | -------------------------------------------------------- |
| データ量 | 数 GB〜数 TB でもメモリ上で列指向処理可能                |
| 言語間   | Python ↔ R ↔ Rust ↔ C++ などで同じデータ形式で受け渡せる |
| 高速処理 | ゼロコピーでのプロセス間通信、列指向計算に最適           |
| 保存形式 | Parquet / Feather と互換性あり、永続化や再利用が容易     |

---

## 3. Python での簡単な ELT サンプル

```python
import pyarrow as pa
import pyarrow.parquet as pq
import duckdb
import pandas as pd
import numpy as np

# --- Extract: CSV/DB から Arrow Table に読み込む ---
df = pd.DataFrame({
    'user_id': np.arange(1, 1_000_001),
    'amount': np.random.rand(1_000_000)
})
table = pa.Table.from_pandas(df)

# --- Load: DuckDB にロード ---
con = duckdb.connect('elt_demo.duckdb')
con.register('arrow_table', table)
con.execute('CREATE TABLE IF NOT EXISTS transactions AS SELECT * FROM arrow_table')

# --- Transform: Arrow Table 上で集計 ---
# SQL で集計して Arrow Table で取得
result = con.execute('SELECT user_id % 100 AS user_group, SUM(amount) AS total_amount FROM transactions GROUP BY user_group').arrow()

# 結果を Parquet に永続化
pq.write_table(result, 'transactions_summary.parquet')
```

ポイント：

1. **Extract**

   - CSV/Parquet/DB から Arrow Table に変換
   - 巨大データでも chunk/batch で読み込み可能

2. **Load**

   - Arrow Table を DuckDB に登録（`con.register()`）
   - ゼロコピーで SQL 処理が可能

3. **Transform**

   - SQL や Polars, PyArrow compute で列指向処理
   - 結果も Arrow Table のまま保存

---

## 4. 巨大データ・分散処理の場合

- バッチ単位で Arrow Table に変換 → Queue/IPC でプロセス間転送
- DuckDB / Polars で並列集計 → 結果を再度 Arrow Table にまとめる
- S3 / Parquet に永続化 → 次段階の ELT/BI ツールで利用可能

---

Arrow を中心に据えると、**ELT の Extract→Load→Transform がすべて高速・列指向・ゼロコピーで処理可能** になります。

---

Arrow を使う場合と使わない場合（通常の pandas DataFrame や CSV/Parquet 経由）の **ELT 処理パフォーマンスの比較** を整理します。ポイントは「列指向＋ゼロコピー」がどれだけ効くかです。

---

## 1. 比較対象

| 方法                        | 特徴                                                                           |
| --------------------------- | ------------------------------------------------------------------------------ |
| **Arrow + DuckDB / Polars** | メモリ上で列指向処理、IPC バッファでプロセス間ゼロコピー可。大規模データ向け。 |
| **pandas + CSV / Parquet**  | DataFrame にロードして行指向で処理。プロセス間でコピーが発生しやすい。         |

---

## 2. サンプルシナリオ

- データ: 1000 万行 × 3 列 (`user_id`, `amount`, `category`)
- 処理: `category` ごとの `amount` 合計
- 計測: pandas CSV、Parquet、Arrow Table + DuckDB の 3 パターン

---

### (A) pandas + CSV

```python
import pandas as pd
import numpy as np
import time

df = pd.DataFrame({
    'user_id': np.arange(1, 10_000_001),
    'amount': np.random.rand(10_000_000),
    'category': np.random.randint(0, 100, size=10_000_000)
})

df.to_csv('data.csv', index=False)

start = time.time()
df2 = pd.read_csv('data.csv')
result = df2.groupby('category')['amount'].sum()
print("pandas CSV:", time.time() - start)
```

- **特徴**: CSV の読み書きで I/O がボトルネック
- **メモリコピー**: 行指向なので列ごと計算が非効率

---

### (B) pandas + Parquet

```python
df.to_parquet('data.parquet', index=False)

start = time.time()
df2 = pd.read_parquet('data.parquet')
result = df2.groupby('category')['amount'].sum()
print("pandas Parquet:", time.time() - start)
```

- **特徴**: 列指向圧縮で CSV より速い
- **制約**: DataFrame にロードする時点でコピー発生

---

### (C) Arrow Table + DuckDB

```python
import pyarrow as pa
import duckdb
import time

table = pa.Table.from_pandas(df)

start = time.time()
con = duckdb.connect()
con.register('t', table)
result = con.execute('SELECT category, SUM(amount) as total_amount FROM t GROUP BY category').arrow()
print("Arrow + DuckDB:", time.time() - start)
```

- **特徴**: 列指向 + Arrow Table 上で直接 SQL 処理
- **ゼロコピー**: 別プロセス間でも IPC でバッファを渡せる
- **I/O**: データベースにロードせずメモリ上で処理

---

## 3. 期待されるパフォーマンス傾向

| 方法                    | I/O 負荷 | メモリコピー | 集計速度 | コメント                                           |
| ----------------------- | -------- | ------------ | -------- | -------------------------------------------------- |
| pandas + CSV            | 高       | 高           | 遅い     | 大規模データではボトルネック                       |
| pandas + Parquet        | 中       | 中           | 中       | 読み込みは高速だがコピーあり                       |
| Arrow + DuckDB / Polars | 低       | 低           | 高速     | 列指向で計算もゼロコピー可能、数十 GB 規模でも効く |

---

**巨大データ（10GB 級）を使った pandas vs Arrow+DuckDB のパフォーマンス比較サンプル** を作ります。ここでは、**生成 → 読み込み → 集計 → 出力** の全工程で時間を計測します。

---

### Python サンプルコード

```python
# performance_compare.py
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import duckdb
import numpy as np
import time
import os

# -----------------------------
# データ生成（約10GB想定）
# -----------------------------
N_ROWS = 50_000_000  # 5千万行 × 3列で約10GB（float64, int64）
CSV_FILE = 'data.csv'
PARQUET_FILE = 'data.parquet'

if not os.path.exists(CSV_FILE):
    print("Generating CSV data...")
    df = pd.DataFrame({
        'user_id': np.arange(N_ROWS),
        'amount': np.random.rand(N_ROWS),
        'category': np.random.randint(0, 1000, size=N_ROWS)
    })
    df.to_csv(CSV_FILE, index=False)
    print("CSV written.")

if not os.path.exists(PARQUET_FILE):
    print("Generating Parquet data...")
    df = pd.read_csv(CSV_FILE, usecols=['user_id', 'amount', 'category'])
    df.to_parquet(PARQUET_FILE, index=False)
    print("Parquet written.")

# -----------------------------
# 1. pandas + CSV
# -----------------------------
print("\n== pandas + CSV ==")
start = time.time()
df_csv = pd.read_csv(CSV_FILE)
load_time = time.time()
result_csv = df_csv.groupby('category')['amount'].sum()
groupby_time = time.time()
result_csv.to_csv('result_csv.csv', index=False)
write_time = time.time()
print(f"Load: {load_time-start:.2f}s, GroupBy: {groupby_time-load_time:.2f}s, Write: {write_time-groupby_time:.2f}s")

# -----------------------------
# 2. pandas + Parquet
# -----------------------------
print("\n== pandas + Parquet ==")
start = time.time()
df_parquet = pd.read_parquet(PARQUET_FILE)
load_time = time.time()
result_parquet = df_parquet.groupby('category')['amount'].sum()
groupby_time = time.time()
result_parquet.to_parquet('result_parquet.parquet', index=False)
write_time = time.time()
print(f"Load: {load_time-start:.2f}s, GroupBy: {groupby_time-load_time:.2f}s, Write: {write_time-groupby_time:.2f}s")

# -----------------------------
# 3. Arrow Table + DuckDB
# -----------------------------
print("\n== Arrow + DuckDB ==")
start = time.time()
df = pd.read_parquet(PARQUET_FILE)
table = pa.Table.from_pandas(df, preserve_index=False)
load_time = time.time()

con = duckdb.connect()
con.register('t', table)
result = con.execute('SELECT category, SUM(amount) AS total_amount FROM t GROUP BY category').arrow()
groupby_time = time.time()

pq.write_table(result, 'result_arrow_duckdb.parquet')
write_time = time.time()
print(f"Load: {load_time-start:.2f}s, GroupBy: {groupby_time-load_time:.2f}s, Write: {write_time-groupby_time:.2f}s")
```

---

### ポイント

1. **データ生成**

   - CSV と Parquet の両方を作成
   - 10GB 規模でも処理可能（メモリ容量に応じて N_ROWS を調整）

2. **計測対象**

   - データ読み込み時間 (`Load`)
   - 集計 / グループ化時間 (`GroupBy`)
   - 結果書き込み時間 (`Write`)

3. **Arrow + DuckDB の利点**

   - 読み込み後は Arrow Table 上で直接 SQL 集計
   - ゼロコピーでプロセス間に渡すことも可能
   - CSV/Parquet を DataFrame に変換する手間やコピーを削減

---

### 期待される傾向

| 方法             | Load | GroupBy | Write | コメント                                               |
| ---------------- | ---- | ------- | ----- | ------------------------------------------------------ |
| pandas + CSV     | 高   | 中      | 高    | I/O ボトルネック大                                     |
| pandas + Parquet | 中   | 中      | 中    | 列指向なので CSV より高速                              |
| Arrow + DuckDB   | 低   | 低      | 中    | 列指向＋ゼロコピーで集計最速、数十 GB 規模でも対応可能 |

---

では、先ほどのサンプルを **バッチ／ストリーム処理対応** に改良して、**メモリ使用量を抑えつつ巨大データを Arrow + DuckDB で高速 ELT** できる形にします。

---

### Python サンプル：バッチ・ストリーム ELT

```python
# batch_stream_elt.py
import pyarrow as pa
import pyarrow.parquet as pq
import duckdb
import pandas as pd
import numpy as np
import time
import os

# -----------------------------
# 設定
# -----------------------------
N_ROWS = 50_000_000  # 総行数（5千万行）
BATCH_SIZE = 5_000_000  # バッチ行数
PARQUET_FILE = 'data.parquet'
RESULT_FILE = 'result_arrow_duckdb.parquet'

# -----------------------------
# データ生成（Parquet）
# -----------------------------
if not os.path.exists(PARQUET_FILE):
    print("Generating Parquet data...")
    for start in range(0, N_ROWS, BATCH_SIZE):
        end = min(start + BATCH_SIZE, N_ROWS)
        df = pd.DataFrame({
            'user_id': np.arange(start, end),
            'amount': np.random.rand(end-start),
            'category': np.random.randint(0, 1000, size=end-start)
        })
        if start == 0:
            df.to_parquet(PARQUET_FILE, index=False)
        else:
            # append mode
            df.to_parquet(PARQUET_FILE, index=False, engine='pyarrow', append=True)
        print(f"Wrote rows {start}-{end}")
    print("Parquet data generated.")

# -----------------------------
# Arrow + DuckDB バッチ集計
# -----------------------------
con = duckdb.connect()
start_time = time.time()

# Parquet をバッチ読み込みして DuckDB に登録
offset = 0
while offset < N_ROWS:
    batch_df = pd.read_parquet(PARQUET_FILE, engine='pyarrow', columns=['user_id','amount','category'], use_threads=True)
    table = pa.Table.from_pandas(batch_df, preserve_index=False)
    con.register(f'batch_{offset}', table)
    if offset == 0:
        sql_union = f"SELECT category, SUM(amount) as total_amount FROM batch_{offset} GROUP BY category"
    else:
        sql_union = f"SELECT category, SUM(amount) as total_amount FROM ({sql_union} UNION ALL SELECT category, SUM(amount) as total_amount FROM batch_{offset}) GROUP BY category"
    offset += BATCH_SIZE

# SQL実行して集計結果を Arrow Table で取得
result = con.execute(sql_union).arrow()
mid_time = time.time()

# 結果を Parquet に書き込み
pq.write_table(result, RESULT_FILE)
end_time = time.time()

print(f"Batch ELT completed. SQL compute: {mid_time-start_time:.2f}s, Write result: {end_time-mid_time:.2f}s")
```

---

### ポイント

1. **バッチ読み込み**

   - Parquet を `BATCH_SIZE` ごとに読み込むことでメモリ使用量を制御
   - 巨大データ（数十 GB）でも処理可能

2. **Arrow Table + DuckDB**

   - バッチごとに Arrow Table に変換して DuckDB に登録
   - SQL で集計 → Arrow Table のまま保持

3. **ゼロコピーに近い**

   - Arrow Table を直接 SQL 処理に渡すのでメモリコピー最小化
   - 必要な場合のみ `to_pandas()` に変換

4. **ストリーム的 ELT**

   - Producer（Parquet バッチ読み込み） → Consumer（DuckDB 集計）モデル
   - 並列プロセス化も可能

---

### 改良ポイント（今後の拡張）

- `multiprocessing.Queue` で Producer/Consumer を分けて **完全並列処理**
- DuckDB の `read_parquet` を使えばさらにシンプルにバッチ集計可能
- Polars を使えば Arrow Table 上でネイティブに列指向計算可能

---

**Producer / Consumer を別プロセスに分けた完全並列ストリーム ELT** のサンプルを作ります。
Arrow Table をバッチ単位で IPC バッファとして渡し、DuckDB で集計、結果も Arrow で返す構成です。

---

### Python サンプル：並列ストリーム ELT

```python
# parallel_stream_elt.py
import pyarrow as pa
import pandas as pd
import numpy as np
import duckdb
import pyarrow.parquet as pq
import multiprocessing as mp
import time
import os

# -----------------------------
# 設定
# -----------------------------
N_ROWS = 50_000_000
BATCH_SIZE = 5_000_000
PARQUET_FILE = 'data.parquet'
RESULT_FILE = 'result_parallel.parquet'

# -----------------------------
# データ生成（Parquet）
# -----------------------------
if not os.path.exists(PARQUET_FILE):
    print("Generating Parquet data...")
    for start in range(0, N_ROWS, BATCH_SIZE):
        end = min(start + BATCH_SIZE, N_ROWS)
        df = pd.DataFrame({
            'user_id': np.arange(start, end),
            'amount': np.random.rand(end-start),
            'category': np.random.randint(0, 1000, size=end-start)
        })
        df.to_parquet(PARQUET_FILE, index=False, engine='pyarrow', append=(start>0))
        print(f"Wrote rows {start}-{end}")
    print("Parquet generated.")

# -----------------------------
# Producer: バッチ読み込みと Arrow IPC バッファ化
# -----------------------------
def producer(queue, parquet_file, batch_size):
    num_rows = pq.ParquetFile(parquet_file).metadata.num_rows
    for start in range(0, num_rows, batch_size):
        end = min(start + batch_size, num_rows)
        df = pd.read_parquet(parquet_file, columns=['user_id','amount','category'])
        table = pa.Table.from_pandas(df, preserve_index=False)
        buf = pa.ipc.serialize_table(table).to_buffer()
        queue.put(buf)
        print(f"Produced rows {start}-{end}")
    queue.put(None)  # 終了シグナル

# -----------------------------
# Consumer: Arrow バッファから DuckDB 集計
# -----------------------------
def consumer(queue, result_queue):
    con = duckdb.connect()
    intermediate_tables = []
    while True:
        buf = queue.get()
        if buf is None:
            break
        table = pa.ipc.deserialize_table(buf)
        con.register(f'batch_{len(intermediate_tables)}', table)
        intermediate_tables.append(f'batch_{len(intermediate_tables)}')
        print(f"Consumed batch {len(intermediate_tables)}")

    # 全バッチを UNION ALL で集計
    sql = " UNION ALL ".join([f"SELECT category, SUM(amount) AS total_amount FROM {t} GROUP BY category" for t in intermediate_tables])
    result = con.execute(f"SELECT category, SUM(total_amount) as total_amount FROM ({sql}) GROUP BY category").arrow()

    # Arrow IPC バッファで返す
    result_buf = pa.ipc.serialize_table(result).to_buffer()
    result_queue.put(result_buf)

# -----------------------------
# メイン: プロセス生成と実行
# -----------------------------
if __name__ == "__main__":
    queue = mp.Queue(maxsize=5)
    result_queue = mp.Queue()

    start_time = time.time()

    prod = mp.Process(target=producer, args=(queue, PARQUET_FILE, BATCH_SIZE))
    cons = mp.Process(target=consumer, args=(queue, result_queue))

    prod.start()
    cons.start()

    prod.join()
    cons.join()

    # 結果受け取り
    result_buf = result_queue.get()
    result_table = pa.ipc.deserialize_table(result_buf)

    pq.write_table(result_table, RESULT_FILE)
    end_time = time.time()

    print(f"Parallel ELT completed in {end_time-start_time:.2f}s")
    print("Result sample:")
    print(result_table.to_pandas().head())
```

---

### 特徴

1. **Producer / Consumer 分離**

   - Producer：Parquet からバッチ読み込み → Arrow IPC バッファ化 → Queue に投入
   - Consumer：Queue から Arrow バッファ受け取り → DuckDB で集計 → 結果を Arrow で返す

2. **ゼロコピーに近い**

   - Arrow Table を IPC バッファとして渡すことで、大規模データでもメモリコピー最小化

3. **ストリーム処理**

   - Queue を通してバッチ単位で処理するため、数十 GB 規模でもメモリ使用量を抑制

4. **並列処理**

   - 複数 Producer / Consumer に拡張可能
   - バックプレッシャー制御によりメモリ不足防止

---

**メモリ上の形式をそのまま共有してコピーを減らす** 。Arrow はこの用途に非常に向いています。整理します。

---

## 1. ゼロコピー処理の基本原則

- **ゼロコピー** とは、データをコピーせずに別プロセスや別言語からアクセスすること。
- 大規模データ（数 GB〜TB 級）では、コピーのコストが非常に大きいため有効。
- 条件：

  1. **列指向のメモリレイアウト**（Arrow Table）
  2. **共有メモリまたは IPC バッファ**（Arrow Buffer）
  3. **対応するライブラリが Arrow を扱えること**

---

## 2. Python 内での例（メモリ上でのゼロコピー）

```python
import pyarrow as pa
import pandas as pd
import numpy as np

# 巨大データ生成
df = pd.DataFrame({
    'a': np.random.rand(10_000_000),
    'b': np.random.rand(10_000_000)
})

# Arrow Table に変換（この時点でコピーは発生するが、以降はゼロコピー）
table = pa.Table.from_pandas(df, preserve_index=False)

# メモリ上のバッファとして取得
buf = pa.ipc.serialize_table(table).to_buffer()

# buf はバイト列として他のプロセスに渡せる
```

- 他プロセスでは `pa.ipc.deserialize_table(buf)` で Arrow Table に復元。
- DataFrame に戻す場合のみコピーが発生。Arrow Table のまま計算すればコピー不要。

---

## 3. Python ↔ R / 他言語間のゼロコピー

- Arrow の **C Data Interface / Arrow IPC** を利用。
- Python で生成した Arrow Table を R 側でそのまま扱える。
- ネットワーク経由で送信する場合も IPC バッファをそのまま送信すればコピーを最小化可能。

### Python → R（Arrow IPC）

```python
# Python
buf = pa.ipc.serialize_table(table).to_buffer()
# buf をソケットや共有メモリで R 側に渡す
```

```r
# R
library(arrow)
# buf を受信して Arrow Table に変換
tab <- arrow::read_ipc_stream(buf)
```

- データを DataFrame に変換するとコピーされるが、Arrow Table のまま処理すればコピーなし。

---

## 4. データベースとの連携

- DuckDB などは Arrow Table を直接受け入れられる。
- Python 側で Arrow Table → DuckDB へ直接登録 → SQL 処理
- 結果も Arrow Table で取得可能 → さらに別プロセスへゼロコピーで渡せる

```python
import duckdb

con = duckdb.connect()
con.register('arrow_table', table)
result = con.execute("SELECT a, SUM(b) FROM arrow_table GROUP BY a").arrow()
```

---

### 5. ポイント

1. **Arrow Table のまま計算**

   - DataFrame に変換するとコピーが発生するため、巨大データでは避ける

2. **共有メモリや IPC バッファでプロセス間通信**

   - ネットワーク越しでも Arrow IPC でバイト列を送るだけ

3. **DB 連携での高速ロード**

   - DuckDB や Polars は Arrow をネイティブに扱えるためゼロコピーが効く

---

まとめると、巨大データを扱う場合は

- **Python 内** → Arrow Table で計算
- **プロセス間 / 言語間** → Arrow IPC / C Data Interface
- **DB 連携** → Arrow Table を直接登録

が「コピーを最小化」する実践的アプローチです。

---

わかりました。では、**Python で巨大データを Arrow Table として扱い、DuckDB で SQL 処理して、別プロセスにゼロコピーで渡すサンプル** を作ります。ここでは説明のためにサイズは小さめにしていますが、原理は数 GB でも同じです。

---

```python
# zero_copy_duckdb_arrow.py
import pyarrow as pa
import pandas as pd
import numpy as np
import duckdb
import multiprocessing as mp

def generate_arrow_table(n_rows=10_000_000):
    """Generate a large DataFrame and convert to Arrow Table"""
    df = pd.DataFrame({
        'x': np.random.randint(0, 1000, size=n_rows),
        'y': np.random.rand(n_rows)
    })
    table = pa.Table.from_pandas(df, preserve_index=False)
    return table

def duckdb_process(table_buffer):
    """DuckDB process: read Arrow Table from buffer, run SQL, return Arrow Table"""
    # Deserialize Arrow Table (ゼロコピー可能な範囲で)
    table = pa.ipc.deserialize_table(table_buffer)

    # DuckDB に接続
    con = duckdb.connect()
    con.register('t', table)

    # SQL処理例：xごとのyの合計
    result = con.execute('SELECT x, SUM(y) as y_sum FROM t GROUP BY x').arrow()

    # Arrow IPC バッファにシリアライズして返す
    buf = pa.ipc.serialize_table(result).to_buffer()
    return buf

def consumer_process(buf):
    """Consumer process: read Arrow Table from buffer and use it"""
    table = pa.ipc.deserialize_table(buf)
    print("Result Table Schema:")
    print(table.schema)
    print("First 5 rows:")
    print(table.to_pandas().head())

if __name__ == "__main__":
    # メインプロセスで巨大データ生成
    table = generate_arrow_table(n_rows=5_000_000)

    # Arrow Table を IPC バッファに変換
    buf = pa.ipc.serialize_table(table).to_buffer()

    # 別プロセスで DuckDB 処理
    with mp.Pool(1) as pool:
        result_buf = pool.apply(duckdb_process, args=(buf,))

    # 別プロセスで結果を受け取り表示
    consumer_process(result_buf)
```

---

### サンプルの流れ

1. メインプロセスで巨大データを生成して Arrow Table に変換
2. Arrow Table を IPC バッファに変換（これを別プロセスに渡すことでコピーを最小化）
3. 別プロセスで DuckDB に登録 → SQL 集計
4. 結果を再び Arrow IPC バッファで返す
5. 消費側プロセスで Arrow Table として読み込み → DataFrame に変換せずに処理可能

---

### 特徴

- **ゼロコピーに近い処理**

  - Arrow Table をバッファとして渡すことで、巨大データでもコピーコストを最小化

- **プロセス間通信対応**

  - `multiprocessing` で簡単にデモ可能

- **DuckDB との組み合わせ**

  - SQL 処理も Arrow Table のまま行えるため高速

---

**Python ↔ Python 間で巨大データをゼロコピーでやり取りする例** を示します。ここでは **Arrow IPC バッファ** と **multiprocessing** を使って、プロセス間でコピーを最小化します。

---

### Python ↔ Python ゼロコピー例

```python
# zero_copy_python.py
import pyarrow as pa
import pandas as pd
import numpy as np
import multiprocessing as mp

def generate_arrow_table(n_rows=5_000_000):
    """Generate a large DataFrame and convert to Arrow Table"""
    df = pd.DataFrame({
        'x': np.random.randint(0, 1000, size=n_rows),
        'y': np.random.rand(n_rows)
    })
    table = pa.Table.from_pandas(df, preserve_index=False)
    return table

def worker_process(buf):
    """Worker process: deserialize Arrow Table, do some processing, return Arrow IPC buffer"""
    # Deserialize Arrow Table（ゼロコピー）
    table = pa.ipc.deserialize_table(buf)

    # 簡単な集計例: xごとのy合計
    import duckdb
    con = duckdb.connect()
    con.register('t', table)
    result = con.execute('SELECT x, SUM(y) as y_sum FROM t GROUP BY x').arrow()

    # 再度 Arrow IPC バッファに変換して返す
    return pa.ipc.serialize_table(result).to_buffer()

def main():
    # 巨大データ生成
    table = generate_arrow_table()

    # Arrow Table を IPC バッファに変換
    buf = pa.ipc.serialize_table(table).to_buffer()

    # プロセス間で Arrow IPC バッファを渡す
    with mp.Pool(1) as pool:
        result_buf = pool.apply(worker_process, args=(buf,))

    # メインプロセスで結果を Arrow Table として受け取り
    result_table = pa.ipc.deserialize_table(result_buf)
    print("Result Schema:")
    print(result_table.schema)
    print("First 5 rows:")
    print(result_table.to_pandas().head())

if __name__ == "__main__":
    main()
```

---

### ポイント

1. **Arrow Table を IPC バッファ化**

   - `pa.ipc.serialize_table(table).to_buffer()` でバイト列化
   - プロセス間で送信可能

2. **別プロセスで Arrow Table として処理**

   - `pa.ipc.deserialize_table(buf)` で復元
   - DataFrame に変換せずそのまま SQL や Arrow compute で計算可能

3. **結果もバッファとして返す**

   - 再び IPC バッファとして渡すことでコピー最小化
   - 必要な場合だけ `to_pandas()` で DataFrame 化

---

### 利点

- Python 内で巨大データ（数 GB）を扱っても、**コピーを最小化してプロセス間で共有可能**
- DuckDB や Polars で SQL/集計処理を直接 Arrow Table に対して行える
- Arrow IPC を経由するだけで、プロセス間通信も高速

---

では、**Python ↔ Python 間で巨大データをストリーム的にゼロコピー処理するプロデューサー・コンシューマモデル** の例を作ります。Arrow IPC バッファを使い、プロセス間でコピーを最小化しつつ、バッチ単位で処理します。

---

### Python プロデューサー・コンシューマ例

```python
# zero_copy_stream.py
import pyarrow as pa
import pandas as pd
import numpy as np
import multiprocessing as mp
import duckdb
import time

def producer(queue, n_rows=10_000_000, batch_size=1_000_000):
    """Generate Arrow Table batches and put IPC buffers into the queue"""
    for start in range(0, n_rows, batch_size):
        end = min(start + batch_size, n_rows)
        df = pd.DataFrame({
            'x': np.random.randint(0, 1000, size=end-start),
            'y': np.random.rand(end-start)
        })
        table = pa.Table.from_pandas(df, preserve_index=False)
        buf = pa.ipc.serialize_table(table).to_buffer()
        queue.put(buf)  # バッファをキューで送信（ゼロコピーに近い）
        print(f"Produced rows {start}-{end}")
    queue.put(None)  # 終了シグナル

def consumer(queue):
    """Read IPC buffers from the queue, process with DuckDB, yield results"""
    con = duckdb.connect()
    while True:
        buf = queue.get()
        if buf is None:
            break
        table = pa.ipc.deserialize_table(buf)
        con.register('t', table)
        result = con.execute('SELECT x, SUM(y) as y_sum FROM t GROUP BY x').arrow()
        print(f"Processed batch, first 5 rows:\n{result.to_pandas().head()}")

if __name__ == "__main__":
    queue = mp.Queue(maxsize=5)  # バッファキューでバックプレッシャー調整
    prod = mp.Process(target=producer, args=(queue,))
    cons = mp.Process(target=consumer, args=(queue,))

    start_time = time.time()
    prod.start()
    cons.start()
    prod.join()
    cons.join()
    print(f"Processing finished in {time.time() - start_time:.2f} seconds")
```

---

### ポイント

1. **バッチ単位でゼロコピー送信**

   - Arrow IPC バッファを `multiprocessing.Queue` に流す
   - データフレーム全体をコピーする必要なし

2. **プロセス間での高速処理**

   - Producer は大量データを生成しながら Queue に送る
   - Consumer は DuckDB で SQL 集計しつつ逐次処理

3. **バックプレッシャー管理**

   - `Queue(maxsize=5)` により、Consumer が遅い場合は Producer が一時停止

4. **スケーラブル**

   - 複数 Consumer プロセスで並列処理可能
   - バッチサイズや Queue サイズを調整してメモリ使用量を制御

---

### メリット

- Python 間で **巨大データをメモリコピーを最小化してやり取り**
- Arrow Table のまま SQL や集計処理可能
- メモリ管理が容易で、数 GB〜数十 GB 規模にも対応可能

---

**Python ↔ R で Arrow Table をゼロコピー共有する例** を示します。ここでは、Python で巨大データを作り Arrow IPC バッファとして保存し、R 側でそのまま読み込む例です。ファイル経由でもメモリ共有でも応用できます。

---

### 1. Python 側（Arrow IPC バッファ生成）

```python
# py_to_r_arrow.py
import pyarrow as pa
import pandas as pd
import numpy as np

# 巨大データ生成
df = pd.DataFrame({
    'x': np.random.randint(0, 1000, size=1_000_000),
    'y': np.random.rand(1_000_000)
})

# Arrow Table に変換
table = pa.Table.from_pandas(df, preserve_index=False)

# Arrow IPC 形式でファイルに保存
with pa.OSFile('arrow_data.arrow', 'wb') as sink:
    with pa.ipc.new_file(sink, table.schema) as writer:
        writer.write_table(table)

print("Arrow IPC file 'arrow_data.arrow' written.")
```

- この時点で **Arrow Table の列指向フォーマットがそのまま保存** されています。
- R 側で読むときも、メモリコピーを最小化可能。

---

### 2. R 側（Arrow IPC ファイルを読み込み）

```r
# r_read_arrow.R
library(arrow)

# Arrow IPC ファイルを直接読み込み
tab <- read_ipc_stream("arrow_data.arrow")

# Arrow Table のまま集計や処理が可能
tab_summary <- tab$group_by("x")$summarise(y_sum = sum(tab$y))$collect()

print(tab_summary[1:5,])
```

- `read_ipc_stream()` はファイルを **Arrow Table として直接読み込む** ため、コピーを最小化できます。
- `collect()` すると DataFrame に変換されますが、Arrow Table のまま処理する場合はコピー不要。

---

### 3. 特徴

1. **Python ↔ R 間での高速データ受け渡し**

   - Arrow IPC ファイル（あるいはメモリバッファ）で共有

2. **ゼロコピーに近い**

   - ファイルを読み込むだけで Arrow Table として扱える

3. **列指向なので集計処理が高速**

   - R でも Python でも Arrow Table のまま group_by や sum が可能

4. **巨大データでも対応可能**

   - 数 GB 規模でもバッファ単位で読み込める

---

### 4. 応用

- ファイルではなく **共有メモリ / ソケット** 経由でも同じ IPC バッファを渡せる
- DuckDB や Polars と組み合わせれば、Python で集計 → R で分析 → Python に返す、といったゼロコピーワークフローが作れる

---
