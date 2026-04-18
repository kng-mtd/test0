# Hugo

## github repository
```
repo: hugo0
URL: https://kng-mtd.github.io/hugo0/
```

## setup hugo
```bash
sudo apt install snapd
sudo snap install hugo
hash -r
hugo version
tldr hugo
```

## make site
```bash
hugo new site hugo0
cd hugo0
git init
```

## hugo themes
`https://github.com/search?q=hugo+theme&type=repositories&s=stars&o=desc`

```bash
git submodule add URL themes/theme0
echo "theme = 'theme0'" >> hugo.toml

ex.
git submodule add https://github.com/adityatelange/hugo-PaperMod.git themes/PaperMod
echo "theme = 'PaperMod'" >> hugo.toml
```

## site setting

hugo.toml
```toml
baseURL = 'https://kng-mtd.github.io/hugo0/'
languageCode = 'en-us'
title = 'My Hugo Site'
theme = 'PaperMod'
```

## make page
```bash
hugo new content posts/post0.md
nano content/posts/post0.md
```
```md
---
title: "Post0"
date: 2026-01-01
draft: true
---

Hello Hugo
```

## test execution

```bash
hugo server -D
```
ctrl+c

http://localhost:1313/hugo0/


### with online ubuntu ex. Killercoda
```bash
wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb
sudo apt install ./cloudflared-linux-amd64.deb

cloudflared tunnel --url http://localhost:1313 --loglevel info
```
```
2026-04-18T07:41:28Z INF |  Your quick Tunnel has been created! Visit it at (it may take some time to be reachable):  |
2026-04-18T07:41:28Z INF |  https://man-parents-scientist-marie.trycloudflare.com                                     |
```

https://xxx-xxx-xxx-xxx.trycloudflare.com


## make directory "public/" for web page files 

```bash
hugo
cd public
git add .
git commit -m 'deploy web page files'
git branch -M main
git remote add origin https://github.com/kng-mtd/hugo0.git
git config --global user.email 'muchagorou112@gmail.com'
git config --global user.name 'kng-mtd'
git push -u origin main
```

## setting, github pages
```
Source: Deploy from a branch
Branch: main
Folder: / (root)
```

https://kng-mtd.github.io/hugo0/





## with github actions, automatic publication

```
hugo0/
├── content/
├── themes/
├── hugo.toml
├── .gitignore
└── .github/workflows/deploy.yml
```

nano .gitignore
```
public/
resources/_gen/
.hugo_build.lock
.DS_Store
.vscode/
.idea/
node_modules/
*.log
```

```
mkdir -p .github/workflows
nano .github/workflows/deploy.yml
```
```yaml
name: Deploy Hugo site to GitHub Pages

on:
  push:
    branches:
      - main

permissions:
  contents: read
  pages: write
  id-token: write

jobs:
  build:
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

      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: ./public

  deploy:
    runs-on: ubuntu-latest
    needs: build

    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}

    steps:
      - name: Deploy to Pages
        id: deployment
        uses: actions/deploy-pages@v4
```


### setting, github pages
```
Source: Deploy from a branch
Branch: main
Folder: / (root)
```
```bash
git add .
git config --global user.email "you@example.com"
git config --global user.name "Your Name"
git commit -m 'setup github actions'
git push origin main
```

https://kng-mtd.github.io/hugo0/

```
hugo new posts/post1.md
nano content/posts/post1.md
```
```md
---
title: "Post1"
date: 2026-04-17
draft: false
---

Hello Hugo
```

```bash
git add content/posts/post1.md
#git add .
git commit -m 'add post1'
git push
```

### PAT auth

```
user navigation
> Setting > Developer settings > Personal access tokens
> Tokens (classic) > Generate new token

ghp_xxxxxxxxxxxxx
```

```bash
git remote add origin https://github.com/kng-mtd/hugo0.git
git config --global credential.helper store
git push -u origin main

Username: kng-mtd
Password: ghp_xxxxxxxxxxxxx
```



