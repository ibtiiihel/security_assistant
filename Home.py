import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QStackedWidget
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt
from main import MyApp  # Assurez-vous que le nom est correct

class HomePage(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Home Page')
        self.setGeometry(100, 100, 800, 600)

        self.setup_ui()

    def setup_ui(self):
        # Layout principal
        main_layout = QVBoxLayout(self)

        # Enveloppe horizontale pour organiser le logo à gauche et le bouton à droite
        header_layout = QHBoxLayout()

        # Logo à gauche
        logo_label = QLabel()
        logo_pixmap = QPixmap(r'C:\Users\sansri\Desktop\Projet CPRJ\Frontend\LOGO.png')
        logo_pixmap = logo_pixmap.scaledToHeight(160, Qt.SmoothTransformation)
        logo_label.setPixmap(logo_pixmap)
        header_layout.addWidget(logo_label, alignment=Qt.AlignTop | Qt.AlignLeft)

        # Bouton à droite
        button = QPushButton('Explore the application')
        button_style = '''
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
        button.setStyleSheet('''
            padding: 12px 17px;
            border-radius: 20px;
            border: 2px solid #FFEA00;
            background: #FFF;
            margin-left: 2px;
        ''' + button_style)

        # Définir le curseur sur le bouton en tant que pointeur
        button.setCursor(Qt.PointingHandCursor)

        # Connectez le clic du bouton à la fonction pour ouvrir une nouvelle fenêtre
        button.clicked.connect(self.open_new_window)

        header_layout.addWidget(button, alignment=Qt.AlignTop | Qt.AlignRight)

        # Ajouter le header_layout à main_layout
        main_layout.addLayout(header_layout)

        # Section2 - Élément1 (Texte) et Élément2 (Image)
        section2_layout = QVBoxLayout()

        # Élément1 - Texte organisé sous forme d'un QHBoxLayout
        element1_layout = QHBoxLayout()

        text_label1 = QLabel()
        text_label1_text = '''
            <span style="color: #000; font-family: Orbitron; font-size: 32px; font-style: normal; font-weight: 600; line-height: 200%; letter-spacing: 3.2px;">
            Découvrez la puissance de <span style="color: #000; font-family: Orbitron; font-size: 40px; font-style: normal; font-weight: 900; line-height: 200%; letter-spacing: 4px;">HackHalt</span><br>
            votre allié pour une sécurité réseau inégalée.</span>
            '''
        text_label1.setText(text_label1_text)
        text_label1.setTextFormat(Qt.RichText)

        # Ajouter le texte à Élément1
        element1_layout.addWidget(text_label1, alignment=Qt.AlignTop | Qt.AlignLeft)

        # Ajouter Élément1 à Section2
        section2_layout.addLayout(element1_layout)

        # Élément2 - Image centrée
        element2_layout = QHBoxLayout()

        image_label = QLabel()
        image_pixmap = QPixmap(r'C:\Users\sansri\Desktop\Projet CPRJ\Frontend\asset.png')
        image_label.setPixmap(image_pixmap)

        # Ajouter l'image centrée à Élément2
        element2_layout.addWidget(image_label, alignment=Qt.AlignCenter)

        # Ajouter Élément2 à Section2
        section2_layout.addLayout(element2_layout)

        # Ajouter Section2 à main_layout
        main_layout.addLayout(section2_layout)

        # Texte représentatif 2
        text_label2 = QLabel()
        text_label2_text = '<span style="color: #000; font-family: Orbitron; font-size: 16px; font-style: normal; font-weight: 600; line-height: 200%; letter-spacing: 1.6px;">Contrôlez, protégez, et explorez en toute confiance, dès maintenant!</span>'
        text_label2.setText(text_label2_text)
        text_label2.setTextFormat(Qt.RichText)

        # Ajouter le texte représentatif 2 à main_layout
        main_layout.addWidget(text_label2, alignment=Qt.AlignTop | Qt.AlignRight)

    def open_new_window(self):
        # Créer une nouvelle instance de MyApp et l'afficher
        new_window = MyApp()
        new_window.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = HomePage()
    window.show()
    sys.exit(app.exec_())
