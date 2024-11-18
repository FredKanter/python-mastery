import csv
#from collections import namedtuple
import collections
import tracemalloc


class RideData(collections.abc.Sequence):
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
            # create new RideData object with sliced data
            sliced_RideData = RideData()  
            for sub_index in range(index.start, index.stop, step):
                record = {'route': self.routes[sub_index],
                          'date': self.dates[sub_index],
                          'daytype': self.daytypes[sub_index],
                          'rides': self.numrides[sub_index]}
                sliced_RideData.append(record)
            return sliced_RideData
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

class Rides:
    def __init__(self, route, date, daytypes, rides) -> None:
        self.route = route
        self.date = date
        self.daytypes = daytypes
        self.rides = rides

class RidesSlots:
    __slots__ = ['route', 'date', 'daytype', 'rides']
    def __init__(self, route, date, daytype, rides):
        self.route = route
        self.date = date
        self.daytype = daytype
        self.rides = rides

def read_rides_as_tuples(filename):
    '''
    Read the bus ride data as a list of tuples
    '''
    records = []
    with open(filename) as f:
        rows = csv.reader(f)
        headings = next(rows)     # Skip headers
        for row in rows:
            route = row[0]
            date = row[1]
            daytype = row[2]
            rides = int(row[3])
            record = (route, date, daytype, rides)
            records.append(record)
    return records

def read_rides_as_dict(filename):
    '''
    Read the bus ride data as a list of dicts
    '''
    #records = [] -> changed with ex2_5
    records = RideData()
    with open(filename) as f:
        rows = csv.reader(f)
        headings = next(rows)     # Skip headers
        for row in rows:
            record = {'route': row[0],
                      'date': row[1],
                      'daytype': row[2],
                      'rides': int(row[3])}
            records.append(record)
    return records

def read_rides_as_class(filename):
    '''
    Read the bus ride data as a list of class Rides instances
    '''
    records = []
    with open(filename) as f:
        rows = csv.reader(f)
        headings = next(rows)     # Skip headers
        for row in rows:
            records.append(Rides(row[0],
                                 row[1],
                                 row[2],
                                 int(row[3])))
    return records

def read_rides_as_class_slots(filename):
    '''
    Read the bus ride data as a list of class RidesSlots instances
    '''
    records = []
    with open(filename) as f:
        rows = csv.reader(f)
        headings = next(rows)     # Skip headers
        for row in rows:
            records.append(RidesSlots(row[0],
                                      row[1],
                                      row[2],
                                      int(row[3])))
    return records

def read_rides_as_named_tuples(filename):
    '''
    Read the bus ride data as a list of named_tuples
    '''
    Row = collections.namedtuple('Row', ['route', 'date', 'daytype', 'rides'])
    records = []
    with open(filename) as f:
        rows = csv.reader(f)
        headings = next(rows)     # Skip headers
        for row in rows:
            records.append(Row(row[0],
                               row[1],
                               row[2],
                               int(row[3])))
    return records

def read_rides_as_columns(filename):
    '''
    Read the bus ride data into 4 lists, representing columns
    '''
    routes = []
    dates = []
    daytypes = []
    numrides = []
    with open(filename) as f:
        rows = csv.reader(f)
        headings = next(rows)     # Skip headers
        for row in rows:
            routes.append(row[0])
            dates.append(row[1])
            daytypes.append(row[2])
            numrides.append(int(row[3]))
    return dict(routes=routes, dates=dates, daytypes=daytypes, numrides=numrides)

if __name__ == '__main__':
    filename = '..\Data\ctabus.csv'
    all_read_methods = [(read_rides_as_tuples, 'tuples'),
                        (read_rides_as_dict, 'dict (mod)'),
                        (read_rides_as_class, 'class'),
                        (read_rides_as_class_slots, 'class_slots'),
                        (read_rides_as_named_tuples, 'named_tuples')]

    for mth, name in all_read_methods:
        tracemalloc.start()
        rows = mth(filename)
        current, peak = tracemalloc.get_traced_memory()
        print(f'Method: {name:15s} Memory Use: Current {current:d}, Peak {peak:d}')
    #print('Memory Use: Current %d, Peak %d' % tracemalloc.get_traced_memory())