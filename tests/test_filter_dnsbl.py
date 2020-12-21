from feedoo.filter.filter_dnsbl import FilterDnsbl, query, query_dnsbls
from feedoo.event import Event
import unittest
import time

def relative_time(ts):
    def _time():
        return ts + time.time()
    return _time

# WARNING : following test do request and result may change ! 
# To fix, we need to find a stable "bad" IP

IP = "1.2.3.4"
DNSBL_LIST = [
    "feb.spamlab.com",
	"rbl.spamlab.com",
	"all.spamrats.com",
	"dyna.spamrats.com"
]
class TestFilterDnsbl(unittest.TestCase):
    def test_query(self):
        domain = query("1.2.3.4", "ipbl.zeustracker.abuse.ch")
        self.assertEqual(domain, None)

    def test_query_2(self):
        domain = query("1.2.3.4", "all.spamrats.com")
        self.assertEqual(domain, "all.spamrats.com")

    def test_query_dnsbls(self):
        result = query_dnsbls(IP, DNSBL_LIST)

        expected = {'percent_score': 25.0, 'domains': ['dyna.spamrats.com']}

    def test_do_ko(self):
        filter_dnsbl = FilterDnsbl(
            match="*", 
            tag="alert",
            key="ip", 
            threshold_percent=50, 
            domains="DNSBL_LIST", 
            alert={"title":"ip blacklisted !"}
        )

        def mock_query_dnsbls(ip, domains):
            return {'percent_score': 50.0, 'domains': ['dyna.spamrats.com', 'all.spamrats.com']}

        event = Event("netflow", 123456789, {"ip":"2.3.4.5"})
        result = filter_dnsbl.do(event, mock_query_dnsbls)
        
        self.assertEqual(len(result), 2)


    def test_do_ok(self):
        filter_dnsbl = FilterDnsbl(
            match="*", 
            tag="alert",
            key="ip", 
            threshold_percent=50, 
            domains="DNSBL_LIST", 
            alert={"title":"ip blacklisted !"}
        )

        def mock_query_dnsbls(ip, domains):
            return {'percent_score': 25.0, 'domains': ['dyna.spamrats.com']}

        event = Event("netflow", 123456789, {"ip":"2.3.4.5"})
        result = filter_dnsbl.do(event, mock_query_dnsbls)

        self.assertEqual(result, event)

    def test_update_1(self):
        filter_dnsbl = FilterDnsbl(
            match="*", 
            tag="alert",
            key="ip", 
            threshold_percent=50, 
            domains="DNSBL_LIST", 
            alert={"title":"ip blacklisted !"}
        )

        def mock_query_dnsbls(ip, domains):
            mock_query_dnsbls.counter += 1
            return {'percent_score': 25.0, 'domains': ['dyna.spamrats.com']}

        mock_query_dnsbls.counter = 0

        event = Event("netflow", 123456789, {"ip":"2.3.4.5"})
        filter_dnsbl.do(event, mock_query_dnsbls)
        filter_dnsbl.update(relative_time(3800)) # remove cache
        filter_dnsbl.do(event, mock_query_dnsbls)

        # cache have been deleted by update (timeout)
        # so query_dnsbls must be called twice
        self.assertEqual(mock_query_dnsbls.counter, 2)





