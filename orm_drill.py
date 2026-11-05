# ALTERNATIVE 課題: SQL と Flask(SQLAlchemy) の対応ドリル
#
# 実行(flask-hello フォルダで): venv/Scripts/python practice/orm_drill.py
# 使うDBはメモリの中だけ。本物の alternative.db には触らない。
#
# やり方
#   1. 各問の `return MADA` を消して、答えを書く
#   2. 保存して実行する。○×と、実際に飛んだSQLが出る
#   3. 全部終わらなくていい。何度でも実行していい
#
# 言葉
#   注文票 = db.select(...)
#   厨房   = db.session.execute(...)
#   箱     = .scalars() の結果。何件も入る。0件でも None にならない
#   本体   = .scalar() の結果。1件の中身。0件なら None
#
# 詰まったら ORM読解ノート: https://claude.ai/artifact/L2uHmajKpqQZxFQjAFKe27
#
# ドリルのデータ(1問ごとにこの状態へ戻る)
#
# user
#   id  username
#   1   kaeriinu
#   2   sample
#
# spot
#   id  user_id  name        work              priority
#   1   1        真野湾      オルタネイティヴ  1
#   2   1        両津港      オルタネイティヴ  1
#   3   1        校舎裏の岡  オルタネイティヴ  2
#   4   1        萬代橋      WAR ENSEMBLE      2
#   5   2        新潟駅      WAR ENSEMBLE      1
#   6   2        横浜駅      オルタネイティヴ  3

from flask import Flask, abort
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime, timezone


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
db.init_app(app)


class Spot(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
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


class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    password_hash: Mapped[str] = mapped_column()


# 未回答の目印。答えを書くときに消す
MADA = "MADA"


# 第1部 読む: SQL を Flask に訳す ---------------------------------------------


def q1():
    """全部のスポット

    SQL: SELECT * FROM spot
    返すもの: 箱
    """

    stmt = db.select(Spot)
    print("① 注文票:", stmt)

    result = db.session.execute(stmt)
    print("② 実行結果:", result)

    box = result.scalars()
    print("③ 取り出した:", box)

    # print("1回目:", list(box))
    # print("2回目:", list(box))
    # for spot in box:
    # print("④ 1件:", spot, spot.name)

    return box


def q2():
    """kaeriinu(ユーザーid=1)のスポット

    SQL: SELECT * FROM spot WHERE user_id = 1
    返すもの: 箱
    """
    stmt = db.select(Spot).filter_by(user_id=1)
    print("① 注文票:", stmt)

    result = db.session.execute(stmt)
    print("② 実行結果:", result)

    box = result.scalars()
    print("③ 取り出した:", box)

    # print("1回目:", list(box))
    # print("2回目:", list(box))
    # for spot in box:
    # print("④ 1件:", spot, spot.name)

    return box


def q3():
    """kaeriinu の、優先度1のスポット

    SQL: SELECT * FROM spot WHERE user_id = 1 AND priority = 1
    返すもの: 箱
    """
    stmt = db.select(Spot).filter_by(user_id=1, priority=1)
    print("① 注文票:", stmt)

    result = db.session.execute(stmt)
    print("② 実行結果:", result)

    box = result.scalars()
    print("③ 取り出した:", box)

    return box


def q4():
    """id=2 のスポット

    SQL: SELECT * FROM spot WHERE id = 2
    返すもの: 本体
    """
    stmt = db.select(Spot).filter_by(id=2)
    print("① 注文票:", stmt)

    result = db.session.execute(stmt)
    print("② 実行結果:", result)

    spot = result.scalar()
    print("③ 取り出した:", spot)

    return spot


def q5():
    """id=999 のスポット(存在しない)

    SQL: SELECT * FROM spot WHERE id = 999
    返すもの: None
    Q4と同じ形で書く。`return None` と直接書くのは無し
    """
    stmt = db.select(Spot).filter_by(id=999)
    print("① 注文票:", stmt)

    result = db.session.execute(stmt)
    print("② 実行結果:", result)

    spot = result.scalar()
    print("③ 取り出した:", spot)

    return spot


def q6():
    """名前が sample のユーザー

    SQL: SELECT * FROM user WHERE username = 'sample'
    返すもの: 本体
    """
    stmt = db.select(User).filter_by(username="sample")
    print("① 注文票:", stmt)

    result = db.session.execute(stmt)
    print("② 実行結果:", result)

    spot = result.scalar()
    print("③ 取り出した:", spot)

    return spot


# 第2部 箱と本体 --------------------------------------------------------------


def q7():
    """kaeriinu のスポットの「名前だけ」をリストにする

    SQL: SELECT * FROM spot WHERE user_id = 1
    返すもの: ["真野湾", "両津港", ...] のようなリスト
    箱を取り出して、for で1件ずつ names に足す
    """

    stmt = db.select(Spot).filter_by(user_id=1)
    print("① 注文票:", stmt)

    result = db.session.execute(stmt)
    print("② 実行結果:", result)

    spot = result.scalars()
    print("③ 取り出した:", spot)
    names = []
    # names.append(spot.name)

    # names = list(spot.names)
    # name = names[0]
    for MUV in spot:
        names.append(MUV.name)
        print(MUV.name)

    return names


def q8(user_id, spot_id):
    """「その番号で、その人のスポット」を1件探す

    SQL: SELECT * FROM spot WHERE user_id = (引数user_id) AND id = (引数spot_id)
    返すもの: 見つかれば本体、無ければ None
    """
    stmt = db.select(Spot).filter_by(user_id=user_id, id=spot_id)
    print("① 注文票:", stmt)

    result = db.session.execute(stmt)
    print("② 実行結果:", result)

    spot = result.scalar()
    print("③ 取り出した:", spot)

    return spot


# 第3部 書く: SQL を Flask に訳す ---------------------------------------------


def q9():
    """スポットを1件追加する

    SQL: INSERT INTO spot (user_id, name, work, priority)
         VALUES (1, '加茂湖', 'オルタネイティヴ', 3)
    返すもの: 無し(return MADA を消すだけ)
    """

    spot = Spot(
        user_id=1,
        name="加茂湖",
        work="オルタネイティヴ",
        priority=3,
    )
    db.session.add(spot)
    db.session.commit()


def q10():
    """id=3 の名前を直す(F2-4 の中身)

    SQL: UPDATE spot SET name = '校舎裏の丘' WHERE id = 3
    手順: id=3 を本体で取り出す → spot.name に新しい名前を入れる → commit
    返すもの: 無し
    """
    stmt = db.select(Spot).filter_by(id=3)
    print("① 注文票:", stmt)

    result = db.session.execute(stmt)
    print("② 実行結果:", result)

    spot = result.scalar()
    print("③ 取り出した:", spot)
    spot.name = "校舎裏の丘"
    db.session.commit()


def q11():
    """id=4 を削除する(F2-5 の中身)

    SQL: DELETE FROM spot WHERE id = 4
    手順: id=4 を本体で取り出す → db.session.delete(spot) → commit
    返すもの: 無し
    """
    return MADA


# 第4部 逆翻訳: Flask を SQL に訳す -------------------------------------------
# SQL を文字列で返す。例: return "SELECT ..."


def q12():
    """次の注文票と同じ結果になる SQL を書く

    db.select(Spot).filter_by(user_id=2)
    """
    return MADA


def q13():
    """次の注文票と同じ結果になる SQL を書く

    db.select(Spot).filter_by(user_id=1, priority=2)
    """
    return MADA


# 第5部 ルート: 全部つなぐ ----------------------------------------------------

# current_user.id の代わり
CURRENT_USER_ID = 1


@app.route("/drill/spots/<int:spot_id>")
def q14(spot_id):
    """詳細ページの1〜4をゼロから書く

    1. URLの番号を受け取る(もう受け取ってる: spot_id)
    2. 「その番号で、自分のスポット」を1件探す(自分 = CURRENT_USER_ID)
    3. 無ければ abort(404)
    4. あれば spot.name を return する
    """
    return MADA


# ここから下は採点。読まなくていい --------------------------------------------

import re
import traceback

from sqlalchemy import Select, event
from sqlalchemy.engine import Engine, Result, Row, ScalarResult


class Unanswered(Exception):
    pass


recording = False
sql_log = []


@event.listens_for(Engine, "before_cursor_execute")
def log_sql(conn, cursor, statement, parameters, context, executemany):
    if recording:
        sql_log.append((statement, parameters))


@event.listens_for(Engine, "commit")
def log_commit(conn):
    if recording:
        sql_log.append(("COMMIT", ()))


def ask(function, *args):
    """答えを実行する。この間に飛んだSQLだけを記録する"""
    global recording
    recording = True
    try:
        result = function(*args)
    finally:
        recording = False
    if result is MADA:
        raise Unanswered
    return result


def seed():
    db.session.remove()
    db.drop_all()
    db.create_all()
    alternative = "オルタネイティヴ"
    db.session.add_all(
        [
            User(id=1, username="kaeriinu", password_hash="-"),
            User(id=2, username="sample", password_hash="-"),
            Spot(id=1, user_id=1, name="真野湾", work=alternative, priority=1),
            Spot(id=2, user_id=1, name="両津港", work=alternative, priority=1),
            Spot(id=3, user_id=1, name="校舎裏の岡", work=alternative, priority=2),
            Spot(id=4, user_id=1, name="萬代橋", work="WAR ENSEMBLE", priority=2),
            Spot(id=5, user_id=2, name="新潟駅", work="WAR ENSEMBLE", priority=1),
            Spot(id=6, user_id=2, name="横浜駅", work=alternative, priority=3),
        ]
    )
    db.session.commit()


def all_spots():
    return db.session.execute(db.select(Spot)).scalars().all()


def name_of(row):
    return row.username if isinstance(row, User) else row.name


def wrong_stage(value):
    if isinstance(value, Select):
        return "注文票のまま。db.session.execute(...) で厨房に渡してない"
    if isinstance(value, Result):
        return "厨房から出たけど皿のまま。.scalars() か .scalar() で取り出してない"
    if isinstance(value, Row):
        return "皿のまま。.first() じゃなく .scalar() で中身を取り出す"
    return None


def check_box(value, expected):
    problem = wrong_stage(value)
    if problem:
        return problem
    if value is None:
        return "None が返ってきた。return を書いたか？"
    if isinstance(value, (Spot, User)):
        return "本体が1件だけ出てる。何件も欲しいときは .scalars()"
    rows = list(value)
    if rows and isinstance(rows[0], Row):
        return "皿のまま並んでる。.all() の前に .scalars() で中身を取り出す"
    names = sorted(name_of(row) for row in rows)
    if names != sorted(expected):
        return f"中身が違う。欲しい: {sorted(expected)} / 出てきた: {names}"
    return None


def check_one(value, expected):
    problem = wrong_stage(value)
    if problem:
        return problem
    if isinstance(value, (ScalarResult, list)):
        return "箱のまま。0件でも箱は None にならない。1件欲しいときは .scalar()"
    if expected is None:
        if value is not None:
            return f"None のはずが「{name_of(value)}」が出てきた。条件を見直せ"
        if not sql_log:
            return "SQL が1回も飛んでない。注文票から書く"
        return None
    if value is None:
        return f"「{expected}」のはずが None。return を書いたか、条件は合ってるか"
    if name_of(value) != expected:
        return f"「{expected}」のはずが「{name_of(value)}」が出てきた"
    return None


def check_names():
    names = ask(q7)
    if not isinstance(names, list):
        return "リストを返す。return names になってるか"
    if names and not isinstance(names[0], str):
        return "名前じゃなく本体を足してる。spot.name を足す"
    expected = ["両津港", "校舎裏の岡", "真野湾", "萬代橋"]
    if sorted(names) != sorted(expected):
        return f"中身が違う。欲しい: {sorted(expected)} / 出てきた: {sorted(names)}"
    return None


def check_owner():
    for user_id, spot_id, expected in [
        (1, 2, "両津港"),
        (1, 999, None),
        (1, 5, None),
        (2, 5, "新潟駅"),
    ]:
        problem = check_one(ask(q8, user_id, spot_id), expected)
        if problem:
            return f"q8({user_id}, {spot_id}): {problem}"
    return None


def check_insert():
    ask(q9)
    if db.session.new:
        return "add はしたけど commit してない。確定しないと保存されない"
    db.session.rollback()
    found = [spot for spot in all_spots() if spot.name == "加茂湖"]
    if len(found) != 1:
        return "加茂湖が保存されてない。Spot(...) を作って add して commit"
    spot = found[0]
    if (spot.user_id, spot.work, spot.priority) != (1, "オルタネイティヴ", 3):
        return "加茂湖は保存されたけど、user_id / work / priority のどれかが違う"
    return None


def check_update():
    ask(q10)
    if db.session.dirty:
        return "書き換えたけど commit してない。確定しないと保存されない"
    db.session.rollback()
    if len(all_spots()) != 6:
        return "行の数が変わった。更新は Spot(...) を新しく作らず、今ある行を書き換える"
    spot = db.session.get(Spot, 3)
    if spot.name != "校舎裏の丘":
        return f"id=3 の名前がまだ「{spot.name}」のまま"
    if sum(spot.name == "校舎裏の丘" for spot in all_spots()) != 1:
        return "id=3 以外の行まで書き換わってる"
    return None


def check_delete():
    ask(q11)
    if db.session.deleted:
        return "delete したけど commit してない。確定しないと消えない"
    db.session.rollback()
    if db.session.get(Spot, 4) is not None:
        return "id=4 がまだ残ってる"
    if len(all_spots()) != 5:
        return "id=4 以外の行まで消えてる"
    return None


def check_sql(function, statement):
    sql = ask(function)
    if not isinstance(sql, str):
        return "SQL を文字列で返す"
    rows = db.session.execute(db.text(sql)).mappings().all()
    if rows and "id" not in rows[0]:
        return "SELECT * で全部の列を取る"
    expected = sorted(spot.id for spot in db.session.execute(statement).scalars())
    found = sorted(row["id"] for row in rows)
    if found != expected:
        return f"結果が違う。欲しいid: {expected} / 出てきたid: {found}"
    ask(db.session.execute, statement)
    return None


def check_route():
    client = app.test_client()
    response = ask(client.get, "/drill/spots/2")
    text = response.get_data(as_text=True)
    if text == MADA:
        raise Unanswered
    if response.status_code != 200 or "両津港" not in text:
        return f"/drill/spots/2 で両津港が出ない(ステータス {response.status_code})"
    if ask(client.get, "/drill/spots/999").status_code != 404:
        return "無い番号で 404 になってない。abort(404) を通ってるか"
    if ask(client.get, "/drill/spots/5").status_code != 404:
        return "他人のスポットが見えてる。持ち主の条件が注文票に無い"
    return None


def show_sql(statement, parameters):
    text = " ".join(statement.split())
    text = re.sub(r"^SELECT .+? FROM ", "SELECT * FROM ", text)
    if parameters:
        return f"{text}  値: {tuple(parameters)}"
    return text


def error_text(error):
    message = str(error).splitlines()[0] if str(error) else ""
    lines = [
        frame.lineno
        for frame in traceback.extract_tb(error.__traceback__)
        if re.fullmatch(r"q\d+", frame.name)
    ]
    place = f"({lines[-1]}行目)" if lines else ""
    return f"{type(error).__name__}: {message} {place}"


MINE = ["真野湾", "両津港", "校舎裏の岡", "萬代橋"]
OTHERS = ["新潟駅", "横浜駅"]

PARTS = [
    (
        "第1部 読む: SQL を Flask に訳す",
        [
            (1, "全部のスポット", lambda: check_box(ask(q1), MINE + OTHERS)),
            (2, "kaeriinu のスポット", lambda: check_box(ask(q2), MINE)),
            (3, "kaeriinu の優先度1", lambda: check_box(ask(q3), MINE[:2])),
            (4, "id=2 のスポット", lambda: check_one(ask(q4), "両津港")),
            (5, "id=999 のスポット", lambda: check_one(ask(q5), None)),
            (6, "sample というユーザー", lambda: check_one(ask(q6), "sample")),
        ],
    ),
    (
        "第2部 箱と本体",
        [
            (7, "名前のリスト", check_names),
            (8, "持ち主つきの1件探し", check_owner),
        ],
    ),
    (
        "第3部 書く: SQL を Flask に訳す",
        [
            (9, "INSERT", check_insert),
            (10, "UPDATE", check_update),
            (11, "DELETE", check_delete),
        ],
    ),
    (
        "第4部 逆翻訳: Flask を SQL に訳す",
        [
            (
                12,
                "user_id=2",
                lambda: check_sql(q12, db.select(Spot).filter_by(user_id=2)),
            ),
            (
                13,
                "user_id=1, priority=2",
                lambda: check_sql(
                    q13, db.select(Spot).filter_by(user_id=1, priority=2)
                ),
            ),
        ],
    ),
    (
        "第5部 ルート: 全部つなぐ",
        [
            (14, "詳細ページ", check_route),
        ],
    ),
]


def grade():
    app.testing = True
    passed = failed = skipped = 0
    with app.app_context():
        for title, questions in PARTS:
            print(f"\n{title}")
            for number, label, check in questions:
                seed()
                sql_log.clear()
                try:
                    problem = check()
                except Unanswered:
                    print(f"Q{number:<3} -  未回答  {label}")
                    skipped += 1
                    continue
                except Exception as error:
                    problem = error_text(error)
                if problem:
                    print(f"Q{number:<3} ×  {label}")
                    print(f"     → {problem}")
                    failed += 1
                else:
                    print(f"Q{number:<3} ○  {label}")
                    passed += 1
                for statement, parameters in sql_log[:4]:
                    print(f"     SQL: {show_sql(statement, parameters)}")
    print(f"\n○ {passed}問 / × {failed}問 / 未回答 {skipped}問")


if __name__ == "__main__":
    grade()
