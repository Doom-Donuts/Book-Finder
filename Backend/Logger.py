import threading
from datetime import datetime

class Logger:
    def __init__(self, filename):
        self.filename = filename
        self.lock = threading.Lock()
        self.Log("-----New Session Started-----\n")
    
    def Log(self,text):
        #Get the current time in the format Y-M-D H:M:S.
        time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[ {time} ]: {text}" 
        self.write_to_file(log_message)

    def write_to_file(self,text):
        #Make sure that no thread is currently writing to the log file
        with self.lock:
            with open(self.filename, "a") as f:
                f.write(text + "\n")

main_logger = Logger("log.txt")
    
        
        

