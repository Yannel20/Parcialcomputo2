import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QLineEdit, QVBoxLayout, QHBoxLayout, QGroupBox
from PyQt5.QtGui import QFont, QPainter, QColor  # Rect no se importa aquí
from PyQt5.QtCore import Qt, QRect  # Importa QRect desde QtCore

class Ahorcado(QWidget):
    def __init__(self):
        super().__init__()

        # Inicializar variables
        self.palabra_secreta = ""
        self.intentos = 6
        self.letras_adivinadas = []

        # Crear la interfaz gráfica
        self.setWindowTitle("Ahorcado")
        self.setGeometry(300, 300, 600, 400)
        self.setStyleSheet("background-color: #f0f0f0;")  # Color de fondo

        # Crear los elementos de la interfaz
        self.label_instrucciones = QLabel("Ingresa la palabra secreta:", self)
        self.label_instrucciones.setFont(QFont("Arial", 12))
        self.line_edit_palabra_secreta = QLineEdit(self)
        self.line_edit_palabra_secreta.setFixedWidth(150)  # Ancho reducido
        self.button_palabra_secreta = QPushButton("Establecer palabra", self)
        self.button_palabra_secreta.setFixedWidth(150)  # Ancho reducido
        self.button_palabra_secreta.clicked.connect(self.establecer_palabra_secreta)

        # Crear elementos para el juego (ocultos inicialmente)
        self.label_palabra = QLabel("", self)
        self.label_palabra.setFont(QFont("Arial", 20))
        self.label_intentos = QLabel("", self)
        self.line_edit = QLineEdit(self)
        self.line_edit.setMaxLength(1)  # Solo permitir una letra
        self.line_edit.setFixedWidth(50)  # Ancho reducido del cuadro de texto
        self.button = QPushButton("Adivinar", self)
        self.button.setFixedWidth(80)  # Ancho reducido del botón
        self.button.clicked.connect(self.adivinar_letra)

        # Crear un layout horizontal para los elementos de configuración
        config_layout = QHBoxLayout()
        config_layout.addWidget(self.line_edit_palabra_secreta)
        config_layout.addWidget(self.button_palabra_secreta)

        # Crear un layout horizontal para el cuadro de texto y el botón de adivinanza
        input_layout = QHBoxLayout()
        input_layout.addWidget(self.line_edit)
        input_layout.addWidget(self.button)

        # Crear el QGroupBox para el dibujo del ahorcado
        self.groupBox = QGroupBox("Ahorcado")
        self.groupBox.setFixedSize(250, 350)

        # Crear un layout vertical principal para el grupo de juego
        layout_juego = QVBoxLayout()
        layout_juego.addWidget(self.label_instrucciones)
        layout_juego.addLayout(config_layout)
        layout_juego.addWidget(self.label_palabra)
        layout_juego.addWidget(self.label_intentos)
        layout_juego.addLayout(input_layout)

        # Establecer el layout principal en la ventana
        main_layout = QHBoxLayout()
        main_layout.addLayout(layout_juego)
        main_layout.addWidget(self.groupBox)

        # Establecer el layout principal en el widget
        self.setLayout(main_layout)

        # Ocultar los elementos del juego al inicio
        self.label_palabra.hide()
        self.label_intentos.hide()
        self.line_edit.hide()
        self.button.hide()

        # Conectar el evento de pintura del QGroupBox
        self.groupBox.paintEvent = self.paintEvent

        self.show()

    def establecer_palabra_secreta(self):
        self.palabra_secreta = self.line_edit_palabra_secreta.text().lower()
        self.line_edit_palabra_secreta.clear()

        if self.palabra_secreta:
            # Mostrar los elementos del juego y ocultar los elementos de configuración
            self.label_palabra.setText("_ " * len(self.palabra_secreta))
            self.label_intentos.setText("Intentos restantes: " + str(self.intentos))
            self.label_palabra.show()
            self.label_intentos.show()
            self.line_edit.show()
            self.button.show()
            self.label_instrucciones.hide()
            self.line_edit_palabra_secreta.hide()
            self.button_palabra_secreta.hide()

    def actualizar_palabra_mostrada(self):
        palabra_mostrada = ' '.join([letra if letra in self.letras_adivinadas else '_' for letra in self.palabra_secreta])
        self.label_palabra.setText(palabra_mostrada)

    def adivinar_letra(self):
        letra = self.line_edit.text().lower()
        self.line_edit.clear()

        if len(letra) != 1 or not letra.isalpha():
            return  # Solo se permite una letra

        if letra in self.letras_adivinadas:
            return  # Letra ya adivinada

        self.letras_adivinadas.append(letra)

        if letra not in self.palabra_secreta:
            self.intentos -= 1
            self.label_intentos.setText("Intentos restantes: " + str(self.intentos))

        self.actualizar_palabra_mostrada()
        self.groupBox.repaint()  # Actualizar el dibujo del ahorcado

        if "_" not in self.label_palabra.text():
            self.label_intentos.setText("¡Felicidades! ¡Has adivinado la palabra!")
            self.button.setEnabled(False)

        if self.intentos <= 0:
            self.label_intentos.setText("¡Lo siento! La palabra era: " + self.palabra_secreta)
            self.button.setEnabled(False)

    def paintEvent(self, event):
        painter = QPainter(self.groupBox)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(QColor(0, 0, 0))

        # Calcular las posiciones relativas dentro del QGroupBox
        offset_x = 20
        offset_y = 20
        ancho = self.groupBox.width() - 40
        alto = self.groupBox.height() - 40

        # Dibujar el ahorcado según el número de intentos restantes
        if self.intentos <= 5:
            painter.drawLine(offset_x, alto, ancho, alto)  # Base
        if self.intentos <= 4:
            painter.drawLine((ancho // 2), alto, (ancho // 2), offset_y)  # Poste vertical
        if self.intentos <= 3:
            painter.drawLine((ancho // 2), offset_y, ancho - offset_x, offset_y)   # Poste horizontal
        if self.intentos <= 2:
            painter.drawLine(ancho - offset_x, offset_y, ancho - offset_x, offset_y + 30)   # Cuerda
        if self.intentos <= 1:
            painter.drawEllipse(QRect(ancho - offset_x - 20, offset_y + 30, 40, 40))  # Cabeza
        if self.intentos == 0:
            painter.drawLine(ancho - offset_x, offset_y + 70, ancho - offset_x, offset_y + 130)  # Cuerpo
            painter.drawLine(ancho - offset_x, offset_y + 90, ancho - offset_x - 20, offset_y + 110)  # Brazo izquierdo
            painter.drawLine(ancho - offset_x, offset_y + 90, ancho - offset_x + 20, offset_y + 110)  # Brazo derecho
            painter.drawLine(ancho - offset_x, offset_y + 130, ancho - offset_x - 20, offset_y + 150)  # Pierna izquierda
            painter.drawLine(ancho - offset_x, offset_y + 130, ancho - offset_x + 20, offset_y + 150)  # Pierna derecha

# Código para ejecutar la aplicación
if __name__== '__main__':
    app = QApplication(sys.argv)
    ventana = Ahorcado()
    sys.exit(app.exec_())