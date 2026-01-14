一般的な用途での Bash と Lua の使い分け

---

## 1. Bash が向いているケース

**基本思想**

- OS に近い操作やコマンド操作を中心にする場合に最適
- 「既存のコマンドやツールをつなぐ」役割

**具体例**

1. **システム管理・運用**

   - ユーザ管理、ディレクトリ構造の管理、パーミッション変更
   - ログローテーションやバックアップ

2. **ファイル操作・テキスト処理**

   - ファイルコピー・移動・削除
   - `grep`、`sed`、`awk` を使った簡易フィルタリング

3. **自動化スクリプト**

   - cron ジョブで定期的に実行
   - コマンドラインツールのラッパー

4. **パイプライン処理**

   - コマンド同士をパイプでつないで処理

**メリット**

- OS コマンドとの親和性が高い
- スクリプトが短く書ける
- 標準入出力の操作が簡単

**デメリット**

- 複雑なロジックやデータ構造の管理には不向き
- 数値計算や高度な文字列操作は苦手

---

## 2. Lua が向いているケース

**基本思想**

- 軽量スクリプト言語で、**ロジック・データ管理・計算・拡張**を担当する場合に最適
- アプリ内組み込みやゲーム、C との連携に向く

**具体例**

1. **組み込みスクリプト**

   - ゲームやアプリの設定スクリプト
   - Wireshark や Nginx などで Lua 経由で機能拡張

2. **ロジック処理・制御フロー**

   - 複雑な条件分岐、ループ、テーブル操作
   - 高速計算や配列操作（LuaJIT でさらに高速）

3. **軽量サーバサイド処理**

   - Nginx + Lua (OpenResty) での高速リクエスト処理

4. **カスタム拡張・プラグイン**

   - C/C++アプリへの埋め込みや API 拡張

5. **データ加工・変換**

   - CSV/JSON/XML のパース・生成
   - 条件付きで大量データを高速処理

**メリット**

- 小規模でも大規模でも柔軟に使える
- 高速で軽量
- データ構造（テーブル）や文字列操作が得意

**デメリット**

- OS 操作やシェルコマンド呼び出しは限定的
- Bash のように「パイプラインでコマンドを繋ぐ」用途には不向き

---

## 3. 総合的な使い分けの考え方

| 用途 / 特徴                  | Bash | Lua                       |
| ---------------------------- | ---- | ------------------------- |
| OS 操作 / ファイル管理       | ◎    | △（限定的）               |
| コマンド連携 / パイプ        | ◎    | △                         |
| データ構造 / 配列 / テーブル | △    | ◎                         |
| 数値計算 / 文字列処理        | △    | ◎                         |
| 組み込み / プラグイン        | ×    | ◎                         |
| 高速処理 / 大量データ        | △    | ◎（JIT ならさらに高速）   |
| スクリプト短時間で書く       | ◎    | △（ロジック複雑だと有利） |

---

---

sudo apt install lua5.4
lua -v

sudo apt install luajit
luajit -v

performance

```
time { s=0; for ((i=0;i<1000000;i++)); do (($RANDOM%2==0)) && ((s+=$RANDOM%100)); done; echo -e "\n bash $s"; }

time { s=0; for i in {1..1000000}; do (($RANDOM%2==0)) && ((s+=$RANDOM%100)); done; echo -e "\n bash with seq $s"; }

time awk 'BEGIN{s=0; for(i=0;i<1e6;i++) if(int(rand()*2)==0) s+=int(rand()*100); print ("\n awk",s)}'

time perl -e 'my $s=0; for (1..1000000) { $s+=int(rand(100)) if int(rand(2))==0 } print "\n perl $s";'

time python3 -c 'import random; s=0;
for _ in range(1000000):
    if random.randint(0,1)==0:
        s+=random.randint(0,99)
print("\n python", s)'

time python3 -c 'import random; s=0; [s:=s+random.randint(0,99) for _ in range(1000000) if random.randint(0,1)==0]; print("\n python with comprehensions",s)'

time python3 -c 'import random; s=sum(random.randint(0,99) for _ in range(1000000) if random.randint(0,1)==0); print("\n python with sum function", s)'

time node -e 'let s=0; for(let i=0;i<1e6;i++){ if((Math.random()*2|0)==0) s+=Math.random()*100|0; } console.log("\n node ",s);'

time bun -e 'let s=0; for(let i=0;i<1e6;i++){ if((Math.random()*2|0)==0) s+=Math.random()*100|0; } console.log("\n bun ",s);'

time lua -e 'local s=0; for i=1,1e6 do if math.random(0,1)==0 then s=s+math.random(0,99) end end; print("\n lua ",s)'

time luajit -e 'local s=0; for i=1,1e6 do if math.random(0,1)==0 then s=s+math.random(0,99) end end; print("\n luajit ",s)'


test.c
 
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
 
int main(){
    long long s=0;
    for(int i=0;i<100000000;i++)
        if(rand()%2==0) s+=rand()%100;
        printf("%lld\n", s);
}
 
gcc -O2 -march=native test.c -o testc
time ./testc
 
 
 
test.cpp
 
#include <iostream>
#include <cstdlib>
#include <ctime>
 
int main(){
    long long s = 0;
    for(int i = 0; i < 100000000; i++)
        if(std::rand()%2==0) s+=std::rand()%100;
    std::cout << s << '\n';
}
 
 
g++ -O2 -march=native test.cpp -o testcpp
time ./testcpp
```

start dialog mode
lua/luajit
os.exit() or ctrl+D

one liner

lua -e '--script--'
luagit -e '--script--'

echo '1 2 3' | lua -e 'local s=0; for n in io.read("\*a"):gmatch("%d+") do s=s+tonumber(n) end; print(s)'

script.lua

#!/usr/bin/env lua
or
#!/usr/bin/env luajit
--- script ---

lua script.lua
or
luajit script.lua

chmod +x script.lua
./script.lua

| 項目                 | Lua（標準）                     | LuaJIT                                               |
| -------------------- | ------------------------------- | ---------------------------------------------------- |
| 実装                 | インタプリタ（C で書かれた VM） | JIT コンパイル付き Lua 5.1 互換 VM                   |
| 実行速度             | 高速（C 速度に近い）            | 超高速（ネイティブコード生成）                       |
| Lua バージョン互換性 | Lua 5.1〜5.4                    | Lua 5.1 互換（一部 5.2+機能非対応）                  |
| メモリ使用           | 小                              | 小〜やや大きい（JIT コード生成分）                   |
| 拡張性               | 標準ライブラリ＋外部モジュール  | 標準＋ FFI で C ライブラリ直接呼び出し可能           |
| 起動時間             | 数 ms                           | 数 ms（Lua よりやや長め、ほぼ無視できる）            |
| デバッグ             | 標準 Lua のツールが使える       | JIT 最適化でスタックトレースがやや読みづらい場合あり |

---

## 【Lua 標準ライブラリ チートシート】

### 1. 基本関数（`_G`）

| 関数                                      | 説明                           |
| ----------------------------------------- | ------------------------------ |
| `print(...)`                              | 標準出力に出力                 |
| `type(v)`                                 | 値の型を返す                   |
| `tostring(v)`                             | 値を文字列に変換               |
| `tonumber(s, base)`                       | 文字列を数値に変換             |
| `error(msg, level)`                       | エラーを発生                   |
| `assert(v, msg)`                          | v が false/nil ならエラー      |
| `pcall(f, ...)`                           | 関数を保護モードで呼び出す     |
| `xpcall(f, err)`                          | エラー時にハンドラを呼ぶ       |
| `select(i, ...)`                          | 可変引数から部分を取得         |
| `next(t, k)`                              | テーブルの次のキーを取得       |
| `pairs(t)`                                | 汎用テーブルイテレータ         |
| `ipairs(t)`                               | 配列部分のイテレータ           |
| `rawget(t, k)` / `rawset(t, k, v)`        | メタテーブルを無視してアクセス |
| `rawequal(a, b)`                          | メタメソッドを無視して比較     |
| `rawlen(t)`                               | テーブル長を返す               |
| `getmetatable(t)` / `setmetatable(t, mt)` | メタテーブル取得・設定         |
| `load(chunk [, chunkname])`               | Lua コード文字列を関数化       |
| `dofile(filename)`                        | ファイルを実行                 |
| `require(modname)`                        | モジュールをロード             |

---

### 2. 文字列ライブラリ（`string`）

| 関数                                  | 説明                |
| ------------------------------------- | ------------------- |
| `string.len(s)`                       | 長さを返す          |
| `string.lower(s)` / `string.upper(s)` | 小文字/大文字変換   |
| `string.sub(s, i, j)`                 | 部分文字列を取得    |
| `string.find(s, pattern)`             | パターン検索        |
| `string.match(s, pattern)`            | 最初のマッチを返す  |
| `string.gmatch(s, pattern)`           | イテレータを返す    |
| `string.gsub(s, pat, repl)`           | 置換                |
| `string.byte(s, i, j)`                | 文字コード取得      |
| `string.char(...)`                    | 文字コード → 文字列 |
| `string.format(fmt, ...)`             | 書式整形            |
| `string.rep(s, n)`                    | 繰り返し            |
| `string.reverse(s)`                   | 反転                |

---

### 3. 数値ライブラリ（`math`）

| 関数                                             | 説明                |
| ------------------------------------------------ | ------------------- |
| `math.abs(x)`                                    | 絶対値              |
| `math.sqrt(x)`                                   | 平方根              |
| `math.floor(x)` / `math.ceil(x)`                 | 切り捨て / 切り上げ |
| `math.max(...)` / `math.min(...)`                | 最大 / 最小         |
| `math.random([m, n])`                            | 乱数                |
| `math.randomseed(x)`                             | 乱数シード設定      |
| `math.sin(x)` / `math.cos(x)` / `math.tan(x)`    | 三角関数            |
| `math.asin(x)` / `math.acos(x)` / `math.atan(x)` | 逆三角関数          |
| `math.log(x [, base])`                           | 対数                |
| `math.exp(x)`                                    | e^x                 |
| `math.deg(x)` / `math.rad(x)`                    | 度 ⇔ ラジアン変換   |
| `math.pi`                                        | π 定数              |
| `math.huge`                                      | 無限大定数          |

---

### 4. テーブルライブラリ（`table`）

| 関数                          | 説明       |
| ----------------------------- | ---------- |
| `table.insert(t, [pos], v)`   | 要素挿入   |
| `table.remove(t, [pos])`      | 要素削除   |
| `table.move(a1, f, e, t, a2)` | 範囲コピー |
| `table.concat(t, sep, i, j)`  | 結合       |
| `table.sort(t [, comp])`      | ソート     |
| `table.unpack(t [, i, j])`    | 展開       |

---

### 5. 入出力ライブラリ（`io`）

| 関数                         | 説明                     |
| ---------------------------- | ------------------------ |
| `io.open(filename [, mode])` | ファイルを開く           |
| `io.close(file)`             | ファイルを閉じる         |
| `io.read(...)`               | 標準入力を読む           |
| `io.write(...)`              | 標準出力に書く           |
| `io.lines(filename)`         | 行イテレータ             |
| `io.flush()`                 | 出力バッファをフラッシュ |

モード例: `"r"` 読み取り, `"w"` 書き込み, `"a"` 追記, `"rb"` バイナリ

---

### 6. OS ライブラリ（`os`）

| 関数                   | 説明                 |
| ---------------------- | -------------------- |
| `os.execute(cmd)`      | シェルコマンド実行   |
| `os.remove(filename)`  | ファイル削除         |
| `os.rename(old, new)`  | ファイル名変更       |
| `os.exit([code])`      | 終了                 |
| `os.getenv(var)`       | 環境変数取得         |
| `os.time([table])`     | 現在時刻 (UNIX time) |
| `os.date([fmt, time])` | 日付文字列整形       |
| `os.difftime(t2, t1)`  | 時間差計算           |
| `os.clock()`           | CPU 使用時間         |

---

### 7. デバッグライブラリ（`debug`）

| 関数                            | 説明             |
| ------------------------------- | ---------------- |
| `debug.getinfo(f [, what])`     | 関数情報取得     |
| `debug.getlocal(f, n)`          | ローカル変数取得 |
| `debug.sethook(f, mask, count)` | フック設定       |
| `debug.traceback([msg])`        | スタックトレース |

---

### 8. コルーチン（`coroutine`）

| 関数                        | 説明                   |
| --------------------------- | ---------------------- |
| `coroutine.create(f)`       | 新しいコルーチン作成   |
| `coroutine.resume(co, ...)` | コルーチン実行再開     |
| `coroutine.yield(...)`      | 一時停止               |
| `coroutine.status(co)`      | 状態確認               |
| `coroutine.wrap(f)`         | 簡易呼び出し用ラッパー |

---

### 9. その他

| 定数・関数 | 説明                   |
| ---------- | ---------------------- |
| `_VERSION` | Lua のバージョン文字列 |
| `_G`       | グローバル環境テーブル |

---

### ファイル入出力（I/O）

ファイルの読み書き・行ごと処理が可能。
Lua の`io`ライブラリは C 言語標準 I/O に直接対応しており高速。

```lua
-- ファイル読み込み
for line in io.lines('input.txt') do
  print(line)
end

-- 書き込み
local f = io.open('out.txt', 'w')
f:write('Hello Lua\n')
f:close()
```

### 標準ライブラリ

#### - 文字列操作 (`string`)

```lua
local s = 'abc123'
print(s:match('%d+'))   -- "123"
print(s:gsub('%a', 'X')) -- "XXX123"
```

#### - 数学 (`math`)

```lua
print(math.sin(math.pi/2))  -- 1
print(math.random(1,100))   -- 1〜100の乱数
```

#### - 時間 (`os`)

```lua
print(os.date('%Y-%m-%d %H:%M:%S'))
print(os.time())  -- UNIX timestamp
```

#### - テーブル操作 (`table`)

```lua
local t = {1,2,3}
table.insert(t,4)
print(table.concat(t, ','))
```

### 再帰・高階関数・クロージャ

Lua は関数を値として扱える。関数式や無名関数、クロージャを自然に扱える。

```lua
-- 再帰関数
function fact(n)
  if n == 0 then return 1 end
  return n * fact(n-1)
end

print(fact(5))

-- クロージャ
function counter()
  local n = 0
  return function() n = n + 1; return n end
end

local c = counter()
print(c(), c(), c())  -- 1 2 3
```

### モジュール構成とスクリプト実行

`require` を使ってファイルをモジュール化できる。
（`require`はカレントディレクトリや標準パスを探索）

```lua
-- mathutil.lua
local M = {}
function M.double(x) return x * 2 end
return M

-- main.lua
local m = require('mathutil')
print(m.double(5))
```

### CLI スクリプトとして

```bash
lua script.lua arg1 arg2
```

Lua 側で引数を受け取る：

```lua
for i,a in ipairs(arg) do
  print(i, a)
end
```

---


基本方針は「**制御は bash、重い処理は Lua**」です。

---

## 基本構成パターン

### 1. bash → lua（stdin / argv）

```bash
#!/bin/bash

cat big.txt | lua process.lua arg1 arg2
```

```lua
-- process.lua
local arg1, arg2 = ...
for line in io.lines() do
    -- heavy logic
    print(line)
end
```

**用途**

* 大量テキスト処理
* awk/sed が読みにくくなった時
* ループ・条件分岐が多い処理

---

### 2. bash → lua（ファイル処理）

```bash
lua process.lua input.csv output.csv
```

```lua
-- process.lua
local in_f, out_f = ...
local fi = io.open(in_f)
local fo = io.open(out_f, 'w')

for line in fi:lines() do
    fo:write(line, '\n')
end

fi:close()
fo:close()
```

**用途**

* CSV / TSV / ログ処理
* bash では辛い状態管理

---

### 3. bash 関数の代わりに lua

```bash
parse() {
    lua - "$@" <<'LUA'
local a,b = ...
print(a + b)
LUA
}

parse 10 20
```

**用途**

* 数値計算
* 正規表現
* 状態を持つ処理

---

## 実践例（bashが遅い典型）

### ❌ bash / awk が辛いケース

* ネストしたループ
* map / set が欲しい
* 複雑な条件分岐
* JSON / 構造化データ

---

### 例1: bash で遅い集計 → lua

```bash
cat data.txt | lua count.lua
```

```lua
-- count.lua
local cnt = {}
for line in io.lines() do
    cnt[line] = (cnt[line] or 0) + 1
end

for k,v in pairs(cnt) do
    print(k, v)
end
```

👉 awk より **可読性・保守性が段違い**

---

### 例2: 正規表現 + 状態遷移

```lua
local state = 'INIT'

for line in io.lines() do
    if state == 'INIT' and line:match('^BEGIN') then
        state = 'BODY'
    elseif state == 'BODY' then
        print(line)
    end
end
```

bash/awk だと **地獄**、Luaだと **普通**

---

## 高速化のコツ（重要）

### 1. lua は **1回起動**

❌ 行ごとに lua 呼び出し
⭕ `cat | lua script.lua`

---

### 2. io.lines() を使う

```lua
for line in io.lines() do
```

* LuaJIT でなくても速い
* メモリ効率が良い

---

### 3. print より write

```lua
io.stdout:write(line, '\n')
```

大量出力では差が出ます。

---

## bash + lua + 他ツールの役割分担

| 役割     | ツール                  |
| ------ | -------------------- |
| ファイル探索 | bash / find          |
| 並列     | xargs / GNU parallel |
| 軽い整形   | sed / cut            |
| 重い処理   | **Lua**              |
| JSON   | jq or Lua            |

---

## lua を「bash の拡張言語」にする設計

```bash
#!/bin/bash
set -e

find . -name '*.log' |
while read f; do
    lua analyze.lua "$f"
done
```
---

## いつ awk より lua を使うべき？

✅ Luaを使うべき

* ロジックが20行を超えた
* 配列 / set / map が欲しい
* 後で仕様変更がありそう

❌ awk のままでいい

* 1〜3行
* 単純な列操作

---


# ① bash ループ → lua に移す（典型）

## 元の bash（遅くなりがち）

```bash
#!/bin/bash

total=0
while read n; do
    if [ "$n" -gt 10 ]; then
        total=$((total + n))
    fi
done < numbers.txt

echo "$total"
```

### 問題点

* 行ごとに bash の数値評価
* 条件が増えると地獄
* 浮動小数点が扱えない

---

## Lua に移行（stdin 処理）

```bash
cat numbers.txt | lua sum.lua
```

```lua
-- sum.lua
local total = 0

for line in io.lines() do
    local n = tonumber(line)
    if n and n > 10 then
        total = total + n
    end
end

print(total)
```

✔ 可読性
✔ 拡張性
✔ 浮動小数点OK

---

# ② awk 集計 → lua（配列 / map）

## awk

```bash
awk '{ cnt[$1]++ } END { for (k in cnt) print k, cnt[k] }' data.txt
```

---

## Lua

```lua
-- count.lua
local cnt = {}

for line in io.lines() do
    local key = line:match('^(%S+)')
    if key then
        cnt[key] = (cnt[key] or 0) + 1
    end
end

for k, v in pairs(cnt) do
    print(k, v)
end
```

---

# ③ awk 列処理 → lua（CSV / TSV）

## awk（TSV）

```bash
awk -F'\t' '{ print $1, $3 }' data.tsv
```

---

## Lua

```lua
-- tsv.lua
for line in io.lines() do
    local c1, c2, c3 = line:match('([^\t]+)\t([^\t]+)\t([^\t]+)')
    if c1 and c3 then
        print(c1, c3)
    end
end
```

---

# ④ awk 正規表現 + 条件 → lua

## awk

```bash
awk '$3 ~ /^ERR/ { print $1, $3 }' log.txt
```

---

## Lua

```lua
for line in io.lines() do
    local c1, c2, c3 = line:match('(%S+)%s+(%S+)%s+(%S+)')
    if c3 and c3:match('^ERR') then
        print(c1, c3)
    end
end
```

---

# ⑤ awk 状態遷移 → lua（これが一番価値あり）

## awk（読めない）

```bash
awk '
/^BEGIN/ { in=1; next }
/^END/   { in=0 }
in { print }
' file.txt
```

---

## Lua（自然）

```lua
local in_block = false

for line in io.lines() do
    if line:match('^BEGIN') then
        in_block = true
    elseif line:match('^END') then
        in_block = false
    elseif in_block then
        print(line)
    end
end
```

---

# ⑥ awk の BEGIN / END → lua

## awk

```bash
awk 'BEGIN { print "start" } { print } END { print "end" }'
```

---

## Lua

```lua
print('start')

for line in io.lines() do
    print(line)
end

print('end')
```

---

# ⑦ bash + awk パイプ → lua 1発に統合

## 元

```bash
cat data.txt |
grep ERROR |
awk '{ sum += $2 } END { print sum }'
```

---

## Lua に統合（高速）

```bash
cat data.txt | lua sum_error.lua
```

```lua
local sum = 0

for line in io.lines() do
    if line:match('ERROR') then
        local _, val = line:match('(%S+)%s+(%S+)')
        sum = sum + (tonumber(val) or 0)
    end
end

print(sum)
```

---

# awk → lua 変換の思考テンプレ

| awk     | lua                       |
| ------- | ------------------------- |
| `$1`    | `line:match('^(%S+)')`    |
| `$NF`   | `line:match('(%S+)%s*$')` |
| `FS`    | `match / gmatch`          |
| 配列      | table                     |
| `BEGIN` | 処理前                       |
| `END`   | 処理後                       |

---

# パフォーマンス注意点（重要）

❌ 行ごとに lua 起動
⭕ `cat | lua script.lua`

❌ print 乱用
⭕ `io.stdout:write()`

---

> **大量出力・高速化が必要 → `io.stdout:write()`**
> **デバッグ・少量出力 → `print()`**


## 1. 機能差（何が違う？）

### `print()`

```lua
print(a, b, c)
```

内部でやっていること：

* `tostring()` を各引数に適用
* 引数間に **タブ** を挿入
* 最後に **改行を自動追加**
* `io.stdout:write(...)` を呼ぶ

つまり **便利だが余計な仕事が多い**。

---

### `io.stdout:write()`

```lua
io.stdout:write(a, ' ', b, '\n')
```

* **何もしてくれない**
* 改行なし
* 文字列以外は自分で変換

👉 **最小コスト**

---

## 2. 速度差（重要）

### 100万行出力の感覚

| 方法                  | 体感    |
| ------------------- | ----- |
| `print()`           | 遅い    |
| `io.stdout:write()` | 明確に速い |

理由：

* `print()` は毎回

  * tostring
  * 区切り処理
  * 改行付与
* `write()` は **素通し**

---

### 実用例（ログ処理）

❌ 遅い

```lua
for line in io.lines() do
    print(line)
end
```

⭕ 速い

```lua
for line in io.lines() do
    io.stdout:write(line, '\n')
end
```

---

## 3. 改行制御（重要差）

### print は必ず改行

```lua
print('a')
print('b')
-- a
-- b
```

### write は自分で管理

```lua
io.stdout:write('a\nb\n')
```

---

## 4. フォーマット出力

### print（簡単）

```lua
print(x, y, z)
```

### write（推奨）

```lua
io.stdout:write(string.format('%d %.3f %s\n', x, y, z))
```

※ `string.format` + `write` は **高速 & 明示的**

---

## 5. stderr に出したい場合

```lua
io.stderr:write('error: invalid input\n')
```

print ではできない（stdout 固定）。

---

## 6. バッファリングの観点

* `write()` は **連続書き込みしやすい**
* 行単位より **塊で書く**とさらに速い

```lua
local buf = {}
for line in io.lines() do
    buf[#buf+1] = line
    buf[#buf+1] = '\n'
end
io.stdout:write(table.concat(buf))
```

---

## 7. 実務での使い分け指針

| 状況        | 使う                  |
| --------- | ------------------- |
| デバッグ      | `print()`           |
| 少量出力      | `print()`           |
| パイプ前提     | `write()`           |
| 大量ログ      | `write()`           |
| 生成系（CSV等） | `write()`           |
| stderr 出力 | `io.stderr:write()` |

---

## 8. bash + lua 文脈での結論

bash と組み合わせる場合：

```bash
cat big.log | lua filter.lua | sort
```

このとき Lua 側は **必ず**：

```lua
io.stdout:write(...)
```

にするべきです。

`print()` を使うと：

* パイプ全体が遅くなる
* CPU が無駄に回る

---



bash ↔ Lua のデータ受け渡しは **5パターン覚えれば十分**です。
「制御は bash、処理は Lua」という前提で、**実務で使う形だけ**まとめます。

---

## 1️⃣ 引数（argv）【最も基本】

### bash → lua

```bash
lua calc.lua 10 20
```

```lua
-- calc.lua
local a, b = tonumber(arg[1]), tonumber(arg[2])
print(a + b)
```

**用途**

* 設定値
* フラグ
* 少量データ

---

## 2️⃣ 標準入力（stdin）【最重要】

### bash → lua（大量データ）

```bash
cat data.txt | lua process.lua
```

```lua
-- process.lua
for line in io.lines() do
    -- heavy processing
    io.stdout:write(line, '\n')
end
```

**用途**

* テキスト
* CSV / TSV
* ログ

👉 **awk/sed の代替はこれ**

---

## 3️⃣ 環境変数（env）【設定向き】

### bash

```bash
export THRESHOLD=10
lua filter.lua
```

### lua

```lua
local th = tonumber(os.getenv('THRESHOLD')) or 0
```

**用途**

* 設定値
* 秘密情報（※注意）

---

## 4️⃣ 一時ファイル（大きな構造）

### bash

```bash
tmp=$(mktemp)
lua gen.lua > "$tmp"
lua consume.lua "$tmp"
rm "$tmp"
```

### lua

```lua
local file = arg[1]
for line in io.lines(file) do
    ...
end
```

**用途**

* 中間結果保存
* デバッグ
* 再利用

---

## 5️⃣ eval / here-doc（関数代替）

### bash → lua（インライン）

```bash
lua - "$@" <<'LUA'
local x, y = ...
print(x * y)
LUA
```

**用途**

* bash 関数の置き換え
* 短い処理

---

# 🔁 lua → bash の受け渡し

## 6️⃣ コマンド置換（値を返す）

```bash
result=$(lua calc.lua 10 20)
echo "$result"
```

Lua 側：

```lua
print(10 + 20)
```

---

## 7️⃣ exit code（真偽・状態）

### lua

```lua
if error then
    os.exit(1)
end
os.exit(0)
```

### bash

```bash
lua check.lua || echo "failed"
```

---

## 8️⃣ JSON（構造化データ）

### lua → bash (jq)

```lua
print('{"ok":true,"count":42}')
```

```bash
json=$(lua gen.lua)
echo "$json" | jq '.count'
```

**用途**

* 複数値
* 配列 / map

---

## 9️⃣ TSV / CSV（最速・最強）

### lua

```lua
io.stdout:write(id, '\t', value, '\n')
```

### bash

```bash
lua gen.lua | while IFS=$'\t' read id value; do
    ...
done
```

---


**bash + lua の並列処理**は「**bashで並列制御、luaで重処理**」


# ① xargs -P（最頻出・最安定）

## 構成

* bash：並列数管理
* lua：1ジョブ処理

---

### 例：ファイルを並列処理

```bash
find logs -name '*.log' |
xargs -P 4 -n 1 lua analyze.lua
```

```lua
-- analyze.lua
local file = arg[1]

for line in io.lines(file) do
    if line:match('ERROR') then
        io.stdout:write(file, '\n')
        break
    end
end
```

### ポイント

* `-P` = 並列数
* Lua は **1ファイル = 1プロセス**
* 安定・速い・簡単

---

# ② GNU parallel（最強）

```bash
find logs -name '*.log' |
parallel -j 8 lua analyze.lua {}
```

### 特徴

* 負荷制御が優秀
* ログ混線しにくい
* 進捗表示あり

---

# ③ bash job control（POSIX）

```bash
#!/bin/bash
max=4
running=0

for f in *.log; do
    lua analyze.lua "$f" &
    ((running++))

    if (( running >= max )); then
        wait -n
        ((running--))
    fi
done

wait
```

### 特徴

* GNU parallel 不要
* 移植性◎
* 記述は少し重い

---

# ④ stdin を分割して並列（高速）

## xargs + stdin

```bash
cat big.txt |
xargs -P 4 -n 1000 lua bulk.lua
```

```lua
-- bulk.lua
for line in io.lines() do
    -- heavy logic
    io.stdout:write(line, '\n')
end
```

### ポイント

* 1000行単位で処理
* Lua 起動回数削減
* 大量データ向け

---

# ⑤ 出力の衝突を避ける（重要）

## ❌ 危険

```lua
io.stdout:write(result, '\n')
```

→ 並列だと混線

---

## ⭕ 安全（1行1 write）

```lua
io.stdout:write(result .. '\n')
```

または

```bash
parallel --line-buffer lua task.lua {}
```

---

# ⑥ 集約パターン（Map → Reduce）

### Map（並列）

```bash
find . -name '*.log' |
parallel lua map.lua {} > tmp.tsv
```

### Reduce（単一）

```bash
lua reduce.lua tmp.tsv
```

---

# ⑦ CPU vs I/O の判断

| 処理    | 並列数         |
| ----- | ----------- |
| CPU重い | `nproc`     |
| I/O重い | `nproc * 2` |
| ネット   | 多め          |

```bash
jobs=$(nproc)
```

---

# ⑧ やってはいけない例（超重要）

```bash
while read line; do
    lua process.lua "$line" &
done
```

❌ Lua起動地獄
❌ コンテキストスイッチ地獄

---

# 🧠 設計テンプレ（実務）

```bash
#!/bin/bash
set -e

jobs=$(nproc)

find input -type f |
xargs -P "$jobs" -n 1 lua worker.lua |
lua reducer.lua
```

---


**bash + lua 並列処理**で一番ハマるのが「集約（reduce）」なので、
**ロックを一切使わない実務テクニック**だけを体系化します。

---

# 基本原則（超重要）

> **並列プロセスは「書かない」**
> **集約は「最後に1回」**

ロックレスはこれだけです。

---

# ① Map → Reduce（王道・最強）

## 構成

```
[input] → (parallel map) → TSV/CSV → (single reduce)
```

---

### Map（並列）

```bash
find logs -name '*.log' |
parallel lua map.lua {} > tmp.tsv
```

```lua
-- map.lua
local file = arg[1]
local count = 0

for line in io.lines(file) do
    if line:match('ERROR') then
        count = count + 1
    end
end

-- one record per process
io.stdout:write(file, '\t', count, '\n')
```

✔ 書き込み競合なし
✔ 1行 = 1プロセス

---

### Reduce（単一）

```lua
-- reduce.lua
local sum = 0

for line in io.lines() do
    local _, cnt = line:match('([^\t]+)\t(%d+)')
    sum = sum + tonumber(cnt)
end

print(sum)
```

---

# ② ファイル分離 → 最後に統合

## 並列（完全ロックレス）

```bash
mkdir -p tmp

find logs -name '*.log' |
parallel 'lua map.lua {} > tmp/{/.}.out'
```

* `{/.}` = 拡張子なしファイル名
* 各プロセス **専用ファイル**

---

## 集約

```bash
cat tmp/*.out | lua reduce.lua
```

---

# ③ シャーディング（キー別集約）

### 目的

* reduce も並列化したい
* 巨大データ

---

### Map（キーで分割）

```lua
-- shard.lua
local key, value = ...

local shard = tonumber(key) % 8
local f = io.open('tmp/shard_' .. shard .. '.tsv', 'a')
f:write(key, '\t', value, '\n')
f:close()
```

❌ これはロックが必要 → **NG**

---

### ⭕ ロックレス版

```bash
parallel lua shard.lua {} ::: input/*
```

```lua
-- shard.lua
local infile = arg[1]
local shards = {}

for line in io.lines(infile) do
    local key, value = line:match('(%S+)%s+(%S+)')
    local s = tonumber(key) % 8

    shards[s] = shards[s] or {}
    shards[s][#shards[s]+1] = key .. '\t' .. value .. '\n'
end

for s, buf in pairs(shards) do
    local f = io.open('tmp/shard_' .. s .. '_' .. infile, 'w')
    f:write(table.concat(buf))
    f:close()
end
```

👉 **「書き込み先 × プロセス」で完全分離**

---

# ④ stdout 原子性を使う（短文のみ）

### POSIX 保証

* **PIPE_BUF（通常 4KB）以内の write は原子的**

---

### 安全な例

```lua
io.stdout:write(id, '\t', value, '\n')
```

✔ 1 write
✔ 4KB 未満
✔ ロック不要

---

### 危険な例

```lua
print(id)
print(value)
```

❌ 混線

---

# ⑤ バイナリ集約（高速・上級）

### Map

```lua
-- write binary
io.stdout:write(string.pack('I4I4', key, value))
```

### Reduce

```lua
while true do
    local buf = io.stdin:read(8)
    if not buf then break end
    local k, v = string.unpack('I4I4', buf)
end
```

✔ 高速
✔ コンパクト
❌ 可読性低

---

# ⑥ SQLite を使わない理由（並列）

| 方法     | 評価    |
| ------ | ----- |
| SQLite | ロック地獄 |
| flock  | 遅い    |
| append | 壊れる   |

👉 **集約はファイル or stdout**

---

# ⑦ 実務テンプレ（完成形）

```bash
#!/bin/bash
set -e

jobs=$(nproc)
tmp=$(mktemp)

find input -type f |
xargs -P "$jobs" -n 1 lua map.lua > "$tmp"

lua reduce.lua < "$tmp"
rm "$tmp"
```

---


**SQLite / DuckDB を並列で使うときの「やっていい／ダメ」**をはっきり分けます。

---

# 結論サマリ（最重要）

| DB     | 並列 WRITE          | 並列 READ | 推奨構成                          |
| ------ | ----------------- | ------- | ----------------------------- |
| SQLite | ❌ 原則NG            | ⭕ OK    | **Map → ファイル → single write** |
| DuckDB | ❌ 外部からの同時WRITE NG | ⭕ 非常に強い | **外で並列 → DuckDBで集約**          |

---

# ① SQLite + 並列の落とし穴

## ❌ やってはいけない例

```bash
find logs -name '*.log' |
parallel lua insert.lua {}
```

```lua
-- insert.lua
db:exec("INSERT INTO errors VALUES (...)")
```

### 何が起きる？

* `database is locked`
* WALでも詰まる
* リトライ地獄
* スループット激減

---

## SQLite の本質

* **同時WRITEは1つだけ**
* WALでも：

  * writer は1
  * readers は複数

👉 並列WRITE = 設計ミス

---

## ⭕ 正しい SQLite 構成（王道）

### Map（並列・DB触らない）

```bash
parallel lua map.lua {} > tmp.tsv
```

### Reduce（単一WRITE）

```lua
-- reduce.lua
db:exec('BEGIN')

for line in io.lines() do
    -- parse
    stmt:bind(...)
    stmt:step()
    stmt:reset()
end

db:exec('COMMIT')
```

✔ 最速
✔ ロックなし
✔ 安定

---

## SQLite 高速化の必須設定（Reduce時）

```sql
PRAGMA journal_mode = WAL;
PRAGMA synchronous = OFF;
PRAGMA temp_store = MEMORY;
PRAGMA cache_size = -200000;
```

※ **Reduce専用プロセスのみ**

---

# ② SQLite で「どうしても並列WRITE」したい場合

### 選択肢（非推奨順）

1. **プロセスごとにDB分ける**
2. 後でATTACHして統合
3. 最終的にVACUUM

```bash
parallel lua map_to_db.lua {} ::: files/*
```

```sql
ATTACH 'db1.sqlite' AS d1;
INSERT INTO main.t SELECT * FROM d1.t;
```

👉 これも **実質 Map → Reduce**

---

# ③ DuckDB + 並列の考え方

## DuckDB の誤解

> 「DuckDB は並列に強い」
> → **内部並列が強い**
> → **外部からの同時WRITEはNG**

---

## ❌ やってはいけない例

```bash
parallel lua duck_insert.lua {}
```

```lua
conn:execute("INSERT INTO table VALUES (...)")
```

### 問題

* ファイルロック
* 不定期クラッシュ
* パフォーマンス低下
# 🏁 最終結論

> **並列中は DB を触るな**

* bash + lua：並列 Map
* ファイル / stdout：中間
* SQLite / DuckDB：最後に Reduce

これが
**最速・最安定・最小コード**です。

---

次に行くなら：

* SQLite-only で擬似並列を作る設計
* DuckDB + Parquet + compaction 戦略
* 巨大ログ（TB級）の shard / multi-reduce

どれいきます？

---

## ⭕ 正しい DuckDB 構成

### ① 外で並列（bash + lua）

```bash
parallel lua map.lua {} > tmp.parquet
```

### ② DuckDB で一気に読む（内部並列）

```sql
INSERT INTO table
SELECT * FROM read_parquet('tmp.parquet');
```

✔ DuckDB の得意技
✔ 超高速
✔ 安定

---

## DuckDB の真価（ここが重要）

* `read_csv_auto`
* `read_parquet`
* `COPY FROM`
* 内部スレッド最適化

👉 **「並列WRITE」より「並列READ」**

---

# ④ SQLite vs DuckDB 役割分担

| 用途       | SQLite | DuckDB |
| -------- | ------ | ------ |
| 小規模更新    | ◎      | △      |
| トランザクション | ◎      | △      |
| 分析       | △      | ◎      |
| 並列集約     | ❌      | ◎      |
| ファイル指向   | △      | ◎      |

---

# ⑤ Lua から DB を使う時の注意

## ❌ Map フェーズで DB open/close

```lua
for file in files do
    db = open()
    insert
    close()
end
```

→ オーバーヘッド地獄

---

## ⭕ Reduce フェーズでまとめて

```lua
db = open()
BEGIN
for all data do
    insert
COMMIT
close
```

---

# ⑥ 安全な設計テンプレ（完成形）

```bash
#!/bin/bash
set -e

jobs=$(nproc)
tmp=$(mktemp)

# Map (parallel, no DB)
find input -type f |
xargs -P "$jobs" -n 1 lua map.lua > "$tmp"

# Reduce (single DB writer)
lua reduce_to_sqlite.lua < "$tmp"
```

DuckDB 版：

```bash
parallel lua map.lua {} ::: files/*
duckdb db.duckdb -c "INSERT INTO t SELECT * FROM read_csv('$tmp')"
```

---

# ⑦ よくある誤解まとめ

| 誤解           | 真実       |
| ------------ | -------- |
| WALなら並列OK    | ❌        |
| DuckDBは何でも並列 | ❌        |
| ロックは悪        | ❌（設計が悪）  |
| DBで集約すべき     | ❌（最後でいい） |

---




10GB 級の CSV でもメモリをオーバーさせずに処理する

---

## 1. **Bash でチャンク分割 + Lua で処理**

```bash
#!/bin/bash
# huge.csv: 10GB級のファイルを処理

# 1,000,000行ごとに分割
split -l 1000000 huge.csv chunk_

# 各チャンクをLuaで処理して結果を保存
for f in chunk_*; do
    luajit -e "
local sum = 0
for line in io.lines('$f') do
    local n = line:match('^(%d+),')
    if n then sum = sum + tonumber(n) end
end
print(sum)
" > "$f.sum" &
done

# 並列処理が終わるまで待機
wait

# 全チャンクの結果を合計
awk '{s+=$1} END{print s}' chunk_*.sum
```

### 解説

1. **split**

   - 10GB を 1,000,000 行ずつに分割。
   - メモリに全体を読み込む必要がなくなる。

2. **LuaJIT**

   - 各チャンクの合計を高速に計算。
   - `io.lines()` はストリーム処理なので、行ごとに読み込みメモリ消費を抑える。

3. **並列化 (`&`)**

   - 複数チャンクを同時に処理して CPU コアを活用。

4. **結果の集約**

   - 最後に `awk` でチャンクごとの合計を足して最終合計を出す。

---

## 2. **パイプだけでディスクを使わない方法（ストリーム処理）**

ディスクにチャンクを作らず、そのままパイプで処理することも可能。

```bash
cat huge.csv | luajit -e '
local sum=0
for line in io.lines() do
    local n=line:match("^(%d+),")
    if n then sum=sum+tonumber(n) end
end
print(sum)
'
```

```bash
#!/bin/bash
# huge.csv → huge_transformed.csv

# 1,000,000行ごとに分割
split -l 1000000 huge.csv chunk_

# 各チャンクをLuaJITで処理
for f in chunk_*; do
    luajit -e "
local infile='$f'
local outfile='$f.out'

local input = io.open(infile, 'r')
local output = io.open(outfile, 'w')

for line in input:lines() do
    local col1, col2 = line:match('^(%d+),(%d+)')
    if col1 and col2 then
        col1 = tonumber(col1)
        col2 = tonumber(col2)
        if col1 % 2 == 0 then
            col2 = col2 * 2
        end
        output:write(col1 .. ',' .. col2 .. '\\n')
    else
        output:write(line .. '\\n')
    end
end

input:close()
output:close()
" &
done

# 並列処理が終わるまで待機

wait

# チャンク結果を結合

cat chunk\_\*.out > huge_transformed.csv

# オプション：一時ファイルを削除

rm chunk*\*
rm chunk*\*.out
```

---

### ■ luarocks の概要

- **目的**: Lua のライブラリ（モジュール）をインストール・管理する
- **形式**: `.rock` ファイル（ソースまたはバイナリ形式）
- **仕組み**:

  - GitHub や LuaRocks.org からライブラリを取得
  - 必要なら C ライブラリをビルドして Lua にリンク

---

### ■ 主なコマンド

| コマンド                  | 説明                     |
| ------------------------- | ------------------------ |
| `luarocks search <name>`  | パッケージを検索         |
| `luarocks install <name>` | パッケージをインストール |
| `luarocks remove <name>`  | アンインストール         |
| `luarocks list`           | インストール済み一覧     |
| `luarocks show <name>`    | パッケージの詳細を表示   |
| `luarocks path`           | Lua のパス設定を表示     |
| `luarocks config`         | 設定を確認・変更         |

---

### ■ 例: Lua で HTTP や JSON を扱う

```bash
luarocks install lua-http
luarocks install dkjson
```

使用例:

```lua
local http = require('http.request')
local json = require('dkjson')

local req = http.new_from_uri('https://api.github.com')
local headers, stream = req:go()
local body = stream:get_body_as_string()

print(json.encode({body=body}, {indent=true}))
```

---

### ■ インストール方法（Ubuntu など）

```bash
sudo apt install luarocks
```

または最新版:

```bash
curl -R -O https://luarocks.org/releases/luarocks-3.11.1.tar.gz
tar zxpf luarocks-3.11.1.tar.gz
cd luarocks-3.11.1
./configure && make && sudo make install
```

---

### ■ Lua バージョン対応

- LuaRocks は **Lua 5.1〜5.4** に対応
- LuaJIT もサポート（Lua 5.1 互換）

---

### ■ 確認

```bash
luarocks --version
luarocks list
```

---

## LuaRocks 代表モジュール一覧

### 1. **データ操作 / JSON**

| モジュール | 説明                              | インストール                 |
| ---------- | --------------------------------- | ---------------------------- |
| `dkjson`   | 純 Lua の JSON パーサ/生成        | `luarocks install dkjson`    |
| `cjson`    | C で高速化された JSON パーサ/生成 | `luarocks install lua-cjson` |
| `luajson`  | もうひとつの JSON ライブラリ      | `luarocks install luajson`   |

---

### 2. **HTTP / Web**

| モジュール   | 説明                                   | インストール                      |
| ------------ | -------------------------------------- | --------------------------------- |
| `lua-http`   | HTTP/HTTPS クライアント・サーバ        | `luarocks install lua-http`       |
| `luasocket`  | TCP/UDP ソケット, HTTP も簡易対応      | `luarocks install luasocket`      |
| `luasec`     | SSL/TLS 対応（luasocket 用）           | `luarocks install luasec`         |
| `resty-http` | OpenResty/Nginx 向け HTTP クライアント | `luarocks install lua-resty-http` |

---

### 3. **データベース / SQLite / MySQL**

| モジュール       | 説明                       | インストール                      |
| ---------------- | -------------------------- | --------------------------------- |
| `lsqlite3`       | SQLite3 操作               | `luarocks install lsqlite3`       |
| `luasql-sqlite3` | LuaSQL 経由の SQLite3 操作 | `luarocks install luasql-sqlite3` |
| `luasql-mysql`   | MySQL 接続                 | `luarocks install luasql-mysql`   |

---

### 4. **MQTT / IoT**

| モジュール | 説明                   | インストール               |
| ---------- | ---------------------- | -------------------------- |
| `luamqtt`  | MQTT クライアント      | `luarocks install luamqtt` |
| `mqtt`     | 純 Lua MQTT ライブラリ | `luarocks install mqtt`    |

---

### 5. **圧縮 / ファイル操作**

| モジュール       | 説明                      | インストール                     |
| ---------------- | ------------------------- | -------------------------------- |
| `luazip`         | ZIP 圧縮/解凍             | `luarocks install luazip`        |
| `lua-filesystem` | ファイル/ディレクトリ操作 | `luarocks install luafilesystem` |

---

### 6. **暗号 / ハッシュ / 暗号化**

| モジュール    | 説明                 | インストール                   |
| ------------- | -------------------- | ------------------------------ |
| `luacrypto`   | OpenSSL ベースの暗号 | `luarocks install luacrypto`   |
| `lua-openssl` | OpenSSL 完全ラッパー | `luarocks install lua-openssl` |
| `bcrypt`      | パスワードハッシュ   | `luarocks install bcrypt`      |

---

### 7. **ユーティリティ / 補助**

| モジュール | 説明                               | インストール                |
| ---------- | ---------------------------------- | --------------------------- |
| `penlight` | 拡張関数・テーブル操作・文字列操作 | `luarocks install penlight` |
| `inspect`  | テーブルの中身を見やすく表示       | `luarocks install inspect`  |
| `luaunit`  | ユニットテスト                     | `luarocks install luaunit`  |

---

### 8. **高速化 / LuaJIT 専用**

| モジュール       | 説明                               | インストール                      |
| ---------------- | ---------------------------------- | --------------------------------- |
| `ffi`            | LuaJIT FFI（C 関数呼び出し）       | 標準同梱                          |
| `bit`            | LuaJIT 用ビット演算                | 標準同梱                          |
| `luajit-request` | HTTP クライアント（LuaJIT 高速版） | `luarocks install luajit-request` |

---


**FFI を使わなくても LuaJIT はかなり速くできます。**
ポイントは「JIT が気持ちよくトレースできる形に書く」ことです。

以下、**実務で効く順**にまとめます。

---

## 0. 結論（超要約）

> **LuaJIT を速くする＝
> ① 型を固定
> ② table を避ける
> ③ 同じループを回す
> ④ JIT を壊さない**

---

## 1. number だけを使う（最重要）

LuaJIT は **number（double）特化**で最適化します。

### 良い

```lua
local x = 0.0
for i = 1, n do
  x = x + i * 0.5
end
```

### 悪い

```lua
local x = 0        -- integer
x = x + 0.5        -- 型揺れ
```

👉 **必ず `0.0` で初期化**

---

## 2. table アクセスを最小化する

### 悪い

```lua
for i=1,n do
  sum = sum + t[i]
end
```

### 良い（ローカル変数化）

```lua
local t_local = t
for i=1,n do
  sum = sum + t_local[i]
end
```

👉 **グローバル / upvalue は地雷**

---

## 3. グローバルを使わない

### 悪い

```lua
sum = sum + math.sin(x)
```

### 良い

```lua
local sin = math.sin
sum = sum + sin(x)
```

👉 **関数参照は必ず local**

---

## 4. 関数を小さくしすぎない

LuaJIT は **関数をまたぐと JIT が切れる**ことがある。

### 悪い

```lua
for i=1,n do
  sum = sum + f(i)
end
```

### 良い

```lua
for i=1,n do
  sum = sum + i * 0.5
end
```

👉 **ホットループ内では展開**

---

## 5. 分岐を減らす（トレースを壊さない）

### 悪い

```lua
if x > 0 then
  a = b + c
else
  a = d + e
end
```

### 良い（条件を外に出す）

```lua
if x > 0 then
  for i=1,n do a = b + c end
else
  for i=1,n do a = d + e end
end
```

👉 **ループ中に分岐しない**

---

## 6. for ループは単純に

* `for i=1,n` が最速
* `while` より安定
* `ipairs` / `pairs` は使わない

---

## 7. メタテーブルを避ける

### 悪い

```lua
setmetatable(t, mt)
```

👉 **JIT 無効化トリガー**

---

## 8. tostring / print をループに入れない

* デバッグ中は OK
* 本番では **即アウト**

---

## 9. JIT を確認する（必須）

```bash
luajit -jv script.lua
```

* `TRACE` が出る → OK
* `NYI` / `abort` → 遅い

---

## 10. LuaJIT が「C になる」例

```lua
local a, b = 1.0, 2.0
local s = 0.0

for i=1,1e8 do
  s = s + a * i + b
end
```

👉 **C と誤差レベル**

---

## 11. それでも遅いときは

### 優先順位

1. アルゴリズム改善
2. LuaJIT 最適化
3. FFI
4. C 実装

---

## 12. 一言まとめ

> **LuaJIT は
> 「素直な数値ループ」だけ書けば
> C に変身する**

---

### 最重要チェックリスト

* [ ] number 固定
* [ ] local 変数化
* [ ] table 最小
* [ ] 分岐なし
* [ ] JIT trace 確認

---

**「LuaJIT JIT abort 実例集」→「FFI を使うべき境界線」**の順で、
**実務で踏みがちな地雷だけ**を厳選します。

---

# 1. LuaJIT JIT abort 実例集（実戦版）

JIT abort ＝

> **「ここから先は JIT できない。インタプリタに戻る」**

`luajit -jv script.lua` で確認できます。

---

## 1.1 table が原因（最頻出）

### ❌ 例

```lua
for i=1,n do
  sum = sum + t[i]
end
```

### abort 理由

* table index
* hash/array 混在
* shape 不安定

### ✅ 回避

```lua
local t0 = t
for i=1,n do
  sum = sum + t0[i]
end
```

---

## 1.2 pairs / ipairs

### ❌

```lua
for k,v in pairs(t) do
  sum = sum + v
end
```

### abort

* iterator が不透明

### ✅

```lua
for i=1,#t do
  sum = sum + t[i]
end
```

---

## 1.3 型が揺れる

### ❌

```lua
x = 0
if cond then x = 1.5 end
```

### abort

* int → double

### ✅

```lua
x = 0.0
```

---

## 1.4 関数呼び出し（特に upvalue）

### ❌

```lua
function f(x) return x*2 end
for i=1,n do sum = sum + f(i) end
```

### abort

* trace split
* call boundary

### ✅

```lua
for i=1,n do sum = sum + i*2 end
```

---

## 1.5 math ライブラリ

### ❌

```lua
sum = sum + math.sin(x)
```

### abort

* C call

### ✅

```lua
local sin = math.sin
sum = sum + sin(x)
```

（完全回避は不可、緩和のみ）

---

## 1.6 メタテーブル

### ❌

```lua
setmetatable(t, mt)
```

### abort

* metamethod call

### ✅

* hot loop では使わない

---

## 1.7 可変長テーブル

### ❌

```lua
t[#t+1] = x
```

### abort

* shape change

### ✅

* サイズ固定
* preallocate

---

## 1.8 tostring / print

### ❌

```lua
print(i)
```

### abort

* I/O call

### ✅

* ループ外へ

---

## 1.9 NYI（Not Yet Implemented）

### 例

* 64bit 整数演算
* 複雑な bit 演算
* coroutine

👉 **仕様的に無理**

---

# 2. FFI を使うべき境界線

## 判断基準（これだけ覚えればOK）

> **「JIT abort を潰し切っても遅いなら FFI」**

---

## 2.1 FFI を使うべきケース（YES）

### ✅ 配列が本質

* 行列
* ベクトル
* 画像
* バッファ

👉 **table が限界**

---

### ✅ 同じループを何億回も回す

* 物理シミュレーション
* DSP
* ゲーム内部計算

---

### ✅ 既存 C ライブラリがある

* BLAS
* FFTW
* libpng

👉 **書かない理由がない**

---

## 2.2 FFI を使わない方がよいケース（NO）

### ❌ 制御フロー中心

* 状態遷移
* パーサ
* ゲームロジック

---

### ❌ 寿命管理が複雑

* ポインタ保持
* 非同期
* スレッド

---

### ❌ チーム開発

* C が読めない人が多い
* デバッグ重視

---

## 2.3 決断フローチャート（実用）

```text
遅い？
  ↓
JIT trace 出てる？
  ├─ NO → LuaJIT 書き方修正
  └─ YES
        ↓
table が原因？
  ├─ YES → FFI
  └─ NO
        ↓
演算が重い？
  ├─ YES → FFI / C
  └─ NO → アルゴリズム
```

---

# 3. 典型的な移行パターン

### Before（LuaJIT 限界）

```lua
for i=1,n do
  sum = sum + t[i] * w[i]
end
```

### After（FFI）

```lua
local a = ffi.new('double[?]', n)
local b = ffi.new('double[?]', n)
```

👉 **10〜50倍**

---

# 4. 一言まとめ

### JIT abort

> **「LuaJIT からの赤信号」**

### FFI 境界線

> **「構造が数値配列なら FFI」
> 「ロジックなら Lua」**


---


## 1️⃣ Lua 標準で簡単な行列計算

Lua の配列（テーブル）を使って行列を表現します。

### 例：2x2 行列の加算

```lua
-- 行列定義
local A = {
  {1, 2},
  {3, 4}
}

local B = {
  {5, 6},
  {7, 8}
}

-- 行列加算
local C = {}
for i = 1, #A do
  C[i] = {}
  for j = 1, #A[1] do
    C[i][j] = A[i][j] + B[i][j]
  end
end

-- 出力
for i = 1, #C do
  for j = 1, #C[1] do
    io.write(C[i][j], " ")
  end
  io.write("\n")
end
```

出力：

```
6 8
10 12
```

---

### 例：行列の掛け算

```lua
-- 2x2行列掛け算
local A = {{1,2},{3,4}}
local B = {{5,6},{7,8}}
local C = {{0,0},{0,0}}

for i=1,2 do
  for j=1,2 do
    for k=1,2 do
      C[i][j] = C[i][j] + A[i][k] * B[k][j]
    end
  end
end

-- 出力
for i=1,2 do
  for j=1,2 do
    io.write(C[i][j], " ")
  end
  io.write("\n")
end
```

出力：

```
19 22
43 50
```

---

## 2️⃣ LuaJIT + FFI で高速化

LuaJIT では C の線形代数ライブラリ（BLAS や OpenBLAS）を FFI で呼べます。
大量の行列計算や大規模データで効果抜群です。

```lua
local ffi = require("ffi")

ffi.cdef[[
void cblas_dgemm(int, int, int, int, int, int,
                 double, double*, int, double*, int,
                 double, double*, int);
]]

-- BLASがリンクされていれば、LuaJITから直接行列計算可能
```

- C ライブラリを呼ぶので**数百万次元でも高速**
- Bash + LuaJIT の組み合わせで、計算集約型スクリプトも作れる

---

## 3️⃣ 外部ライブラリを使う方法

Lua には行列計算用のライブラリもあります。

- **Torch7**（古いが強力、Lua ベース）
- **Luarocks 経由の `numlua`**
- **Lua Matrix Library (lmatrix)**

例：Luarocks でインストール

```bash
luarocks install numlua
```

使い方：

```lua
local nm = require("numlua")
local A = nm.array({{1,2},{3,4}})
local B = nm.array({{5,6},{7,8}})
local C = A + B
print(C)
```

---

## 1️⃣ LuaJIT 行列掛け算スクリプト例

`matmul.lua`:

```lua
#!/usr/bin/env luajit

local N = 1000  -- 行列サイズ

-- 行列生成関数（ランダム値）
local function random_matrix(n)
    local M = {}
    for i = 1, n do
        M[i] = {}
        for j = 1, n do
            M[i][j] = math.random()
        end
    end
    return M
end

-- 行列掛け算
local function matmul(A, B, n)
    local C = {}
    for i = 1, n do
        C[i] = {}
        for j = 1, n do
            local sum = 0
            for k = 1, n do
                sum = sum + A[i][k] * B[k][j]
            end
            C[i][j] = sum
        end
    end
    return C
end

-- 行列生成
local A = random_matrix(N)
local B = random_matrix(N)

-- 計算開始
local t0 = os.clock()
local C = matmul(A, B, N)
local t1 = os.clock()

print(string.format("Time elapsed: %.3f sec", t1 - t0))
-- 確認としてC[1][1]だけ表示
print("C[1][1] =", C[1][1])
```

---

## 2️⃣ 実行方法

```bash
chmod +x matmul.lua
./matmul.lua
```

---

## 1️⃣ 前提

- CSV は **カンマ区切りの数値**
- 行数と列数は同じ（正方行列）
- LuaJIT で高速に行列計算する

---

## 2️⃣ Bash + LuaJIT スクリプト例

`csv_matmul.lua`:

```lua
#!/usr/bin/env luajit

-- CSVをテーブルに読み込む
local function read_csv()
    local M = {}
    for line in io.lines() do
        local row = {}
        for num in line:gmatch("[^,]+") do
            table.insert(row, tonumber(num))
        end
        table.insert(M, row)
    end
    return M
end

-- 行列掛け算
local function matmul(A, B)
    local n = #A
    local C = {}
    for i = 1, n do
        C[i] = {}
        for j = 1, n do
            local sum = 0
            for k = 1, n do
                sum = sum + A[i][k] * B[k][j]
            end
            C[i][j] = sum
        end
    end
    return C
end

-- CSV読み込み（標準入力）
local A = read_csv()
local B = read_csv()

-- 計算開始
local t0 = os.clock()
local C = matmul(A, B)
local t1 = os.clock()

print(string.format("Time elapsed: %.3f sec", t1 - t0))

-- 出力例: Cの先頭行のみ
for j=1,#C[1] do
    io.write(C[1][j], ",")
end
print()
```

---

## 3️⃣ Bash 側で CSV を渡す例

CSV 例（`matrix.csv`）：

```csv
1,2,3
4,5,6
7,8,9
```

Bash からパイプで実行：

```bash
cat matrix.csv matrix.csv | ./csv_matmul.lua
```

- 上段の `matrix.csv` が **A**
- 下段の `matrix.csv` が **B**
- LuaJIT が両方読み込み、行列掛け算を行います

---

## 改良ポイント

1. **メモリ節約**

   - Lua テーブルにすべて読み込まず、**チャンク単位**で処理可能

2. **ファイルパイプ対応**

   - Bash から標準入力で行列を渡す

3. **高速化**

   - LuaJIT でネイティブループ
   - 大規模行列も数秒以内に計算可能

---

## 改良版スクリプト例

`csv_matmul_large.lua`:

```lua
#!/usr/bin/env luajit

-- CSVをチャンクで読み込み行列に変換する関数
local function read_csv_chunk(nrows)
    local M = {}
    local count = 0
    for line in io.lines() do
        local row = {}
        for num in line:gmatch("[^,]+") do
            table.insert(row, tonumber(num))
        end
        table.insert(M, row)
        count = count + 1
        if nrows and count >= nrows then
            break
        end
    end
    return M
end

-- 行列掛け算（A: m×k, B: k×n）
local function matmul(A, B)
    local m, k, n = #A, #B, #B[1]
    local C = {}
    for i = 1, m do
        C[i] = {}
        for j = 1, n do
            local sum = 0
            for p = 1, k do
                sum = sum + A[i][p] * B[p][j]
            end
            C[i][j] = sum
        end
    end
    return C
end

-- ファイルから行列を生成（必要に応じてチャンク指定）
local t0 = os.clock()
local A = read_csv_chunk() -- 標準入力またはBashパイプ
local B = read_csv_chunk() -- 2番目のCSV

-- 計算
local C = matmul(A, B)
local t1 = os.clock()

print(string.format("Time elapsed: %.3f sec", t1 - t0))

-- 出力先：必要に応じてファイルへ
for i=1,#C do
    for j=1,#C[1] do
        io.write(C[i][j])
        if j<#C[1] then io.write(",") end
    end
    io.write("\n")
end
```

---

## 使い方（Bash から）

```bash
cat A.csv B.csv | ./csv_matmul_large.lua > C.csv
```

- `A.csv` と `B.csv` が正方行列
- LuaJIT が高速に行列計算して `C.csv` に書き出す
- 数百万行でも LuaJIT なら数秒～十数秒で計算可能

---

## 💡 改良点まとめ

1. **チャンク処理**で巨大 CSV でもメモリ消費を抑制
2. Bash のパイプで入力可能
3. LuaJIT のネイティブ実行で高速
4. CSV 形式で直接ファイル出力可能

---

## 1️⃣ 改良ポイント

1. **行列をすべてメモリに読み込まない**

   - `A` を行ごとに読み込み
   - `B` は列ごとに保持（必要最小限の列だけ保持）

2. **Bash パイプ対応**

   - 標準入力から `A.csv` と `B.csv` を渡す

3. **出力ストリーム**

   - 計算が終わった行からすぐ出力

---

## 2️⃣ LuaJIT ストリーム行列計算スクリプト

`csv_matmul_stream.lua`:

```lua
#!/usr/bin/env luajit

-- 行列Aを標準入力から1行ずつ読み込むジェネレータ
local function read_csv_lines()
    local co = coroutine.create(function()
        for line in io.lines() do
            local row = {}
            for num in line:gmatch("[^,]+") do
                table.insert(row, tonumber(num))
            end
            coroutine.yield(row)
        end
    end)
    return co
end

-- 列ごとの行列Bをメモリに読み込む
local function read_csv_columns()
    local Bcols = {}
    local rows = {}
    for line in io.lines() do
        local row = {}
        local c = 1
        for num in line:gmatch("[^,]+") do
            row[c] = tonumber(num)
            Bcols[c] = Bcols[c] or {}
            table.insert(Bcols[c], tonumber(num))
            c = c + 1
        end
        table.insert(rows, row)
    end
    return Bcols, #rows, #Bcols
end

-- 1行分の行列Aと列ごとのBから計算
local function matmul_row(rowA, Bcols)
    local result = {}
    for j, colB in ipairs(Bcols) do
        local sum = 0
        for i = 1, #rowA do
            sum = sum + rowA[i] * colB[i]
        end
        result[j] = sum
    end
    return result
end

-- --- メイン処理 ---
-- Bashから: cat A.csv B.csv | ./csv_matmul_stream.lua
-- 1. 標準入力からAの行ジェネレータ
local coA = read_csv_lines()

-- 2. Bの行列はファイルで渡す場合、2つ目のファイルを再度開く
-- 今回はB.csvを別ファイルとして渡す前提
local Bfile = arg[1] or "B.csv"
local fB = io.open(Bfile, "r")
local Bcols, BrowN, BcolN = {},0,0
do
    local lines = {}
    for line in fB:lines() do table.insert(lines,line) end
    fB:close()
    for r, line in ipairs(lines) do
        local c=1
        for num in line:gmatch("[^,]+") do
            Bcols[c] = Bcols[c] or {}
            Bcols[c][r] = tonumber(num)
            c = c + 1
        end
    end
end

-- 3. 計算とストリーム出力
while true do
    local ok, rowA = coroutine.resume(coA)
    if not ok or not rowA then break end
    local rowC = matmul_row(rowA, Bcols)
    for j=1,#rowC do
        io.write(rowC[j])
        if j<#rowC then io.write(",") end
    end
    io.write("\n")
end
```

---

## 3️⃣ Bash での使い方

```bash
# A.csvの行列を標準入力で渡し、B.csvは引数として指定
cat A.csv | ./csv_matmul_stream.lua B.csv > C.csv
```

---

## 1️⃣ 基本

Lua には標準で SQLite は組み込まれていませんが、**Lua 用の SQLite バインディング** を使うことで操作可能です。

### 主な方法

1. **LuaRocks で LuaSQLite3 を使う**（最も一般的）
2. **LuaJIT + FFI で SQLite を直接呼ぶ**（高速）

---

## 2️⃣ LuaSQLite3 の例

### インストール

```bash
luarocks install luasql-sqlite3
```

### サンプルコード

```lua
local sqlite3 = require("luasql.sqlite3")

-- SQLite環境を作成
local env = sqlite3.sqlite3()

-- データベースに接続（なければ作成）
local conn = env:connect("test.db")

-- テーブル作成
conn:execute([[
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    name TEXT,
    age INTEGER
)
]])

-- データ挿入
conn:execute("INSERT INTO users (name, age) VALUES ('Alice', 30)")
conn:execute("INSERT INTO users (name, age) VALUES ('Bob', 25)")

-- データ取得
local cur = conn:execute("SELECT * FROM users")
local row = cur:fetch({}, "a") -- "a" は連想配列として取得

while row do
    print(row.id, row.name, row.age)
    row = cur:fetch(row, "a")
end

-- 接続閉じる
conn:close()
env:close()
```

---

## 3️⃣ LuaJIT + FFI で SQLite を使う（高速）

LuaJIT は C の SQLite ライブラリを直接呼べるので、**大規模 DB や高速処理に最適**です。

```lua
local ffi = require("ffi")

ffi.cdef[[
typedef struct sqlite3 sqlite3;
typedef struct sqlite3_stmt sqlite3_stmt;
int sqlite3_open(const char *filename, sqlite3 **ppDb);
int sqlite3_close(sqlite3*);
int sqlite3_exec(sqlite3*, const char *sql, void*, void*, char **errmsg);
]]

local lib = ffi.load("sqlite3")

local db = ffi.new("sqlite3*[1]")
assert(lib.sqlite3_open("test.db", db) == 0)
print("Database opened!")

-- SQL 実行例
assert(lib.sqlite3_exec(db[0], "CREATE TABLE IF NOT EXISTS t1(id INT, val TEXT);", nil, nil, nil) == 0)
print("Table created!")

lib.sqlite3_close(db[0])
```

- FFI を使うと **ループ内で大量挿入** も高速
- LuaSQLite3 よりさらに **ネイティブ速度**

---

## 1️⃣ 基本的な考え方

CUI ダッシュボードは大体以下の機能を使います：

1. **画面クリア**

   ```lua
   io.write("\27[2J")  -- 画面クリア
   io.write("\27[H")   -- カーソルを左上に戻す
   ```

2. **カーソル移動**

   ```lua
   io.write("\27[5;10H")  -- 5行目、10列目に移動
   ```

3. **色付け**

   ```lua
   io.write("\27[31m")  -- 赤文字
   io.write("\27[0m")   -- 色リセット
   ```

4. **定期更新**

   - Lua の `os.execute("sleep 1")` か `socket.sleep(1)` で一定間隔で更新

---

## 2️⃣ 簡単なサンプル：リアルタイム数値表示

```lua
#!/usr/bin/env luajit
local socket = require("socket")  -- sleep用

-- データサンプル
local value = 0

while true do
    -- 画面クリア
    io.write("\27[2J\27[H")

    -- ヘッダ
    io.write("\27[1;32mCUI Dashboard\27[0m\n")
    io.write("====================\n")

    -- データ表示
    io.write(string.format("Counter: \27[34m%d\27[0m\n", value))
    io.write(string.format("CPU Load: \27[31m%.2f%%\27[0m\n", math.random() * 100))

    -- グラフ風表示
    local bar = math.floor(math.random() * 50)
    io.write("Progress: [" .. string.rep("#", bar) .. string.rep("-", 50-bar) .. "]\n")

    -- 更新
    value = value + 1
    socket.sleep(0.5)
end
```

---

## 3️⃣ ターミナル UI ライブラリ（さらに便利）

Lua だけで低レベルのエスケープシーケンスを書くより、**ライブラリを使うと便利**です。

1. **lcurses / curses**

   - `ncurses` を Lua から使える
   - ウィンドウ分割、文字描画、キー入力に対応
   - 例：

     ```lua
     local curses = require "curses"
     curses.initscr()
     curses.cbreak()
     curses.echo(false)
     local win = curses.newwin(10, 40, 0, 0)
     win:addstr(0,0,"Hello CUI")
     win:refresh()
     curses.endwin()
     ```

2. **termfx**（LuaJIT 向け）

   - 高速描画、色付き文字、カーソル制御
   - 軽量で簡単に CUI ダッシュボードを作れる

---

## 1️⃣ 標準 Lua では HTTP はない

Lua の標準ライブラリには HTTP クライアントは入っていません。そのため以下の方法を使います：

1. **LuaSocket**（シンプル、LuaRocks で導入可能）
2. **LuaHTTP**（LuaRocks、HTTPS 対応、非同期も可）
3. **LuaJIT + FFI + cURL**（高速、LuaJIT 向け）

---

## 2️⃣ LuaSocket を使う（簡単）

### インストール

```bash
luarocks install luasocket
```

### GET リクエスト例

```lua
local http = require("socket.http")
local ltn12 = require("ltn12")

local url = "http://httpbin.org/get"
local response = {}

local res, code, headers, status = http.request{
    url = url,
    sink = ltn12.sink.table(response)
}

if res then
    print("Status code:", code)
    print("Response body:", table.concat(response))
else
    print("Request failed:", status)
end
```

---

### POST リクエスト例

```lua
local http = require("socket.http")
local ltn12 = require("ltn12")

local url = "http://httpbin.org/post"
local body = "name=Alice&age=30"
local response = {}

local res, code = http.request{
    url = url,
    method = "POST",
    headers = {
        ["Content-Length"] = #body,
        ["Content-Type"] = "application/x-www-form-urlencoded"
    },
    source = ltn12.source.string(body),
    sink = ltn12.sink.table(response)
}

print("Status code:", code)
print("Response body:", table.concat(response))
```

---

## 3️⃣ LuaHTTP を使う（HTTPS 対応）

### インストール

```bash
luarocks install http
```

### GET リクエスト例

```lua
local http_request = require("http.request")

local headers, stream = assert(http_request.new_from_uri("https://httpbin.org/get"):go())
local body = assert(stream:get_body_as_string())

print(headers)
print(body)
```

- HTTPS が必要な場合は LuaHTTP のほうが簡単
- LuaSocket は HTTPS だと `luasec` が必要

---

## 4️⃣ LuaJIT + cURL FFI（高速・大量リクエスト向け）

```lua
local ffi = require("ffi")
ffi.cdef[[
typedef void CURL;
CURL *curl_easy_init(void);
int curl_easy_setopt(CURL *handle, int option, ...);
int curl_easy_perform(CURL *handle);
void curl_easy_cleanup(CURL *handle);
]]

local curl = ffi.load("curl")
local handle = curl.curl_easy_init()
-- オプション設定、実行、後処理
curl.curl_easy_cleanup(handle)
```

---

**Lua + Copas で非同期 HTTP サーバ**

## 1. **準備**

- Lua 5.1/5.2
- LuaSocket (`luarocks install luasocket`)
- Copas (`luarocks install copas`)

---

## 2. **簡易非同期 HTTP サーバ例**

```lua
-- async_http.lua
local socket = require("socket")
local copas  = require("copas")

-- サーバ作成
local server = assert(socket.bind("*", 8080))
server:settimeout(0)  -- ノンブロッキング

-- Copasでサーバに接続ハンドラを追加
copas.addserver(server, function(client)
    client = copas.wrap(client)  -- 非同期ラップ

    -- リクエスト受信
    local request_line = client:receive("*l")
    if request_line then
        print("Received: " .. request_line)

        -- 簡単なHTTPレスポンス
        local body = "Hello from Lua + Copas!\n"
        local response = table.concat{
            "HTTP/1.1 200 OK\r\n",
            "Content-Type: text/plain\r\n",
            "Content-Length: ", #body, "\r\n",
            "Connection: close\r\n\r\n",
            body
        }
        client:send(response)
    end

    client:close()
end)

print("Async HTTP server running on port 8080...")
copas.loop()  -- 非同期ループ開始
```

---

## 3. **実行**

```bash
lua async_http.lua
```

確認:

```bash
curl http://localhost:8080
```

---

## 🧩 1. Lua で MQTT を使う方法は 2 つある

| 方法                                       | 概要                                        | 備考                    |
| ------------------------------------------ | ------------------------------------------- | ----------------------- |
| **① LuaSocket + LuaMQTT ライブラリ**       | 一般的な Lua 環境で使える純 Lua 実装        | 軽量で依存少ない        |
| **② OpenResty / NodeMCU など組み込み環境** | 特定環境（ESP8266 や nginx/LuaJIT）用の実装 | IoT や Web サーバー向け |

---

## 🚀 2. 通常の Lua 環境で使う例（LuaMQTT）

### 🔧 インストール

Ubuntu などで LuaRocks を使います：

```bash
sudo apt install luarocks
sudo luarocks install lua-mqtt
sudo luarocks install luasocket
```

これで `mqtt` と `socket` モジュールが使えるようになります。

---

## 📜 3. サンプルコード（Subscribe）

```lua
local mqtt = require('mqtt')

-- Connect to broker
local client = mqtt.client{
    uri = 'mqtt://test.mosquitto.org',
    clean = true
}

-- Subscribe callback
client:on{
    message = function(sub, topic, payload)
        print('Received:', topic, payload)
    end
}

-- Subscribe topic
client:subscribe('test/topic')

-- Start loop
client:loop_forever()
```

この例では、`test.mosquitto.org`（公開 MQTT ブローカ）に接続し、
`test/topic` に届いたメッセージを CUI に表示します。

---

## 📤 4. Publish（送信）

```lua
local mqtt = require('mqtt')

local client = mqtt.client{
    uri = 'mqtt://test.mosquitto.org',
    clean = true
}

client:connect()
client:publish('test/topic', 'Hello from Lua!', 0, false)
client:disconnect()
```

---

## ⚡ 5. LuaJIT でも使用可能

`luajit` でも同じコードが動作します。
速度がほしい場合は LuaJIT + LuaSocket の組み合わせが最適です。

例：

```bash
luajit mqtt_sub.lua
```

---

## 🧠 6. 応用（リアルタイム CUI ダッシュボード）

MQTT で受け取ったデータを Lua の CUI ライブラリ（例：`ansicolors`, `curses`, `termfx`）で表示すれば、
軽量な**ターミナルダッシュボード**も作れます。

---

## ⚙️ 7. 代表的な Lua MQTT ライブラリ

| ライブラリ                  | 特徴                              |
| --------------------------- | --------------------------------- |
| **lua-mqtt**                | 純 Lua 実装。軽量でどこでも動く。 |
| **luamqttc**                | C バインディングで高速。          |
| **OpenResty resty-mqtt**    | nginx/LuaJIT 上で動作。           |
| **NodeMCU mqtt モジュール** | IoT 用（ESP8266 など）。          |

---

## 💬 まとめ

| 比較項目     | Lua             | Node.js            |
| ------------ | --------------- | ------------------ |
| 起動時間     | 速い（ms 単位） | やや遅い           |
| メモリ消費   | 少ない（数 MB） | 多い（数十 MB）    |
| ライブラリ数 | 少なめ          | 豊富               |
| MQTT 実装    | 複数あり、軽量  | `mqtt.js` など豊富 |

Lua は**軽量なデーモンや IoT 用途**に最適、
Node.js は**Web 統合や API 連携が多い場合**に有利です。

---

では、Ubuntu 上で **LuaJIT + LuaRocks 環境** を構築し、
SQLite・HTTP・MQTT を動かす **最小サンプル** を作る手順とコードを示します。

---

## 1. LuaJIT + LuaRocks インストール

```bash
# LuaJITをインストール
sudo apt update
sudo apt install -y luajit build-essential libreadline-dev

# LuaRocksをインストール
sudo apt install -y luarocks

# LuaRocksでLuaJIT用を使う場合
# パス確認
luarocks config lua_version
```

確認:

```bash
luajit -v
luarocks --version
```

---

## 2. 必要モジュールのインストール

```bash
# SQLite3
luarocks install lsqlite3

# HTTPクライアント
luarocks install lua-http

# MQTTクライアント
luarocks install luamqtt

# JSON
luarocks install dkjson
```

---

## 3. サンプルコード（main.lua）

```lua
-- main.lua
local sqlite3 = require("lsqlite3")
local http = require("http.request")
local mqtt = require("luamqtt")
local json = require("dkjson")

-- ========================
-- SQLite3 テスト
-- ========================
local db = sqlite3.open_memory()
db:exec("CREATE TABLE test (id INTEGER PRIMARY KEY, name TEXT);")
db:exec("INSERT INTO test (name) VALUES ('Alice');")
db:exec("INSERT INTO test (name) VALUES ('Bob');")

for row in db:nrows("SELECT * FROM test;") do
    print("SQLite:", row.id, row.name)
end
db:close()

-- ========================
-- HTTP GET テスト
-- ========================
local req = http.new_from_uri("https://api.github.com")
local headers, stream = assert(req:go())
local body = assert(stream:get_body_as_string())
print("HTTP body length:", #body)

-- JSON パーステスト
local parsed, _, err = json.decode(body)
if parsed then
    print("JSON keys example:", next(parsed))
else
    print("JSON decode error:", err)
end

-- ========================
-- MQTT テスト (ローカルブローカー用)
-- ========================
local client = mqtt.client{
    uri = "mqtt://localhost:1883",
    clean = true,
}

client:connect()
client:subscribe{"test/topic"}
client:publish{topic="test/topic", payload="Hello Lua MQTT!"}
print("MQTT published message")
client:disconnect()
```

---

## 4. 実行方法

```bash
luajit main.lua
```

出力例:

```
SQLite: 1 Alice
SQLite: 2 Bob
HTTP body length: 12345
JSON keys example: current_user_url
MQTT published message
```

---

## 5. ポイント

1. **LuaJIT で高速動作**

   - LuaJIT の整数ループや C ライブラリ呼び出しは非常に高速。

2. **LuaRocks で簡単モジュール管理**

   - HTTP, MQTT, SQLite, JSON を一括で管理可能。

3. **メモリ軽量**

   - Python や Node.js より軽量で高速。

4. **IoT や CUI ダッシュボード** に最適

   - LuaJIT + SQLite + MQTT で軽量サーバやデータ収集ツールが作れる。

---
