# 日更文献订阅：搭建Arxiv论文日推流水线

**本节内容适用人群：科研工作者，想要了解Arxiv日更文章，跟紧学科最新进展的人群；**

### 达成的效果

根据本节内容，你能达成如下效果：

```json
把所感兴趣的日更Arxiv文章以及相关总结（由chatgpt生成），以issue的形式更新在你的github个人仓库中，仅需浏览每日issue，即可了解每日科研进展，无需人工检索，无需本地化部署。
```

展示个人仓库中的每日Issue：

```json
Issue构成：
- #关键词
 - ##论文名称
  - 论文链接、作者、摘要、chatgpt生成的总结
```



## 需求分析

1、及时获取最新的感兴趣的arxiv论文，可以通过预设关键字，并匹配文章摘要，抓取感兴趣文章；

2，利用chatgpt对匹配的文章进行总结摘要；

3、自动化流程，通过github的action方法自动实现，定时操作（比如，每日更新一次），我们仅需查看特定仓库issue即可。

## 总体原理

1）利用python抓取特定Arxiv日更文章，下载匹配文章，利用ChatGPT API分析和总结文章内容，并形成issue，发布在个人github仓库中；

2）使用Github Action实现云端部署和定时操作；

## 快速上手

### 1、复制Folk本仓库

访问本仓库`https://github.com/justchenhao/ChatDailyPapers`，点击`Folk`克隆本仓库；

修改仓库名称（创库名），例如 "hello-world"；

该仓库用于承接每日推送的Arxiv文献信息。

### 2、把复制的仓库克隆到本地

克隆你的仓库到本地：

```bash
git clone https://github.com/XXX/xxx.git
```

### 3、配置 GitHub Actions Secrets

不要把任何令牌写入 `config.py` 或提交到仓库。进入仓库的
`Settings → Secrets and variables → Actions`，新建：

- `OPENAI_API_KEY`：用于论文总结的 OpenAI API Key；

工作流会使用 GitHub 内置的短期 `GITHUB_TOKEN` 创建 Issue，因此无需创建
或保存个人访问令牌。若本地运行，先在终端设置：

```bash
export OPENAI_API_KEY='...'
export GITHUB_TOKEN='...'
export GITHUB_REPOSITORY='OWNER/REPOSITORY'
```

### 4、提交更新到Github

在仓库根目录打开`bash`命令行，输入`git`推送命令：

```bash
git status # 查看有更新的文件
git add.  # 缓存区增加文件
git commit -m 'first commit' # 代码由缓存区提交到本地仓库区
git push origin main  # 推送origin分支到远程main仓库
```

工作流会在定时任务执行，或在 Actions 页面手动运行后创建 Issue；普通 push
不会触发它。等待任务结束后，可以在 Issues 中查看更新，同时 `export` 文件夹
会新增记录完整内容的 `.md` 文件。

## 更多功能

### 修改定时推送逻辑（可选）

在仓库目录`.github/workflows/`，修改`main.yml`文件：

```
name: "daily allerts"
on:
  workflow_dispatch:
  schedule:
    -   cron: "10 20 * * 1,2,3,4,5"
permissions:
  contents: write
  issues: write
jobs:
  backup:
    runs-on: ubuntu-latest
    name: Backup
    timeout-minutes: 25
    steps:
      -   uses: actions/checkout@v2
      -   name: Set up Python 3.9
          uses: actions/setup-python@v1
          with:
            python-version: 3.9
      -   name: Setup dependencies
          run: |
            if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
      -   name: Run backup
          run: python main.py

      -   name: Commit changes
          uses: elstudio/actions-js-build/commit@v3
          with:
            commitMessage: Automated snapshot
```

根据以上yml文件，github会定时触发预定流程（10 20 * * 1,2,3,4,5表示每周一,周二,周三,周四,周五的20:10，因为[arxiv](https://arxiv.org/help/submit)每天在零时区的20点更新，也就是说在东八区是每天4点更新，或者是在更新仓库后也会触发动作）； 具体触发过程：在指定环境下，安装依赖指定文件（由requirements.txt指定），然后执行`main.py`文件，最后，提交变化更新本仓库；

### 本地调试

本地运行方法：

```cmd
python PATH-TO-CODE/main.py
```

本地调试过程中，可以在`main.py`中增加以下两行，支持本地代理：

```python
os.environ["http_proxy"] = "http://127.0.0.1:XXXX"   # 端口修改为本地代理端口
os.environ["https_proxy"] = "http://127.0.0.1:XXXX"
```



## Chatpaper

本仓库对Arxiv论文的检索和文献总结功能的实现，参考的是[Chatpaper](https://github.com/kaixindelele/ChatPaper)。

目前仅根据文献摘要和简介部分，进行以下5个问题的提问，使用者可以自行修改提示词，以实现更多定制化功能。

```python
- (1):What is the research background of this article?
- (2):What are the past methods? What are the problems with them? What difference is the proposed approach from existing methods? How does the proposed method address the mentioned problems? Is the proposed approach well-motivated? 
- (3):What is the contribution of the paper?
- (4):What is the research methodology proposed in this paper?
- (5):On what task and what performance is achieved by the methods in this paper? Can the performance support their goals?
```



### 注意事项

需要注意需要在本仓库的action设置中，把Workflow permissions改为read and write permission，以支持每日生成的`.md`文件正常上传到仓库。

# 参考

Git常见操作方法：https://www.ruanyifeng.com/blog/2015/12/git-cheat-sheet.html

arxiv文章自动issue：https://github.com/kobiso/get-daily-arxiv-noti

配置github个人访问令牌：https://docs.github.com/cn/github/authenticating-to-github/keeping-your-account-and-data-secure/creating-a-personal-access-token

chatpaper：https://github.com/kaixindelele/ChatPaper
