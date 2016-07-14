#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import pypandoc
from functools import partial
from PySide import QtGui, QtCore, QtWebKit

PY_FILE = sys.argv[0]
CURRENT_FILE = sys.argv[-1]
LINE_FILE = os.path.join(os.path.dirname(PY_FILE), "pandocViewer_lineInfo.txt")


class Preview(QtGui.QWidget):

    def __init__(self, parent=None):
        super(Preview, self).__init__(parent)

        self.setWindowTitle("Preview")
        self.resize(768, 900)

        # self.css = "C:\Users\michi\Desktop\github.css"
        self.css = os.path.join(os.path.dirname(__file__), "github.css")

        self.createUI()
        self.layoutUI()

    def setWatcher(self, watcher):
        self.watcher = watcher

    def createUI(self):
        self.web = self.createView()

        self.addressLE = QtGui.QLineEdit(CURRENT_FILE)
        self.addressLE.returnPressed.connect(self.setAddress)

        self.selectButton = QtGui.QPushButton("Select")
        self.selectButton.clicked.connect(self.setLocalFile)

    def createView(self):
        """ Create/Setup QWebView """

        web = QtWebKit.QWebView(self)
        webSettings = QtWebKit.QWebSettings.globalSettings()
        webSettings.setAttribute(QtWebKit.QWebSettings.PluginsEnabled, True)
        webSettings.setAttribute(
            QtWebKit.QWebSettings.DnsPrefetchEnabled, True)
        webSettings.setAttribute(QtWebKit.QWebSettings.JavascriptEnabled, True)
        webSettings.setAttribute(
            QtWebKit.QWebSettings.OfflineStorageDatabaseEnabled, True)
        webSettings.setAttribute(
            QtWebKit.QWebSettings.LocalStorageDatabaseEnabled, True)
        web.setStyleSheet("background-color: white")
        webSettings.setUserStyleSheetUrl(QtCore.QUrl.fromLocalFile(self.css))

        return web

    def layoutUI(self):
        toolbarLayout = QtGui.QBoxLayout(QtGui.QBoxLayout.LeftToRight)
        toolbarLayout.addWidget(self.addressLE)
        toolbarLayout.addWidget(self.selectButton)
        layout = QtGui.QBoxLayout(QtGui.QBoxLayout.TopToBottom)
        layout.setSpacing(2)
        layout.setContentsMargins(2, 2, 2, 2)
        layout.addLayout(toolbarLayout)
        layout.addWidget(self.web)
        self.setLayout(layout)

    def convert(self, path):
        markdown_path = self.addressLE.text()
        output = pypandoc.convert(
            markdown_path,
            "html",
            extra_args=["-c %s" % self.css])
        return output

    def reload(self):
        md_path = self.addressLE.text()
        md = self.convert(md_path)
        self.web.setHtml(md)

    def setAddress(self):
        md_path = self.addressLE.text()
        md = self.convert(md_path)
        self.web.setHtml(md)

        if md_path not in self.watcher.files():
            self.watcher.addPath(md_path)

    def dummy(self, num):
        frame = self.web.page().mainFrame()
        maxHeight = frame.scrollBarMaximum(QtCore.Qt.Vertical)
        print maxHeight

        currentHeight = int(maxHeight * (num / 100.0))
        print currentHeight
        frame.setScrollPosition(QtCore.QPoint(0, currentHeight))

    def setLocalFile(self):
        f = self.fileDialog()
        self.addressLE.setText(f)

        self.setAddress()

    def fileDialog(self):
        """ File dialog """

        return QtGui.QFileDialog.getOpenFileName()[0]


def file_changed(*args):
    window = args[0]
    window.reload()

    if os.path.exists(LINE_FILE):
        lineInfoFile = open(LINE_FILE, 'r')
        line = int(lineInfoFile.read().split()[0])
        window.dummy(line)


def main():
    app = QtGui.QApplication(sys.argv)
    w = Preview()
    watcher = QtCore.QFileSystemWatcher()
    watcher.fileChanged.connect(partial(file_changed, w))
    w.setWatcher(watcher)
    w.show()
    w.raise_()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
