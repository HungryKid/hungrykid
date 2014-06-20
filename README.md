sandwich
====================

![NUCOA MARGERINE, KIDS ON SWING by George Eastman House, on Flickr](https://farm4.staticflickr.com/3113/3122866921_5384bfae46_m.jpg "NUCOA MARGERINE, KIDS ON SWING by George Eastman House, on Flickr")

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
        $ git clone git://github.com/yyuu/pyenv.git ~/.pyenv
        $ echo 'export PYENV_ROOT="${HOME}/.pyenv"' >> ~/.zshrc
        $ echo 'if [ -d "${PYENV_ROOT}" ]; then' >> ~/.zshrc
        $ echo '    export PATH=${PYENV_ROOT}/bin:$PATH' >> ~/.zshrc
        $ echo '    eval "$(pyenv init -)"' >> ~/.zshrc
        $ echo 'fi' >> ~/.zshrc
        $ exec $SHELL -l

        # install pyenv-virtualenv
        $ git clone git://github.com/yyuu/pyenv-virtualenv.git  ~/.pyenv/plugins/pyenv-virtualenv

        # install pyenv-pip-rehash
        $ git clone git://github.com/yyuu/pyenv-pip-rehash.git ~/.pyenv/plugins/pyenv-pip-rehash

        # install python
        $ pyenv install -l
        $ pyenv install 2.7.6
        $ pyenv global 2.7.6
        $ pyenv rehash
        $ pyenv versions
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
        $ plenv install 5.18.2 —-as 5.18
        $ plenv global 5.18
        $ plenv rehash
        $ plenv versions

        # install cpanm
        $ plenv install-cpanm

        # install daiku, cinnamon
        $ plenv exec cpanm Daiku Cinnamon
        ```
2. Clone this repository

    ```
    $ git clone git@github.com:wata/sandwich.git
    $ cd sandwich
    ```
3. Install python module dependency

    ```
    $ pip install -r requirements.txt
    ```

4. Setup DB

    ```
    $ daiku db:setup
    ```

5. Setup host

    ```
    $ sudo vi /etc/hosts

    ...

    127.0.0.1 sandwich.com
    ```

How to start local server
---------------------------------------------

```
$ python index.py
```

* Update dependency
    ```
    $ pip freeze > requirements.txt

    ```
