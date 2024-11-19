# tableformat.py
from abc import ABC, abstractmethod


class TableFormatter(ABC):
    @abstractmethod
    def headings(self, headers):
        pass

    @abstractmethod
    def row(self, rowdata):
        pass

class ColumnFormatMixin:
    formats = []
    def row(self, rowdata):
        rowdata = [(fmt % d) for fmt, d in zip(self.formats, rowdata)]
        super().row(rowdata)

class UpperHeadersMixin:
    def headings(self, headers):
        super().headings([h.upper() for h in headers])
    
class TextTableFormatter(TableFormatter):
    def headings(self, headers):
        print(' '.join('%10s' % h for h in headers))
        print(('-'*10 + ' ')*len(headers))
    
    def row(self, rowdata):
        print(' '.join('%10s' % d for d in rowdata))

class CSVTableFormatter(TableFormatter):
    def headings(self, headers):
        print(','.join('%s' % h for h in headers))
        #print(('-'*10 + ' ')*len(headers))
    
    def row(self, rowdata):
        print(','.join('%s' % d for d in rowdata))

class HTMLTableFormatter(TableFormatter):
    def headings(self, headers):
        print('<tr> '+' '.join('<th>%s</th>' % h for h in headers)+' </tr>')

    def row(self, rowdata):
        print('<tr> '+' '.join('<td>%s</td>' % d for d in rowdata)+' </tr>')


def create_formatter(format,
                     column_formats=[],
                     upper_headers=False):
    '''
    if format == 'text':
        return  TextTableFormatter()
    elif format == 'csv':
        return CSVTableFormatter()
    elif format == 'html':
        return HTMLTableFormatter()
    else:
        raise NotImplementedError()
    '''
    if format not in ['text', 'csv', 'html']:
        raise NotImplementedError()
    all_base_formatter =  {'text': TextTableFormatter,
                           'csv': CSVTableFormatter,
                           'html': HTMLTableFormatter}
    base_formatter = all_base_formatter[format]

    if column_formats and upper_headers:
        # Clean to define class in func?
        class PortfolioFormatter(ColumnFormatMixin,
                                 UpperHeadersMixin,
                                 base_formatter):
            formats = column_formats
        return PortfolioFormatter()
    elif column_formats:
        class PortfolioFormatter(ColumnFormatMixin, base_formatter):
            formats = column_formats
        return PortfolioFormatter()
    elif upper_headers:
        class PortfolioFormatter(UpperHeadersMixin, base_formatter):
            pass
        return PortfolioFormatter()
    else:
        return base_formatter() 


def print_table(seq_obj, attr_names, formatter):
    # check formatter class
    if not isinstance(formatter, TableFormatter):
        raise TypeError('Expected a TableFormatter')
    # print headers
    formatter.headings(attr_names)

    for s in seq_obj:
        rowdata = [getattr(s, name) for name in attr_names]
        formatter.row(rowdata)

