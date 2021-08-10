from typing import List
import csv
import sys
import logging


class CsvHandler:

    def __init__(self, datarefiner):
        self.output = []
        self.line_count = 0
        self.row_count = 0
        self.headline_row = 0
        self.target_row = 0
        self.id_row = 0
        self.date_row = 0
        self.refiner = datarefiner

# Load a CSV file into a list
# Mode will determine which kind of CSV is committed
# Mode = 0 for the raw data CSV, Mode = 1 for the resulted CSV
    def load_csv(self, source: [str], mode: [int]) -> List[List[str]]:

        self.output = []
        self.line_count = 0
        self.row_count = 0
        self.headline_row = 0
        self.target_row = 0
        self.id_row = 0
        self.date_row = 0                                    # reset counter and output on every new method call

        with open(source, encoding='utf-8') as csv_file:     # try to open CSV file
            try:
                csv_reader = csv.reader(csv_file, delimiter=';')
            except csv.Error as error:
                sys.exit("file {}, line {}: {}".format(source, csv_reader.line_num, error))
            logging.info("CSV successfully loaded")

            if mode == 0:
                try:                                          # try to get the first line
                    headline = csv_reader.__next__()
                except csv.Error as error:
                    sys.exit("file {}, line {}: {}".format(source, csv_reader.line_num, error))

                logging.info("Searching desired data")
                for x in headline:                            # find desired rows in CSV
                    if x == '"title"' or x == 'title':
                        self.headline_row = self.row_count
                        self.row_count += 1
                    elif x == '"body"' or x == 'body':
                        self.target_row = self.row_count
                        self.row_count += 1
                    elif x == '"id"' or x == 'id':
                        self.id_row = self.row_count
                        self.row_count += 1
                    elif x == '"date"' or x == 'date':
                        self.date_row = self.row_count
                        self.row_count += 1
                    else:
                        self.row_count += 1
                logging.info("Desired data found")

                logging.info("Convert CSV into List")                # clear data of unnecessary information
                for row in csv_reader:
                    if not row:                 # catch empty row
                        continue
                    self.output.append([row[self.id_row], row[self.date_row],
                                        row[self.headline_row], row[self.target_row]])
                    self.line_count += 1

                logging.info(f"Converting was successful: {self.line_count} Lines")
                self.refiner.set_line_count_data(self.line_count)  # push line_count to the DataRefiner Class
                if not self.output:
                    logging.error("Seems like your data CSV is empty, double check that CSV file has data in it")
                    sys.exit("data CSV file empty")
                else:
                    return self.output

            if mode == 1:
                try:  # try to get the first line
                    headline = csv_reader.__next__()
                except csv.Error as error:
                    sys.exit("file {}, line {}: {}".format(source, csv_reader.line_num, error))

                logging.info("Searching desired tensors")
                for x in headline:  # find desired rows in CSV
                    if x == 'title':
                        self.headline_row = self.row_count
                        self.row_count += 1
                    elif x == 'body':
                        self.target_row = self.row_count
                        self.row_count += 1
                    else:
                        self.row_count += 1
                logging.info("Desired tensors found")

                logging.info("Convert CSV into List")  # clear data of unnecessary information
                for row in csv_reader:
                    if not row:                         # catch empty row
                        continue
                    self.output.append([row[self.headline_row], row[self.target_row]])
                    self.line_count += 1
                logging.info("Tensors successfully converted")

                self.refiner.set_line_count_result(self.line_count)    # push line_count to the DataRefiner Class
                if not self.output:
                    logging.error("Seems like your result CSV is empty, double check that CSV file has data in it")
                    sys.exit("Result CSV file empty")
                else:
                    return self.output

            else:
                logging.error("Wrong MODE in [load_csv]: Mode must be 0 or 1 {load_csv('Filename','Mode')}")
                sys.exit("Wrong Mode to load any CSV, check 'pipeline.log'")

# Create a CSV file for the results
    @staticmethod
    def create_result_csv(filename: [str]):
        try:
            with open(filename, 'w', encoding='utf-8') as csv_file:
                csv_writer = csv.writer(csv_file, delimiter=';')
                csv_writer.writerow(["id", "date", "title", "body"])
        except csv.Error as error:
            logging.error("Could not create CSV file for results [create_result_csv]")
            sys.exit("file {}, line {}: {}".format(filename, csv_writer, error))

# Create a CSV file for the results
    @staticmethod
    def create_value_csv(filename: [str]):
        try:
            with open(filename, 'w', encoding='utf-8') as csv_file:
                csv_writer = csv.writer(csv_file, delimiter=';')
                csv_writer.writerow(["max_positive", "min_positive", "max_neutral",
                                     "min_neutral", "max_negative", "min_negative"])
        except csv.Error as error:
            logging.error("Could not create CSV file for values [create_value_csv]")
            sys.exit("file {}, line {}: {}".format(filename, csv_writer, error))

# Write a List into a CSV file (appending)
    @staticmethod
    def write_result_csv(filename: [str], arg1: [str], arg2: [str], arg3: [str], arg4: [str]):
        try:
            with open(filename, 'a+', encoding='utf-8', newline='') as csv_file:
                csv_writer = csv.writer(csv_file, delimiter=';')
                csv_writer.writerow([arg1, arg2, arg3, arg4])
        except csv.Error as error:
            logging.error("Could not find CSV file for results [write_result_csv]")
            sys.exit("file {}, line {}: {}".format(filename, csv_writer, error))
        logging.info("Result saved")
