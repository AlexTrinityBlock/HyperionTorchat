# Python program to implement server side of chat room.
import socket
import select
import sys
from _thread import *

#偵聽port
Port = 9052

#使用者清單
list_of_clients = []

#歡迎詞
welcome =""

#客戶資料結構
class Client:
	def __init__(self):
		self.conn=None
		self.username=None
		self.key=None

#清除換行符與空白
def cleanString(username):
	username.split()
	username.strip()
	username=username.replace("\n","")
	return username

#找尋用戶
def findUserByName(name):
	for client in list_of_clients:
		if client.username==name:
			return client

#找尋用戶在list中的索引位置
def findUserIndexByName(name):
	for index,client in enumerate(list_of_clients):
		if client.username==name:
			return index

#用戶清單
def userList():
	print("更新用戶列表\n-------")
	for client in list_of_clients:
			print(client.username)
	print("\n")

#連線關閉器
def connect_close(username):
	print("用戶關閉連線嘗試關閉連線\n")
	client=findUserByName(username)
	client.conn.close()
	remove(username)

#名稱存在
def nameIsUsed(username):
	for client in list_of_clients:
		if client.username==username:
			return True
	return False

#取得歡迎詞
def getWelcome():
	with open('/app/welcome','r') as file:
		text = file.read()
	return text

#客戶端執行緒函數
def clientthread(conn, addr):
	try:
		conn.send(welcome.encode("UTF-8"))
		print("用戶執行緒建立成功，開始回應 \n")
		conn.send("請告訴我你的名字（至少三個字）\n".encode("UTF-8"))
		username=(conn.recv(2048)).decode("UTF-8")
		username=cleanString(username)

		#禁止重複名稱
		while nameIsUsed(username):
			conn.send("名字重複了，重取一個吧^_^\n".encode("UTF-8"))
			username=(conn.recv(2048)).decode("UTF-8")
			username=cleanString(username)

		#禁止非法名稱
		while len(username) < 3 :
			conn.send("名字至少三個字唷，重取一個吧^_^\n".encode("UTF-8"))
			conn.send("請告訴我你的名字\n".encode("UTF-8"))
			username=(conn.recv(2048)).decode("UTF-8")
			username=cleanString(username)
		
		message="你的名字是 "+username+"一起聊天吧～～ ^_^ \n"
		conn.send(message.encode("UTF-8"))
		client = Client()
		client.username=username
		client.conn=conn
		list_of_clients.append(client)
		userList()

	except:
		print("用戶啟動時中斷 \n")
		conn.close()

	#用戶主迴圈
	while True:
			try:
				message = (conn.recv(2048)).decode("UTF-8")
				if message:
					print ("<"+username+">:"+message)
					message_to_send = "<"+username+">:"+message
					broadcast(message_to_send,username)
				else:
					print(username,"用戶主動離線")
					connect_close(username)
					break
			except:
				pass

#客戶端廣播函數
def broadcast(message, username):
	for client in list_of_clients:
		if client.username != username:
			while True:
				try:
					client.conn.send(message.encode("UTF-8"))
					break
				except:
					pass


#從清單中移除
def remove(username):
	index=findUserIndexByName(username)
	print("嘗試從維護連線清單刪除用戶\n",username)
	del list_of_clients[index]


#主函數
if __name__ == '__main__':
	
	#載入歡迎詞
	print("載入歡迎詞")
	welcome=getWelcome()

	#設置連線
	print("設置socket連線參數")
	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	server.bind(("0.0.0.0", Port))
	server.listen(100)
	while True:
		conn, addr = server.accept()
		print ("遠端主機嘗試連線伺服器\n")
		#建立子執行緒
		start_new_thread(clientthread,(conn,addr))	

	conn.close()
	server.close()

