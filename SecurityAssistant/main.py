import sys
import socket
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QStackedWidget, QProgressBar,
    QFormLayout, QLineEdit, QTextBrowser
)
from PyQt5 import QtCore
from PyQt5.QtGui import QPixmap, QFont, QIcon
from Detect_Enum import scan_network, detect_os, scan_ports , identify_services , nmap_vulnerability_scan
from PyQt5.QtCore import QTimer

class PortScanThread(QtCore.QThread):
    update_signal = QtCore.pyqtSignal(list, int)

    def __init__(self, host, parent=None):
        super().__init__(parent)
        self.host = host

    def run(self):
        start_port = 79
        end_port = 8080
        open_ports = []
        total_ports = end_port - start_port + 1

        for port in range(start_port, end_port + 1):
            status = self.check_port_status(port)
            if status == 'open' or status == "filtered":
                open_ports.append([port, status])
            progress = int((port - start_port + 1) / total_ports * 100)

            # Utiliser QMetaObject.invokeMethod pour appeler la fonction dans le thread principal
            self.update_signal.emit(open_ports, progress)

    def check_port_status(self, port):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(2)
                s.connect((self.host, port))
                return "open"
        except ConnectionRefusedError:
            return 'closed'
        except socket.timeout:
            return 'filtered'



class ScanThread(QtCore.QThread):
    update_signal = QtCore.pyqtSignal(int, list)

    def __init__(self, parent=None):
        super().__init__(parent)

    def run(self):
        network = "192.168.1"
        active_machines = scan_network(network, self.update_progress)
        self.update_signal.emit(100, active_machines)

    def update_progress(self, value):
        self.update_signal.emit(value, [])

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.stacked_widget = QStackedWidget(self)
        main_layout = QVBoxLayout(self)
        self.initNavbar(main_layout)
        self.initPages()

        main_layout.addWidget(self.stacked_widget)
        self.stacked_widget.setCurrentIndex(0)

        self.setStyleSheet('background-color: #fff;')

        font = QFont()
        font.setPointSize(12)

        self.setMinimumSize(500, 500)
        self.setWindowIcon(QIcon('C:\\Users\\sansri\\Desktop\\Projet CPRJ\\Frontend\\logo.ico'))
        self.setWindowTitle('HackHalt')
        self.show()

    def initNavbar(self, main_layout):
        navbar_layout = QHBoxLayout()

        logo_label = QLabel(self)
        logo_pixmap = QPixmap('C:\\Users\\sansri\\Desktop\\\Projet CPRJ\\Frontend\\logo 1.jpg')
        logo_label.setPixmap(logo_pixmap)
        navbar_layout.addWidget(logo_label)

        buttons_layout = QHBoxLayout()
        btn_style = '''
            color: #000;
            text-align: center;
            font-family: Orbitron;
            font-size: 12px;
            font-style: normal;
            font-weight: 700;
            line-height: 100%;
            letter-spacing: 2.4px;
            margin-left: 5px;
        '''

        button_texts = ['Host Enumeration', 'OS Detection', 'Port Enumeration' ,'Scan Network','Vulnerabilities Detection']
        for index, btn_text in enumerate(button_texts):
            btn = QPushButton(btn_text)
            btn.setStyleSheet('''
                padding: 12px 17px;
                border-radius: 20px;
                border: 2px solid #FFEA00;
                background: #FFF;
                margin-left: 2px;
            ''')
            btn.setStyleSheet(btn.styleSheet() + btn_style)
            btn.setCursor(QtCore.Qt.PointingHandCursor)
            btn.clicked.connect(lambda _, index=index: self.on_button_clicked(index))
            buttons_layout.addWidget(btn)


        buttons_layout.setSpacing(5)
        navbar_layout.addLayout(buttons_layout)
        main_layout.addLayout(navbar_layout)

    def initPages(self):
        for label_text in ['Host Enumeration', 'OS Detection', 'Port Enumeration','Scan Network','Vulnerabilities Detection']:
            page = QWidget()
            content_widget = self.get_content_widget(label_text)
            layout = QFormLayout(page)
            layout.addRow(label_text, content_widget)
            self.stacked_widget.addWidget(page)

    def get_content_widget(self, label_text):
        if label_text == 'Host Enumeration':
            return HostEnum()
        elif label_text == 'OS Detection':
            return OSDetect()
        elif label_text == 'Port Enumeration':
            return PortEnum()
        elif label_text == 'Scan Network':
            return ScanNet()
        elif label_text == 'Vulnerabilities Detection':
            return VulnDet()

    def on_button_clicked(self, index):
        self.stacked_widget.setCurrentIndex(index)

class HostEnum(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QFormLayout(self)
        scan_button = QPushButton("Start Network Scan")
        scan_button.clicked.connect(self.start_network_scan)
        layout.addRow(scan_button)
        self.progress_bar = QProgressBar(self)
        layout.addRow("Progress:", self.progress_bar)
        self.scan_thread = ScanThread()
        self.scan_thread.update_signal.connect(self.update_scan_results)
        self.active_machines_label = QLabel()
        layout.addRow("Active Machines:", self.active_machines_label)

    def start_network_scan(self):
        self.clear_results()
        self.scan_thread.start()

    def update_scan_results(self, value, active_machines):
        if active_machines:
            machines_text = "\n".join(active_machines)
            self.active_machines_label.setText(f"Active Machines:\n{machines_text}")
        else:
            self.active_machines_label.setText("No active machines found on the network.")
        self.progress_bar.setValue(value)

    def clear_results(self):
        self.active_machines_label.clear()
        self.progress_bar.setValue(0)

class OSDetect(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QFormLayout(self)
        host_ip = socket.gethostbyname(socket.gethostname())
        ip_label = QLabel(f"{host_ip}")
        layout.addRow("Your IP Address: ", ip_label)
        detect_button = QPushButton("Detect OS")
        detect_button.clicked.connect(self.detect_os)
        layout.addRow(detect_button)
        self.result_label = QLabel()
        layout.addRow("Detection Result:", self.result_label)

    def detect_os(self):
        host_ip = socket.gethostbyname(socket.gethostname())
        result = detect_os(host_ip)
        self.result_label.setText(result)

class PortEnum(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        layout = QFormLayout(self)

        # Obtenez automatiquement l'adresse IP de la machine
        host_ip = socket.gethostbyname(socket.gethostname())

        # Ajoutez une étiquette pour afficher l'adresse IP
        ip_label = QLabel(f"{host_ip}")
        layout.addRow("Your IP Address:", ip_label)

        # Créez un bouton pour déclencher la détection des ports
        scan_button = QPushButton("Scan Ports")
        scan_button.clicked.connect(self.scan_ports)
        layout.addRow(scan_button)

        # Enlevez la barre de progression pour afficher le progrès du scan
        # self.progress_bar = QProgressBar(self)
        # layout.addRow("Progress:", self.progress_bar)

        # Ajoutez une zone de texte pour afficher les résultats
        self.result_browser = QTextBrowser()
        layout.addRow("Scan Result:", self.result_browser)

        # Thread pour l'analyse des ports
        self.scan_thread = PortScanThread(host_ip, self)
        self.scan_thread.update_signal.connect(self.update_scan_results)  # Connecter le signal ici

    def scan_ports(self):
        # Démarrez le thread pour l'analyse des ports
        self.scan_thread.start()

    def update_scan_results(self, open_ports, progress):
        # Vous n'avez plus besoin de la barre de progression, vous pouvez laisser cette fonction telle quelle

        # Affichez les résultats dans la zone de texte
        if open_ports:
            result_text = "\n".join([f"Port {port} : {status}" for port, status in open_ports])
            self.result_browser.setPlainText(result_text)
        else:
            self.result_browser.setPlainText("No open ports found on this machine.")

class ScanNet(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)

        # Ajoutez une étiquette pour afficher les résultats de la numérisation
        self.result_browser = QTextBrowser(self)
        layout.addWidget(self.result_browser)

        # Ajoutez un bouton pour lancer la numérisation
        scan_button = QPushButton("Scan Network")
        scan_button.clicked.connect(self.scan_network)
        layout.addWidget(scan_button)

    def scan_network(self):
        # Obtenez l'adresse IP de la machine locale
        host_ip = socket.gethostbyname(socket.gethostname())

        # Appelez la fonction identify_services avec l'adresse IP
        identified_services = identify_services(host_ip)

        # Affichez des messages de débogage
        print(f"Scanning network for host: {host_ip}")
        print(f"Identified services: {identified_services}")

        # Affichez les résultats dans le QTextBrowser
        if identified_services:
            result_text = "\n".join([f"Port {port} : {service}" for port, service in identified_services.items()])
            self.result_browser.setPlainText(result_text)
        else:
            self.result_browser.setPlainText("No services identified on this machine.")

class VulnDet(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        layout = QFormLayout(self)

        # Ajoutez un bouton pour lancer la détection des vulnérabilités
        scan_button = QPushButton("Detect Vulnerabilities")
        scan_button.clicked.connect(self.detect_vulnerabilities)
        layout.addRow(scan_button)

        # Ajoutez une zone de texte pour afficher les résultats
        self.result_browser = QTextBrowser()
        layout.addRow("Vulnerability Scan Result:", self.result_browser)

    def detect_vulnerabilities(self):
        # Obtenez l'adresse IP de la machine locale
        host_ip = socket.gethostbyname(socket.gethostname())

        # Appelez la fonction nmap_vulnerability_scan avec l'adresse IP
        nmap_vulnerability_scan(host_ip, self.result_browser)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
