# panda-bamboos-rank   
python crawl for panda bamboos rank    
    
### 功能：
这是一个python爬虫。    
这是用来爬取熊猫主播的竹子数，并进行排序比较。   

### 使用方法：   
直接cmd窗口运行 python xxx.py   
   
### 目前项目进度：   
1. 以前做了个selenium版本的，但是存在一些问题（有些房间号没有数据），爬取时间也比较缓慢。   
2. 现在用了一个非官方的API  [pandatvAPI](https://github.com/MatteO-Matic/pandatvAPI)，所以直接用requests就可以了。
3. 最近又加了个并发，用的是很简单的grequests
4. 现在把项目放到阿里学生主机上，每天8pm爬取一次，保存为csv文件，主播的房间号是保存成pickle文件，以实现增量抓取。
5. 现在暂时在纠结如何处理这些数据
> csv直接变成html表格
> 使用类似jinja2之类的模板
> 将数据存储起来，用js处理，正好做个网站（本人学了一丢丢前端知识）
   
