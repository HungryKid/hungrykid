#!/bin/sh

if mysql -uroot -e 'use hungrykid' > /dev/null 2>&1; then
    mysql -uroot -e 'DROP DATABASE hungrykid'
fi

echo 'create hungrykid db ...'
mysql -uroot -e 'CREATE DATABASE hungrykid'

echo ''
echo 'setup hungrykid db ...'
python manager.py

echo ''
echo 'done.'
