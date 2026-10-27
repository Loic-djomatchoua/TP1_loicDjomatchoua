import sys
from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import (
    QDialog, QDialogButtonBox, QFormLayout, QFrame, QHBoxLayout, QLabel,
    QLineEdit, QMainWindow, QMenu, QMessageBox, QPushButton, QScrollArea,
    QVBoxLayout, QWidget,QApplication
)
from app.core.storage import StorageError, VaultStorage
from app.ui.generator_ui import GeneratorDialog

class EntryDialog(QDialog):
    def __init__(self, parent=None, entre=none):
        super().__init__(parent)
        self.setWindowTitle("Modifier une entree" if entre else "Ajouter une entree")
        self.resize(460,220)
        layout.QVBoxLayout()
        form = QFormLayout()

        self.email = QLineEdit(entre["email"] if entre else "")
        self.mot_passe = QLineEdit(entre["mot_passe"] if entre else "")
        self.mot_passe.setEchoMode(QLineEdit.EchoMode.Password)
        form.addRow("Email", self.email)
        form.addRow("Mot de passe", self.mot_passe)
        layout.addLayout(form)
        generer = QPushButton("Generer")
        generer.clicked.connect(self.generer)
        layout.addWidget(generer)
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accepter)
        buttons.rejected.connect(self.rejeter)
        layout.addWidget(buttons)

    def generer(self):
        dialog = GeneratorDialog(self)
        if dialog.exec() == QDilaog.DialogCode.Accepted:
            self.mot_passe.setText(dialog.mot_recent)

    def rejeter(self):
        if not self.email.text().strip() or not self.mot_passe.text():
            QMessageBox.warning(self, "Champs requis", "Indiquer un e-mail et un mot de passe")
        super().accept()

    def entre(self):
        return {"email": self.email.text().strip(), "mot_passe":self.mot_passe.text()}

class EntryRow(QFrame):
    def __init__(self,entre,modifier, supprimer,parent=None):
        super().__init__(parent)
        self.entre = entre
        self.setFrameShape(QFrame.Shape.Style.StyledPanel)
        layout = QHLayoutBox()
        email= QLabel(entre["email"])
        email.setTextFormat(Qt.TextFormat.PlainText)
        email.setWordWrap(True)

        self.mot_passe = QLabel("******")
        self.mot_passe.setTextFormat(Qt.TextFormat.PlainText)
        self.mot_passe.setWordWrap(True)
        layout.addWidget(email,2)
        layout.addWidget(self.mot_passe,2)
        for text, action in (("Reveler", self.reveler), ("Modifier", modifier), ("Supprimer",supprimer)):
            button = QPushButton(text)
            button.clicked.connect(action)
            layout.addWidget(button)
        self.timer = QTimer()
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(lambda:self.mot_passe.setText("*******"))
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.context_menu)
        self.modifier_action = modifier
        self.supprimer_action = supprimer

    def reveler(self):
        self.mot_passe.setText(self.entre["mot_passe"])
        self.timer.start(5000)

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.reveler()
        super().mouseDoubleClickEvent(event)

    def context_menu(self, position):
        menu = QMenu(self)
        menu.addAction("Reveler pendant 5 secondes", self.reveler)
        menu.addAction(self.modifier_action)
        menu.addAction(self.supprimer_action)
        menu.exec(self.mapToGlobal(position))

