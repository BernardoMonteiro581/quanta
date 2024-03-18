import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton,  QInputDialog
from PyQt6.QtGui import QPainter, QColor, QPen
from PyQt6.QtCore import Qt
import pyqtgraph as pg
import matplotlib.pyplot as plt
from miniquanta import identify_high_volatility
from miniquanta import get_forex_data

class CandlestickChart(QWidget):
    def __init__(self, data, parent=None):
        super().__init__(parent)
        self.data = data
        self.setMinimumSize(800, 600)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        width = int(self.width() / max(len(self.data), 1))
        max_price = max(day['high'] for day in self.data)
        min_price = min(day['low'] for day in self.data)
        price_range = max_price - min_price

        green_color = QColor(0, 255, 0)
        red_color = QColor(255, 0, 0)
        
        for i, day in enumerate(self.data):
            x = int(i * width)
            y_high = int((max_price - day['high']) / price_range * self.height())
            y_low = int((max_price - day['low']) / price_range * self.height())
            y_open = int((max_price - day['open']) / price_range * self.height())
            y_close = int((max_price - day['close']) / price_range * self.height())

            if y_close > y_open :
                painter.setBrush(green_color)
                painter.drawRect(x, y_close, width, y_open - y_close)
            else:
                painter.setBrush(red_color)
                painter.drawRect(x, y_open, width, y_close - y_open)

        # converter argumentos float para int para evitar o erro
            rect_width = int(width * 0.4)
            rect_height = int(max(1, abs(y_close - y_open)))
            painter.drawRect(x + int(width * 0.3), min(y_open, y_close), rect_width, rect_height)

           
            painter.drawLine(x + int(width * 0.5), y_high, x + int(width * 0.5), y_low)


class ForexAnalysisApp(QMainWindow):
    def __init__(self, data):
        super().__init__()
        self.setWindowTitle("Forex Analysis")
        self.centralWidget = QWidget()
        self.layout = QVBoxLayout(self.centralWidget)
        self.setCentralWidget(self.centralWidget)
        
        self.data = data
        
        # Criar botão para escolher moeda
        self.symbol_button = QPushButton("Change Symbol")
        self.symbol_button.clicked.connect(self.change_symbol)
        self.layout.addWidget(self.symbol_button)
        
        # Inicializar o gráfico com a moeda padrão
        self.update_chart('EURUSD')  # Moeda padrão
        
    def update_chart(self, symbol):
        # Limpar o layout antes de atualizar o gráfico
        for i in reversed(range(self.layout.count())):
            self.layout.itemAt(i).widget().setParent(None)
        
        # Atualizar o gráfico com a nova moeda
        self.symbol = symbol
        self.chart_widget = CandlestickChart(get_forex_data(symbol))
        self.layout.addWidget(self.chart_widget)
        
    def change_symbol(self):
        items = ['EURUSD', 'GBPUSD', 'USDJPY']  # Lista de moedas disponíveis
        item, ok = QInputDialog.getItem(self, "Change Symbol", 
                                         "Select Symbol:", items, 0, False)
        if ok and item:
            self.update_chart(item)
        # Implementar a lógica para alterar a moeda quando o botão for clicado
        # Por exemplo, você pode abrir um diálogo de seleção de moeda aqui
        # ou implementar a lógica para escolher a moeda de uma lista predefinida
        pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    symbol = 'EURUSD'  # Moeda padrão
    data = get_forex_data(symbol)
    high_volatility_dates = identify_high_volatility(data, 20, 0.005)
    print("High Volatility Dates:", high_volatility_dates)
    main_window = ForexAnalysisApp(data)
    main_window.show()
    sys.exit(app.exec())
