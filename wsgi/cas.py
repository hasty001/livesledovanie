from datetime import tzinfo, timedelta, datetime

HOUR = timedelta(hours=2)
# v zime +1 oproti UTC.
# v lete +2

class UTC(tzinfo):
    """UTC"""

    def utcoffset(self, dt):
        return HOUR

    def tzname(self, dt):
        return "UTC+1"

    def dst(self, dt):
        return HOUR

def cas():
    utc = UTC()
    d = datetime.now(tz=utc)
    return d

print "toto je koniec cas.py"