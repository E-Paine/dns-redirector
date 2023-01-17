class Component:

    def __init__(self, thread, server):
        self._thread = thread
        self._server = server

    def start(self):
        self._thread.start()

    def join(self):
        self._thread.join()

    def shutdown(self):
        self._server.shutdown()
