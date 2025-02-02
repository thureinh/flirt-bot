# FlirtBot

FlirtBot is an automated bot that interacts with users on various platforms using OpenAI's API. It uses Selenium for web automation and can remember previous messages to provide a more personalized experience.

## Features
- Automated interactions using OpenAI's API
- Web automation with Selenium
- Memorizes previous messages for personalized responses

## Installation

### Prerequisites
- Python 3.x
- Google Chrome
- ChromeDriver

### Steps

1. **Clone the repository:**
    ```sh
    git clone https://github.com/thureinh/flirt-bot.git
    cd FlirtBot
    ```

2. **Create a virtual environment:**
    ```sh
    python -m venv venv
    ```

3. **Activate the virtual environment:**
    - On Windows:
        ```sh
        venv\Scripts\activate
        ```
    - On macOS/Linux:
        ```sh
        source venv/bin/activate
        ```

4. **Install the required libraries:**
    ```sh
    pip install -r requirements.txt
    ```

5. **Download and install ChromeDriver:**
    - Download ChromeDriver from [here](https://sites.google.com/a/chromium.org/chromedriver/downloads).
    - Extract the downloaded file and place it in a directory included in your system's PATH.

6. **Set up environment variables:**
    - Create a [.env](http://_vscodecontentref_/0) file in the root directory of the project.
    - Add your OpenAI API key to the [.env](http://_vscodecontentref_/1) file:
        ```
        API_KEY=your_openai_api_key
        ```

## Usage

To run the bot, execute the following command:
```sh
python FlirtBot.py

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