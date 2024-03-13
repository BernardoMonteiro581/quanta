import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout
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
        width = self.width() / max(len(self.data), 1)
        max_price = max(day['high'] for day in self.data)
        min_price = min(day['low'] for day in self.data)
        price_range = max_price - min_price

        for i, day in enumerate(self.data):
            x = int(i * width)
            y_high = int((max_price - day['high']) / price_range * self.height())
            y_low = int((max_price - day['low']) / price_range * self.height())
            y_open = int((max_price - day['open']) / price_range * self.height())
            y_close = int((max_price - day['close']) / price_range * self.height())

            if y_close > y_open :
                painter.setPen(pg.mkPen('g'))
                painter.setPen (pg.mkBrush('g'))
            else:
                painter.setPen(pg.mkPen('r'))
                painter.setPen (pg.mkBrush('r'))

        # converter argumentos float para int para evitar o erro
            rect_width = int(width * 0.4)
            rect_height = int(max(1, abs(y_close - y_open)))
            painter.drawRect(x + int(width * 0.3), min(y_open, y_close), rect_width, rect_height)

           
            painter.drawLine(x + int(width * 0.5), y_high, x + int(width * 0.5), y_low)





class ForexAnalysisApp(QMainWindow):
    def __init__(self, data):
        super().__init__()
        self.setWindowTitle("Forex Analysis")
        self.setCentralWidget(CandlestickChart(data))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    symbol = 'EURUSD'
    data = get_forex_data(symbol)
    high_volatility_dates = identify_high_volatility(data, 20, 0.005)  # Exemplo: janela de 20 dias, limiar de 0.5%
    print("High Volatility Dates:", high_volatility_dates)
    main_window = ForexAnalysisApp(data)
    main_window.show()
    sys.exit(app.exec())
