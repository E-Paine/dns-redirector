class Component:

    def __init__(self, server, thread):
        self.thread = thread
        self.server = server

    def start(self):
        self.thread.start()

    def join(self):
        self.thread.join()

    def shutdown(self):
        self.server.shutdown()
