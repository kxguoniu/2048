# -*- coding: utf-8 -*-
import wx
import time
import datetime
import random
from ctypes import CDLL

SIDE = 4
ID_MENU_NEW = wx.NewId()
ID_MENU_UP = wx.NewId()
ID_MENU_DOWN = wx.NewId()
ID_MENU_EXIT = wx.NewId()
ID_MENU_ABOUT = wx.NewId()
ID_MENU_LOOK = wx.NewId()
Gamemusic = 0
kaixin = []
time_flag = True
play_flag = True

class Example(wx.Frame):
	def __init__(self,*args, **kwargs):
		wx.Frame.__init__(self,None,-1,style=wx.DEFAULT_FRAME_STYLE^wx.MAXIMIZE_BOX^wx.RESIZE_BORDER)
		self.InitUI()

	def InitUI(self):
		try:
			self.CreateMenuBar()
			self.CreateMain()
			self.CreateStatus()
			self.Bind(wx.EVT_KEY_DOWN,self.OnKeyDown)
			self.Bind(wx.EVT_CLOSE, self.OnClose)
			self.SetBackgroundColour('#BBADA0')
			self.SetSize((480,550))
			self.SetTitle('2048')
			self.setIcon()
			self.Center()
			self.Show()
		except Exception as e:
			with open('error.log','w') as f:
				f.write(repr(e))

	def CreateMenuBar(self):
		self.mb = wx.MenuBar()
		self.GameMenu = wx.Menu()
		self.GameMenu.Append(ID_MENU_NEW, u'新游戏(N)\t\tF2')
		self.GameMenu.AppendSeparator()
		self.GameMenu.Append(ID_MENU_UP, u'上一步(U)\tF3')
		self.GameMenu.Append(ID_MENU_DOWN, u'下一步(D)\tF4')
		self.GameMenu.AppendSeparator()
		self.GameMenu.Append(ID_MENU_EXIT, u'退出(X)')
		self.HelpMenu = wx.Menu()
		self.HelpMenu.Append(ID_MENU_ABOUT, u'关于2048(V)\tF1')
		self.mb.Append(self.GameMenu,u'&游戏(G)')
		self.mb.Append(self.HelpMenu,u'&帮助(H)')
		self.SetMenuBar(self.mb)
		self.Bind(wx.EVT_PAINT, self.OnPaint)
		self.Bind(wx.EVT_MENU, self.OnNew, id=ID_MENU_NEW)
		self.Bind(wx.EVT_MENU, self.OnUp, id=ID_MENU_UP)
		self.Bind(wx.EVT_MENU, self.OnDown, id=ID_MENU_DOWN)
		self.Bind(wx.EVT_MENU, self.OnExit, id=ID_MENU_EXIT)
		self.Bind(wx.EVT_MENU, self.OnAbout, id=ID_MENU_ABOUT)

	def insert(self,data):
		getZeroIndex = []
		for i in range(4):
			for j in range(4):
				if data[i][j] == 0:
					getZeroIndex.append([i, j])
		if getZeroIndex != []:
			randomZeroIndex = random.choice(getZeroIndex)
			data[randomZeroIndex[0]][randomZeroIndex[1]] = random.choice([2,4])
		return data

	def CreateMain(self):
		self.data_left = []
		self.data_right = []
		self.show_time = [u"时间: ","0"]
		self.show_list = [u"得分: ","0",u"步数: ","0"]
		self.colors = {0:'#CCC0B4',2:'#EEE4DA',4:'#EDE0C8',8:'#F2B179',16:'#EC8D54',32:'#F67C5F',64:'#EA5937',128:'#804000',256:'#F1D04B',512:'#E4C02A',1024:'#EE7600',2048:'#D5A500',4096:'#E4C02A',8192:'#804000',16384:'#EA5937',32768:'#EE7600'}
		self.scFont = wx.Font(36,wx.SWISS,wx.NORMAL,wx.BOLD,faceName=u"Roboto")
		self.data = [[0 for i in range(4)] for i in range(4)]
		self.data = self.insert(self.data)
		self.data = self.insert(self.data)
		self.mm = CDLL("mm.dll")

	def OnPaint(self, event): self.ShowWindow()

	def ShowWindow(self):
		dc = wx.ClientDC(self)
		dc.SetFont(self.scFont)
		for row in range(4):
			for col in range(4):
				value = self.data[row][col]
				color = self.colors[value]
				if value==2 or value ==4:
					dc.SetTextForeground('#776e65')
				else:
					dc.SetTextForeground('#FFFFFF')
				dc.SetBrush(wx.Brush(color))
				dc.SetPen(wx.Pen(color))
				dc.DrawRoundedRectangle(15+col*115,15+row*115,100,100,2)
				size = dc.GetTextExtent(str(value))
				while size[0]>75:
					self.scFont = wx.Font(self.scFont.GetPointSize()*9/10,wx.SWISS,wx.NORMAL,wx.BOLD,faceName=u"Roboto")
					dc.SetFont(self.scFont)
					size = dc.GetTextExtent(str(value))
				if value!=0: dc.DrawText(str(value),15+col*115+(100-size[0])/2,15+row*115+(100-size[1])/2)
		self.ShowStatus(self.status)

	def CreateStatus(self):
		self.status = self.CreateStatusBar()
		self.status.SetFieldsCount(4)
		self.ShowStatus(self.status)

	def ShowStatus(self,status):
		self.status = status
		self.status.SetStatusText(self.show_time[0] + str(self.show_time[1]),1)
		self.status.SetStatusText(self.show_list[0] + str(self.show_list[1]),2)
		self.status.SetStatusText(self.show_list[2] + str(self.show_list[3]),3)

	def ShowTime(self):
		global start_time
		global time_flag
		if time_flag:
			start_time = datetime.datetime.now()
			time_flag = False
		end_time = datetime.datetime.now()
		run_time = (end_time - start_time)
		self.show_time[1] = str(run_time.seconds)
		wx.CallLater(1000, self.ShowTime)
		self.ShowStatus(self.status)

	def OnKeyDown(self,event):
		self.ShowTime()
		if self.Over(self.data):
			self.mm.AsyncPlaySoundW(u"musics/over.wav")
			message = u"           不好意思，游戏结束。下次走运！    \n\n        游戏时间：%s秒                    游戏得分：%s分"%(self.show_time[1],self.show_list[1])
			dial  = wx.MessageBox(message, u'游戏失败', wx.YES_NO | wx.NO_DEFAULT, self)
			if dial == wx.YES:
				self.Destroy()
			else:
				self.NewGame()
		keyCode = event.GetKeyCode()
		if keyCode==wx.WXK_UP:
			self.data = self.Move_Up(self.data)
			self.Move_Key(self.data)
		elif keyCode==wx.WXK_DOWN:
			self.data = self.Move_Down(self.data)
			self.Move_Key(self.data)
		elif keyCode==wx.WXK_LEFT:
			self.data = self.Move_Left(self.data)
			self.Move_Key(self.data)
		elif keyCode==wx.WXK_RIGHT:
			self.data = self.Move_Right(self.data)
			self.Move_Key(self.data)
		else:
			self.GameKey(keyCode,event)

	def GameKey(Code,event):
		if Code==wx.WXK_F1:
			self.OnAbout(event)
		elif Code==wx.WXK_F2:
			self.OnNew(event)
		elif Code==wx.WXK_F3:
			self.OnUp(event)
		elif Code==wx.WXK_F4:
			self.OnDown(event)

	def Move_Key(self,data):
		global Gamemusic
		self.mm.AsyncPlaySoundW(u"musics\\move.wav")
		if Gamemusic: self.mm.AsyncPlaySoundW(u"musics\\merge.wav")
		Gamemusic = 0
		self.data = data
		Number = 1 + int(self.show_list[3])
		self.show_list[3] = str(Number)
		self.data = self.insert(self.data)
		data_list = []
		self.data_left.append(list([self.data,self.show_list]))
		del self.data_right[0:]
		self.ShowWindow()
		if play_flag:
			self.GameWin()

	def Over(self,matrix):
		for item_list in matrix:
			if 0 in item_list:
				return False
		for i in range(4):
			for j in range(4):
				if i < 4 - 1:
					if matrix[i][j] == matrix[i+1][j]:
						return False
				if j < 4 - 1:
					if matrix[i][j] == matrix[i][j+1]:
						return False
		return True

	def GameAppend(self,Name,Data,Show_list):
		data_list = []
		if Name == 1:
			data_list.append(list([Data,Show_list]))
			return data_list
		elif Name == 2:
			data_list.append(list([Data,Show_list]))
			return data_list

	def Move_Right(self,matrix):
		right_list = []
		for item_list in matrix:
			right_list.append(self.handle_list_item_right(item_list))
		return right_list

	def Move_Left(self,matrix):
		right_list = []
		for item_list in matrix:
			right_list.append(self.handle_list_item_left(item_list))
		return right_list

	def Move_Down(self,matrix):
		down_list = []
		config_list = [0, 0, 1, matrix]
		matrix = self.inversion_data_list(config_list)
		for item_list in matrix:
			down_list.append(self.handle_list_item_right(item_list))
		config_list = [0, 0, 1, down_list]
		down_list = self.inversion_data_list(config_list)
		return down_list

	def Move_Up(self,matrix):
		up_list = []
		config_list = [0, 0, 1, matrix]
		matrix = self.inversion_data_list(config_list)
		for item_list in matrix:
			up_list.append(self.handle_list_item_left(item_list))
		config_list = [0, 0, 1, up_list]
		up_list = self.inversion_data_list(config_list)
		return up_list

	def handle_list_item_right(self,my_list):
		list_0 = self.del_item_0(my_list)
		list_0 = self.add_same_number(list_0, 'right')
		list_1 = self.del_item_0(list_0)
		list_1 = self.add_item_0(list_1, 'right')
		return list_1

	def handle_list_item_left(self,my_list):
		list_0 = self.del_item_0(my_list)
		list_0 = self.add_same_number(list_0, 'left')
		list_1 = self.del_item_0(list_0)
		list_1 = self.add_item_0(list_1, 'left')
		return list_1

	def del_item_0(self,my_list):
		list_0 = []
		for item in my_list:
			if item != 0:
				list_0.append(item)
		return list_0

	def add_item_0(self,my_list, direction):
		for i in range(4 - len(my_list)):
			if direction == 'right':
				my_list.insert(0, 0)
			elif direction == 'left':
				my_list.append(0)
		return my_list

	def add_same_number(self,my_list, direction):
		global Gamemusic
		if direction == 'right':
			for i in range(len(my_list)-1, -1, -1):
				if i >= 1:
					if my_list[i-1] == my_list[i]:
						Gamemusic = 1
						Number = my_list[i] + int(self.show_list[1])
						self.show_list[1] = str(Number)
						my_list[i-1] = 0
						my_list[i] = 2*my_list[i]
						i +=  1
		else:
			for i in range(len(my_list)):
				if i >= 1:
					if my_list[i-1] == my_list[i]:
						Gamemusic = 1
						Number = my_list[i] + int(self.show_list[1])
						self.show_list[1] = str(Number)
						my_list[i] = 0
						my_list[i-1] = 2*my_list[i-1]
						i +=  1
		return my_list

	def inversion_data_list(self,config_list):
		data_list = config_list[3]
		if config_list[2] == 1:
			new_list = []
			for i in range(len(data_list[0])):
				temp_list = []
				for j in range(len(data_list)):
					temp_list.append(data_list[j][i])
				new_list.append(temp_list)
			data_list = new_list
		if config_list[0] == 1:
			new_list = []
			for temp_list in data_list:
				new_list.insert(0,temp_list)
			data_list = new_list
		if config_list[1] == 1:
			new_list = []
			for temp_list in data_list:
				new_list.append(temp_list[::-1])
			data_list = new_list
		return data_list

	def NewGame(self):
		global time_flag
		time_flag = True
		self.data = [[0 for i in range(4)] for i in range(4)]
		self.data = self.insert(self.data)
		self.data = self.insert(self.data)
		self.show_list[1] = '0'
		self.show_list[3] = '0'
		del self.data_left[0:]
		self.ShowWindow()

	def OnNew(self,e):
		self.NewGame()

	def OnUp(self,e):
		print len(self.data_left)
		if len(self.data_left) == 1 or len(self.data_left) == 0:
			dial = wx.MessageDialog(None, u"不能再退了！！", u'警告', wx.OK|wx.ICON_EXCLAMATION)
			dial.ShowModal()
		else:
			self.data_right.append([self.data,self.show_list])
			self.data_left.pop()
			self.data = self.data_left[-1][0]
			self.show_list = self.data_left[-1][1]
			self.ShowWindow()

	def OnDown(self,e):
		if len(self.data_right) == 0:
			dial = wx.MessageDialog(None, u"不能再退了！！", u'警告', wx.OK|wx.ICON_EXCLAMATION)
			dial.ShowModal()
		else:
			self.data = self.data_right[-1][0]
			self.show_list = self.data_right[-1][1]
			self.data_right.pop()
			self.data_left.append([self.data,self.show_list])
			self.ShowWindow()

	def OnExit(self,e):
		self.Close()

	def OnClose(self,e):
		dial = wx.MessageDialog(None, u'您确定要退出游戏吗?', u'退出游戏',wx.YES_NO | wx.NO_DEFAULT | wx.ICON_EXCLAMATION)
		ret = dial.ShowModal()
		if ret == wx.ID_YES:
			self.Destroy()
		else:
			e.Veto()

	def setIcon(self):
		icon = wx.Icon("images/icon.ico",wx.BITMAP_TYPE_ICO)
		self.SetIcon(icon)

	def GameWin(self):
		global play_flag
		for item_list in self.data:
			if 2048 in item_list:
				dial = wx.MessageDialog(None, u'您赢了!\n您想继续玩吗?', u'游戏结束',wx.YES_NO | wx.NO_DEFAULT | wx.ICON_EXCLAMATION)
				ret = dial.ShowModal()
				if ret == wx.ID_YES:
					play_flag = False
					return
				else:
					self.Destroy()

	def OnAbout(self,event):
		a = MyDialog(self).Show()


class MyDialog(wx.Dialog): 
	def __init__(self, parent): 
		super(MyDialog, self).__init__(parent, size = (470,380),style=wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN)
		self.SetTitle(u'关于“2048”')
		panel = wx.Panel(self)
		sizer = wx.GridBagSizer(5,5)
		icon = wx.StaticBitmap(panel, bitmap=wx.Bitmap('images/window.png'))
		sizer.Add(icon, pos=(0, 0), span=(0,4), flag=wx.LEFT,border=15)
		line = wx.StaticLine(panel,size=(444,2))
		sizer.Add(line,pos=(1,0),span=(0,4),flag=wx.LEFT|wx.BOTTOM,border=10)
		icon2 = wx.StaticBitmap(panel, bitmap=wx.Bitmap('images/icon.ico'),size=(40,45))
		sizer.Add(icon2, pos=(2, 0), flag=wx.LEFT,border=15)
		text2 = wx.StaticText(panel, label=u" 2048 小游戏\n 版本 1.0.0\n 版权所有 © 2017 牛开心。保留所有权利。",size=(50,50))
		sizer.Add(text2, pos=(2, 1), span=(1,4), flag=wx.TOP|wx.EXPAND, border=0)
		text4 = wx.StaticText(panel, label=u" 牛开心使用Python2.7和wxPython写的一款益智小游戏\n 本产品使用权属于：所有人")
		sizer.Add(text4, pos=(4, 1), span=(1,4), flag=wx.TOP|wx.LEFT, border=0)
		panel.SetSizer(sizer)


app = wx.App()
Example()
app.MainLoop()
