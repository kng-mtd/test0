# bash script cheatsheet

## notes

- run default editor
  ctrl+x+e

---

- super user
  sudo command
  sudo user0
  sudo -i
  exit
  sudo shutdown -h now

---

- sudo group
  getent group sudo
  sudo adduser user0
  sudo usermod -aG sudo user0
  sudo deluser user0

---

- backup .bashrc
  cp .bashrc .bashrc.org

---

- open terminal
  gnome-terminal

---

- bash builtin commands
  compgen -b
  help

| コマンド                                  | 説明                                 |
| ----------------------------------------- | ------------------------------------ |
| `:`                                       | 何もしない（常に成功）。             |
| `.` / `source`                            | スクリプトを現在のシェルで実行。     |
| `break`                                   | ループを抜ける。                     |
| `continue`                                | 次のループへ進む。                   |
| `eval`                                    | 文字列をコマンドとして評価・実行。   |
| `exec`                                    | 現シェルを別のコマンドに置き換える。 |
| `exit`                                    | シェルを終了する。                   |
| `return`                                  | 関数から値を返す。                   |
| `if` / `then` / `else` / `elif` / `fi`    | 条件分岐構文。                       |
| `for` / `while` / `until` / `do` / `done` | ループ構文。                         |
| `case` / `esac`                           | パターンマッチ分岐。                 |
| `trap`                                    | シグナル受信時の処理を設定。         |
| `wait`                                    | 子プロセス終了を待機。               |

| コマンド                 | 説明                                 |
| ------------------------ | ------------------------------------ |
| `echo`                   | テキストを出力。                     |
| `printf`                 | 書式付き出力（echo より安全）。      |
| `read`                   | 標準入力から行を読み込む。           |
| `mapfile` / `readarray`  | 標準入力を配列に読み込む。           |
| `pwd`                    | 現在のディレクトリを表示。           |
| `cd`                     | カレントディレクトリを変更。         |
| `pushd`                  | ディレクトリスタックに追加して移動。 |
| `popd`                   | スタックを戻る。                     |
| `dirs`                   | ディレクトリスタックを表示。         |
| `test` / `[ ]` / `[[ ]]` | 条件式評価。                         |
| `ulimit`                 | リソース制限の設定・表示。           |
| `times`                  | CPU 時間を表示。                     |
| `true` / `false`         | 常に成功または失敗を返す。           |

| コマンド              | 説明                                |
| --------------------- | ----------------------------------- |
| `declare` / `typeset` | 変数の型・属性を設定。              |
| `local`               | 関数内のローカル変数を定義。        |
| `readonly`            | 変数を読み取り専用にする。          |
| `unset`               | 変数または関数を削除。              |
| `let`                 | 算術式を評価。                      |
| `set`                 | シェルオプションや変数を設定。      |
| `export`              | 環境変数を設定または一覧表示。      |
| `shopt`               | Bash 固有のシェルオプションを設定。 |
| `getopts`             | スクリプト内の引数を解析。          |

| コマンド  | 説明                                             |
| --------- | ------------------------------------------------ |
| `help`    | builtin コマンドのヘルプ表示。                   |
| `type`    | コマンドの種類（builtin / file / alias）を表示。 |
| `builtin` | builtin を強制実行（同名外部コマンドを無視）。   |
| `command` | alias や関数を無視して実行。                     |
| `caller`  | 現在の関数呼び出しスタック情報を出力。           |
| `history` | コマンド履歴を表示・操作。                       |
| `fc`      | 履歴から再実行または編集。                       |
| `hash`    | コマンドパスのキャッシュを操作。                 |
| `enable`  | builtin の有効化・無効化を設定。                 |

| コマンド  | 説明                                     |
| --------- | ---------------------------------------- |
| `bg`      | 停止したジョブをバックグラウンドで再開。 |
| `fg`      | ジョブをフォアグラウンドで再開。         |
| `jobs`    | 現在のジョブ一覧を表示。                 |
| `disown`  | ジョブをシェル管理から切り離す。         |
| `kill`    | プロセスにシグナルを送信。               |
| `suspend` | シェルを一時停止。                       |
| `logout`  | ログインシェルを終了。                   |

| コマンド   | 説明                                             |
| ---------- | ------------------------------------------------ |
| `alias`    | コマンドの別名を定義。                           |
| `unalias`  | alias を削除。                                   |
| `compgen`  | 補完候補を生成。                                 |
| `complete` | 補完動作を定義。                                 |
| `compopt`  | 補完オプションを設定。                           |
| `umask`    | ファイル作成時のデフォルトパーミッションを設定。 |

---

bash external commands

echo $PATH
ls /bin /dir/bin

find $(echo $PATH | tr ':' ' ') -maxdepth 1 -type f -executable 2>/dev/null
find $(echo $PATH | tr ':' ' ') -maxdepth 1 -type f -executable 2>/dev/null -exec basename {} \;

---

- apt managed packages
  apt list --installed

---

- all usable commands
  compgen -c
  compgen -c | sort -u

---

- all excutable binary files
  echo $PATH | tr ':' '\n' | xargs -I {} find {} -maxdepth 1 -type f -executable 2>/dev/null

---

| カテゴリ        | コマンド例                                                                       |
| --------------- | -------------------------------------------------------------------------------- |
| ファイル操作    | `ls`, `cp`, `mv`, `rm`, `mkdir`, `rmdir`, `find`, `locate`                       |
| テキスト処理    | `cat`, `less`, `grep`, `awk`, `sed`, `head`, `tail`, `sort`, `uniq`, `cut`, `tr` |
| 圧縮/アーカイブ | `tar`, `gzip`, `zip`, `unzip`, `xz`                                              |
| システム情報    | `uname`, `lsb_release`, `df`, `du`, `top`, `ps`, `free`, `uptime`                |
| ネットワーク    | `ping`, `curl`, `wget`, `netstat`, `ss`, `ip`, `ifconfig`, `nslookup`            |
| ユーザー/権限   | `sudo`, `su`, `chmod`, `chown`, `id`, `whoami`, `groups`                         |
| プロセス管理    | `kill`, `pkill`, `jobs`, `bg`, `fg`, `nice`, `renice`                            |
| パッケージ管理  | `apt`, `dpkg`, `snap`                                                            |
| エディタ        | `nano`, `vim`, `vi`, `less`                                                      |
| ログ・監査      | `dmesg`, `journalctl`, `tail -f /var/log/syslog`                                 |

---

- shared object (.so)
  ldd /bin/bash

| ライブラリ名         | 役割                                                                                |
| -------------------- | ----------------------------------------------------------------------------------- |
| linux-vdso.so.1      | カーネルが提供する仮想的なシステムコールアクセラレータ                              |
| libtinfo.so.6        | ターミナル情報ライブラリ（ncurses の一部）。Bash のコマンドライン編集機能などで使用 |
| libdl.so.2           | `dlopen()` などの関数を提供。動的に.so をロードできる                               |
| libc.so.6            | GNU C ライブラリ（glibc）。標準 I/O、文字列、ファイル操作など Bash 内部もこれを利用 |
| ld-linux-x86-64.so.2 | ELF 実行ファイルをロード・リンクするためのランタイムリンカ                          |

sudo find /lib /x86*64-linux-gnu/ -type f -name '*.so*' 2>/dev/null | sort | less
sudo find /lib /usr/lib -type f -name '*.so\_' 2>/dev/null | sort | less

| カテゴリ                  |                                                 |
| ------------------------- | ----------------------------------------------- |
| 標準 C ライブラリ         | `libc.so.6`, `libm.so.6`                        |
| 数学関数ライブラリ        | `libm.so.6`                                     |
| スレッド（POSIX Threads） | `libpthread.so.0`                               |
| 動的リンク機能            | `libdl.so.2`                                    |
| 圧縮                      | `libz.so.1`, `libbz2.so.1`                      |
| ネットワーク              | `libresolv.so.2`, `libnsl.so.1`, `libcurl.so.4` |
| OpenSSL 関連              | `libssl.so.3` / `libcrypto.so.3`                |
| 端末操作                  | `libtinfo.so`, `libncurses.so`                  |
| セキュリティ              | `libcrypto.so`, `libssl.so`                     |
| SQLite データベース       | `libsqlite3.so.0`                               |
| C++標準ライブラリ         | `libstdc++.so.6`                                |
| Python 埋め込みランタイム | `libpython3.x.so`                               |

- apt managed libraries (lib---)
  apt list --installed | grep '^lib'

---

## script rules

### run script

one liner
bash -c '--script--'
or
{ --script--;--script--;...; }

script file
script.sh

```
#!/bin/bash
( bash script )
```

bash script.sh

chmod +x script.sh
./script.sh

check syntax

bash -n script.sh

debug mode

bash -x script.sh

```
set -x
---
---
...
set +x
```

---

### path

- directory
  dir1/dir2.../
- file
  dir1/dir2.../file

---

### comment out with

`# comment`

### break line with ;

`command1 ; command2 ;...`

### continue line with \

```
command ---\
---\
---
```

### pipe with |

```
command1 | command2 | command3..

{
  command1
  command2
  ...
} | command3
```

---

### stdin, stdout, stderr

from file, nothing

```
--- < file
--- < /dev/null
```

output to new file

```
--- > file
```

add output to exist file

```
--- >> file
```

process error message

```
--- > /dev/null # show only error
--- 2> /dev/null # show only result
--- > /dev/null 2>&1 # show nothing
--- 2> file, --- 2>> file # save error message
--- > file1 2> file2 # save each output to other file
--- > file 2>&1 # save all output to a same file
```

add string to command

```
command <<< str

command <<EOF
line1
line2
...
EOF
```

---

### auto run

| コマンド     | 説明                           |
| ------------ | ------------------------------ |
| `crontab -e` | 現在のユーザーのジョブを編集   |
| `crontab -l` | 登録されているジョブ一覧を表示 |
| `crontab -r` | 現在のジョブを削除             |

crontab -e
分 時 日 月 曜日 コマンド

| 設定           | 意味           | cron 書式      |
| -------------- | -------------- | -------------- |
| 毎分           | 毎分実行       | `* * * * *`    |
| 10 分ごと      | 10 分間隔      | `*/10 * * * *` |
| 毎時 0 分      | 毎時実行       | `0 * * * *`    |
| 毎日 0 時      | 毎日深夜に実行 | `0 0 * * *`    |
| 毎週日曜 0 時  | 週次実行       | `0 0 * * 0`    |
| 毎月 1 日 0 時 | 月次実行       | `0 0 1 * *`    |

cron の出力は /var/log/syslog に記録されます。

`grep CRON /var/log/syslog`

---

### sequence

- {0..9}
  0 1 2...9
- {00...10}
  00 01..10
- {9..0}
  9 8...0
- {0..10..2}
  0 2...10
- {a..z}
  a b...z
- {0..2}\_{0..2}
  0_0 0_1 0_2 1_0 1_1 1_2 2_0 2_1 2_2
- {a..c}\_{0..2}
  a_0 a_1 a_2 b_0 b_1 b_2 c_0 c_1 c_2

---

### env variable

```
printenv

$HOME
$USER
$HOSTNAME
$ PATH
echo $PATH | sed 's/:/\n/g'


var=str
export var
bash script.sh

script.sh
echo $var


export var=value
    or
add 'var=value' to .bashrc
source ~/.bashrc

PATH="$PATH:new path"

$RANDOM
$RANDOM$RANDOM
```

---

### variable

```
var=string
var='string has space'
var=$(command)

$var
"$var in string" # interpolation / expansion
$((var)) # as integer
```

---

### parameter expansion

| 処理                             | パラメータ展開     | 同等コマンド                                       |
| :------------------------------- | :----------------- | :------------------------------------------------- |
| 文字数                           | `${#var}`          | `echo -n "$var" \| wc -c`                          |
| i 文字目から末尾まで             | `${var:i}`         | `echo "$var" \| cut -c$((i+1))-`                   |
| 後ろから i 文字目から末尾まで    | `${var: -i}`       | `echo "$var" \| rev \| cut -c1-$i \| rev`          |
| i 文字目から k 文字取得          | `${var:i:k}`       | `echo "$var" \| cut -c$((i+1))-$((i+k))`           |
| 後ろから i 文字目から k 文字取得 | `${var: -i:k}`     | `echo "$var" \| rev \| cut -c$i-$((i+k-1)) \| rev` |
| 小文字化                         | `${var,,}`         | `echo "$var" \| tr '[:upper:]' '[:lower:]'`        |
| 大文字化                         | `${var^^}`         | `echo "$var" \| tr '[:lower:]' '[:upper:]'`        |
| 置換                             | `${var/str0/str1}` | `echo "$var" \| sed 's/str0/str1/'`                |
| デフォルト値                     | `${var:-default}`  | `[ -n "$var" ] && echo "$var" \|\| echo "default"` |

| 構文           | 意味                   | 例                                       |
| :------------- | :--------------------- | :--------------------------------------- |
| `${var#glob}`  | 前方の最短マッチを削除 | `${var#*/}` → 最初の `/` まで削除        |
| `${var##glob}` | 前方の最長マッチを削除 | `${var##*/}` → 最後の `/` まで削除       |
| `${var%glob}`  | 後方の最短マッチを削除 | `${var%.*}` → 最初の `.` から後ろを削除  |
| `${var%%glob}` | 後方の最長マッチを削除 | `${var%%.*}` → 最後の `.` から後ろを削除 |

---

### argument

```
script.sh arg1 arg2 ...
$0 : scirpt file
$1 : arg1
$2 : arg2 ...
$@ : arg1 arg2 ...
$# : n of args
```

---

command1 | xargs command2
command | xargs

- -t
- -I{} command {}
- -n num
- -P num
- -0
- -r

```
ls | xargs -n5

ls | xargs ls

ls | xargs -I{} echo `pwd`/{}

ls | cut -d. -f1 | xargs -I{} mv {}.ext0 {}.ext1

seq 20 | xargs -n1 -P4 bash -c 'echo $0; sleep 1'
```

---

### array

```
arr=(str0 str1 str2...)
${arr[0]} : one element
${arr[@]} : all elements

${#arr[@]} : array size
${!arr[@]} : all indexes

i=0,1,2...
${arr[$i]}

${arr[@]:i:k} : slice forward
${arr[@]: -i:k} : slice back

arr+=(str) : add element
arr[i]=str : update elemtnt
unset arr[i] : delete element

arr1=("${arr0[@]}") : copy arr
```

---

### associated array

```
declare -A obj
obj[key]=value
${obj[key]}
```

### arithmetic operation

```
a=int1
((a++)) ((a--))
((a+=num)) ((a-=num)) ((a*=num)) ((a/=num)) ((a%=num))

$((a+num)) $((a-num)) $((a\*num)) $((a/num)) $((a%num))
$((a**num))

b=int2
((a+=b)) ((a-=b)) ((a*=b)) ((a/=b)) ((a%=b))

$((a+b)) $((a-b)) $((a\*b)) $((a/b)) $((a%b))

a=real1
b=real2
echo $a+$b | bc
echo $a-$b | bc
echo $a*$b | bc
result=$(echo $a*$b | bc)
echo "scale=2;$a/$b" | bc
result=$(echo "scale=2;$a/$b" | bc)

perl -e "print $a/$b"
c=$(perl -e "print $a/$b")
echo $c
```

calculation with bc -l

| 関数      | 説明                            |
| --------- | ------------------------------- |
| `s(x)`    | sin(x)（ラジアン）              |
| `c(x)`    | cos(x)（ラジアン）              |
| `a(x)`    | arctangent(x)（結果はラジアン） |
| `l(x)`    | 自然対数 ln(x)                  |
| `e(x)`    | e^x（指数関数）                 |
| `j(n, x)` | ベッセル関数 Jₙ(x)              |
| `sqrt(x)` | 平方根                          |

calculation with perl -e

| 関数         | 説明               |
| ------------ | ------------------ |
| `abs(x)`     | 絶対値             |
| `sin(x)`     | sin（ラジアン）    |
| `cos(x)`     | cos（ラジアン）    |
| `atan2(y,x)` | arctan(y/x)        |
| `exp(x)`     | e^x                |
| `log(x)`     | 自然対数（ln）     |
| `sqrt(x)`    | 平方根             |
| `int(x)`     | 小数点以下切り捨て |
| `rand(x)`    | 0〜x 未満の乱数    |
| `srand(x)`   | 乱数シード設定     |

---

### other perl functions

| 関数                         | 説明                   |
| ---------------------------- | ---------------------- |
| `chomp($x)`                  | 改行を削除             |
| `chop($x)`                   | 最後の 1 文字を削除    |
| `length($x)`                 | 文字数を返す           |
| `index($str, $substr)`       | 部分文字列の位置       |
| `substr($str, $start, $len)` | 部分文字列             |
| `lc`, `uc`                   | 小文字化・大文字化     |
| `sprintf(fmt, ...)`          | 文字列フォーマット     |
| `join($sep, @arr)`           | 配列を連結             |
| `split($sep, $str)`          | 文字列を分割           |
| `reverse($x)`                | 逆順（文字列 or 配列） |

| 関数              | 説明               |
| ----------------- | ------------------ |
| `push(@a, $x)`    | 末尾に追加         |
| `pop(@a)`         | 末尾を削除         |
| `shift(@a)`       | 先頭を削除         |
| `unshift(@a, $x)` | 先頭に追加         |
| `keys(%h)`        | ハッシュのキー一覧 |
| `values(%h)`      | ハッシュの値一覧   |
| `each(%h)`        | ハッシュを反復     |

---

## output

echo str1 str2...

- -n
- -e

escape sequence
| シーケンス | 意味 |
| ------- | ---------------- |
| `\n` | 改行（newline） |
| `\t` | タブ（tab） |
| `\\` | `\` を出力 |
| `\'` | `'` を出力 |
| `\"` | `"` を出力 |
| `\a` | 端末のベル音 またはフラッシュ |
| `\b` | 1 文字戻る 書き効果あり） |
| `\c` | 出力をここで終了 |
| `\r` | 行頭へ戻る 上書き出力などに使う |
| `\v` | 垂直タブ 縦方向のスペース |
| `\f` | 改ページ |
| `\$var` | 変数展開しない |
| `\0NNN` | 8 進数コード（ASCII） |

---

printf format str1 str2...

| format      | 意味                        | 例                        | 出力         |
| ----------- | --------------------------- | ------------------------- | ------------ |
| `%s`        | 文字列                      | `printf "%s\n" "hello"`   | hello        |
| `%c`        | 1 文字                      | `printf "%c\n" 65`        | A            |
| `%d` / `%i` | 10 進整数                   | `printf "%d\n" 42`        | 42           |
| `%o`        | 8 進整数                    | `printf "%o\n" 10`        | 12           |
| `%x`        | 16 進整数（小文字）         | `printf "%x\n" 255`       | ff           |
| `%X`        | 16 進整数（大文字）         | `printf "%X\n" 255`       | FF           |
| `%f`        | 浮動小数点                  | `printf "%.2f\n" 3.14159` | 3.14         |
| `%e`        | 指数表記（小文字）          | `printf "%e\n" 12345`     | 1.234500e+04 |
| `%E`        | 指数表記（大文字）          | `printf "%E\n" 12345`     | 1.234500E+04 |
| `%g`        | `%f` または `%e` の自動切替 | `printf "%g\n" 0.000123`  | 0.000123     |
| `%G`        | `%f` または `%E` の自動切替 | `printf "%G\n" 0.000123`  | 0.000123     |
| `%%`        | `%` リテラル                | `printf "%%\n"`           | %            |

| format    | 意味                     |
| --------- | ------------------------ |
| `%10s`    | 右寄せ、幅 10            |
| `%-10s`   | 左寄せ、幅 10            |
| `%04d`    | 整数ゼロ埋め、幅 4       |
| `%.2f`    | 浮動小数点、小数 2 桁    |
| `%10.2f`  | 幅 10、小数 2 桁、右寄せ |
| `%-10.2f` | 幅 10、小数 2 桁、左寄せ |

echo vs printf

```
for i in {1..10000}; do
  echo "$i" >> result.txt
done

for i in {1..10000}; do
  printf '%s\n' "$i"
done > result.txt
```

| 方法                        | 改行付き出力 | I/O 効率 | 安定性 |
| --------------------------- | ------------ | -------- | ------ |
| `echo "${arr[@]}"`          | 不可         | 中       | 低     |
| `printf '%s\n' "${arr[@]}"` | 可           | 高       | 高     |

---

clear

---

## control structure

### input

```
read var1 var2...
  input
    str1 str2...

read var1
read var2
...
  input
    str1
    str2
    ...

read -a arr
  input
    el0 el1 el2...

read -r var1 var2... <<< "${arr0[@]}"

read -r var1 var2... <<< "$(fn0)"
```

- -p 'message'
- -sp 'password'
- -a
- -r

---

```
mapfile/readarray arr
  input
    str1
    str2
    ...
    ctrl+d

echo ${arr[@]}

mapfile arr < file.txt

mapfile arr < <(command)
```

- -t
- -d delim
- -n line
- -s line

---

#### select

```
PS3='message'
select i in str1 str2...;do
  case $i in
    str1)
      ---;;
    str2)
      ---;;
    ...
    *)
      ---;;
  esac
done
```

```
PS3='message'
select i in opt1 opt2...;do
  case $REPLY in
    1)
      ---;;
    2)
      ---;;
    ...
    *)
      ---;;
  esac
done
```

```
opts=(str1 str2...)
PS3='message'
select i in ${opts[@]};do
  [[ $i == str ]] && break
  -- $i --
done
```

---

### conditions

```
command1 && command2
command1 && command2 || command3

[[ $a == str ]] && command
[[ $a != str ]] && command
! [[ $a == str ]] && command
[[ ! $a == str ]] && command

[[ "$a" == "str has space" ]] && command

[[ $a == glob ]] && command
[[ $a =~ regex ]] && command

[[ $a == glob / =~ regex ]] && echo $a #filter

[[ $a =~ regex ]] && echo ${BASH_REMATCH[0]} # capture all
[[ $a =~ regex ]] && echo ${BASH_REMATCH[1]} # capture first
[[ $a =~ regex ]] && echo ${BASH_REMATCH[2]} # capture second

[[ $a == str1 || $a == str2 ]] && command
[[ $a == str1 ]] || [[ $a == str2 ]] && command
[[ $a == str1 && $b == str2 ]] && command
[[ $a == str1 ]] && [[ $b == str2 ]] && command

[[ $a == str ]] && command1 || command2

[[ $a == str ]] && { command11; command12; } \
|| { command21; command22; }

[[ $a == str1 ]] && command1 \
|| { [[ $a == str2 ]] && command2 || command3; }

[[ $a > str ]], [[ $a >= str ]]
[[ $a < str ]], [[ $a <= str ]]

(( a == int ))
(( a == b )), (( a != b ))
(( a == int1 && b == int2))
(( a == int1 )) && (( b == int2))
(( a == int1 || b == int2))
(( a == int1 )) || (( b == int2))
(( a > b )), (( a >= b ))
(( a < b )), (( a <= b ))

[[ -n var ]]
[[ -z var ]]
[[ -f file ]]
[[ -d dir/ ]]
[[ -e file ]]
[[ -s file ]]
[[ -r file ]]
[[ -w file ]]
[[ -x file ]]
```

---

```
case $a in
  regex1)
    command1;;
  regex2)
    command2;;
  regex3)
    command3;;
  ...
  *)
    command0;;
esac
```

---

### loop

```
for i in 0 1 2..;do
  -- $i --
done

for i in {0..9..3};do
  -- $i --
done

for i in ${arr[@]};do
  -- $i --
done

for i in "$@";do
  -- $i --
done

for f in file1 file2...;do
 -- $f --
done

for i in $(ls);do
  -- $i --
done

for ---;do
  ---
  [[condition]] && continue
  [[condition]] && break
  [[condition]] && break 2
  [[condition]] && exit0/1
done
```

---

```
while [[condition]];do
  ---
done

while true;do
 ---
 [[condition]] && continue
 [[condition]] && break
done

while read -p 'message' a;do
  [[ $a = 0 ]] && break || \
  -- $a --
done

while read -r ln;do
  -- $line --
done < file.txt

   or (to be less I/O)

mapfile -t lines < file.txt
for ln in ${lines[@]};do
  -- $ln --
done
```

#### batch output/input process

batch output

```
input_file="input.txt"
output_file="output.txt"
> "$output_file"

batch_size=1000
batch=()
count=0

while IFS= read -r ln; do
  [[ -z "$ln" ]] && continue
  ln1= -- process to $ln --
  batch+=("$ln1")
  ((count++))

  (( count == batch_size )) && {
    printf "%s\n" "${batch[@]}" >> "$output_file"
    batch=()
    count=0
  }
done < "$input_file"

(( count > 0 )) && printf "%s\n" "${batch[@]}" >> "$output_file"
```

use file descriptor

```
input_file="input.txt"
output_file="output.txt"

batch_size=1000
batch=()
count=0

exec 3> "$output_file"

while IFS= read -r ln; do
  [[ -z "$ln" ]] && continue

  batch+=("$(command <<< "$ln")")
  ((count++))

  ((count == batch_size)) && {
    printf "%s\n" "${batch[@]}" >&3
    batch=()
    count=0
  }
done < "$input_file"

((count > 0)) && printf "%s\n" "${batch[@]}" >&3

exec 3>&-
```

watching memory usage

```
input_file="input.txt"
output_file="output.txt"

max_mem=10485760  # 10MB
batch=()
batch_bytes=0

exec 3> "$output_file"

while IFS= read -r ln; do
  [[ -z "$line" ]] && continue

  ln1= -- process to $ln --
  batch+=("$ln1")

  line_bytes=$(printf "%s\n" "$ln1" | wc -c)
  (( batch_bytes += line_bytes ))

  (( batch_bytes >= max_mem )) && {
    printf "%s\n" "${batch[@]}" >&3
    batch=()
    batch_bytes=0
  }
done < "$input_file"

(( batch_bytes > 0 )) && printf "%s\n" "${batch[@]}" >&3

exec 3>&-
```

batch input with mapfile

```
input_file="input.txt"
output_file="output.txt"

max_mem=10485760   # 10MB
chunk_lines=10000
batch=()
batch_bytes=0

exec 3> "$output_file"
exec 4< "$input_file"

while true; do
  mapfile -t -n "$chunk_lines" lines <&4
  (( ${#lines[@]} == 0 )) && break

  for ln in "${lines[@]}"; do
    [[ -z "$ln" ]] && continue

    ln1=-- process to $ln --
    batch+=("$ln1")

    line_bytes=$(printf "%s\n" "$ln1" | wc -c)
    (( batch_bytes += line_bytes ))

    (( batch_bytes >= max_mem )) && {
      printf "%s\n" "${batch[@]}" >&3
      batch=()
      batch_bytes=0
    }
  done
done

(( batch_bytes > 0 )) && printf "%s\n" "${batch[@]}" >&3

exec 3>&-
exec 4<&-
```

---

### shell function

```
fn0(){
  ---
  local var=str
  -- $var --
  return 0/not 0
}

fn0
a=$(fn0)
```

```
fn0(){
  local var=str
  -- $var, $1, $2, $3...--
  return 0/not 0
}

fn0 str1 str2 str3...
```

---

## file process

touch file1 file2...
touch glob
touch file{seq} #ex. file{00..99}.txt

---

cat file1 file2...

- -n
- -s

---

less

- -N

---

pwd

---

ls
ls glob

- -l
- -a
- -h
- -S
- -t
- -R

---

cd

- cd ~
- cd ..
- cd -

---

mkdir dir/

- -p
- -m ooo

---

cp file0 file1
cp -r dir0/ dir1/

---

mv file dir/
mv file0 file1

---

rm file
rm -r dir/

---

ln file link

- -s

---

alias abbr='command line'
unalias abbr

---

diff file1 file2

- -u
- -y

---

locate glob1 glob2...

(sudo apt install mlocate)
updatedb

- -i
- -b
- -A
- -r

---

find path glob

- -name glob
- -iname glob
- -name glob1 -o -name glob2
- -name glob1 -a -name glob2
- -type f/d/l
- -user username
- -size +100M/+1G/...

---

zip file.zip file1 file2...

- -r file.zip dir/

unzip file.zip

- -d dir
- -o

---

gzip file
gunzip file.gz

---

tar -czvf file.tar.gz dir/
tar -xzvf file.tar.gz

---

split -dl num file ./dir/part\_

- -l
- -d
- -a num
- -b num

`cat part_* > merge`

---

rsync dir0/ dir1/
rsync dir0 dir1/

- -a
- -v
- -z
- -u
- --delete
- -e ssh

regularly backup

```
crontab -e

0 1 \* \* \* rsync -az dir0/ dir1/
```

---

## text process

locale

```
$LANG

export LC_ALL=en_US.UTF-8
export LC_ALL=ja_JP.UTF-8

LC_ALL=en_US.UTF-8 command
```

- -a

| カテゴリ      | 意味                                   |
| ------------- | -------------------------------------- |
| `LC_CTYPE`    | 文字コード・文字分類（日本語処理の要） |
| `LC_COLLATE`  | 並び順（sort など）                    |
| `LC_TIME`     | 日付・時刻フォーマット                 |
| `LC_NUMERIC`  | 数値表記（小数点など）                 |
| `LC_MONETARY` | 通貨表記                               |
| `LC_MESSAGES` | メッセージ言語                         |
| `LANG`        | 全体のデフォルト                       |
| `LC_ALL`      | 最上位の上書き設定（全部を統一）       |

---

wc < file

- -l
- -w
- -c

---

head file1 file2...

- -n line

---

tail file1 file2...

- -n line
- -f

---

sort file

- -n
- -r
- -u
- -t delim (ex. ' ', $'\t' ) -k num1,num2
- -S memory size (ex. 1G)

---

column file

- -t

---

rev file (not for multi byte character)

---

tr chr1 chr2 < file.txt (not for multi byte character)

- a-z A-Z
- A-Z a-z
- '\t' ' '
- '\t' ,
- , '\t'
- chr01chr02... chr11chr2...

- tr -d 0-9
- tr -cd 0-9
- tr -s ' '
- tr -s '\t'
- tr -s ' \t'
- tr -s '\n'

delete new line at not end
`tr -d '\\n' < file.txt`

use POSIX class
`tr '[:lower:]' '[:upper:]' < file.txt`

delete except number,alphabet,new line
`tr -cd '[:alnum:]\n' < file.txt`

| POSIX クラス | 意味                                 | マッチする文字                                                   |     |
| ------------ | ------------------------------------ | ---------------------------------------------------------------- | --- |
| `[:alnum:]`  | 英数字                               | A–Z, a–z, 0–9                                                    |     |
| `[:alpha:]`  | 英字のみ                             | A–Z, a–z                                                         |     |
| `[:digit:]`  | 数字                                 | 0–9                                                              |     |
| `[:lower:]`  | 小文字                               | a–z                                                              |     |
| `[:upper:]`  | 大文字                               | A–Z                                                              |     |
| `[:space:]`  | 空白全般（スペース, タブ, 改行など） | `' '`, `\t`, `\n`, …                                             |     |
| `[:blank:]`  | 空白とタブのみ                       | `' '`, `\t`                                                      |     |
| `[:punct:]`  | 句読点や記号                         | `! " # $ % & ' ( ) * + , - . / : ; < = > ? @ [ \ ] ^ _ { \| } ~` |
| `[:graph:]`  | 印字可能文字（空白以外）             | 英数字・記号                                                     |     |
| `[:print:]`  | 印字可能文字（空白を含む）           | すべての可視文字＋スペース                                       |     |
| `[:cntrl:]`  | 制御文字                             | `\n`, `\t`, `\r`, `\0`, …                                        |     |
| `[:xdigit:]` | 16 進数字                            | 0–9, A–F, a–f                                                    |     |

---

cut file (not for multi byte character)

```
- -c num #ex. -c3
- -c"$var" #ex. -c"$a"
- -c num- #ex. -c5-
- -c -num #ex. -c-5
- -c num1-num2 #ex. -c2-6
- -c num1,num2... #ex. -c2,6
- -c 'num1-num2,num3-num4...' #ex. -c'2-4,6-8'
- --complement

- -d delim -f num #ex. -d' ' -f3
- -d"$var1" -f"$var2" #ex. -d"$a" -f"$b"
- -d delim -f 'num1-num2,num3-num4...'
```

if delim is not just a single space

```
tr -s ' ' < file | cut -d' ' -f num
tr -s '[:blank:]' < file | cut -d' ' -f num
```

---

paste file1 file2

- -d delim
- -s

join file1 file2

- -1 num
- -2 num
- -a 1
- -a 2
- -e chr
- -o

| 用途             | コマンド                   | 説明                   |
| ---------------- | -------------------------- | ---------------------- |
| 横方向に単純結合 | `paste file1 file2`        | 同じ行番号で連結       |
| 区切り変更       | `paste -d ',' file1 file2` | タブ以外で区切る       |
| キーで結合       | `join file1 file2`         | SQL の JOIN 的動作     |
| 外部結合         | `join -a 1` or `-a 2`      | 片方にしかない行も出す |

---

grep regex file1 file2...

- -n
- -c
- -i
- -v
- -w
- -h regex file1 file2...
- -e regex1 -e regex2... file
- -R regex dir/
- -o
- -E

delete empty line

```
grep -v '^$' file.txt
grep -v '^[[:space:]]*$' file.txt
```

#### glob (wildcard)

- ? : one character
- \* : some characters
- [chr1 chr2...] : any one character
- [!chr1 chr2...] : other character
- {str1 str2...} : any one string
- {0..9} : 0-9 sequence

#### regular expression (regex)

- . [abc] [^abc] : any one charcter
- \* : repeat character
- ^str : start
- str$ : end

#### extended regex

- (regex) : group
- (regex)? : 0 or 1
- (regex)\+ : repeat
- (regex){m} / {m,n} / {m,} : repeat >=m, <=n
- (regex1 | regex2 |...) : or

---

sed script file1 file2...
sed -e 'script1' -e 'script2'... file1 file2...

- -e
- -i
- -E
- -s

script

```
-n line p #ex. 3p
-n "$var"p #ex. "$a"p
-n "$var,+num p" #ex. "$a,+3p"
-n line1,line2 p' #ex. 2,4p
-n 'line,$p' #ex. '5,$p'
-n line1 p;line2 p' #ex. 2p;4p
-n line~step p #ex. 1~3p
-n /regex/p
-n '/regex/!p' # is equal /regex/d
-n line,/regex/p #ex. 3,/regex/p
-n /regex/,line p #ex. /regex/,5p
-n /regex/,+num p #ex. /regex/,+3p
-n /regex1/,/regex2/p

line d #ex. 3d
"$var"d #ex. "$a"d
line,"$var"d #ex. 5,"$a"d
"$var",line d #ex. "$a",10d
/regex/d
/regex/q

s/regex/str/
s/regex/str/g
s/regex//g
s/regex/str/num
"$var s/regex/str/"
line s/regex/str/ #ex. 5s/regex/str/
line1,line2 s/regex/str/ #ex. 2,4s/regex/str/

-n s/regex/str/p

s/--(regex)--/--\1--/
s/--(re1)--(re2)--/--\1--\2--/

'/regex/i\text'
'/regex/a\text'
'/regex/c\text'

glob=---
str=---
sed "s/$glob/$str/g" file

sed 's/　/ /g'

s/<[^>]*>//g file.html/xml #only for simple html/xml

perl -CSDA -0777 -pe 's/<.*?>//sg' file.html/xml
```

---

awk 'script' file

- -F
- -f
- -v

script

```
{print $num1,num2,...}
{print $num1 num2 ...}
{print $num1 "str1" num2 "str2"...}
$num1==str {print $num2,num3...}
!$num1==str {print $num2,num3...}
$num1==str1 && $num2==str2 {print $num3,num4...}
$num1==str1 || $num2==str2 {print $num3,num4...}
$num1+$num2==str {print $num3,num4...}

/regex/{print $num1,num2,...}
$num1 ~/regex/ {print $num2,$num3...}
$num1 !~/regex/ {print $num2,$num3...}

{print $NF}
NF<int {print $num1,num2,...}

NR==line {print $num1,num2,...}
NR==line1, NR==line2 {print $num1,num2,...}

FS="str0",OFS="str1" {print $num1,$num2...}

BEGIN{script1} END{script2} script3
#ex. BEGIN{print "start"} END{print "finish"} {print $num1,num2}

```

functions

- length($num)
- tolower($num), toupper($num)
- substr($num,index1,index2)
- index($num,str)
- split($num,arr,delim)
- sub(str0,str1,$num)
- gsub(str0,str1,$num)

- int($num)
- sqrt($num)
- exp($num)
- log($num)
- sin($num)
- cos($num)
- atan2($num1,$num2)
- rand()

---

#### make csv from text

sed -nE 's/--(re1)--(re2)--(re3)--/\1,\2,\3/p' file.txt > file.csv
ex.

- delim : space, 3 columns

```
sed -nE 's/^([^ ]+) +([^ ]+) +([^ ]+)/\1,\2,\3/p' file.txt > file.csv
```

- delim : space, tab, 3 columns

```
sed -nE 's/^([^[:space:]]+)[[:space:]]+([^[:space:]]+)[[:space:]]+([^[:space:]]+)/\1,\2,\3/p' file.txt > file.csv
```

- extract only number, 3 columns

```
sed -nE 's/._?([0-9]+)._?([0-9]+)._?([0-9]+)._/\1,\2,\3/p' file.txt > file.csv
```

- if string has " escape with ""
- if string has space, tab, new line, comma surround all with "

```
sed 's/"/""/g; s/^/"/; s/$/"/' file.txt > file.csv
```

- delim : space, some columns

```
perl -pe 's/\s+/,/g' file.txt > file.csv

awk '{$1=$1; gsub(/ +/, ","); print}' file.txt > file.csv

sed -E ':a; s/^([^ ]+) +([^ ]+)/\1,\2/; ta' file.txt > file.csv
```

---

## system monitor

| ファイル                 | 主な内容                                            | 例・用途                                          |
| ------------------------ | --------------------------------------------------- | ------------------------------------------------- |
| /var/log/syslog          | システム全般のログ（サービス・カーネル・cron など） | Ubuntu 系で最重要。トラブル調査・起動ログ確認など |
| /var/log/auth.log        | 認証・ログイン関連の記録                            | `sudo` 実行履歴、不正ログイン調査など             |
| /var/log/boot.log        | 起動プロセスの詳細ログ                              | サービスの起動順や失敗の特定                      |
| /var/log/cron.log        | cron ジョブ実行履歴                                 | 定期タスクが正常に実行されたか確認                |
| /var/log/apt/history.log | apt コマンドによるパッケージ管理履歴                | いつどのパッケージを更新/削除したか               |
| /var/log/faillog         | ログイン失敗履歴                                    | セキュリティ監査用 (`faillog -a` で確認)          |
| /var/log/wtmp            | ログイン・ログアウト履歴                            | `last` コマンドで閲覧                             |
| /var/log/btmp            | 失敗したログイン試行                                | `lastb` コマンドで閲覧                            |

---

df

- -h

---

du

- -h
- -d num
- -sh \* | sort -h | tail -n 10
- -ah \* | sort -h | tail -n 10

---

lscpu

- -e

---

lsblk

- -f

---

free

- -h
- -t

---

hostname

- -I

---

whoami

---

who

---

ps

- -f
- -e
- --forest

---

kill PID
pkill process-name

- -9
- -STOP
- -CONT
- -HUP

---

jobs

- -l

---

sleep 1
sleep 0.1
sleep 1d 1h 1m 1s

---

wait PID

---

| Action                             | Command                          |
| ---------------------------------- | -------------------------------- |
| Start job in background            | `command &`                      |
| List background jobs               | `jobs`                           |
| Resume stopped job in background   | `bg %job_number`                 |
| Bring background job to foreground | `fg %job_number`                 |
| Get last backgroud job PID         | `pid=$!`                         |
| Wait for a certain jobs to finish  | `wait PID`                       |
| Wait for jobs to finish            | `wait`                           |
| Kill background job                | `kill %job_number` or `kill PID` |

---

lsof

- file
- +D dir/
- -u user
- -i :port
- -i

---

time script.sh
time bash -c '--script--'
time { --script--; }

---

watch -n sec command

---

date

- -I
- -R
- -u
- +%F, +%D, +%T
- +%y, +%m, +%d, +%H, +%M, +%S

`date '+%y/%m/%d'`

---

top, htop

---

## network

ping

- -c
- -i
- -W

run if connection is available
(ping -c 1 -W 1 url > /dev/null 2>&1 && command1) || command2

---

wget url

- -q
- -b
- -O ./path/file
- -P ./dir
- -r url/dir/

---

curl url

- -O
- -d 'data'
- -u user:password

---

ftp

prepare FTP server

```
sudo apt install vsftpd
sudo nano /etc/vsftpd.conf
```

| 設定                    | 説明                               | 推奨値 |
| ----------------------- | ---------------------------------- | ------ |
| `listen=YES`            | デーモンモードで起動               | YES    |
| `anonymous_enable=NO`   | 匿名ログイン禁止                   | NO     |
| `local_enable=YES`      | ローカルユーザーのログインを許可   | YES    |
| `write_enable=YES`      | ファイルの書き込み許可             | YES    |
| `chroot_local_user=YES` | ユーザーをホームディレクトリに制限 | YES    |

```
sudo adduser ftpuser

sudo systemctl restart vsftpd
sudo systemctl enable vsftpd
```

access to FTP server

```
ftp xxx.xxx.xxx.xxx

ftp> ls
ftp> cd dir
ftp> get file
ftp> put file
ftp> bye
```

- -i
- -n
- -v

prepare SFTP server

```
sudo apt install vsftpd
sudo nano /etc/vsftpd.conf
```

listen=YES
listen_ipv6=NO
anonymous_enable=NO
local_enable=YES
write_enable=YES
chroot_local_user=YES

ssl_enable=YES
allow_anon_ssl=NO
force_local_data_ssl=YES
force_local_logins_ssl=YES
rsa_cert_file=/etc/ssl/certs/vsftpd.pem
rsa_private_key_file=/etc/ssl/private/vsftpd.key
ssl_ciphers=HIGH

```
sudo mkdir -p /etc/ssl/private
sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
 -keyout /etc/ssl/private/vsftpd.key \
 -out /etc/ssl/certs/vsftpd.pem

sudo adduser ftpuser

sudo systemctl restart vsftpd
sudo systemctl enable vsftpd
```

access to SFTP server

```
lftp -u ftpuser,password -e "set ftp:ssl-force true; set ssl:verify-certificate no" ftps://192.168.1.10
```

---

ssh user@hostname / IP

- -p port

```
ssh-keygen -t rsa -b 2048
ssh-copy-id user0@xxx.xxx.xxx.xxx

ssh user0@xxx.xxx.xxx.xxx
```

---

scp file user@hostname/IP:path/dir/
scp -r dir user@hostname/IP:path/dir/
scp user@hostname/IP:path/file ./

- -P

---

## binary file

hexdump file

- -C

---

base64 file.bin > file.b64
base64 -d file.b64 > file.bin

---

xxd file.bin

xxd -p file.bin > file.hex
xxd -pr file.hex > file.bin

```
hex=$(xxd -p file0.bin | tr -d '\n')
echo "$hex"

echo -n "$hex" | xxd -pr > file1.bin
```

---

## audio

aplay file.wav

---

mpg123 file.mp3

---

ffmpeg

ffmpeg -i file.wav file.mp3

---

espeak-ng -v ja 'text' --stdout > file.wav

---

open-jtalk

---

## tmux multiplexer

|          |                |             |                |
| -------- | -------------- | ----------- | -------------- |
| ctrl+`b` | プレフィックス |             |                |
|          | **基本**       |             | **session**    |
| `?`      | キー一覧       | `s`         | 一覧選択       |
| `:`      | コマンド       | `d`         | デタッチ       |
|          |                | `&`         | 名前変更       |
|          |                |             |                |
|          | **window**     |             | **pane**       |
| `c`      | 新規作成       | `%`         | 左右分割       |
| `w`      | 選択           | `"`         | 上下分割       |
| `0`-`9`  | 指定番号へ移動 | `q`         | 番号表示       |
| `&`      | 破棄           | `→`         | 方向へ移動     |
| `n`      | 次へ           | ctrl+`→`    | サイズ変更     |
| `p`      | 前へ           | `!`         | ウィンドウ化   |
| `l`      | 以前のへ       | `x`         | 破棄           |
| `'`      | 入力番号へ     | `o`         | 順に移動       |
| `.`      | 番号変更       | `;`         | 以前のへ移動   |
| `,`      | 名前変更       | `z`         | 最大化         |
| `f`      | 検索           | space       | レイアウト変更 |
|          | **コピー**     | alt-`1`-`5` | レイアウト変更 |
| `[`      | モード開始     | `{`         | 前方向に入替   |
| space    | 開始位置決定   | `}`         | 後方向に入替   |
| enter    | 終了位置決定   | ctrl+`o`    | 全体入れ替え   |
| `]`      | 貼り付け       | `t`         | 時計表示       |
|          |                |             |                |
|          | **plugin**     |             | **resurrect**  |
| `I`      | インストール   | ctrl+`s`    | tmux 設定保存  |
| `U`      | アップデート   | ctrl+`r`    | tmux 設定復活  |

|                             |                           |
| --------------------------- | ------------------------- |
| **tmux コマンド**           |                           |
| `tmux`                      | 新規 session 開始         |
| `tmux new -s 名前`          | 名前を付けて session 開始 |
| `tmux ls`                   | session 一覧              |
| `tmux lsc`                  | 接続クライアント一覧      |
| `tmux a`                    | session 再開              |
| `tmux kill-session`         | セッションを終了          |
| `tmux kill-session -t 名前` | セッションを指定して終了  |
| `tmux kill-server`          | tmux 全体を終了           |
| `tmux source ~/.tmux.conf`  | .tmux.conf の再読込       |
| `tmux -V`                   | バージョン確認            |
