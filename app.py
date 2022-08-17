from flask import Flask, render_template, request

import SGD_loan_1
import SGD_loan_2
import SGD_card
import SGD_insurance
import crwl

app = Flask(__name__)

@app.route('/community.html')
def community():
    return render_template('community.html')

@app.route('/goal.html')
def goal():
    return render_template('goal.html')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/indexcopy.html')
def indexcopy():
    return render_template('indexcopy.html')

@app.route('/information.html')
def information():
        result = crwl.crwl_result()

        headings = ("제목")

        return render_template("information.html",headings=headings, result=result)

@app.route('/login.html')
def login():
    return render_template('login.html')

@app.route('/main.html')
def main():
    return render_template('main.html')

@app.route('/management.html')
def management():
    return render_template('management.html')

@app.route('/map.html')
def map():
    return render_template('map.html')

@app.route('/map3.html')
def map3():
    return render_template('map3.html')

@app.route('/maps.html')
def maps():
    return render_template('maps.html')

@app.route('/maptest.html')
def maptest():
    return render_template('maptest.html')

@app.route('/mpa2.html')
def mpa2():
    return render_template('mpa2.html')

# ------------------------------------------------대출(금융)-------------------------------------------
# ---------------------------------------------------------------------------------------------------

@app.route('/management_loan_1.html',methods = ['POST', 'GET'])
def  management_loan_1():
    if request.method == 'POST':

      age = request.form['생년']
      rate = request.form['이자']
      money = request.form['금액']

      print(age)
      print(rate)
      print(money)

      result1 = SGD_loan_1.recommend_loan1(age, rate, money)

      headings = ("기관코드", "업권", "대출상품1", "대출상품2", "대출상품3", "대출금리")

      return render_template('management_loan_1.html', headings=headings, result=result1)

    else:
        return render_template('management_loan_1.html')

@app.route('/result_loan_1_1.html',methods = ['POST', 'GET'])
def result_loan_1_1():
    if request.method == 'POST':

      age = request.form['생년']
      rate = request.form['이자']
      money = request.form['금액']

      result5 = SGD_loan_1.recommend_loan1(age, rate, money)

      headings=("기관코드","업권","대출상품1","대출상품2","대출상품3","대출금리")

      return render_template("result_loan_1_1.html",headings=headings,result = result5)

    else:
        return render_template("result_loan_1_1.html")

# ------------------------------------------------대출(대부)-------------------------------------------
# ---------------------------------------------------------------------------------------------------

@app.route('/management_loan_2.html',methods = ['POST', 'GET'])
def management_loan_2():
    if request.method == 'POST':

      age = request.form['생년']
      rate = request.form['이자']
      money = request.form['금액']

      result2 = SGD_loan_2.recommend_loan2(age, rate, money)

      print(age)
      print(rate)
      print(money)

      headings=("기관코드","업권","대출상품1","대출상품2","대출상품3","대출금리")

      return render_template('management_loan_2.html',headings=headings,result = result2)
    else:
        return render_template('management_loan_2.html')

@app.route('/result_loan_1_2.html',methods = ['POST', 'GET'])
def result_loan_1_2():
    if request.method == 'POST':

      age = request.form['생년']
      rate = request.form['이자']
      money = request.form['금액']

      result6 = SGD_loan_1.recommend_loan1(age, rate, money)

      headings = ("기관코드", "업권", "대출상품1", "대출상품2", "대출상품3", "대출금리")

      return render_template("result_loan_1_2.html", headings=headings, result=result6)

    else:
        return render_template("result_loan_1_2.html")


@app.route('/result_loan_2_1.html',methods = ['POST', 'GET'])
def result_loan_2_1():
    if request.method == 'POST':

      age = request.form['생년']
      rate = request.form['이자']
      money = request.form['금액']

      print(age)
      print(rate)
      print(money)

      result7 = SGD_loan_2.recommend_loan2(age, rate, money)

      headings=("기관코드","업권","대출상품1","대출상품2","대출상품3","대출금리")

      return render_template("result_loan_2_1",headings=headings,result = result7)

    else:
        return render_template("result_loan_2_1")

@app.route('/result_loan_2_2.html',methods = ['POST', 'GET'])
def result_loan_2_2():
    if request.method == 'POST':

      age = request.form['생년']
      rate = request.form['이자']
      money = request.form['금액']

      result8 = SGD_loan_2.recommend_loan2(age, rate, money)

      headings = ("기관코드", "업권", "대출상품1", "대출상품2", "대출상품3", "대출금리")

      return render_template("result_loan_2_2.html", headings=headings, result=result8)

    else:
        return render_template("result_loan_2_2.html")

# ------------------------------------------------카드------------------------------------------------
# ---------------------------------------------------------------------------------------------------

@app.route('/management_card.html',methods = ['POST', 'GET'])
def management_card():
    if request.method == 'POST':

      age = request.form['생년']
      credit = request.form['신용판매한도금액']
      cash = request.form['현금서비스한도금액']

      result3 = SGD_card.recommend_card(age, credit, cash)

      headings=("기관코드","업권","카드유형1","카드유형2")

      return render_template('management_card.html',headings=headings,result = result3)

    else:
        return render_template('management_card.html')

@app.route('/result_card_1.html',methods = ['POST', 'GET'])
def result_card_1():
    if request.method == 'POST':


      age = request.form['생년']
      credit = request.form['신용판매한도금액']
      cash = request.form['현금서비스한도금액']

      headings=("기관코드","업권","카드유형1","카드유형2")
      result9 = SGD_card.recommend_card(age, credit, cash)

      return render_template("result_card_1.html",headings=headings,result = result9)

    else:
        return render_template("result_card_1.html")

@app.route('/result_card_2.html',methods = ['POST', 'GET'])
def result_card_2():
    if request.method == "POST":

      age = request.form['생년']
      credit = request.form['신용판매한도금액']
      cash = request.form['현금서비스한도금액']

      result8 = SGD_card.recommend_card(age, credit, cash)

      headings=("기관코드","업권","카드유형1","카드유형2")

      return render_template("result_card_2.html", headings=headings, result=result8)

    else:
        return render_template("result_card_2.html")

# ------------------------------------------------보험------------------------------------------------
# ---------------------------------------------------------------------------------------------------

@app.route('/management_insurance.html',methods = ['POST', 'GET'])
def management_insurance():

    if request.method == 'POST':

      age = request.form['생년']
      residence = request.form['거주지']
      payment = request.form['납입보험료']

      result4 = SGD_insurance.recommend_insurance(age, residence, payment)

      headings=("기관코드","업권","보험종류")

      return render_template('management_insurance.html',headings=headings,result = result4)

    else:
        return render_template('management_insurance.html')

@app.route('/result_insurance_1.html',methods = ['POST', 'GET'])
def result_insurance_1():
    if request.method == 'POST':

      age = request.form['생년']
      residence = request.form['거주지역']
      payment = request.form['납입보험료']

      result11 = SGD_insurance.recommend_insurance(age, residence, payment)
      headings=("기관코드","업권","보험종류")

      return render_template("result_insurance_1.html",headings=headings,result = result11)

    else:
        return render_template("result_insurance_1.html")

@app.route('/result_insurance_2.html',methods = ['POST', 'GET'])
def result_insurance_2():
    if request.method == 'POST':

        age = request.form['생년']
        residence = request.form['거주지역']
        payment = request.form['납입보험료']

        result12 = SGD_insurance.recommend_insurance(age, residence, payment)

        headings = ("기관코드", "업권", "보험종류")

        return render_template("result_insurance_2.html", headings=headings, result=result12)

    else:
        return render_template("result_insurance_2.html")

if __name__ ==  '__main__':
    app.debug = True
    app.run()



