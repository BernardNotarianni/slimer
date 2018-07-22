import sys
import logging
import threading
import traceback
import ListSerializer
import ListDeserializer
from ListExecutor import ListExecutor

import socketserver

class SlimRequestHandler(socketserver.StreamRequestHandler):

    def __init__(self, request, client_address, server):
        self.logger = logging.getLogger('SlimRequestHandler')
        self.logger.debug('__init__')
        socketserver.StreamRequestHandler.__init__(self, request, client_address, server)
        return


    def handle(self):
        self.logger.debug("slim request handle started")
        self.wfile.write(b'Slim -- V0.3\n')

        running = True
        while running:
            instructionLength = int(self.rfile.read(6))
            self.rfile.read(1)
            instructions = self.rfile.read(instructionLength).decode('utf-8')
            self.logger.debug("len={} data={}".format(instructionLength, instructions))

            if instructions == 'bye':
                self.logger.debug("'bye' received")
                running = False
            else:
                statements = ListDeserializer.deserialize(instructions)
                self.executor = ListExecutor()
                results = self.executor.execute(statements)
                x = ListSerializer.serialize(results)
                response = '%06d:%s' % (len(x), x)
                self.logger.debug("reponse={}".format(response))
                self.wfile.write(response.encode('utf-8'))

        self.logger.debug("server shutdown requested")
        self.server.done()

class SlimerServer(socketserver.ThreadingMixIn, socketserver.TCPServer):

    def __init__(self, host, port):
        self.logger = logging.getLogger('SlimServer')
        self.logger.debug('__init__')
        self.logger.info("starting server on {}:{}".format(host, port))
        super().__init__((host, port), SlimRequestHandler)

    def done(self):
        self.logger.info("shutting down server")
        self.shutdown()


class StreamToLogger(object):
    """
    Fake file-like stream object that redirects writes to a logger instance.
    """
    def __init__(self, logger, log_level=logging.INFO):
        self.logger = logger
        self.log_level = log_level
        self.linebuf = ''

    def write(self, buf):
        for line in buf.rstrip().splitlines():
            self.logger.log(self.log_level, line.rstrip())

    def flush(self):
        return



logging.basicConfig(
   level=logging.DEBUG,
   format='%(asctime)s:%(levelname)s:%(name)s:%(message)s',
   filename="slimer.log",
   filemode='a'
)

stdout_logger = logging.getLogger('STDOUT')
sl = StreamToLogger(stdout_logger, logging.INFO)
sys.stdout = sl

stderr_logger = logging.getLogger('STDERR')
sl = StreamToLogger(stderr_logger, logging.ERROR)
sys.stderr = sl

logging.debug('args : %s' % sys.argv)
path = sys.argv[1]

port =  int(sys.argv[2])
host = 'localhost'
logging.debug('starting slim server at host={} port={}'.format(host, port))

# Activate the server; this will keep running until you
# interrupt the program with Ctrl-C
server = SlimerServer(host, port)
server.serve_forever()

logging.debug("server terminated")

