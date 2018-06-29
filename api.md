# 2018 世界杯查询接口

## 返回所有32强所有球队
page为页数，为数字
```
/32/<int:page>/

```
## 返回每个小组净胜球最多的球队
```
/most_gd/
```
## 返回比分差距最大的3场比赛记录(按照比赛日期逆序排序)
```
/most-gap-3/
```
## 返回每个小组晋级的两只球队(排名优先级：积分、净胜球、球队名)
```
/promotion/
```

### 如果没有数据库，没有安装依赖包，请按以下步骤：
#### 1 安装Chrome浏览器
#### 2 进入testProject目录
#### 3 pip install -r requirements.txt
#### 4 进入worldCupSpider目录
#### 5 python run.py
#### 6 进入testProject目录
#### 7 python manage.py

