# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'T_Rax_RubyControl.ui'
#
# Created: Fri Sep 27 22:01:05 2013
#      by: PyQt4 UI code generator 4.9.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_ruby_control_widget(object):
    def setupUi(self, ruby_control_widget):
        ruby_control_widget.setObjectName(_fromUtf8("ruby_control_widget"))
        ruby_control_widget.resize(250, 483)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(ruby_control_widget.sizePolicy().hasHeightForWidth())
        ruby_control_widget.setSizePolicy(sizePolicy)
        ruby_control_widget.setMinimumSize(QtCore.QSize(250, 410))
        ruby_control_widget.setMaximumSize(QtCore.QSize(255, 66000))
        ruby_control_widget.setBaseSize(QtCore.QSize(0, 0))
        ruby_control_widget.setStyleSheet(_fromUtf8("\n"
"#ruby_control_widget, #temperature_control_widget, #diamond_control_widget, QTabWidget::pane, QTabWidget::tab-bar,\n"
"#experiment_tab, #calibration_tab{\n"
"    background: #1E1E1E;    \n"
"}\n"
"\n"
"#temperature_control_widget {\n"
"    padding-left: 5px;\n"
"}\n"
"\n"
"QLabel , QCheckBox, QGroupBox, QRadioButton  {\n"
"    color: #F1F1F1;\n"
"    font-weight: bold;\n"
"}\n"
"QCheckBox{\n"
"    border-radius: 5px;\n"
"}\n"
"QRadioButton {\n"
"    font-weight: normal;\n"
"}\n"
"\n"
"QLineEdit{\n"
"    border-radius: 5px;\n"
"    background: #F1F1F1;\n"
"    color: black;\n"
"}\n"
"\n"
"QPushButton{\n"
"    color:white;\n"
"    border-color: black;\n"
"    border: 2px solid #F1F1F1;\n"
"    border-radius: 11px;\n"
"    font-weight: bold;\n"
"    padding: 5px;\n"
"}\n"
"#temperature_control_widget QPushButton {\n"
"    background: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5, stop:0.20398 rgba(221, 124, 40, 255), stop:1 rgba(0, 0, 0, 255))\n"
"}\n"
"\n"
"#ruby_control_widget QPushButton {\n"
"    background: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5, stop:0.20398 rgba(197, 0, 3, 255), stop:1 rgba(0, 0, 0, 255))\n"
"}\n"
"\n"
"#diamond_control_widget QPushButton{\n"
"    background: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5, stop:0.20398 rgba(27, 0, 134, 255), stop:1 rgba(0, 0, 0, 255))\n"
"}\n"
"\n"
"QPushButton::hover{\n"
"    border:2px solid #fff;\n"
"    margin: 0.5px;\n"
"}\n"
"\n"
"QPushPutton::press{\n"
"   border:2px solid #fff;\n"
"    margin: 2px;\n"
"}\n"
"\n"
"QGroupBox {\n"
"    border: 2px solid #F1F1F1;\n"
"    border-radius: 5px;\n"
"    margin-top: 7px;\n"
"    padding: 0px\n"
"}\n"
"QGroupBox::title {\n"
"     subcontrol-origin: margin;\n"
"     left: 20px\n"
" }\n"
" \n"
"QTabBar::tab {\n"
"    background: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5, stop:0.20398 rgba(221, 124, 40, 255), stop:1 #1E1E1E);\n"
"    border: 2px solid  #F1F1F1;\n"
"    border-top-left-radius: 4px;\n"
"    border-top-right-radius: 10px;\n"
"    padding: 5px;\n"
"    padding-right: 10px;\n"
"    color: #FFF;\n"
"    font-weight: bold;\n"
"    width:85px;\n"
"    margin-left: 7px\n"
"}\n"
"\n"
"QTabBar::tab:hover {\n"
"    border-color: #fff;\n"
"}\n"
"\n"
"QTabBar::tab:selected {\n"
"\n"
"    border:3px solid  #FFF;\n"
"    border-bottom-color: #1E1E1E;\n"
"}\n"
"\n"
"QTabBar::tab:!selected {\n"
"    \n"
"    margin-top: 2px;\n"
"}\n"
""))
        self.verticalLayout_2 = QtGui.QVBoxLayout(ruby_control_widget)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.groupBox = QtGui.QGroupBox(ruby_control_widget)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.horizontalLayout_5 = QtGui.QHBoxLayout(self.groupBox)
        self.horizontalLayout_5.setContentsMargins(11, -1, -1, 10)
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setSizeConstraint(QtGui.QLayout.SetFixedSize)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.load_exp_data_btn = QtGui.QPushButton(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.load_exp_data_btn.sizePolicy().hasHeightForWidth())
        self.load_exp_data_btn.setSizePolicy(sizePolicy)
        self.load_exp_data_btn.setMinimumSize(QtCore.QSize(90, 0))
        self.load_exp_data_btn.setObjectName(_fromUtf8("load_exp_data_btn"))
        self.gridLayout.addWidget(self.load_exp_data_btn, 0, 0, 1, 1)
        self.exp_filename_lbl = QtGui.QLabel(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.exp_filename_lbl.sizePolicy().hasHeightForWidth())
        self.exp_filename_lbl.setSizePolicy(sizePolicy)
        self.exp_filename_lbl.setObjectName(_fromUtf8("exp_filename_lbl"))
        self.gridLayout.addWidget(self.exp_filename_lbl, 0, 1, 1, 1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setSizeConstraint(QtGui.QLayout.SetFixedSize)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.load_previous_exp_data_btn = QtGui.QPushButton(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.load_previous_exp_data_btn.sizePolicy().hasHeightForWidth())
        self.load_previous_exp_data_btn.setSizePolicy(sizePolicy)
        self.load_previous_exp_data_btn.setMaximumSize(QtCore.QSize(40, 22))
        self.load_previous_exp_data_btn.setObjectName(_fromUtf8("load_previous_exp_data_btn"))
        self.horizontalLayout.addWidget(self.load_previous_exp_data_btn)
        self.load_next_exp_data_btn = QtGui.QPushButton(self.groupBox)
        self.load_next_exp_data_btn.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.load_next_exp_data_btn.sizePolicy().hasHeightForWidth())
        self.load_next_exp_data_btn.setSizePolicy(sizePolicy)
        self.load_next_exp_data_btn.setMaximumSize(QtCore.QSize(40, 22))
        self.load_next_exp_data_btn.setObjectName(_fromUtf8("load_next_exp_data_btn"))
        self.horizontalLayout.addWidget(self.load_next_exp_data_btn)
        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 1)
        self.exp_folder_name_lbl = QtGui.QLabel(self.groupBox)
        self.exp_folder_name_lbl.setObjectName(_fromUtf8("exp_folder_name_lbl"))
        self.gridLayout.addWidget(self.exp_folder_name_lbl, 2, 0, 1, 2)
        self.auto_process_cb = QtGui.QCheckBox(self.groupBox)
        self.auto_process_cb.setObjectName(_fromUtf8("auto_process_cb"))
        self.gridLayout.addWidget(self.auto_process_cb, 1, 1, 1, 1)
        self.horizontalLayout_5.addLayout(self.gridLayout)
        self.verticalLayout_2.addWidget(self.groupBox)
        self.roi_setup_btn = QtGui.QPushButton(ruby_control_widget)
        self.roi_setup_btn.setObjectName(_fromUtf8("roi_setup_btn"))
        self.verticalLayout_2.addWidget(self.roi_setup_btn)
        self.groupBox_2 = QtGui.QGroupBox(ruby_control_widget)
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.verticalLayout = QtGui.QVBoxLayout(self.groupBox_2)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.comboBox = QtGui.QComboBox(self.groupBox_2)
        self.comboBox.setMinimumSize(QtCore.QSize(0, 25))
        self.comboBox.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.comboBox.setStyleSheet(_fromUtf8("text-align: right;"))
        self.comboBox.setObjectName(_fromUtf8("comboBox"))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.addItem(_fromUtf8(""))
        self.horizontalLayout_2.addWidget(self.comboBox)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.gridLayout_2 = QtGui.QGridLayout()
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.label = QtGui.QLabel(self.groupBox_2)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 2)
        spacerItem1 = QtGui.QSpacerItem(19, 15, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem1, 0, 2, 1, 1)
        spacerItem2 = QtGui.QSpacerItem(52, 14, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem2, 1, 0, 1, 1)
        self.reference_ruby_pos_txt = QtGui.QLineEdit(self.groupBox_2)
        self.reference_ruby_pos_txt.setMinimumSize(QtCore.QSize(0, 22))
        self.reference_ruby_pos_txt.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.reference_ruby_pos_txt.setObjectName(_fromUtf8("reference_ruby_pos_txt"))
        self.gridLayout_2.addWidget(self.reference_ruby_pos_txt, 1, 1, 1, 1)
        self.label_3 = QtGui.QLabel(self.groupBox_2)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout_2.addWidget(self.label_3, 1, 2, 1, 1)
        self.label_2 = QtGui.QLabel(self.groupBox_2)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout_2.addWidget(self.label_2, 2, 0, 1, 2)
        spacerItem3 = QtGui.QSpacerItem(19, 15, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem3, 2, 2, 1, 1)
        spacerItem4 = QtGui.QSpacerItem(52, 15, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem4, 3, 0, 1, 1)
        self.ruby_pos_lbl = QtGui.QLabel(self.groupBox_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ruby_pos_lbl.sizePolicy().hasHeightForWidth())
        self.ruby_pos_lbl.setSizePolicy(sizePolicy)
        self.ruby_pos_lbl.setFocusPolicy(QtCore.Qt.TabFocus)
        self.ruby_pos_lbl.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.ruby_pos_lbl.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.ruby_pos_lbl.setObjectName(_fromUtf8("ruby_pos_lbl"))
        self.gridLayout_2.addWidget(self.ruby_pos_lbl, 3, 1, 1, 1)
        self.label_4 = QtGui.QLabel(self.groupBox_2)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout_2.addWidget(self.label_4, 3, 2, 1, 1)
        self.label_5 = QtGui.QLabel(self.groupBox_2)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout_2.addWidget(self.label_5, 4, 0, 1, 1)
        spacerItem5 = QtGui.QSpacerItem(19, 14, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem5, 4, 2, 1, 1)
        spacerItem6 = QtGui.QSpacerItem(52, 15, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem6, 5, 0, 1, 1)
        self.pressure_lbl = QtGui.QLabel(self.groupBox_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pressure_lbl.sizePolicy().hasHeightForWidth())
        self.pressure_lbl.setSizePolicy(sizePolicy)
        self.pressure_lbl.setMinimumSize(QtCore.QSize(0, 22))
        self.pressure_lbl.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.pressure_lbl.setAutoFillBackground(True)
        self.pressure_lbl.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.pressure_lbl.setObjectName(_fromUtf8("pressure_lbl"))
        self.gridLayout_2.addWidget(self.pressure_lbl, 5, 1, 1, 1)
        self.label_6 = QtGui.QLabel(self.groupBox_2)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.gridLayout_2.addWidget(self.label_6, 5, 2, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout_2)
        self.verticalLayout_2.addWidget(self.groupBox_2)
        self.fit_ruby_btn = QtGui.QPushButton(ruby_control_widget)
        self.fit_ruby_btn.setObjectName(_fromUtf8("fit_ruby_btn"))
        self.verticalLayout_2.addWidget(self.fit_ruby_btn)
        spacerItem7 = QtGui.QSpacerItem(20, 46, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem7)

        self.retranslateUi(ruby_control_widget)
        QtCore.QMetaObject.connectSlotsByName(ruby_control_widget)

    def retranslateUi(self, ruby_control_widget):
        ruby_control_widget.setWindowTitle(_translate("ruby_control_widget", "Form", None))
        self.groupBox.setTitle(_translate("ruby_control_widget", "Experiment", None))
        self.load_exp_data_btn.setText(_translate("ruby_control_widget", "Load Data", None))
        self.exp_filename_lbl.setText(_translate("ruby_control_widget", "Pt_30.spe", None))
        self.load_previous_exp_data_btn.setText(_translate("ruby_control_widget", "<--", None))
        self.load_next_exp_data_btn.setText(_translate("ruby_control_widget", "-->", None))
        self.exp_folder_name_lbl.setText(_translate("ruby_control_widget", "TextLabel", None))
        self.auto_process_cb.setText(_translate("ruby_control_widget", "autoprocess", None))
        self.roi_setup_btn.setText(_translate("ruby_control_widget", "ROI Setup", None))
        self.groupBox_2.setTitle(_translate("ruby_control_widget", "Pressure", None))
        self.comboBox.setItemText(0, _translate("ruby_control_widget", "hydrostatic", None))
        self.comboBox.setItemText(1, _translate("ruby_control_widget", "non-hydrostatic", None))
        self.label.setText(_translate("ruby_control_widget", "Reference ruby:", None))
        self.reference_ruby_pos_txt.setText(_translate("ruby_control_widget", "150", None))
        self.label_3.setText(_translate("ruby_control_widget", "nm", None))
        self.label_2.setText(_translate("ruby_control_widget", "Measured ruby:", None))
        self.ruby_pos_lbl.setText(_translate("ruby_control_widget", "500", None))
        self.label_4.setText(_translate("ruby_control_widget", "nm", None))
        self.label_5.setText(_translate("ruby_control_widget", "Pressure:", None))
        self.pressure_lbl.setText(_translate("ruby_control_widget", "150", None))
        self.label_6.setText(_translate("ruby_control_widget", "GPa", None))
        self.fit_ruby_btn.setText(_translate("ruby_control_widget", "Fit Ruby", None))

