# -*- coding: utf-8 -*-
import sys
import threading
import socket
from PyQt4 import QtCore, QtGui
from httpWidget import Ui_HttpWidget
import urllib
from urlparse import parse_qsl


#from pyfb import Pyfb
import time
from time import gmtime,strftime

import csv

email_id = 'abc@facebook.com'#'Default'
groupID = 0

class httpWidget(QtGui.QWidget):
	global clisock
	#22clisock = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
	#clisock = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )

	def __init__(self,q,filename=None,parent=None):
		super(httpWidget, self).__init__(parent)
		self.ui = Ui_HttpWidget()
		self.ui.setupUi(self)
		self.current_query = ""
		self.reading_time = time.time()

		filename = "df_test.csv"
		self.fp = open(filename,'aw')
		self.writer = csv.writer(self.fp,delimiter='\t')

		# set margins
		l = self.layout()
		l.setMargin(0)
		self.ui.horizontalLayout.setMargin(5)

		#############################################################################
		#Part for FACEBOOK Authentication											#
		# remove '#1.' when FACEBOOK login is needed								#
		#############################################################################

		#1. FACEBOOK_APP_ID = '178358228892649'
		#1. self.facebook = Pyfb(FACEBOOK_APP_ID)
		#############################################################################
		##>facebook.authenticate()													#
		#############################################################################
		#1. self.facebook.set_permissions(["user_about_me", "email"])
		#1. url = urllib.unquote( self.facebook.get_auth_url() )

		url = 'http://www.google.com/search?hl=en&q='+q
		self.ui.url.setText(url)

		# load page
		self.ui.webView.setUrl(QtCore.QUrl(url))
		# history buttons:
		self.ui.back.setEnabled(False)
		self.ui.next.setEnabled(False)

		QtCore.QObject.connect(self.ui.back,QtCore.SIGNAL("clicked()"), self.back)
		QtCore.QObject.connect(self.ui.next,QtCore.SIGNAL("clicked()"), self.next)
		QtCore.QObject.connect(self.ui.url,QtCore.SIGNAL("returnPressed()"), self.url_changed)
		QtCore.QObject.connect(self.ui.webView,QtCore.SIGNAL("linkClicked (const QUrl&)"), self.link_clicked)
		QtCore.QObject.connect(self.ui.webView,QtCore.SIGNAL("urlChanged (const QUrl&)"), self.link_clicked)
		QtCore.QObject.connect(self.ui.webView,QtCore.SIGNAL("loadProgress (int)"), self.load_progress)
		QtCore.QObject.connect(self.ui.webView,QtCore.SIGNAL("titleChanged (const QString&)"), self.title_changed)
		QtCore.QObject.connect(self.ui.webView,QtCore.SIGNAL("loadFinished(bool)"),self.urlExtract)
		QtCore.QObject.connect(self.ui.reload,QtCore.SIGNAL("clicked()"), self.reload_page)
		QtCore.QObject.connect(self.ui.stop,QtCore.SIGNAL("clicked()"), self.stop_page)
		QtCore.QObject.connect(self.ui.chat,QtCore.SIGNAL("clicked()"), self.chatClicked)	
		QtCore.QMetaObject.connectSlotsByName(self)
	
	def urlExtract(self):
		url = self.ui.url.text()

		page = self.ui.webView.page()
		h = page.currentFrame().toHtml()
		h = unicode(h)

		a = h.find('id=\"resultStats\"')
		if not a == -1:
			h = h[a:]
			a = h.find('About')
			h = h[a+6:]
			a = h.find('results')
			print h[:a]
		
		if "?" in url:
			dataset = url.split("?")[1]
			for data in dataset.split("&"):
				key = data.split("=")[0]
				value = data.split("=")[1]

				if key == "q":
					record = [str(v) for v in value.split("+")]
					self.current_query = record
					record.append(h[:a])
					# time_record = strftime("%Y-%m-%d %H:%M:%S", gmtime())
					# record.append(time_record)
					self.writer.writerows([record])

		if "#" in url:
			global email_id
			dataset = url.split("#")[1]
			for data in dataset.split("&"):
				key = data.split("=")[0]
				value = data.split("=")[1]
		
		t = time.time()-self.reading_time
		self.reading_time = time.time()
		#self.writer.writerows([record])

	def chatClicked(self):
		"""
		if self.chatClient.isHidden():
			self.chatClient.show()
		else:
			self.chatClient.hide()
		"""
		#--chat_client( 'localhost', 2626)
		#11main(sys.argv, 'adf')
		#self.chroom = ChatRoomWidget(self)
		#self.chroom.show()
		pass

	
	def url_changed(self):
		"""
		Url have been changed by user
		"""

		page = self.ui.webView.page()
		history = page.history()
		if history.canGoBack():
			self.ui.back.setEnabled(True)
		else:
			self.ui.back.setEnabled(False)
		if history.canGoForward():
			self.ui.next.setEnabled(True)
		else:
			self.ui.next.setEnabled(False)
		
		url = self.ui.url.text()

		if (not ("http://" in url)) or (not ("https://")):
			url = "http://" + url

		
		self.ui.webView.setUrl(QtCore.QUrl(url))

	def stop_page(self):
		"""
		Stop loading the page
		"""
		self.ui.webView.stop()
	
	def title_changed(self, title):
		"""
		Web page title changed - change the tab name
		"""
		self.setWindowTitle(title)
	
	def reload_page(self):
		"""
		Reload the web page
		"""
		self.ui.webView.setUrl(QtCore.QUrl(self.ui.url.text()))
	
	def link_clicked(self, url):
		"""
		Update the URL if a link on a web page is clicked
		"""
			
		page = self.ui.webView.page()
		history = page.history()
		if history.canGoBack():
			self.ui.back.setEnabled(True)
		else:
			self.ui.back.setEnabled(False)

		if history.canGoForward():
			self.ui.next.setEnabled(True)
		else:
			self.ui.next.setEnabled(False)

		self.ui.url.setText(url.toString())

	
	def load_progress(self, load):
		"""
		Page load progress
		"""
		if load == 100:
			self.ui.stop.setEnabled(False)
		else:
			self.ui.stop.setEnabled(True)
		
	def back(self):
		"""
		Back button clicked, go one page back
		"""
		page = self.ui.webView.page()
		history = page.history()
		history.back()
		if history.canGoBack():
			self.ui.back.setEnabled(True)
		else:
			self.ui.back.setEnabled(False)
	
	def next(self):
		"""
		Next button clicked, go to next page
		"""
		page = self.ui.webView.page()
		history = page.history()
		history.forward()
		if history.canGoForward():
			self.ui.next.setEnabled(True)
		else:
			self.ui.next.setEnabled(False)

	def closeEvent(self,e):
		self.fp.close()


	def keyPressEvent(self,e):
		if ((e.key() == QtCore.Qt.Key_L) and (QtGui.QApplication.keyboardModifiers() & QtCore.Qt.ControlModifier)):
			self.ui.url.selectAll()
			self.ui.url.setFocus()



if __name__ == "__main__":
	app = QtGui.QApplication(sys.argv)
	myapp = httpWidget(sys.argv[1])
	myapp.show()
	sys.exit(app.exec_())
