from PySide6.QtCore import QThreadPool
from Backend.Worker import Worker

#There wasn't a good place to put this so I've placed it here for now.
threadpool = QThreadPool().globalInstance()
def run_func_async(event,worker_func,*args,**kwargs):
    worker = Worker(event,worker_func,*args,**kwargs)
    threadpool.start(worker)