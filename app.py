# Flaskを読み込む(render_template=HTMLを返す, request=送られたデータを受け取る)
from flask import Flask, render_template, request
# 日時を扱う道具を読み込む(Pythonに最初から入ってる)
from datetime import datetime
# タイムゾーン(地域ごとの時刻)を扱う道具
from zoneinfo import ZoneInfo

# アプリ本体を作る
app = Flask(__name__)

# 「/」(トップページ)にアクセスが来たら、この関数を実行する
@app.route("/")
def home():
    return "<h1>Hello! 俺のFlaskサーバーが動いてるぞ。</h1>"

@app.route("/about")
def about():
    return "<h1>このサイトについて</h1><p>イラスト描いてます。</p>"

# 「/time」にアクセスが来たら、今の時刻を計算して返す
@app.route("/time")
def show_time():
    now = datetime.now(ZoneInfo("Asia/Tokyo"))        # ① 今の時刻を「日本時間」で取得
    now_str = now.strftime("%Y年%m月%d日 %H時%M分%S秒")  # ② 読みやすい形に整える
    return render_template("time.html", now=now_str)     # ③ time.html に now を渡して表示

# 「/greet」: 名前を入力してもらい、あいさつを返す
@app.route("/greet", methods=["GET", "POST"])
def greet():
    if request.method == "POST":              # ① 送信ボタンが押されて来た時
        username = request.form["username"]   # ② 入力された名前を取り出す
        return render_template("greet.html", name=username)  # ③ あいさつを返す
    return render_template("form.html")       # ④ 普通にアクセスされた時は入力画面を出す

# 「/calc」: 数字を2つ受け取って足し算を返す
@app.route("/calc", methods=["GET", "POST"])
def calc():
    if request.method == "POST":
        num1 = int(request.form["num1"])   # ① 入力を「数字」に変換(ここが肝!)
        num2 = int(request.form["num2"])   # ②
        answer = num1 + num2               # ③ 足し算
        return render_template("calc_result.html", num1=num1, num2=num2, answer=answer)
    return render_template("calc.html")    # ④ 普通のアクセスなら入力画面

# 「/gallery」: イラストを並べて表示する
@app.route("/gallery")
def gallery():
    return render_template("gallery.html")

# 「/works」: 作品を文章つき・タブ切り替えで紹介する
@app.route("/works")
def works():
    return render_template("works.html")

# 「/alternative」: 進捗トラッカー ALTERNATIVE(MVP=イラスト1枚の5段階タブ)
@app.route("/alternative")
def alternative():
    return render_template("alternative.html")

# 「/study」: 資格(FE)の週間プログレス。localStorageでチェック状態を保存
@app.route("/study")
def study():
    return render_template("study.html")

# このファイルを直接実行したらサーバーを起動する
if __name__ == "__main__":
    app.run(debug=True)
