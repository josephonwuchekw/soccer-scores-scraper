from PyQt5 import QtCore as qtc
import os
import subprocess


class SpiderThread(qtc.QThread):
    signal = qtc.pyqtSignal()
    output_signal = qtc.pyqtSignal('PyQt_PyObject')

    def __init__(self):
        qtc.QThread.__init__(self)

    def __del__(self):
        self.wait()

    def run(self):
        if os.path.exists('result.csv'):
            os.remove('result.csv')
        cmd = "scrapy crawl match_fixtures_spider"
        proc = subprocess.Popen(
            cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        self.proc_id = proc.pid
        print(self.proc_id)
        out = proc.communicate()
        for line in out:
            self.output_signal.emit(line)
        self.signal.emit()
