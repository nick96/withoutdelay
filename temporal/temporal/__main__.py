import logging

from temporal import server

logging.basicConfig(level=logging.INFO)
server.serve()