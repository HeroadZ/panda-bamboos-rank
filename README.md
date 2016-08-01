# panda-bamboos-rank
python crawl for panda bamboos rank    
    
这是一个python爬虫，用了selenium。    
这是用来爬取熊猫主播的竹子数，并进行排序比较。   

使用方法：直接cmd窗口运行 python selenium_test.py   
我在程序里设置了爬取的正在直播页数为2页，可以自行改变   
结果保存为csv文件，房间号列表保存为pickle文件，是增量的    
   
项目特性：    
1、在爬取正在直播的主播时，由于主播在线时间不固定，需要多次爬取    
2、在获取每个房间的id和竹子时，使用了一个非官方的pandaTV API  [pandatvAPI](https://github.com/MatteO-Matic/pandatvAPI)
