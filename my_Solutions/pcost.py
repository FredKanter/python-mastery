def portfolio_cost(filename):
    cost = 0
    types = (str, int, float)

    with open(filename, 'r') as f:
        for lineno, line in enumerate(f):
            items = line.split(' ')
            try:
                items = [func(item) for item, func in zip(items, types)]
                cost += items[1] * items[2]
            except ValueError as e:
                print(f'Could´t parse line {lineno}: {items}')
                print(f'Reason: {e}')
            
    return cost

if __name__ == '__main__':
    filename = '..\\Data\\portfolio.dat'
    #filename = '..\\Data\\portfolio3.dat'
    print(f'Total cost: {portfolio_cost(filename)}')