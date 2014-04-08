'''
Created on Apr 8, 2014

@author: jordans
'''

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import logging
from datetime import datetime

logging.basicConfig(format='%(asctime)s %(message)s', filename='patch.log', level=logging.INFO)

class SortedDict(dict):
    class Iterator(object):
        def __init__(self, sorted_dict):
            self._dict = sorted_dict
            self._keys = sorted(self._dict.keys())
            self._nr_items = len(self._keys)
            self._idx = 0

        def __iter__(self):
            return self

        def next(self):
            if self._idx >= self._nr_items:
                raise StopIteration

            key = self._keys[self._idx]
            value = self._dict[key]
            self._idx += 1

            return key, value

        __next__ = next

    def __iter__(self):
        return SortedDict.Iterator(self)

    iterkeys = __iter__



class PatchTracker(QWidget):
    def __init__(self, parent=None):
        super(PatchTracker, self).__init__(parent)

        self.servers = SortedDict()

        self.oldTodo = ''
        self.oldScan = ''
        self.oldReboot = ''
        self.oldPatch = ''
        self.oldFinish = ''

        self.todoText = QTextEdit()
        self.scanText = QTextEdit()
        self.patchText = QTextEdit()
        self.rebootText = QTextEdit()
        self.finishText = QTextEdit()

        self.todoButton = QPushButton("&ToDo")
        self.todoButton.show()        
        self.scanButton = QPushButton("&Scan")
        self.scanButton.show()
        self.patchButton = QPushButton("&Patch")
        self.patchButton.show()
        self.rebootButton = QPushButton("&Reboot")
        self.rebootButton.show()
        self.finishButton = QPushButton("&Finish")
        self.finishButton.show()

        dataLabel = QLabel("Date (YYYY-MM-DD):")
        self.dateText = QLineEdit()
        filenameLabel = QLabel("Filename:")
        self.filenameText = QLineEdit()
        self.loadButton = QPushButton("&Load")
        self.loadButton.show()        

        self.todoButton.clicked.connect(self.addTodoEvent)
        self.scanButton.clicked.connect(self.addScanEvent)
        self.patchButton.clicked.connect(self.addPatchEvent)
        self.rebootButton.clicked.connect(self.addRebootEvent)
        self.finishButton.clicked.connect(self.addFinishEvent)
        self.loadButton.clicked.connect(self.loadLog)

        mainLayout = QGridLayout()
        mainLayout.addWidget(self.todoText, 0, 0)
        mainLayout.addWidget(self.todoButton, 1, 0)
        mainLayout.addWidget(self.scanText, 0, 1)
        mainLayout.addWidget(self.scanButton, 1, 1)
        mainLayout.addWidget(self.patchText, 0, 2)
        mainLayout.addWidget(self.patchButton, 1, 2)
        mainLayout.addWidget(self.rebootText, 0, 3)
        mainLayout.addWidget(self.rebootButton, 1, 3)
        mainLayout.addWidget(self.finishText, 0, 4)
        mainLayout.addWidget(self.finishButton, 1, 4)
        
        mainLayout.addWidget(dataLabel, 3, 0)
        mainLayout.addWidget(self.dateText, 4, 0)
        mainLayout.addWidget(filenameLabel, 5, 0)
        mainLayout.addWidget(self.filenameText, 6, 0)
        mainLayout.addWidget(self.loadButton, 7, 0)

        self.setLayout(mainLayout)
        self.setWindowTitle("Manual Patching Tracker")

    def addTodoEvent(self):
        for each in self.todoText.toPlainText().split('\n'):
            if each not in self.oldTodo:
                logging.info("TODO: %s" % each)
        self.oldTodo = self.todoText.toPlainText()

    def addScanEvent(self):
        # does nothing
        pass
    
    def addPatchEvent(self):
        for each in self.patchText.toPlainText().split('\n'):
            if each not in self.oldPatch:
                logging.info("PATCH: %s" % each)
        self.oldPatch = self.patchText.toPlainText()
    
    def addRebootEvent(self):
        for each in self.rebootText.toPlainText().split('\n'):
            if each not in self.oldReboot:
                logging.info("REBOOT: %s" % each)
        self.oldReboot = self.rebootText.toPlainText()
    
    def addFinishEvent(self):
        for each in self.finishText.toPlainText().split('\n'):
            if each not in self.oldFinish:
                logging.info("FINISH: %s" % each)
        self.oldFinish = self.finishText.toPlainText()

    def loadLog(self):
        
        used = []
        todoList = ''
        patchList = ''
        rebootList = ''
        finishList = ''
        
        format = "%Y-%m-%d"

        if self.dateText.text() == "":
            desired_date = datetime.min
        else:
            desired_date = datetime.strptime(self.dateText.text(), format)
        
        with open(self.filenameText.text()) as f:
        
            for line in reversed(list(f)):
                array = line.split(' ')
                if array[3] not in used:
                    log_date = datetime.strptime(array[0], format)
                    if log_date >= desired_date:
                        if array[2] == "TODO:":
                            todoList += array[3] 
                        elif array[2] == "PATCH:":
                            patchList += array[3] 
                        elif array[2] == "REBOOT:":
                            rebootList += array[3] 
                        elif array[2] == "FINISH:":
                            finishList += array[3] 
                        
                        used.append(array[3])

        self.todoText.setText(todoList)
        self.patchText.setText(patchList)
        self.rebootText.setText(rebootList)
        self.finishText.setText(finishList)
        
        self.oldTodo = todoList
        self.oldReboot = rebootList
        self.oldPatch = patchList
        self.oldFinish = finishList        
        
            
        """
        open file
        from bottom of the file until date < date
            for each line
                if server not in the 'used' list
                    add server to action list based on label
                    add server to 'used' list
        """
        pass

"""
query:
    what's finished
    what's not
        compare to todo to finish

load from date? 
    go backwards? 

"""
if __name__ == '__main__':
    
    from PyQt5.QtWidgets import QApplication
    import sys
    
    app = QApplication(sys.argv)

    tracker = PatchTracker()
    tracker.show()

    sys.exit(app.exec_())