import logging

# Creates a logging file for easy debugging and failure searching -> pipeline.log
class Documenter:

    def __init__(self):
        logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', datefmt='%d/%m/%Y %H:%M:%S', # Date in German format, if desired change it
                            filename='pipeline.log', filemode='w', level=logging.DEBUG)
