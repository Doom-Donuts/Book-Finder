from PySide6.QtCore import QObject, Signal


class WorkerSignals(QObject):
    """Signals from a running worker thread.

    finished
        No data

    error
        tuple (exctype, value, traceback.format_exc())

    result
        object data returned from processing, anything

    Code adapted from Martin Fitzpatrick, 
    https://www.pythonguis.com/tutorials/multithreading-pyside6-applications-qthreadpool/
    """
    
    finished = Signal()
    error = Signal(tuple)
    result = Signal(object)

class Events(QObject):
    EventList = {}

    def get_signals(self,event):
        if event not in self.EventList:
            raise Exception("Error: attempted to get event that does not exist")
        else:
            return self.EventList[event]
            

    #Function that allows you to subscribe to an existing type of event
    def subscribe(self, event, error_funcs=None, result_funcs=None, finished_func=None):
        if event not in self.EventList:
            print("Error: event requested doesn't exist")

        if error_funcs is not None:
            for func in error_funcs:
                self.EventList[event].error.connect(func)
        
        if result_funcs is not None:
            for func in result_funcs:
                self.EventList[event].result.connect(func)

        if finished_func is not None:
            for func in finished_func:
                self.EventList[event].finished.connect(func)
    
    #Function that creates a new type of event
    def create_event(self,event_name):
        self.EventList[event_name] = WorkerSignals()



event_list = Events()

