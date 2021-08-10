from typing import List
import re
import logging


class DataRefiner:

    def __init__(self):
        self.max_value_pos: float = 0  # pos = positive
        self.min_value_pos: float = 0
        self.max_value_neu: float = 0  # methods missing
        self.min_value_neu: float = 0  # methods missing
        self.max_value_neg: float = 0  # methods missing
        self.min_value_neg: float = 0  # methods missing
        self.max_value_title_pos: float = 0  # methods missing
        self.min_value_title_pos: float = 0  # methods missing
        self.max_value_title_neu: float = 0  # methods missing
        self.min_value_title_neu: float = 0  # methods missing
        self.max_value_title_neg: float = 0  # methods missing
        self.min_value_title_neg: float = 0  # methods missing
        self.line_count_raw_data = 0
        self.line_count_raw_data_results = 0

# Setter
    def set_max_pos(self, value): #ggf. nicht benötigt
        self.max_value_pos = value

    def set_min_pos(self, value): #ggf. nicht benötigt
        self.min_value_pos = value

    def set_line_count_data(self, value):
        self.line_count_raw_data = value

    def set_line_count_result(self, value):
        self.line_count_raw_data_results = value

# Getter
    def get_max_pos(self): #ggf. nicht benötigt
        return self.max_value_pos

    def get_min_pos(self): #ggf. nicht benötigt
        return self.min_value_pos

    def get_line_count_data(self):
        return self.line_count_raw_data

    def get_line_count_result(self):
        return self.line_count_raw_data_results

# Methods
    # check if the amount of lines is equal between raw data and result
    def check_line_count(self) -> bool:
        if self.line_count_raw_data_results == self.line_count_raw_data:
            logging.debug("Line count equal: continue computation")
            return True
        else:
            logging.debug("Line Count unequal: double check filenames and make sure the code is not interrupted")
            print_warning()
            return False

    # parses the SequenceClassifierObject into a 'clean' string // Edit from wiser David: NO it doesn't it returns a list in a list, need to fix
    @staticmethod
    def clear_logits(logits): # -> tuple[List, List]:
        raw = str(logits).split('\n')
        clean_title_logits = re.findall('[-]?\d+[.]\d+|[-]?\d+[.]\d+e[+]*[-]*\d', raw[0])
        clean_text_logits = re.findall('[-]?\d+[.]\d+|[-]?\d+[.]\d+e[+]*[-]*\d', raw[1])
        return clean_title_logits, clean_text_logits

    @staticmethod
    def clear_value(value: [str]) -> List:
        return (re.findall('[-]?\d+[.]\d+|[-]?\d+[.]\d+e[+]*[-]*\d', value))

    def find_amplitude(self, tensors: List[List[str]]):
        for values in tensors:
            value = values[0].split(',')
            try:
                for x in range(3):
                    value[x] = self.clear_value(value[x])
            except IndexError as error:
                logging.error("Tensor values missing for title", error)
                print_warning()

            if float(value[0][0]) > self.max_value_title_pos:          # clear_value gives back a list in a list, need to fix !! NOT WORKING SO FAR (REGEX macht mich fertig...)
                self.max_value_title_pos = float(value[0][0])          # the matrices are a hack but it should work with it
            if float(value[0][0]) < self.min_value_title_pos:
                self.min_value_title_pos = float(value[0][0])
            if float(value[1][0]) > self.max_value_title_neg:
                self.max_value_title_neg = float(value[1][0])
            if float(value[1[0]]) < self.min_value_title_neg:
                self.min_value_title_neg = float(value[1][0])
            if float(value[2][0]) > self.max_value_title_neu:
                self.max_value_title_neu = float(value[2][0])
            if float(value[2][0]) < self.min_value_title_neu:
                self.min_value_title_neu = float(value[2][0])

            value = values[1].split(',')
            try:      # meckert wegen duplizierung, mir fällt aber im moment nicht ein wie man das anders lösen sollte da es eben nicht genau der gleiche code ist
                for x in range(3):
                    value[x] = self.clear_value(value[x])
            except IndexError as error:
                logging.error("Tensor values missing for body", error)
                print_warning()

                if float(value[0][0]) > self.max_value_pos:
                    self.max_value_pos = float(value[0][0])
                if float(value[0][0]) < self.min_value_pos:
                    self.min_value_pos = float(value[0][0])
                if float(value[1][0]) > self.max_value_neg:
                    self.max_value_neg = float(value[1][0])
                if float(value[1][0]) < self.min_value_neg:
                    self.min_value_neg = float(value[1][0])
                if float(value[2][0]) > self.max_value_neu:
                    self.max_value_neu = float(value[2][0])
                if float(value[2][0]) < self.min_value_neu:
                    self.min_value_neu = float(value[2][0])
        logging.info("Found all amplitudes")


def print_warning():
    print("Warning: check 'pipeline.log'")
