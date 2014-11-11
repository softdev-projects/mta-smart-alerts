from datetime import datetime
import urllib2
import xml.etree.ElementTree as ET

MTA_SERVICE_STATUS_URL = 'http://web.mta.info/status/serviceStatus.txt'


def service_status():
    service_status_xml = urllib2.urlopen(MTA_SERVICE_STATUS_URL).read()
    return MTASubwayStatus(service_status_xml)


class MTASubwayStatus(object):
    '''
    Represents the MTA subway service status at a certain point in time.
    '''

    def __init__(self, response_xml):
        self.raw_xml = response_xml
        self.xml_tree = ET.fromstring(response_xml)
        self.retrieved_at = self._parse_time()
        self.delays = self._parse_delays()

    def _parse_time(self):
        timestamp = self.xml_tree.find('timestamp').text
        format_string = '%m/%d/%Y %I:%M:%S %p'
        return datetime.strptime(timestamp, format_string)

    def _parse_delays(self):
        delays = []
        for line in self.xml_tree.find('subway'):
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
        self.time = datetime.strptime(line_node.find('Time').text.strip(),
                                      '%I:%M%p')