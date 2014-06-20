#!/usr/bin/env python
# coding:utf-8

import sys
import os
cur_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(cur_dir, '../'))

from __init__ import engine
from user import metadata, users

metadata.create_all(engine)