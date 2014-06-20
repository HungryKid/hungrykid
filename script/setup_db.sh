#!/bin/sh

if mysql -uroot -e 'use sandwich' > /dev/null 2>&1; then
    mysql -uroot -e 'DROP DATABASE sandwich'
fi

echo 'create sandwich db ...'
mysql -uroot -e 'CREATE DATABASE sandwich'

echo ''
echo 'setup sandwich db ...'
python script/dbmanager.py

echo 'done.'