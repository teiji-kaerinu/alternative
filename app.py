# Flaskを読み込む(render_template=HTMLを返す, request=送られたデータを受け取る)
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime, timezone


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///alternative.db"
# initialize the app with the extension
db.init_app(app)


class Spot(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    work: Mapped[str] = mapped_column()
    address: Mapped[str | None] = mapped_column()
    lat: Mapped[float | None] = mapped_column()
    lng: Mapped[float | None] = mapped_column()
    scene_note: Mapped[str | None] = mapped_column()
    priority: Mapped[int] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc)
    )
    # datetime.now(timezone.utc)


# 「/」トップページ
@app.route("/")
def home():
    return render_template("index.html")


# 「/gallery」: イラストを並べて表示する
@app.route("/gallery")
def gallery():
    return render_template("gallery.html")


# 「/works」: 作品を文章つき・タブ切り替えで紹介する
@app.route("/works")
def works():
    return render_template("works.html")


# --- ここから下が ALTERNATIVE 本体(聖地巡礼)。これから実装する ---
# TODO: F1 ユーザー登録・ログイン        (Flask-Login)
# TODO: F2 スポットのCRUD                 (Flask-SQLAlchemy)
# TODO: F3 訪問記録の投稿(写真1枚)        (Cloudinary)
# TODO: F4 一覧と絞り込み(未訪問/訪問済み)
# TODO: F5 地図表示                       (Leaflet + OpenStreetMap)


# このファイルを直接実行したらサーバーを起動する
if __name__ == "__main__":
    app.run(debug=True)
