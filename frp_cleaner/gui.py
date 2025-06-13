import sys
import logging
from PyQt5.QtWidgets import (
    QApplication, QWidget, QFileDialog,
    QLabel, QPushButton, QVBoxLayout, QMessageBox
)
from cleaner.img_manager import (
    convert_sparse_to_raw, mount_image,
    unmount_image, prepare_and_patch_all
)
from cleaner.frp_detector import detect_targets
from cleaner.frp_neutralizer import neutralize

logging.basicConfig(
    filename="logs/frp_cleaner.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s: %(message)s"
)

class FRPToolGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("FRP Cleaner Samsung")
        self.resize(450, 250)

        self.label = QLabel("Nenhum ficheiro carregado.")
        self.btn_img = QPushButton("Carregar system.img")
        self.btn_ap = QPushButton("Carregar pasta ROM (AP...)")
        self.btn_keys = QPushButton("Carregar pasta Keys")
        self.btn_run = QPushButton("Executar Limpeza")
        self.btn_run.setEnabled(False)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.btn_img)
        layout.addWidget(self.btn_ap)
        layout.addWidget(self.btn_keys)
        layout.addWidget(self.btn_run)
        self.setLayout(layout)

        self.btn_img.clicked.connect(self.load_img)
        self.btn_ap.clicked.connect(self.load_ap)
        self.btn_keys.clicked.connect(self.load_keys)
        self.btn_run.clicked.connect(self.run_clean)

        self.img_path = ""
        self.ap_folder = ""
        self.keys_folder = ""

    def load_img(self):
        f,_ = QFileDialog.getOpenFileName(self, "Selecionar system.img", "", "Imagens Android (*.img)")
        if f:
            self.img_path = f
            self.update_status()
            self.enable_run()

    def load_ap(self):
        d = QFileDialog.getExistingDirectory(self, "Selecionar pasta ROM extraída")
        if d:
            self.ap_folder = d
            self.update_status()
            self.enable_run()

    def load_keys(self):
        d = QFileDialog.getExistingDirectory(self, "Selecionar pasta Keys")
        if d:
            self.keys_folder = d
            self.update_status()
            self.enable_run()

    def update_status(self):
        status = f"IMG: {self.img_path or '—'} | AP: {self.ap_folder or '—'} | Keys: {self.keys_folder or '—'}"
        self.label.setText(status)

    def enable_run(self):
        if self.img_path and self.ap_folder and self.keys_folder:
            self.btn_run.setEnabled(True)

    def run_clean(self):
        try:
            # Reutiliza lógica do CLI
            raw = self.img_path
            if "sparse" in raw:
                raw = convert_sparse_to_raw(raw)
            mnt = mount_image(raw)
            targets = detect_targets(mnt)
            if targets:
                neutralize(targets, "rename")
            unmount_image()
            pkg = prepare_and_patch_all(self.ap_folder, self.keys_folder)
            QMessageBox.information(self, "Sucesso", f"Pacote final: {pkg}")
        except Exception as e:
            QMessageBox.critical(self, "Erro", str(e))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FRPToolGUI()
    window.show()
    sys.exit(app.exec_())
