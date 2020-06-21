import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.dbterms

# 용어별 링크에 접근하기 위한 Seq.번호를 가져오기 
def get_word_seq():
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.post('https://terms.tta.or.kr/dictionary/dictionaryNewWordList.do', headers=headers, data={'listPage':1})
    soup = BeautifulSoup(data.text, 'html.parser')

    each_page = soup.select('#m_content > ul > li > dl')

    word_seqs =[]
    for one in each_page:
        word_seq = one.select('dl > dt > a')[0]['href']
        word_seq = word_seq[-10:-2]
        word_seqs.append(word_seq)
    #print(word_seqs)
    return word_seqs
    

# Seq.번호별로 용어 설명 페이지에서 용어/설명/이미지를 가져 와서 DB에 하나의 레코드를 Insert하는 함수 
def get_term(word_seq):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}

    data = requests.post('https://terms.tta.or.kr/dictionary/dictionaryView.do', headers=headers, data={'word_seq':word_seq})
    
    soup = BeautifulSoup(data.text, 'html.parser')
    
    each_term = soup.select_one('#cont > dl > dt').text.strip() 
    each_desc = soup.select_one('#cont > dl > dd > div').text
    each_img = soup.select_one('#cont > dl > dd > div').find('img')
    image_src = None
    if None != each_img:
        image_src = each_img['src']


    doc = {
    'each_term': each_term,
    'each_desc': each_desc,
    #'each_img': each_img    
    # 'term_like : term_like    
    }
    # DB에 하나의 레코드 Insert
    db.learnterm.insert_one(doc)
    print('완료!\n', each_term)
    print(image_src)


# 기존 learnterm 콜렉션을 삭제하고, 출처 ter 가져온 후, 크롤링하여 DB에 저장합니다.
def insert_all():
    db.learnterm.drop()  # learnterm 콜렉션을 모두 지워줍니다.
    print(get_word_seq())
    word_seqs =  get_word_seq()
    for word_seq in word_seqs:
        get_term(word_seq)


### 웹페이지에서 가져온 데이터를 모두 DB에 Insert하기 
insert_all()
