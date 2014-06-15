# coding:utf-8

import pygame.mixer
import time
import commands
import re
import csv
import glob
import random

pygame.mixer.init()

def update():
	#arpテーブルをアップデートして出力
	com = "ping -c 3 133.101.51.255"
	commands.getoutput(com)
	out = commands.getoutput("arp -a")
	print out
	return out.splitlines()

def main():
	list=[]
	iplist = set([])
	beforeArray = update()
	cnt = 0
	maclist = []
	maclistCSV = csv.reader(file("Mac.conf",'r'))
	for row in maclistCSV:
		maclist.append(row)
	files = glob.glob('voice/random/*.wav')
	
	#main loop
	while True:
		print cnt
		#reset ip lidt
		if cnt == 500:
			iplist = set([])
			cnt = 0
		#delete unknown IP
		if cnt%50==0:
			for line in list:
				if '?' in line:
					ip=line.split()[1].replace("(","").replace(")","")
					print commands.getoutput("arp -d "+ip)
		#delete week connect
		for s in iplist:
			out = commands.getoutput("ping -c 1 -W 4 "+s)
			m = re.search("100%",out)
			if m :
				commands.getoutput("sudo arp -d " + s)
		list = update()
		
		
		for s1 in list:
		       	for s2 in beforeArray:
		       		if s1 == s2 :
		       			break
			else:	
				#出力情報の整形		
				print re.split('\ *ether\ *|\ +',s1)
				mac = re.split('\ *ether\ *|\ +',s1)[3]
				ip=s1.split()[1].replace("(","").replace(")","")
				splitedIP=re.split('\.',ip)
				united=""
				#外からの接続かどうか判定
				for decimal in splitedIP:
					binary = format(int(decimal),'b')
					united=united+str.format('{0:08d}', int(binary))
				match = re.search('1000010101100101001100[01]{10,10}',united)
				#内からの接続
				if match:
					print "[ACCEPTED] host:"+s1.split()[0]+" IP:"+ip+" mac:"+str(mac)
					iplist.add(s1.split()[0])
				#外からの接続
				else:
					print "[REJECTED] host:"+s1.split()[0]+" IP:"+ip+" mac:"+str(mac)
					break
				#再生
				for member in maclist:
       					if member[0] == mac:
						print member[1]
						try:
							pygame.mixer.music.load(member[2])
						except:
							print "wav load error"
						break
				else:
					length=len(files)
					rand=random.randrange(0,length-1)
					try:
						pygame.mixer.music.load(files[rand])
					except:
						print "wav load error"
				pygame.mixer.music.play(1)
		beforeArray = list
			#待機秒数
       		time.sleep(5)
		cnt+=1
									
if __name__ == '__main__':
    main()
