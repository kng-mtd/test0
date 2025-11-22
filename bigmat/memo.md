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
