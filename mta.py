from datetime import datetime
import urllib2
import xml.etree.ElementTree as ET

MTA_SERVICE_STATUS_URL = 'http://web.mta.info/status/serviceStatus.txt'


def service_status():
    service_status_xml = urllib2.urlopen(MTA_SERVICE_STATUS_URL).read()
    tree = ET.fromstring(service_status_xml)
    return MTASubwayStatus(tree)


class MTASubwayStatus(object):
    '''
    Represents the MTA subway service status at a certain point in time.
    '''

    def __init__(self, response_xml):
        self.raw_xml = response_xml
        self.retrieved_at = self._parse_time()
        self.delays = self._parse_delays()

    def _parse_time(self):
        timestamp = self.raw_xml.find('timestamp').text
        format_string = '%m/%d/%Y %I:%M:%S %p'
        return datetime.strptime(timestamp, format_string)

    def _parse_delays(self):
        delays = []
        for line in self.raw_xml.find('subway'):
            if self._line_delayed(line):
                delays.append(MTASubwayDelay(line))
        return delays

    def _line_delayed(self, line_node):
        return line_node.find('status').text == 'DELAYS'

    def has_delays(self):
        return bool(self.delays)


class MTASubwayDelay(object):
    def __init__(self, line_node):
        self.line = line_node.find('name').text
        self.info = line_node.find('text').text
        self.date = datetime.strptime(line_node.find('Date').text, '%m/%d/%Y')
        self.time = datetime.strptime(line_node.find('Time').text, '%I:%M%p')