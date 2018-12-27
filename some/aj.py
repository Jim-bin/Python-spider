# -*- coding:utf-8 -*_

import requests
import json

headers = {
    'Accept': 'application/json',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Content-Length': '1919',
    'Content-Type': 'application/json',
    'Cookie': 'bid=FvGxnjrHNYI; gr_user_id=c211a350-d924-429f-9028-afd61661913f; _vwo_uuid_v2=DD2B02C913FD5A4D2EFE19BBBB71F1473|8e6abeedccfd8ccd3b590f121d180376; __utmc=30149280; __utmz=30149280.1545471350.6.6.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); viewed="10756112_5273955_1088168_27069345_26601155_10590856"; _ga=GA1.3.497061328.1543886034; ap_v=0,6.0; __utma=30149280.497061328.1543886034.1545471350.1545887406.7; _gid=GA1.3.452249281.1545887527; _pk_ref.100001.a7dd=%5B%22%22%2C%22%22%2C1545887527%2C%22https%3A%2F%2Fwww.jianshu.com%2Fp%2Fb29375404479%22%5D; _pk_ses.100001.a7dd=*; _pk_id.100001.a7dd=ee586b77c5c08a27.1545487781.2.1545889502.1545488713.',
    'DNT': '1',
    'Host': 'read.douban.com',
    'Origin': 'https://read.douban.com',
    'Referer': 'https://read.douban.com/category/?kind=114',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
    'X-CSRF-Token': 'null',
}

data = {"sort":"hot","page":1,"kind":114,"query":"\n    query getFilterWorksList($works_ids: [ID!], $user_id: ID) {\n      worksList(worksIds: $works_ids) {\n        \n    \n    title\n    cover\n    url\n    isBundle\n  \n    \n    url\n    title\n  \n    \n    author {\n      name\n      url\n    }\n    origAuthor {\n      name\n      url\n    }\n    translator {\n      name\n      url\n    }\n  \n    \n    abstract\n    editorHighlight\n  \n    \n    isOrigin\n    kinds {\n      \n    name @skip(if: true)\n    shortName @include(if: true)\n    id\n  \n    }\n    ... on WorksBase @include(if: true) {\n      wordCount\n      wordCountUnit\n    }\n    ... on WorksBase @include(if: true) {\n      \n    isEssay\n    \n    ... on EssayWorks {\n      favorCount\n    }\n  \n    \n    isNew\n    \n    averageRating\n    ratingCount\n    url\n  \n  \n  \n    }\n    ... on WorksBase @include(if: false) {\n      isColumn\n      isEssay\n      onSaleTime\n      ... on ColumnWorks {\n        updateTime\n      }\n    }\n    ... on WorksBase @include(if: true) {\n      isColumn\n      ... on ColumnWorks {\n        isFinished\n      }\n    }\n    ... on EssayWorks {\n      essayActivityData {\n        \n    title\n    uri\n    tag {\n      name\n      color\n      background\n      icon2x\n      icon3x\n      iconSize {\n        height\n      }\n      iconPosition {\n        x y\n      }\n    }\n  \n      }\n    }\n    highlightTags {\n      name\n    }\n  \n    ... on WorksBase @include(if: false) {\n      \n    fixedPrice\n    salesPrice\n    isRebate\n  \n    }\n    ... on EbookWorks {\n      \n    fixedPrice\n    salesPrice\n    isRebate\n  \n    }\n    ... on WorksBase @include(if: true) {\n      ... on EbookWorks {\n        id\n        isPurchased(userId: $user_id)\n        isInWishlist(userId: $user_id)\n      }\n    }\n  \n        id\n        isOrigin\n      }\n    }\n  ","variables":{"user_id":""}}

url = 'https://read.douban.com/j/kind/'

r = requests.post(url, headers=headers, data=json.dumps(data))
text = r.text
text = json.loads(text)
total = text["total"]
lists = text["list"]
for i in lists:
    title = i.['title']
    cover = i.['cover']
    book_url = 'https://read.douban.com' + i.['book_url']
    book_url = 'https://read.douban.com' + i.['book_url']
# print(total)
# print(lists)
