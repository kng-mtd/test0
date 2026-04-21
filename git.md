# Gitメモ

## インストールと確認

```bash
sudo apt install git-all
git --version
```

## リポジトリの作成

```bash
mkdir work
cd work
git init
ls -a
```

- `.git` ディレクトリがGitのデータベース
- 構成：
  - worktree（作業ディレクトリ）
  - stage（インデックス）
  - repository（履歴）


## ファイル作成・状態確認

```bash
nano readme.txt
git status
```


## ステージング

```bash
git add readme.txt
git add .
```


## コミット

```bash
git config --global core.editor 'nano'
# または
export EDITOR=/usr/bin/nano

git commit
# または
git commit -m 'message'
```


## ログ確認

```bash
git log
git log --oneline
git log -1
```


## ファイル変更と追加

```bash
nano readme.txt
nano readme2.txt
git status

git add .
git status
```


## コミット（変更＋追加）

```bash
git commit -a
git commit -a -m 'message'
```


## 差分確認

### ステージ vs 最終コミット

```bash
git diff --staged
```

### 作業ディレクトリ vs 最終コミット

```bash
git diff
```

### コミット同士

```bash
git diff commitA commitB
git difftool commitA commitB

git diff HEAD~1 HEAD
git difftool HEAD~1 HEAD
```


## 変更の取り消し

### ステージを戻す

```bash
git restore --staged readme.txt
```

### 作業ディレクトリを戻す

```bash
git restore readme.txt
```


## ブランチ操作

### 確認

```bash
git branch
```

### 作成・切替

```bash
git branch dev1
git switch dev1

# 同時に作成＋切替
git switch -c dev1
```

## マージ、ブランチ削除

```bash
git switch main
git merge dev1
git branch -d dev1
```


## コンフリクト対応

```bash
git status
```

コンフリクト内容：

```
<<<<<<< HEAD
mainの内容
=======
devの内容
>>>>>>> dev
```

対応：

- 手動で修正
- マーカー削除

```bash
git add readme.txt
git commit
```

---

## 同一サーバ内、リモート（共有リポジトリ）利用

### リモート作成（ローカル擬似サーバ）

```bash
mkdir /tmp/rmt_work.git
cd /tmp/rmt_work.git
git init --bare
```


### クローン

```bash
git clone /tmp/rmt_work.git work1
cd work1
```


### コミット

```bash
touch README.md
git add .
git commit -m 'init'
```

### プッシュ、プル

```bash
git push origin main
#or
git push -u origin main #first
git push #since then
git pull
```


### ブランチ確認

```bash
git branch -a
```


### リモートマージ

```bash
git merge origin/main
```

---


## GitHub 利用

### ローカルから開発開始、GitHubをリモートとして追加

```bash
git remote -v
```
> enpty
```
git remote add origin git@github.com:kng-mtd/repo0.git
```
> https exists
```
git remote set-url origin git@github.com:kng-mtd/repo0.git
```
```
git remote -v
```

### git push設定

```bash
git config --global user.name 'kng-mtd'
git config --global user.email 'xxx@gmail.com'
git config --list
```

### GitHubレポジトリから開発開始

### PAT認証
```bash
git clone https://github.com/kng-mtd/repo0.git
```

github

https://github.com/settings

1 Developer settings
2 Personal access tokens
3 Tokens (classic)
4 Generate new token (classic)
5 Note
6 Expiration (recommend 30days or 90days)
7 Scopes
8 Generate token
```
ghp_xxxxxxxxxxxxx
```

```bash
git push

Username: kng-mtd
Password: ghp_xxxxxxxxxxxxx
```

PAT入力省略
```bash
git config --global credential.helper store
```



### SSH認証

```bash
ssh-keygen -t ed25519 -C 'xxx@gmail.com'
cat ~/.ssh/id_ed25519
cat ~/.ssh/id_ed25519.pub
```

github

https://github.com/settings/keys

1 personal account
2 SSH and GPG keys
3 New SSH key
4 (paste ssh-public key)
5 add key

```bash
ssh -T git@github.com
```

```bash
git clone git@github.com:kng-mtd/hugo0.git
```

### ローカル更新

```bash
git pull origin main
git pull origin main --rebase #GitHub上コミットをローカルに反映

git fetch origin
```

---

## ブランチ作業

```bash
git switch -c dev1
git add .
git commit -m 'message'

git push origin dev1
#or
git push -u origin dev1 #first
git push #since then
```

---

## Pull Request（GitHub上）

1. ブランチをpush
2. GitHubでPR作成
3. レビュー依頼
4. マージ
5. ブランチ削除
