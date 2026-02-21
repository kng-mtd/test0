git

sudo apt install git-all

git --version

#make working directory at local/remote

mkdir work
cd work

#make stage, repository on working directory

git init
ls -a

> .git file is database for git
> 'worktree', 'stage', 'repository' on working directory

#make and modify file on working directory 'worktree'

nano readme.txt

> write and save contents
> git status

#add file to stage

git add readme.txt
git add .

> add all modified files

git status

#commit file from stage to repository with a message

git config --global core.editor 'nano'
or
export EDITOR=/usr/bin/nano

git commit

> write message at 1st line
> write about change as message
> or
> git commit -m 'message'

git status

#see log
git log

#see just commit message in log
git log --oneline

#see last log
git log -1

#modify file, add new file on worktree

nano readme.txt
git status

nano readme2.txt
git status

#add all files to stage

git add .
git status

#commit modified file from woretree,
new file from stage to repository with a message

git commit -a
or
git commit -a -m 'massage'
git status
git log

> see change history

#see difference between last commit file and stage file

nano readme.txt
git add
git commit
nano readme.txt

> modify file
> git add .
> git status
> git diff --staged

#see difference between last commit file and worktree file

nano readme.txt
git add
git commit
nano readme.txt

> modify file
> git status
> git diff

#see diffrence between commits

git log --oneline
git diff commitA commitB
git difftool commitA commitB

git diff HEAD~1 HEAD
git difftool HEAD~1 HEAD

#revert stage file with last commit file

git restore -staged readme.txt
git status

#revert worktree file with last commit file

git restore readme.txt
git status

#branch for bugfix, development of main branch
branch is label, its add by last commit

#see exist branch at now

git branch

> myself is in HEAD branch at now

#add sub branch, and switch branch, like using other worktree,
#and modify file and commit

git branch dev1
git branch
git switch dev1
git branch
or
git branch -c dev1
git branch

#modify file in sub branch worktree
git commit -a -m 'message'

#move to main branch

git switch main
git branch

#copy branch to main branch and delete branch

git merge dev1
git log
git branch -d dev1

#merge occur confilct if it modify file and commit in main branch worktree after making sub branch

#see conflict in merging and solve it

git status

> see conflict file (unmerged paths)
> git checkput main
> see conflict file, find
> <<<<<HEAD contents
> =====
> sub branch contents>>>>>
> correct code and delete <<,==,>>
> git add readme.txt
> git commit
> git log

#multi user share direcory of host or localhost as remote repository

> on host (path: (host or localhost)/tmp)
> mkdir rmt_work
> cd rmt_work
> git init

#integrate remote repositry to local repository,

mkdir work1
cd work1
git clone /tmp/rmt_work.git/
ls
cd rmt_work
ls -a
git status
git log
git remote -v

#after cloning get other users commit to remote repository

git pull /tmp/rmt_work.git/
git log

#modify worktree file, and commit to local repository

> modify worktree file
> git commit -a -m 'message'

#copy local repository to remote repository (origin)
git push origin main

#see branch local and remote
git branch -a

#merge remote branch, remote name 'origin'
git merge origin/main

#use git-hub

register user name and email on git-hub web site

#initialize user for using git-hub
git config --global user.name 'km'
git config --global user.email muchagorou112@gmail.com
git config --list

on git-hub web site, make repository with the same name as local repository

#add remote repository to local
git add origin git-hub repository URL(https://---.git)

#pull repository files to local repository and worktree
git pull origin main

> update local repository as remote repository (sharing contents with members)

#pull repository files to l
ocal just repository
git fetch origin

#make sub branch for my working
git switch -c dev1

modify files

#add and commit to sub branch
git add .
git commit -m 'message'

#push sub branch files to remote repository
git push origin dev1

on git-hub web site

do pull reqouest, compare main and sub branch
make request, write title and comment about change
choose reviewer

after review

merge to main and delete sub branch
