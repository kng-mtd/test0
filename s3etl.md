# 1. ローカル ワークフロー概要

```
① S3 上の対象ファイルをダウンロード（必要に応じて複数ファイル）
② DuckDB に読み込む（既存テーブル）
③ 更新・行追加を含む MERGE / INSERT / UPDATE 処理
④ 新しい CSV ファイルとしてローカルに書き出す
⑤ S3 にアップロード（上書きまたは置換）
```

ポイント：

- 「更新＋追加」を一度に処理できる
- 複数分割ファイルをループで処理可能
- 1 行が大きくても DuckDB のストリーミングで安全

---

# 2. Python + DuckDB 例（行追加込み）

```python
import duckdb
import boto3

bucket = 'mybucket'
file_key = 'table/part-0001.csv'
updated_file = 'part-0001.new.csv'
update_data_file = 'updates.csv'  # 更新＋追加のデータが含まれる

s3 = boto3.client('s3')
s3.download_file(bucket, file_key, 'part-0001.csv')

con = duckdb.connect()

# 既存 CSV 読み込み
con.execute("""
CREATE TABLE t AS
SELECT * FROM read_csv_auto('part-0001.csv', SAMPLE_SIZE=0)
""")

# 更新＋追加データを読み込む
con.execute("""
CREATE TABLE updates AS
SELECT * FROM read_csv_auto(?, SAMPLE_SIZE=0)
""", [update_data_file])

# MERGE で更新（UPDATE）＋行追加（INSERT）
con.execute("""
MERGE INTO t AS dst
USING updates AS src
ON dst.id = src.id
WHEN MATCHED THEN UPDATE SET val = src.val, updated_at = src.updated_at
WHEN NOT MATCHED THEN INSERT (id, val, updated_at)
VALUES (src.id, src.val, src.updated_at)
""")

# CSV に書き出す
con.execute(f"COPY t TO '{updated_file}' (HEADER TRUE)")

# S3 にアップロード
s3.upload_file(updated_file, bucket, file_key)
```

---

# 3. 複数ファイル対応（行追加対応）

```python
target_files = ['part-0001.csv', 'part-0002.csv']  # 更新対象ファイル
update_data_file = 'updates.csv'

for file_key in target_files:
    local_tmp = file_key.replace('/', '_')
    local_tmp_new = local_tmp + '.new.csv'

    s3.download_file(bucket, file_key, local_tmp)

    con.execute(f"CREATE TABLE t AS SELECT * FROM read_csv_auto('{local_tmp}', SAMPLE_SIZE=0)")
    con.execute(f"CREATE TABLE updates AS SELECT * FROM read_csv_auto('{update_data_file}', SAMPLE_SIZE=0)")

    con.execute("""
    MERGE INTO t AS dst
    USING updates AS src
    ON dst.id = src.id
    WHEN MATCHED THEN UPDATE SET val = src.val, updated_at = src.updated_at
    WHEN NOT MATCHED THEN INSERT (id, val, updated_at)
    VALUES (src.id, src.val, src.updated_at)
    """)

    con.execute(f"COPY t TO '{local_tmp_new}' (HEADER TRUE)")
    s3.upload_file(local_tmp_new, bucket, file_key)
```

---

# 4. ポイント

1. **MERGE の `WHEN NOT MATCHED THEN INSERT` で行追加**
2. 複数ファイルにまたがる場合は **更新対象ファイルごとに処理**
3. S3 への再アップロードは **tmp → 本番置換** が安全
4. ファイルサイズは 50〜100MB 程度を目安
5. 1 行が大きくても DuckDB のストリーミングで安全

---

**Bash + AWS CLI + DuckDB CLI** で「S3 上の分割 CSV に対して更新＋行追加」を行う方法を整理します。

# 前提

- S3 に分割 CSV（例：`part-0001.csv`, `part-0002.csv`）がある
- 更新・追加用の CSV（例：`updates.csv`）がローカルにある
- DuckDB CLI がインストールされている
- ファイルサイズは 50〜100MB 程度
- 1 行が大きい場合もあるので **部分処理/ストリーミング** を想定

---

# 1. 単一ファイルの更新＋追加（Bash 例）

```bash
#!/bin/bash
set -e

BUCKET=mybucket
FILE_KEY=table/part-0001.csv
LOCAL_FILE=part-0001.csv
LOCAL_NEW=part-0001.new.csv
UPDATES=updates.csv

# S3 から対象ファイルをダウンロード
aws s3 cp "s3://$BUCKET/$FILE_KEY" "$LOCAL_FILE"

# DuckDB CLI で更新＋追加
duckdb <<SQL
-- 既存ファイル読み込み
CREATE TABLE t AS SELECT * FROM read_csv_auto('$LOCAL_FILE', SAMPLE_SIZE=0);

-- 更新＋追加データ読み込み
CREATE TABLE updates AS SELECT * FROM read_csv_auto('$UPDATES', SAMPLE_SIZE=0);

-- MERGE（更新＋行追加）
MERGE INTO t AS dst
USING updates AS src
ON dst.id = src.id
WHEN MATCHED THEN UPDATE SET val = src.val, updated_at = src.updated_at
WHEN NOT MATCHED THEN INSERT (id, val, updated_at)
VALUES (src.id, src.val, src.updated_at);

-- 新しい CSV に書き出し
COPY t TO '$LOCAL_NEW' (HEADER TRUE);
SQL

# 新しい CSV を S3 にアップロード（上書き）
aws s3 cp "$LOCAL_NEW" "s3://$BUCKET/$FILE_KEY"
```

---

# 2. 複数ファイル対応（ループ）

```bash
#!/bin/bash
set -e

BUCKET=mybucket
FILES=("table/part-0001.csv" "table/part-0002.csv")
UPDATES=updates.csv

for FILE_KEY in "${FILES[@]}"; do
    LOCAL_FILE=$(basename "$FILE_KEY")
    LOCAL_NEW="$LOCAL_FILE.new"

    aws s3 cp "s3://$BUCKET/$FILE_KEY" "$LOCAL_FILE"

    duckdb <<SQL
CREATE TABLE t AS SELECT * FROM read_csv_auto('$LOCAL_FILE', SAMPLE_SIZE=0);
CREATE TABLE updates AS SELECT * FROM read_csv_auto('$UPDATES', SAMPLE_SIZE=0);

MERGE INTO t AS dst
USING updates AS src
ON dst.id = src.id
WHEN MATCHED THEN UPDATE SET val = src.val, updated_at = src.updated_at
WHEN NOT MATCHED THEN INSERT (id, val, updated_at)
VALUES (src.id, src.val, src.updated_at);

COPY t TO '$LOCAL_NEW' (HEADER TRUE);
SQL

    aws s3 cp "$LOCAL_NEW" "s3://$BUCKET/$FILE_KEY"
done
```

---

# 3. ポイント

1. **DuckDB CLI で全て SQL で完結**
2. **MERGE** で「既存行の更新＋新規行追加」を一度に処理
3. **SAMPLE_SIZE=0** で全行を読み込む（1 行が大きくても安全に処理）
4. 複数ファイルはループ処理 → メモリ消費を分散
5. S3 へのアップロードは **新ファイルを tmp → 上書き** が安全

---

# 4. 大規模データ向け注意

- 1 行が非常に大きい場合は、Bash + DuckDB でも **メモリ消費に注意**
- 必要に応じて **DuckDB の `LIMIT` / 部分処理 / ファイルごとの分割**
- 更新対象行だけを別 CSV にして処理すると効率的

---

**Bash + DuckDB + S3 Select を組み合わせて、S3 上の分割 CSV に対して「条件抽出＋更新＋追加」をフル自動で行うワークフロー** を示します。

---

# 1. ワークフロー概要

1. **S3 Select** で対象ファイルから必要な行だけをストリーム取得
2. **DuckDB CLI** で読み込み、SQL で条件抽出・更新・追加
3. **新しい CSV をローカルに出力**
4. **S3 に上書きアップロード**
5. 複数ファイルはループ処理

特徴：

- 巨大 CSV でも **全体をダウンロードせずに処理可能**
- 1 行が大きくても安全（ストリーミング）
- SQL で複雑な条件や更新・追加も可能

---

# 2. Bash + DuckDB フル自動例

```bash
#!/bin/bash
set -e

BUCKET=mybucket
FILES=("table/part-0001.csv" "table/part-0002.csv")
UPDATES=updates.csv      # 更新行 CSV
ADD_ROWS=add_rows.csv    # 追加行 CSV

for FILE_KEY in "${FILES[@]}"; do
    LOCAL_TMP=$(basename "$FILE_KEY").tmp.csv
    LOCAL_NEW=$(basename "$FILE_KEY").new.csv

    # 1. S3 Select で既存行のうち更新対象外を抽出
    aws s3api select-object-content \
        --bucket "$BUCKET" \
        --key "$FILE_KEY" \
        --expression "SELECT * FROM S3Object s WHERE s.id NOT IN (SELECT id FROM S3Object)" \
        --expression-type SQL \
        --input-serialization '{"CSV": {"FileHeaderInfo": "USE"}}' \
        --output-serialization '{"CSV": {}}' \
        "$LOCAL_TMP"

    # 2. DuckDB で更新・追加処理
    duckdb <<SQL
-- 既存行をテーブルに読み込む
CREATE TABLE t AS SELECT * FROM read_csv_auto('$LOCAL_TMP', SAMPLE_SIZE=0);

-- 更新行を読み込む
CREATE TABLE updates AS SELECT * FROM read_csv_auto('$UPDATES', SAMPLE_SIZE=0);

-- 追加行を読み込む
CREATE TABLE add_rows AS SELECT * FROM read_csv_auto('$ADD_ROWS', SAMPLE_SIZE=0);

-- MERGE: 更新行を反映、存在しない場合は追加
MERGE INTO t AS dst
USING updates AS src
ON dst.id = src.id
WHEN MATCHED THEN UPDATE SET val = src.val, updated_at = src.updated_at
WHEN NOT MATCHED THEN INSERT (id, val, updated_at)
VALUES (src.id, src.val, src.updated_at);

-- 追加行も挿入
INSERT INTO t
SELECT * FROM add_rows;

-- 新しい CSV に書き出す
COPY t TO '$LOCAL_NEW' (HEADER TRUE);
SQL

    # 3. S3 にアップロード（上書き）
    aws s3 cp "$LOCAL_NEW" "s3://$BUCKET/$FILE_KEY"
done
```

---

# 3. ポイント

1. **S3 Select で対象行だけ抽出**

   - 更新対象行以外をストリーム出力
   - メモリ消費最小化

2. **DuckDB で MERGE + INSERT**

   - 更新と追加を同時に処理
   - SQL で条件抽出や加工も可能

3. **複数ファイルもループ処理**

   - 更新・追加対象の CSV があれば全ファイルに適用可能

4. **安全な S3 上書き**

   - tmp ファイル → 新ファイル → S3 上書き
   - 元ファイルは保持できる

---

# 4. メモリ・パフォーマンスの工夫

- `SAMPLE_SIZE=0` で全行スキャン（行が大きくても OK）
- 更新対象のファイルだけ処理 → 大規模データでも効率的
- 1 行が非常に大きい場合は、**DuckDB のストリーミング処理**で対応

---

**「更新対象行だけを S3 Select で抽出 → ローカル保存せずに DuckDB にパイプで渡して更新・追加 → S3 に書き戻す」** 完全ストリーム版の Bash ワークフローを作ります。

---

# 前提

- S3 上の CSV 分割ファイルがある（例：`part-0001.csv`）
- 更新用 CSV（例：`updates.csv`）、追加行 CSV（例：`add_rows.csv`）はローカルにある
- DuckDB CLI と AWS CLI が利用可能
- 1 行が大きくてもメモリ効率良く処理したい

---

# 1. フロー概要

```
① S3 Select で更新対象行だけ抽出 → DuckDB に直接パイプ
② 既存行（更新対象外）は S3 Select で抽出 → DuckDB にパイプ
③ DuckDB 内で MERGE + INSERT
④ COPY でローカル CSV または S3 に直接書き出し
⑤ S3 上書き
```

ポイント：

- 一時ファイル不要 → メモリ消費最小
- DuckDB の SQL で更新・追加・条件抽出可能

---

# 2. Bash + DuckDB 完全ストリーム例

```bash
#!/bin/bash
set -e

BUCKET=mybucket
FILE_KEY=table/part-0001.csv
NEW_FILE=part-0001.new.csv
UPDATES=updates.csv       # 更新行
ADD_ROWS=add_rows.csv     # 追加行

# 1. DuckDB CLI にストリームを渡す
duckdb <<SQL
-- 既存行（更新対象外）を S3 Select でパイプ入力
CREATE TABLE t AS
SELECT * FROM read_csv_auto('stdin', SAMPLE_SIZE=0);

-- 更新行を読み込む
CREATE TABLE updates AS
SELECT * FROM read_csv_auto('$UPDATES', SAMPLE_SIZE=0);

-- 追加行を読み込む
CREATE TABLE add_rows AS
SELECT * FROM read_csv_auto('$ADD_ROWS', SAMPLE_SIZE=0);

-- MERGE: 更新行
MERGE INTO t AS dst
USING updates AS src
ON dst.id = src.id
WHEN MATCHED THEN UPDATE SET val = src.val, updated_at = src.updated_at
WHEN NOT MATCHED THEN INSERT (id, val, updated_at)
VALUES (src.id, src.val, src.updated_at);

-- INSERT: 追加行
INSERT INTO t
SELECT * FROM add_rows;

-- 新しい CSV に書き出す
COPY t TO '$NEW_FILE' (HEADER TRUE);
SQL
< <(
  # S3 Select で更新対象外の既存行だけ抽出して標準出力
  aws s3api select-object-content \
    --bucket "$BUCKET" \
    --key "$FILE_KEY" \
    --expression "SELECT * FROM S3Object s WHERE s.id NOT IN (SELECT id FROM S3Object)" \
    --expression-type SQL \
    --input-serialization '{"CSV": {"FileHeaderInfo": "USE"}}' \
    --output-serialization '{"CSV": {}}' \
    /dev/stdout
)

# 2. S3 にアップロード
aws s3 cp "$NEW_FILE" "s3://$BUCKET/$FILE_KEY"
```

---

# 3. ポイント

1. **S3 Select → DuckDB に直接パイプ**

   - 一時ファイルを作らないのでメモリ効率良い
   - 巨大ファイルでも安全

2. **更新＋追加＋条件抽出** が DuckDB の SQL 内で完結

3. 複数ファイルも `for FILE_KEY in part-*.csv; do ... done` で処理可能

4. 更新対象行の抽出条件は S3 Select の SQL で自由に設定可能

---

# 4. 注意点

- DuckDB CLI は標準入力を **ストリーム処理** できるが、あまり巨大な行や巨大ファイルだと一度に読み込むのでメモリ注意
- 更新対象行の CSV はローカルに置く必要あり（追加行・更新行）
- S3 Select は SQL 文が限定的なので複雑な JOIN はできない → DuckDB で結合

---

# 1. 推奨ワークフロー図（テキストによる図示）

## A. s3 cp + ローカル更新（小規模向け）

```
[S3 CSV (大きな単一/分割ファイル)]
              |
              v
        s3 cp download
              |
              v
         local DuckDB
       (update + append)
              |
              v
        s3 cp upload
```

特徴: シンプルだが DL/UL が重く、大規模には向かない。

---

## B. S3 Select + DuckDB（ローカル保存）

```
[S3 CSV]
   |     \
   |      \
   |   S3 Select (更新対象行のみ)
   |            |
   v            v
 s3 cp      partial.csv
   |            |
   +------> DuckDB (update + append)
                    |
                    v
                 new.csv
                    |
                    v
            s3 cp upload
```

特徴: 更新対象が少ないときに効率良い。

---

## C. S3 Select → DuckDB 直結（完全ストリーミング）

```
[S3 CSV]
   |
   | S3 Select (更新対象行のみ)
   |   (stream)
   v
[STDOUT] ----> DuckDB (update + append; no temp file)
                     |
                     v
                  output.csv
                     |
                     v
                s3 cp upload
```

特徴: ローカルファイル不要、最速、メモリ最小、巨大分割にも対応。

---

# 2. 速度比較表（概算）

前提:

- CSV 分割は 1 ファイル 100MB
- 更新対象 10%
- 10GB = 100 ファイル、50GB = 500 ファイル、100GB = 1000 ファイル
- DuckDB 100MB を処理するのに約 5 秒
- ネットワークは 1Gbps（1GB ≈ 8 秒）

## A. s3 cp + ローカル更新

| データ量 | DL + UL | DuckDB  | 総時間     |
| -------- | ------- | ------- | ---------- |
| 10GB     | 160 秒  | 500 秒  | 約 660 秒  |
| 50GB     | 800 秒  | 2500 秒 | 約 3300 秒 |
| 100GB    | 1600 秒 | 5000 秒 | 約 6600 秒 |

---

## B. S3 Select + ローカル保存

| データ量 | S3 Select DL（10%） | DuckDB  | 総時間     |
| -------- | ------------------- | ------- | ---------- |
| 10GB     | 8 秒〜10 秒         | 500 秒  | 約 510 秒  |
| 50GB     | 40 秒               | 2500 秒 | 約 2540 秒 |
| 100GB    | 80 秒               | 5000 秒 | 約 5080 秒 |

---

## C. S3 Select → DuckDB パイプ（完全ストリーム）

| データ量 | S3 Select DL（10%） | DuckDB  | 総時間     |
| -------- | ------------------- | ------- | ---------- |
| 10GB     | 8 秒〜10 秒         | 500 秒  | 約 510 秒  |
| 50GB     | 40 秒               | 2500 秒 | 約 2540 秒 |
| 100GB    | 80 秒               | 5000 秒 | 約 5080 秒 |

ローカル保存が無くなる分、安定しやすく、メモリ使用量も最小。

---

# 3. 規模ごとの推奨方式

| 規模        | 推奨方式                  | 理由                                            |
| ----------- | ------------------------- | ----------------------------------------------- |
| 数百 MB     | s3 cp                     | 容量が小さく動作が単純                          |
| 1GB〜5GB    | s3 cp または S3 Select    | どちらでも実用的                                |
| 10GB〜30GB  | S3 Select                 | ネットワーク削減効果が大きい                    |
| 30GB〜100GB | S3 Select → DuckDB パイプ | 完全ストリームが最も効率的                      |
| 100GB〜1TB  | 完全ストリーム一択        | s3 cp は非現実的、S3 Select で 90% 以上削減可能 |

---

- 小規模なら s3 cp が最も簡単。
- 更新対象が少ないなら S3 Select（10〜30GB くらいが効果絶大）。
- 巨大分割や 100GB 以上では **S3 Select → DuckDB パイプ（完全ストリーム）** が最速・最安・最安定。

**S3 で巨大テーブルを「分割ファイル」として管理しつつ、追加・更新を行う構成のベストプラクティス**を、あなたの用途（1 行 ≈ 1MB、binary 列あり / base64 もあり）に合わせてまとめます。

**S3 を「append/log ストレージ」として使い、更新は「差分ファイル + compact（マージ）」で処理するのが最適**です。

理由：

- **1 行が 1MB** は非常に大きい
- **更新を直接 Parquet の部分書き換えで行うことは不可能**
- **S3 はオブジェクト単位（ファイル単位）でしか更新できない**
- Big binary を含むので **行指向ストレージとして扱う必要** があるが、Parquet は行指向ではない

よって、「更新のたびに Parquet を全部作り直す」ではコストが破綻します。

---

# 1. 基本的な構成（最も現実的）

## **１）レコードはすべて “append-only” で記録（ログ構造）**

- 新規行 → 新規ファイルに追記
- 更新行 → 「更新レコード」を別ファイルへ追記
- 削除行 → tombstone レコードを別ファイルに書く

### ファイル名例

```
table/
  part-000000.parquet
  part-000001.parquet
  updates/
    upd-20251130-001.parquet
    upd-20251130-002.parquet
  deletes/
    del-20251130-001.parquet
```

---

## **２）定期的に compaction（マージ）処理で “実体テーブル” を作り直す**

- 更新された行だけ抽出（S3 Select or AWS SDK）
- 古い行を排除
- 新しい “compact” ファイルを作成する
- compact 後に古いファイル・update ファイルを削除/アーカイブする

### メリット

- S3 の書き換えが不要
- 更新は cheap（ただの追記）
- compact はバッチ処理なのでコスト制御しやすい

---

# 2. バイナリ列の扱い

## 選択肢 A：**S3 オブジェクトに分離（一番良い）**

```
main-table/
  part-0000.parquet
  ...
blobs/
  <id>.bin
```

Parquet 側は blob の URI だけ持つ。

**メリット**

- Delta Lake や Iceberg と同じ戦略
- Parquet ファイルが巨大化しない
- 1 行 1MB の問題がほぼ解消

**注意点**

- Eventually consistency を考慮する
- blob のライフサイクル管理が必要

---

## 選択肢 B：binary を base64 にして Parquet に入れる

可能だが、以下の理由で非推奨：

- Parquet は列指向 → 1 行が 1MB だと効果が薄い
- Parquet 1row ≈ 1MB は compression が効きにくい
- 巨大すぎて compaction が遅い
- S3 GET コストも高くなる

## 選択肢 C：binary 列はバイナリ型のまま Parquet に入れる

base64 よりはマシだが、やはり 1 行が大きいと効率悪い。

---

# 3. 分割の戦略（最も重要）

1. **ファイルサイズは 32MB〜256MB の間**
2. 行サイズが巨大なので

   - **1 ファイルあたり最大 100〜200 行**

3. ディレクトリ階層は時間 or ID ベース

   ```
   table/YYYY/MM/DD/part-xxxxx.parquet
   ```

4. 更新ファイルはさらに小さく細分化

   ```
   updates/dt=2025-11-30/upd-001.parquet
   ```

---

# 4. 更新方法まとめ（ワークフロー）

## 新規追加

- Parquet 小ファイルへ append 書き込み
  （ParquetWriter で “new small file” を作る）

## 更新

1. 更新対象 ID を S3 Select で抽出
2. 更新行だけを「update ファイル」に書く
3. compact 時に本体へマージ

## compact（毎日、または 1GB 溜まったら）

1. base ファイル + update ファイルを Python or Spark or DuckDB で読み込み
2. 最新行だけ残す
3. 新しい base ファイルを出力
4. 古い base / update ファイルを削除

---

# 5. 選ぶべきフォーマット

| フォーマット               | binary | 更新                       | 説明                                  |
| -------------------------- | ------ | -------------------------- | ------------------------------------- |
| **Parquet**                | ◯      | ×（不可）                  | 高速・圧縮効率良いが row 更新できない |
| **ORC**                    | ◯      | ×                          | 同上                                  |
| **JSONL**                  | ◯      | ◯（append + compact 向き） | row 1MB ならこれが最も現実的          |
| **SQLite-on-S3（S3Fuse）** | ◯      | △                          | 重くて推奨しない                      |

**row が巨大 → Parquet 向きではない**
→ JSONL or Arrow IPC のほうが向いているケースが多い。

---

### 最も安定・高速・管理しやすい構成

```
S3
 ├ table_main/    ← base（JSONL or Parquet） 小さく分割
 ├ table_updates/ ← update レコード（JSONL）
 ├ table_deletes/ ← tombstone
 └ blobs/         ← binary（外部ストレージ）
```

- 追加＝ append
- 更新＝ update ログ追加
- 削除＝ delete ログ追加
- compaction ＝低頻度で大ファイル生成
- binary は別オブジェクトに切り離す

この構造は **Delta Lake / Iceberg / Hudi と同じ戦略**

---

# **CSV でも技術的には可能だが、JSONL のほうが圧倒的に適している。**

特に「1 行 = 約 1MB」「binary 列あり」「更新を append + compact 方式で行う」という条件では、
**CSV はかなりつらく、JSONL のほうが安全で高速で堅牢** です。

# 1. CSV が向いていない理由

## **1）バイナリ列（もしくは base64）があると CSV が壊れやすい**

- base64 には `,` や `\n` が入らないので CSV と相性は悪くないが、
- 問題は **サイズ（1MB）と escape の複雑さ**。

CSV のルール：

- `,` を含むと `"..."` で囲む必要
- 改行を含むと `"..."` で囲む必要
- `" "` を含むと `""` とエスケープ

**1MB の長大フィールドを CSV の escape で処理するのは重い**。
また、エスケープ漏れは**テーブル全体を壊す致命的事故になる**。

---

## **2）更新処理（部分抽出・置換）が非常にやりにくい**

CSV はフィールドが positional （位置依存）なので、

- カラム追加・削除があった時に壊れやすい
- JSONL と違って「1 行 → 1 JSON」として扱えない
- Python や Bash で巨大行（1MB）を処理すると escape が面倒

compact 処理も JSONL より困難。

---

## **3）S3 Select が CSV を扱う場合はクオートの制限が多い**

AWS S3 Select for CSV には以下の制限：

- カラムにクオートが入ると select 不能になるケースがある
- エスケープの仕様がデフォルト `"`, `""` 固定で柔軟性がない
- 1 行 1MB レコードに弱い

AWS S3 Select は CSV より JSON のほうが明確に安定します。

---

## **4）DuckDB / Spark / Pandas などの CSV パースは「重い」**

1MB のフィールドを持つ CSV は、

- パーサが毎回 escape 処理
- JSONL より CPU 使用率が高い
- 並列読み込みもあまり効かない

CSV パースは「レイテンシ高」「メモリ消費多」という弱点があります。

---

# 2. JSONL が圧倒的に適している理由

## **1）1 行 = 1 レコード で扱いやすい**

JSON Lines の強み：

```
{"id":1,"bin":"<base64>","meta":{...}}
{"id":2,"bin":"<base64>","meta":{...}}
```

- 行の境界が明確
- 解釈不能になるリスクが低い
- コンパクト作業が script で簡単

---

## **2）構造が柔軟で “column schema drift” に自然対応**

CSV は列順固定、JSONL は柔軟。

更新・追加時にスキーマが変わっても扱いやすい。

---

## **3）巨大 1 行でも JSON パーサは問題なく処理する**

JSONL は以下の性質が強い：

- 1 行 1MB → JSON として普通に扱える
- base64 をそのまま出せる
- DuckDB も JSONL を読み込める（flexible）
- 圧縮（gzip）も効く

---

## **4）S3 Select は JSON のほうが安定**

AWS S3 Select for JSON の特長：

- エスケープ要件が少ない
- key-based query が可能
- CSV より大きいレコードに強い

---

# 3. CSV を使う場合の条件（例外的）

以下の条件を満たすなら CSV もアリ：

- 完全に “固定列 & 固定フォーマット”
- バイナリ列は **別の S3 オブジェクトに分離**（CSV 内に base64 を入れない）
- 行サイズ < 200KB（推奨）
- S3 Select をほとんど使わない
- 全てのアプリが “CSV の escape ルールを厳密に実装” できる

あなたの場合（行 1MB・binary あり）には当てはまらないので CSV は不向き。

---


## 1 行 1MB + binary 列 + 更新/compact

この条件では **CSV は壊れやすく、扱いが非常に難しい。**

## JSONL のほうが圧倒的に安全・高速・簡単。

---

**JSONL ではバイナリ列を「そのまま」持つことはできません。必ず Base64 などのエンコードが必要です。**

# JSONL は「生のバイナリ」を保存できない

## 保存できない理由

JSON / JSONL は仕様として以下を許しません：

- バイト列（0x00 などの制御文字）
- 任意のバイトシーケンス
- 非 UTF-8 文字

つまり、1M バイトの binary blob を JSON の文字列フィールドに入れる場合、
**UTF-8 安全な表現に変換する必要があります。**

→ **Base64** が標準的。

---

# JSONL でバイナリを扱う正しい形

## Base64 にする例

```jsonl
{"id": 1, "image": "iVBORw0KGgoAAAANSUhEUgAA..."}
{"id": 2, "image": "AAABAAEAICAAAAEAIACoEAAAFgAAACgAAA..."}
```

## Hex (Base16) にしても良い

（ただしサイズが 2 倍になるので非推奨）

---

# なぜ生のバイナリを JSONL に入れられないのか？

### 1. JSON 文字列は UTF-8 テキストしか許可しない

0x00–0x1F などの control bytes の多くは JSON パース不能。

### 2. S3, Athena, DuckDB, jq, Lambda など

**JSON 文字列フィールド内部に生バイトがあるとほぼ全部壊れる。**

特にストリーミング処理 (pipe → DuckDB) が即死する。

---

# 例外：**MessagePack** や **Parquet** などは生バイナリ OK

もし base64 が嫌ならフォーマットを替える必要があります。

### MessagePack (msgpack)

- binary type をネイティブに保持
- Python / Go / Node で高速
- JSONL より compact

### Parquet

- `BINARY` 型にそのまま保存
- 圧縮も効く
- S3 Select は使えない（CSV/JSON しか無理）

### Avro

- bytes 型をサポート
- S3 Select は対応していない

---

# JSONL を選ぶ場合の結論

### JSONL は便利：append、line-based、S3 で扱いやすい

### しかし **binary 列だけは base64 で持つしかない**

---

# 補足：1 行 1MB の JSONL（base64 込み）は問題？

概ね問題ありません。

- S3 append (バケット側) → NG（疑似 append を実装）
- S3 multipart upload → OK
- S3 Select → 1MB/行は重いが動く
- `jq` や Python → 正常に処理できる
- DuckDB → `read_ndjson_auto` で読めるが巨大行は重くなる

もし巨大 binary 列が中心なら JSONL より **Parquet Binary** を強く推奨します。

---

JSONL に対する`awk` と `jq` の速度比較について整理します。実際の用途（JSONL の大きさや構造、フィルタ内容）によって差が出ます。

# 1. 前提条件

- ファイル形式：JSONL（1 行 = 1 JSON オブジェクト、1MB/行 の場合もある）
- 行数：100 万行程度
- フィルタ条件：

  - 数値フィールドの比較（num2 > 0.5）
  - 文字列フィールドの比較（str == "aaa"）

---

# 2. 単純比較（フラット JSON、1 行 100 ～ 200 バイト程度）

### Bash / awk 例

```bash
time awk '{
  match($0, /"num2":[ ]*([0-9.]+)/, m);
  if (m[1] > 0.5) print $0
}' dummy.jsonl > out.jsonl
```

- 軽量で高速（数百万行でも数秒～ 10 秒程度）
- メモリ消費は非常に少ない
- 注意点：正規表現でしか JSON を解釈していないので、複雑な JSON は誤動作する可能性

---

### Bash / jq 例

```bash
time jq 'select(.num2 > 0.5)' dummy.jsonl > out.jsonl
```

- JSON パーサを内部で使っているため正確
- 行数 100 万、1 行 100〜200B だと awk とほぼ同等の速度（若干遅いことがある）
- メモリ消費は awk よりやや多いが、ストリーム処理できるため問題なし

---

# 3. 大きい行（1 行 1MB）での比較

- awk は正規表現で処理するため 1 行 1MB でも直接比較は可能
- jq は JSON パーサを通すので CPU 負荷が高くなる
- 結果：

  - awk：CPU 負荷低く、やや高速
  - jq：CPU 負荷高め、メモリ使用増加、1 行 1MB の場合は awk より遅いことが多い

---

# 4. メリット・デメリットまとめ

| ツール | メリット                                                    | デメリット                                      |
| ------ | ----------------------------------------------------------- | ----------------------------------------------- |
| awk    | 高速、メモリ効率良い、軽量                                  | JSON 構造が複雑だと不正確、文字列の比較が難しい |
| jq     | JSON パーサ使用で正確、ネスト・配列にも対応、複雑条件も簡単 | CPU 負荷高め、巨大行では遅くなる、awk より重い  |

---

# 5. 実用上の判断目安

1. **JSONL がフラットで単純な条件**
   → awk が最速

2. **JSONL にネスト、配列、Base64 バイナリなどがある**
   → jq を使うべき

3. **行サイズ 1MB 超の場合**

   - awk は CPU 使用量低めで高速
   - jq はやや遅くなるが、正確性優先なら許容範囲

---

S3 から取得したデータを **Lua で処理する場合**

---

# 1. S3 から Lua にデータを渡す方法

## (A) `aws s3 cp -` で標準出力を Lua で読み込む

```bash
aws s3 cp s3://my-bucket/dummy.jsonl - | lua process.lua
```

### Lua 側（process.lua）

```lua
-- 1行ずつ読み込むストリーム処理
for line in io.lines() do
    local num1 = line:match('"num1"%s*:%s*(%d+)')
    local num2 = line:match('"num2"%s*:%s*([0-9.]+)')
    local str  = line:match('"str"%s*:%s*"(%a+)"')

    if num2 and tonumber(num2) > 0.5 then
        print(line)  -- 条件に合う行だけ出力
    end
end
```

- `io.lines()` は標準入力を **1 行ずつ読み込む**
- メモリに全ファイルを保持せずに処理可能
- JSON の正規表現処理で簡単なフラット JSON に対応

---

## (B) S3 Select の結果を Lua で受け取る

- S3 Select は **標準出力で JSONL を返す**
- Lua 側で受け取って同様に `io.lines()` で処理可能

```bash
aws s3api select-object-content \
  --bucket my-bucket \
  --key dummy.jsonl \
  --expression "SELECT * FROM S3Object s WHERE s.num2 > 0.5" \
  --expression-type SQL \
  --input-serialization '{"JSON":{"Type":"LINES"}}' \
  --output-serialization '{"JSON":{}}' \
  | lua process.lua
```

- この場合、**S3 側でフィルタ済み** の行だけ Lua に渡せるのでさらに高速

---

# 2. 大容量 JSONL に対するメモリ効率

- Lua は **1 行ずつ読み込む限りメモリ消費は行サイズ単位**
- 1 行 1MB × 100 万行でも、メモリは 1MB + Lua のオーバーヘッド程度
- バッファサイズが大きくなると多少増えるが、通常のフラット JSON なら問題なし

---

# 3. バイナリ列の処理

- JSON 内に Base64 で格納されたバイナリがある場合、Lua 側でデコード可能：

```lua
local b64 = require("mime").unb64  -- LuaSocket の mime モジュールなど
local decoded = b64(base64string)
```

- 1 行単位でデコードできるのでメモリ効率は維持される

---

Lua が `awk` や `jq` より速いかどうかは、**用途と処理内容によって変わります**。整理してみます。

---

# 1. 処理対象の規模

- **行数**: 数十万〜数百万行
- **1 行のサイズ**: 数百バイト〜1MB
- **JSON 構造**: フラットかネストか

---

# 2. パフォーマンス傾向

| ツール | 長所                                                                                   | 短所                                                                           | 大規模 JSONL での挙動                                                                       |
| ------ | -------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------- |
| `awk`  | - 軽量で高速<br>- 正規表現だけで済む簡単なフィルタは非常に速い                         | - JSON 構造を正確に扱えない<br>- 複雑条件は書きにくい                          | 1 行ずつ処理するのでメモリ効率は最高                                                        |
| `jq`   | - 正確に JSON を扱える<br>- 複雑なフィルタやネストに強い                               | - JSON パーサを内部で使うため CPU 負荷高め                                     | 1 行 1MB だと awk より遅くなることが多い                                                    |
| Lua    | - ストリーム処理可能<br>- 正規表現 + JSON ライブラリで柔軟<br>- 軽量なバイナリ処理も可 | - JSON ライブラリは Lua 側にロードが必要<br>- パースは jq より高速とは限らない | フラット JSON の単純条件なら awk と同等〜少し遅い<br>ネスト JSON では jq より速い場合もある |

---

# 3. 具体的な目安

- **単純な数値/文字列比較のみ（フラット JSONL）**
  → `awk` が最速
- **ネスト JSON や Base64 バイナリの処理**
  → `jq` は正確だがやや遅くなる
  → Lua + JSON ライブラリなら **jq より軽量で高速** に処理できる可能性がある
- **1 行が大きい場合（1MB）**
  → awk / Lua はメモリ効率良好
  → jq は JSON パーサ内部でメモリ使用増加

---


- **フラット JSON + 単純フィルタ → awk 最速**
- **複雑な JSON → Lua + JSON ライブラリは jq より軽量で高速になる場合がある**
- **行サイズが大きい場合 → Lua は jq より有利**
- Lua は **処理を自分で細かく制御できる**ので、特定条件で最適化可能

---

**「S3 上の巨大 JSONL を append + update + compact で管理する構成」** と「DuckDB に JSONL をストリームで送り、join/merge（更新マージ）する方法」を **Python 版・Bash 版** の両方で示します。

あなたの用途（1 行 ≈1MB・binary あり）に合わせて、
**完全ストリーム（ローカルに保存しない）で動くように最適化** しています。

---

# =========================================

# ① JSONL append（追加）

# =========================================

### ■ Python（boto3 + streaming）

```python
import boto3
import json
import uuid

s3 = boto3.client('s3')
bucket = 'my-bucket'
prefix = 'table/'

def append_record(record):
    data = json.dumps(record) + '\n'
    key = f"{prefix}append-{uuid.uuid4()}.jsonl"
    s3.put_object(Bucket=bucket, Key=key, Body=data)

# usage
append_record({
    "id": 1001,
    "blob": "base64...",
    "ts": "2025-11-30T12:00:00Z"
})
```

---

### ■ Bash（AWS CLI）

```bash
# 1行 JSON を append 用ファイルとして新規アップロード
echo '{"id":1001,"blob":"base64...", "ts":"2025-11-30"}' \
  | aws s3 cp - s3://my-bucket/table/append-$(uuidgen).jsonl
```

---

# =========================================

# ② JSONL update（部分更新ログ追加）

# =========================================

更新行を「update-log/」に追加し、後で compact でマージします。

### ■ Python

```python
def update_record(record):
    data = json.dumps(record) + '\n'
    key = f"table-update/update-{uuid.uuid4()}.jsonl"
    s3.put_object(Bucket=bucket, Key=key, Body=data)

# example
update_record({
    "id": 1001,
    "blob": "base64-new",
    "ts": "2025-11-30T13:00:00Z"
})
```

### ■ Bash

```bash
echo '{"id":1001,"blob":"base64-new","ts":"2025-11-30T13:00"}' \
  | aws s3 cp - s3://my-bucket/table-update/update-$(uuidgen).jsonl
```

---

# =========================================

# ③ S3 JSONL → DuckDB でストリーム merge/compact

# =========================================

## ★ ポイント

- S3 の JSONL を **直接 `aws s3 cp --quiet` で標準出力へ流す**
- pipe で DuckDB に渡し、`read_jsonl_auto()` で読み込む
- compact（最新レコードだけ残す）を行い、新しい compact ファイルを S3 に書き戻す

---

# ③-A：Bash（完全ストリーム compact）

### ■ 1. 全 append & update ファイルを統合し、DuckDB で merge

```bash
#!/bin/bash

BUCKET="my-bucket"
PREFIX="table/"
UP_PREFIX="table-update/"
OUT="compact-$(date +%Y%m%d%H%M%S).jsonl"

# DuckDB SQL（最新 ts で行を更新）
SQL="
CREATE TABLE merged AS
SELECT *
FROM read_jsonl_auto('/dev/stdin');

-- 最新 ts を持つレコードのみ
CREATE TABLE compact AS
SELECT *
FROM (
  SELECT *,
         ROW_NUMBER() OVER (PARTITION BY id ORDER BY ts DESC) AS rn
  FROM merged
)
WHERE rn = 1;

COPY (SELECT * FROM compact) TO '/dev/stdout' (FORMAT JSONL);
"

# 実行（巨大 JSONL をストリームで送り、ストリームで結果を受け取る）
aws s3 cp s3://$BUCKET/$PREFIX - --recursive --quiet \
| aws s3 cp s3://$BUCKET/$UP_PREFIX - --recursive --quiet \
| duckdb -c "$SQL" \
| aws s3 cp - s3://$BUCKET/table-compact/$OUT

echo "done: table-compact/$OUT"
```

### 動作説明

1. `aws s3 cp --recursive -` で複数 JSONL を連結して stdout に
2. DuckDB が `/dev/stdin` を JSONL として読み込む
3. `PARTITION BY id ORDER BY ts DESC` で最新行だけ残す
4. 結果を `/dev/stdout` へ JSONL として流す
5. それを S3 にアップロード

→ **1TB の JSONL でもローカル保存なし**
→ **メモリ使用量は DuckDB のクエリ最中のみ**

---

# ③-B：Python（完全ストリーム compact）

```python
import boto3
import duckdb
import subprocess

bucket = "my-bucket"
prefix_main = "table/"
prefix_up = "table-update/"
out_key = f"table-compact/compact.jsonl"

s3 = boto3.client("s3")

# ---- S3 JSONL を stdout にストリームで連結 ----
def stream_all_jsonl():
    # main
    objs = s3.list_objects_v2(Bucket=bucket, Prefix=prefix_main).get('Contents', [])
    for o in objs:
        body = s3.get_object(Bucket=bucket, Key=o['Key'])['Body']
        for chunk in body.iter_lines():
            yield chunk + b"\n"

    # updates
    objs2 = s3.list_objects_v2(Bucket=bucket, Prefix=prefix_up).get('Contents', [])
    for o in objs2:
        body = s3.get_object(Bucket=bucket, Key=o['Key'])['Body']
        for chunk in body.iter_lines():
            yield chunk + b"\n"


# ---- DuckDB で merge（最新のみ） ----
con = duckdb.connect()
con.execute("""
CREATE TABLE merged AS
SELECT *
FROM read_jsonl_auto('/dev/stdin');

CREATE TABLE compact AS
SELECT *
FROM (
  SELECT *,
    ROW_NUMBER() OVER (PARTITION BY id ORDER BY ts DESC) rn
  FROM merged
)
WHERE rn = 1;

COPY (SELECT * FROM compact) TO 'result.jsonl' (FORMAT JSONL);
""")

# ---- 結果を S3 にアップロード ----
s3.upload_file("result.jsonl", bucket, out_key)
```

※ Python 版は `/dev/stdin` の扱いの都合で一旦ローカルファイルへ出力しているが、完全ストリーム版にすることも可能。

---

# =========================================

# ④ 完全ストリーム「S3 → DuckDB → S3」1 行もローカル保存しない（最速版）

# =========================================

### DuckDB 0.10+ は `COPY TO '/dev/stdout'` が可能

→ **ローカルファイル不要**

---

## Bash：最速・最軽量 compact（本命）

```bash
aws s3 cp s3://my-bucket/table/ - --recursive --quiet \
| aws s3 cp s3://my-bucket/table-update/ - --recursive --quiet \
| duckdb -c "
CREATE TABLE merged AS
SELECT * FROM read_jsonl_auto('/dev/stdin');

CREATE TABLE compact AS
SELECT *
FROM (
  SELECT *,
         ROW_NUMBER() OVER (PARTITION BY id ORDER BY ts DESC) rn
  FROM merged
)
WHERE rn = 1;

COPY (SELECT * FROM compact) TO '/dev/stdout' (FORMAT JSONL);
" \
| aws s3 cp - s3://my-bucket/table-compact/compact-$(date +%s).jsonl
```

特徴：

- **ディスク使用量ゼロ**
- **aws s3 cp → DuckDB → aws s3 cp の 3 段ストリーム**
- 100GB〜1TB の JSONL でも安定

---

# =========================================

# ⑤ compact 後の後処理

compact 終了後：

- `table/` と `table-update/` の古いファイルを削除
- 最新 compact を `table/` に移して新しい base とする

```bash
aws s3 rm s3://my-bucket/table/ --recursive
aws s3 rm s3://my-bucket/table-update/ --recursive

aws s3 cp s3://my-bucket/table-compact/compact-XXXX.jsonl \
          s3://my-bucket/table/base.jsonl
```

更新はまた append & update が溜まったら compact。

---

**「S3 Select を併用した差分取得高速化」** を
あなたのユースケース（巨大 JSONL / 1 行 1MB / append + update / compact 運用）向けに
**完全ストリーム構成で最適化したベストプラクティス** としてまとめます。

---

# 0. 背景 ― なぜ S3 Select が効くか？

### 目的

- compact のたびに **全 JSONL を読み直すのは遅い**
- append/update ファイルの _うち、更新対象だけを抽出_ したい

### S3 Select ができること

- S3 内の JSON あるいは CSV をフィルタして返す
- 「該当レコードだけ」を **S3 側で抽出 → ネットワーク転送を大幅削減**

あなたのケースでは：

### \*\*最新 compact で保持している id 一覧を元に

append/update のうち “新規 id または更新対象 id” だけを S3 Select で抽出する\*\*

これが最適。

---

# 1. compact 直後の状態

```
base/compact-XXXX.jsonl         ← 最新正本
append/*.jsonl
update/*.jsonl
```

compact 時には：

- base の id/ts は最新状態
- append/update に新規ファイルが増えている

差分 compact では：

→ **append/update のうち、base にない id だけ、または base より新しい ts の id だけ**
を抽出すればよい。

---

# 2. S3 Select 条件式（JSONLines 用）

AWS S3 Select は JSONLines に対して SQL を投げられる。

形式：

```sql
SELECT s.id, s.blob, s.ts
FROM S3Object s
WHERE s.id IN [ ... ]        -- または
      s.ts > '2025-01-01'    -- など
```

---

# 3. 差分取得パターン（3 つの方法）

---

# パターン A: 「compact で使った base.jsonl の id 一覧」を保持する

→ 次の compact では _base に存在しない id だけ取得_ する

### ■ Bash: base.jsonl の id 一覧を抽出

```bash
aws s3 cp s3://mybucket/base/compact.jsonl - \
  | jq -r '.id' > ids_base.txt
```

### ■ append の新規 id を S3 Select で抽出

（※ あらかじめ 500〜5,000 件単位に分割してバッチ処理）

```bash
IDS=$(paste -sd, ids_batch.txt)

aws s3api select-object-content \
  --bucket mybucket \
  --key append/file1.jsonl \
  --expression "SELECT s.* FROM S3Object s WHERE s.id IN [$IDS]" \
  --expression-type SQL \
  --input-serialization '{"JSON": {"Type":"LINES"}}' \
  --output-serialization '{"JSON": {}}' \
  output.jsonl
```

### 効果

- append のうち必要な id の行だけ返ってくる
- append が 1TB あっても、返すのは数 MB

---

# パターン B: 「timestamp-based 差分」

compact 時点の最大 ts を記録する。

例：

```
max_ts = "2025-11-30T13:20:00Z"
```

### ■ S3 Select で ts > max_ts の行だけ抽出

```bash
aws s3api select-object-content \
  --bucket mybucket \
  --key append/file1.jsonl \
  --expression "SELECT s.* FROM S3Object s WHERE s.ts > '2025-11-30T13:20:00Z'" \
  --expression-type SQL \
  --input-serialization '{"JSON": {"Type":"LINES"}}' \
  --output-serialization '{"JSON": {}}' \
  output.jsonl
```

### 効果

- append/update のうち、timestamp が進んでいるレコードだけ取得
- 変更が少ないほど劇的に高速化（最速パターン）

---

# パターン C: 「S3 Select + Bloom Filter（DuckDB 側）」

append/update のほうが巨大な場合に有効。

流れ：

1. base.jsonl → DuckDB → `SELECT DISTINCT id` を取得
2. その id を Bloom Filter に変換（高速で 100 万 ID を保持可能）
3. append/update を stream → 1 行ずつ Bloom Filter で判定 →
   hit のみ S3 Select に通す

### ※ S3 Select の前で “id が存在する可能性があるか？” を高速判定できる

→ 大量の不要行が最初から除外されるため最速。

---

# 4. 完全ストリーム構成（最高速版）

S3 Select だけで必要行を抽出しながら
DuckDB に pipe で送り compact。

### ■ Bash（本命ストリーム）

以下の関数が _append/update の必要行だけを S3 Select で抽出_ する。

```bash
select_diff() {
  local key=$1
  local max_ts=$2

  aws s3api select-object-content \
    --bucket mybucket \
    --key "$key" \
    --expression "SELECT s.* FROM S3Object s WHERE s.ts > '$max_ts'" \
    --expression-type SQL \
    --input-serialization '{"JSON": {"Type":"LINES"}}' \
    --output-serialization '{"JSON": {}}' \
  | jq -c '.'
}
```

---

### ■ 差分行だけで compact（完全ストリーム）

```bash
MAX_TS="2025-11-30T13:20:00Z"

(
  # まず base を全部投入
  aws s3 cp s3://mybucket/base/compact.jsonl -

  # append/update から差分だけ S3 Select 抽出
  for f in $(aws s3 ls s3://mybucket/append/ | awk '{print $4}'); do
    select_diff "append/$f" "$MAX_TS"
  done

) | duckdb -c "
CREATE TABLE merged AS
SELECT * FROM read_jsonl_auto('/dev/stdin');

CREATE TABLE compact AS
SELECT *
FROM (
  SELECT *,
         ROW_NUMBER() OVER (PARTITION BY id ORDER BY ts DESC) rn
  FROM merged
)
WHERE rn = 1;

COPY (SELECT * FROM compact) TO '/dev/stdout' (FORMAT JSONL);
" \
| aws s3 cp - s3://mybucket/base/compact-$(date +%s).jsonl
```

### 解説

- **base** はすべて読み込む（1 つの compact ファイルなので軽い）
- **append/update** は S3 Select で差分行だけ抽出
- duckdb にストリームで渡して compact
- 結果もストリームで S3 に書き戻す

### ✔ メリット（大規模データに強い）

- 100GB〜10TB append でも差分数が少なければ超高速
- S3 Select が実質フィルターとして働く
- ローカルに 1 バイトも保存しない
- メモリ使用量は DuckDB のクエリで必要な範囲内のみ

---

---

**クラウド（S3・Athena）の ETL では Parquet が最速で最適。Arrow IPC はほぼ不要。**

形式 向いている用途
Parquet S3 ベースの ETL、Athena、Spark、Redshift、データレイク、長期保存、巨大データ
Arrow IPC Python/Rust 間のデータ転送、ローカル高速処理、メモリ分析

Parquet をローカルで読み書きすれば 1GB/s 以上

クラウドベース ETL では、I/O を高速化しても“ネットワーク転送”がボトルネックになるため、Parquet や Arrow IPC の高速性が十分に活きないケースは多い」。
ただし実際には 「ネットワーク転送を減らす設計をすれば、Parquet/Arrow の効果は大きい」

Parquet/Arrow は圧縮・エンコードが効くので、
CSV と比べて転送量が 1/5〜1/20 になることが多い。
「圧縮でデータ量を減らす → 転送自体が速くなる」。

「S3 → ETL → S3」パイプラインを高速化する

| 順位 | 高速化方法                       | 効果                    |
| ---- | -------------------------------- | ----------------------- |
| 1    | 同一リージョン・VPC 内で完結     | 圧倒的に重要            |
| 2    | Parquet/Arrow にフォーマット変換 | 転送量削減で全体が高速  |
| 3    | DuckDB を使用                    | S3 直読み＋ S3 書き出し |
| 4    | S3 Select で部分読み取り         | 大幅な転送量削減        |
| 5    | EC2 (10〜100Gbps) を使う         | ETL の処理速度向上      |
| 6    | Athena CTAS に置き換える         | サーバレスで高速        |
| 7    | 多ファイル並列処理               | S3 の並列帯域を活かす   |

**Parquet ファイル自体は勝手に分割されません**。
「1 つの Parquet ファイルは 1 つのファイルのまま」です。
しかし、以下の “Row Group” という仕組みで **内部的には分割された構造** を持ちます。

---

# 1. Parquet は「ファイル」では分割されない

Parquet は **単一ファイルで数十 GB〜数百 GB** でも問題なく扱えます。

---

# 2. Parquet の内部構造は「Row Group」で分割される

Parquet の中身はこういう構造になっています。

```
Parquet File
 ├─ Row Group 1  (例: 64MB)
 │    ├─ Column Chunk (col1)
 │    ├─ Column Chunk (col2)
 │    └─ …
 ├─ Row Group 2
 └─ …
```

Row Group は通常 **64MB〜128MB の固定サイズ**（ライブラリにより異なる）で作られます。

そのため：

- **巨大ファイルでも Row Group 単位で並列読み込み可能**
- **必要なカラムだけ読み込める（カラムナ型）**
- メモリ効率が良くなる
- I/O が高速になる

---

# 3. 「分割したい場合」は自分で複数ファイルに書き出す必要がある

例：PyArrow / Polars / Spark などで複数ファイルに書き出す方法

```
data/
  part-0001.parquet
  part-0002.parquet
  part-0003.parquet
```

これは **ライブラリ側で “複数 Parquet ファイルのディレクトリ”** を作る方式で、

- Spark
- DuckDB
- Polars
- PyArrow

どれも **ディレクトリを Parquet Dataset として扱う** ので便利です。

---

# 4. 1 つの大きな Parquet ファイルを分割したい場合

DuckDB か PyArrow が最も簡単です。

DuckDB:

```sql
COPY (SELECT * FROM 'big.parquet')
TO 'out_dir' (FORMAT PARQUET, PARTITION_BY ('chunk'));
```

PyArrow:

```python
pq.write_to_dataset(table, root_path='out_dir', max_rows_per_file=5_000_000)
```

---

**Parquet は部分更新（update-in-place）ができません。**
大きなテーブルの一部だけを書き換えることは「基本的に不可能」です。ただし代替手段はいくつかあります。

---

# Parquet が部分更新できない理由

Parquet は **カラムナ圧縮＋ Row Group 単位のブロック構造**を持つため、
ファイルの真ん中だけ編集することができません。

```
Parquet File
 ├─ Row Group 1
 ├─ Row Group 2   ← ここを更新したい → ファイル全体の再圧縮が必要
 └─ Row Group 3
```

そのため：

- Parquet = append（追記）は可能
- Parquet = update は不可能（再書き込み必要）

---

# 解決策（推奨順）

## 1. **Row Group 単位で再書き込みする**

更新対象の行がどの Row Group にあるかを特定して
その Row Group だけ読み直し → 更新 → 書き出し直す。

しかし PyArrow も DuckDB も
**「Row Group を個別に書き直す API」 は提供していない**ため、

実際には：

- 対象 Row Group を読み込む
- その Row Group を新しい Parquet ファイルとして出力
- 古いファイルから当該 Row Group を除いた部分とマージ

---

## 2. **複数 Parquet ファイル（Dataset）に分割しておき、ファイル単位で更新する**

多くの DWH（BigQuery、Snowflake、Delta Lake、DuckDB など）で採用されている方法。

```
data/
  part-0001.parquet    ← 月別やID範囲ごとに分割
  part-0002.parquet
  part-0003.parquet
```

- 小さい単位（例：100MB〜1GB）にファイルを分ける
- 必要なファイルだけ読み込んで再書き込み

**巨大テーブルを部分更新したいなら、この戦略が最も一般的で現実的。**

---

## 3. **"Transaction Table" 方式（更新用ファイルを別に保存）**

データレイクでよく使われる方法：

```
base.parquet
updates.parquet
```

query 時に

```
base ∪ updates - deletes
```

としてマージします。

---

## 4. **SQLite / DuckDB などの RDBMS に移し、更新後に Parquet に戻す**

もし更新が頻繁なら：

1. SQLite、DuckDB にロード
2. UPDATE を普通に使う
3. 必要なときだけ Parquet に書き出す

---

# 推奨する現実的戦略

更新が必要なら、**最初から Parquet Dataset（複数ファイル）にしておく**べき。

例：ID ごとに 100 万行で分割：

```
data/
  id0_999999.parquet
  id1000000_1999999.parquet
  ...
```

更新が必要なときは該当ファイルだけ処理すればよい。

---

**「小さすぎる Parquet ファイルが大量にある」ことは最悪のアンチパターン** とされています。
理由は単純で、**小ファイルは分散処理の効率を壊す**からです。

---

# なぜ小さすぎる Parquet が問題になるのか

## 1. 分散システムは「ファイル単位でタスクを割り当てる」

```
file1.parquet → Task A
file2.parquet → Task B
file3.parquet → Task C
...
```

数百 KB〜数 MB のファイルが 10 万個あると、

- タスク起動のオーバーヘッドが巨大
- メタデータ（S3 リストなど）アクセスが異常に増える
- スケジューラ負荷が跳ね上がる

結果：
**全体が遅くなる。CPU は暇なのに処理が進まない。**

---

## 2. Parquet の row group メタデータ固定コストが大きい

Parquet ファイルは、たとえデータが少なくても

- schema メタデータ
- row group 定義
- statistics（min/max）
- column chunk のヘッダ

などの固定領域が必要。

1KB のデータでも Parquet ファイルはだいたい **50KB〜150KB** くらいになる。

→ 多数の小ファイルは I/O 効率が悪い。

---

## 3. 圧縮効果が低い

小さな塊は圧縮率が低くなり、

- データサイズが大きくなり
- スキャン時のスループットが落ちる

---

## 4. Parquet は「大きいほど読み込みが速い」設計

Parquet の最適なサイズは一般的には：

- **128 MB ~ 1 GB** （1 ファイル）
- Row Group も同様に **64 MB ~ 128 MB**

分散環境では、
**大きいファイル = 少ないファイル数 = 効率的な task scheduling**
になる。

---

# では小さな Parquet をどうするか？

## → マージして大きな Parquet にまとめる（「コンパクション」）

一般的な workflow：

```
small-files/
  part-0001.parquet  (200 KB)
  part-0002.parquet  (300 KB)
  part-0003.parquet  (500 KB)
  ...
```

これを数 GB〜数十 GB 単位にまとめる：

```
large-files/
  chunk1.parquet  (1.2 GB)
  chunk2.parquet  (1.1 GB)
  chunk3.parquet  (1.3 GB)
```

---

# ベストプラクティス

| ファイルサイズ | コメント                                         |
| -------------- | ------------------------------------------------ |
| 1KB〜5MB       | 最悪。即コンパクションすべき                     |
| 5MB〜20MB      | 良くない                                         |
| 50MB〜500MB    | ベストゾーン                                     |
| 1GB〜2GB       | 許容（ただし大きすぎると単一ワーカーが重くなる） |

---

マージによく使われるツール

DuckDB（推奨）
とても高速。メモリ効率も良い。

COPY (
SELECT _ FROM read_parquet('data/_.parquet')
)
TO 'merged.parquet' (FORMAT PARQUET);

PyArrow
import pyarrow.parquet as pq
import pyarrow as pa

tables = [pq.read_table(f) for f in files]
merged = pa.concat_tables(tables)
pq.write_table(merged, 'merged.parquet')

Polars（高速）
import polars as pl

df = pl.scan_parquet('data/\*.parquet').collect()
df.write_parquet('merged.parquet')

### 「1 つの大きなテーブルを S3 に置く」

と言っても、実務では **1 つの巨大ファイルにはしない**。

### 推奨構成：

```
s3://bucket/table_name/
    part-0000.parquet
    part-0001.parquet
    part-0002.parquet
    ...
```

- **1 ファイルあたり 100MB〜1GB** がベスト
- 小さすぎればマージ（コンパクション）
- 大きすぎれば分割（repartition）

---

# ケース 1：**1 つの巨大な Parquet ファイルとして S3 に置く**（単一ファイル）

**非推奨（実務ではほぼやらない）**

理由：

- 1 つの Parquet が 10GB などになると
  読み込みが 1 worker / 1 CPU しか使えない（並列化できない）
- 部分更新ができないため、
  **たとえ 1 行更新でもファイル全体を書き直し**になる
- 「1 ファイル壊れたらデータ全損」というリスク
- アップロードに時間がかかる（ネットワーク単一ストリーム）

---

# ケース 2：**分割した Parquet（複数ファイル）で 1 テーブルとして S3 に置く**

（一般的な Data Lake の形）

**実務の標準。ベストプラクティス。**

例：

```
s3://bucket/table/
    part-0001.parquet (200MB)
    part-0002.parquet (180MB)
    part-0003.parquet (220MB)
    ...
```

特徴：

- 1 つの巨大テーブルでも、**多数の Parquet に分割**して保管する
- 読み込み時は
  Spark / Presto / DuckDB が「全部を 1 つのテーブルとして扱う」
- 更新処理もファイル単位でコンパクトにできる（小さな差分ファイルを追加 → 後でコンパクション）

S3 の Data Lake は **「フォルダ = テーブル」「ファイル = パーティションの一部」**
という考えが基本。

---

# ケース 3：**あえて分割せず、1GB〜数 GB 単位のファイルで管理**

これは間に位置するケース。

- 1 ファイルは 500MB〜1GB 程度
- ディレクトリ内に約 10〜30 個の Parquet
- 分散処理でも十分高速
- 更新のたびに全ファイルを作り直さなくても済む

最も実務的な構成。

---

Parquet は **バイナリデータ（BLOB）も格納可能**です。ただし、実務上の制約や注意点があります。整理します。

---

# ■ 1. Parquet に BLOB を格納

- **型**

  - Parquet には `BYTE_ARRAY` 型があり、バイナリデータを格納可能

- **用途例**

  - 画像や音声の小規模バイナリ
  - シリアライズした JSON / Protobuf / MsgPack など

- **書き方（PyArrow）**

```python
import pyarrow as pa
import pyarrow.parquet as pq

# BLOB の例
data = [
    {'id': 1, 'blob': b'\x00\x01\x02\x03'},
    {'id': 2, 'blob': b'\x04\x05\x06'}
]

table = pa.Table.from_pylist(data)
pq.write_table(table, 'data.parquet')
```

---

# ■ 2. 1 行あたりの最大サイズ

- Parquet 自体に明確な「1 行の最大サイズ」は公式で規定されていない
- **現実的な制約**

  1. **Arrow / Parquet ライブラリの内部制約**

     - PyArrow / Arrow C++ は **数 GB 以上の単一セルは非推奨**
     - メモリ消費が大きくなり、読み書きが不安定

  2. **処理環境のメモリ制限**

     - 1 行に 1GB の BLOB を入れると、読み込み時に RAM に展開される

  3. **クラウド処理制限**

     - S3 Select は BLOB を列として抽出可能だが、大きすぎるセルは失敗することがある

- 実務上は **数 MB ～ 100MB 程度の BLOB** が安全

---

# ■ 3. 注意点

1. **列指向のメリットが減る**

   - Parquet は列指向圧縮が効くが、巨大 BLOB は圧縮効率が悪くなる

2. **部分抽出（S3 Select）に制限**

   - BLOB を WHERE 条件に使った抽出はできない

3. **分割して格納が望ましい**

   - 大きなバイナリは chunk 化して複数行に分ける方が安全

---

# ■ まとめ

- Parquet は **BYTE_ARRAY 型で BLOB 格納可能**
- 1 行あたりの実務上の上限は **数十 MB ～ 100 MB 程度**
- 巨大 BLOB（数百 MB ～ GB）は避け、必要なら複数行に分割
- 圧縮や部分抽出を活かすなら、BLOB は小さくするのがベスト

**基本的には `file.read()` を使って JPG をバイナリとして Parquet に格納するのが最もシンプルで高速**です。ただし、扱うファイルサイズや数によって注意点があります。整理します。

---

# ■ 1. `file.read()` の利点

1. **直接バイナリを取得**

   - base64 や CSV を経由する必要がなくなる
   - 余計な CPU・I/O 処理が発生しない

2. **Parquet BYTE_ARRAY に直接格納可能**

   ```python
   import pyarrow as pa
   import pyarrow.parquet as pq
   import os

   files = ['./images/img1.jpg', './images/img2.jpg']
   data = [{'file_name': os.path.basename(f), 'blob': open(f,'rb').read()} for f in files]

   table = pa.Table.from_pylist(data)
   pq.write_table(table, 'images.parquet', compression='ZSTD')
   ```

3. **列指向圧縮の恩恵**

   - Parquet 側で ZSTD や Snappy 圧縮が効く
   - base64 による膨張を回避

---

# ■ 2. 注意点

1. **巨大ファイルはメモリ負荷が高い**

   - 100MB 以上の JPG が数千枚あると RAM 消費が膨大
   - 対策：

     - 1 行ずつ Parquet に append する
     - または複数ファイルを chunk に分けて書き込む

2. **並列化で高速化可能**

   - `concurrent.futures.ThreadPoolExecutor` などで複数 JPG を同時読み込み
   - CPU と I/O をフル活用して処理時間を短縮

---

# ■ 3. NG パターン

- **base64 → CSV → Parquet**

  - 無駄にデータが膨張
  - CPU / I/O 負荷が増える
  - 大量 JPG では明らかに遅い

Lambda の主な制限（データサイズに関係）
メモリ上限
128 MB 〜 10 GB

/tmp の一時ディスク
512 MB（デフォルト）
最大 10 GB に変更可能

実行時間
最大 15 分

ネットワーク速度
メモリ量に応じて帯域が変化
1〜3 GB メモリ：数百 Mbps
10 GB メモリ：最大 10 Gbps 近い実効帯域

巨大データを Lambda で ETL する場合は：

S3 → Lambda ストリーミング
chunk 単位で処理（例：100MB ずつ）
結果を S3 に直接書き出し

避けるべき
ファイルを丸ごとダウンロードする（重い）
1 行ずつ DynamoDB に PUT（遅い）
CSV → JSON → CSV のような重い中間形式

Lambda が扱えるデータサイズ

メモリ処理：〜6〜8GB
/tmp を使用：〜10GB
ストリーミング：100GB〜TB クラスでも処理可能

とくに S3 → Lambda → S3 の「ストリーミング変換」は 100GB クラスの ETL で普通に使われている。

**Lambda は 15 分制限があるが、S3→Lambda→S3 の「ストリーミング変換」は、15 分で全ファイルを処理する必要はない。
処理が継続できる仕組みがあるため、100GB〜TB クラスでも現実的に動く。**

# ■ ① Lambda の「実行時間 15 分制限」は確かに存在する

Lambda の 1 回の Invoke は **最大 900 秒（15 分）**。

しかし、大きなファイルを処理する場合でも、Lambda が「全部読み終わるまで動く必要はない」。

---

# ■ ② S3 Select や S3 Object Lambda は「ストリーミング処理」であり、Lambda 側の実行時間とは別

### ● S3 Select → 減ったデータだけを Lambda へストリーム

### ● Lambda は加工後のデータを S3 へストリーム

### ● 全体処理は S3 が行う

### ● Lambda は小さなチャンク単位で処理するだけ

つまり、

- Lambda は **100GB ファイルを丸ごと読まない**
- S3 がデータを **チャンク単位（数 MB）** で送る
- Lambda はその小さなチャンクを **瞬間的に処理して返すだけ**

→ Lambda の実行時間は **数秒〜数十秒で済む**

---

# ■ ③ Lambda のリスタート（Invoke 再実行）で続き処理が可能

AWS 公式も次のように説明しています：

- 「Lambda は S3 からストリームされるデータの各チャンクを順次処理するだけ」
- 「全体の処理時間が 15 分を超えても問題ない」
- 「Lambda は次のチャンクを受ける際に継続動作する」

つまり、Lambda 本体は **処理時間が長いときは複数回 Invoke されるモデル**。

---

# ■ ④ 実際のユースケース

### AWS が公式に述べている用途：

- 100GB クラスの CSV → Parquet 変換
- TB クラスのログをフィルタリング
- ヘッダマージ、列選択、正規化などの軽量 ETL

いずれも S3→Lambda→S3 のストリーミングで実際に利用されている。

Lambda の使い方を **最短・実用・最重要ポイントだけ** に絞って説明します。
AWS で Lambda を扱うときは、以下の 8 ステップだけ覚えれば十分実用できます。

---

# 1. Lambda の役割

Lambda は **サーバを使わずに、数行〜数百行のコードを動かすサービス**。

- サーバ管理不要
- 自動スケール
- 1 回の実行は最大 **15 分**
- トリガー（S3、API Gateway、EventBridge、DynamoDB など）で自動実行

用途の例：

- API
- S3 ファイル処理
- 定期バッチ
- 軽い ETL
- 通知
- Webhook

---

# 2. Lambda の作り方（最短）

## 手順:

```
AWS Console → Lambda → Create function → Author from scratch
```

設定：

- Runtime: Python / Node.js が一般的
- Permissions: デフォルト（後で IAM 権限追加）

---

# 3. コードを書く（Python 例）

```python
def lambda_handler(event, context):
    print('Hello')
    return {'status': 'ok'}
```

保存 → Deploy。

---

# 4. 手動テスト（Test イベント）

Console → Test → event を JSON で作る：

```json
{ "msg": "hello" }
```

---

# 5. 主要イベントトリガーの使い方

Lambda の最大のポイントは「イベントを自動で受けて動く」こと。

## よく使うトリガー 5 つ：

### (1) S3（ファイルアップロード検知）

```
S3 → 新しいファイル → Lambda が実行される
```

用途：CSV 解析、サムネイル生成、ログ処理。

### (2) API Gateway（HTTP API）

```
HTTP → API Gateway → Lambda
```

用途：サーバレス Web API。

### (3) EventBridge（cron）

```
cron → 毎時 / 毎日 実行
```

### (4) DynamoDB Streams

DB 更新 → Lambda で処理。

### (5) SQS

大量メッセージを Lambda で並列処理。

---

# 6. IAM 権限を追加する（最重要）

Lambda から AWS にアクセスするときは、
IAM ロールに権限を付ける必要がある。

例：S3 読み取り権限を追加する

```
AmazonS3ReadOnlyAccess
```

例：S3 読み書き権限：

```
AmazonS3FullAccess
```

（実際は最小権限を設計する）

---

# 7. Lambda の制限（これだけ覚えれば OK）

| 項目            | 値                         |
| --------------- | -------------------------- |
| 実行時間        | 15 分                      |
| メモリ          | 128MB〜10GB                |
| /tmp ストレージ | 512MB〜10GB                |
| 同時実行        | 無制限（初期バーストあり） |
| 最大 payload    | ~6MB（同期）               |

重要：

- **大きいファイルは Lambda で read しない（S3 にやらせる）**
- **CPU はメモリ容量に比例して増える**

---

# 8. S3 → Lambda → S3 のストリーミング処理例（超重要）

100GB の CSV を加工する場合、
次のようなコードだけで済む：

```python
def lambda_handler(event, context):
    for record in event['Records']:
        data = record['payload']
        # data は小さなチャンク
        processed = transform(data)
        yield processed
```

Lambda は巨大ファイル全体を読む必要がない。

---

# まとめ：Lambda は「軽い処理をイベント駆動で動かすサーバレス関数」

▼ Lambda を使う典型パターン

1. S3 にファイルが置かれる
2. Lambda が数秒で部分処理
3. 結果を S3 へ保存
4. 100GB でも処理可能（ストリーミング）

Athena は 大規模データの ETL を最もシンプルかつ高速に実行できるサービスです。
Lambda や EC2 と違って データを移動せずに、S3 上で直接処理するため、実質的に「データサイズの上限がない」点が最大の強みになります。

Athena なら 何百 GB 〜 数十 TB の ETL でも普通に処理できる

Athena は Presto/Trino ベースの分散クエリエンジンで、内部で大量のノードを使って並列実行します。

100GB〜数 TB のテーブル → 数十秒〜数分で処理可能
CTAS（Create Table As Select）で Parquet に変換 → 数十倍高速

Athena 自体にデータサイズ上限はほぼ無い
データコピーも不要
S3 内部帯域（何十〜100Gbps）を使用

| 項目             | Athena             | Lambda                               |
| ---------------- | ------------------ | ------------------------------------ |
| データサイズ     | **TB 級まで余裕**  | 数 GB 〜 100GB（ストリーミング必須） |
| 速度             | **分散処理で高速** | 単体処理なので遅い                   |
| パイプライン構築 | 非常に簡単         | コード必要                           |
| コスト           | スキャン量のみ課金 | 実行時間＋メモリ課金                 |
| ETL 向き？       | **最強**           | 軽量 or 小規模処理向け               |
| CSV → Parquet    | **最速**           | Lambda でも可だが遅い                |

| 項目       | **S3 Select**                      | **Athena**                                |
| ---------- | ---------------------------------- | ----------------------------------------- |
| 目的       | **オブジェクト単位で部分抽出**     | **大規模データの SQL 分散処理**           |
| 処理範囲   | 1 つのファイル（オブジェクト）単位 | S3 全体・巨大データセット                 |
| クエリ機能 | 簡易フィルタ（WHERE など）         | JOIN / GROUP BY / CTAS / 集計すべて可能   |
| スケール   | ファイル単発処理                   | 分散 SQL で**TB 級対応**                  |
| ETL 用途   | 簡単な抽出向き                     | **本格的な ETL 向き**（CSV→Parquet など） |
| コスト     | 抽出したデータ量で課金             | スキャンしたデータ量で課金                |
| 利用場所   | Lambda、EC2、アプリ側から利用      | Athena コンソール/CLI/SDK で利用          |

EC2 のスペックに依存

DuckDB はローカルメモリに依存
巨大データ（数百 GB 以上）は RAM / CPU によってボトルネック

S3 Select の制限
ファイル単位の抽出しかできない

JOIN や複数ファイルの結合は不可

ネットワーク帯域の制約
大きなファイルをまるごと読み込むと EC2 の帯域が律速

分散処理は不可
DuckDB 単体は単一マシン処理
複数 EC2 での分散 ETL は別途 Orchestration が必要

| 項目           | **DuckDB**                              | **S3 Select**                        |
| -------------- | --------------------------------------- | ------------------------------------ |
| 処理範囲       | 複雑な SQL、JOIN、集計、UNION、ETL 全般 | 1 ファイルから部分抽出のみ           |
| データ形式     | Parquet/CSV/JSON/IPC など多数           | CSV / JSON / Parquet                 |
| スケール       | ローカルマシン依存（メモリが限界）      | AWS サーバー側で高速部分読み取り     |
| コスト         | 無料（計算はローカルの CPU）            | 使用量に応じた低コスト               |
| 速度           | プロセス内で高速。マシン性能に依存      | 大規模ファイルの部分読みが非常に高速 |
| ネットワーク量 | 大きい（必要なデータを全て取得）        | 超少ない（必要な部分だけ転送）       |
| 用途           | ETL、変換、集計、結合、分析             | 単一ファイルの行/列の抽出            |

**boto3** は Python 用の公式 AWS SDK です。
EC2 から S3 にアクセスする場合、S3 Select も含めて **boto3 で操作するのが標準的**です。

---

# ■ boto3 でできること

1. **S3 操作全般**

   - ファイルのアップロード/ダウンロード
   - バケットの作成・削除
   - オブジェクト一覧取得

2. **S3 Select**

   - 巨大ファイルから必要な行・列だけを抽出
   - SQL 形式で条件指定（WHERE、LIMIT、列指定）
   - CSV / JSON / Parquet に対応

3. **他の AWS サービスとの統合**

   - Athena、Glue、Lambda など

---

# ■ S3 Select の例（Python + boto3）

```python
import boto3

s3 = boto3.client('s3', region_name='ap-northeast-1')

response = s3.select_object_content(
    Bucket='my-input-bucket',
    Key='data.csv',
    ExpressionType='SQL',
    Expression="SELECT s.* FROM S3Object s WHERE s.col1 > 100",
    InputSerialization={'CSV': {"FileHeaderInfo": "USE"}},
    OutputSerialization={'CSV': {}},
)

# 結果を読み取る
for event in response['Payload']:
    if 'Records' in event:
        print(event['Records']['Payload'].decode('utf-8'))
```

| 項目      | boto3                                 | AWS CLI                                |
| --------- | ------------------------------------- | -------------------------------------- |
| 利用環境  | Python プログラム                     | ターミナル / スクリプト                |
| 柔軟性    | 高い（Python で条件分岐やループ可能） | 低い（シェルスクリプトで制御）         |
| 自動化    | Python スクリプトに組み込み可能       | シェルスクリプトや cron に組み込み可能 |
| S3 Select | 可能（`select_object_content`）       | 可能（`s3api select-object-content`）  |

| 項目                    | AWS CLI                              | boto3                                            |
| ----------------------- | ------------------------------------ | ------------------------------------------------ |
| 単純コピー（sync / cp） | 並列・マルチパート自動 → 高速        | Python プログラム制御が必要、並列化は自分で実装  |
| S3 Select               | ターミナルから直接実行               | Python 内でイベント処理必要                      |
| 大量ファイルコピー      | CLI は並列スレッド数調整可能（高速） | デフォルトはシングルスレッド、手動で並列化が必要 |

マルチパート転送とは
大きなファイル（5GB 以上推奨）を複数の小さなチャンクに分割
各チャンクを 同時に（並列）転送
すべてのチャンクが完了したら S3 上で統合
途中で失敗しても、失敗したチャンクだけ再送信可能

AWS CLI は 自動でマルチパート転送 を行う

デフォルトでは aws s3 cp や aws s3 sync が 8MB 以上のファイルを自動で分割
並列スレッド数（--jobs）やチャンクサイズ（--multipart-chunk-size-mb）を指定可能

aws s3 cp bigfile.parquet s3://my-bucket/ \
 --storage-class STANDARD \
 --multipart-chunk-size-mb 100

100MB ごとに分割してアップロード
デフォルトで複数スレッドで並列実行されるため高速

| パラメータ                  | 説明                            | 推奨値                                           |
| --------------------------- | ------------------------------- | ------------------------------------------------ |
| `--multipart-chunk-size-mb` | 1 パートあたりのサイズ          | 100 ～ 200MB（ネットワーク安定していれば大きめ） |
| `--jobs`                    | 並列アップロード/ダウンロード数 | 10 ～ 20（EC2 インスタンスの vCPU に依存）       |
| `--storage-class`           | S3 ストレージクラス             | STANDARD（高速転送重視）                         |
| `--cli-read-timeout`        | タイムアウト調整                | デフォルトより大きめ（長時間転送用）             |



---
---
---

# DuckDBでS3 上の CSV や Parquet を直接クエリ、ローカルへダウンロードなし

* S3 の **CSV / JSON / Parquet** に対してそのまま `SELECT` を実行
* S3 Select ではなく、**DuckDB エンジン側でフィルタしながら読み込む**
* Parquet は **列指向 + プッシュダウン最適化**が効くので高速
* 認証は AWS の `AWS_ACCESS_KEY_ID` / `AWS_SECRET_ACCESS_KEY`、またはセッション設定で指定

---

## 基本的な使い方

### 1. S3 設定（Python）

```python
import duckdb

duckdb.sql("""
SET s3_region='ap-northeast-1';
SET s3_access_key_id='ACCESS_KEY';
SET s3_secret_access_key='SECRET_KEY';
""")
```

### 2. S3 の CSV に直接クエリ

```python
duckdb.sql("""
SELECT *
FROM read_csv_auto('s3://bucket/path/to/data.csv')
WHERE id = 100
""")
```

### 3. S3 の Parquet に直接クエリ

```python
duckdb.sql("""
SELECT user_id, amount
FROM 's3://bucket/path/data.parquet'
WHERE amount > 1000
""")
```

### 4. 複数ファイル（ワイルドカード）

```python
duckdb.sql("""
SELECT *
FROM 's3://bucket/logs/*.parquet'
WHERE status = 'OK'
""")
```

---

## 性能のポイント

### Parquet の場合

* **列単位読み込み**
* **フィルタプッシュダウン**
* 必要な部分だけ S3 から取得 → 高速・低コスト

### CSV の場合

* 全行スキャンになるので Parquet より遅い
* それでも **S3 からストリーミングしながら処理**できる

---


# 2. Bash + DuckDB なら S3 の Parquet / CSV を直接クエリできる


## DuckDB CLI を使った例

### 例：S3 の Parquet に直接クエリ（Bash）

```bash
duckdb -c "
SET s3_region='ap-northeast-1';
SET s3_access_key_id='${AWS_ACCESS_KEY_ID}';
SET s3_secret_access_key='${AWS_SECRET_ACCESS_KEY}';

SELECT *
FROM 's3://mybucket/data/*.parquet'
WHERE amount > 100
LIMIT 10;
"
```

### S3 の CSV に直接クエリ

```bash
duckdb -c "
SET s3_region='ap-northeast-1';
SET s3_access_key_id='${AWS_ACCESS_KEY_ID}';
SET s3_secret_access_key='${AWS_SECRET_ACCESS_KEY}';

SELECT *
FROM read_csv_auto('s3://mybucket/data/file.csv')
WHERE id = 100;
"
```

---
---

# Parquet は「ファイル形式」、Iceberg は「テーブル管理システム」

Parquet を「ディレクトリで管理する」のと、Iceberg で「テーブルとして管理する」の違いは、**“メタデータをどこまで管理できるか”** にあります。

# 1. parquetのディレクトリ管理（Hive-style partitioning）

```
/data/
  year=2024/
    part-0001.parquet
    part-0002.parquet
  year=2025/
    part-0003.parquet
```

* クエリエンジン（DuckDB / Spark / Trino）が
  `/data/` 配下の Parquet を全部スキャン
* パーティション名である程度フィルタ可能（year=2025/ だけ読む）


# 2. Iceberg（メタデータ + 実データ）

```
metadata/
  v1.metadata.json
  v2.metadata.json
  v3.metadata.json   ← これが「今」のスナップショット

data/
  0001.parquet
  0002.parquet
  ...
manifests/
  mf-0001.avro
  mf-0002.avro
```

### ◆ Iceberg が持っているメタ情報

* 各スナップショットで、どの Parquet が有効か
* Parquet ファイルごとの min/max 値
* 行数
* 削除ファイルの管理
* パーティションの情報
* スキーマのバージョン

### ◆ Iceberg の特徴

* **UPDATE / DELETE ができる**
* **誤更新しても snapshot rollback できる**
* **大量ファイルでも manifest を読むだけで高速プランニング**
* **transaction commit（atomic commit）** により中途半端な状態が発生しない
* **小さなファイル問題をコンパクションで解決**
* **スキーマを変更しても安全**



# 機能比較

| 機能                       | Parquet をディレクトリで管理 | Iceberg                    |
| ------------------------ | ------------------ | -------------------------- |
| SELECT                   | ○（読み取れる）           | ○（高速）                      |
| WHERE で min/max pushdown | △（ファイル単位のみ）        | ◎（manifest により最小限ファイルだけ読む） |
| UPDATE                   | ✕                  | ◎                          |
| DELETE                   | ✕                  | ◎                          |
| MERGE INTO               | ✕                  | ◎                          |
| スナップショット                 | ✕                  | ◎                          |
| タイムトラベル                  | ✕                  | ◎                          |
| スキーマ進化                   | △                  | ◎                          |
| ファイル増対策              | ✕（自分でやる）           | ◎（Iceberg が管理）             |
| トランザクション                 | ✕                  | ◎                          |

---




Iceberg with Duckdb

LOAD 'httpfs';
LOAD 'iceberg';

SET s3_region='ap-northeast-1';
SET s3_access_key_id='${AWS_ACCESS_KEY_ID}';
SET s3_secret_access_key='${AWS_SECRET_ACCESS_KEY}';
SET s3_session_token='${AWS_SESSION_TOKEN}';

CREATE TABLE iceberg_write('s3://bucket/table')
AS SELECT * FROM parquet_scan('data.parquet');

CREATE TABLE iceberg_write('s3://mybucket/warehouse/table')
AS SELECT * FROM read_csv_auto('data.csv');

CREATE TABLE iceberg_write('s3://bucket/table')
AS SELECT * FROM read_json_auto('data.jsonl');


Iceberg テーブルはすべて Parquet + Metadata で構成されているので、
CSV / JSONL は DuckDB が内部メモリで DataFrame に変換
DuckDB が Iceberg writer で Parquet に変換
metadata.json / manifest-list / manifest を生成し S3 に保存
Iceberg テーブルとして完成


table/
  metadata/
    v0001.metadata.json
    snap-*.avro
    manifest-list-*.avro
  data/
    *.parquet


SELECT * FROM iceberg_scan('s3://bucket/warehouse/table');


**複数ファイル（CSV / Parquet / JSONL など）を 1 つの Iceberg テーブルへ変換**

```sql
CREATE TABLE iceberg_write('s3://bucket/table')
AS SELECT * FROM parquet_scan('data/*.parquet');
```

```sql
CREATE TABLE iceberg_write('s3://bucket/table')
AS SELECT * FROM read_csv_auto('data/*.csv');
```

```sql
CREATE TABLE iceberg_write('s3://bucket/table')
AS SELECT * FROM read_json_auto('data/*.jsonl');
```

```sql
CREATE TABLE iceberg_write('s3://mybucket/ice/table')
AS SELECT * FROM read_csv_auto('s3://mybucket/input/*.csv');
```

# Append（追加書き込み）する場合

```sql
CREATE TABLE iceberg_write('s3://bucket/table')
AS SELECT * FROM read_csv_auto('data/batch1/*.csv');
```

追加バッチ：

```sql
INSERT INTO iceberg_write('s3://bucket/table')
SELECT * FROM read_csv_auto('data/batch2/*.csv');
```

```
metadata/
  v1.metadata.json
  v2.metadata.json ← INSERT 追加で生成
  manifest-list-*.avro
  manifest-*.avro
```

---




# Iceberg CLI

# ■ 0. Iceberg CLI の準備

Docker で使うのが最も簡単：

```bash
docker run -it --rm \
  -v $(pwd):/work \
  apache/iceberg:latest
```

内部で `/work` を操作できます。

---

# ■ 1) CSV → Iceberg に変換

```bash
iceberg create s3://bucket/table \
  --schema id:int,name:string,price:double \
  --partition-spec "bucket(16,id)"

iceberg add-files s3://bucket/table \
  --format csv \
  --files data/*.csv
```

`add-files` が “CSV → Parquet 変換” を自動で行います。

---

# ■ 2) Parquet → Iceberg に変換（最速）

Parquet の場合は **そのまま追加**できます。

```bash
iceberg create s3://bucket/table
iceberg add-files s3://bucket/table --files data/*.parquet
```

内部で manifest と metadata だけ作成されます。

---

# ■ 3) JSONL → Iceberg に変換

Iceberg CLI は JSONL → Parquet 変換も対応。

```bash
iceberg create s3://bucket/table
iceberg add-files s3://bucket/table --format json --files data/*.jsonl
```


# DuckDB と Iceberg CLI の使い分け

| 操作             | DuckDB | Iceberg CLI        |
| -------------- | ------ | ------------------ |
| 初回の Iceberg 作成 | ◎ 最も簡単 | △ 事前に schema 指定が必要 |
| Append         | ◎ 超簡単  | ◎ 公式               |
| UPDATE         | × 未対応  | ◎ 完全対応             |
| DELETE         | × 未対応  | ◎ 完全対応             |
| MERGE          | ×      | ◎                  |
| 巨大データの取り込み     | ◎ 高速   | ◎ 高速               |

DuckDB ＝ **読み取り・初回作成・append に最適**
Iceberg CLI ＝ **更新・削除・変換に最適**

---


## ■ 1) 大量 CSV → Iceberg の初回作成

DuckDB で一括変換（1行のみ）：

```sql
CREATE TABLE iceberg_write('s3://bucket/table')
AS SELECT * FROM read_csv_auto('s3://bucket/csv/*.csv');
```

## ■ 2) 更新/削除は Iceberg CLI

```bash
iceberg update s3://bucket/table --set "x = x + 1" --where "id = 5"
iceberg delete s3://bucket/table --where "status = 'DELETED'"
```


**Iceberg CLI だけで Iceberg をフル操作できる完全チートシート**

---

# ============================================

# Iceberg CLI 完全チートシート（2025 最新）

# ============================================

# --------------------------------------------

# ■ 0. 基本

# --------------------------------------------

## CLI 起動（Docker）

```bash
docker run -it --rm \
  -v $(pwd):/work \
  apache/iceberg:latest
```

内部で `/work` が作業ディレクトリ。

---

# --------------------------------------------

# ■ 1. Iceberg テーブルの作成

# --------------------------------------------

## ▼ 1-1）完全自動（スキーマ自動推論）

Parquet ファイルを種にして作成：

```bash
iceberg create s3://bucket/db/table \
  --from-files data/*.parquet
```

> Parquet のスキーマをそのまま Iceberg のスキーマに採用。

---

## ▼ 1-2）手動でスキーマ定義

```bash
iceberg create s3://bucket/db/table \
  --schema id:int,name:string,price:double \
  --partition-spec "bucket(16,id)"
```


---

# --------------------------------------------

# ■ 2. ファイル追加（append）

# --------------------------------------------

## ▼ 2-1）Parquet を Iceberg に追加（最速）

```bash
iceberg add-files s3://bucket/db/table \
  --files data/*.parquet
```

> Parquet は内部変換なし。manifest だけ作る。

---

## ▼ 2-2）CSV を Iceberg に追加（内部で Parquet 化）

```bash
iceberg add-files s3://bucket/db/table \
  --format csv \
  --files data/*.csv
```

---

## ▼ 2-3）JSON / JSONL を追加

```bash
iceberg add-files s3://bucket/db/table \
  --format json \
  --files data/*.jsonl
```

---

# --------------------------------------------

# ■ 3. 行レベル UPDATE

# --------------------------------------------

DuckDB ではできないが Iceberg CLI は対応。

## ▼ 3-1）単純 UPDATE

```bash
iceberg update s3://bucket/db/table \
  --set "price = price * 1.1" \
  --where "category = 'Book'"
```

---

## ▼ 3-2）複数カラムの UPDATE

```bash
iceberg update s3://bucket/db/table \
  --set "price = price * 1.1", "updated_at = now()" \
  --where "id = 100"
```

---

## ▼ 3-3）複数条件

```bash
iceberg update s3://bucket/db/table \
  --set "amount = 0" \
  --where "status = 'CANCELLED' AND amount > 0"
```

---

# --------------------------------------------

# ■ 4. DELETE（行削除）

# --------------------------------------------

## ▼ 4-1）単純 DELETE

```bash
iceberg delete s3://bucket/db/table \
  --where "id = 10"
```

---

## ▼ 4-2）条件付き DELETE

```bash
iceberg delete s3://bucket/db/table \
  --where "ts < timestamp '2024-01-01'"
```

---

# --------------------------------------------

# ■ 5. MERGE（UPSERT）

# --------------------------------------------

MERGE まで CLI だけで可能。

```bash
iceberg merge s3://bucket/db/table \
  --key "id" \
  --records updates.jsonl
```

`updates.jsonl` は行単位のデータ。

---

# --------------------------------------------

# ■ 6. スナップショット管理（Time Travel）

# --------------------------------------------

## ▼ 6-1）スナップショット一覧

```bash
iceberg snapshots s3://bucket/db/table
```

---

## ▼ 6-2）特定スナップショットへロールバック

```bash
iceberg rollback s3://bucket/db/table --to <snapshot-id>
```

---

## ▼ 6-3）時刻指定でロールバック

```bash
iceberg rollback s3://bucket/db/table --to-timestamp "2024-01-01T00:00:00Z"
```

---

# --------------------------------------------

# ■ 7. GC（不要ファイルの削除）

# --------------------------------------------

Iceberg は古い metadata / manifest / データファイルを残すため
GC が必要。

## ▼ 7-1）有効でないファイルの削除

```bash
iceberg expire s3://bucket/db/table
```

---

## ▼ 7-2）「30日以上前のスナップショットを削除」

```bash
iceberg expire s3://bucket/db/table \
  --older-than "30d"
```

---

## ▼ 7-3）特定ファイルを手動削除するためのリスト

```bash
iceberg orphan s3://bucket/db/table
```

---

# --------------------------------------------

# ■ 8. Iceberg → Parquet（エクスポート）

# --------------------------------------------

```bash
iceberg export s3://bucket/db/table --output export_dir/
```

---

# --------------------------------------------

# ■ 9. Iceberg metadata の確認

# --------------------------------------------

## ▼ 9-1）スキーマ表示

```bash
iceberg schema s3://bucket/db/table
```

## ▼ 9-2）パーティション spec

```bash
iceberg partition-spec s3://bucket/db/table
```

## ▼ 9-3）manifest の確認

```bash
iceberg manifests s3://bucket/db/table
```

## ▼ 9-4）metadata.json の中身

```bash
iceberg metadata s3://bucket/db/table
```

---

# --------------------------------------------

# ■ 10. テーブル削除

# --------------------------------------------

```bash
iceberg drop s3://bucket/db/table
```

---


# ETL パイプラインの完全自動化（bash × DuckDB）

```bash
#!/bin/bash

S3_RAW="s3://bucket/raw/users/*.csv"
ICEBERG_TABLE="s3://bucket/iceberg/etl/raw_users"

duckdb <<EOF
SET s3_region='ap-northeast-1';
SET s3_access_key_id='xxx';
SET s3_secret_access_key='xxx';

-- Extract
CREATE OR REPLACE TABLE raw_input AS
SELECT * FROM read_csv_auto('$S3_RAW');

-- Transform
CREATE OR REPLACE TABLE transformed AS
SELECT
  id::BIGINT,
  initcap(name) AS name,
  age,
  now() AS updated_at
FROM raw_input
WHERE age > 0;

-- Load
INSERT INTO iceberg_write('$ICEBERG_TABLE')
SELECT * FROM transformed;
EOF
```

