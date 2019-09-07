from PyQt5 import QtCore, QtGui, QtWidgets
from configobj import ConfigObj
import json

class Ui_MainWindow(QtWidgets.QDialog):
    def setupUi(self, MainWindow):
        self.title = 'JSON Parser'
        self.parser = ConfigObj('config/config.conf')
        self.tests = self.parser.sections
        self.test_properties = {}
        self.red_color = QtGui.QColor(255, 0, 0)
        self.black_color = QtGui.QColor(0, 0, 0)

        MainWindow.setObjectName(self.title)
        MainWindow.resize(800, 695)
        
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")

        #JSON Label
        self.create_json_label()

        #JSON File Name Text Area
        self.create_filename_field()

        #JSON Browse Button
        self.create_browse_btn()

        #Test Type Label
        self.create_testtype_label()

        #Test Type Drop Down
        self.create_testtype_dropdown()
        self.fill_dropdown()

        #Test Type Parse Button
        self.create_parse_btn()

        #Create Horizontal Layout
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")

        #Left JSON Object List
        self.create_left_list()

        #Right JSON Values List
        self.create_right_list()

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        
        file_menu = self.menubar.addMenu('File')
        edit_menu = self.menubar.addMenu('Edit')

        exit_action = QtWidgets.QAction('Exit', self)
        file_menu.addAction(exit_action)
        exit_action.triggered.connect(self.exit_app)

        font_action = QtWidgets.QAction('Font', self)
        edit_menu.addAction(font_action)
        font_action.triggered.connect(self.create_font)

        MainWindow.setMenuBar(self.menubar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def create_font(self):
        self.openFontDialog()

    def openFontDialog(self):
        font, ok = QtWidgets.QFontDialog.getFont()
        if ok:
            self.right_list.setFont(font)

    def exit_app(self):
        exit()

    def load_test_properties(self, test_name):
        for section in self.parser.sections:
            if section == test_name:
                for subsection in self.parser[section]:
                    self.test_properties[subsection] = []
                    for property_name in self.parser[section][subsection]:
                        self.test_properties[subsection].append({property_name:self.parser[section][subsection][property_name]})

    def fill_dropdown(self):
        for x in self.tests:
            self.combo_box.addItem(x)

    def set_using_test(self):
        self.current_test = self.combo_box.currentText()

    def load_json_file(self):
        self.json_text.setPlainText("")
        fname = QtWidgets.QFileDialog.getOpenFileName(self, 'Open File', 'c\\', 'Charles JSON Files (*.chlsj)')
        self.json_text.insertPlainText(fname[0])
        try:
            f = open(fname[0], 'r')
            self.file_data = json.load(f)
        except:
            pass

    def create_testtype_label(self):
        self.test_label = QtWidgets.QLabel(self.centralwidget)
        self.test_label.setObjectName("test_label")
        self.gridLayout.addWidget(self.test_label, 1, 0, 1, 1)

    def create_browse_btn(self):
        self.browse_btn = QtWidgets.QPushButton(self.centralwidget)
        self.browse_btn.setMinimumSize(QtCore.QSize(0, 24))
        self.browse_btn.setMaximumSize(QtCore.QSize(16777215, 24))
        self.browse_btn.setObjectName("browse_btn")
        self.browse_btn.clicked.connect(self.load_json_file)
        self.gridLayout.addWidget(self.browse_btn, 0, 3, 1, 1)

    def create_filename_field(self):
        self.json_text = QtWidgets.QPlainTextEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.json_text.sizePolicy().hasHeightForWidth())
        self.json_text.setSizePolicy(sizePolicy)
        self.json_text.setMinimumSize(QtCore.QSize(0, 24))
        self.json_text.setMaximumSize(QtCore.QSize(16777215, 24))
        self.json_text.setObjectName("json_text")
        self.gridLayout.addWidget(self.json_text, 0, 2, 1, 1)
        self.json_text.setReadOnly(True)

    def create_testtype_dropdown(self):
        self.combo_box = QtWidgets.QComboBox(self.centralwidget)
        self.combo_box.setMinimumSize(QtCore.QSize(0, 24))
        self.combo_box.setMaximumSize(QtCore.QSize(16777215, 24))
        self.combo_box.setObjectName("combo_box")
        self.combo_box.currentTextChanged.connect(self.set_using_test)
        self.gridLayout.addWidget(self.combo_box, 1, 2, 1, 1)        

    def create_json_label(self):
        self.json_label = QtWidgets.QLabel(self.centralwidget)
        self.json_label.setMinimumSize(QtCore.QSize(0, 24))
        self.json_label.setMaximumSize(QtCore.QSize(16777215, 24))
        self.json_label.setObjectName("json_label")
        self.gridLayout.addWidget(self.json_label, 0, 0, 1, 1)

    def create_right_list(self):
        self.right_list = QtWidgets.QTextEdit(self.centralwidget)
        self.right_list.setObjectName("right_list")
        self.horizontalLayout.addWidget(self.right_list)
        self.right_list.setReadOnly(True)
        self.gridLayout.addLayout(self.horizontalLayout, 2, 0, 1, 4)

    def create_left_list(self):
        self.left_list = QtWidgets.QListWidget(self.centralwidget)
        self.left_list.setObjectName("left_list")
        self.horizontalLayout.addWidget(self.left_list)
        self.left_list.clicked.connect(self.print_json)

    def print_json(self):
        self.right_list.clear()
        num = self.left_list.currentRow()
        for k, v in self.event_variables[num].items():
            if v == "MISSING":
                self.right_list.setTextColor(self.red_color)
                self.right_list.append(k + ":" + v)
            else:
                self.right_list.setTextColor(self.black_color)
                self.right_list.append(k + ":" + v)

    def create_parse_btn(self):
        self.parse_btn = QtWidgets.QPushButton(self.centralwidget)
        self.parse_btn.setObjectName("parse_btn")
        self.gridLayout.addWidget(self.parse_btn, 1, 3, 1, 1)
        self.parse_btn.clicked.connect(self.parse_json)

    def add_to_call_list(self, key, var, value):
        if key not in self.event_variables:
            self.event_variables[key] = {}
        self.event_variables[key].__setitem__(var, value)

    def parse_json(self):
        if self.current_test == 'Select A Test':
            self.msg_box = QtWidgets.QMessageBox.about(self, "Error", "Please select a test type.")
            return
        if self.json_text.toPlainText() == '':
            self.msg_box = QtWidgets.QMessageBox.about(self, "Error", "Please select a JSON file.")
            return

        self.load_test_properties(self.current_test)
        
        if self.current_test == 'WEB-FTS Full Segment/Video Test':
            self.parse_fts_video()
        elif self.current_test == 'WEB-Fox Nation Long Form':
            self.parse_web()
        elif self.current_test == 'WEB-FTS Page/Track Test':
            self.parse_fts_page_track()

    def parse_web(self):
        self.event_counter = 0
        self.event_variables = {}
        for array_item in self.file_data:
            if array_item['status'] != 'COMPLETE' or array_item['response']['status'] != 200:
                continue # filter out all bad calls
            if 'body' not in array_item['request']:
                continue # filter out anything that doesn't have data
        
            unparsed_json = array_item['request']['body']['text']
            unparsed_json_dict = json.loads(unparsed_json)

            if 'series' in unparsed_json_dict:
                continue
            
            try:
                if unparsed_json_dict['type'] == 'track':
                    if unparsed_json_dict['event'] in self.test_properties:
                        self.left_list.insertItem(self.event_counter, unparsed_json_dict['event'])
                        for prop_var_dict in self.test_properties[unparsed_json_dict['event']]:
                            for prop_name in prop_var_dict:
                                for item in prop_var_dict.get(prop_name):
                                    if item in unparsed_json_dict['properties']:
                                        self.add_to_call_list(self.event_counter, str(item), str(unparsed_json_dict['properties'][item]))
                                    elif item in unparsed_json_dict['context']['traits']:
                                        self.add_to_call_list(self.event_counter, str(item), str(unparsed_json_dict['context']['traits'][item]))
                                    else:
                                        self.add_to_call_list(self.event_counter, str(item), "MISSING")
                        self.event_counter += 1

                elif unparsed_json_dict['type'] == 'page':
                    continue

            except:
                continue #only after track/page calls - sometimes we get 'counter' calls

    def parse_fts_video(self):
        self.event_counter = 0
        self.event_variables = {}
        for array_item in self.file_data:
            if array_item['status'] != 'COMPLETE' or array_item['response']['status'] != 200:
                continue # filter out all bad calls
            if 'body' not in array_item['request']:
                continue # filter out anything that doesn't have data
        
            unparsed_json = array_item['request']['body']['text']
            unparsed_json_dict = json.loads(unparsed_json)

            if 'series' in unparsed_json_dict:
                continue
            
            try:
                if unparsed_json_dict['type'] == 'track':
                    if unparsed_json_dict['event'] in self.test_properties:
                        self.left_list.insertItem(self.event_counter, unparsed_json_dict['event'])
                        for prop_var_dict in self.test_properties[unparsed_json_dict['event']]:
                            for prop_name in prop_var_dict:
                                for item in prop_var_dict.get(prop_name):
                                    if item in unparsed_json_dict['properties']:
                                        self.add_to_call_list(self.event_counter, str(item), str(unparsed_json_dict['properties'][item]))
                                    else:
                                        self.add_to_call_list(self.event_counter, str(item), "MISSING")
                        self.event_counter += 1

                elif unparsed_json_dict['type'] == 'page':
                    continue

            except:
                continue #only after track/page calls - sometimes we get 'counter' calls

    def parse_fts_page_track(self):
        self.event_counter = 0
        self.event_variables = {}
        for array_item in self.file_data:
            if array_item['status'] != 'COMPLETE' or array_item['response']['status'] != 200:
                continue # filter out all bad calls
            if 'body' not in array_item['request']:
                continue # filter out anything that doesn't have data
        
            unparsed_json = array_item['request']['body']['text']
            unparsed_json_dict = json.loads(unparsed_json)
            
            try:
                if unparsed_json_dict['type'] == 'track':
                    if unparsed_json_dict['event'] in self.test_properties:
                        self.left_list.insertItem(self.event_counter, unparsed_json_dict['event'])
                        for prop_var_dict in self.test_properties[unparsed_json_dict['event']]:
                            for prop_name in prop_var_dict:
                                for item in prop_var_dict.get(prop_name):
                                    if item in unparsed_json_dict['properties']:
                                        self.add_to_call_list(self.event_counter, str(item), str(unparsed_json_dict['properties'][item]))
                                    elif item == 'event':
                                        self.add_to_call_list(self.event_counter, 'event', str(unparsed_json_dict['event']))
                                    else:
                                        self.add_to_call_list(self.event_counter, str(item), "MISSING")
                        self.event_counter += 1

                elif unparsed_json_dict['type'] == 'page':
                    if unparsed_json_dict['name'] in self.test_properties:
                        self.left_list.insertItem(self.event_counter, unparsed_json_dict['name'])
                        for prop_var_dict in self.test_properties[unparsed_json_dict['name']]:
                            for prop_name in prop_var_dict:
                                for item in prop_var_dict.get(prop_name):
                                    if item in unparsed_json_dict['properties']:
                                        self.add_to_call_list(self.event_counter, str(item), str(unparsed_json_dict['properties'][item]))
                                    elif item == 'name':
                                        self.add_to_call_list(self.event_counter, 'name', str(unparsed_json_dict['name']))
                                    elif item == 'category':
                                        self.add_to_call_list(self.event_counter, 'category', str(unparsed_json_dict['category']))
                                    else:
                                        self.add_to_call_list(self.event_counter, str(item), "MISSING")
                        self.event_counter += 1

            except:
                continue #only after track/page calls - sometimes we get 'counter' calls

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate(self.title, self.title))
        self.browse_btn.setText(_translate(self.title, "Browse"))
        self.test_label.setText(_translate(self.title, "Test Type:"))
        self.parse_btn.setText(_translate(self.title, "Parse"))
        self.json_label.setText(_translate(self.title, "JSON File:"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.setWindowIcon(QtGui.QIcon('icon.png'))
    MainWindow.show()
    sys.exit(app.exec_())
