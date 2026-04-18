# Gitメモ

## インストールと確認

```bash
sudo apt install git-all
git --version
```

---

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

---

## ファイル作成・状態確認

```bash
nano readme.txt
git status
```

---

## ステージング

```bash
git add readme.txt
git add .
```

---

## コミット

```bash
git config --global core.editor 'nano'
# または
export EDITOR=/usr/bin/nano

git commit
# または
git commit -m 'message'
```

---

## ログ確認

```bash
git log
git log --oneline
git log -1
```

---

## ファイル変更と追加

```bash
nano readme.txt
nano readme2.txt
git status

git add .
git status
```

---

## コミット（変更＋追加）

```bash
git commit -a
git commit -a -m 'message'
```

---

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

---

## 変更の取り消し

### ステージを戻す

```bash
git restore --staged readme.txt
```

### 作業ディレクトリを戻す

```bash
git restore readme.txt
```

---

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

---

## マージ、ブランチ削除

```bash
git switch main
git merge dev1
git branch -d dev1
```

---

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

## ローカルリモート（共有リポジトリ）

### リモート作成（ホスト側）

```bash
mkdir /tmp/rmt_work
cd /tmp/rmt_work
git init --bare
```

---

### クローン

```bash
mkdir work1
cd work1
git clone /tmp/rmt_work.git
```

---

### 取得

```bash
git pull /tmp/rmt_work.git
```

---

### プッシュ

```bash
git push origin main
```

---

### ブランチ確認

```bash
git branch -a
```

---

### リモートマージ

```bash
git merge origin/main
```

---

## GitHub 利用

### 初期設定

```bash
git config --global user.name 'kng-mtd'
git config --global user.email 'muchagorou112@gmail.com'
git config --list
```

---

### リモート追加

```bash
git remote add origin https://github.com/km/repo0.git

git remote -v
```

---

### 取得

```bash
git pull origin main
git fetch origin
```

---

### ブランチ作業

```bash
git switch -c dev1
git add .
git commit -m 'message'
git push origin dev1
```

---

## Pull Request（GitHub上）

1. ブランチをpush
2. GitHubでPR作成
3. レビュー依頼
4. マージ
5. ブランチ削除
