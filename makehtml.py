from __future__ import division
import csv,os,re,sys
from cStringIO import StringIO

import codes

  # <script src="//code.jquery.com/jquery-1.10.2.js"></script>

    # <script type="text/javascript" src="https://ajax.googleapis.com/ajax/libs/jquery/1.9.0/jquery.min.js"></script> 
    # <script src="http://code.jquery.com/ui/1.11.4/jquery-ui.js"></script>
    # <script src="http://code.jquery.com/jquery-1.10.2.js"></script>
top = """
    <meta content="text/html; charset=utf-8" http-equiv="Content-Type"/>
    <link rel="stylesheet" href="mytheme.css" >
    <link rel="stylesheet" href="https://ajax.googleapis.com/ajax/libs/jqueryui/1.11.4/themes/smoothness/jquery-ui.css">
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js"></script>
        
    <script src="https://ajax.googleapis.com/ajax/libs/jqueryui/1.11.4/jquery-ui.min.js"></script>
    
    <script src="jquery.tablesorter.min.js"></script> 
    <script>
    $(document).ready(function() 
        { 
            $("table").tablesorter();
            $( document ).tooltip();
        } 
    ); 
    </script>

    <style>
    
    .pctsign { font-size: 80%; padding-left: 0.3em; }
    .sel { text-decoration: underline; }
    .nav { font-size: 80%; }
    .content { margin: 1em; }
    hr { margin-top: 1em; margin-bottom: 1em; }
    a.subtle { text-decoration: none }
    a.subtle:hover { text-decoration: underline; }
    a.csvlink { text-decoration: none; font-size: 80%; }
    a.csvlink:hover { text-decoration: underline }

    </style>

    <h1>Historical On-time Performance of U.S. Flights</h1>

"""

overall = list(csv.DictReader(open("summary_data/overall.csv")))[0]

def info(out):
    print>>out, """
    <p>This is calculated from historical data from July 2014 through June 2015.
    <ul>
    <li><b>Failure Rate:</b> The 
    percentage of flights that are cancelled or diverted.
    (Overall: {bigfailrate})

    <li><b>Delay Rate:</b> The 
    percentage of flights that arrive more than 1 hour after their scheduled arrival time,
    or fail to arrive at all.
    (Overall: {bigdelayrate})
    </ul>
    """.format(bigfailrate=nicenum(overall['pfail_raw']),
            bigdelayrate=nicenum(overall['pdelay1hr_raw']))

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
    # print>>out, condlink("pair.html", "by route")
    print>>out, condlink("month.html", "by month")
    print>>out, "&nbsp;&nbsp;&nbsp;", condlink("about.html", "About this website")
    print>>out, "</div>"

def makepage(filename, title, niceinfo, content, no_info=False):
    f = "html/" + filename
    print f
    with open(f,'w') as fp:
        # basepath = "" if "/" not in filename else "../" * filename.count("/")
        print>>fp, top
        print>>fp, "<title>%s</title>" % title
        navstuff(fp, filename)
        print>>fp, "<hr><div class=content>"
        print>>fp, "<div class=pageinfo>%s</div>" % niceinfo
        if not no_info: info(fp)
        print>>fp, content
        print>>fp, "</div>"

def nicenum(prob):
    prob = float(prob)
    pct = round(prob*1000)/10
    return str(pct) + "<span class=pctsign>%</span>"

def niceint(num):
    assert float(num)==int(num)
    num = int(num)
    return "{:,}".format(num)

COUNT_THRESH = 1
num_stat_cols = 7

def rate_td(word, n, raw, est):
    if abs(raw-est) > .001:
        inner = """ ({raw:.1f}% raw, {est:.1f}% estimated)""".format(raw=raw*100,est=est*100)
    else:
        inner = """"""

    return """<td title="{k} {word}{inner}">{estnice}""".format(
            word=word, inner=inner,
            k=int(round(n*raw)), n=int(n),
            estnice=nicenum(est))

def maketable(csvfile, do_name_lookups=True):
    out = StringIO()
    fp = open("summary_data/" + csvfile)
    rows = csv.reader(iter(fp))
    header = rows.next()
    assert set(header[-num_stat_cols:]) == set(["n","pfail_raw","pdelay1hr_raw","pfail_ac","pdelay1hr_ac", "pfail_bayes", "pdelay1hr_bayes"])
    infokeys = header[:-num_stat_cols]
    # print>>out, "<table>"
    print>>out, "<a class=csvlink href='summary_data/%s'>[csv]</a>" % csvfile
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
        if int(d['n']) < COUNT_THRESH: continue

        print>>out, "<tr>"
        for k in infokeys:
            print>>out, "<td>"
            s = linkify(d[k], longname=do_name_lookups)
            print>>out, s

        print>>out, "<td>", niceint(int(d['n']))
        print>>out, rate_td("failed flights", int(d['n']), float(d['pfail_raw']), float(d['pfail_bayes']))
        print>>out, rate_td("delayed flights", int(d['n']), float(d['pdelay1hr_raw']), float(d['pdelay1hr_bayes']))
    print>>out, "</tbody>"
    print>>out, "</table>"
    return out.getvalue()

def carrier_wikilink(carrier_code):
    name = codes.carriers_dict[carrier_code]['name']
    return "https://en.wikipedia.org/wiki/{wikiname}".format(
            wikiname=name.replace(" ","_"),
    )

def linkify(s, longname=True):
    if s in codes.airports_dict:
        h = "<a href={s}.html>{s}</a>".format(s=s)
    elif s in codes.carriers_dict:
        h = "<a href={s}.html>{s}</a>".format(s=s)
    else:
        h = s
    if longname:
        name = codes.getname(s)
        h += " - " + name
    return h

def make_twoway_table(csvfile, col_nicename, col_codename, 
        names=[
        "Num. Outgoing Flights", "Outgoing Failure Rate", "Outgoing Delay Rate",
        "Num. Incoming Flights", "Incoming Failure Rate", "Incoming Delay Rate",],
        do_name_lookups=True):
    out = StringIO()

    print>>out, "<a class=csvlink href='summary_data/%s'>[csv]</a>" % csvfile
    print>>out, "<table cellpadding=3 border=1 cellspacing=0>"
    print>>out, "<thead>"
    print>>out, "<tr>"
    print>>out, "<th>", col_nicename
    for name in names:
        print>>out, "<th>" + name
    print>>out, "</thead>"

    print>>out, "<tbody>"
    for d in csv.DictReader(open("summary_data/" + csvfile)):
        n = max(int(d['n.x']), int(d['n.y']))
        if n < COUNT_THRESH: continue

        print>>out, "<tr>"
        s = d[col_codename]
        print>>out, "<td>", linkify(s, longname=do_name_lookups)
        print>>out, "<td>", niceint(int(d['n.x']))
        print>>out, rate_td("failed flights", int(d['n.x']), float(d['pfail_raw.x']), float(d['pfail_bayes.x']))
        print>>out, rate_td("delayed flights", int(d['n.x']), float(d['pdelay1hr_raw.x']), float(d['pdelay1hr_bayes.x']))
        print>>out, "<td>", niceint(int(d['n.y']))
        print>>out, rate_td("failed flights", int(d['n.y']), float(d['pfail_raw.y']), float(d['pfail_bayes.y']))
        print>>out, rate_td("delayed flights", int(d['n.y']), float(d['pdelay1hr_raw.y']), float(d['pdelay1hr_bayes.y']))
    print>>out, "</tbody>"
    print>>out, "</table>"
    return out.getvalue()

## Top summary pages

h = maketable("rank_carrier.csv")
makepage("carriers.html", "Carrier Performance", 
    """Which carriers are on-time? This shows the percentage of flights that arrive late, for each carrier.""",
h)

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
    "Which times of the year tend to have on-time flights?  For each month, this shows the percentage of flights that month which are late.",
    maketable("rank_month.csv", do_name_lookups=False))

# makepage("pair.html", "Route performance",
# """Which routes are on time? For each route (an origin and destination), this shows the percentage of flights that arrive to their destination late.   <P><b>Note:</b> routes with a small number of flights, like less than 1000, show much higher failure and delay rates than they really have had.  See the <a href="about.html">about page</a> for an explanation.""",
#         maketable("rank_pair.csv", do_name_lookups=False))

makepage("airports.html", "Airport Performance",
        """For each airport, how many <i>incoming</i> and <i>outgoing</i>
        flights are on-time?
        We define whether a flight is on-time by looking at when it arrives at
        its destination.
        """,
        make_twoway_table("rank_airports.csv", "Airport", "ORIGIN")
        )


## Per-Airport breakdowns

all_airports = {d['ORIGIN']:d for d in csv.DictReader(open("summary_data/rank_airports.csv"))}

for airport in all_airports:
# for airport in ["BDL"]:
    print airport
    d=all_airports[airport]

    h_carriers = make_twoway_table("by_airport/%s_carriers.csv" % airport,
            "Carrier", "CARRIER")
    h_ins = maketable("by_airport/%s_ins.csv" % airport, do_name_lookups=False)
    h_outs= maketable("by_airport/%s_outs.csv" % airport, do_name_lookups=False)
    h_outin=make_twoway_table("by_airport/%s_outin.csv" % airport,
            "Airport", "DEST",
            names=[
                "Num. <i>from</i> %s" % airport,
                "Failure Rate <i>from</i> %s" % airport,
                "Delay Rate <i>from</i> %s" % airport,
                "Num. <i>to</i> %s" % airport,
                "Failure Rate <i>to</i> %s" % airport,
                "Delay Rate <i>to</i> %s" % airport,
            ],
            do_name_lookups=False
            )


    makepage("%s.html" % airport, "%s Performance" % airport, """
        Performance for <b>{airport} - {name}</b> ({city})
        """.format(airport=airport, **codes.airports_dict[airport]),
        """
        Rates at {airport}:
        <ul>
        <li>Failure rate: {failrate}
        <li>Delay rate: {delayrate}
        </ul>

        <hr class=subsection>
        Performance for <b>carriers</b> operating flights at this airport:
        {h_carriers}
        <hr class=subsection>
        Performance for the {numroutes} <b>routes</b> in and out of this airport:
        {h_outin}
        """.format(
        failrate=nicenum( 0.5*(float(d['pfail_bayes.x']) + float(d['pfail_bayes.y'])) ),
        delayrate=nicenum(0.5*(float(d['pdelay1hr_bayes.x'])+float(d['pdelay1hr_bayes.y']))),
        numroutes=len(list(open("summary_data/by_airport/%s_outin.csv" % airport)))-1,
            **locals()),
    )


## Per-Carrier breakdowns


all_carriers = {d['CARRIER']: d for d in csv.DictReader(open("summary_data/rank_carrier.csv"))}

for carrier in all_carriers:
    # print carrier
    d = all_carriers[carrier]

    h_pairs = maketable("by_carrier/{carrier}_pairs.csv".format(**locals()),
            do_name_lookups=False)

    h_by_airport = ""

    numroutes = len(list(open("summary_data/by_carrier/{carrier}_pairs.csv".format(**locals())))) - 1

    makepage("%s.html" % carrier, "%s Performance" % carrier,
    """
    <p>Performance for <b>{carrier} - {name}</b>
    <p><a href="{wikilink}">Wikipedia link for {name}</a>
    """.format(wikilink=carrier_wikilink(carrier), name=codes.getname(carrier),
        **locals()),
    """
    Rates for {carrier}:
    <ul>
    <li>Failure rate: {failrate}
    <li>Delay rate: {delayrate}
    </ul>
    <hr>
    <b>{carrier}'s routes:</b>
    This carrier operates {numroutes} routes in the database.
    Here's the failure and delay rates for each route by this carrier.
    {h_pairs}
    
    <!--
    For each airport, here's the failure and delay rates
    for both incoming and outgoing flights operated by this carrier.
    {h_by_airport}
    -->
    """.format(
        failrate=nicenum(float(d['pfail_bayes'])),
        delayrate=nicenum(float(d['pdelay1hr_bayes'])),
        **locals())
    )

grand_total = sum(int(d['n']) for d in csv.DictReader(open("summary_data/rank_month.csv")))

makepage("about.html", "About this website", """
        <h1>About</h1>
        <p>This website displays on-time performance
        by U.S. airlines and airports,
        as collected by the Bureau of Transportation Statistics,
        with data
        from <a href="http://www.transtats.bts.gov/DL_SelectFields.asp?Table_ID=236">this site</a>.
        The numbers are based on historical records from
        one year of historical data (July 2014 through June 2015),
        only for flights between 
        the busiest 100 airports during this period.
        This is {grand_total:,} flights total.

        <p>
        The percentages are calculated with Bayesian smoothing: if a particular
        route has very few flights, like less than a thousand, we display a
        number that's not the raw percentage but one closer to the overall
        average, since there isn't much data yet to make a deterimination of
        the failure or delay rate.  Hovering the mouse over a percentage will
        show the raw data.
        <span style="font-size: 80%">[Details: we use a simple empirical Bayes approach,
        calculating the posterior mean given a Beta prior
        whose parameters were fit on the dataset of MLEs for all
        route/carrier combinations.
        The CSV files contain "pfail_raw" and "pdelay1hr_raw" columns
        which are the simple percentages. Multiplyling "pfail_raw" by "n"
        will get the number of failed flights.]</span>

        <p>There are many factors that don't get taken into account.
        For example, these calculations aren't very good at
        assigning blame between
        the carrier, origin airport, and destination airport.
        And the delay and failure rates don't consider really important factors
        like weather or time of flight, etc.

        <p>
        In the meantime, the code and data is available at
        <a href="https://github.com/brendano/flightstats">github.com/brendano/flightstats</a>.

        <p>Website started by <a href="http://brenocon.com/">Brendan O'Connor</a>
        when stuck, not for the first time, in O'Hare.

        """.format(**locals()),
        "",
        no_info=True
        )

# DELETED agresti-coull explanation

"""
        Percentages show pessimistic "worst-case" delay rates and failure rates,
        to control for when there's a lack of data.
        If there are a large number of flights, this is just the historical percentage.
        If there only a small number of flights,
        that simple calculation might look lower than it really is just due to luck.
        To remedy this, we instead show a <i>higher</i> number, the worst-case rate:
        it's high enough such that there's only a 2% chance the true rate
        is higher.
        (I guess we could call it a "98% worst case", or "two-sigma worst case". 
        The calculation is based on an
        <a href="https://en.wikipedia.org/wiki/Binomial_proportion_confidence_interval">Agresti-Coull</a> confidence interval.)

        <p>
        For example, if there were 10,000 flights and 100 failures,
        the raw percentage is 1%, but our method would report a slightly higher
        number: 1.2%.
        If there were only 100 flights and 1 failed, our method actually
        reports 6%,
        since from those 100 flights it could have been the case that the future would have 6% failures, but they got lucky on those 100.
        Therefore our numbers are harsh when there is not much data,
        such as on routes with only a few hundred
        flights; there's not enough data on them to trust they will have a
        small delay rate in the future.
        (The webpages do not show entries where there's fewer than 100 flights,
        since the rates are not reliable. But they can be accessed in the csv download.)
"""
