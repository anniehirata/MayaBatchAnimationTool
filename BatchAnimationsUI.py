from PySide2 import QtCore, QtWidgets, QtGui
from shiboken2 import wrapInstance
import maya.OpenMayaUI
import os
import BatchAnimations
reload(BatchAnimations)
'''
Annie Hirata
Module that contains the UI for users to batch apply animations to a chosen character
To run the UI

try:
    dialog.close()
    dialog.deleteLater()
except:
    pass
    
dialog = BatchAnimationsDialog()
dialog.show()
'''

def get_maya_window():
    maya_window_ptr = maya.OpenMayaUI.MQtUtil.mainWindow()
    
    # Take this pointer and make it a long and create an instance of the pointer that is a QWidget
    return wrapInstance(long(maya_window_ptr), QtWidgets.QWidget)


class ProgressDialog(QtWidgets.QDialog):
    def __init__(self):
        maya_main = get_maya_window()
        super(ProgressDialog, self).__init__(maya_main)

        self.setWindowTitle("Batch Animations")
        self.setMinimumWidth(500)
        self.setMinimumHeight(100)
        self.setModal(False)

        self._create_widgets()
        self._create_layout()

    def _create_widgets(self):
        self._text = QtWidgets.QLabel()
        self._text.setWordWrap(True)
        self._text.setText("Applying animations...")
        
        self._progress_bar = QtWidgets.QProgressBar()

    def _create_layout(self):
        self._main_layout = QtWidgets.QVBoxLayout(self)
        self._main_layout.addWidget(self._text)
        self._main_layout.addWidget(self._progress_bar)

    def set_max_progress(self, max_progress):
        self._progress_bar.setMaximum(max_progress)

    def set_progress_value(self, value):
        self._progress_bar.setValue(value)

    def set_label_text(self, text):
        self._text.setText(text)


class BatchAnimationsDialog(QtWidgets.QDialog):
    def __init__(self):
        # Make the maya window the parent
        maya_main = get_maya_window()
        super(BatchAnimationsDialog, self).__init__(maya_main)

        # Basic window setup
        self.setWindowTitle("Batch Animations")
        self.setMinimumWidth(500)
        self.setMinimumHeight(175)
        self.setModal(True)
        
        self._create_widgets()
        self._create_layouts()
        self._create_connections()


    def _create_widgets(self):
        self._create_title_widget()
        self._create_char_widgets()
        self._create_anim_widgets()
        self._create_save_widgets()
        self._create_buttons()

    def _create_title_widget(self):
        self._title_text = QtWidgets.QLabel()
        self._title_text.setAlignment(QtCore.Qt.AlignHCenter)
        self._title_text.setText("Apply animations to a selected character")

    def _create_char_widgets(self):
        self._char_file_label = QtWidgets.QLabel()
        self._char_file_label.setText("Character File")

        self._char_file_input = QtWidgets.QLineEdit()
        self._char_file_button = QtWidgets.QPushButton()
        self._char_file_button.setIcon(QtGui.QIcon(":fileOpen.png"))

    def _create_anim_widgets(self):
        self._anim_dir_label = QtWidgets.QLabel()
        self._anim_dir_label.setText("Animation Files Directory")

        self._anim_dir_input = QtWidgets.QLineEdit()
        self._anim_dir_button = QtWidgets.QPushButton()
        self._anim_dir_button.setIcon(QtGui.QIcon(":fileOpen.png"))

    def _create_save_widgets(self):
        self._save_dir_label = QtWidgets.QLabel()
        self._save_dir_label.setText("Save Directory")

        self._save_dir_input = QtWidgets.QLineEdit()
        self._save_dir_button = QtWidgets.QPushButton()
        self._save_dir_button.setIcon(QtGui.QIcon(":fileOpen.png"))

    def _create_buttons(self):
        self._batch_button = QtWidgets.QPushButton("Batch Animations")
        self._cancel_button = QtWidgets.QPushButton("Cancel")


    def _create_layouts(self):
        self._main_layout = QtWidgets.QVBoxLayout(self)

        # Create sub layouts
        self._create_char_layout()
        self._create_anim_layout()
        self._create_save_layout()
        self._create_button_layout()

        # Organize main layout
        self._organize_main_layout()

    def _create_char_layout(self):
        self._char_layout = QtWidgets.QHBoxLayout(self)
        self._char_layout.addWidget(self._char_file_label)
        self._char_layout.addWidget(self._char_file_input)
        self._char_layout.addWidget(self._char_file_button)

    def _create_anim_layout(self):
        self._anim_layout = QtWidgets.QHBoxLayout(self)
        self._anim_layout.addWidget(self._anim_dir_label)
        self._anim_layout.addWidget(self._anim_dir_input)
        self._anim_layout.addWidget(self._anim_dir_button)

    def _create_save_layout(self):
        self._save_layout = QtWidgets.QHBoxLayout(self)
        self._save_layout.addWidget(self._save_dir_label)
        self._save_layout.addWidget(self._save_dir_input)
        self._save_layout.addWidget(self._save_dir_button)

    def _create_button_layout(self):
        self._button_layout = QtWidgets.QHBoxLayout(self)
        self._button_layout.addWidget(self._batch_button)
        self._button_layout.addWidget(self._cancel_button)

    def _organize_main_layout(self):
        self._main_layout.addWidget(self._title_text)
        self._main_layout.addLayout(self._char_layout)
        self._main_layout.addLayout(self._anim_layout)
        self._main_layout.addLayout(self._save_layout)
        self._main_layout.addLayout(self._button_layout)
    

    def _create_connections(self):
        self._char_file_button.clicked.connect(self._char_file_dialog)
        self._anim_dir_button.clicked.connect(self._anim_dir_dialog)
        self._save_dir_button.clicked.connect(self._save_dir_dialog)

        self._batch_button.clicked.connect(self._execute_batching)
        self._cancel_button.clicked.connect(self.close)

    def _char_file_dialog(self):
        file_types = "(*.ma, *.mb)"
        file = self._create_file_dialog("Choose a character file", file_types)
        
        if file:
            self._char_file_input.setText(file)

    def _create_file_dialog(self, prompt, file_types):
        file = QtWidgets.QFileDialog.getOpenFileName(self, prompt, filter=file_types)
        return file[0]

    def _anim_dir_dialog(self):
        directory = self._create_dir_dialog("Choose the directory that contains the animations")
        if directory:
            self._anim_dir_input.setText(directory)

    def _save_dir_dialog(self):
        directory = self._create_dir_dialog("Choose a save directory")
        if directory:
            self._save_dir_input.setText(directory)

    def _create_dir_dialog(self, prompt):
        directory = QtWidgets.QFileDialog.getExistingDirectory(self, prompt)
        if directory:
            return directory

    def _execute_batching(self):
        char_file = self._char_file_input.text()
        anim_dir = self._anim_dir_input.text()
        save_dir = self._save_dir_input.text()

        # File error handling
        if not char_file or not anim_dir or not save_dir:
            QtWidgets.QMessageBox.warning(self, "Error", "All inputs are required.")
            return

        if not os.path.exists(char_file):
            QtWidgets.QMessageBox.warning(self, "Error", "Character file does not exist: {}".format(char_file))
            return

        if not os.path.exists(anim_dir):
            QtWidgets.QMessageBox.warning(self, "Error", "Animation directory does not exist: {}".format(anim_dir))
            return

        try:
            # Close main dialog and show progress bar
            self.close()
            self._progress_dialog = ProgressDialog()
            self._progress_dialog.show()

            # Do batching
            BatchAnimations.batch_animations(char_file, anim_dir, save_dir, self._progress_dialog)
        except Exception as e:
            QtWidgets.QMessageBox.warning(self, "Error", str(e))
            print(e)
        finally:
            # Close progress bar
            self._progress_dialog.close()


