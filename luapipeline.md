Lua で **MQTT** を使う代表的な方法は **LuaSocket + MQTT クライアントライブラリ** を使う構成です。
軽量で組み込み・IoT・ブローカー検証用途に向いています。

---

## 全体像

```
Lua script
  └─ MQTT client library
       └─ TCP/TLS
            └─ MQTT Broker (e.g. Mosquitto)
```

---

### **lua-mqtt（純Lua）**

- LuaSocket 依存
- QoS 0/1/2 対応
- シンプル・可読性が高い

👉 [https://github.com/xHasKx/luamqtt](https://github.com/xHasKx/luamqtt)

## 最小構成（lua-mqtt）

### 依存関係

```bash
sudo apt install lua5.4 luarocks
luarocks install luasocket
luarocks install luamqtt
```

---

## Publish の例

```lua
local mqtt = require('mqtt')

local client = mqtt.client {
  uri = 'mqtt://localhost:1883',
  client_id = 'lua-pub-1',
}

assert(client:connect())

client:publish {
  topic = 'test/topic',
  payload = 'hello from lua',
  qos = 0,
  retain = false,
}

client:disconnect()
```

---

## Subscribe の例

```lua
local mqtt = require('mqtt')

local client = mqtt.client {
  uri = 'mqtt://localhost:1883',
  client_id = 'lua-sub-1',
}

client:on {
  connect = function()
    client:subscribe { topic = 'test/topic', qos = 0 }
  end,

  message = function(pkt)
    print('topic:', pkt.topic)
    print('payload:', pkt.payload)
  end,
}

assert(client:connect())

-- event loop
while true do
  client:iteration()
end
```

---

## TLS（SSL）接続例

```lua
local client = mqtt.client {
  uri = 'mqtts://broker.example.com:8883',
  client_id = 'lua-tls-1',
  cafile = '/etc/ssl/certs/ca-certificates.crt',
}
```

---

## Broker（検証用）

ローカル検証には **Eclipse Mosquitto** が最適です。

```bash
sudo apt install mosquitto mosquitto-clients
mosquitto -v
```

---

## Lua + MQTT が向いている用途

- 軽量 ETL / スクリプト
- IoT ゲートウェイ
- MQTT → LMDB / SQLite ブリッジ
- NATS / MQTT 比較検証

---

## NATS や LMDB と組み合わせるなら

あなたのこれまでの関心（MQTT / NATS / LMDB）的には：

```
MQTT → Lua (subscribe)
     → LMDB (高速ローカル書き込み)
     → バッチ or NATS pub
```

という構成がかなり相性が良いです。

---

必要なら次に：

- QoS 1/2 の挙動
- reconnect / keepalive 実装
- MQTT → LMDB 最小コード
- Lua での高スループット設計

のどれかを具体コード付きで説明できます。
