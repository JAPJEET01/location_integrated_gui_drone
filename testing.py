
from PyQt5 import Qt, QtCore
from gnuradio import qtgui
from gnuradio import analog
from gnuradio import gr
from gnuradio.filter import firdes
from PyQt5.QtWidgets import QLabel, QHBoxLayout, QApplication, QFrame, QVBoxLayout, QWidget, QLineEdit, QTableWidget, QTableWidgetItem, QCheckBox, QSizePolicy, QScrollArea
from gnuradio import uhd
from gnuradio.fft import window
import sys
import signal
import sip
from gnuradio import network
import csv
import subprocess
import time
import iridium
import serial
# import firebase_reader
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
# from gnuradio import uhd

import random
from PyQt5.QtWidgets import QTableWidgetItem

import openpyxl

new_freq = 40e6
from PyQt5.QtCore import QTimer


cred = credentials.Certificate("rpigps-229ad-firebase-adminsdk-88p3l-c6b5f0113f.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://rpigps-229ad-default-rtdb.firebaseio.com/'
})

# Reference to the database
ref = db.reference('/data')
root_ref = db.reference('/')
root_ref.delete()
x='500'



def handle_change(event):
            global x
            if len(event.data) == 21:
                x = event.data

ref.listen(handle_change)

print(x)
class DarkPalette:
    def __init__(self):
        self.primary_color = Qt.QColor(53, 53, 53)
        self.secondary_color = Qt.QColor(35, 35, 35)
        self.tertiary_color = Qt.QColor(42, 130, 218)
        self.text_color = Qt.QColor(255, 255, 255)
        self.disabled_text_color = Qt.QColor(127, 127, 127)
        self.background_color = Qt.QColor(25, 25, 25)
        self.disabled_background_color = Qt.QColor(45, 45, 45)
        self.highlight_color = Qt.QColor(42, 130, 218)

    def apply(self, app):
        app.setStyle("Fusion")
        dark_palette = Qt.QPalette()
        dark_palette.setColor(Qt.QPalette.Window, self.background_color)
        dark_palette.setColor(Qt.QPalette.WindowText, self.text_color)
        dark_palette.setColor(Qt.QPalette.Base, self.secondary_color)
        dark_palette.setColor(Qt.QPalette.AlternateBase, self.background_color)
        dark_palette.setColor(Qt.QPalette.ToolTipBase, self.secondary_color)
        dark_palette.setColor(Qt.QPalette.ToolTipText, self.text_color)
        dark_palette.setColor(Qt.QPalette.Text, self.text_color)
        dark_palette.setColor(Qt.QPalette.Disabled, Qt.QPalette.Text, self.disabled_text_color)
        dark_palette.setColor(Qt.QPalette.Button, self.secondary_color)
        dark_palette.setColor(Qt.QPalette.ButtonText, self.text_color)
        dark_palette.setColor(Qt.QPalette.Disabled, Qt.QPalette.ButtonText, self.disabled_text_color)
        dark_palette.setColor(Qt.QPalette.BrightText, self.highlight_color)
        dark_palette.setColor(Qt.QPalette.Link, self.tertiary_color)
        dark_palette.setColor(Qt.QPalette.Highlight, self.highlight_color)
        dark_palette.setColor(Qt.QPalette.Disabled, Qt.QPalette.Highlight, self.disabled_background_color)
        dark_palette.setColor(Qt.QPalette.HighlightedText, self.text_color)
        dark_palette.setColor(Qt.QPalette.Disabled, Qt.QPalette.HighlightedText, self.disabled_text_color)

        app.setPalette(dark_palette)


class Testing(gr.top_block, Qt.QWidget):
    def __init__(self):
        gr.top_block.__init__(self, "Not titled yet", catch_exceptions=True)
        screen_resolution = Qt.QDesktopWidget().screenGeometry()
        width = screen_resolution.width() // 2
        height = screen_resolution.height() // 2
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Not titled yet")
        self.setGeometry(0, 0, width, height)
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except BaseException as exc:
            print(f"Qt GUI: Could not set Icon: {str(exc)}", file=sys.stderr)
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "testing")

        self.settings = Qt.QSettings("GNU Radio", "simple")
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frequency)
        self.toggle_frequency = False  # Flag to toggle between two frequencies
        self.timer.start(5)

        try:
            geometry = self.settings.value("geometry")
            if geometry:
                self.restoreGeometry(geometry)
        except BaseException as exc:
            print(f"Qt GUI: Could not restore geometry: {str(exc)}", file=sys.stderr)

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 20e6
        self.freq = freq = 40e6

       
        ##################################################
        # Blocks
        ##################################################

        self.uhd_usrp_source_0 = uhd.usrp_source(
            ",".join(("", '')),
            uhd.stream_args(
                cpu_format="fc32",
                args='',
                channels=list(range(0,1)),
            ),
        )
        self.uhd_usrp_source_0.set_samp_rate(samp_rate)
        self.uhd_usrp_source_0.set_time_unknown_pps(uhd.time_spec(0))

        self.uhd_usrp_source_0.set_center_freq(70e6, 0)
        self.uhd_usrp_source_0.set_antenna("RX2", 0)
        self.uhd_usrp_source_0.set_gain(50, 0)

        self.iridium_fft_burst_tagger_0 = iridium.fft_burst_tagger(1626000000, (1024*16), int(samp_rate), 1000, 1000,
                                    100, 0, 0, 7, 512, False)
        
        self.iridium_iuchar_to_complex_2 = iridium.iuchar_to_complex()

        # self.network_tcp_source_1 = network.tcp_source.tcp_source(itemsize=gr.sizeof_gr_complex*1,addr='127.0.0.1',port=6000,server=False)
        

        # Create a new frame
        self.new_frame = Qt.QFrame()
        self.new_layout = Qt.QHBoxLayout(self.new_frame)
        
        # Logo
        self.logo_label = Qt.QLabel(self)
        pixmap = Qt.QPixmap('logo.png')  # Replace 'logo.png' with your logo file
        pixmap_scaled = pixmap.scaledToWidth(100)  # Adjust the width as needed
        self.logo_label.setPixmap(pixmap_scaled)
        self.new_layout.addWidget(self.logo_label, 0, QtCore.Qt.AlignRight)

        # Heading Text
        self.heading_label = Qt.QLabel("RF DRISTI MAP", self)
        self.heading_label.setStyleSheet("font-size: 25px; font-weight: bold;")  # Adjust font size and style as needed
        self.new_layout.addWidget(self.heading_label, 0, QtCore.Qt.AlignLeft)
        self.top_layout.addWidget(self.new_frame)

        # Input Fields
        self.input_label1 = Qt.QLabel("FREQUENCY RANGE:", self)
        self.input_field1 = Qt.QLineEdit(self)
        self.input_label2 = Qt.QLabel("SUB FREQUENCY RANGE:", self)
        self.input_field2 = Qt.QLineEdit(self)
        self.input_label3 = Qt.QLabel("RESOLUTION:", self)
        self.input_field3 = Qt.QLineEdit(self)

        self.top_layout.addWidget(self.input_label1)
        self.top_layout.addWidget(self.input_field1)
        self.top_layout.addWidget(self.input_label2)
        self.top_layout.addWidget(self.input_field2)
        self.top_layout.addWidget(self.input_label3)
        self.top_layout.addWidget(self.input_field3)

        # After adding input fields, create a new frame for displaying .csv data
        self.csv_frame = Qt.QFrame()
       
        
       
        self.csv_layout = QVBoxLayout(self.csv_frame)
        self.top_layout.addWidget(self.csv_frame)

        # Create a table widget to display .csv data
        self.csv_table = Qt.QTableWidget()
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidget(self.csv_table)
        self.scroll_area.setWidgetResizable(True)
        self.csv_layout.addWidget(self.scroll_area)

        # Function to load .csv file
        # self.load_excel('file.xlsx')
        # self.load_csv('/home/usrp/Documents/usrp_python_codes/output.csv')
        self.csv_timer = Qt.QTimer()
        self.csv_timer.timeout.connect(self.update_csv_column)
        self.csv_timer.timeout.connect(self.load_csv)
        self.csv_timer.start(1000)

        # Waterfall Sink
        self.qtgui_waterfall_sink_x_0 = qtgui.waterfall_sink_c(
            4096, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            350000000, #fc
            640000000, #bw
            "", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_waterfall_sink_x_0.set_update_time(0.10)
        self.qtgui_waterfall_sink_x_0.enable_grid(False)
        self.qtgui_waterfall_sink_x_0.enable_axis_labels(True)

        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        colors = [0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_waterfall_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_waterfall_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_waterfall_sink_x_0.set_color_map(i, colors[i])
            self.qtgui_waterfall_sink_x_0.set_line_alpha(i, alphas[i])

        self.qtgui_waterfall_sink_x_0.set_intensity_range(-140, 10)

        self._qtgui_waterfall_sink_x_0_win = sip.wrapinstance(self.qtgui_waterfall_sink_x_0.qwidget(), Qt.QWidget)

        self.top_layout.addWidget(self._qtgui_waterfall_sink_x_0_win)

        ##################################################
        # Connections
        ##################################################


        self.connect((self.iridium_fft_burst_tagger_0, 0), (self.iridium_iuchar_to_complex_2, 0))
        self.connect((self.iridium_iuchar_to_complex_2, 0), (self.qtgui_waterfall_sink_x_0, 0))
        self.connect((self.uhd_usrp_source_0, 0), (self.iridium_fft_burst_tagger_0, 0))

        self.include_drone_detection_checkbox = Qt.QCheckBox("Include Drone Detection")
        self.include_drone_detection_checkbox.setChecked(False)  
        self.top_layout.addWidget(self.include_drone_detection_checkbox)


        self.run_python_script("offline_marker.py") 

        ##################################################
        # Connections
        ##################################################

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "testing")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()
        # self.process.kill()
        event.accept()

    def update_frequency(self):
        global new_freq

        # time.sleep(5)
        current_freq = self.uhd_usrp_source_0.get_center_freq(0)
        new_freq = current_freq + 20e6  # Increment by 10 MHz

        if(new_freq >= 640e6 ):
            new_freq = 40e6

        self.uhd_usrp_source_0.set_center_freq(new_freq, 0)
        print('center freq change to : ', new_freq)



    def load_csv(self, file_path='/home/usrp/Music/final_files/output.csv'):


        with open(file_path, 'r', newline='') as csvfile:
            csv_reader = csv.reader(csvfile)
            data = list(csv_reader)

        data = data[-50:-2]
        max_column = 0
        max_row = len(data)
        if len(data) > 0:
            max_column = max(len(row) for row in data)
        
        self.csv_table.clearContents()
        self.csv_table.setRowCount(max_row)
        self.csv_table.setColumnCount(max_column)
        
        column_headers = ["time", "location", "frequency", "channel magnitude", "channel bandwidth"]
        self.csv_table.setHorizontalHeaderLabels(column_headers[:max_column])
        
        for i, row in enumerate(data):
            for j, cell_value in enumerate(row):
                item = QTableWidgetItem(str(cell_value))
                self.csv_table.setItem(i, j, item)


    def update_csv_column(self, file_path='/home/usrp/Music/final_files/output.csv', column_index=1, new_value=3100):
        # Read the CSV file
        with open(file_path, 'r', newline='') as csvfile:
            csv_reader = csv.reader(csvfile)
            data = list(csv_reader)
        
        # Calculate the range for the latest rows (e.g., the last 50 rows)
        start_index = max(0, len(data) - 170)
        end_index = len(data)
        
        # Update the specified column in the latest rows only
        for i in range(start_index, end_index):
            if len(data[i]) > column_index:
                data[i][column_index] = x
        
        # Write the updated data back to the CSV file
        with open(file_path, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerows(data)



    def read_lat_long_from_serial(self, port='/dev/ttyACM0', baudrate=9600, timeout=1):
    # Initialize the serial port
        ser = serial.Serial(port, baudrate, timeout=timeout)
        
        lat_long_values = []

        try:
            while True:
                # Read a line from the serial port
                line = ser.readline().decode('utf-8').strip()
                if line:
                    # Split the line into latitude and longitude
                    lat_str, long_str = line.split(',')

                    print(line , type(line), str(line))  # Optional: print for debugging

        except KeyboardInterrupt:
            # Handle the exit condition (Ctrl+C)
            print("Exiting...")
        finally:
            # Close the serial port
            ser.close()
        
        return lat_long_values


    def read_last_two_numbers(port='/dev/ttyACM0', baud_rate=9600):
        try:
            # Open the serial port
            ser = serial.Serial(port, baud_rate, timeout=1)
            print(f"Connected to {port} at {baud_rate} baud rate.")
            
            while True:
                if ser.in_waiting > 0:
                    # Read a line from the serial port
                    data = ser.readline().decode('utf-8').rstrip()
                    print(f"Received data: {data}")
                    
                    # Extract all numbers from the data using regular expressions
                    numbers = data.split(',')
                    
                    if len(numbers) >= 2:
                        # Get the last two numbers and return them as a comma-separated string
                        last_two_numbers = f"{numbers[-2]},{numbers[-1]}"
                        return last_two_numbers
    
        except serial.SerialException as e:
            print(f"Error: {e}")
        
        finally:
            if 'ser' in locals() and ser.is_open:
                ser.close()
                print("Serial port closed.")

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.analog_sig_source_x_0.set_sampling_freq(self.samp_rate)
        self.qtgui_waterfall_sink_x_0.set_frequency_range(0, self.samp_rate)

    def run_python_script(self, script_path):
        pass
        # self.process = subprocess.Popen(["python", script_path])
    

    def update_frequency(self):
        global new_freq

        # time.sleep(5)
        current_freq = self.uhd_usrp_source_0.get_center_freq(0)
        new_freq = current_freq + 20e6  # Increment by 10 MHz

        if(new_freq >= 650e6 ):
            new_freq = 40e6

        self.uhd_usrp_source_0.set_center_freq(new_freq, 0)
        # print('center freq change to : ', new_freq)


    

def main(top_block_cls=Testing, options=None):
    qapp = Qt.QApplication(sys.argv)
    dark_palette = DarkPalette()
    dark_palette.apply(qapp)
    tb = top_block_cls()
    tb.start()

    screen_resolution = Qt.QDesktopWidget().screenGeometry()
    width = screen_resolution.width() // 2
    height = screen_resolution.height() - 60
    # tb.resize(height, width)
    # tb.setFixedSize(height, width)
    tb.setFixedWidth(width)
    tb.setFixedHeight(height)
    left_pos = 0
    tb.move(left_pos, 0)

    # process = run_python_script("offline_marker.py")  
    
    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()
        
        Qt.QApplication.quit()



    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
