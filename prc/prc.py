################################################################################
############################## Classes #########################################
################################################################################
import code

class PRC(code.InteractiveConsole):
    """
        Main PRC class

        Variables:
        _queue          - Data queue

    """
    def raw_input(self,prompt=None):
        """
            Raw input for interpreter

            Input:
            data        - Input python code string

            Returns:
            data
        """
        return self._queue.get()

    def set_queue(self,queue):
        """
            Sets input queue

            Input:
            queue       - Data queue

            Returns:
            Nothing
        """
        self._queue = queue

################################################################################
############################## Functions #######################################
################################################################################


if __name__=="__main__":
    import threading
    import Queue
    import time

    data_queue = Queue.Queue()
    prc = PRC()
    prc.set_queue(data_queue)
    th = threading.Thread(target=prc.interact)
    th.daemon = True
    th.start()

    data_queue.put("pass")
    data_queue.put("pass")
    data_queue.put("pass")
    data_queue.put("import sys")
    data_queue.put("print sys.path")
    data_queue.put("def kkk():")
    data_queue.put("    print 'aaa'")
    data_queue.put("")
    data_queue.put("kkk()")

    time.sleep(1)
