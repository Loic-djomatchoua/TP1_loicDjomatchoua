# Nom : [Votre nom]
# Numéro d'étudiant : [Votre numéro]
# GitHub : [votre-username]

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QScrollArea, QLabel, QInputDialog, QMessageBox, QMenu
)
from PySide6.QtCore import Qt

from app.core.storage import VaultStorage
from app.ui.generator_ui import GeneratorDialog


class MainWindow(QMainWindow):
    def __init__(self, vault_file="vault.json"):
        super().__init__()
        self.setWindowTitle("Coffre-fort")
        self.setFixedSize(520, 450)
        self.storage = VaultStorage(vault_file)
        self.entries = self.storage.load()
        self.init_ui()

    def init_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)

        # Zone défilante pour la liste des entrées
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.list_container = QWidget()
        self.list_layout = QVBoxLayout(self.list_container)
        self.scroll_area.setWidget(self.list_container)
        main_layout.addWidget(self.scroll_area)

        # Menu contextuel (clic droit)
        self.scroll_area.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.scroll_area.customContextMenuRequested.connect(self.show_context_menu)

        # Boutons de gestion
        btn_layout = QHBoxLayout()
        btn_add = QPushButton("Ajouter")
        btn_add.clicked.connect(self.add_entry)
        btn_edit = QPushButton("Modifier")
        btn_edit.clicked.connect(self.edit_entry)
        btn_delete = QPushButton("Supprimer")
        btn_delete.clicked.connect(self.delete_entry)
        btn_sort = QPushButton("Trier par e-mail")
        btn_sort.clicked.connect(self.sort_entries)

        btn_layout.addWidget(btn_add)
        btn_layout.addWidget(btn_edit)
        btn_layout.addWidget(btn_delete)
        btn_layout.addWidget(btn_sort)
        main_layout.addLayout(btn_layout)

        self.refresh_list()

    def refresh_list(self):
        # Vider la liste
        while self.list_layout.count():
            item = self.list_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        for i, entry in enumerate(self.entries):
            label = QLabel(f"{entry['email']} — {'*' * 10}")
            label.setStyleSheet("padding: 5px; border-bottom: 1px solid #ddd;")
            label.setProperty("index", i)
            label.setProperty("revealed", False)
            label.mouseDoubleClickEvent = lambda event, idx=i, lbl=label: self.reveal_password(idx, lbl)
            self.list_layout.addWidget(label)

        self.list_layout.addStretch()

    def reveal_password(self, index, label):
        """Révèle temporairement le mot de passe au double-clic."""
        password = self.entries[index]["password"]
        if label.property("revealed"):
            label.setText(f"{self.entries[index]['email']} — {'*' * 10}")
            label.setProperty("revealed", False)
        else:
            label.setText(f"{self.entries[index]['email']} — {password}")
            label.setProperty("revealed", True)
            # Masquer à nouveau après 5 secondes
            from PySide6.QtCore import QTimer
            QTimer.singleShot(5000, lambda: self.refresh_list())

    def show_context_menu(self, position):
        menu = QMenu(self)
        action_reveal = menu.addAction("Révéler le mot de passe")
        action_edit = menu.addAction("Modifier")
        action_delete = menu.addAction("Supprimer")

        action = menu.exec(self.scroll_area.mapToGlobal(position))
        widget = self.scroll_area.childAt(position)
        if widget is None:
            return
        index = widget.property("index")
        if index is None:
            return

        if action == action_reveal:
            self.reveal_password(index, widget)
        elif action == action_edit:
            self.edit_entry_at(index)
        elif action == action_delete:
            self.delete_entry_at(index)

    def add_entry(self):
        email, ok = QInputDialog.getText(self, "Ajouter", "Adresse e-mail :")
        if not ok or not email:
            return
        dialog = GeneratorDialog(self)
        if dialog.exec():
            self.storage.add_entry(email, dialog.current_password)
            self.entries = self.storage.load()
            self.refresh_list()

    def edit_entry(self):
        # Prend la première entrée sélectionnée (simplification)
        if self.entries:
            self.edit_entry_at(0)

    def edit_entry_at(self, index):
        if not (0 <= index < len(self.entries)):
            return
        entry = self.entries[index]
        email, ok = QInputDialog.getText(
            self, "Modifier", "Adresse e-mail :", text=entry["email"]
        )
        if not ok or not email:
            return
        dialog = GeneratorDialog(self)
        if dialog.exec():
            self.storage.update_entry(index, email, dialog.current_password)
            self.entries = self.storage.load()
            self.refresh_list()

    def delete_entry(self):
        if self.entries:
            self.delete_entry_at(0)

    def delete_entry_at(self, index):
        if not (0 <= index < len(self.entries)):
            return
        reply = QMessageBox.question(
            self, "Confirmation",
            f"Supprimer l'entrée {self.entries[index]['email']} ?"
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.storage.delete_entry(index)
            self.entries = self.storage.load()
            self.refresh_list()

    def sort_entries(self):
        self.entries.sort(key=lambda e: e["email"].lower())
        self.storage.save(self.entries)
        self.refresh_list()

    def closeEvent(self, event):
        """Sauvegarde automatique à la fermeture."""
        try:
            self.storage.save(self.entries)
        except IOError as e:
            QMessageBox.warning(self, "Erreur", str(e))
        event.accept()