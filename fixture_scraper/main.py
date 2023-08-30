from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg
import sys
import os
import json

from DataTableWidget import Ui_Form as DataTableUI
from SpiderThread import SpiderThread


class ContinueToNextMatch(Exception):
    pass


class MainWindow(qtw.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.ui = DataTableUI()
        self.ui.setupUi(self)
        self.ui.refreshBtn.clicked.connect(self.start_crawler)

        # Crawling thread
        self.crawling_thread = SpiderThread()
        self.crawling_thread.signal.connect(self.finished)
        self.crawling_thread.output_signal.connect(self.checkpoint)

        self.show()

    def start_crawler(self):
        self.ui.refreshBtn.setText('Fetching...')
        self.ui.refreshBtn.setEnabled(False)
        self.crawling_thread.start()

    def finished(self):
        self.ui.refreshBtn.setText('Fetch matches')
        self.ui.refreshBtn.setEnabled(True)
        self.populateRows()

    def checkpoint(self, signal):
        print(signal)

    # def stop(self):
    #     print(self.crawling_thread.proc_id)
    #     os.kill(self.crawling_thread.proc_id)
    #     self.ui.refreshBtn.setText('Refresh')
    #     self.ui.refreshBtn.setEnabled(True)

    def populateRows(self):
        data = []
        # Load nerdy tips data
        with open('fixtures.json') as jsonFile:
            fetchedMatches = json.load(jsonFile)

            data.append({
                "id": str(len(data)+1),
                "platform": {
                    "name": "nerdytips",
                    "url": "nerdytips.com",
                    "matches": fetchedMatches
                }
            })

        allMatches = []
        platforms = []
        loadedMatches = []
        cellFont = qtg.QFont()
        cellFont.setPointSize(12)

        for entry in data:
            platforms.append({
                "platform": entry["platform"]["name"],
                "numOfMatches": len(entry["platform"]["matches"]),
                "numOfRows": 0
            })
            allMatches += entry["platform"]["matches"]

        for i in range(len(allMatches)):
            try:
                for m in loadedMatches:
                    if m["home"] == allMatches[i]["home"] and m["home"] == allMatches[i]["home"] and m["kickoff"] == allMatches[i]["kickoff"]:
                        raise ContinueToNextMatch
            except ContinueToNextMatch:
                continue

            # Index
            idxObjName = f"indexField_{i}"
            indexField = qtw.QLabel()
            indexField.setText(str(i+1))
            indexField.setFont(cellFont)
            indexField.setAlignment(qtc.Qt.AlignCenter)
            indexField.setObjectName(idxObjName)
            indexField.setStyleSheet("#"+idxObjName+"{\n"
                                     "    border:1px solid #ccc;\n"
                                     "    padding:10px;\n"
                                     "}")
            self.ui.gridLayout.addWidget(indexField, i+1, 0, 1, 1)

            # Match
            matchObjName = f"matchField_{i}"
            matchField = qtw.QLabel()
            matchField.setText(
                f'{allMatches[i]["home"].capitalize()} {allMatches[i]["score_result"]} {allMatches[i]["away"].capitalize()}')
            matchField.setFont(cellFont)
            matchField.setAlignment(qtc.Qt.AlignCenter)
            matchField.setObjectName(matchObjName)
            matchField.setStyleSheet("#"+matchObjName+"{\n"
                                     "    border:1px solid #ccc;\n"
                                     "    padding:10px;\n"
                                     "}")
            self.ui.gridLayout.addWidget(matchField, i+1, 1, 1, 1)
            loadedMatches.append(
                {"home": allMatches[i]["home"], "away": allMatches[i]["away"], "kickoff": allMatches[i]["kickoff"]})

            # Time
            timeObjName = f"timeField_{i}"
            timeField = qtw.QLabel()
            timeField.setText(f'{allMatches[i]["kickoff"]}')
            timeField.setFont(cellFont)
            timeField.setAlignment(qtc.Qt.AlignCenter)
            timeField.setObjectName(timeObjName)
            timeField.setStyleSheet("#"+timeObjName+"{\n"
                                    "    border:1px solid #ccc;\n"
                                    "    padding:10px;\n"
                                    "}")
            self.ui.gridLayout.addWidget(timeField, i+1, 2, 1, 1)

            # Platform
            platformLayout = qtw.QVBoxLayout()

            for j in range(len(data)):
                count = 0
                for match in data[j]["platform"]["matches"]:
                    if match["home"] == allMatches[i]["home"] and match["away"] == allMatches[i]["away"]:
                        count += 1
                        if count == 1:
                            platformObjName = f"platformField_{i}_{j}_{count}"
                            platFormName = qtw.QLabel()
                            platFormName.setText(match["platform"])
                            platFormName.setObjectName(platformObjName)
                            platFormName.setStyleSheet("#"+platformObjName+"{\n"
                                                       "    border:1px solid #ccc;\n"
                                                       "    padding:10px;\n"
                                                       "}")
                            platFormName.setAlignment(qtc.Qt.AlignCenter)
                            platFormName.setFont(cellFont)
                            platformLayout.addWidget(platFormName)
                        elif count == len(data):
                            platformObjName = f"platformField_{i}_{j}_{count}"
                            platFormName = qtw.QLabel()
                            platFormName.setText(" ")
                            platFormName.setObjectName(platformObjName)
                            platFormName.setStyleSheet("#"+platformObjName+"{\n"
                                                       "    border:1px solid #ccc;\n"
                                                       "    padding:10px;\n"
                                                       "}")
                            platFormName.setAlignment(qtc.Qt.AlignCenter)
                            platFormName.setFont(cellFont)
                            platformLayout.addWidget(platFormName)
                        else:
                            platformObjName = f"platformField_{i}_{j}_{count}"
                            platFormName = qtw.QLabel()
                            platFormName.setText("")
                            platFormName.setObjectName(platformObjName)
                            platFormName.setStyleSheet("#"+platformObjName+"{\n"
                                                       "    border:1px solid #ccc;\n"
                                                       "    padding:10px;\n"
                                                       "}")
                            platFormName.setAlignment(qtc.Qt.AlignCenter)
                            platFormName.setFont(cellFont)
                            platformLayout.addWidget(platFormName)

            self.ui.gridLayout.addLayout(platformLayout, i+1, 3, 1, 1)

            # Tips
            tipsLayout = qtw.QVBoxLayout()

            for j in range(len(data)):
                count = 0
                for match in data[j]["platform"]["matches"]:
                    if match["home"] == allMatches[i]["home"] and match["away"] == allMatches[i]["away"]:
                        count += 1
                        if count == 1:
                            tipsObjName = f"tipsField_{i}_{j}_{count}"
                            tipName = qtw.QLabel()
                            tipName.setText(match["tip"])
                            tipName.setObjectName(tipsObjName)
                            tipName.setStyleSheet("#"+tipsObjName+"{\n"
                                                  "    border-top:1px solid #ccc;\n"
                                                  "    padding:10px;\n"
                                                  "}")
                            tipName.setAlignment(qtc.Qt.AlignCenter)
                            tipName.setFont(cellFont)
                            tipsLayout.addWidget(tipName)
                        elif count == len(data):
                            tipsObjName = f"tipsField_{i}_{j}_{count}"
                            tipName = qtw.QLabel()
                            tipName.setText(" ")
                            tipName.setObjectName(tipsObjName)
                            tipName.setStyleSheet("#"+tipsObjName+"{\n"
                                                  "    border-top:1px solid #ccc;\n"
                                                  "    padding:10px;\n"
                                                  "}")
                            tipName.setAlignment(qtc.Qt.AlignCenter)
                            tipName.setFont(cellFont)
                            tipsLayout.addWidget(platFormName)
                        else:
                            tipName = qtw.QLabel()
                            tipName.setText("")
                            tipName.setAlignment(qtc.Qt.AlignCenter)
                            tipName.setFont(cellFont)
                            tipsLayout.addWidget(tipName)

            self.ui.gridLayout.addLayout(tipsLayout, i+1, 4, 1, 1)

            # tipsObjName = f"tipsField_{i}"
            # tipsField = qtw.QLabel()
            # tipsField.setText(f'{allMatches[i]["tip"]}')
            # tipsField.setFont(cellFont)
            # tipsField.setAlignment(qtc.Qt.AlignCenter)
            # tipsField.setObjectName(tipsObjName)
            # tipsField.setStyleSheet("#"+tipsObjName+"{\n"
            #                         "    border:1px solid #ccc;\n"
            #                         "    padding:10px;\n"
            #                         "}")
            # self.ui.gridLayout.addWidget(tipsField, i+1, 4, 1, 1)


if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    w = MainWindow(windowTitle="Sports scraper")
    sys.exit(app.exec_())
