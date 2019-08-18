#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cgi
import sys
import io

from collections import OrderedDict
import datetime
import json

# [TODO]: ワンタイムトークンの検証

# POSTデータの受信
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

form = cgi.FieldStorage()

# ファイルの保存
if 'file' in form:
	csvData = form.getfirst('file', '')
	if csvData != '':
		# 現在時刻を文字列で取得
		dt_now = datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')
		# CSVファイルを現在時刻をファイル名として保存
		with open('system/data/csv/'+dt_now+'.csv', 'bw') as fp:
			fp.write(csvData)
		# データリストの読み込み
		with open('system/data/datalist.json', 'r') as fp:
			dataList = json.load(fp, object_pairs_hook=OrderedDict)
		# データリストへ登録
		with open('system/data/datalist.json', 'w') as fp:
			dataList['list'].append(dt_now+'.csv')
			fp.write(json.dumps(dataList))
		