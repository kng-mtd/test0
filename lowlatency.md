# MQTT

https://chatgpt.com/c/6993690f-29ec-8322-9a93-43e4fb6967d6

sudo apt install -y mosquitto mosquitto-clients

## MQTT broker

ls -l /etc/mosquitto/  
less /etc/mosquitto/mosquitto.conf  
ls -l /var/log/mosquitto/

systemctl status mosquitto  
sudo systemctl start mosquitto  
sudo systemctl enable mosquitto  
sudo systemctl stop mosquitto  
sudo systemctl disable mosquitto

ss -lntp | grep 1883

start mqtt broker on defalut listen port 1883

mosquitto -p 1883

**ログを確認 verbose モード**

mosquitto -v  
mosquitto -p 1883 -v > mosquitto.log 2>&1

sudo tail -f /var/log/mosquitto/mosquitto.log

**journalctl**

journalctl -u mosquitto -f

**最小構成で起動**

mosquitto -c /dev/null -v

**バックグラウンド**

mosquitto -d

## MQTT publisher/subscriber

terminal A  
mosquitto_sub -h localhost -t test/topic0

terminal B  
mosquitto_pub -h localhost -t test/topic0 -m msg0

or

mosquitto_sub --- &
ps
mosquitto_pub ---
fg

**Topic のワイルドカードを理解する**

`+`（1階層）
mosquitto_sub -t 'sensor/+/temp'

`#`（すべて）  
mosquitto_sub -t 'sensor/#'

**ファイル送信**

mosquitto_pub -t test/topic0 -f data.json

**retain（状態を覚えさせる）**

mosquitto_pub -t status/server -m 'online' -r

あとから sub すると最後の値が即届く

mosquitto_sub -t status/server

**QoS を試す（0 / 1 / 2）**

mosquitto_pub -t qos/test -m 'qos1' -q 1  
mosquitto_sub -t qos/test -q 1

| QoS | 意味                           |
| --- | ------------------------------ |
| 0   | at most once（速い・欠損あり） |
| 1   | at least once（重複あり）      |
| 2   | exactly once（最重）           |

**クライアントIDを指定**

mosquitto_sub -t test/topic0 -i sub1  
mosquitto_pub -t test/topic0 -m msg0 -i pub1

**クリーンセッション無効（再接続時に受信）**

mosquitto_sub -t test/topic0 -q 1 -c -i sub1

- `-c` : clean session = false
- `-i` : client id

**設定ファイルを読む**

less /etc/mosquitto/mosquitto.conf

- `listener 1883`
- `allow_anonymous true`
- `persistence false`
- `log_dest`

**設定ファイル指定**

mosquitto -c /etc/mosquitto/mosquitto.conf

**匿名接続を明示的に許可**

sudo nano /etc/mosquitto/conf.d/local.conf

listener 1883  
allow_anonymous true  
sudo systemctl restart mosquitto

**anonymous 無効（設定ファイル）**

allow_anonymous false  
password_file /etc/mosquitto/passwd

**パスワード作成**

mosquitto_passwd -c /etc/mosquitto/passwd user1

**認証付き pub/sub**

mosquitto_pub -t test/topic -m hi -u user1 -P pass  
mosquitto_sub -t test/topic -u user1 -P pass

## MQTT publisher performance measurement

only publish

time seq 1000000 | mosquitto_pub -h localhost -t test -q 0 -l # `-l` : read from stdin

publish + subscribe on the same server

mosquitto_sub -t test > /dev/null &
time seq 1000000 | mosquitto_pub -h localhost -t test -q 0 -l

ps
pkill mosquitto_sub

1k massages from 1k pubisher

time (
for j in $(seq 1000); do
seq 1000 | mosquitto_pub -t test/topic -q 0 -l &
done
wait
)

### MQTTで性能評価するときの指標

まず「何を測るか」を固定します。

| 指標             | 意味                           |
| ---------------- | ------------------------------ |
| Throughput       | 秒間メッセージ数               |
| Latency          | publish → subscribe までの遅延 |
| Fan-out          | 1 pub → N sub の性能           |
| Connection scale | 同時接続数                     |
| Payload size     | メッセージサイズ耐性           |
| QoS cost         | QoS 0/1/2 の差                 |
| Retain cost      | retain のオーバーヘッド        |

mosquitto_sub -t test > /dev/null &

### ペイロードサイズの影響

time dd if=/dev/zero bs=1000 count=1000 | base64 \
|mosquitto_pub -t test -l

| サイズ | 傾向       |
| ------ | ---------- |
| < 1KB  | 超高速     |
| 10KB   | まだ軽い   |
| 100KB  | 急に落ちる |
| >1MB   | MQTT用途外 |

### QoS別性能差

mosquitto_pub -t test -m msg0 -q 0  
mosquitto_pub -t test -m msg1 -q 1  
mosquitto_pub -t test -m msg2 -q 2

### Fan-out（1→多）

for i in $(seq 1000); do  
 mosquitto_sub -t test > /dev/null &  
done

mosquitto_pub -t test -m msg0

- subscriber 数に **ほぼ線形に負荷増**
- Mosquitto は fan-out が非常に強い

### 同時接続数テスト（簡易）

for i in $(seq 1 1000); do  
  mosquitto_sub -t test -i sub$i &  
done

ss -ant | grep 1883 | wc -l

### ログで内部挙動を見る

sudo tail -f /var/log/mosquitto/mosquitto.log

- client connected
- socket error
- dropped message

---

## Mosquitto の「多数 client 接続テスト」

### 0. 前提

mosquitto -c /dev/null -v

- `/etc/mosquitto/conf.d/*.conf` を読まない
- 永続化・ACL・ログ I/O を切る
- **純粋な接続性能・スループット測定**になる

---

### 1. mosquitto-clients だけでの簡易接続テスト

#### 1-1. Subscriber を大量に起動（bash）

for i in $(seq 1 1000); do  
  mosquitto_sub -t test/topic -i sub$i -q 0 &  
done

ps aux | grep mosquitto_sub | wc -l

#### 1-2. Publisher を投下

mosquitto_pub -t test/topic -m "hello"

→ **全 subscriber が受信できるか**を確認

---

### 2. 本格的負荷テスト（mosquitto_rr / mosquitto_pub loop）

#### 2-1. 高頻度 publish（1 client）

while true; do
mosquitto_pub -t test/topic -m "$(date +%s%N)"
done

top

#### 2-2. 並列 Publisher（100 client）

for i in $(seq 1 100); do
  (
    while true; do
      mosquitto_pub -t test/topic -m "p$i"
done
) &
done

観察ポイント:

- broker CPU
- message drop
- subscriber の遅延

---

### 3. 接続数スケールテスト

#### 3-1. 接続だけして publish しない

for i in $(seq 1 5000); do
  mosquitto_sub -t idle/topic -i idle$i &
done

ss -tan | grep 1883 | wc -l

→ **何 client まで落ちずに接続できるか**

#### 3-2. OS 制限に注意

ulimit -n
ulimit -n 100000

sysctl:

sysctl net.ipv4.ip_local_port_range
sysctl net.core.somaxconn

---

### 4. 計測すべき指標（必須）

| 指標   | 見るコマンド                    |
| ------ | ------------------------------- |
| 接続数 | `ss -tan \| grep 1883 \| wc -l` |
| CPU    | `top`                           |
| メモリ | `free -m`                       |
| 遅延   | publish 時刻 vs receive         |
| 切断   | mosquitto `-v` ログ             |

---

### 5. IoT を想定するなら重要な設計ポイント

- **常時接続を前提にしない**
- publish 間隔をランダム化
- retain を乱用しない
- QoS 1 は最小限
- client ID 再利用禁止

---

# NATS

## server

docker run --rm -it --name nats -p 4222:4222 -p 8222:8222 nats:latest -js

docker ps | grep nats

ss -lntp | grep 4222

curl http://localhost:8222
http://localhost:8222

docker logs nats
nats server check

## producer/consumer

nats sub subject0 &
nats pub subject0 msg0
fg

echo msg0 | nats pub subject0

**subject（トピック）**

foo
foo.bar
foo.bar.baz

**ワイルドカード**

- = 1階層
  > = 全階層

nats sub "foo.\*"
nats sub "foo.>"

**Queue Subscribe（ワーカープール）**

nats sub foo --queue workers

複数立てると **1メッセージ = 1ワーカー** に自動分配。

用途：

- バックエンド処理
- ETL
- 非同期ジョブ

**JetStream（永続化・再送・ACK）**

Stream 作成

nats stream add mystream \
 --subjects "events.>" \
 --storage file

publish

nats pub events.test "hello"

durable consumer

nats consumer add mystream myconsumer
nats consumer next mystream myconsumer

- 永続化
- ACK
- 再送
- Pull / Push

**MQTT との正確な対応関係**

| 概念           | MQTT       | NATS          |
| -------------- | ---------- | ------------- |
| Pub/Sub        | topic      | subject       |
| QoS0           | QoS 0      | Core NATS     |
| QoS1/2         | QoS 1/2    | JetStream     |
| Retain         | retain     | Stream        |
| Consumer Group | shared sub | Queue Sub     |
| RPC            | なし       | Request/Reply |

- Core NATS: **数百万 msg/sec**
- JetStream: 永続化ありでも **数十万 msg/sec**
- MQTT（Mosquitto）: 数万〜十万程度

**モニタリング（HTTP）**

接続数
curl http://localhost:8222/connz

サブスク状況
curl http://localhost:8222/subsz

サーバ統計
curl http://localhost:8222/varz

---

**performance measurement**

nats bench test.subject0 --pub 1 --sub 1 --msgs 1000000 --size 16
nats bench test.subject0 --pub 4 --sub 4 --msgs 1000000 --size 64
nats bench test.subject0 --pub 1 --sub 1 --msgs 1000000 --size 16 --js

多数 subscriber

for i in $(seq 1 100); do
nats sub test.load &
done

接続確認
ss -tan | grep 4222 | wc -l

sudo pkill nats

高頻度 publish

while true; do
nats pub test.load "$(date +%s%N)"
done

**MQTT と併用する典型構成**

```
IoT Device (MQTT)
        |
        v
Mosquitto
        |
        v
NATS Core
        |
        v
Worker / DB / Stream
```

- MQTT = device-facing
- NATS = backend-facing

---

## queue subscriber（ロードバランス）

**NATS Core の queue subscriber**は、**同じ subject を購読している複数 consumer に対して、1 メッセージを 1 consumer だけに配る仕組み**です。

### 通常の subscribe（fan-out）

nats sub job.task

```
Publisher
   |
   v
subA   subB   subC
（全員が受信）
```

- **全 subscriber が同じメッセージを受信**
- ログ配信・通知向け

### queue subscribe（fan-out → fan-in）

nats sub job.task --queue workers

```
Publisher
   |
   v
subA   subB   subC
   \    |    /
     queue group
        ↓
   （誰か1人）
```

- **1 メッセージ = 1 subscriber**
- 自動ロードバランス
- ワーカー処理向け

- NATS サーバが **ラウンドロビン**で振り分け
- 処理速度の速い consumer が **自然に多く受け取る**
- 外部 LB / coordination 不要

### Subscriber（3 ワーカー）

nats sub job.test --queue workers

これを **3ターミナル**で起動

### Publisher

for i in $(seq 1 10); do
nats pub job.test "task $i"
done

- 各 subscriber が **バラバラに task を受信**
- 重複なし

---

### queue 名が違うとどうなる？

nats sub job.test --queue A
nats sub job.test --queue B

```
Publisher
   |
   +--> queue A（1人）
   +--> queue B（1人）
```

- **queue ごとに 1 メッセージ**
- マルチサービス構成に便利

### 注意点（重要）

処理保証はない

- consumer が落ちたら **メッセージは消える**
- ACK / retry なし（Core）

順序保証なし

- 同一 subject でも consumer が違う

---

# MQTT、NATS比較

## 1. 設計思想の違い（性能差の根本原因）

| 観点       | MQTT (Mosquitto)   | NATS                          |
| ---------- | ------------------ | ----------------------------- |
| 主用途     | IoT / Edge         | Cloud / Microservices         |
| プロトコル | MQTT（状態ful）    | NATS Protocol（極薄）         |
| セッション | 常時接続・状態保持 | 基本 stateless                |
| QoS        | 0 / 1 / 2          | at-most-once（JetStream除く） |
| 軽量度     | 軽い               | **異常に軽い**                |

**NATSは「性能最優先」設計**

---

## 2. 純性能（目安値・localhost）

### Throughput（QoS 0 相当）

| 指標    | Mosquitto | NATS             |
| ------- | --------- | ---------------- |
| msg/sec | 5万〜15万 | **100万〜300万** |
| latency | 0.5〜2 ms | **0.1〜0.3 ms**  |
| CPU効率 | 良い      | **非常に良い**   |

※ 単一ノード・ローカル・最適条件

---

## 3. Fan-out（1 pub → N sub）

| 条件     | Mosquitto | NATS             |
| -------- | --------- | ---------------- |
| 1 → 10   | ほぼ線形  | 余裕             |
| 1 → 100  | 強い      | **ほぼノーダメ** |
| 1 → 1000 | CPU依存   | **まだ余裕**     |

NATS は **fan-out が異常に強い**。

---

## 4. 同時接続数

| 指標       | Mosquitto  | NATS           |
| ---------- | ---------- | -------------- |
| 同時接続   | 数千〜数万 | **数十万**     |
| 接続コスト | やや重い   | **非常に軽い** |

IoT デバイス大量接続 → MQTT
サービス間大量接続 → NATS

---

## 5. Payload サイズ耐性

| サイズ | Mosquitto | NATS |
| ------ | --------- | ---- |
| < 1KB  | ◎         | ◎    |
| 10KB   | ○         | ◎    |
| 100KB  | △         | ○    |
| 1MB    | ❌        | △    |

**どちらも巨大データは非推奨**
NATSの方がまだ耐える。

---

## 6. 永続化

| 機能         | Mosquitto   | NATS                  |
| ------------ | ----------- | --------------------- |
| 永続キュー   | △（限定的） | **JetStream**         |
| Replay       | 弱い        | **強力**              |
| Exactly once | QoS 2（重） | JetStream（設計次第） |

**NATS + JetStream ≒ Kafka-lite**

---

## 7. 実運用での選択基準

### MQTT を選ぶべきケース

- IoT / センサー
- 不安定ネットワーク
- スリープ・再接続前提
- QoS / retain が必要

### NATS を選ぶべきケース

- マイクロサービス間通信
- 高スループット
- 低レイテンシ
- Cloud / Kubernetes

---

**MQTT → NATS ブリッジの最小構成（bash）**

## 最小ブリッジ（1トピック）

### 構成

```
MQTT (mosquitto)
  └─ test/topic
       ↓
bash pipe
       ↓
NATS subject: sensors.test
```

---

## ワンライナー版（最小）

docker run --rm -it --name nats -p 4222:4222 nats:latest

nats sub subject0 &

mosquitto_sub -h localhost -t topic0 |
while read -r msg; do
nats pub subject0 "$msg"
done &

seq 5 | while read i; do mosquitto_pub -h localhost -t topic0 -m "msg-$i"; done

---

## topic → subject を変換したい場合

### MQTT topic を含める

nats sub 'mqtt.sensors.>' &

mosquitto_sub -v -t sensors/+/data |
while read -r topic msg; do
subj="mqtt.${topic//\//.}"
  nats pub "$subj" "$msg"
done &

mosquitto_pub -h localhost -t sensors/temp/data -m '24.5'
mosquitto_pub -h localhost -t sensors/hum/data -m '60'

---

## QoS / 再接続を最低限考慮

mosquitto_sub \
 -q 0 \
 -R \
 -t sensors/# |
while read -r msg; do
nats pub sensors.raw "$msg" || sleep 0.1
done

- `-R` : retained message 無視
- QoS 0（高頻度前提）

---

## JetStream

JetStream は **Core の弱点を補う層**。

### JetStream が追加するもの

| 機能      | 意味        |
| --------- | ----------- |
| 永続化    | disk 保存   |
| ACK       | 受信保証    |
| Replay    | 再取得      |
| Pull      | 低負荷      |
| Retention | TTL / count |

---

## JetStream を使うとどうなる？

```text
Device → publish
        → JetStream Stream に保存
        → ACK 返却
```

**QoS1 相当**

それでも MQTT に負ける点（重要）

1 プロトコル成熟度

- MQTT は IoT 特化
- 再接続・keepalive が洗練

2 クライアント実装

- JetStream client は heavier
- マイコン向けは限定的

3 電力・帯域

MQTT <<< JetStream

JetStream が「成立する」デバイス条件

Linux device
Gateway / Edge
常時電源
メモリ数十MB以上
再送は QoS1 で十分

Raspberry Pi / Gateway / 車載 / Factory Edge

---

JetStream が「無理」なデバイス

MCU
センサー直結
数KB RAM
超省電力

正しい使い分け

```
[ Sensor / MCU ]
        ↓ MQTT
    Mosquitto
        ↓ bridge
    NATS JetStream
        ↓
  Stream / KV / Consumer
```

---

## ロス許容・高頻度 構成

センサーデータ（高頻度・欠損OK）には「MQTT QoS0 + NATS Core + 非同期集約」が最も強い
JetStream **ではない**のがポイントです。

```
[ Sensor / Device ]
        |
        | MQTT QoS0（fire-and-forget）
        v
   Mosquitto（軽量）
        |
        | bridge / consumer
        v
   NATS Core（超高速）
        |
        | fan-out / buffering
        v
   Aggregator / Processor
        |
        +--> 時系列DB（間引き・集約）
        +--> File / Object Store
```

---

なぜこの構成が強いのか

1 欠損 OK = 再送・永続は不要

センサーデータの特徴

- 毎秒〜毎ミリ秒
- 全点揃わなくてよい
- トレンドが重要

**QoS0 / Core が最適**

2 JetStream を使うと逆に詰まる

JetStream は

- disk write
- ACK
- retention 管理

3 NATS Core は「落ちる前に流す」

NATS Core の思想

- とにかく速く流す
- 遅いやつは置いていく

センサーデータ向き

---

### MQTT QoS0 + NATS Core の役割分担

| 層        | 役割               |
| --------- | ------------------ |
| MQTT      | デバイス接続・安定 |
| NATS Core | 超高速分配         |
| Consumer  | 遅延・欠損吸収     |

欠損を前提にした設計テクニック

1. 間引き（downsampling）

1000 msg/sec → 100 msg/sec

NATS consumer 側で処理

2. 集約（window）

1秒間の avg / min / max

3. 最新値上書き（KV風）

device_id → last_value

※ JetStream KV は使わず **メモリ or LMDB**

スケール特性（重要）

| 増えるもの | どうなる         |
| ---------- | ---------------- |
| device 数  | MQTT で吸収      |
| frequency  | NATS Core が吸収 |
| consumer   | fan-out          |

---

# LMDB

sudo apt install -y liblmdb-dev lmdb-utils
mdb_stat -V

man mdb

## LMDB の CLI（mdb\_\*）主なコマンドの使い方

LMDB は **ライブラリ中心**の設計ですが、実運用・検証で使う CLI はほぼ **`mdb_*` 系だけ**です。

LMDB は **Environment = ディレクトリ** です。

```
/data/lmdb/
  ├─ data.mdb
  └─ lock.mdb
```

CLI は **常にディレクトリを指定**します。

1. mdb_stat

mdb_stat /data/lmdb

```
Map size: 10485760
Page size: 4096
Entries: 1000000
Depth: 3
```

DB 指定（名前付き DB）

mdb_stat -d mydb /data/lmdb

フラグ付き（詳細）

mdb_stat -a /data/lmdb

2. mdb_dump（バックアップ / 中身確認）

全 DB を dump

mdb_dump /data/lmdb > dump.txt

特定 DB のみ

mdb_dump -s mydb /data/lmdb > mydb.dump

バイナリ安全

mdb_dump -p /data/lmdb > dump.bin

3. mdb_load（リストア / 初期投入）

mdb_load /data/lmdb < dump.txt

既存 DB 上書き

mdb_load -f dump.txt /data/lmdb

バイナリ dump から

mdb_load -p /data/lmdb < dump.bin

- 書き込みは **単一 writer**
- load 中は他 writer を止める

4. mdb_copy（本番向け安全バックアップ）

mdb_copy /data/lmdb /backup/lmdb_copy

低負荷モード

mdb_copy -n /data/lmdb /backup/lmdb_copy

**ポイント**

- reader を止めなくてよい
- mmap を壊さない
- **dump より速い**

5. mdb_env（環境チェック）

mdb_env /data/lmdb

- map size
- max readers
- page size

6. mdb_drop（DB 削除・全消し）

mdb_drop -s mydb /data/lmdb

全削除

mdb_drop -d /data/lmdb

7. mdb_chk（整合性チェック）

mdb_chk /data/lmdb

- クラッシュ後の確認

8. その他

| コマンド    | 用途                     |
| ----------- | ------------------------ |
| mdb_get     | 単キー取得（デバッグ用） |
| mdb_put     | 単キー挿入（テスト用）   |
| mdb_del     | 単キー削除               |
| mdb_readers | reader 一覧              |

mdb_readers /data/lmdb

9. 実運用での典型フロー

状態確認

mdb_stat /data/lmdb

安全バックアップ

mdb_copy -n /data/lmdb /backup/$(date +%F)

障害調査

mdb_stat -a /data/lmdb
mdb_chk /data/lmdb

10. 単一キー読み込み：`mdb_get`

mdb_get /data/lmdb mydb mykey

- 第1引数: **Environment ディレクトリ**
- 第2引数: DB 名（省略可）
- 第3引数: key

DB 名なし（メイン DB）

mdb_get /data/lmdb mykey

バイナリキー / 値（16進）

mdb_get -x /data/lmdb mydb deadbeef

失敗時

- key がなければ **無出力**
- exit code ≠ 0

範囲・全件読み込みは、CLI では基本できない

LMDB の CLI には：

- cursor 操作
- range scan
- prefix scan
- limit / order

**が存在しません。**

全件を「見る」唯一の方法

`mdb_dump` を使う（読み込み扱い）

mdb_dump /data/lmdb

ただし：

- **重い**
- 本番では非推奨
- 人間が grep する用途

mdb_dump /data/lmdb | grep sensor123

LMDB は：

- mmap
- zero-copy
- cursor 前提
- トランザクション前提

**CLI で触る DB ではない**

CLI の役割

- 状態確認
- 障害調査
- バックアップ
- 「この key ある？」の即席確認

アプリの役割

- scan
- prefix
- 集計
- join 的処理

---

## lmdbパッケージ

- npm の公式パッケージ **`lmdb`** は、**Node.js / Bun / Deno で LMDB を使うためのインターフェイス**です。
- LMDB の高速・堅牢な特性を活かしつつ、**JavaScript オブジェクトをそのまま保存・取得できるようにラッピング**されています。
- 超高速で効率の良い key-value ストアインターフェイス
- JS のデータ（オブジェクト・配列・Buffer など）を扱える
- ACID（整合性保証）対応
- 同期読み込み + 非同期書き込み
- トランザクション管理やカーソル・バッチ処理も可能
- 圧縮（LZ4）オプションあり

---

インストール

npm install lmdb

基本的な使い方

DB を開く

import { open } from 'lmdb';

let db = open({
path: 'lmdb0',
compression: true
});

- `path`：データ格納ディレクトリ
- `compression`: optional, LZ4 圧縮を有効化

データの保存・取得

await db.put('key1', { key11: 'val11' });
let value = db.get('key1');
console.log(value.key11);

- `put`: 書き込み
- `get`: 取得
- put は非同期 batched 写き込みでスループット改善

トランザクション

db.transaction(() => {
db.put('key2', { key21: 'val21' });
db.get('key2');
});

Range クエリ（範囲取得）

for (let {key,val} of db.getRange({ start, end })) {
...
}

- 範囲スキャンが iterable でできる
- `filter`, `limit`, `offset` など指定可能

複数データベース

let users = db.openDB('users');
let products = db.openDB('products');

1つの LMDB environment 内で複数 DB を管理可能。

エンコーディング

- 鍵・値は JSON だけでなく
  - binary
  - ordered-binary
  - custom encoder
    など対応

パフォーマンスと耐久性

- 内部で LMDB の mmap を使い、読み込みは **同期で超高速**
- 書き込みは非同期 batching で効率的に処理
- デフォルトでは crash-proof（クラッシュしても壊れにくい）設計

---

## Node.js + LMDB における batch 処理設計パターン

**LMDB の性能は「commit 回数」で決まる**

- 1 put = 1 commit ❌
- **N put = 1 commit ✅**

1. 基本パターン①：サイズベース batch（最頻出）

```
import { open } from 'lmdb';

const db = open({ path: './db' });

let queue = [];
const BATCH_SIZE = 1000;

function enqueue(key, value) {
  queue.push([key, value]);
  if (queue.length >= BATCH_SIZE) {
    flush();
  }
}

function flush() {
  if (queue.length === 0) return;

  db.transaction(() => {
    for (const [k, v] of queue) {
      db.put(k, v);
    }
  });

  queue = [];
}
```

2. 基本パターン②：時間ベース batch（実務向け）

const INTERVAL_MS = 50;

setInterval(() => {
flush();
}, INTERVAL_MS);

3. パターン③：イベントキュー型（NATS / MQTT 連携）

NATS queue
↓
Node.js worker
↓
in-memory queue
↓
LMDB batch commit

nats.subscribe('iot.telemetry', (msg) => {
enqueue(msg.deviceId, msg.payload);
});

4. パターン④：Write-Behind Cache（Redis 置換）

read → LMDB（即）
write → memory → batch → LMDB

const cache = new Map();

function set(key, value) {
cache.set(key, value);
enqueue(key, value);
}

function get(key) {
return cache.get(key) ?? db.get(key);
}

- read latency = **RAM**
- write durability = **LMDB**
- Redis localhost 利用を完全に置換可能

5. パターン⑤：Atomic update（カウンタ・集計）

正しい batch 集計

const counters = new Map();

function incr(key) {
counters.set(key, (counters.get(key) ?? 0) + 1);
}

function flushCounters() {
db.transaction(() => {
for (const [k, delta] of counters) {
db.put(k, (db.get(k) ?? 0) + delta);
}
});
counters.clear();
}

① await db.put を多用しない

- 1 put = 1 fsync になりがち
- **transaction で囲む**

② batch を大きくしすぎない

③ process exit 時の flush

process.on('SIGTERM', () => flush());
process.on('SIGINT', () => flush());

---

## LMDB（Node.js）での cursor / range 操作によるスキャン方法

- Node.js では **`getRange()` が cursor の薄いラッパ**

1. 全件スキャン（基本）

import { open } from 'lmdb';

const db = open({ path: './db' });

for (const { key, value } of db.getRange()) {
console.log(key, value);
}

2. prefix scan（最頻出・実務）

キー設計（前提）

device:{deviceId}:state
device:{deviceId}:telemetry

prefix 指定

for (const { key, value } of db.getRange({ start: 'device:123:' })) {
if (!key.startsWith('device:123:')) break;
console.log(key, value);
}

- `start` で **B+Tree の該当位置へ一発ジャンプ**
- `break` で prefix 範囲を抜ける

3. 厳密な範囲指定（start / end）

for (const { key, value } of db.getRange({
start: 'device:1000:',
end: 'device:2000:'
})) {
console.log(key);
}

4. limit / offset（ページング）

for (const { key, value } of db.getRange({
start: 'event:',
limit: 100
})) {
console.log(key);
}

5. 逆順スキャン（latest N 件）

for (const { key, value } of db.getRange({
start: 'event:',
reverse: true,
limit: 10
})) {
console.log(key);
}

6. トランザクション付き scan（安全）

db.transaction(() => {
for (const { key, value } of db.getRange({ start: 'device:' })) {
// 一貫性のある snapshot
}
});

7. 高速にするキー設計

良い例（ゼロパディング）

event:00000001
event:00000002
event:00000010

8. binary key

const db = open({
path: './db',
encoding: 'ordered-binary'
});

9. IoT / NATS 文脈での実用例

device 単位の state 取得

for (const r of db.getRange({ start: `device:${id}:` })) {
if (!r.key.startsWith(`device:${id}:`)) break;
}

offline device 抽出

for (const { key, value } of db.getRange({ start: 'lastSeen:' })) {
if (Date.now() - value > 60_000) {
// offline
}
}

---

## LMDB の「読み出し/書き込み」python `liblmdb-dev` 利用

1. 書き込み（WRITE）

基本の流れ（必須）

mdb_txn_begin(env, NULL, 0, &txn);
mdb_dbi_open(txn, NULL, 0, &dbi);
mdb_put(txn, dbi, &key, &val, 0);
mdb_txn_commit(txn);

正しい書き込み単位

mdb_txn_begin(env, NULL, 0, &txn);

for (...) {
mdb_put(txn, dbi, &key, &val, 0);
}
mdb_txn_commit(txn);

上書き / 重複 key

mdb_put(txn, dbi, &key, &val, 0);
mdb_put(txn, dbi, &key, &val, MDB_NOOVERWRITE);

2. 読み出し（READ）

単一 key 取得

mdb_txn_begin(env, NULL, MDB_RDONLY, &txn);
mdb_get(txn, dbi, &key, &val);
mdb_txn_abort(txn);

range scan

MDB_cursor \*cursor;

mdb_txn_begin(env, NULL, MDB_RDONLY, &txn);
mdb_cursor_open(txn, dbi, &cursor);

while (mdb_cursor_get(cursor, &key, &val, MDB_NEXT) == 0) {
}

mdb_cursor_close(cursor);
mdb_txn_abort(txn);

start / end を使う

mdb_cursor_get(cursor, &key, &val, MDB_SET_RANGE);

3. purge（削除 = write）

削除も **write txn**

mdb_cursor_del(cursor, 0);

---

## Python での LMDB CRUD（Create / Read / Update / Delete）の最小かつ実務向けパターン

1. LMDB 環境の作成（DB open）

import lmdb

env = lmdb.open(
'data.lmdb',
map*size=1024 * 1024 \_ 1024, # 1GB
max_dbs=1,
subdir=True,
lock=True,
sync=True, # durability重視（Falseで高速）
)

- `map_size` は **後から拡張しにくい**ので大きめ推奨
- `sync=False` にすると batch は数十倍速くなる

2. CREATE / UPDATE（put）

key = b'user:001'
value = b'alice'

with env.begin(write=True) as txn:
txn.put(key, value)

- **LMDB では CREATE と UPDATE は同じ**
- 既存 key は自動的に上書き

上書き防止（insert only）

with env.begin(write=True) as txn:
ok = txn.put(key, value, overwrite=False)
if not ok:
print('key already exists')

3. READ（get）

with env.begin() as txn:
value = txn.get(b'user:001')

if value is not None:
print(value.decode())

4. DELETE（delete）

with env.begin(write=True) as txn:
txn.delete(b'user:001')

5. EXISTS チェック

with env.begin() as txn:
exists = txn.get(b'user:001') is not None

6. JSON を扱う場合

import json

key = b'user:002'
obj = {'name': 'bob', 'age': 30}

with env.begin(write=True) as txn:
txn.put(key, json.dumps(obj).encode())

with env.begin() as txn:
raw = txn.get(key)
if raw:
obj = json.loads(raw)

7. BATCH INSERT（高速・重要）

with env.begin(write=True) as txn:
for i in range(100_000):
k = f'user:{i:06d}'.encode()
v = str(i).encode()
txn.put(k, v)

8. SCAN（cursor）

with env.begin() as txn:
with txn.cursor() as cur:
for k, v in cur:
print(k, v)

prefix scan

prefix = b'user:'
with env.begin() as txn:
with txn.cursor() as cur:
if cur.set_range(prefix):
for k, v in cur:
if not k.startswith(prefix):
break
print(k, v)

9. RANGE SCAN（key order）

start = b'user:010000'
end = b'user:020000'

with env.begin() as txn:
with txn.cursor() as cur:
if cur.set_range(start):
for k, v in cur:
if k >= end:
break
print(k, v)

LMDB は **key の byte order がそのままソート順**

10. COUNT（件数）

with env.begin() as txn:
stat = txn.stat()
print(stat['entries'])

11. fsync / durability 設計の要点

| 用途              | 設定                          |
| ----------------- | ----------------------------- |
| 金融・重要データ  | `sync=True`                   |
| IoT / log / cache | `sync=False`                  |
| 高速 batch        | 大 transaction + `sync=False` |

---

## performance

### node.js

npm install lmdb

testlmdb.mjs

```
import { open } from 'lmdb';

const db = open({
  path: './lmdb-js',
  mapSize: 1024 * 1024 * 1024,
});

const N = 100_000;

console.time('write_batch');
await db.transaction(() => {
  for (let i = 0; i < N; i++) {
    db.put(`key${i}`, `value${i}`);
  }
});
console.timeEnd('write_batch');

console.time('read_random');
for (let i = 0; i < N; i++) {
  db.get(`key${i}`);
}
console.timeEnd('read_random');

console.time('read_scan');
for (const _ of db.getRange()) {
}
console.timeEnd('read_scan');

db.close();
```

### python

pip install lmdb

testlmdb.py

```
import lmdb
import time

env = lmdb.open(
    './lmdb-py',
    map_size=1024 * 1024 * 1024,
    ##sync=True,
    ##metasync=True
)

N = 100_000

# ---------- WRITE (batch) ----------
start = time.perf_counter()

with env.begin(write=True) as txn:
    for i in range(N):
        txn.put(f'key{i}'.encode(), f'value{i}'.encode())
env.sync()

print('write_batch:', time.perf_counter() - start)

# ---------- READ (random) ----------
start = time.perf_counter()

with env.begin() as txn:
    for i in range(N):
        txn.get(f'key{i}'.encode())

print('read_random:', time.perf_counter() - start)

# ---------- READ (scan) ----------
start = time.perf_counter()

with env.begin() as txn:
    with txn.cursor() as cur:
        for _ in cur:
            pass

print('read_scan:', time.perf_counter() - start)

env.close()
```

---

## ETL

- ETL は「速さ」より **再実行可能性**
- batch は **止まっても途中から再開できる**
- 失敗時に **壊れない / 二重書きしない**

1. Extract（取り込み）

### ファイル / STDIN / DB 共通ルール

- **ストリーム処理**
- 全件メモリに載せない

CSV → generator

import csv

def extract_csv(path):
with open(path, newline='') as f:
reader = csv.DictReader(f)
for row in reader:
yield row

2. Transform（変換）

def transform(row):
return {
'id': row['id'],
'value': int(row['value']),
'ts': row['timestamp'][:10]
}

3. Load（LMDB 書き込み）

import json
import lmdb

env = lmdb.open('etl.lmdb', map_size=10\*\*9, sync=False)

def load_batch(records):
with env.begin(write=True) as txn:
for r in records:
key = f"r:{r['id']}".encode()
val = json.dumps(r).encode()
txn.put(key, val)

4. Chunk / batch 設計（必須）

def chunked(iterable, size):
buf = []
for x in iterable:
buf.append(x)
if len(buf) == size:
yield buf
buf = []
if buf:
yield buf

ETL main loop

for chunk in chunked(extract_csv('data.csv'), 10_000):
records = []
for row in chunk:
records.append(transform(row))
load_batch(records)

5. 再実行可能設計

方法① watermark（最後の処理位置）

STATE_KEY = b'\_state:last_id'

def get_last_id(env):
with env.begin() as txn:
v = txn.get(STATE_KEY)
return int(v) if v else 0

def save_last_id(env, last_id):
with env.begin(write=True) as txn:
txn.put(STATE_KEY, str(last_id).encode())

方法② idempotent key

key = f"order:{order_id}".encode()
txn.put(key, val, overwrite=False)

6. エラー処理戦略

for chunk in chunks:
try:
process(chunk)
except Exception as e:
log_error(chunk, e)

7. 並列化の考え方（LMDB 前提）

Process A,B,C : extract + transform
↓ queue
Process W : LMDB write

8. fsync / durability 設計

| フェーズ      | 設定           |
| ------------- | -------------- |
| daily ETL     | sync=False     |
| final commit  | sync=True      |
| critical data | 常に sync=True |

---

## **LMDB → Parquet / DuckDB** を **ETL / batch 前提**で設計・実装

```
LMDB (source)
  └─ cursor scan
      └─ transform
          ├─ Parquet (archive / lake)
          └─ DuckDB (analytics / SQL)
```

1. LMDB → Parquet

pip install lmdb pyarrow duckdb

1.LMDB scan → dict generator

```
import lmdb, json

def scan_lmdb(path, prefix=b''):
    env = lmdb.open(path, readonly=True, lock=False)
    with env.begin() as txn:
        with txn.cursor() as cur:
            if prefix and not cur.set_range(prefix):
                return
            for k, v in cur:
                if prefix and not k.startswith(prefix):
                    break
                yield json.loads(v)
```

Parquet writer（chunk）

```
import pyarrow as pa
import pyarrow.parquet as pq

def lmdb_to_parquet(lmdb_path, parquet_path, chunk_size=50_000):
    writer = None
    buf = []

    for row in scan_lmdb(lmdb_path):
        buf.append(row)
        if len(buf) == chunk_size:
            table = pa.Table.from_pylist(buf)
            if writer is None:
                writer = pq.ParquetWriter(parquet_path, table.schema)
            writer.write_table(table)
            buf.clear()

    if buf:
        table = pa.Table.from_pylist(buf)
        if writer is None:
            writer = pq.ParquetWriter(parquet_path, table.schema)
        writer.write_table(table)

    if writer:
        writer.close()
```

2. LMDB → DuckDB（直接ロード）

方法① Parquet → DuckDB（推奨）

```
import duckdb

con = duckdb.connect('analytics.duckdb')
con.execute("""
CREATE TABLE events AS
SELECT * FROM read_parquet('data.parquet')
""")
```

方法② LMDB → DuckDB 直接 insert

```
import duckdb

con = duckdb.connect('analytics.duckdb')
con.execute("""
CREATE TABLE events (
  id VARCHAR,
  value INTEGER,
  ts DATE
)
""")

rows = []
for r in scan_lmdb('data.lmdb'):
    rows.append((r['id'], r['value'], r['ts']))
    if len(rows) == 10_000:
        con.executemany("INSERT INTO events VALUES (?, ?, ?)", rows)
        rows.clear()

if rows:
    con.executemany("INSERT INTO events VALUES (?, ?, ?)", rows)
```

3. 再実行可能設計

watermark（LMDB 側）

STATE_KEY = b'\_state:last_key'

def load_state(env):
with env.begin() as txn:
return txn.get(STATE_KEY)

def save_state(env, key):
with env.begin(write=True) as txn:
txn.put(STATE_KEY, key)

→ 中断しても **途中から再開**

## LMDB vs Redis 概念比較

① ローカル state / cache

**LMDB の方が速くて安全**

- context switch なし
- socket なし
- zero-copy read
- fsync 管理が自動

② IoT / Edge / Worker 内 cache

```
NATS queue
   ↓
worker
   ↓
LMDB
```

- device state
- last seen
- dedup
- aggregation buffer

Redis を置く意味がなくなる

③ Redis を「KVS」としか使っていない場合

使っている Redis 機能が

- GET / SET
- TTL なし
- 単純 key-value

**LMDB で完全代替可**

「代わりにならない」ケース

分散・共有 cache

```
app1 ─┐
app2 ─┼─ Redis
app3 ─┘
```

LMDB:

- ファイル
- 1 ホスト
- 排他 writer

TTL / eviction に依存している

Redis:

- TTL
- LRU / LFU
- eviction policy

LMDB

- ファイル置くだけ
- 壊れにくい
- backup が安全（`mdb_copy`）
- 運用コストほぼゼロ

Redis

- デーモン管理
- ポート管理
- メモリ制限
- 再起動設計

---

## **MQTT → NATS Core → Node.js → LMDB（batch write）最小・現実構成**

[ Sensor ]
↓ MQTT QoS0
Mosquitto
↓ (subscribe & forward)
Node.js Bridge
↓ NATS Core
Node.js Consumer
↓ (batch)
LMDB

```

| 層         | 役割           |
| --------- | ------------ |
| MQTT      | デバイス接続・不安定吸収 |
| NATS Core | 高速 fan-out   |
| LMDB      | 高速ローカル永続     |
| HA        | NATS 側で担保    |
| 欠損        | 許容（QoS0）     |



① MQTT → NATS ブリッジ（Node.js）

npm install mqtt nats


`mqtt_to_nats.js`
```

'use strict';

const mqtt = require('mqtt');
const { connect, StringCodec } = require('nats');

const MQTT_URL = 'mqtt://127.0.0.1:1883';
const MQTT_TOPIC = 'sensor/#';

const NATS_URL = 'nats://127.0.0.1:4222';
const NATS_SUBJECT_PREFIX = 'sensor.';

(async () => {
const nc = await connect({ servers: NATS_URL });
const sc = StringCodec();

const client = mqtt.connect(MQTT_URL, { clean: true });

client.on('connect', () => {
client.subscribe(MQTT_TOPIC, { qos: 0 });
});

client.on('message', (topic, payload) => {
// topic: sensor/temp/1 → sensor.temp.1
const subject = NATS_SUBJECT_PREFIX + topic.replace(/\//g, '.');
nc.publish(subject, payload);
});
})();

````

② NATS → LMDB（batch write）




---

「1秒 window 集約 → LMDB 保存」

```text
MQTT sensor
  ↓
Mosquitto
  ↓
NATS (buffer / fan-in)
  ↓
Node.js subscriber
  ↓
1秒ごとに batch
  ↓
LMDB write (single writer)
````

## LMDB → SQLite バッチ転送

```text
MQTT sensors
  ↓
Mosquitto
  ↓
NATS
  ↓
Node.js subscriber
  ↓
LMDB (fast append / window aggregate)
        ↓ (periodic read)
      SQLite (query / analytics)
```

- **LMDB = ingest buffer + short-term store**
- **SQLite = durable / queryable store**

LMDB → SQLite は安全に同時実行できる？

- LMDB reader はロックフリー
- Writer（集約書き込み）と Reader（SQLite 転送）は共存可能
- SQLite 側は「単一 writer」を守ればOK

```js
import { open } from 'lmdb';
import sqlite3 from 'better-sqlite3';

const lmdb = open({
  path: './lmdb',
  name: 'agg',
  readOnly: true,
});

const sqlite = sqlite3('data.db');

// last written ts
const lastTs = sqlite.prepare('SELECT value FROM meta WHERE key = ?').get('last_ts')?.value ?? 0;

const insert = sqlite.prepare(`
  INSERT INTO metrics(ts, avg, min, max)
  VALUES (?, ?, ?, ?)
`);

const updateMeta = sqlite.prepare(`
  INSERT OR REPLACE INTO meta(key, value)
  VALUES ('last_ts', ?)
`);

const tx = sqlite.transaction(() => {
  let maxTs = lastTs;

  for (const { key, value } of lmdb.getRange({
    start: String(lastTs + 1),
  })) {
    const ts = Number(key);
    insert.run(ts, value.avg, value.min, value.max);
    if (ts > maxTs) maxTs = ts;
  }

  updateMeta.run(maxTs);
});

tx();
```

---

**LMDB purge（古いデータ削除）**

**LMDB の purge は「range delete + 少数トランザクション」一択**

- 1 key ずつ delete ❌
- 全 scan ❌
- TTL フラグ ❌

---

1. LMDB purge の前提知識

LMDB の性質

- B+tree
- 単一 writer
- delete は **tree の再編成**を伴う
- 大量 delete = write lock を長時間保持

**短時間でまとめて消す**が正解

2. 推奨 key 設計

purge しやすい key

```text
<epoch_sec>
<epoch_sec>|device
<epoch_sec>|device|seq
```

- **time が prefix**
- 単調増加

3. 基本 purge：watermark 方式

- 「SQLite に転送済みの最大 ts」まで消す
- LMDB 側に状態を持たない

import { open } from 'lmdb'

const db = open({
path: './lmdb',
name: 'agg'
})

const PURGE_BEFORE_TS = 1700000000

const tx = db.transaction(() => {
for (const { key } of db.getRange({
end: PURGE_BEFORE_TS
})) {
db.remove(key)
}
})

tx()

4. 高速 purge（chunking）

大量データの場合、1 tx が長くなりすぎるのを防ぐ

```js
const CHUNK = 10_000;

while (true) {
  let count = 0;

  const tx = db.transaction(() => {
    for (const { key } of db.getRange({ end: cutoff })) {
      db.remove(key);
      if (++count >= CHUNK) break;
    }
  });

  tx();

  if (count === 0) break;
}
```

5. 最速 purge：DB ローテーション

- 古いデータは一切不要
- window 単位で分かれている

```text
lmdb/
  agg_20260217/
  agg_20260218/
```

```js
// 日付が変わったら
close old db
rm -rf agg_20260216
open new db
```

---

## **「MQTT → LMDB を直接つなぐ」**構成の **長所 / 短所 / 使える条件 / 使わない方がいい条件**

MQTT → LMDB を直接つなぐ構成

```text
Sensors
  ↓ MQTT
Subscriber (Node / C)
  ↓
LMDB
```

長所（メリット）

1. レイテンシ最小

- 中継なし
- コピー回数が少ない
- TCP → process → mmap

**μs〜ms オーダー**

2. 構成が最小

- Mosquitto + 1 process
- 外部 queue 不要
- デバッグしやすい

3. 小規模では十分速い

- 数千〜数万 msg/s
- 単一 writer 前提
- ローカルセンサー集約

短所（デメリット）

1. Backpressure が弱い

何が起きる？

- LMDB write txn が詰まる
- MQTT client の callback がブロック
- mosquitto 側でキューが溢れる

**落ちる時は一気**

2. 再送・再処理が弱い

- QoS0：欠損あり
- QoS1：dup 処理が必要
- QoS2：重い

LMDB は **queue ではない**

3. 単一 writer 制約が直撃

- MQTT message は burst する
- LMDB write txn は 1 つ
- ingest スレッドが詰まる

4. 責務が混ざる

```text
network IO + parse + aggregate + storage
```

- バグると全部止まる
- 再起動時の復旧が面倒

直結が「許される」条件

以下を **全部満たす**なら OK

- ingest < 数万 msg/s
- 欠損 OK
- 単一プロセス
- 再送不要
- データ寿命が短い
- 落ちても再起動でOK

**PoC / edge device 向き**

直結が「ダメ」な条件

1つでも当てはまるなら避ける

- ingest が burst する
- 複数 consumer が必要
- replay / rewind したい
- 後段処理が重い
- 書き込み停止が許されない

MQTT → NATS → LMDB が強い理由

```text
MQTT
 ↓
NATS (buffer / fan-out)
 ↓
LMDB
```

NATS が吸収するもの

- burst
- backpressure
- consumer 遅延
- reconnect

LMDB は **storage 専念**

比較まとめ

| 項目       | MQTT→LMDB | MQTT→NATS→LMDB |
| ---------- | --------- | -------------- |
| 構成       | ◎         | △              |
| レイテンシ | ◎         | ○              |
| 安定性     | △         | ◎              |
| スケール   | ❌        | ◎              |
| 再送       | △         | ◎              |
| 運用       | △         | ◎              |

---

## SQLite vs LMDB

testsqlite.py

```
import sqlite3
import time
import os
import random
import string

DB = 'test.sqlite'
N = 100_000

if os.path.exists(DB):
    os.remove(DB)

conn = sqlite3.connect(DB)
cur = conn.cursor()

cur.execute('PRAGMA journal_mode=WAL')
cur.execute('PRAGMA synchronous=NORMAL')

cur.execute('CREATE TABLE kv (k TEXT PRIMARY KEY, v TEXT)')
conn.commit()

def rand():
    return ''.join(random.choices(string.ascii_letters, k=32))

# write batch
t0 = time.time()
cur.execute('BEGIN')
for i in range(N):
    cur.execute('INSERT INTO kv VALUES (?,?)', (f'k{i}', rand()))
conn.commit()
print('sqlite write_batch:', time.time() - t0)

# random read
t0 = time.time()
for i in range(N):
    k = f'k{random.randint(0, N-1)}'
    cur.execute('SELECT v FROM kv WHERE k=?', (k,))
    cur.fetchone()
print('sqlite read_random:', time.time() - t0)

conn.close()
```

testlmdb2.py

```
import lmdb
import time
import os
import random
import string
import shutil

PATH = './lmdbdata'
N = 100_000

if os.path.exists(PATH):
    shutil.rmtree(PATH)

env = lmdb.open(
    PATH,
    map_size=1024 * 1024 * 1024,  # 1GB
    max_dbs=1,
    # sync=False,
    # writemap=True,
    # metasync=False
)

def rand():
    return ''.join(random.choices(string.ascii_letters, k=32)).encode()

# write batch
t0 = time.time()
with env.begin(write=True) as txn:
    for i in range(N):
        txn.put(f'k{i}'.encode(), rand())
print('lmdb write_batch:', time.time() - t0)

# random read
t0 = time.time()
with env.begin() as txn:
    for i in range(N):
        k = f'k{random.randint(0, N-1)}'.encode()
        txn.get(k)
print('lmdb read_random:', time.time() - t0)

env.close()
```

---

## LMDB キャッシュの位置づけ

```
Memory cache (dict / LRU)
        ↓ miss
LMDB (local persistent cache)
        ↓ miss
Remote (API / DB / S3)
```

- mmap ベース → **読み取りが非常に速い**
- 永続化 → **再起動してもキャッシュが残る**
- single-writer → **更新は集約が必要**

---

### LMDB がキャッシュに向いている理由

強み

- Redis 不要（依存削減）
- fsync を緩めれば **ほぼメモリ速度**
- 数百万〜数千万 key でも安定
- プロセス間共有が容易

弱み（理解必須）

- TTL がない（自前実装）
- 分散キャッシュではない
- write は 1 プロセスのみ

---

### 基本設計パターン

key 設計

cache:{namespace}:{id}

value 構造（TTL 対応）

{
"value": "...",
"expire_at": 1735689600
}

---

### 基本 CRUD（キャッシュ用）

import lmdb, json, time

env = lmdb.open(
'cache.lmdb',
map_size=2 \* 1024\*\*3,
sync=False,
lock=True
)

SET

def cache_set(key, value, ttl_sec):
expire_at = int(time.time()) + ttl_sec
data = {
'value': value,
'expire_at': expire_at
}
with env.begin(write=True) as txn:
txn.put(key.encode(), json.dumps(data).encode())

GET（TTL チェック）

def cache_get(key):
now = int(time.time())
with env.begin() as txn:
raw = txn.get(key.encode())
if not raw:
return None

    obj = json.loads(raw)
    if obj['expire_at'] < now:
        cache_delete(key)
        return None

    return obj['value']

DELETE

def cache_delete(key):
with env.begin(write=True) as txn:
txn.delete(key.encode())
``

---

### TTL クリーンアップ

LMDB は自動削除しない → **掃除が必須**

方法① read 時に削除（lazy）

- 上の `cache_get()` がそれ
- 実装が簡単
- ゴミは残りやすい

方法② 定期 sweep（推奨）

def sweep_expired():
now = int(time.time())
with env.begin(write=True) as txn:
cur = txn.cursor()
for k, v in cur:
obj = json.loads(v)
if obj['expire_at'] < now:
cur.delete()

cron
_/10 _ \* \* \* python sweep.py

---

## LRU / サイズ制限（Redis 的機能）

- LMDB 単体では困難
- **上位にメモリ LRU を置く**

```
LRU dict (1万件)
   ↓ miss
LMDB
```

---

### 高速化の鉄則（キャッシュ用途）

1. sync=False

lmdb.open(..., sync=False)

2. write を集約する

with env.begin(write=True) as txn:
for k, v in batch:
txn.put(k, v)

3. write 専用プロセス

```
worker N (read)
   ↓ queue
writer 1 (lmdb)
```

---

### 使うべき / 使うべきでないケース

向いている

- ローカル API キャッシュ
- IoT edge node
- CLI / batch の中間結果
- 再計算が高コストなデータ

向いていない

- 分散キャッシュ
- 強い TTL / eviction 要件
- 高頻度 write（数万/s を複数プロセス）

---

### A.MQTT 側で subscriber を分ける方式

```
MQTT broker
 ├─ sub sensors/fast/#  → NATS → LMDB
 ├─ sub sensors/slow/#  → NATS → SQLite
 ├─ sub sensors/log/#   → NATS → …
```

### B.MQTT は1 subscriber、NATS で分ける方式

```
MQTT broker
 └─ sub sensors/#
       ↓
     NATS (topic→subject)
       ├─ sub mqtt.sensors.fast.> → LMDB
       ├─ sub mqtt.sensors.slow.> → SQLite
       └─ sub mqtt.sensors.log.>  → …
```

| 観点            | A: MQTT分岐 | B: NATS分岐     |
| --------------- | ----------- | --------------- |
| 構造の美しさ    | △           | **◎**           |
| 拡張性          | △           | **◎**           |
| 再配線コスト    | 高          | **低**          |
| Fan-out         | MQTT依存    | **NATS得意**    |
| 再処理 / replay | ほぼ不可    | **JetStream可** |
| 運用            | 複雑        | **単純**        |
| 将来変更        | 壊れやすい  | **強い**        |

MQTT は「末端プロトコル」

- IoT / edge 向け
- Topic はあるが **fan-out・再配線が弱い**
- subscriber 増えるほど broker 負荷増

NATS は「分配・配線のためのミドル層」

- subject wildcard
- fan-out が O(1) 感覚
- subscriber 増やしても publisher 側変更ゼロ

```text
mqtt.sensors.fast.>   → LMDB
mqtt.sensors.slow.>   → SQLite
mqtt.sensors.>        → monitor
```

LMDB / SQLite は「処理特性が真逆」

| DB     | 向き                  |
| ------ | --------------------- |
| LMDB   | burst / cache / queue |
| SQLite | durable / SQL / join  |

→ **処理要件で subscriber を分けたい**
→ MQTT 側で分けると設計が歪む

再処理・実験ができる

B の場合

- 新しい subscriber を **追加するだけ**
- 過去データも JetStream で replay 可能

A の場合

- MQTT subscriber を追加
- broker 設定変更
- 再送不可

MQTT subscriber を増やすと

- broker が全 subscriber に copy
- QoS 管理が増える
- retain 処理が重くなる

NATS subscriber を増やすと

- fan-out が軽い
- QoS 概念なし（速い）
- subject match が超軽量

```text
MQTT
  └─ single subscriber
       ↓
   NATS (topic → subject)
       ├─ LMDB writer (fast path)
       ├─ SQLite writer (slow path)
       ├─ Monitor / metrics
       └─ Debug / replay
```

---

なぜ MQTT はエッジ止まりがよいか

MQTT は「軽さ特化」

- 小さなメモリ
- 低帯域
- 不安定ネットワーク

MQTT を中枢にすると苦しくなる

| 問題     | 実際に起きること                  |
| -------- | --------------------------------- |
| Fan-out  | subscriber 増えると broker が重い |
| 再処理   | replay ができない                 |
| 配線変更 | broker 設定が必要                 |
| 分岐     | topic 設計が複雑化                |
| 観測性   | メトリクス弱い                    |

NATS は配線のためのミドル層

- fan-out が本業
- subject wildcard が強力
- subscriber 追加が無コスト
- 後段を自由に組み替え可能

再処理・耐久性を後付けできる

- JetStream を足すだけ
- replay / backfill / audit が可能

MQTT 単体ではほぼ不可能。

例外（MQTT を残すべきケース）

| ケース          | 判断     |
| --------------- | -------- |
| device ↔ device | MQTT     |
| retain が本質   | MQTT     |
| 超低遅延 QoS    | MQTT     |
| 超小規模        | MQTT単体 |

mqtt_nats_bridge.py

```
import asyncio
import signal
from nats.aio.client import Client as NATS
import paho.mqtt.client as mqtt

MQTT_BROKER = 'localhost'
MQTT_TOPIC  = 'sensors/#'
NATS_URL    = 'nats://localhost:4222'

loop = asyncio.get_event_loop()
nc = NATS()

def on_message(client, userdata, msg):
    subj = 'mqtt.' + msg.topic.replace('/', '.')
    loop.create_task(nc.publish(subj, msg.payload))

async def main():
    await nc.connect(servers=[NATS_URL])

    m = mqtt.Client(client_id='mqtt-nats-bridge')
    m.on_message = on_message
    m.connect(MQTT_BROKER, 1883)
    m.subscribe(MQTT_TOPIC, qos=0)
    m.loop_start()

    stop = asyncio.Future()
    for s in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(s, stop.set_result, None)
    await stop

    m.loop_stop()
    await nc.close()

loop.run_until_complete(main())
```

# MQTT and lua

## Lua と MQTT の関係

- Lua は **軽量・組み込み向け**
- MQTT は **低リソース端末向け**
- **相性は非常に良い**（ゲートウェイ / edge で定番）

Lua で MQTT subscribe（最小）

sudo apt install lua5.1 luarocks
luarocks install lua-mqtt

最小 subscriber

sub.lua

```lua
local mqtt = require('mqtt')

local client = mqtt.client{
  uri = 'mqtt://localhost',
  id  = 'lua-subscriber'
}

client:on{
  connect = function()
    print('connected')
    client:subscribe{ topic = 'sensors/#' }
  end,

  message = function(pkt)
    print(pkt.topic, pkt.payload)
  end
}

client:connect()
client:loop_forever()
```

lua sub.lua

mosquitto_pub -t test/topic0 -m msg0

Lua で MQTT publish

pub.lua

```lua
local mqtt = require('mqtt')

local client = mqtt.client{
  uri = 'mqtt://localhost',
  id  = 'lua-publisher'
}

client:connect()
client:publish{
  topic   = 'test/topic0',
  payload = 'msg0'
}
client:disconnect()
```

lua pub.lua

Lua × MQTT が向いている理由

| 項目     | 評価      |
| -------- | --------- |
| メモリ   | ◎（数MB） |
| CPU      | ◎         |
| 起動速度 | ◎         |
| 安定性   | ○         |
| 実装量   | 少ない    |

---

### lua-mqtt（純 Lua / libuv ベース）

- 非同期
- reconnect 対応
- 長時間常駐向き
- API が素直

luarocks install mqtt

クライアント生成

```lua
local mqtt = require('mqtt')

local client = mqtt.client{
  uri      = 'mqtt://localhost',
  id       = 'bridge-1',
  clean    = true,
  keepalive = 60
}
```

イベント API

lua-mqtt は **イベント駆動**

```lua
client:on{
  connect = function()
    print('connected')
  end,

  message = function(pkt)
    print(pkt.topic, pkt.payload)
  end,

  error = function(err)
    print('error', err)
  end,

  close = function()
    print('connection closed')
  end
}
```

pkt.topic -- string
pkt.payload -- string
pkt.qos -- 0/1/2
pkt.retain -- boolean

subscribe / publish

```lua
client:subscribe{
  topic = 'test',
  qos   = 0
}

client:publish{
  topic   = 'test',
  payload = 'msg0',
  qos     = 0,
  retain  = false
}
```

実行ループ（必須）

```lua
client:connect()
mqtt.run()
```

### MQTT → topic 変換 → 処理

```lua
local mqtt = require('mqtt')

local c = mqtt.client{ uri = 'mqtt://localhost' }

c:on{
  connect = function()
    c:subscribe{ topic = 'test' }
  end,

  message = function(pkt)
    local subject = 'mqtt.' .. pkt.topic:gsub('/', '.')
    local msg = pkt.payload
    print(subject, msg)
  end
}

c:connect()
mqtt.run()
```
