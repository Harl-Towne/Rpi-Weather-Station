from PyQt5.QtCore import QThreadPool, QRunnable


class workerGeneric(QRunnable):

    def __init__(self, fcn, callback, *args, **kwargs):
        super(workerGeneric, self).__init__()
        self.fcn = fcn
        self.args = args
        self.kwargs = kwargs
        self.callback = callback

    def run(self):
        self.fcn(*self.args, **self.kwargs)
        self.callback()


def threadqueuing(fcn):
    def queuing_fcn(*args2, **kwargs2):
        threadQueue.enqueue(fcn, *args2, **kwargs2)

    return queuing_fcn


class threadQueue:
    threadpool = QThreadPool()
    queue = list()
    executing = False

    @staticmethod
    def enqueue(fcn, *args, **kwargs):
        threadQueue.queue.append((fcn, args, kwargs))
        if not threadQueue.executing:
            threadQueue._advance_queue()

    @staticmethod
    def _task_complete():  # DON'T YOU EVER FUCKING DARE CALL THIS FUNCTION MANUALLY
        if len(threadQueue.queue) > 0:
            threadQueue._advance_queue()
        else:
            threadQueue.executing = False

    @staticmethod
    def _advance_queue():  # DON'T YOU EVER FUCKING DARE CALL THIS FUNCTION MANUALLY
        threadQueue.executing = True
        next_task = threadQueue.queue.pop()
        worker = workerGeneric(next_task[0], threadQueue._task_complete, *next_task[1], **next_task[2])
        threadQueue.threadpool.start(worker)
