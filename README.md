# app 评论处理系统
[评论分类](https://alittlegreens.github.io/app_report/#/)

## 一、抓取应用数据
通过fetch_comment.py 抓取评论数据

**首先配置应用信息**

1. 设置应用程序 ID
appid = 1544760744

 2. 设置包名
appid_android = 'com.philips.ph.babymonitorplus'

 3. 设置你想筛选哪个版本的评论 commentjson = '1.1.1'

程序执行完毕后，评论的json文件会在comment文件夹中生成


## 二 评论分类
将Json文件导入到[评论分类](https://alittlegreens.github.io/app_report/#/) 进行分类


## 三、将分类好的评论导入Flutter项目中

