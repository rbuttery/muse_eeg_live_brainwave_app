import sys
from datetime import datetime
from pythonosc import dispatcher, osc_server

class OSCHandler:
    def __init__(self, ip, port, to_csv=False):
        self.ip = ip 
        self.port = port
        self.to_csv = to_csv
        self.dispatcher = dispatcher.Dispatcher()
        self.file = None
        if self.to_csv:
            # Open a file to write data
            self.file = open(f"eeg_data_{datetime.now().strftime('%Y%m%d%H%M%S')}.csv", 'w')

    def add_handler(self, address, handler):
        self.dispatcher.map(address, handler)

    def start(self):
        server = osc_server.ThreadingOSCUDPServer((self.ip, self.port), self.dispatcher)
        print(f"Listening for OSC messages on {self.ip}:{self.port}")
        server.serve_forever()

    def close_file(self):
        if self.file:
            self.file.close()

def eeg_handler(address, *args):
    dateTimeObj = datetime.now()
    printStr = dateTimeObj.strftime("%Y-%m-%d %H:%M:%S.%f")
    for arg in args:
        printStr += "," + str(arg)
    if handler.to_csv:
        handler.file.write(printStr + '\n')
    else:
        print(printStr)

if __name__ == "__main__":
    to_csv = False
    # Check if the user wants to export data to CSV
    if len(sys.argv) > 1 and sys.argv[1] == '--to-csv':
        to_csv = True

    handler = OSCHandler("127.0.0.1", 7000, to_csv)
    handler.add_handler("/muse/eeg", eeg_handler)
    try:
        handler.start()
    except KeyboardInterrupt:
        print("Shutting down server.")
        handler.close_file()
