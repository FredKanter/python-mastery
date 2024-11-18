# sol2_2.py

'''
1. How many bus routes exist in Chicago?

2. How many people rode the number 22 bus on February 2, 2011?
What about any route on any date of your choosing?

3. What is the total number of rides taken on each bus route?

4. What five bus routes had the greatest ten-year increase in ridership 
from 2001 to 2011?
'''

from pprint import pprint
import random
from collections import defaultdict, Counter

import my_Solutions.readrides as rr

def print_route_utilization(route, rpd):
    # rpd: routes per date
    passengers = rpd[route][-1]
    print(f"On {route[1]} {passengers} people rode on bus " 
          f"number {route[0]}")
    
def count_rides(routes):
    rides_counter = Counter()
    for route in routes:
        rides_counter[route['route']] += route['rides']
    return rides_counter

# (1)
def count_routes(routes):
    unique_routes = {route['route'] for route in routes}
    print(f'Chicago has {len(unique_routes)} bus routes')

# (2)
def count_passengers(route, getRandom=False):
    routes_per_date = defaultdict(list)
    for route in route:
        routes_per_date[(route['route'], route['date'])].append(route['daytypes'])
        routes_per_date[(route['route'], route['date'])].append(route['rides'])
    
    print_route_utilization(('22', '02/02/2011'), routes_per_date)

    # get random entry from rows and check in routes_per_date
    if getRandom:
        rand_indx = random.randint(1, len(rows))
        random_route = (rows[rand_indx]['route'], rows[rand_indx]['date'])
        print_route_utilization(random_route, routes_per_date)

# (3)
def total_nb_rides(route):
    total_rides = count_rides(route)
    pprint(total_rides.most_common(15))

# (4)
def ridership_increase(rows):
    # Filter rides from 2001 to 2011
    year_2001 = [row for row in rows if '2001' in row['date']]
    year_2011 = [row for row in rows if '2011' in row['date']]

    # Count total rides for each route for that year
    total_rides_2001 = count_rides(year_2001)
    total_rides_2011 = count_rides(year_2011)
    top_increase_routes = (total_rides_2011 - total_rides_2001).most_common(5)
    pprint(top_increase_routes)

if __name__ == '__main__':
    file_ctabus = '..\Data\ctabus.csv'
    rows = rr.read_rides_as_dict(file_ctabus)

    count_routes(rows)
    count_passengers(rows)
    total_nb_rides(rows)
    ridership_increase(rows)