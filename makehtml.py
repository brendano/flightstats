from __future__ import division
import csv,os
from cStringIO import StringIO

import codes

top = """
    <meta content="text/html; charset=utf-8" http-equiv="Content-Type"/>
    <link rel="stylesheet" href="mytheme.css" >
    <script type="text/javascript" src="https://ajax.googleapis.com/ajax/libs/jquery/1.9.0/jquery.min.js"></script> 
    <script type="text/javascript" src="http://brenocon.com/js/tablesorter/2.7.2/js/jquery.tablesorter.min.js"></script> 
    <script>
    $(document).ready(function() 
        { 
            $("table").tablesorter();
        } 
    ); 
    </script>

    <style>
    .pctsign { font-size: 80%; padding-left: 0.3em; }
    .sel { text-decoration: underline; }
    .nav { font-size: 80%; }
    .content { margin: 1em; }

    </style>

    <h1>Historical On-time Performance of U.S. Flights</h1>

"""

def info(out):
    print>>out, """
    <p>This is calculated from historical data from June 2014 through June 2015.
    <ul>
    <li><b>Failure Rate:</b> The percentage of flights that are cancelled or diverted.
    <li><b>Delay Rate:</b> The percentage of flights that arrive more than 1 hour after their scheduled arrival time.
    </ul>
    """

def navstuff(out, curpage):
    def condlink(pagename, text):
        if curpage==pagename:
            return """<span class=sel>%s</span>""" % text
        return """<a href="%s">%s</a>""" % (pagename, text)

    print>>out, "<div class=nav>"
    print>>out, "View performance:"
    print>>out, condlink("carriers.html", "by carrier")
    print>>out, condlink("airports.html", "by airport")
    # print>>out, condlink("origin.html", "by origin")
    print>>out, condlink("pair.html", "by route")
    print>>out, condlink("month.html", "by month")
    print>>out, "&nbsp;&nbsp;&nbsp;", condlink("about.html", "About this website")
    print>>out, "</div>"

def makepage(filename, title, niceinfo, content, no_info=False):
    f = "html/" + filename
    print f
    with open(f,'w') as fp:
        print>>fp, top
        print>>fp, "<title>%s</title>" % title
        navstuff(fp, filename)
        print>>fp, "<hr><div class=content>"
        print>>fp, "<div class=pageinfo>%s</div>" % niceinfo
        if not no_info: info(fp)
        print>>fp, content
        print>>fp, "</div>"

def nicenum(prob):
    pct = round(prob*1000)/10
    return str(pct) + "<span class=pctsign>%</span>"

def niceint(num):
    return "{:,}".format(num)

def maketable(csvfile, do_name_lookups=True):
    out = StringIO()
    fp = open("summary_data/" + csvfile)
    rows = csv.reader(iter(fp))
    header = rows.next()
    assert header[-5:] == ["n","pfail_raw","pdelay1hr_raw","pfail","pdelay1hr"]
    infokeys = header[:-5]
    # print>>out, "<table>"
    print>>out, "<table cellpadding=3 border=1 cellspacing=0>"
    print>>out, "<thead>"
    print>>out, "<tr>"
    for k in infokeys:
        print>>out, "<th>" + k
    print>>out, "<th>Num. Flights"
    print>>out, "<th>Failure Rate", "<th>Delay Rate"
    print>>out, "</thead>"

    print>>out, "<tbody>"
    for d in csv.DictReader(open("summary_data/" + csvfile)):
        print>>out, "<tr>"
        for k in infokeys:
            print>>out, "<td>"
            s = codes.getname(d[k]) if do_name_lookups else d[k]
            print>>out, s
        print>>out, "<td>", niceint(int(d['n']))
        print>>out, "<td>", nicenum(float(d['pfail']))
        print>>out, "<td>", nicenum(float(d['pdelay1hr']))
    print>>out, "</tbody>"
    print>>out, "</table>"
    return out.getvalue()

def make_airport_table(csvfile, do_name_lookups=True):
    out = StringIO()

    print>>out, "<table cellpadding=3 border=1 cellspacing=0>"
    print>>out, "<thead>"
    print>>out, "<tr>"
    print>>out, "<th>", "Airport"
    print>>out, "<th>Num. Incoming Flights"
    print>>out, "<th>Incoming Failure Rate", "<th>Incoming Delay Rate"
    print>>out, "<th>Num. Outgoing Flights"
    print>>out, "<th>Outgoing Failure Rate", "<th>Outgoing Delay Rate"
    print>>out, "</thead>"

    print>>out, "<tbody>"
    for d in csv.DictReader(open("summary_data/" + csvfile)):
        print>>out, "<tr>"
        print>>out, "<td>", codes.getname(d["ORIGIN"])
        print>>out, "<td>", niceint(int(d['n.x']))
        print>>out, "<td>", nicenum(float(d['pfail.x']))
        print>>out, "<td>", nicenum(float(d['pdelay1hr.x']))
        print>>out, "<td>", niceint(int(d['n.y']))
        print>>out, "<td>", nicenum(float(d['pfail.y']))
        print>>out, "<td>", nicenum(float(d['pdelay1hr.y']))
    print>>out, "</tbody>"
    print>>out, "</table>"
    return out.getvalue()


h = maketable("rank_carrier.csv")
makepage("carriers.html", "Carrier Performance", "Which carriers are on-time? This shows the percentage of flights that arrive late, for each carrier.", h)
makepage("dest.html", "Destination Performance",
    """Which <i>destination</i> airports are on-time?
    For a particular airport, this shows the percentage of flights that arrive to them late.
    """,
    maketable("rank_dest.csv"))
makepage("origin.html", "Origin Performance",
    """Which <i>origin</i> airports are on-time?
    For all flights that leave a particular airport,
    this shows the percentage that 
    get to their destination late.
    """,
    maketable("rank_origin.csv"))
makepage("month.html", "Month (season) performance",
    "Which times of the year tend to have on-time flights?  For each month, this shows the percentage of flights that month that are late.",
    maketable("rank_month.csv"))
makepage("pair.html", "Route performance",
"""Which routes are on time? For each route (an origin and destination), this shows the percentage of flights that arrive to their destination late.   <P><b>Note:</b> routes with a small number of flights, like less than 1000, show much higher failure and delay rates than they really have had.  See the <a href="about.html">about page</a> for an explanation.""",
        maketable("rank_pair.csv", do_name_lookups=False))

makepage("airports.html", "Airport Performance",
        """For each airport, how many <i>incoming</i> and <i>outgoing</i>
        flights are on-time?
        This defines whether a flight is on-time by when it arrives at its destination.
        """,
        make_airport_table("rank_airports.csv"))


grand_total = sum(int(d['n']) for d in csv.DictReader(open("summary_data/rank_month.csv")))

makepage("about.html", "About this website", """
        <h1>About</h1>
        <p>This website displays on-time performance
        by U.S. airlines and carriers,
        as collected by the Bureau of Transportation Statistics,
        with data
        from <a href="http://www.transtats.bts.gov/DL_SelectFields.asp?Table_ID=236">this site</a>.
        The current numbers are based on historical records from
        June 2014 through June 2015, only for flights between 
        the busiest 100 airports during this period.
        This is {grand_total:,} flights total.

        <p>
        Percentages show worst-case delay rates and failure rates.
        If there are a large number of flights, this is just the historical percentage.
        If there only a small number of flights,
        that simple calculation might look lower than it really is just due to luck.
        To remedy this, we instead show the worst-case rate:
        the true percentage has a 98% chance of being lower than what we show.
        (It's not really a worst-case; call it a "98% worst case". 
        The calculation is the upper side of a <a href="https://en.wikipedia.org/wiki/Binomial_proportion_confidence_interval">Agresti-Coull</a> confidence interval.)
        Therefore our numbers are overly harsh for, say, routes with only a few dozen flights; there's not enough data on them to trust they will have a small delay rate in the future.

        <p>Much more sophisticated statistical analysis methods are possible
        for this problem.
        For example, these calculations aren't very good at
        assigning blame between
        the carrier, origin airport, and destination airport.
        In the meantime, the code and data is available at
        <a href="https://github.com/brendano/flightstats">github.com/brendano/flightstats</a>.

        <p>Website created by <a href="http://brenocon.com/">Brendan O'Connor</a>.

        """.format(**locals()),
        "",
        no_info=True
        )

with open("html/index.html",'w') as fp:
    print>>fp, """
<meta http-equiv="refresh" content="0; url=http://brenocon.com/flightstats/carrier.html">
"""

