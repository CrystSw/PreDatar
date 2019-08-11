# ===============================
#  SimpleHTTPServer(Extension)
#  @version 1.0
# -------------------------------
#  @author CrystSw
# ===============================
import http.server
import socketserver
import re
import os

# ------------------------
# パラメータ
# ------------------------
PORT = 8080
Handler = http.server.CGIHTTPRequestHandler

# ------------------------
# アクセスルール(自由に拡張できます)
#
# 【拡張時】
# <好きな変数> = re.compile('^/<任意の正規表現>$')
# deny = [dregex1, <ここに上で指定した変数を指定>]
# ------------------------
# アクセスを禁止するファイル(優先度:低)
dregex1 = re.compile('^/(\w+)\.py$')
deny = [dregex1]
# アクセスを許可するファイル(優先度:高)
aregex1 = re.compile('^/analysis/script/(\w+)\.py$')
allow = [aregex1]

# ------------------------
# クラスの継承によるアクセス制御
# ------------------------
class AccessControlHTTPRequestHandler(Handler):
	# CGIディレクトリの変更
	cgi_directories = ['/analysis/script']
	
	def checkAccess(self):
		# ファイルが存在するか
		if os.path.exists('./'+self.path[1:]) == False:
			return True
		# アクセスルールを検証する
		for delem in deny:
			# 禁止リストに登録されているか
			if delem.match(self.path) != None:
				for aelem in allow:
					# 許可リストに登録されているか
					if aelem.match(self.path) != None:
						# 許可リスト優先に従い，アクセスを許可する
						return True
				# 禁止リストに従い，アクセスを拒否する
				return False
		# 禁止リストに登録されていないため，アクセスを許可する
		return True
	
	def do_GET(self):
		if self.checkAccess() == True:
			super(AccessControlHTTPRequestHandler, self).do_GET()
		else:
			self.send_error(403, "You don't have permission to access")
	
	def do_POST(self):
		if self.checkAccess() == True:
			super(AccessControlHTTPRequestHandler, self).do_POST()
		else:
			self.send_error(403, "You don't have permission to access")			

# ------------------------
# サーバ処理
# ------------------------
with socketserver.ThreadingTCPServer(("", PORT), AccessControlHTTPRequestHandler) as httpd:
	print("serving at port", PORT)
	httpd.serve_forever()