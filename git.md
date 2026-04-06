# Git 基本メモ（整理版）

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

## マージ

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
git config --global user.name 'km'
git config --global user.email 'your@email.com'
git config --list
```

---

### リモート追加

```bash
git remote add origin https://xxx.git
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

---

「**Hugo → GitHub Pages 自動デプロイ**」を最短構成でまとめます。
（pushするだけでサイト更新される状態まで）

---

# 全体像（これだけ理解すればOK）

```text
Hugoで生成 → GitHubにpush → 自動ビルド → 公開
```

---

# ① Hugoサイト作成

```bash
hugo new site mysite
cd mysite
```

---

# ② テーマ追加（例：PaperMod）

```bash
git init
git submodule add https://github.com/adityatelange/hugo-PaperMod.git themes/PaperMod
```

`hugo.toml` を編集：

```toml
baseURL = 'https://ユーザー名.github.io/mysite/'
languageCode = 'en-us'
title = 'My Site'
theme = 'PaperMod'
```

---

# ③ 記事作成

```bash
hugo new posts/first.md
```

編集：

```bash
nano content/posts/first.md
```

```md
+++
title = 'First Post'
date = 2026-01-01
+++

Hello Hugo
```

---

# ④ ローカル確認

```bash
hugo server
```

👉 [http://localhost:1313](http://localhost:1313) で確認

---

# ⑤ GitHubリポジトリ作成

GitHub で：

- リポジトリ名：`mysite`
- Public
- READMEなし

---

# ⑥ Git初期化＆push

```bash
git add .
git commit -m 'init'
git branch -M main
git remote add origin https://github.com/ユーザー名/mysite.git
git push -u origin main
```

---

# ⑦ 自動デプロイ設定（これが重要）

`.github/workflows/hugo.yml` を作る：

```bash
mkdir -p .github/workflows
nano .github/workflows/hugo.yml
```

中身：

```yaml
name: Deploy Hugo site

on:
  push:
    branches:
      - main

jobs:
  build-deploy:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout
        uses: actions/checkout@v4
        with:
          submodules: true

      - name: Setup Hugo
        uses: peaceiris/actions-hugo@v3
        with:
          hugo-version: 'latest'

      - name: Build
        run: hugo --minify

      - name: Deploy
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./public
```

---

# ⑧ push（これで自動化スタート）

```bash
git add .
git commit -m 'add workflow'
git push
```

---

# ⑨ GitHub Pages設定

GitHubの：

- Settings → Pages
- Source：
  - **Deploy from a branch**
  - Branch：`gh-pages`

---

# ⑩ 公開URL

```text
https://ユーザー名.github.io/mysite/
```

---

# 更新方法（今後はこれだけ）

```bash
hugo new posts/xxx.md
# 編集
git add .
git commit -m 'post'
git push
```

👉 自動でビルド＆公開

---

# よくあるハマり

### submodule忘れ

```bash
git submodule update --init --recursive
```

---

### baseURLミス

```toml
baseURL = 'https://ユーザー名.github.io/mysite/'
```

---

### gh-pages未設定

→ 表示されない

---

「**Hugo → Cloudflare Pages（自動デプロイ）**」を最短でいきます。
（GitHub連携して push だけで公開される構成）

---

# 全体像

```text
Hugo → GitHub → Cloudflare Pages → 自動公開
```

👉 GitHub Pagesより速くて設定もシンプル

---

# ① Hugoサイト作成（済んでいればOK）

```bash
hugo new site mysite
cd mysite
git init
```

テーマ（例）：

```bash
git submodule add https://github.com/adityatelange/hugo-PaperMod.git themes/PaperMod
```

`hugo.toml`：

```toml
baseURL = '/'
title = 'My Site'
theme = 'PaperMod'
```

👉 Cloudflareでは `baseURL='/'` がポイント

---

# ② GitHubにpush

GitHub にリポジトリ作成して：

```bash
git add .
git commit -m 'init'
git branch -M main
git remote add origin https://github.com/ユーザー名/mysite.git
git push -u origin main
```

---

# ③ Cloudflare Pages設定

Cloudflare にログイン

1. 「Pages」へ
2. 「Create a project」
3. 「Connect to Git」

👉 GitHubと連携してリポジトリ選択

---

# ④ ビルド設定（重要）

設定はこれだけ：

```text
Framework preset: Hugo
Build command: hugo
Build output directory: public
```

---

# ⑤ デプロイ

「Save and Deploy」

👉 数十秒で公開される

---

# ⑥ 公開URL

```text
https://xxxx.pages.dev
```

---

# 更新方法（今後）

```bash
git add .
git commit -m 'update'
git push
```

👉 自動デプロイされる

---

# カスタムドメイン（任意）

Cloudflare Pagesで：

- 「Custom domains」
- ドメイン追加

👉 DNSも自動設定される（Cloudflare使ってれば特に楽）

---

# よくあるハマり

### baseURLミス

```toml
baseURL = '/'
```

---

### テーマ読み込めない

```bash
git submodule update --init --recursive
```

---

### ビルド失敗

→ Hugo version指定（必要な場合）

```text
Environment variable:
HUGO_VERSION = 0.1xx.x
```

---

# GitHub Pagesとの違い（重要）

| 項目       | Cloudflare Pages | GitHub Pages |
| ---------- | ---------------- | ------------ |
| 速度       | 速い             | 普通         |
| 設定       | 簡単             | やや面倒     |
| 自動ビルド | 標準             | Actions必要  |
| CDN        | 強い             | 普通         |

---
