import csv


class CsvInfo:
    def __init__(self, reader: csv.DictReader):
        self.headers = next(reader)
        self.lines = reader.line_num
        self.data_types = reader.fieldnames
