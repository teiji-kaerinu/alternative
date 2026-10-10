# よく使うコマンド

このプロジェクトで実際に使うものだけを置く。使って覚えたものは、ここに1行ずつ足していく。

コマンドはすべて **VS Codeのターミナル（`flask-hello` の場所）** で打つ。
一度打ったコマンドは、ターミナルで **↑キー** を押せば呼び戻せる。

---

## サーバーを起動する

| やりたいこと | コマンド / キー |
|---|---|
| 起動（保存すると自動で再起動） | `venv\Scripts\flask run --debug` |
| 止める | `Ctrl+C` |
| 起動（デバッガ・ブレークポイントを使う） | 「実行とデバッグ」で **Flask** を選んで `F5` |
| デバッガを再起動 | `Ctrl+Shift+F5`（**app.pyを直したら必ず押す**。自動では再起動しない） |
| デバッガを止める | `Shift+F5` |

- 起動したら `http://127.0.0.1:5000/spots` を開く
- `F5` の設定ファイル（`.vscode/launch.json`）はgitに上がらない。別のPCでは作り直す
- `Address already in use` が出たら、前のサーバーが動いたまま。止めてから起動し直す

## shellでDBを触る

```
venv\Scripts\flask shell
```

```python
from app import db, Spot          # 最初に必ずimportする
spot = Spot(name="...", work="...", priority=1)
db.session.add(spot)
db.session.commit()
db.session.rollback()             # commitでエラーが出たら、まずこれで片付ける
exit()                            # shellから出る
```

```python
from werkzeug.security import generate_password_hash,check_password_hash
                                  #ハッシュ関数に通すため、暗号化複合化のimport
```

## DBの形を変える（モデルを書き換えたとき）

いつもこの順番。**migrateとupgradeの間に、生成されたファイルを必ず読む。**

| 順 | コマンド | 何が起きるか |
|---|---|---|
| 1 | `venv\Scripts\flask db migrate -m "何をしたか"` | `migrations/versions/` に変更の設計図ができる |
| 2 | （ファイルを開いて読む） | 意図した列・制約が入っているか確かめる |
| 3 | `venv\Scripts\flask db upgrade` | 設計図どおりにDBを書き換える |

| ほかに | コマンド |
|---|---|
| 1つ前の形に戻す | `venv\Scripts\flask db downgrade` |
| 今どの版か見る | `venv\Scripts\flask db current` |

DBの中身は、VS Codeで `instance/alternative.db` を開く（SQLite Viewer）。

## アプリの中身を確かめる

| やりたいこと | コマンド |
|---|---|
| ルート（URL）の一覧を見る | `venv\Scripts\flask routes` |
| flaskのコマンド一覧を見る | `venv\Scripts\flask --help` |
| migrate系のコマンド一覧を見る | `venv\Scripts\flask db --help` |

## git（家PCと会社PCを行き来する）

| いつ | コマンド |
|---|---|
| **作業を始める前に必ず** | `git pull` |
| 何が変わったか見る | `git status` |
| 作業が終わったら | VS Codeの「ソース管理」でメッセージを書いて `Ctrl+Enter` → 同期（push） |

## パッケージ（めったに使わない）

| いつ | コマンド |
|---|---|
| 新しいPCで環境を作る | `python -m venv venv` → `venv\Scripts\pip install -r requirements.txt` |
| パッケージを足したあと | `venv\Scripts\pip freeze \| Out-File -Encoding utf8 requirements.txt` |

PowerShellで `>` を使って書き出すと文字コードがUTF-16になって崩れる。だから `Out-File -Encoding utf8` を使う。

## VS Code

| やりたいこと | キー |
|---|---|
| **迷ったらこれ（全機能を検索できる）** | `Ctrl+Shift+P` |
| Markdownを横にプレビュー | `Ctrl+K` → `V` |
| Markdownをプレビューだけ表示 | `Ctrl+Shift+V` |
| ターミナルの開閉 | `Ctrl+@` |
| ファイルを名前で開く | `Ctrl+P` |
