import sys
from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import (
    QDialog, QDialogButtonBox, QFormLayout, QFrame, QHBoxLayout, QLabel,
    QLineEdit, QMainWindow, QMenu, QMessageBox, QPushButton, QScrollArea,
    QVBoxLayout, QWidget,QApplication
)
from app.core.storage import StorageError, VaultStorage
from app.ui.generator_ui import GeneratorFenetre

#Fenêtre  permettant d'ajouter ou de modifier une entrée et son erreur personnalisée.
class EntryDialog(QDialog):
    def __init__(self, parent=None, entre=None):
        super().__init__(parent)
        self.setWindowTitle("Modifier une entree" if entre else "Ajouter une entree")
        self.resize(460,220)
        layout = QVBoxLayout(self)
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
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

# Ouvre le générateur de mot de passe
    def generer(self):
        dialog = GeneratorFenetre(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.mot_passe.setText(dialog.mot_recent)

#Verifie les champs avant de valider les fenêtres
    def accepter(self):
        if self.email.text().strip() == "":
            QMessageBox.warning(
                self,
                "Champ requis",
                "Indiquez un e-mail."
            )
        elif self.mot_passe.text() == "":
            QMessageBox.warning(
                self,
                "Champ requis",
                "Indiquez un mot de passe."
            )
        else:
         self.accept()

#Retourne les données sous forme de dictionanire
    def entre(self):
        return {"email": self.email.text().strip(), "mot_passe":self.mot_passe.text()
                }

# Ligne graphique representant une entrée du coffre-fort
class EntryRow(QFrame):
    def __init__(self,entre,modifier, supprimer,parent=None):
        super().__init__(parent)
        self.entre = entre
        self.setFrameShape(QFrame.Shape.StyledPanel)
        layout = QHBoxLayout(self)
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
        self.timer = QTimer(self)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(lambda:self.mot_passe.setText("*******"))
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.context_menu)
        self.modifier_action = modifier
        self.supprimer_action = supprimer

# Affiche le mot de passe pendant 5 secondes
    def reveler(self):
        self.mot_passe.setText(self.entre["mot_passe"])
        self.timer.start(5000)

#Permet de reveler le mot de passe avec un double-clic gauche
    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.reveler()
        super().mouseDoubleClickEvent(event)

    def context_menu(self, position):
        menu = QMenu(self)
        menu.addAction("Reveler pendant 5 secondes", self.reveler)
        menu.addAction(self.modifier_action)
        menu.addAction(self.supprimer_action)

        position_souris = QCursor.pos()
        menu.exec(position_souris)

class MainWindow(QMainWindow):
    def __init__(self,vault_file = "vault.json"):
        super().__init__()
        self.setWindowTitle("Coffre-fort")
        self.resize(1000, 580)
        self.storage = VaultStorage(vault_file)
        self.entrees = []
        self.modifications_non_enregistrees = False
        self.chargement_echoue = False
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        avertissement = QLabel("TP : stockage en texte clair. N 'utilisez pas de vrais identifiants.")
        avertissement.setWordWrap(True)
        layout.addWidget(avertissement)

        path_label = QLabel(f"Fichier : {vault_file}")
        path_label.setTextFormat(Qt.TextFormat.PlainText)
        path_label.setWordWrap(True)
        layout.addWidget(path_label)
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        layout.addWidget(self.scroll,1)
        actions =  QHBoxLayout()
        self.ajouter_button = QPushButton("Ajouter")
        self.ajouter_button.clicked.connect(self.ajouter_entrer)
        actions.addWidget(self.ajouter_button)
        trier = QPushButton("Trier par email (A-Z)")
        trier.clicked.connect(self.trier_entrees)
        actions.addWidget(trier)
        generateur = QPushButton("Generateur")
        generateur.clicked.connect(self.ouvrir_generateur)
        actions.addWidget(generateur)
        layout.addLayout(actions)

        try:
            self.entrees = self.storage.chargement()
        except StorageError as exc:
            self.chargement_echoue = True
            self.ajouter_button.setEnabled(False)

            self.chargement_erreur = str(exc)
            QTimer.singleShot(0, self.montre_chargement_erreur)
        self.rafraichir()

    def montre_chargement_erreur(self):
        QMessageBox.critical(self, "Coffre inaccessible", self.chargement_erreur +
                             "\nLe fichier ne sera pas ecrase.Corrigez-le ou utilisez --vault_file"
                             "avec un autre chemin, puis relancez.")

    def rafraichir(self):
        old = self.scroll.takeWidget()
        if old:
            old.deleteLater()
        container = QWidget()
        layout = QVBoxLayout(container)
        if not self.entrees:
            layout.addWidget(QLabel("Aucune entree."))
        for entre in self.entrees:
            row = EntryRow(entre,
                           lambda checked = False, e=entre: self.modifier_entre(e),
                           lambda checked = False, e=entre: self.supprimer_entre(e))
            layout.addWidget(row)
        layout.addStretch()
        self.scroll.setWidget(container)
        self.statusBar().showMessage(f"{len(self.entrees)} entree(s)")

    def ouvrir_generateur(self):
        GeneratorFenetre(self).exec()

    def ajouter_entrer(self):
        if self.chargement_echoue:
            return
        dialog = EntryDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.entrees.append(dialog.entre())
            self.modifications_non_enregistrees = True
            self.rafraichir()

    def modifier_entre(self, entre):
        dialog = EntryDialog(self,entre)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            entre.update(dialog.entre())
            self.modifications_non_enregistrees = True
            self.rafraichir()

    def supprimer_entre(self, entre):
        box = QMessageBox()
        box.setWindowTitle("Confirmer la suppression")
        box.setTextFormat(Qt.TextFormat.PlainText)
        box.setText(f"Supprimer {entre['email']} ?")
        box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        box.setDefaultButton(QMessageBox.StandardButton.No)
        if box.exec() == QMessageBox.StandardButton.Yes:
            self.entrees = [ e for e in self.entrees if e is not entre]
            self.modifications_non_enregistrees =  True
            self.rafraichir()


    def trier_entrees(self):
        if self.chargement_echoue:
            return
        self.entrees.sort(key = lambda e : e["email"].lower())
        self.modifications_non_enregistrees = True
        self.rafraichir()


    def closeEvent(self,event):
        if self.chargement_echoue or not self.modifications_non_enregistrees:
            event.accept()
        try:
            self.storage.sauvegarder(self.entrees)
        except StorageError as exc:
            QMessageBox.critical(self, "Sauvegarde impossible" , str(exc) +
                                 "\nLa fenetre reste ouverte pour conserver les modifications.")
            event.ignore()
        event.accept()

if __name__ == "__main__":
  app = QApplication(sys.argv)
  window = MainWindow()
  window.show()
  sys.exit(app.exec())


