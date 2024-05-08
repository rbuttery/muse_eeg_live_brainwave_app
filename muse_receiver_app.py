import sys
import threading
from collections import defaultdict
from datetime import datetime
from PyQt6.QtWidgets import (QApplication, QVBoxLayout, QWidget, QScrollArea, QHBoxLayout, QComboBox,
                             QLabel, QPushButton, QDoubleSpinBox, QFileDialog)
from PyQt6.QtCore import QTimer
import pyqtgraph as pg
from pythonosc import dispatcher, osc_server

class OSCDataPlotter():
    def __init__(self, ip="127.0.0.1", port=7000):
        self.ip = ip
        self.port = port
        self.live_data = []
        self.endpoints = defaultdict(list)

        self.dispatcher = dispatcher.Dispatcher()
        self.dispatcher.map("*", self.generic_handler)

        self.server_thread = threading.Thread(
            target=lambda: osc_server.ThreadingOSCUDPServer((self.ip, self.port), self.dispatcher).serve_forever()
        )
        self.server_thread.start()

        self.main_widget = QWidget()
        self.layout = QVBoxLayout(self.main_widget)

        self.ctrl_widget = QWidget()
        self.ctrl_layout = QHBoxLayout(self.ctrl_widget)
        self.layout.addWidget(self.ctrl_widget)

        self.stream_box = QComboBox()
        self.ctrl_layout.addWidget(self.stream_box)
        self.stream_box.activated.connect(self.stream_change)

        self.time_range_label = QLabel("Time Range (s):")
        self.ctrl_layout.addWidget(self.time_range_label)
        self.time_range_spin = QDoubleSpinBox()
        self.time_range_spin.setRange(1, 3600)
        self.time_range_spin.setValue(15)
        self.time_range_spin.setSingleStep(1)
        self.ctrl_layout.addWidget(self.time_range_spin)

        self.save_button = QPushButton("Save Data")
        self.ctrl_layout.addWidget(self.save_button)
        self.save_button.clicked.connect(self.save_data)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)

        self.plots = []
        self.curves_list = []
        self.values = self.endpoints

        self.main_widget.setLayout(self.layout)
        self.scroll.setWidget(self.main_widget)
        self.scroll.show()

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_plot)
        self.timer.timeout.connect(self.update_stream_box)
        self.timer.start(100)

    def generic_handler(self, address: str, *args):
        dateTimeObj = datetime.now()
        if address not in self.endpoints:
            self.endpoints[address] = [str(i) for i in range(len(args))]
        self.live_data.append([dateTimeObj] + [address] + list(args))

    def update_plot(self):
        if not self.values:
            return
        now = datetime.now()
        def filter_data(address, value_index):
            return [
                data[2 + value_index] for data in self.live_data
                if data[1] == address and (now - data[0]).total_seconds() <= self.time_range_spin.value()
            ]
        for idx, (value, plot, curve) in enumerate(zip(self.values, self.plots, self.curves_list)):
            data = filter_data(self.endpoint, idx)
            if data:
                curve.setData(data)

    def stream_change(self, index):
        if index < 0:
            return
        self.endpoint = self.stream_box.itemText(index)
        for plot in self.plots:
            self.layout.removeWidget(plot)
            plot.close()
        self.plots = []
        self.curves_list = []
        self.values = self.endpoints[self.endpoint]
        for idx, value in enumerate(self.values):
            plot = pg.plot(title=f"{value} (from {self.endpoint}) Data")
            plot.setLabel("bottom", "Time Step")
            curve = plot.plot(pen=pg.mkPen(pg.intColor(idx, 6)), name=value)
            self.curves_list.append(curve)
            self.plots.append(plot)
            self.layout.addWidget(plot)

    def save_data(self):
        def filter_selected_data():
            return [data for data in self.live_data if data[1] == self.endpoint]
        save_path, _ = QFileDialog.getSaveFileName(None, "Save Data", "", "CSV Files (*.csv);;All Files (*)")
        if save_path:
            with open(save_path, 'w') as file:
                selected_data = filter_selected_data()
                for data in selected_data:
                    file.write(','.join([str(x) for x in data]) + '\n')

    def update_stream_box(self):
        current_streams = sorted(self.endpoints.keys())
        active_streams = [self.stream_box.itemText(i) for i in range(self.stream_box.count())]
        new_streams = set(current_streams) - set(active_streams)
        for stream in new_streams:
            self.stream_box.addItem(stream)

    def run(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_plot)
        self.timer.timeout.connect(self.update_stream_box)
        self.timer.start(100)
        sys.exit(app.exec())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    osc_data_plotter = OSCDataPlotter(port=7000)
    osc_data_plotter.run()