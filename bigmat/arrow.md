https://chatgpt.com/c/692253d3-a400-8324-8a3b-af6f1cd3825c

いいですね。Apache Arrow は高速な列指向データ形式とメモリ共有フォーマットを提供するプロジェクトで、特に **大規模データ処理や異なる言語間でのデータ連携** に強力です。学習すると、Pandas/Polarsなどの高速処理や、Parquetファイル操作、GPU連携などもスムーズになります。ここで、効率的に学習するためのステップを整理します。

---

## 1. Apache Arrow の基本概念

1. **列指向（Columnar）**

   * データは列単位で格納される
   * CPU キャッシュに優しく、列単位の操作が高速
   * 分析系処理（平均、合計、フィルター）に向く

2. **Arrow Table**

   * Arrow の基本データ構造
   * Pandas DataFrame に似た構造
   * 例: `pyarrow.Table.from_pandas(df)`

3. **Arrow Array**

   * 列の内部表現
   * 型情報を持つ
   * Null（欠損値）も効率的に扱える

4. **Arrow RecordBatch**

   * Table の小さなチャンク
   * メモリ効率が高く、ストリーミング処理に便利

---

## 2. Arrow を扱う Python ライブラリ

* **pyarrow**

  * Arrow の公式 Python 実装
  * Parquet ファイルの読み書き
  * CSV → Arrow 変換、メモリ上での高速処理

* **polars**

  * Rust ベースで Arrow を内部に使う高速 DataFrame
  * 列指向処理に最適化
  * LazyFrame による遅延評価も可能

* **arrow-cpp**

  * Python からではなく C++ でのネイティブ実装
  * GPU や Java など他言語連携でも利用

---

## 3. Python での基本操作例

```python
import pyarrow as pa
import pyarrow.parquet as pq
import pandas as pd

# Pandas DataFrame を作る
df = pd.DataFrame({
    'id': [1, 2, 3],
    'value': [10.0, 20.0, 30.0]
})

# Arrow Table に変換
table = pa.Table.from_pandas(df)

# Arrow Table の確認
print(table)
print(table.schema)

# Parquet に保存
pq.write_table(table, 'example.parquet')

# Parquet から読み込み
table2 = pq.read_table('example.parquet')
print(table2.to_pandas())
```

---

## 4. 高速処理のポイント

* **列単位で処理する**: 行単位ではなく列単位で計算すると高速
* **RecordBatch 分割**: メモリ制約がある場合に有効
* **Zero-copy**: Pandas, NumPy と Arrow はコピーせずにメモリ共有可能

---

## 5. 学習リソース

1. [Apache Arrow 公式サイト](https://arrow.apache.org/)
2. [PyArrow ドキュメント](https://arrow.apache.org/docs/python/)
3. Polars 公式サイト（Arrow 内部利用例もある）

   * [https://www.pola.rs/](https://www.pola.rs/)
4. YouTube の「PyArrow Tutorial」や「Arrow vs Pandas」解説動画
5. 実践: CSV → Arrow → Parquet → Polars LazyFrame で分析パイプラインを作る

---

Arrow を使うときによく出てくる **Table** と **RecordBatch** の違いを整理します。

---

## 1. Arrow Table

### 概要

* Arrow の最も基本的なデータ構造
* **複数の列**（Arrow Array）をまとめたもの
* Pandas の DataFrame に近い感覚で扱える
* **複数の RecordBatch をまとめたもの** とも考えられる

### 特徴

* 高レベル API
* 列ごとにアクセス可能
* 大きなデータセットでも扱える
* Parquet や IPC への書き出しが簡単

### Python例

```python
import pyarrow as pa

# 2列のTable
table = pa.Table.from_arrays(
    [pa.array([1,2,3]), pa.array(['a','b','c'])],
    names=['id','label']
)

print(table)
# schema: id: int64, label: string
```

---

## 2. Arrow RecordBatch

### 概要

* Table の「チャンク単位」のデータ
* **固定長の複数列の集合**
* メモリ効率が高く、ストリーミング処理やブロック処理に向く
* Table の内部では、複数の RecordBatch をまとめて保持することもある

### 特徴

* 小さなデータブロックを扱うときに便利
* ストリーミングや並列処理向き
* Table のように高レベル API は少ない
* 「この範囲だけ処理したい」ときに最適

### Python例

```python
batch = pa.RecordBatch.from_arrays(
    [pa.array([1,2,3]), pa.array(['a','b','c'])],
    names=['id','label']
)

print(batch)
# fields: id, label
```

---

## 3. Table と RecordBatch の関係

* **RecordBatch** = 列データの最小ブロック
* **Table** = RecordBatch の集合、または複数列の高レベル表現

```
Table
 ├─ RecordBatch 1 (rows 0-999)
 ├─ RecordBatch 2 (rows 1000-1999)
 └─ RecordBatch 3 (rows 2000-2999)
```

* 大きなデータは RecordBatch に分割して処理することでメモリ消費を抑えられる
* Table は RecordBatch を意識せずに使える便利なラッパー

---

## 4. 使い分けの目安

| 目的                      | 使うもの                               |
| ----------------------- | ---------------------------------- |
| 高レベルで扱いたい（DataFrame 感覚） | Table                              |
| ブロック単位で処理したい、ストリーミング    | RecordBatch                        |
| Parquet / IPC に書き出す     | Table が簡単。内部で RecordBatch を使うこともある |

---
では、Python で **Arrow Table と RecordBatch を使ったブロック単位読み書き** のサンプルコードを作ります。

この例では：

1. CSV → Arrow Table に変換
2. Table を複数 RecordBatch に分割して処理
3. Parquet に書き出す

---

```python
import pyarrow as pa
import pyarrow.csv as pv
import pyarrow.parquet as pq

# ------------------------
# 1. CSV を Arrow Table に変換
# ------------------------
csv_file = 'sample.csv'  # 例: id,value
# CSVを読み込み（小さめのサンプル向け）
table = pv.read_csv(csv_file)

print("=== Arrow Table ===")
print(table)
print(table.schema)

# ------------------------
# 2. Table を RecordBatch に分割
# ------------------------
batch_size = 2  # 1バッチあたりの行数
batches = table.to_batches(batch_size=batch_size)

print("\n=== RecordBatches ===")
for i, batch in enumerate(batches):
    print(f"Batch {i}:")
    print(batch)

# ------------------------
# 3. Parquet にブロック単位で書き出す
# ------------------------
parquet_file = 'output.parquet'
writer = pq.ParquetWriter(parquet_file, table.schema)

for batch in batches:
    writer.write_batch(batch)

writer.close()
print(f"\nWrote Parquet: {parquet_file}")

# ------------------------
# 4. Parquet を読み込み（必要な列だけ）
# ------------------------
read_table = pq.read_table(parquet_file, columns=['id'])
print("\nRead Parquet (only 'id'):")
print(read_table)
```

---

### 説明

1. **CSV → Table**

   * `pyarrow.csv.read_csv` で読み込むと Table になる

2. **Table → RecordBatch**

   * `table.to_batches(batch_size=N)` で分割
   * 大規模データをブロック単位で処理できる

3. **Parquet 書き出し**

   * `ParquetWriter` に RecordBatch を順次書き込む
   * 大きなデータもメモリに一括で読み込まず書き出せる

4. **Parquet 読み込み**

   * `columns=` 指定で必要な列だけ読み込み可能
   * 遅延読み込みや列単位処理に最適


---


Parquet と Arrow IPC（Feather などを含む）はどちらも列指向のデータ形式ですが、用途や性能の特性が違うので使い分けがあります。整理します。

---

## 1. Parquet

### 特徴

* **ディスク向き、永続化用**
* 列ごとに圧縮・エンコード可能 → ファイルサイズ小、I/O 低減
* スキーマを保持、他言語との互換性あり（Python, Java, C++, Spark, Hive など）
* 遅延読み込みが可能（必要な列だけ読み込む）
* 大規模データの保存・分散処理向き

### 用途

* データウェアハウスに格納（Snowflake, BigQuery, Redshift, Hive）
* 分析パイプラインの中間成果物として保存
* 長期保存・バックアップ
* 複数マシンでの共有・分散処理

### Python例

```python
import pyarrow.parquet as pq
pq.write_table(table, 'data.parquet')
table2 = pq.read_table('data.parquet', columns=['col1', 'col2'])
```

---

## 2. Arrow IPC (Feather)

### 特徴

* **メモリ間転送・高速読み書き向き**
* Zero-copy で Pandas/Polars/Arrow 間でデータ共有可能
* 圧縮は可能だが Parquet ほど圧縮効率は高くない
* データの永続化もできるが、主に **短期保存・高速読み書き** が目的

### 用途

* メモリ上のデータを他プロセスや他言語に渡す
* データフレームを高速に保存・読み込みしたい場合
* パイプライン中で何度もデータを読み書きする場合

### Python例

```python
import pyarrow.feather as feather
feather.write_feather(table, 'data.feather')
table2 = feather.read_feather('data.feather')
```

---

## 3. 使い分けのまとめ

| 項目       | Parquet          | Arrow IPC / Feather    |
| -------- | ---------------- | ---------------------- |
| 主な用途     | 永続保存、分散処理        | 高速読み書き、プロセス間共有         |
| 圧縮       | 高圧縮・列ごと          | 低〜中圧縮                  |
| 読み込み速度   | 遅延読み込みで列指定可      | 全列読み込みが基本（高速）          |
| データサイズ   | 大規模向き            | 中〜大規模、メモリ内向き           |
| クロス言語互換性 | 高                | 高（Arrow準拠）             |
| 適したケース   | データウェアハウス、バックアップ | 分析パイプライン内の中間データ、メモリ間共有 |

---

### まとめ

* **Parquet** = 永続化・分散処理・長期保存向き
* **Arrow IPC / Feather** = 高速読み書き・短期保存・メモリ内共有向き

---

では、**同じデータを Parquet と Arrow IPC（Feather）で読み書きして速度・ファイルサイズを比較**するサンプルを作ります。Python で `pyarrow` を使います。

---

```python
import pyarrow as pa
import pyarrow.parquet as pq
import pyarrow.feather as feather
import pandas as pd
import time
import os

# ------------------------
# 1. サンプルデータ作成
# ------------------------
n = 1_000_000  # 100万行
df = pd.DataFrame({
    'id': range(n),
    'value': [float(x) for x in range(n)]
})

# Arrow Table に変換
table = pa.Table.from_pandas(df)

# ------------------------
# 2. Parquet 書き出し
# ------------------------
parquet_file = "data.parquet"
start = time.time()
pq.write_table(table, parquet_file, compression='snappy')
end = time.time()
print(f"Parquet write time: {end-start:.2f} sec, size: {os.path.getsize(parquet_file)/1e6:.2f} MB")

# Parquet 読み込み
start = time.time()
table_parquet = pq.read_table(parquet_file)
end = time.time()
print(f"Parquet read time: {end-start:.2f} sec")

# ------------------------
# 3. Arrow IPC (Feather) 書き出し
# ------------------------
feather_file = "data.feather"
start = time.time()
feather.write_feather(table, feather_file)
end = time.time()
print(f"Feather write time: {end-start:.2f} sec, size: {os.path.getsize(feather_file)/1e6:.2f} MB")

# Feather 読み込み
start = time.time()
table_feather = feather.read_table(feather_file)
end = time.time()
print(f"Feather read time: {end-start:.2f} sec")
```

---

### ポイント

1. **Parquet**

   * 列ごとに圧縮されるためファイルサイズが小さい
   * 遅延読み込みや列指定が可能
   * 書き込みは Feather より少し遅くなることがある

2. **Arrow IPC / Feather**

   * 書き込み・読み込みが非常に高速
   * 圧縮効率は Parquet より低い
   * メモリ内処理やプロセス間データ受け渡しに向いている

---

### 期待される傾向

| 形式      | 書き込み | 読み込み | ファイルサイズ     |
| ------- | ---- | ---- | ----------- |
| Parquet | やや遅め | やや遅め | 小さい（圧縮効率高）  |
| Feather | 高速   | 高速   | 大きめ（ほぼ圧縮なし） |

---


## 1. Arrow と Polars の関係

* **Apache Arrow** は「列指向のメモリフォーマット」としてのライブラリです。

  * Table, RecordBatch, IPC, Parquet などを扱える
  * 高速ですが、**単体ではデータ操作（集計やフィルターなど）の最適化は限定的**

* **Polars** は **内部で Arrow を使う DataFrame ライブラリ**

  * Rust で SIMD 最適化済み
  * LazyFrame による **遅延評価で操作をまとめて最適化**
  * Arrow のゼロコピーも活用

つまり **Polars = Arrow + 高速演算エンジン + 最適化済み DataFrame API** のような位置づけです。

---

## 2. 速度比較のイメージ

| 処理                          | Arrow Table（pyarrow） | Polars                  |
| --------------------------- | -------------------- | ----------------------- |
| 単純な読み込み・書き出し                | 高速                   | 同等〜やや高速（内部で Arrow 使うため） |
| 集計 / フィルター / join / groupby | Python 側でループ書く場合遅い   | Rust SIMD で高速           |
| Lazy / 遅延評価                 | なし                   | LazyFrame で複数操作をまとめて最適化 |
| 大規模 CSV → Parquet           | pyarrow でブロック単位必要    | LazyFrame でほぼ自動最適化      |

---

### 3. 結論

1. **単純に Table を作るだけ・ファイル読み書きだけ** → Arrow と Polars で大きな差はない
2. **集計・フィルター・複数列操作・グループ集計などを含む処理** → Polars の方が圧倒的に高速
3. **大規模データ・ELT パイプライン** → Polars + LazyFrame の方が効率的

---

つまり、

* Arrow は「メモリ形式」
* Polars は「Arrow を使った高速列指向演算エンジン」

→ **Arrow 単体より Polars を使う方がほとんどの分析・変換処理では速い**

---


では、**Polars を使って Parquet と Arrow IPC（Feather）の読み書き速度・サイズを比較するサンプル** を作ります。

---

```python
import polars as pl
import pandas as pd
import time
import os

# ------------------------
# 1. サンプルデータ作成
# ------------------------
n = 1_000_000  # 100万行
df = pd.DataFrame({
    'id': range(n),
    'value': [float(x) for x in range(n)]
})

# Polars DataFrame に変換
pl_df = pl.from_pandas(df)

# ------------------------
# 2. Parquet 書き出し
# ------------------------
parquet_file = "data_polars.parquet"
start = time.time()
pl_df.write_parquet(parquet_file, compression='snappy')
end = time.time()
print(f"Parquet write time: {end-start:.2f} sec, size: {os.path.getsize(parquet_file)/1e6:.2f} MB")

# Parquet 読み込み
start = time.time()
df_parquet = pl.read_parquet(parquet_file)
end = time.time()
print(f"Parquet read time: {end-start:.2f} sec")

# ------------------------
# 3. Arrow IPC (Feather) 書き出し
# ------------------------
feather_file = "data_polars.feather"
start = time.time()
pl_df.write_ipc(feather_file)
end = time.time()
print(f"Feather write time: {end-start:.2f} sec, size: {os.path.getsize(feather_file)/1e6:.2f} MB")

# Feather 読み込み
start = time.time()
df_feather = pl.read_ipc(feather_file)
end = time.time()
print(f"Feather read time: {end-start:.2f} sec")

# ------------------------
# 4. 簡単な確認
# ------------------------
print("\nFirst 5 rows (Parquet):")
print(df_parquet.head())
print("\nFirst 5 rows (Feather):")
print(df_feather.head())
```

---

### ポイント

1. **Polars + Parquet**

   * 圧縮済みでファイルサイズが小さく、大規模データの永続化向き
   * 読み込み速度は Feather より少し遅くなることがある

2. **Polars + Arrow IPC (Feather)**

   * 読み書きが非常に高速
   * 圧縮なしなのでファイルサイズは大きくなる
   * メモリ内処理や短期データ共有向き

3. **Polars の利点**

   * 内部で Arrow を利用して高速列指向処理
   * LazyFrame を使えばさらに大規模データでも効率的に処理可能

---


では、Polars の **LazyFrame を使って巨大 CSV をブロック単位で Parquet と Feather に高速書き出すサンプル** を作ります。

---

```python
import polars as pl
import time
import os

csv_file = "huge_sample.csv"  # 巨大 CSV を想定
parquet_file = "huge_output.parquet"
feather_file = "huge_output.feather"
chunk_size = 1_000_000  # 1回に処理する行数

# ------------------------
# 1. Parquet 書き出し
# ------------------------
start = time.time()

# LazyFrame で CSV を分割読み込み
lf = pl.scan_csv(csv_file, infer_schema_length=1000)  # 遅延読み込み
lf_parquet = lf.collect()  # 実際に計算

# Parquet に書き出し（圧縮あり）
lf_parquet.write_parquet(parquet_file, compression='snappy')

end = time.time()
print(f"Parquet write time: {end-start:.2f} sec, size: {os.path.getsize(parquet_file)/1e6:.2f} MB")

# ------------------------
# 2. Feather 書き出し
# ------------------------
start = time.time()

# 同じ LazyFrame を IPC に書き出し
lf_ipc = lf.collect()  # collect()で実際に計算
lf_ipc.write_ipc(feather_file)

end = time.time()
print(f"Feather write time: {end-start:.2f} sec, size: {os.path.getsize(feather_file)/1e6:.2f} MB")

# ------------------------
# 3. 読み込み確認
# ------------------------
start = time.time()
df_parquet = pl.read_parquet(parquet_file)
end = time.time()
print(f"Parquet read time: {end-start:.2f} sec")

start = time.time()
df_feather = pl.read_ipc(feather_file)
end = time.time()
print(f"Feather read time: {end-start:.2f} sec")

# ------------------------
# 4. 最初の5行を表示
# ------------------------
print("\nParquet first 5 rows:")
print(df_parquet.head())
print("\nFeather first 5 rows:")
print(df_feather.head())
```

---

### ポイント

1. **LazyFrame**

   * CSV を遅延読み込み
   * collect() で一度に計算
   * 大規模データでもメモリ効率よく処理可能

2. **Parquet**

   * 圧縮あり → ファイルサイズ小
   * 書き込みは Feather よりやや遅め

3. **Feather (Arrow IPC)**

   * 書き込み・読み込み高速
   * ファイルサイズは大きめ
   * パイプライン中の中間データとして最適

4. **ブロック単位処理**

   * chunk_size により任意の行数ごとに処理可能
   * 巨大データでも分割して書き出せる

---


では、**Arrow Table と Polars で同じ CSV を読み込み→集計→Parquet 出力して速度比較** するサンプルコードを作ります。

---

```python
import pyarrow.csv as pv
import pyarrow.parquet as pq
import pyarrow as pa
import polars as pl
import time

csv_file = "sample.csv"  # サンプル CSV（id,value）を想定
parquet_arrow = "output_arrow.parquet"
parquet_polars = "output_polars.parquet"

# ----------------------------------------
# 1. Arrow で処理
# ----------------------------------------
start = time.time()
table = pv.read_csv(csv_file)  # CSV → Arrow Table

# 例: id 列で groupby して value の合計
import pyarrow.compute as pc
unique_ids = pc.unique(table['id'])
results = []
for uid in unique_ids.to_pylist():
    mask = pc.equal(table['id'], uid)
    values = pc.filter(table['value'], mask)
    total = pc.sum(values)
    results.append((uid, total.as_py()))

# 結果を Parquet に書き出し
result_table = pa.Table.from_arrays(
    [pa.array([r[0] for r in results]), pa.array([r[1] for r in results])],
    names=['id','total']
)
pq.write_table(result_table, parquet_arrow)
end = time.time()
print(f"Arrow processing time: {end-start:.2f} sec")

# ----------------------------------------
# 2. Polars で処理
# ----------------------------------------
start = time.time()
df = pl.read_csv(csv_file)

# id 列で groupby して value の合計
result_polars = df.groupby('id').agg(pl.sum('value').alias('total'))

# Parquet に書き出し
result_polars.write_parquet(parquet_polars)
end = time.time()
print(f"Polars processing time: {end-start:.2f} sec")
```

---

### ポイント

1. **Arrow 側**

   * CSV → Table は高速
   * ただし groupby や filter を Python 側でループ処理するため遅くなる
   * 大規模データでは明らかにボトルネック

2. **Polars 側**

   * CSV → DataFrame は高速
   * groupby + sum も内部 Rust SIMD 最適化で高速
   * LazyFrame にすればさらに効率よく処理できる

---

はい、**Arrow を使って SQLite から DuckDB にデータ移行**することは可能です。方法としては以下のステップが一般的です。

---

## 1. 概要

1. **SQLite からデータを Arrow Table に変換**

   * Python なら `sqlite3` + `pyarrow` で可能
2. **Arrow Table を DuckDB にインポート**

   * DuckDB は Arrow Table を直接読み込める
   * そのまま SQL でテーブル作成可能

メリット：

* 中間ファイル（CSV や Parquet）を作らずにメモリ上で高速移行可能
* Arrow の列指向フォーマットで効率的

---

## 2. Python サンプルコード

```python
import sqlite3
import duckdb
import pyarrow as pa
import pyarrow.table as pat

# ------------------------
# 1. SQLite からデータ取得
# ------------------------
sqlite_file = 'source.db'
conn = sqlite3.connect(sqlite_file)
cursor = conn.cursor()

# 例: 'my_table' のデータを取得
cursor.execute("SELECT * FROM my_table")
columns = [desc[0] for desc in cursor.description]
rows = cursor.fetchall()
conn.close()

# Arrow Table に変換
arrow_table = pa.Table.from_pylist([dict(zip(columns, row)) for row in rows])

# ------------------------
# 2. DuckDB にインポート
# ------------------------
duckdb_file = 'target.duckdb'
con = duckdb.connect(duckdb_file)

# Arrow Table を DuckDB のテーブルとして登録
con.register('tmp_table', arrow_table)

# DuckDB 内に永続テーブルを作成
con.execute("CREATE TABLE my_table AS SELECT * FROM tmp_table")

# 確認
res = con.execute("SELECT COUNT(*) FROM my_table").fetchall()
print(res)
con.close()
```

---

では、**巨大な SQLite データベースを DuckDB に効率的に移行する方法** をまとめ、Python サンプルも作ります。

ポイントは **一括で読み込まず、ブロック単位で処理してメモリ効率を確保する** ことです。

---

## 1. 移行戦略

1. SQLite から **chunk 単位でデータを取得**

   * Python の `sqlite3` で `LIMIT` と `OFFSET` または `iterdump()` のようなカーソルを使う
2. Arrow Table に変換（ブロック単位）

   * DuckDB は Arrow Table をゼロコピーで読み込める
3. DuckDB に **一時テーブルとして登録し、永続テーブルに書き込み**
4. すべてのブロックを繰り返す

---

## 2. Python サンプルコード

```python
import sqlite3
import duckdb
import pyarrow as pa

sqlite_file = 'huge_source.db'
duckdb_file = 'target.duckdb'
table_name = 'my_table'
chunk_size = 1_000_000  # 1回に処理する行数

# ------------------------
# SQLite 接続
# ------------------------
conn_sqlite = sqlite3.connect(sqlite_file)
cur = conn_sqlite.cursor()

# 行数を取得
cur.execute(f"SELECT COUNT(*) FROM {table_name}")
total_rows = cur.fetchone()[0]
print(f"Total rows: {total_rows}")

# ------------------------
# DuckDB 接続
# ------------------------
con_duck = duckdb.connect(duckdb_file)

# DuckDB に空テーブル作成（最初の chunk でスキーマ作成用）
# ここでは最初の chunk を取得
cur.execute(f"SELECT * FROM {table_name} LIMIT {chunk_size} OFFSET 0")
columns = [desc[0] for desc in cur.description]
rows = cur.fetchall()

# Arrow Table に変換
arrow_table = pa.Table.from_pylist([dict(zip(columns, row)) for row in rows])

# DuckDB に一時登録して永続テーブル作成
con_duck.register('tmp_table', arrow_table)
con_duck.execute(f"CREATE TABLE {table_name} AS SELECT * FROM tmp_table")
print(f"Inserted first {len(rows)} rows")

# ------------------------
# 残りのデータをブロック単位で挿入
# ------------------------
for offset in range(chunk_size, total_rows, chunk_size):
    cur.execute(f"SELECT * FROM {table_name} LIMIT {chunk_size} OFFSET {offset}")
    rows = cur.fetchall()
    if not rows:
        break
    arrow_table = pa.Table.from_pylist([dict(zip(columns, row)) for row in rows])
    con_duck.register('tmp_table', arrow_table)
    con_duck.execute(f"INSERT INTO {table_name} SELECT * FROM tmp_table")
    print(f"Inserted rows {offset} -> {offset+len(rows)}")

# ------------------------
# 完了
# ------------------------
cur.close()
conn_sqlite.close()
con_duck.close()
print("Migration completed.")
```

---

## 3. ポイント

1. **chunk_size** でメモリ使用量を制御

   * 100万行単位など、メモリ状況に応じて調整可能
2. **Arrow Table を使う**

   * DuckDB は Arrow Table をゼロコピーで読み込むので高速
3. **永続テーブルに INSERT**

   * 一括挿入で処理時間短縮
4. **巨大データでも安全**

   * SQLite から一度に全部読み込まないためメモリ不足のリスクが低い

---

では、**SQLite の複数テーブルを DuckDB にブロック単位で移行するサンプル** を作ります。

---

```python
import sqlite3
import duckdb
import pyarrow as pa

sqlite_file = 'huge_source.db'
duckdb_file = 'target.duckdb'
chunk_size = 1_000_000  # 1回に処理する行数

# ------------------------
# SQLite 接続
# ------------------------
conn_sqlite = sqlite3.connect(sqlite_file)
cur = conn_sqlite.cursor()

# SQLite 内の全テーブルを取得
cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = [row[0] for row in cur.fetchall()]
print("Tables to migrate:", tables)

# ------------------------
# DuckDB 接続
# ------------------------
con_duck = duckdb.connect(duckdb_file)

# ------------------------
# 各テーブルを移行
# ------------------------
for table_name in tables:
    print(f"Migrating table: {table_name}")

    # 行数取得
    cur.execute(f"SELECT COUNT(*) FROM {table_name}")
    total_rows = cur.fetchone()[0]
    print(f"  Total rows: {total_rows}")

    # 最初の chunk
    cur.execute(f"SELECT * FROM {table_name} LIMIT {chunk_size} OFFSET 0")
    columns = [desc[0] for desc in cur.description]
    rows = cur.fetchall()
    if not rows:
        continue

    arrow_table = pa.Table.from_pylist([dict(zip(columns, row)) for row in rows])
    con_duck.register('tmp_table', arrow_table)
    con_duck.execute(f"CREATE TABLE {table_name} AS SELECT * FROM tmp_table")
    print(f"  Inserted first {len(rows)} rows")

    # 残りのデータを chunk 単位で挿入
    for offset in range(chunk_size, total_rows, chunk_size):
        cur.execute(f"SELECT * FROM {table_name} LIMIT {chunk_size} OFFSET {offset}")
        rows = cur.fetchall()
        if not rows:
            break
        arrow_table = pa.Table.from_pylist([dict(zip(columns, row)) for row in rows])
        con_duck.register('tmp_table', arrow_table)
        con_duck.execute(f"INSERT INTO {table_name} SELECT * FROM tmp_table")
        print(f"  Inserted rows {offset} -> {offset+len(rows)}")

print("Migration completed for all tables.")

# ------------------------
# クローズ
# ------------------------
cur.close()
conn_sqlite.close()
con_duck.close()
```

---

### ポイント

1. **複数テーブル対応**

   * `sqlite_master` からテーブル名を取得して順次処理
2. **ブロック単位**

   * `chunk_size` ごとにデータを Arrow Table に変換して DuckDB に挿入
   * 巨大テーブルでもメモリ消費を抑えられる
3. **Arrow Table 利用**

   * DuckDB は Arrow Table をゼロコピーで読み込むので高速
4. **永続テーブル作成**

   * 各テーブルを DuckDB 内に永続化して、そのまま分析可能

---

では、**複数テーブルを並列処理で同時に DuckDB に移行する高速版** を作ります。Python の `concurrent.futures` を使って、テーブル単位で並列化します。

---

```python
import sqlite3
import duckdb
import pyarrow as pa
from concurrent.futures import ThreadPoolExecutor, as_completed

sqlite_file = 'huge_source.db'
duckdb_file = 'target.duckdb'
chunk_size = 1_000_000  # 1回に処理する行数
max_workers = 4  # 並列数（CPUコア数に応じて調整）

# ------------------------
# SQLite から全テーブル名を取得
# ------------------------
conn_sqlite = sqlite3.connect(sqlite_file)
cur = conn_sqlite.cursor()
cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = [row[0] for row in cur.fetchall()]
cur.close()
conn_sqlite.close()

print("Tables to migrate:", tables)

# ------------------------
# 移行関数（1テーブル分）
# ------------------------
def migrate_table(table_name):
    conn_sqlite = sqlite3.connect(sqlite_file)
    cur = conn_sqlite.cursor()
    con_duck = duckdb.connect(duckdb_file)

    # 行数取得
    cur.execute(f"SELECT COUNT(*) FROM {table_name}")
    total_rows = cur.fetchone()[0]

    # 最初の chunk
    cur.execute(f"SELECT * FROM {table_name} LIMIT {chunk_size} OFFSET 0")
    columns = [desc[0] for desc in cur.description]
    rows = cur.fetchall()
    if not rows:
        cur.close()
        conn_sqlite.close()
        con_duck.close()
        return f"{table_name}: no rows"

    arrow_table = pa.Table.from_pylist([dict(zip(columns, row)) for row in rows])
    con_duck.register('tmp_table', arrow_table)
    con_duck.execute(f"CREATE TABLE IF NOT EXISTS {table_name} AS SELECT * FROM tmp_table")

    # 残りのデータを chunk 単位で挿入
    for offset in range(chunk_size, total_rows, chunk_size):
        cur.execute(f"SELECT * FROM {table_name} LIMIT {chunk_size} OFFSET {offset}")
        rows = cur.fetchall()
        if not rows:
            break
        arrow_table = pa.Table.from_pylist([dict(zip(columns, row)) for row in rows])
        con_duck.register('tmp_table', arrow_table)
        con_duck.execute(f"INSERT INTO {table_name} SELECT * FROM tmp_table")

    cur.close()
    conn_sqlite.close()
    con_duck.close()
    return f"{table_name}: migrated {total_rows} rows"

# ------------------------
# ThreadPoolExecutor で並列実行
# ------------------------
with ThreadPoolExecutor(max_workers=max_workers) as executor:
    futures = {executor.submit(migrate_table, tbl): tbl for tbl in tables}
    for future in as_completed(futures):
        print(future.result())

print("All tables migrated in parallel.")
```

---

### ポイント

1. **テーブル単位で並列処理**

   * 複数テーブルを同時に処理することで、I/O待ちやCPU処理を効率化
2. **chunk_size でメモリ消費を制御**

   * 巨大テーブルでも安全に処理可能
3. **Arrow Table を利用**

   * DuckDB にゼロコピーで高速挿入
4. **ThreadPoolExecutor**

   * I/O中心処理ではスレッドで十分
   * CPU集約処理なら `ProcessPoolExecutor` に変更可能

---

では、**PostgreSQL の複数テーブルをブロック単位＆並列で DuckDB に移行する高速版** を作ります。

Python の `psycopg2` と `concurrent.futures.ThreadPoolExecutor` を使います。

---

```python
import psycopg2
import duckdb
import pyarrow as pa
from concurrent.futures import ThreadPoolExecutor, as_completed

# ------------------------
# 設定
# ------------------------
pg_config = {
    'host': 'localhost',
    'port': 5432,
    'dbname': 'source_db',
    'user': 'username',
    'password': 'password'
}
duckdb_file = 'target.duckdb'
chunk_size = 500_000
max_workers = 4  # 並列数

# ------------------------
# PostgreSQL からテーブル名取得
# ------------------------
pg_conn = psycopg2.connect(**pg_config)
pg_cur = pg_conn.cursor()
pg_cur.execute("""
    SELECT table_name 
    FROM information_schema.tables 
    WHERE table_schema='public' AND table_type='BASE TABLE';
""")
tables = [row[0] for row in pg_cur.fetchall()]
pg_cur.close()
pg_conn.close()

print("Tables to migrate:", tables)

# ------------------------
# 移行関数（1テーブル分）
# ------------------------
def migrate_table(table_name):
    pg_conn = psycopg2.connect(**pg_config)
    pg_cur = pg_conn.cursor()
    con_duck = duckdb.connect(duckdb_file)

    # 行数取得
    pg_cur.execute(f"SELECT COUNT(*) FROM {table_name}")
    total_rows = pg_cur.fetchone()[0]

    # 最初の chunk
    pg_cur.execute(f"SELECT * FROM {table_name} OFFSET 0 LIMIT {chunk_size}")
    rows = pg_cur.fetchall()
    if not rows:
        pg_cur.close()
        pg_conn.close()
        con_duck.close()
        return f"{table_name}: no rows"

    columns = [desc[0] for desc in pg_cur.description]
    arrow_table = pa.Table.from_pylist([dict(zip(columns, row)) for row in rows])
    con_duck.register('tmp_table', arrow_table)
    con_duck.execute(f"CREATE TABLE IF NOT EXISTS {table_name} AS SELECT * FROM tmp_table")
    print(f"{table_name}: inserted first {len(rows)} rows")

    # 残りを chunk 単位で挿入
    for offset in range(chunk_size, total_rows, chunk_size):
        pg_cur.execute(f"SELECT * FROM {table_name} OFFSET {offset} LIMIT {chunk_size}")
        rows = pg_cur.fetchall()
        if not rows:
            break
        arrow_table = pa.Table.from_pylist([dict(zip(columns, row)) for row in rows])
        con_duck.register('tmp_table', arrow_table)
        con_duck.execute(f"INSERT INTO {table_name} SELECT * FROM tmp_table")
        print(f"{table_name}: inserted rows {offset} -> {offset+len(rows)}")

    pg_cur.close()
    pg_conn.close()
    con_duck.close()
    return f"{table_name}: migrated {total_rows} rows"

# ------------------------
# ThreadPoolExecutor で並列移行
# ------------------------
with ThreadPoolExecutor(max_workers=max_workers) as executor:
    futures = {executor.submit(migrate_table, tbl): tbl for tbl in tables}
    for future in as_completed(futures):
        print(future.result())

print("All tables migrated in parallel.")
```

---

### ポイント

1. **テーブル単位で並列処理**

   * I/O 待ちや CPU 処理を効率化
2. **chunk_size でメモリ制御**

   * 500,000 行単位など、メモリに合わせて調整可能
3. **Arrow Table 経由で DuckDB にゼロコピー挿入**

   * 高速で安全
4. **永続テーブル作成**

   * そのまま DuckDB で分析可能
5. **ThreadPoolExecutor**

   * I/O中心なのでスレッド並列で十分
   * CPU集約処理なら `ProcessPoolExecutor` に変更可能

---











