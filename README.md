# 2233
- 个人github上，太多烂尾的库，综合一波。。
- 这个库里将放各种bili上的code就是了。。
- 2019/02/08 再次维护这堆项目（能跑就行）

## 目录结构

- [danmuku.py](#弹幕爬虫说明) --- 弹幕爬虫
- [robfloor.py](#BILI_RobFloor) --- 抢楼器 （暂未维护）
- [dosign.py](#直播签到，银瓜子换硬币) --- 直播签到，银瓜子换硬币脚本
- old --- 存放旧代码（git会有记录，还是有点麻烦




## BILI_RobFloor

### 说明

- 自制B站抢楼器，目前为多线程demo版
- 账号被封一概不负责
- 目前基本就是封装调用了三个api。。。orz

### 使用方法

- 当前目录下bilicookies文件存里登录cookie信息
- 修改task函数，bi.run()传入相应的参数
- 线程数，线程的等待自行调整

BILI类内，run(av_num, floor, content)，av_num为要抢的视频号，floor是要抢的楼层，content是要发的评论的内容。不传入av_num则是搜索订阅的最新视频。



## 直播签到，银瓜子换硬币

- 当前目录下bilicookies文件存里登录cookie信息（最好是保存成功签到时用的cookies）
- 然后执行dosign.py。即可
- 若想自动化执行，找个服务器，Linux下可用 crontab设置定时任务。
- silver2coin函数会使用银瓜子兑换硬币（升级用），自行决定使用与否，默认注释




## 弹幕爬虫说明

- 目前是爬取指定av号或ep号番剧的弹幕存到本地
- 弹幕信息有内容，时间，和时间2233

### 使用方法

```powershell
PS E:\GITWORKS\BILI> python .\danmuku.py -h
usage: danmuku.py [-h] [-i INPUT] [-o OUTPUT]

Welcome to BILI

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        set the av_number or eq_number to crawl
  -o OUTPUT, --output OUTPUT
                        set the filename to store
PS E:\GITWORKS\BILI> python .\danmuku.py -i av42807128 -o danmu.csv
42807128
cid = 75051785
写入弹幕ing...
写入完成...请查看danmu.csv
```



