# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'httpWidget.ui'
#
# Created: Sat Dec  6 17:47:32 2008
#      by: PyQt4 UI code generator 4.4.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_HttpWidget(object):
    def setupUi(self, HttpWidget):
        HttpWidget.setObjectName("HttpWidget")
        HttpWidget.resize(800, 500)
        self.verticalLayout = QtGui.QVBoxLayout(HttpWidget)
        self.verticalLayout.setObjectName("verticalLayout")

        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.back = QtGui.QPushButton(HttpWidget)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("back.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.back.setIcon(icon)
        self.back.setObjectName("back")
        self.horizontalLayout.addWidget(self.back)

        self.next = QtGui.QPushButton(HttpWidget)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("next.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.next.setIcon(icon1)
        self.next.setObjectName("next")
        self.horizontalLayout.addWidget(self.next)

        self.stop = QtGui.QPushButton(HttpWidget)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("stop.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.stop.setIcon(icon2)
        self.stop.setObjectName("stop")
        self.horizontalLayout.addWidget(self.stop)

        self.reload = QtGui.QPushButton(HttpWidget)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("reload.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.reload.setIcon(icon3)
        self.reload.setObjectName("reload")
        self.horizontalLayout.addWidget(self.reload)

        self.url = QtGui.QLineEdit(HttpWidget)
        self.url.setObjectName("url")
        self.horizontalLayout.addWidget(self.url)


        # Chatting ui initialization
        self.chat = QtGui.QPushButton(HttpWidget)
        self.chat.setText('Chat')
        self.chat.setObjectName('chat')
        self.horizontalLayout.addWidget(self.chat)

        # Web View
        self.webViewLayout = QtGui.QVBoxLayout()
        self.webView = QtWebKit.QWebView(HttpWidget)
        self.webView.settings().setDefaultTextEncoding("utf-8")
        self.webView.setUrl(QtCore.QUrl("about:blank"))
        self.webView.setObjectName("webView")
 

        
        # Putting Together
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout.addWidget(self.webView)

        self.retranslateUi(HttpWidget)
        QtCore.QMetaObject.connectSlotsByName(HttpWidget)

    def retranslateUi(self, HttpWidget):
        HttpWidget.setWindowTitle(QtGui.QApplication.translate("HttpWidget", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.back.setToolTip(QtGui.QApplication.translate("HttpWidget", "Back", None, QtGui.QApplication.UnicodeUTF8))
        self.next.setToolTip(QtGui.QApplication.translate("HttpWidget", "Next", None, QtGui.QApplication.UnicodeUTF8))
        self.stop.setToolTip(QtGui.QApplication.translate("HttpWidget", "Stop", None, QtGui.QApplication.UnicodeUTF8))
        self.reload.setToolTip(QtGui.QApplication.translate("HttpWidget", "Reload", None, QtGui.QApplication.UnicodeUTF8))
        self.chat.setToolTip(QtGui.QApplication.translate('HttpWidget', 'Chat', None, QtGui.QApplication.UnicodeUTF8))

from PyQt4 import QtWebKit
