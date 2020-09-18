# 说明
以后代码全部在这里存放，使用 git 管理。写好一个版本后执行以下步骤：
```
git add . # 添加所有文件
git commit -m "commit message"
git push # 上传至服务器
```
前端后端 均clone此包至本地，前端只管编辑 frontend，后端只管编辑 backend，不要碰不是自己管理的东西。
每次 commit 时写清本次 commit 加了哪些东西。
相关的文档、需求也将在 coding.net更新

***

注意 git commit 前确保无关的文件不要添加进来，可以在.gitignore里写清楚不添加哪些东西，也可以在 git add 阶段手动添加需要 commit 的文件。

***
使用 
```
git clone https://e.coding.net/fakenews/fakenews.git 
```
clone仓库 至本地


***

各自注册 coding.net,我会邀请你们成为团队成员。

*** 
* code:0 有数据且请求成功
* code:1 请求成功但无数据
* code:2 请求失败,参数有误