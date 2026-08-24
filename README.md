# flask-hello / ALTERNATIVE

Pythonの学習として始めた Flask アプリ。最小サーバーから始めて、動的ページ・テンプレート・フォーム・画像表示・タブUIと段階的に機能を積み上げ、個人用の進捗トラッカー **ALTERNATIVE** の開発へ発展させている。

> ALTERNATIVE … イラスト制作・プログラム練習・資格勉強の進捗を、モチベを上げつつ楽しく見返す個人用トラッカー。名前は「マブラヴ オルタネイティヴ」由来(積み重ねて、より良い自分へ)。

## 主な機能(ルート一覧)

| URL | 内容 |
|-----|------|
| `/` | トップ(Hello) |
| `/time` | 現在時刻を表示(動的ページ・タイムゾーン対応) |
| `/calc` | 足し算電卓(フォーム入力→計算) |
| `/greet` | 名前を入力するとあいさつを返す(GET/POST) |
| `/gallery` | イラストギャラリー(クリックで拡大=ライトボックス) |
| `/works` | 作品紹介(タブ切り替え) |
| `/alternative` | 進捗トラッカー ALTERNATIVE(5段階タブ+タグ+リンク) |
| `/study` | 基本情報(FE)の週間プログレス(チェック状態を保存) |
| `/network` | ネットワーク用語まとめ(FE ネットワーク分野 全9章・復習チェック付き) |

## 使用技術

- **Python 3 / Flask** — サーバー・ルーティング
- **Jinja2** — HTMLテンプレート(`templates/`)
- **HTML / CSS / JavaScript** — 画面・タブ切り替え・ライトボックス
- 静的ファイルは `static/` 配下

## ローカルでの起動方法

```bash
# 仮想環境を作成して有効化(初回のみ)
python -m venv venv
venv\Scripts\activate        # Windows

# Flask をインストール
pip install flask

# サーバー起動
python app.py
```

起動後、ブラウザで `http://localhost:5000` を開く。

## 今後の予定(ロードマップ)

- [ ] データ保存(localStorage → Flask + SQLite への移行)
- [ ] 作品の登録・編集・削除(CRUD)
- [ ] ログイン機能
- [ ] レスポンシブ対応・テスト追加

---

*Pythonを学びながら「作りたいもの」を形にしていく記録。*
