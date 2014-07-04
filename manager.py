#!/usr/bin/env python
# coding:utf-8

from hungrykid import engine
from hungrykid.models.user import metadata
metadata.create_all(engine)

from hungrykid.models.shop import metadata
metadata.create_all(engine)
