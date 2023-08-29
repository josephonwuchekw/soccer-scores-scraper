import sys
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg

from DataTableWidget import Ui_Form as DataTableUI


class MainWindow(qtw.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.ui = DataTableUI()
        self.ui.setupUi(self)

        dataModel = [
            {
                "id": 1,
                "platform": {
                    "name": "platform 1",
                    "url": "www.platform.com",
                    "matches": [
                        {
                            "home": "arsenal",
                            "away": "manchester united",
                            "kickoff": "12:00",
                            "tip": "1 - 2",
                            "platform": "platform 1"
                        },
                        {
                            "home": "liverpool",
                            "away": "manchester city",
                            "kickoff": "12:00",
                            "tip": "2 - 3",
                            "platform": "platform 1"
                        }
                    ],
                },
            },
            {
                "id": 2,
                "platform": {
                    "name": "platform 2",
                    "url": "www.platform.com",
                    "matches": [
                        {
                            "home": "arsenal",
                            "away": "manchester united",
                            "kickoff": "12:00",
                            "tip": "1 - 1",
                            "platform": "platform 2"
                        },
                        {
                            "home": "liverpool",
                            "away": "manchester city",
                            "kickoff": "12:00",
                            "tip": "1 - 3",
                            "platform": "platform 2"
                        }
                    ],
                },
            }
        ]

        self.populateRows(dataModel)
        self.show()

    def populateRows(self, data):
        allMatches = []
        platforms = []
        cellFont = qtg.QFont()
        cellFont.setPointSize(12)

        for entry in data:
            matchList = entry["platform"]["matches"]
            allMatches += matchList

        for i in range(len(allMatches)):
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
                f'{allMatches[i]["home"].capitalize()} - {allMatches[i]["away"].capitalize()}')
            matchField.setFont(cellFont)
            matchField.setAlignment(qtc.Qt.AlignCenter)
            matchField.setObjectName(matchObjName)
            matchField.setStyleSheet("#"+matchObjName+"{\n"
                                     "    border:1px solid #ccc;\n"
                                     "    padding:10px;\n"
                                     "}")
            self.ui.gridLayout.addWidget(matchField, i+1, 1, 1, 1)

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
            platformObjName = f"platformField_{i}"
            platformField = qtw.QLabel()
            platformField.setText(f'{allMatches[i]["platform"]}')
            platformField.setFont(cellFont)
            platformField.setAlignment(qtc.Qt.AlignCenter)
            platformField.setObjectName(platformObjName)
            platformField.setStyleSheet("#"+platformObjName+"{\n"
                                        "    border:1px solid #ccc;\n"
                                        "    padding:10px;\n"
                                        "}")
            self.ui.gridLayout.addWidget(platformField, i+1, 3, 1, 1)

            # Tips
            tipsObjName = f"tipsField_{i}"
            tipsField = qtw.QLabel()
            tipsField.setText(f'{allMatches[i]["tip"]}')
            tipsField.setFont(cellFont)
            tipsField.setAlignment(qtc.Qt.AlignCenter)
            tipsField.setObjectName(tipsObjName)
            tipsField.setStyleSheet("#"+tipsObjName+"{\n"
                                    "    border:1px solid #ccc;\n"
                                    "    padding:10px;\n"
                                    "}")
            self.ui.gridLayout.addWidget(tipsField, i+1, 4, 1, 1)


if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    w = MainWindow(windowTitle="Sports scraper")
    sys.exit(app.exec_())
