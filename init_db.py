import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.dbsparta

# DB에 저장할 용어의 url을 가져옵니다. 

def get_terms():
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get('https://terms.tta.or.kr/dictionary/dictionaryNewWordList.do', headers=headers)

    soup = BeautifulSoup(data.text, 'html.parser')

    all_contents = soup.select('#m_content > ul > li > dl')   #m_content > ul > li > dl:nth-child(1) > dt > a > b > font

    terms = []
    for one in all_contents:
        term = one.select_one('dt > a > b ').text.strip()
        desc = one.select_one('> dd').get_text()
        term = term + desc
        terms.append(term)        
    return terms

print(get_terms())


# 출처 url로부터 영화인들의 사진, 이름, 최근작 정보를 가져오고 mystar 콜렉션에 저장합니다.



# def insert_term(term):
#     headers = {
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
#     data = requests.get(url, headers=headers)

#     soup = BeautifulSoup(data.text, 'html.parser')

#     name = soup.select_one('#content > div.article > div.mv_info_area > div.mv_info.character > h3 > a').text
#     img_url = soup.select_one('#content > div.article > div.mv_info_area > div.poster > img')['src']
#     recent = soup.select_one(
#         '#content > div.article > div.mv_info_area > div.mv_info.character > dl > dd > a:nth-child(1)').text

#     doc = {
#         'name': name,
#         'img_url': img_url,
#         'recent': recent,
#         'url': url,
#         'like': 0
#     }

#     db.mystar.insert_one(doc)
#     print('완료!', name)



# 기존 mystar 콜렉션을 삭제하고, 출처 url들을 가져온 후, 크롤링하여 DB에 저장합니다.


# def insert_all():
#     db.terms.drop()  # mystar 콜렉션을 모두 지워줍니다.
#     terms = get_terms()
#     for term in terms:
#         insert_star(term)


### 실행하기
# insert_all()