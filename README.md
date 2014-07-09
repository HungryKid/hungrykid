HungryKid
====================

[![wercker status](https://app.wercker.com/status/c8f03971061aefe06f7e5db2b39cf274/m "wercker status")](https://app.wercker.com/project/bykey/c8f03971061aefe06f7e5db2b39cf274)

![Puppy hungry "Big Bone" by Jack Fiallos, on Flickr](https://c2.staticflickr.com/2/1070/540747396_5542b42cca_m.jpg "Puppy hungry "Big Bone" by Jack Fiallos, on Flickr")

How to setup local development environment
---------------------------------------------

1. Preparations in advance
    * homebrew  
        ```
        # install homebrew on mac os
        $ ruby -e "$(curl -fsSL https://raw.github.com/mxcl/homebrew/go/install)"

        ```
    * python - pyenv, virtualenv, pip
        ```
        # install pyenv
        $ brew install pyenv
        $ brew install pyenv-virtualenv
        $ echo 'export PYENV_ROOT="${HOME}/.pyenv"' >> ~/.zshrc
        $ echo 'if [ -d "${PYENV_ROOT}" ]; then' >> ~/.zshrc
        $ echo '    export PATH=${PYENV_ROOT}/bin:$PATH' >> ~/.zshrc
        $ echo '    eval "$(pyenv init -)"' >> ~/.zshrc
        $ echo 'fi' >> ~/.zshrc
        $ exec $SHELL -l

        # configure pyenv
        $ pyenv install 2.7.7
        $ pyenv virtualenv 2.7.7 hungryenv
        $ cd <hungrykid directory>
        $ pyenv local hungryenv
        ```
    * perl - plenv(w/ perl-build), cpanm, carton, daiku, cinnamon
        ```
        # install plenv w/ perl-build
        $ git clone git://github.com/tokuhirom/plenv.git ~/.plenv
        $ git clone git://github.com/tokuhirom/Perl-Build.git ~/.plenv/plugins/perl-build/
        $ echo 'export PLENV_ROOT="${HOME}/.plenv"' >> ~/.zshrc
        $ echo 'if [ -d "${PLENV_ROOT}" ]; then' >> ~/.zshrc
        $ echo '    export PATH=${PLENV_ROOT}/bin:$PATH' >> ~/.zshrc
        $ echo '    eval "$(plenv init -)"' >> ~/.zshrc
        $ echo 'fi' >> ~/.zshrc
        $ exec $SHELL -l

        # install perl
        $ plenv available
        $ plenv install 5.20.0 —-as 5.20
        $ plenv global 5.20
        $ plenv rehash
        $ plenv versions

        # install cpanm
        $ plenv install-cpanm

        # install daiku, cinnamon
        $ plenv exec cpanm Daiku Cinnamon
        ```
2. Clone this repository

    ```
    $ git clone git@github.com:HungryKid/hungrykid.git
    $ cd hungrykid
    ```
3. Install python module dependency

    ```
    $ daiku pip:install
    ```

4. Setup DB

    ```
    $ daiku db:setup
    ```

5. Setup host

    ```
    $ sudo vi /etc/hosts

    ...

    127.0.0.1 hungrykid.me
    ```

How to start local server
---------------------------------------------

```
$ daiku server:start
```

* Update dependency
    ```
    $ daiku pip:freeze

    ```

Daiku commands
------------------------------------------

```
$ daiku -T
daiku server:start    # サーバ起動
daiku db:setup        # データベースのセットアップ
daiku batch:crawl     # ショップデータのクローリング
daiku venv:init       # プロジェクト用Python仮想環境の作成
daiku pip:install     # （Python）依存モジュールのインストール
daiku pip:update      # （Python）依存モジュールのアップデート
daiku pip:freeze      # （Python）依存モジュールの凍結
daiku carton:install  # （Perl）依存モジュールのインストール
daiku carton:update   # （Perl）依存モジュールのアップデート
```
