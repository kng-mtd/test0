# bash script cheatsheet

## notes

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

- bash internal commands
  compgen -b
  compgen -b | sort -u
  help

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

- common library (.so)
  sudo find /lib /usr/lib -type f -name '_.so_' 2>/dev/null | sort | less

---

- apt managed librarys (lib---)
  apt list --installed | grep '^lib'

---

| ライブラリ                       | 用途                                        |
| -------------------------------- | ------------------------------------------- |
| `libc.so.6`                      | 標準 C ライブラリ（ほぼ全てのアプリが使用） |
| `libm.so.6`                      | 数学関数ライブラリ                          |
| `libpthread.so.0`                | スレッド（POSIX Threads）                   |
| `libdl.so.2`                     | 動的リンク機能                              |
| `libssl.so.3` / `libcrypto.so.3` | OpenSSL 関連                                |
| `libsqlite3.so.0`                | SQLite データベース                         |
| `libz.so.1`                      | zlib 圧縮ライブラリ                         |
| `libcurl.so.4`                   | HTTP 通信                                   |
| `libstdc++.so.6`                 | C++標準ライブラリ                           |
| `libpython3.x.so`                | Python 埋め込みランタイム                   |

---

## script rules

### run script

script.sh

```
#!/bin/bash
( bash script )
```

bash script.sh

chmod +x script.sh
./script.sh

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

```
grep CRON /var/log/syslog
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

| 構文              | 意味                   | 例                                       |
| :---------------- | :--------------------- | :--------------------------------------- |
| `${var#pattern}`  | 前方の最短マッチを削除 | `${var#*/}` → 最初の `/` まで削除        |
| `${var##pattern}` | 前方の最長マッチを削除 | `${var##*/}` → 最後の `/` まで削除       |
| `${var%pattern}`  | 後方の最短マッチを削除 | `${var%.*}` → 最初の `.` から後ろを削除  |
| `${var%%pattern}` | 後方の最長マッチを削除 | `${var%%.*}` → 最後の `.` から後ろを削除 |

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

command1 | xargs command2

- -n num
- I{}
- P num
- -0
- -r

---

### array

```
arr=(str0 str1 str2...)
${arr[0]} : one element
${arr[@]} : all elements

${#arr[@]}} : array size
${!arr[@]}} : all indexes

i=0,1,2...
${a[$i]}

${arr[@]:i:k} : slice forward
${arr[@]: -i:k} : slice back

arr+=(str) : add element
arr[i]=str : update elemtnt
unset arr[0] : delete element

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
$((a+num)) $((a-num)) $((a\*num)) $((a/num)) $((a%num))
$((a**num))
$((a++)) $((a--))
$((a+=num)) $((a-=num)) $((a*=num)) $((a/=num)) $((a%=num))

b=int2
$((a+b)) $((a-b)) $((a\*b)) $((a/b)) $((a%b))
$((a+=b)) $((a-=b)) $((a*=b)) $((a/=b)) $((a%=b))

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

## file process

echo str1 str2...

- -n
- -e \n \t \\$ \\" \\'

---

clear

---

touch file1 file2...

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

- -l
- -a
- -h
- -S
- -t
- -R

glob (wildcard for filename)

- ? : one character
- \* : some characters
- [chr1 chr2...] : any one character
- {str1 str2...} : any one string
- {0..9} : 0-9 sequence

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

locate pattern1 pattern2...

(sudo apt install mlocate)
updatedb

- -i
- -b
- -A
- -r

---

find path pattern(string+glob)

- -name pattern
- -iname pattern
- -name pattern1 -o -name pattern2
- -name pattern1 -a -name pattern2
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

wc

- -l
- -w

---

head file1 file2...

- -n num

---

tail file1 file2...

- -n num
- -f

---

sort file

- -n
- -r
- -u
- -t delim (ex. ' ', $'\t' ) -k num1,num2

---

cut file

- -c num
- -c num-
- -c -num
- -c num1-num2
- -d delim -f num
- -d delim -f num1-num2

---

tr chr1 chr2 < file.txt

- a-z A-Z
- A-Z a-z
- $'\t' ' '
- $'\t' ,
- , $'\t'

- tr -d 0-9
- tr -cd 0-9
- tr -s ' '
- tr -s '\t'
- tr -s '\n'

delete new line at not end

```

tr -d '\\n' < test.sh

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

column file

- -t

---

grep regexp file

- -n
- -i
- -v
- -o
- -E

delete empty line

```

grep -v '^$' file.txt
grep -v '^[[:space:]]*$' file.txt

```

#### regular expression

- . [abc] [^abc] : one charcter
- \* : repeat character
- ^str : start
- str$ : end

#### extended regexp

- (regexp) : group
- (regexp)? : 0 or 1
- (regexp)\+ : repeat
- (regexp){m} / {m,n} / {m,} : repeat >=m, <=n
- (regexp1 | regexp2 |...) : or

---

sed 'script' file

- 'line d'
- 'line1,line2 d'
- 'line,$ d'
- '/regexp/d'
- -n '/regexp/p'
- 's/regexp/str/', 's/regexp/str/g'
- 's/--(regexp)--/--\1--/'
- 's/--(re1)--(re2)--/--\1--\2--/'
- -i
- -E

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

---

watch -n sec command

---

date

- -I
- -R
- -u
- +%F, +%D
- +%y, +%m, +%d, +%H, +%M, +%S

```

date '+%y/%m/%d'

```

---

top
htop

---

## network

hostname

- -I

---

whoami

---

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

## control structure

### read var/array

- -p 'message'
- -sp 'password'
- -a
- -r

read -r var1 var2... <<< "${arr0[@]}"

read -r var1 var2... <<< "$(fn0)"

---

### conditions

```
[ $a = str ] && comand
[ $a != str ] && comand
! [ $a = str ] && comand
[ ! $a = str ] && comand

[ $a = str1 -o $a = str2 ] && command
[ $a = str1 ] || [ $a = str2 ] && command
[ $a = str1 -a $b = str2 ] && command
[ $a = str1 ] && [ $b = str2 ] && command

[ $a = str ] && comand1 || commnad2

[ $a = str1 ] && command1 || \
{
[ $a = str2 ] && command2 || \
command3
}

[ $a -eq int ]
[ $a -eq $b ], [ $a -ne $b ]
[ $a -gt $b ], [ $a -ge $b ]
[ $a -lt $b ], [ $a -le $b ]

[ -n var ]
[ -z var ]
[ -e file ]
[ -f file ]
[ -d dir/ ]
```

---

### case

```
case $a in
  regexp1)
    command1;;
  regexp2)
    command2;;
  regexp3)
    command3;;
  ...
  *)
    command0;;
esac
```

---

### for

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
  [condition] && continue
  [condition] && break
  [condition] && break 2
  [condition] && exit0/1
done
```

---

### while

```
while [condition];do
  ---
done

while true;do
 ---
 [condition] && break
done

while read -p 'message' a;do
  [ $a = 0 ] && break || \
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

batch input from file

```
batch=1000
exec 3< file.txt

while true; do
    mapfile -t -n "$batch" lines <&3
    (( ${#lines[@]} == 0 )) && break

    for ln in "${lines[@]}"; do
      -- $ln --
    done
    unset lines
done
exec 3<&-
```

---

### select

```
select i in opt1 opt2...;do
  case $i in
    opt1)
      ---;;
    opt2)
      ---;;
    ...
    *)
      ---;;
  esac
done

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

---

### shell function

```
fn0(){
  ---
  echo str
  return 0/not 0
}

fn0
a=$(fn0)
```

```
fn0(){
  -- $1, $2, $3...--
  return 0/not 0
}

fn0 str1 str2 str3...
```

---
