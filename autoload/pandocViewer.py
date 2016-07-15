#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import pypandoc
from PySide import QtGui, QtCore, QtWebKit

PY_FILE = sys.argv[0]
CURRENT_FILE = sys.argv[-1]
LINE_FILE = os.path.join(os.path.dirname(PY_FILE), "pandocViewer_lineInfo.txt")


class Preview(QtGui.QWidget):

    def __init__(self, parent=None):
        super(Preview, self).__init__(parent)

        self.setWindowTitle("Preview")
        self.resize(768, 900)

        self.css = os.path.join(os.path.dirname(__file__), "github.css")

        self.createUI()
        self.layoutUI()

        self.url = None

    def setWatcher(self, watcher):
        self.watcher = watcher

    def createUI(self):
        self.web = self.createView()
        self.web.loadFinished.connect(self.loaded)

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

    def setAddress(self):
        md_path = self.addressLE.text()
        md = self.convert(md_path)
        self.web.setHtml(md)

        self.url = md_path

        if md_path not in self.watcher.files():
            self.watcher.addPath(md_path)

    def setLocalFile(self):
        f = self.fileDialog()
        self.addressLE.setText(f)

        self.setAddress()

    def fileDialog(self):
        """ File dialog """

        return QtGui.QFileDialog.getOpenFileName()[0]

    def reloadPage(self):
        """ Reload current content """

        md = self.convert(self.url)
        self.web.setHtml(md)

    def loaded(self):
        """ Set page scrollbar height after loaded """

        if os.path.exists(LINE_FILE):
            lineInfoFile = open(LINE_FILE, 'r')
            lineNum = int(lineInfoFile.read().split()[0])
            lineInfoFile.close()
        else:
            lineNum = 0

        frame = self.web.page().mainFrame()
        maxHeight = frame.scrollBarMaximum(QtCore.Qt.Vertical)
        currentHeight = int(maxHeight * (lineNum / 100.0))
        frame.setScrollPosition(QtCore.QPoint(0, currentHeight))


def main():
    app = QtGui.QApplication(sys.argv)
    w = Preview()
    watcher = QtCore.QFileSystemWatcher()
    watcher.fileChanged.connect(w.reloadPage)
    w.setWatcher(watcher)
    w.show()
    w.raise_()
    w.setAddress()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
