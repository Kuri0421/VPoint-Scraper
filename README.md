# VPoint Scraper

[![Python](https://custom-icon-badges.herokuapp.com/badge/Python-3572A5.svg?logo=Python&logoColor=white)]()
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

## これは何🧐

三井住友カード株式会社が提供するポイントプログラム「Vポイント」のポイント履歴をスクレイピングするためのプログラムです。

指定した期間のポイント履歴を取得し、CSVファイルに出力します。

CSVファイルなので。Excel等で煮るなり焼くなり好きなようにしてください。


## 目次📚
- [前提条件🔍](#前提条件🔍)
- [導入🔽](#導入🔽)
- [使い方🚀](#使い方🚀)
- [お願い🙇‍♂️](#お願い🙇‍♂️)
- [ライセンス📜](#ライセンス📜)

## 前提条件🔍
- 三井住友カードのVPASS会員であること
- Chromeブラウザがインストールされていること
- Python 3.8以上 (Windowsの場合はexeファイルを使用するため不要)
- 依存パッケージ (requirements.txt参照)(Windowsの場合はexeファイルを使用するため不要)

## 導入🔽
PythonのスクリプトをPyinstallerでexe化したものを [Releases](https://github.com/Kuri0421/VPointScraper/releases/) にて配布しています。
> [!WARNING]
> Pyinstallerでexe化したのでWindows Defender等のセキュリティソフトによってはトロイの木馬等の判定が出るかもしれません。その場合は無視して実行してください。
信用できないなら使わないでください。

動作確認はしていませんが、LinuxやMacOSの場合は、Pythonのスクリプトをそのまま実行してください。
多分動くと思います。多分。

事前にPythonと依存パッケージをインストールしてください。

```bash
pip install -r requirements.txt
```

## 使い方🚀

### Windowsの場合
Windowsの場合は、コマンドプロンプトやPowerShellを開いて、以下のコマンドを実行してください。
```bash
VPointScraper.exe -s [取得を開始する年月] -e [取得を終了する年月]
```
> [!WARNING]
> CSVファイルを出力するため管理者権限が必要です。管理者権限で実行してください。


#### 例 (2019年1月から2024年2月までのポイント履歴を取得する場合)
```bash
VPointScraper.exe -s 2019012 -e 202402
```

### LinuxやMacOSの場合
```bash
python main.py -s [取得を開始する年月] -e [取得を終了する年月]
```
#### 例 (2019年1月から2024年2月までのポイント履歴を取得する場合)
```bash
python main.py -s 2019012 -e 202402
```

### ログイン処理
三井住友カードのログイン画面が表示されるので、ログインしてください。
60秒以内にログインしないとタイムアウトします。

ログイン後にポイント履歴の取得が開始されます。

> [!NOTE]
> ログイン情報は保存されません。毎回ログインが必要です。
自動入力もできません。手動で入力してください。
引数や環境変数、構成ファイル等でログイン情報を保存させることも考えましたが、セキュリティ的にけしからんと思ったのでやめました。
## お願い🙇‍♂️

作者はPythonを中途半端に学んでしまっているため、実質初心者です。このプログラムには多くの問題があるかもしれません。もしもっといいコードの書き方や改善点があれば、ぜひ優しく教えてください。

## ライセンス📜

このプロジェクトのライセンスは[MIT License](LICENSE)です。

This project is licensed under the [MIT License](LICENSE).

