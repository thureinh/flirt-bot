# フリートボット

フリートボットは、OpenAIのAPIを使用してさまざまなプラットフォームでユーザーと対話する自動ボットです。Seleniumを使用してWeb自動化を行い、以前のメッセージを記憶してよりパーソナライズされた体験を提供します。

## 特徴
- OpenAIのAPIを使用した自動対話
- SeleniumによるWeb自動化
- 以前のメッセージを記憶してパーソナライズされた応答を提供

## インストール

### 前提条件
- Python 3.x
- Google Chrome
- ChromeDriver

### 手順

1. **リポジトリをクローンする:**
    ```sh
    git clone https://github.com/thureinh/flirt-bot.git
    cd FlirtBot
    ```

2. **仮想環境を作成する:**
    ```sh
    python -m venv venv
    ```

3. **仮想環境を有効にする:**
    - Windowsの場合:
        ```sh
        venv\Scripts\activate
        ```
    - macOS/Linuxの場合:
        ```sh
        source venv/bin/activate
        ```

4. **必要なライブラリをインストールする:**
    ```sh
    pip install -r requirements.txt
    ```

5. **ChromeDriverをダウンロードしてインストールする:**
    - [こちら](https://sites.google.com/a/chromium.org/chromedriver/downloads)からChromeDriverをダウンロードします。
    - ダウンロードしたファイルを解凍し、システムのPATHに含まれるディレクトリに配置します。

6. **環境変数を設定する:**
    - プロジェクトのルートディレクトリに [.env](http://_vscodecontentref_/8) ファイルを作成します。
    - OpenAI APIキーを [.env](http://_vscodecontentref_/9) ファイルに追加します:
        ```
        API_KEY=your_openai_api_key
        ```

## 使用方法

ボットを実行するには、次のコマンドを実行します:
```sh
python FlirtBot.py
```