from feedoo.abstract_action import AbstractAction
from feedoo.hash_storage import HashStorage
from feedoo.event import Event
import time
import dns.resolver
import multiprocessing
import itertools
import socket

def query(ip:str, domain:list):
    reverse_ip = ".".join(ip.split(".")[::-1])
    try:
        dns.resolver.resolve('{}.{}'.format(reverse_ip, domain), 'A')
        return domain
    except dns.resolver.NXDOMAIN as e:
        return None

def query_dnsbls(ip:str, domains:list, _query=query):

    tmp = {"percent_score": 0, "domains":[]}
    matching = 0
    with multiprocessing.Pool() as p:
        results = p.starmap(_query, zip(itertools.cycle([ip]), domains))

    for domain in results:
        if domain is not None:
            matching += 1
            tmp["domains"].append(domain)
    tmp["percent_score"] = 100.0 * matching / len(domains)
    return tmp


class FilterDnsbl(AbstractAction):
    def __init__(self, match:str, tag:str, key:str, threshold_percent:int, domains:list, alert:dict, db_path:str=None, db_table:str="default_table", timeout:int=3600):
        AbstractAction.__init__(self, match)
        self._domaines = domains # domains to request
        self._cache = HashStorage(db_path, timeout, db_table)
        self._timeout = timeout
        self._last_trigger = 0
        self._key = key
        self._tag = tag
        self._threshold_percent = threshold_percent
        self._alert = alert

    def do(self, event:tuple, _query_dnsbls=query_dnsbls):
        if self._key in event.record:
            ip = event.record[self._key]
            try:
                socket.inet_aton(ip)
            except socket.error:
                self._log.warning("Ip {} is not valid".format(ip))
                return event
                
            if ip not in self._cache:
                self._cache[ip] = _query_dnsbls(ip, self._domaines)
                
            if self._cache[ip]["percent_score"] >= self._threshold_percent:
                # ip is in blacklist
                alert_record = dict(self._alert)
                alert_record["timestamp"] = int(time.time())
                alert_record["key"] = self._key
                alert_record["value"] = ip
                alert_record["domains"] = ",".join(self._cache[ip]["domains"])

                return [event, Event(self._tag, int(time.time()), alert_record)]

        return event

    def update(self, _time=time.time):
        if _time() - self._last_trigger > self._timeout/10:
            self._last_trigger = _time()
            for ip in tuple(self._cache.get_timeout(_time)):
                del self._cache[ip]





