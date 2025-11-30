https://chatgpt.com/c/692253d3-a400-8324-8a3b-af6f1cd3825c

Apache Arrow は高速な列指向データ形式とメモリ共有フォーマットを提供するプロジェクトで、特に **大規模データ処理や異なる言語間でのデータ連携** に強力です。

## 1. Apache Arrow の基本概念

1. **列指向（Columnar）**

   - データは列単位で格納される
   - CPU キャッシュに優しく、列単位の操作が高速
   - 分析系処理（平均、合計、フィルター）に向く

2. **Arrow Table**

   - Arrow の基本データ構造
   - Pandas DataFrame に似た構造
   - 例: `pyarrow.Table.from_pandas(df)`

3. **Arrow Array**

   - 列の内部表現
   - 型情報を持つ
   - Null（欠損値）も効率的に扱える

4. **Arrow RecordBatch**

   - Table の小さなチャンク
   - メモリ効率が高く、ストリーミング処理に便利

---

## 2. Arrow を扱う Python ライブラリ

- **pyarrow**

  - Arrow の公式 Python 実装
  - Parquet ファイルの読み書き
  - CSV → Arrow 変換、メモリ上での高速処理

- **polars**

  - Rust ベースで Arrow を内部に使う高速 DataFrame
  - 列指向処理に最適化
  - LazyFrame による遅延評価も可能

- **arrow-cpp**

  - Python からではなく C++ でのネイティブ実装
  - GPU や Java など他言語連携でも利用

---

```bash
sudo apt install -y python-venv python-full
python3 -m venv venv0
cd venv0
. bin/activate
pip install pyarrow

mkdir arrow
cd arrow
```

```python
import pyarrow as pa
import pyarrow.parquet as pq

#import pandas as pd
# # Pandas DataFrame を作る
# df = pd.DataFrame({
#     'id': [1, 2, 3],
#     'value': [10.0, 20.0, 30.0]
# })

# # Arrow Table に変換
# table = pa.Table.from_pandas(df)

arr1=pa.array([1,2,3])
arr2=pa.array([10.0,20.0,30.0])

table1=pa.table({'id':arr1, 'value':arr2})

# Arrow Table の確認
print(table1.schema)
print(table1)

# Parquet に保存
pq.write_table(table1, 'example.parquet')

# Parquet から読み込み
table2 = pq.read_table('example.parquet')

print(table2)
print(table2.to_pandas())
```

---

## 4. 高速処理のポイント

- **列単位で処理する**: 行単位ではなく列単位で計算すると高速
- **RecordBatch 分割**: メモリ制約がある場合に有効
- **Zero-copy**: Pandas, NumPy と Arrow はコピーせずにメモリ共有可能

---

Arrow を使うときによく出てくる **Table** と **RecordBatch** の違いを整理します。

## 1. Arrow Table

### 概要

- Arrow の最も基本的なデータ構造
- **複数の列**（Arrow Array）をまとめたもの
- Pandas の DataFrame に近い感覚で扱える
- **複数の RecordBatch をまとめたもの** とも考えられる

### 特徴

- 高レベル API
- 列ごとにアクセス可能
- 大きなデータセットでも扱える
- Parquet や IPC への書き出しが簡単

---

## 2. Arrow RecordBatch

### 概要

- Table の「チャンク単位」のデータ
- **固定長の複数列の集合**
- メモリ効率が高く、ストリーミング処理やブロック処理に向く
- Table の内部では、複数の RecordBatch をまとめて保持することもある

### 特徴

- 小さなデータブロックを扱うときに便利
- ストリーミングや並列処理向き
- Table のように高レベル API は少ない
- 「この範囲だけ処理したい」ときに最適

```python
import pyarrow as pa

arr1=pa.array([1,2,3])
arr2=pa.array(['a','b','c'])
arr3=pa.array([1.1,2.2,3.3])

table=pa.table({'id':arr1, 'label':arr2, 'val':arr3})

print(table)

batch1 = pa.RecordBatch.from_pydict({
   'id':arr1, 'label':arr2, 'val':arr3
,1})

print(batch1)

batch3 = pa.RecordBatch.from_pydict({
   'id':arr1, 'label':arr2, 'val':arr3
,3})

print(batch3)
```

---

## 3. Table と RecordBatch の関係

- **RecordBatch** = 列データの最小ブロック
- **Table** = RecordBatch の集合、または複数列の高レベル表現

```
Table
 ├─ RecordBatch 1 (rows 0-999)
 ├─ RecordBatch 2 (rows 1000-1999)
 └─ RecordBatch 3 (rows 2000-2999)
```

- 大きなデータは RecordBatch に分割して処理することでメモリ消費を抑えられる
- Table は RecordBatch を意識せずに使える便利なラッパー

---

## 4. 使い分けの目安

| 目的                                     | 使うもの                                          |
| ---------------------------------------- | ------------------------------------------------- |
| 高レベルで扱いたい（DataFrame 感覚）     | Table                                             |
| ブロック単位で処理したい、ストリーミング | RecordBatch                                       |
| Parquet / IPC に書き出す                 | Table が簡単。内部で RecordBatch を使うこともある |

---

# Arrow basic

https://arrow.apache.org/docs/python/index.html

```python
import pyarrow as pa

days = pa.array([1, 12, 17, 23, 28], type=pa.int8())
months = pa.array([1, 3, 5, 7, 1], type=pa.int8())
years = pa.array([1990, 2000, 1995, 2000, 1995], type=pa.int16())

birthdays_table = pa.table([days, months, years],
names=["days", "months", "years"])

birthdays_table


import pyarrow.parquet as pq

pq.write_table(birthdays_table, 'birthdays.parquet')
reloaded_birthdays = pq.read_table('birthdays.parquet')

reloaded_birthdays


import pyarrow.compute as pc

pc.value_counts(birthdays_table["years"])


import pyarrow.dataset as ds

ds.write_dataset(birthdays_table, "savedir", format="parquet",
   partitioning=ds.partitioning(
      pa.schema([birthdays_table.schema.field("years")])
   )
)

birthdays_dataset = ds.dataset("savedir", format="parquet", partitioning=["years"])

birthdays_dataset.files



# data type

#Fixed-length primitive types:
#ex. int16(), float32(), bool_() True/False, binary(num), timestamp('ms')

#Variable-length primitive types:
#ex. string(), binary()

#Nested types:
#ex. list, struct

import pyarrow as pa

f=pa.field('col_int16', pa.int16())
f
f.name
f.type

f=pa.field('col_list', pa.list_(pa.int16()))
f
f.name
f.type


s=pa.schema([('f0', pa.int16()), ('f1', pa.float32()), ('f2', pa.string())])
s
s.names
s.types

f=pa.field('fx', pa.timestamp('ms'))
s1=s.set(3,f)
s1
s1=s.set(2,f)
s1


arr=pa.array([0,1,2,None,4], pa.int16())
arr
arr.type
arr[0]
arr[1:5]
len(arr)
arr.null_count


arr0=pa.array([0,1,2,3], pa.int16())
arr1=pa.array([True, False, True, None])
arr2=pa.array(['abc', 'def', 'ghi', 'jkl'])

arr=pa.StructArray.from_arrays((arr0,arr1,arr2), names=('f0','f1','f2'))
arr
arr.type


batch = pa.RecordBatch.from_pydict({'f0':arr0,'f1':arr1,'f2':arr2})
batch
batch.schema
batch.num_rows
batch.num_columns
batch[0]
batch.slice(0,2)
batch.slice(1,2)
batch.slice(0,2)[0]
batch[0].slice(0,2)


[batch]+[batch]
[batch]*3

table=pa.Table.from_batches([batch]*3)
table
table.schema
table.num_rows
table.num_columns
table[0]
table[0].chunk(0)
table[0].num_chunks
table.slice(0,7)
table.slice(0,7)[0]
table[0].slice(0,7)


import pandas as pd
table.to_pandas()

[table]+[table]
[table]*3

tables=pa.concat_tables([table]*3)
tables
tables.num_rows
tables.num_columns


table=pa.table([arr0,arr1,arr2], names=['f0','f1','f2'])
table=pa.Table.from_pydict({'f0':arr0,'f1':arr1,'f2':arr2})



# compute functions
https://arrow.apache.org/docs/python/api/compute.html#api-compute

import pyarrow as pa
import pyarrow.compute as pc

a=pa.array([1, 2, 3, 4, 5])
pc.sum(a)


a = pa.array([0, 1, 0, 2])
b = pa.array([1, 1, 2, 2])
pc.equal(a, b)


a = pa.array([2, 3, 4, 1])
pc.min(a)
pc.max(a)


t=pa.table([
      pa.array([1,2,1,2,1,2]),
      pa.array([1,2,3,4,5,6]),
], names=['key', 'val'])

t.group_by('key').aggregate([('val', 'sum')])

t=pa.table([
      pa.array([1,2,1,2,1,2]),
      pa.array([1,2,3,4,5,6]),
      pa.array([1,2,3,4,5,6]),
], names=['key', 'val1', 'val2'])

t.group_by('key').aggregate([('key', 'count'),('val1', 'mean'),('val2', 'stddev') ])

# aggregation functions
# all, any, count, distinct,
# max, min, mean, approximate_median, mode,
# variance, stddev, kurtosis, skew



# join


```

---

**Arrow Table と RecordBatch を使ったブロック単位読み書き**

1. CSV → Arrow Table に変換
2. Table を複数 RecordBatch に分割して処理
3. Parquet に書き出す

arrow0.py

```python
import pyarrow as pa
import pyarrow.csv as pv
import pyarrow.parquet as pq

# ------------------------
# 1. CSV を Arrow Table に変換
# ------------------------
table0 = pv.read_csv('data.csv')

print(table0)

# ------------------------
# 2. Table を RecordBatch に分割
# ------------------------
batches = table0.to_batches(max_chunksize=1000)

for i, batch in enumerate(batches):
    print(f"Batch {i}:")
    print(batch)

# ------------------------
# 3. Parquet にブロック単位で書き出す
# ------------------------
writer = pq.ParquetWriter('data.parquet', table0.schema)

for batch in batches:
    writer.write_batch(batch)

writer.close()

# ------------------------
# 4. Parquet を読み込み（必要な列だけ）
# ------------------------
table1 = pq.read_table('data.parquet', columns=['val'])
print(table1)
```

---

### 説明

1. **CSV → Table**

   - `pyarrow.csv.read_csv` で読み込むと Table になる

2. **Table → RecordBatch**

   - `table.to_batches(batch_size=N)` で分割
   - 大規模データをブロック単位で処理できる

3. **Parquet 書き出し**

   - `ParquetWriter` に RecordBatch を順次書き込む
   - 大きなデータもメモリに一括で読み込まず書き出せる

4. **Parquet 読み込み**

   - `columns=` 指定で必要な列だけ読み込み可能
   - 遅延読み込みや列単位処理に最適

---

Parquet と Arrow IPC（Feather などを含む）はどちらも列指向のデータ形式ですが、用途や性能の特性が違うので使い分けがあります。整理します。

---

## 1. Parquet

### 特徴

- **ディスク向き、永続化用**
- 列ごとに圧縮・エンコード可能 → ファイルサイズ小、I/O 低減
- スキーマを保持、他言語との互換性あり（Python, Java, C++, Spark, Hive など）
- 遅延読み込みが可能（必要な列だけ読み込む）
- 大規模データの保存・分散処理向き

### 用途

- データウェアハウスに格納（Snowflake, BigQuery, Redshift, Hive）
- 分析パイプラインの中間成果物として保存
- 長期保存・バックアップ
- 複数マシンでの共有・分散処理

```python
import pyarrow.parquet as pq
pq.write_table(table, 'data.parquet')
table1 = pq.read_table('data.parquet', columns=['col1', 'col2'])
```

---

## 2. Arrow IPC (Feather)

### 特徴

- **メモリ間転送・高速読み書き向き**
- Zero-copy で Pandas/Polars/Arrow 間でデータ共有可能
- 圧縮は可能だが Parquet ほど圧縮効率は高くない
- データの永続化もできるが、主に **短期保存・高速読み書き** が目的

### 用途

- メモリ上のデータを他プロセスや他言語に渡す
- データフレームを高速に保存・読み込みしたい場合
- パイプライン中で何度もデータを読み書きする場合

```python
import pyarrow.feather as feather
feather.write_feather(table1, 'data.feather')
table2 = feather.read_feather('data.feather')
```

---

## 3. 使い分けのまとめ

| 項目             | Parquet                          | Arrow IPC / Feather                          |
| ---------------- | -------------------------------- | -------------------------------------------- |
| 主な用途         | 永続保存、分散処理               | 高速読み書き、プロセス間共有                 |
| 圧縮             | 高圧縮・列ごと                   | 低〜中圧縮                                   |
| 読み込み速度     | 遅延読み込みで列指定可           | 全列読み込みが基本（高速）                   |
| データサイズ     | 大規模向き                       | 中〜大規模、メモリ内向き                     |
| クロス言語互換性 | 高                               | 高（Arrow 準拠）                             |
| 適したケース     | データウェアハウス、バックアップ | 分析パイプライン内の中間データ、メモリ間共有 |

---

### まとめ

- **Parquet** = 永続化・分散処理・長期保存向き
- **Arrow IPC / Feather** = 高速読み書き・短期保存・メモリ内共有向き

---

**Parquet と Arrow IPC（Feather）で読み書きして速度・ファイルサイズを比較**

arrow1.py

```python
import pyarrow as pa
import pyarrow.parquet as pq
import pyarrow.feather as feather
import time
import os

# ------------------------
# 1. サンプルデータ作成
# ------------------------
n = 1_000_000  # 100万行
table = pa.table({'id':range(n),'value':[float(x) for x in range(n)]
})

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

1. **Parquet**

   - 列ごとに圧縮されるためファイルサイズが小さい
   - 遅延読み込みや列指定が可能
   - 書き込みは Feather より少し遅くなることがある

2. **Arrow IPC / Feather**

   - 書き込み・読み込みが非常に高速
   - 圧縮効率は Parquet より低い
   - メモリ内処理やプロセス間データ受け渡しに向いている

---

| 形式    | 書き込み | 読み込み | ファイルサイズ         |
| ------- | -------- | -------- | ---------------------- |
| Parquet | やや遅め | やや遅め | 小さい（圧縮効率高）   |
| Feather | 高速     | 高速     | 大きめ（ほぼ圧縮なし） |

| 圧縮方式 | 圧縮率 | 速度       | 特徴                             |
| -------- | ------ | ---------- | -------------------------------- |
| snappy   | 低〜中 | 速い       | 分析用途で標準、CPU に優しい     |
| gzip     | 高     | 遅い       | 配布用途（ファイル小さくしたい） |
| brotli   | 高     | やや遅い   | Web 配信向け                     |
| zstd     | 高     | 速い       | 最近人気、snappy より圧縮率良い  |
| LZ4      | 低〜中 | とても速い | 超高速                           |

---

## 1. Arrow と Polars の関係

- **Apache Arrow** は「列指向のメモリフォーマット」としてのライブラリです。

  - Table, RecordBatch, IPC, Parquet などを扱える
  - 高速ですが、**単体ではデータ操作（集計やフィルターなど）の最適化は限定的**

- **Polars** は **内部で Arrow を使う DataFrame ライブラリ**

  - Rust で SIMD 最適化済み
  - LazyFrame による **遅延評価で操作をまとめて最適化**
  - Arrow のゼロコピーも活用

つまり **Polars = Arrow + 高速演算エンジン + 最適化済み DataFrame API** のような位置づけです。

---

## 2. 速度比較のイメージ

| 処理                               | Arrow Table（pyarrow）        | Polars                                  |
| ---------------------------------- | ----------------------------- | --------------------------------------- |
| 単純な読み込み・書き出し           | 高速                          | 同等〜やや高速（内部で Arrow 使うため） |
| 集計 / フィルター / join / groupby | Python 側でループ書く場合遅い | Rust SIMD で高速                        |
| Lazy / 遅延評価                    | なし                          | LazyFrame で複数操作をまとめて最適化    |
| 大規模 CSV → Parquet               | pyarrow でブロック単位必要    | LazyFrame でほぼ自動最適化              |

---

### 3. 結論

1. **単純に Table を作るだけ・ファイル読み書きだけ** → Arrow と Polars で大きな差はない
2. **集計・フィルター・複数列操作・グループ集計などを含む処理** → Polars の方が圧倒的に高速
3. **大規模データ・ELT パイプライン** → Polars + LazyFrame の方が効率的

- Arrow は「メモリ形式」
- Polars は「Arrow を使った高速列指向演算エンジン」

→ **Arrow 単体より Polars を使う方がほとんどの分析・変換処理では速い**

---

**Polars を使って Parquet と Arrow IPC（Feather）の読み書き速度・サイズを比較**

---

arrow2.py

```python
import pyarrow as pa
import polars as pl
import time
import os

# ------------------------
# 1. サンプルデータ作成
# ------------------------
n = 1_000_000  # 100万行
table = pa.table({'id':range(n),'value':[float(x) for x in range(n)]
})

# Polars DataFrame に変換
pl_df = pl.from_arrow(table)

# ------------------------
# 2. Parquet 書き出し
# ------------------------
parquet_file = "data.parquet"
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
feather_file = "data.feather"
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

1. **Polars + Parquet**

   - 圧縮済みでファイルサイズが小さく、大規模データの永続化向き
   - 読み込み速度は Feather より少し遅くなることがある

2. **Polars + Arrow IPC (Feather)**

   - 読み書きが非常に高速
   - 圧縮なしなのでファイルサイズは大きくなる
   - メモリ内処理や短期データ共有向き

3. **Polars の利点**

   - 内部で Arrow を利用して高速列指向処理
   - LazyFrame を使えばさらに大規模データでも効率的に処理可能

---

Polars の **LazyFrame を使って巨大 CSV を Parquet と Feather に高速書き出す**

arrow3.py

```python
import polars as pl
import time
import os

csv_file = "dummy1.csv"
parquet_file = "data.parquet"
feather_file = "data.feather"

# ------------------------
# 1. Parquet 書き出し
# ------------------------
start = time.time()

# LazyFrame で CSV を分割読み込み
lf = pl.scan_csv(csv_file, infer_schema_length=1000)  # 遅延読み込み、型を始め1000行で推定
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

1. **LazyFrame**

   - CSV を遅延読み込み
   - collect() で一度に計算
   - 大規模データでもメモリ効率よく処理可能

2. **Parquet**

   - 圧縮あり → ファイルサイズ小
   - 書き込みは Feather よりやや遅め

3. **Feather (Arrow IPC)**

   - 書き込み・読み込み高速
   - ファイルサイズは大きめ
   - パイプライン中の中間データとして最適

---

**Polars で CSV を chunk 読み込み → Parquet と Feather（IPC）を chunk 書き込み**

---

arrow4.py

```python
import polars as pl
import pyarrow as pa
import pyarrow.parquet as pq
import pyarrow.ipc as ipc
import os
import time

csv_file = "dummy1.csv"
parquet_file = "data.parquet"
feather_file = "data.feather"
chunk_size = 1_000_000  # 100万行ずつ処理

# ------------------------
# 1. Parquet 書き出し（PyArrow ParquetWriter）
# ------------------------
start = time.time()
reader = pl.read_csv_batched(csv_file, batch_size=chunk_size)
writer = None

while True:
    batches = reader.next_batches(1)
    if not batches:
        break
    df = batches[0]
    table = df.to_arrow()  # Polars → Arrow Table

    if writer is None:
        writer = pq.ParquetWriter(parquet_file, table.schema, compression='snappy')

    writer.write_table(table)

if writer:
    writer.close()

end = time.time()
print(f"Parquet write time: {end-start:.2f} sec, size: {os.path.getsize(parquet_file)/1e6:.2f} MB")

# ------------------------
# 2. Feather（IPC）書き出し（PyArrow）
# ------------------------
start = time.time()
reader = pl.read_csv_batched(csv_file, batch_size=chunk_size)
writer = None

while True:
    batches = reader.next_batches(1)
    if not batches:
        break
    df = batches[0]
    table = df.to_arrow()
    arrow_batches = table.to_batches()

    if writer is None:
        writer = ipc.RecordBatchFileWriter(feather_file, table.schema)

    for batch in arrow_batches:
        writer.write_batch(batch)

if writer:
    writer.close()

end = time.time()
print(f"Feather write time: {end-start:.2f} sec, size: {os.path.getsize(feather_file)/1e6:.2f} MB")

# ------------------------
# 3. 読み込み確認
# ------------------------
df_parquet = pl.read_parquet(parquet_file)
df_feather = pl.read_ipc(feather_file)

print("\nParquet first 5 rows:")
print(df_parquet.head())
print("\nFeather first 5 rows:")
print(df_feather.head())
```

---

### 1. CSV の chunk 読み込み

- **Polars の`read_csv_batched`**を使い、巨大 CSV を指定した行数ごと（chunk）に読み込む
- メモリに全体を読み込まず、1 回に処理する量を制限できる
- `next_batches(n)`で 1 回に取得する chunk 数を指定
- 返り値はリストなので、1 つずつ取り出して処理する

---

### 2. Parquet 書き出し（PyArrow）

- Polars DataFrame を直接 Parquet に書き込む機能は制限があるため、**PyArrow の ParquetWriter**を使う
- Polars DataFrame を Arrow Table に変換してから書き込む
- 初回 chunk では Arrow Table のスキーマを指定して ParquetWriter を作成
- 以降の chunk は writer に追記
- 最後に writer を閉じてファイルを確定
- 圧縮形式（例：Snappy）を指定でき、高速かつ軽量なファイルを作れる

---

### 3. Feather（IPC）書き出し（PyArrow）

- Polars DataFrame を Arrow Table に変換
- Arrow Table を RecordBatch に分割
- **RecordBatchFileWriter**で chunk ごとに書き込み
- 初回 chunk でスキーマを指定して writer を作成
- 以降の chunk を順次書き込み
- 最後に writer を閉じてファイルを確定
- Feather 形式は高速読み書きが可能で Arrow エコシステムと互換性が高い

---

### 4. 読み込み確認

- Polars で Parquet / Feather を読み込む
- `.head()`などで一部を確認
- CSV → Parquet/Feather → Polars という流れで、Pandas を介さずに効率的にデータを扱える

---

### 5. まとめ

- **Polars の chunk 読み込み**で巨大 CSV をメモリ効率よく処理
- **Parquet は PyArrow ParquetWriter**、**Feather は RecordBatchFileWriter**で chunk 書き込み
- **Polars → Arrow Table**の変換で Pandas を介さず処理
- メモリ消費を抑えつつ、高速に大量データを保存・読み込み可能

---

**Arrow Table と Polars で同じ CSV を読み込み → 集計 →Parquet 出力して速度比較**

arrow5.py

```python
import pyarrow as pa
import pyarrow.csv as pv
import pyarrow.compute as pc
import pyarrow.parquet as pq
import polars as pl
import time

csv_file = "dummy1.csv"
parquet_arrow = "arrow.parquet"
parquet_polars = "polars.parquet"

# ----------------------------------------
# 1. Arrow で処理
# ----------------------------------------
start = time.time()

table = pv.read_csv(csv_file)
result = table.group_by('id').aggregate([('value', 'sum')])

pq.write_table(result, parquet_arrow)

end = time.time()
print(f"Arrow processing time: {end-start:.2f} sec")

# ----------------------------------------
# 2. Polars で処理
# ----------------------------------------
start = time.time()
df = pl.read_csv(csv_file)

result_polars = df.group_by('id').agg(pl.sum('value').alias('total'))

result_polars.write_parquet(parquet_polars)

end = time.time()
print(f"Polars processing time: {end-start:.2f} sec")
```

---

1. **Arrow 側**

   - CSV → Table は高速
   - ただし groupby や filter を Python 側でループ処理するため遅くなる
   - 大規模データでは明らかにボトルネック

2. **Polars 側**

   - CSV → DataFrame は高速
   - groupby + sum も内部 Rust SIMD 最適化で高速
   - LazyFrame にすればさらに効率よく処理できる

---

**SQLite ファイルをそのまま読み込み、DuckDB の SQL で操作**
SQLite のデータを直接クエリできて、高速に `Parquet` や `Feather` に変換できます。

### 1. 前提パッケージ

```bash
pip install duckdb pandas pyarrow
```

---

### 2. SQLite を DuckDB で読み込む

```python
import duckdb
import pandas as pd

# SQLite ファイルのパス
sqlite_file = 'example.db'

# DuckDB で接続（メモリ上）
con = duckdb.connect()

# SQLite ファイルを直接参照してクエリ
df = con.execute(f"SELECT * FROM read_sqlite('{sqlite_file}', 'my_table')").fetchdf()
```

- `read_sqlite(sqlite_file, table_name)` で SQLite テーブルを直接読み込めます。
- 複数テーブルも同様に読み込めます。

---

### 3. Feather / Parquet に出力

```python
# Feather
df.to_feather('output.feather')

# Parquet
df.to_parquet('output.parquet', engine='pyarrow', compression='snappy')
```

---

### 4. SQLite 全テーブルを一括出力（例）

```python
tables = con.execute(f"SELECT name FROM read_sqlite('{sqlite_file}', 'sqlite_master') WHERE type='table'").fetchall()

for table_name, in tables:
    df = con.execute(f"SELECT * FROM read_sqlite('{sqlite_file}', '{table_name}')").fetchdf()
    df.to_parquet(f'{table_name}.parquet', engine='pyarrow', compression='snappy')
    df.to_feather(f'{table_name}.feather')
```

- これで SQLite 内の全テーブルを自動で Parquet / Feather に変換できます。
- DuckDB は内部的に **列指向処理** なので、大きな SQLite でも高速です。

---

SQLite の全テーブルを **高速かつメモリ効率よく** Parquet と Feather に変換する Python スクリプトのサンプルを作ります。DuckDB を使うので、大規模データでも高速です。

```python
#!/usr/bin/env python3
# sqlite_to_parquet_feather.py
# Convert all SQLite tables to Parquet and Feather using DuckDB

import duckdb
import pandas as pd
import os
import argparse

def export_sqlite(sqlite_file, output_dir, batch_size=100_000):
    os.makedirs(output_dir, exist_ok=True)

    con = duckdb.connect()

    # SQLite 内の全テーブル名を取得
    tables = con.execute(f"""
        SELECT name
        FROM read_sqlite('{sqlite_file}', 'sqlite_master')
        WHERE type='table'
    """).fetchall()

    print(f"Found tables: {[t[0] for t in tables]}")

    for table_name, in tables:
        print(f"\nProcessing table: {table_name}")

        # DuckDB で SQLite テーブルをストリーミング
        query = f"SELECT * FROM read_sqlite('{sqlite_file}', '{table_name}')"
        arrow_table = con.execute(query).arrow()

        # Parquet に分割書き出し
        parquet_file = os.path.join(output_dir, f"{table_name}.parquet")
        writer = None
        for i, batch in enumerate(arrow_table.to_batches(batch_size=batch_size)):
            if writer is None:
                writer = duckdb.ParquetWriter(parquet_file, batch.schema)
            writer.write_table(batch)
        if writer:
            writer.close()
        print(f"Parquet written: {parquet_file}")

        # Feather に書き出し
        feather_file = os.path.join(output_dir, f"{table_name}.feather")
        pd_df = arrow_table.to_pandas()
        pd_df.to_feather(feather_file)
        print(f"Feather written: {feather_file}")

    con.close()
    print("\nAll tables exported successfully.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Export all SQLite tables to Parquet and Feather using DuckDB")
    parser.add_argument("sqlite_file", help="Path to the SQLite file")
    parser.add_argument("output_dir", help="Directory to store Parquet/Feather files")
    args = parser.parse_args()

    export_sqlite(args.sqlite_file, args.output_dir)
```

---

### 使い方

```bash
python sqlite_to_parquet_feather.py example.db output_dir
```

- `output_dir` に各テーブル名で Parquet と Feather が作成されます。
- `batch_size` を調整すれば、超巨大テーブルもメモリ効率よく書き出せます。

---

**Arrow を使って SQLite から DuckDB にデータ移行**

---

## 1. 概要

1. **SQLite からデータを Arrow Table に変換**

   - Python なら `sqlite3` + `pyarrow` で可能

2. **Arrow Table を DuckDB にインポート**

   - DuckDB は Arrow Table を直接読み込める
   - そのまま SQL でテーブル作成可能

メリット：

- 中間ファイル（CSV や Parquet）を作らずにメモリ上で高速移行可能
- Arrow の列指向フォーマットで効率的

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

**巨大な SQLite データベースを DuckDB に効率的に移行する方法**

## 1. 移行戦略

1. SQLite から **chunk 単位でデータを取得**

   - Python の `sqlite3` で `LIMIT` と `OFFSET` または `iterdump()` のようなカーソルを使う

2. Arrow Table に変換（ブロック単位）

   - DuckDB は Arrow Table をゼロコピーで読み込める

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

1. **chunk_size** でメモリ使用量を制御

   - 100 万行単位など、メモリ状況に応じて調整可能

2. **Arrow Table を使う**

   - DuckDB は Arrow Table をゼロコピーで読み込むので高速

3. **永続テーブルに INSERT**

   - 一括挿入で処理時間短縮

4. **巨大データでも安全**

   - SQLite から一度に全部読み込まないためメモリ不足のリスクが低い

---

**SQLite の複数テーブルを DuckDB にブロック単位で移行するサンプル**

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

1. **複数テーブル対応**

   - `sqlite_master` からテーブル名を取得して順次処理

2. **ブロック単位**

   - `chunk_size` ごとにデータを Arrow Table に変換して DuckDB に挿入
   - 巨大テーブルでもメモリ消費を抑えられる

3. **Arrow Table 利用**

   - DuckDB は Arrow Table をゼロコピーで読み込むので高速

4. **永続テーブル作成**

   - 各テーブルを DuckDB 内に永続化して、そのまま分析可能

---

**複数テーブルを並列処理で同時に DuckDB に移行する高速版** を作ります。Python の `concurrent.futures` を使って、テーブル単位で並列化します。

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

1. **テーブル単位で並列処理**

   - 複数テーブルを同時に処理することで、I/O 待ちや CPU 処理を効率化

2. **chunk_size でメモリ消費を制御**

   - 巨大テーブルでも安全に処理可能

3. **Arrow Table を利用**

   - DuckDB にゼロコピーで高速挿入

4. **ThreadPoolExecutor**

   - I/O 中心処理ではスレッドで十分
   - CPU 集約処理なら `ProcessPoolExecutor` に変更可能

---

**PostgreSQL の複数テーブルをブロック単位＆並列で DuckDB に移行する高速版**

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

1. **テーブル単位で並列処理**

   - I/O 待ちや CPU 処理を効率化

2. **chunk_size でメモリ制御**

   - 500,000 行単位など、メモリに合わせて調整可能

3. **Arrow Table 経由で DuckDB にゼロコピー挿入**

   - 高速で安全

4. **永続テーブル作成**

   - そのまま DuckDB で分析可能

5. **ThreadPoolExecutor**

   - I/O 中心なのでスレッド並列で十分
   - CPU 集約処理なら `ProcessPoolExecutor` に変更可能

---
