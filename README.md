# panda-bamboos-rank   
python crawl for panda bamboos rank    
    
### 功能：
这是一个python爬虫。    
这是用来爬取熊猫主播的竹子数，并进行排序比较。 

v1展示页面： [熊猫TV竹子Top20](http://zuilexuan.com/panda/rank.html)

### 项目近况：
1. 目前做了个v1版本
2. 这个v1版本开发环境是：python3.5 、 windows 10
3. 使用的python库有requests、pickle、pymongo等
4. 使用了mongodb数据库
5. 使用echarts来展示数据，并稍微做了点移动端支持
6. 使用了一个非官方的API  [pandatvAPI](https://github.com/MatteO-Matic/pandatvAPI)，但是熊猫最近升级了一些地址，比如roomid那个就变了

### 历史遗留问题：
1. 删除了selenium版本，可在提交记录里查看
2. 移除了并发模块grequests，因为API有限制，不想用代理池 

### 使用方法：
1. 先安装好mongodb数据库，启动数据库 $ mongod
2. 运行爬虫文件 $ python panda_crawler.py
3. 运行分析脚本生成json文件 $python analyze.py
4. bamboos_rank.json就是我们的数据
5. roomList.pickle是保存房间号的，用于实现增量抓取
6. rank.html实现了使用echarts和jquery来展示数据，本地不可调试（跨域问题）。

   
