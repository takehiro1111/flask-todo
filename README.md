# pipenv 環境構築（mac）

Macで`pipenv`を使用してPython環境を構築する手順は以下の通りです。`pipenv`は、Pythonのパッケージ管理と仮想環境を統合して扱うツールです。

### 1. Homebrewのインストール (もしまだインストールしていない場合)

Homebrewは、macOS用のパッケージマネージャーです。まず、Homebrewがインストールされていない場合は、以下のコマンドをターミナルで実行してインストールします。

```bash
/bin/bash -c "$(curl -fsSL <https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh>)"

```

### 2. Pipenvのインストール

Homebrewを使って`pipenv`をインストールします。ターミナルで以下のコマンドを実行します。

```bash
brew install pipenv

```

### 3. プロジェクトディレクトリの作成

プロジェクトのためのディレクトリを作成し、その中に移動します。

※ディレクトリ名は任意でOKです。

```bash
mkdir flask-todo-project
cd flask-todo-project

```

### 4. Pipenv環境のセットアップ

`pipenv`を使ってPythonの仮想環境を作成します。この際、使用するPythonのバージョンを指定できます。例えば、Python 3.12を使用する場合は以下のようにします。

```bash
pipenv --python 3.12

```

これにより、指定されたバージョンのPython仮想環境が作成されます。インストールが成功すると、`Pipfile`というファイルがプロジェクトに作成され、環境設定が管理されます。

### 6. 仮想環境のアクティベート

仮想環境をアクティベートするには、以下のコマンドを実行します。

```bash
pipenv shell

```

これで、仮想環境内でPythonのスクリプトやコマンドを実行できるようになります。

### 8. 仮想環境の終了

仮想環境を終了するには、以下のコマンドでシェルを抜けます。

```bash
exit

```

### 5. Flaskのインストール
```bash
mkdir flask-todo-project
cd flask-todo-project

```

```bash
pipenv shell
pipenv install Flask
exit
```
