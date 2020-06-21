from pymongo import MongoClient

from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.dbterms


# HTML을 주는 부분
@app.route('/')
def home():
    return render_template('index.html')

# API 역할을 하는 부분
@app.route('/api/list', methods=['GET'])
def terms_list():
    # 1. learnterm 목록 전체를 검색합니다. 
    # 참고) find({},{'_id':False})
    # 2. 성공하면 success 메시지와 함께 terms_list 목록을 클라이언트에 전달합니다.

    terms_list = list(db.learnterm.find({},{'_id':False}) ) # 커서를 list로 변환 

    print(terms_list)
    
    return jsonify({'result': 'success','msg':'list 연결되었습니다!', 'terms_list':terms_list})


@app.route('/api/search', methods=['POST'])
def term_like():
    # 1. 클라이언트가 전달한 term_give를 term_receive 변수에 넣습니다.
    term_receive = request.form['term_give']
    print(term_receive)
    # 2. learnterm 목록에서 find_all으로 each_term이 term_receive와 일치하는 each_term을 찾습니다.
    search_term = db.learnterm.find_all({'each_term':term_receive})
    print(search_term)
    # 3. term의 like 에 1을 더해준 new_like 변수를 만듭니다.
    new_like = term['like'] + 1
    print(new_like)
    # 4. mystar 목록에서 name이 name_receive인 문서의 like 를 new_like로 변경합니다.
    db.learnterm.update_one({'name':name_receive},{'$set': {'like':new_like}})

    # 5. 성공하면 success 메시지를 반환합니다.
    return jsonify({'result': 'success','msg':'like 연결되었습니다!'})


@app.route('/api/like', methods=['POST'])
def term_like():
    # 1. 클라이언트가 전달한 term_give를 term_receive 변수에 넣습니다.
    term_receive = request.form['term_give']
    print(term_receive)
    # 2. learnterm 목록에서 find_all으로 each_term이 term_receive와 일치하는 each_term을 찾습니다.
    term = db.learnterm.find_one({'each_term':term_receive})
    # 3. term의 like 에 1을 더해준 new_like 변수를 만듭니다.
    new_like = term['like'] + 1
    # print(new_like)
    # 4. mystar 목록에서 name이 name_receive인 문서의 like 를 new_like로 변경합니다.
    db.learnterm.update_one({'each_term':term_receive},{'$set': {'like':new_like}})
    # 5. 성공하면 success 메시지를 반환합니다.
    return jsonify({'result': 'success','msg':'like 연결되었습니다!'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)