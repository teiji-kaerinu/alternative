# Flaskを読み込む(render_template=HTMLを返す, request=送られたデータを受け取る)
from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime, timezone
from flask_migrate import Migrate
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, ValidationError
from werkzeug.security import generate_password_hash
from flask_login import LoginManager, UserMixin


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)

login_manager = LoginManager()

app = Flask(__name__)
login_manager.init_app(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///alternative.db"
app.config.from_prefixed_env()

# initialize the app with the extension
db.init_app(app)
migrate = Migrate(app, db)


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


class User(UserMixin, db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    password_hash: Mapped[str] = mapped_column()


@login_manager.user_loader
def user_loader(user_id):
    return db.session.get(User, int(user_id))


class RegisterForm(FlaskForm):
    username = StringField("ユーザー名", validators=[DataRequired()])
    password = PasswordField("パスワード", validators=[DataRequired()])
    submit_button = SubmitField("登録")

    def validate_username(self, field):
        stmt = db.select(User).filter_by(username=field.data)
        user = db.session.execute(stmt).scalar()
        if user != None:
            raise ValidationError("この名前はもう使われています")


# 「/」トップページ
@app.route("/")
def home():
    return render_template("index.html")


# 「/gallery」: イラストを並べて表示する
@app.route("/gallery")
def gallery():
    return render_template("gallery.html")


# 「/spots」: スポットを並べて表示する
@app.route("/spots")
def spots():
    spots = db.session.execute(db.select(Spot)).scalars()
    return render_template("spots.html", spots=spots)


# 　「/register」:　登録画面の表示
@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        password_hash = generate_password_hash(password)
        user = User(username=username, password_hash=password_hash)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("spots"))
    return render_template("register.html", form=form)
    # print(form)


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
