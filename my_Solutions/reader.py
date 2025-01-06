# reader.py

import csv
import collections
import tracemalloc
from sys import intern
from abc import ABC, abstractmethod
from typing import List, Dict, IO


class CSVParser(ABC):
    def parse(self, filename):
        records = []
        with open(filename) as f:
            rows = csv.reader(f)
            headers = next(rows)
            for row in rows:
                record = self.make_record(headers, row)
                records.append(record)
        return records

    @abstractmethod
    def make_record(self, headers, row):
        pass

class DictCSVParser(CSVParser):
    def __init__(self, types):
        self.types = types

    def make_record(self, headers, row):
        return { name: func(val) for name, func, val in zip(headers, self.types, row) }

class InstanceCSVParser(CSVParser):
    def __init__(self, cls):
        self.cls = cls

    def make_record(self, headers, row):
        return self.cls.from_row(row)

class DataCollection(collections.abc.Sequence):
    def __init__(self):
        # Each value is a list with all the values (a column)
        self.routes = []
        self.dates = []
        self.daytypes = []
        self.numrides = []
        
    def __len__(self):
        # All lists assumed to have the same length
        return len(self.routes)

    def __getitem__(self, index):
        # check for slice tuple
        if isinstance(index, slice):
            # check for missing step size
            step = 1 if index.step is None else index.step
            # create new DataCollection object with sliced data
            sliced_dc = DataCollection()  
            for sub_index in range(index.start, index.stop, step):
                record = {'route': self.routes[sub_index],
                          'date': self.dates[sub_index],
                          'daytype': self.daytypes[sub_index],
                          'rides': self.numrides[sub_index]}
                sliced_dc.append(record)
            return sliced_dc
        else:
            return { 'route': self.routes[index],
                    'date': self.dates[index],
                    'daytype': self.daytypes[index],
                    'rides': self.numrides[index] }

    def append(self, d):
        self.routes.append(d['route'])
        self.dates.append(d['date'])
        self.daytypes.append(d['daytype'])
        self.numrides.append(d['rides'])


def read_rides_as_columns(filename, types=[str, str, str, int]):
    '''
    Read the bus ride data. General purpose version (ex2_6)
    '''
    records = DataCollection()
    with open(filename) as f:
        rows = csv.reader(f)
        headers= next(rows)
        for row in rows:
            records.append({ name:func(val) for name, func, val in zip(headers, types, row) })
    return records

# Depricated ex5.1 - keep for documentation purposes
'''
    def read_csv_as_dicts(filename, coltypes):
        parser = DictCSVParser(coltypes)
        record = parser.parse(filename)
        return record

    def read_csv_as_instances(filename, cls):
        \'''
        Read a CSV file into a list of instances
        \'''
        parser = InstanceCSVParser(cls)
        records = parser.parse(filename)
        return records
'''

# TODO add type hints
def read_csv_as_dicts(filename: str, headers=None) -> List[Dict]:
    '''
    Read CSV data into a list of dictionaries with optional type conversion
    ''' 
    with open(filename) as file:
        records = csv_as_dicts(file, headers=headers)
    return records

def csv_as_dicts(file, types: List, headers=None) -> List[Dict]:
    '''
    Read CSV data into a list of dictionaries with optional type conversion
    '''
    rows = csv.reader(file)
    records = []
    if headers is None:
        print(f'No headers provided. Extract headers from first row.')
        headers = next(rows)    
    for row in rows:
        record = { name: func(val) 
                    for name, func, val in zip(headers, types, row) }
        records.append(record)
    return records

def read_csv_as_instances(filename: str) -> List:
    '''
    Read CSV data into a list of instances
    '''
    with open(filename) as file:
        records = csv_as_instances(file)
    return records

def csv_as_instances(file: IO, cls) -> List:
    '''
    Read CSV data into a list of instances
    '''
    rows = csv.reader(file)
    records = []
    headers = next(rows)
    for row in rows:
        record = cls.from_row(row)
        records.append(record)
    return records

def check_mem_usage():
    # check memory for str
    tracemalloc.start()
    data = read_rides_as_columns('..\\Data\\ctabus.csv', [str, str, str, int])
    print(f'Mem usage for str: {tracemalloc.get_traced_memory()}') 

    # check memory for intern
    data = read_rides_as_columns('..\\Data\\ctabus.csv', [intern, intern, str, int])
    print(f'Mem usage for intern: {tracemalloc.get_traced_memory()}')

if __name__ == '__main__':
    check_mem_usage()