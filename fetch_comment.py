import os
import requests
import json
import concurrent.futures
from google_play_scraper import Sort, reviews
from pygtrans import Translate
from dateutil import parser
import time
import random



# 设置应用程序 ID
appid = 1544760744
appid_android = 'com.philips.ph.babymonitorplus'

# 设置输出文件名
commentjson = '1.1.1'

# 翻译
client = Translate()
client.translate

# 设置语言和国家列表
arrcc = [
  {'cc': 'cn', 'country': "中国"},
  {'cc': 'us', 'country': "美国"},
  {'cc': 'gb', 'country': "英国"},
  {'cc': 'hk', 'country': "中国香港"},
  {'cc': 'my', 'country': "马来西亚"},
  {'cc': 'th', 'country': "泰国"},
  {'cc': 'sg', 'country': "新加坡"},
  {'cc': 'id', 'country': "印度尼西亚"},
  {'cc': 'vn', 'country': "越南"},
  {'cc': 'ae', 'country': "阿拉伯联合酋长国"},
  {'cc': 'sa', 'country': "沙特阿拉伯"},
  {'cc': 'dk', 'country': "丹麦"},
  {'cc': 'fi', 'country': "芬兰"},
  {'cc': 'se', 'country': "瑞典"},
  {'cc': 'eg', 'country': "埃及"},
  {'cc': 'it', 'country': "意大利"},
  {'cc': 'fr', 'country': "法国"},
  {'cc': 'nl', 'country': "荷兰"},
  {'cc': 'at', 'country': "奥地利"},
  {'cc': 'ch', 'country': "瑞士"},
  {'cc': 'be', 'country': "比利时"},
  {'cc': 'pl', 'country': " 波兰"},
  {'cc': 'pt', 'country': " 葡萄牙"},
  {'cc': 'cz', 'country': " 捷克"},
  {'cc': 'es', 'country': "西班牙"},
  {'cc': 'hu', 'country': "匈牙利"},
  {'cc': 'ro', 'country': "罗马尼亚"},
  {'cc': 'de', 'country': "德国"},
  {'country': "加拿大", 'cc': 'ca'},
  {'country': "阿尔及利亚", 'cc': 'dz'},
  {'country': "爱尔兰", 'cc': 'ie'},
  {'country': "爱沙尼亚", 'cc': 'ee'},
  {'country': "挪威", 'cc': 'no'},
  {'country': "希腊", 'cc': 'gr'},
  {'country': "塞浦路斯", 'cc': 'cy'},
  {'country': "斯洛文尼亚", 'cc': 'si'},
  {'country': "拉脱维亚", 'cc': 'lv'},
  {'country': "立陶宛", 'cc': 'lt'},
  {'country': "卢森堡", 'cc': 'lu'},
  {'country': "马耳他", 'cc': 'mt'},
  {'country': "斯洛伐克", 'cc': 'sk'},
  {'country': "克罗地亚", 'cc': 'hr'},
  {'country': "保加利亚", 'cc': 'bg'},
  {'country': "冰岛", 'cc': 'is'},
]

android_arrcc = [
  {'lang': 'cn', 'country': "中国"},
  {'lang': 'hk', 'country': "中国香港"},
  {'lang': 'my', 'country': "马来西亚"},
  {'lang': 'th', 'country': "泰国"},
  {'lang': 'sg', 'country': "新加坡"},
  {'lang': 'id', 'country': "印度尼西亚"},
  {'lang': 'vn', 'country': "越南"},
  {'lang': 'ae', 'country': "阿拉伯联合酋长国"},
  {'lang': 'sa', 'country': "沙特阿拉伯"},
  {'lang': 'da', 'country': "丹麦"},
  {'lang': 'fi', 'country': "芬兰"},
  {'lang': 'sk', 'country': "瑞典"},
  {'lang': 'eg', 'country': "埃及"},
  {'lang': 'it', 'country': "意大利"},
  {'lang': 'fr', 'country': "法国"},
  {'lang': 'nl', 'country': "荷兰"},
  {'lang': 'at', 'country': "奥地利"},
  {'lang': 'ch', 'country': "瑞士"},
  {'lang': 'be', 'country': "比利时"},
  {'lang': 'pl', 'country': " 波兰"},
  {'lang': 'pt', 'country': " 葡萄牙"},
  {'lang': 'cs', 'country': " 捷克"},
  {'lang': 'es', 'country': "西班牙"},
  {'lang': 'hu', 'country': "匈牙利"},
  {'lang': 'ro', 'country': "罗马尼亚"},
  {'lang': 'de', 'country': "德国"},
  {'lang': 'en', 'country': "英国"},
  {'country': "加拿大", 'lang': 'ca'},
  {'country': "阿尔及利亚", 'lang': 'dz'},
  {'country': "爱尔兰", 'lang': 'ie'},
  {'country': "爱沙尼亚", 'lang': 'ee'},
  {'country': "挪威", 'lang': 'no'},
  {'country': "希腊", 'lang': 'gr'},
  {'country': "塞浦路斯", 'lang': 'cy'},
  {'country': "斯洛文尼亚", 'lang': 'si'},
  {'country': "拉脱维亚", 'lang': 'lv'},
  {'country': "立陶宛", 'lang': 'lt'},
  {'country': "卢森堡", 'lang': 'lu'},
  {'country': "马耳他", 'lang': 'mt'},
  {'country': "斯洛伐克", 'lang': 'sk'},
  {'country': "克罗地亚", 'lang': 'hr'},
  {'country': "保加利亚", 'lang': 'bg'},
  {'country': "冰岛", 'lang': 'is'},
]

# 初始化变量
all_ios_reviews = []
alljson = {}
all_total = 0


def translate_content(content):
  trans = client.translate(content)
  if isinstance(trans, list):
    trans = trans[0]
  return trans.translatedText


def fetch_reviews(country_item, page):
  cc = country_item['cc']
  country_name = country_item['country']
  myurl = f"https://itunes.apple.com/rss/customerreviews/page={page}/id={appid}/sortby=mostrecent/json?l=en&&cc={cc}"
  print(f'正在获取 {country_name} 第 {page} 页评论')
  
  response = requests.get(myurl)
  response.raise_for_status()
  myjson = response.json()
  feed = myjson["feed"]
  
  # 检查是否有数据
  if 'entry' not in feed or not feed['entry']:
    print(f'{country_name} 第 {page} 页没有数据，跳过当前国家')
    return False
    
  entry = feed['entry']
  if not isinstance(entry, dict):
    for obj in entry:
      obj['os'] = {"label": "IOS"}
      obj['cc'] = cc
      obj['ty_review_type'] = '0'  # 0 代表未定义, 1 代表需求 2 代表bug
      obj['ty_question_type'] = '0'  # ty_question_type ： 0代表未分类，通知问题、配网问题、拉流问题、网络问题、设备问题、崩溃问题、需求性问题、适配问题、兼容性问题、非问题、其他 依次递增
      obj['content_translate'] = obj['content']['label']
      obj['title_translate'] = obj['title']['label']
    all_ios_reviews.extend(entry)
  else:
    entry['os'] = {"label": "IOS"}
    entry['cc'] = cc
    entry['ty_question_type'] = '0'  # ty_question_type ： 0代表未分类，通知问题、配网问题、拉流问题、网络问题、设备问题、崩溃问题、需求性问题、适配问题、兼容性问题、非问题、其他 依次递增
    entry['ty_review_type'] = '0'  # 0 代表未定义, 1 代表需求 2 代表bug
    entry['content_translate'] = entry['content']['label']
    entry['title_translate'] = entry['title']['label']
    all_ios_reviews.append(entry)
  alljson = myjson
  alljson['feed']['entry'] = all_ios_reviews
  print(f'{country_name} 第 {page} 页评论获取完成，当前总评论数：{len(all_ios_reviews)}')
  return True


# 串行执行，每次请求后随机延时1-2秒
for country_item in arrcc:
  for page in range(1, 11):
    has_data = fetch_reviews(country_item, page)
    if not has_data:
      break  # 如果当前页没有数据，跳出内层循环，处理下一个国家
    # 随机延时1-2秒
    delay = random.uniform(0.5, 1.5)
    print(f'等待 {delay:.1f} 秒后继续...')
    time.sleep(delay)

print("app store comment length:"+str(len(all_ios_reviews)))

all_android_reviews = []


def convert_review_to_ios(review):
  reviewToiOS = {
    "author": {
      "uri": {"label": ""},
      "name": {"label": ""},
      "label": ""
    },
    "updated": {"label": ""},
    "im:rating": {"label": ""},
    "im:version": {"label": ""},
    "id": {"label": ""},
    "title": {"label": ""},
    "content": {
      "label": "",
      "attributes": {"type": "text"}
    },
    "content_translate": "",
    "title_translate": "",
    "link": {
      "attributes": {
        "rel": "related",
        "href": ""
      }
    },
    "im:voteSum": {"label": "0"},
    "im:contentType": {
      "attributes": {
        "term": "Application",
        "label": "Application"
      }
    },
    "im:voteCount": {"label": "0"},
    "os": {"label": "android"},
    "cc": ""

  }
  reviewToiOS['author']['name']['label'] = review['userName']
  reviewToiOS['author']['label'] = review['userName']
  reviewToiOS['updated']['label'] = review['at'].strftime('%Y-%m-%dT%H:%M:%SZ')
  reviewToiOS['im:rating']['label'] = review['score']
  if review['reviewCreatedVersion'] is None:
    reviewToiOS['im:version']['label'] = '1.0.0'
  else:
    reviewToiOS['im:version']['label'] = review['reviewCreatedVersion']
  reviewToiOS['id']['label'] = review['reviewId']
  reviewToiOS['content']['label'] = review['content']
  reviewToiOS['title_translate'] = ''
  reviewToiOS['cc'] = review['cc']
  reviewToiOS['content_translate'] = review['content']
  reviewToiOS['im:voteSum']['label'] = review['thumbsUpCount']
  reviewToiOS['im:voteCount']['label'] = review['thumbsUpCount']
  reviewToiOS['os']['label'] = 'android'
  reviewToiOS['ty_review_type'] = '0'  # 0 代表未定义, 1 代表需求 2 代表bug
  reviewToiOS[
    'ty_question_type'] = '0'  # ty_question_type ： 0代表未分类，通知问题、配网问题、拉流问题、网络问题、设备问题、崩溃问题、需求性问题、适配问题、兼容性问题、非问题、其他 依次递增
  return reviewToiOS


# 获取评论
def get_review_by_cc(cc):
  reviewList = reviews(
    app_id=appid_android,  # type: ignore
    sort=Sort.NEWEST,
    count=3000,
    lang=cc
  )
  if reviewList[0] is not None:

    for androidItem in reviewList[0]:
      androidItem["cc"] = cc

    all_android_reviews.extend(reviewList[0])
  else:
    print('no review')


iosList = []

with concurrent.futures.ThreadPoolExecutor() as executor:
  for country_item in android_arrcc:
    executor.submit(get_review_by_cc, country_item['lang'])

# 转换评价格式
for review in all_android_reviews:
  ios_review = convert_review_to_ios(review)
  iosList.append(ios_review)

print("google play comment length:"+str(len(iosList)))

all_ios_reviews.extend(iosList)

# # 筛选版本
all_ios_reviews = [d for d in all_ios_reviews if str(d['im:version']['label']) == commentjson]

unique_dict_array = []
id_set = set()

for item in all_ios_reviews:
  if item['updated']['label'] not in id_set:
    unique_dict_array.append(item)
    id_set.add(item['updated']['label'])

all_ios_reviews = unique_dict_array

# 筛选title
titles = [d['title']['label'] for d in all_ios_reviews]

title_texts = client.translate(titles)
for index, text in enumerate(title_texts):
  all_ios_reviews[index]['title_translate'] = text.translatedText

# 筛选内容
contents = [d['content']['label'] for d in all_ios_reviews]

texts = client.translate(contents)
for index, text in enumerate(texts):
  all_ios_reviews[index]['content_translate'] = text.translatedText

print("V"+commentjson+" comment length:"+str(len(all_ios_reviews)))

# 使用sorted()函数和lambda函数按时间戳排序
timeSortList = sorted(all_ios_reviews, key=lambda x: parser.parse(x["updated"]["label"]),reverse=True)


# '你好，谷歌'
#             >>> texts = client.translate(['批量测试', '批量翻译'], target='en')
#             >>> for text in texts:
#             ...     print(text.translatedText)

# 将 JSON 数据写入文件
directory = "comment"
if not os.path.exists(directory):
 os.makedirs(directory)
file_path = os.path.join(directory, "V"+commentjson + ".json")
with open(file_path, 'w') as f:
  json.dump({'feed': {'entry': timeSortList}}, f, indent=4)
