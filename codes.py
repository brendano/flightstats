# -*- encoding: utf-8 -*-
import re
import os

carriers = """
OO	SkyWest Airlines
EV	ExpressJet Airlines
MQ	Envoy Air
6A	AVIACSA
9K	Cape Air
A0	L'Avion
A7	Air Plus Comet
AA	American
AC	Air Canada
AF	Air France
AI	Air India
AM	Aeromexico
AR	Aerolineas Argentinas
AS	Alaska
AT	Royal Air Maroc
AV	Avianca
AY	Finnair
AZ	Alitalia
B6	JetBlue
BA	British Airways
BD	bmi british midland
BR	EVA Airways
C6	CanJet Airlines
CA	Air China
CI	China
CO	Continental
CX	Cathay
CZ	China Southern
DL	Delta
EI	Aer Lingus
EK	Emirates
EO	EOS
F9	Frontier
FI	Icelandair
FJ	Air Pacific
FL	AirTran
G4	Allegiant
GQ	Big Sky
HA	Hawaiian
HP	America West
HQ	Harmony
IB	Iberia
JK	Spanair
JL	JAL
JM	Air Jamaica
KE	Korean
KU	Kuwait
KX	Cayman
LA	LanChile
LH	Lufthansa
LO	LOT
LT	LTU
LW	Pacific Wings
LX	SWISS
LY	El Al
MA	MALEV
MH	Malaysia
MU	China Eastern
MX	Mexicana
NH	ANA
NK	Spirit
NW	Northwest
NZ	Air New Zealand
OS	Austrian
OZ	Asiana
PN	Pan American
PR	Philippine
QF	Qantas
QK	Air Canada Jazz
RG	VARIG
SA	South African
SK	SAS
SN	SN Brussels
SQ	Singapore
SU	Aeroflot
SY	Sun Country
TA	Taca
TG	Thai
TK	Turkish
TN	Air Tahiti Nui
TP	TAP
TS	Air Transat
U5	USA 3000
UA	United
UP	Bahamasair
US	US Air
V3	Copa
VS	Virgin Atlantic
VX	Virgin America
WA	Western
WN	Southwest
WS	WestJet
XE	ExpressJet
Y2	Globespan
Y7	Silverjet
YV	Mesa
YX	Midwest
ZK	Great Lakes
"""

# This list is pretty incomplete
airports = """
Calgary	Calgary International Airport	Alberta	YYC
Montréal	Pierre Elliott Trudeau International Airpor	Quebec	YUL
Ottawa	Ottawa Macdonald-Cartier International Airport	Ontario	YOW
Québec	Quebéc City Airport, Jean Lesage International Airport	Quebec	YQB
Toronto	Lester B. Pearson International Airport	Ontario	YYZ
Vancouver	Vancouver International Airport	British Columbia	YVR
Atlanta	Hartsfield-Jackson Atlanta International	Georgia	ATL
Anchorage	Ted Stevens Anchorage International Airport	Alaska	ANC
Austin	Austin-Bergstrom International	Texas	AUS
Baltimore	Baltimore/Washington International - BWI Airport	Maryland	BWI
Boston	Logan International	Massachusetts	BOS
Charlotte	Charlotte Douglas International	North Carolina	CLT
Chicago	Chicago Midway Airport	Illinois	MDW
Chicago	Chicago O'Hare International	Illinois	ORD
Cincinnati	Cincinnati/Northern Kentucky International	Ohio	CVG
Cleveland	Cleveland Hopkins International	Ohio	CLE
Columbus	Port Columbus International	Ohio	CMH
Dallas	Dallas/Ft. Worth International - DFW Airport	Texas	DFW
Denver	Denver International Airport	Colorado	DEN
Detroit	Detroit Metropolitan Wayne County Airport	Michigan	DTW
Fort Lauderdale	Fort Lauderdale/Hollywood International	Florida	FLL
Fort Myers	Southwest Florida International	Florida	RSW
Hartford	Bradley International	Connecticut	BDL
Honolulu	Hawaii Honolulu International	Hawaii	HNL
Houston	George Bush Intercontinental	Texas	IAH
Houston	William P. Hobby Airport	Texas	HOU
Indianapolis	Indianapolis International	Indiana	IND
Kansas City	Kansas City International	Missouri	MCI
Las Vegas	McCarran International	Nevada	LAS
Los Angeles	Los Angeles International - LAX Airport	California	LAX
Memphis	Memphis International	Tennessee	MEM
Miami	Miami International Airport	Florida	MIA
Minneapolis	Minneapolis/St. Paul International	Minnesota	MSP
Nashville	Nashville International	Tennessee	BNA
New Orleans	Louis Armstrong International	Louisiana	MSY
New York	John F. Kennedy International	New York	JFK
New York	LaGuardia International	New York	LGA
Newark	Newark Liberty International	New Jersey	EWR
Oakland	Metropolitan Oakland International	California	OAK
Ontario	Ontario International	California	ONT
Orlando	Orlando International	Florida	MCO
Philadelphia	Philadelphia International	Pennsylvania	PHL
Phoenix	Sky Harbor International	Arizona	PHX
Pittsburgh	Pittsburgh International	Pennsylvania	PIT
Portland	Portland International	Oregon	PDX
Raleigh-Durham	Raleigh-Durham International	North Carolina	RDU
Sacramento	Sacramento International	California	SMF
Salt Lake City	Salt Lake City International	Utah	SLC
San Antonio	San Antonio International	Texas	SAT
San Diego	Lindbergh Field International	California	SAN
San Francisco	San Francisco International	California	SFO
San Jose	Mineta San José International	California	SJC
Santa Ana	John Wayne Airport, Orange County	California	SNA
Seattle	Seattle-Tacoma International - Seatac Airport	Washington	SEA
St. Louis	Lambert-St. Louis International	Missouri	STL
Tampa	Tampa International	Florida	TPA
Washington D.C.	Dulles International Airport	Washington D.C.	IAD
Washington D.C.	Ronald Reagan Washington National	Washington D.C.	DCA
"""

carriers_dict = dict(L.strip().split("\t") for L in carriers.strip().split("\n"))


airports_dict = {}
# for L in airports.strip().split("\n"):
#     city,airportname,state,code = L.split("\t")
#     airports_dict[code] = {'city':city, 'name':airportname, 'state':state, 'code':code}

def wikiclean(markup):
    markup = re.sub(r"\|.*?\]\]","",markup)
    markup = markup.replace("[[","").replace("]]","")
    markup = re.sub(r"(, *)?United +States", "", markup)
    return markup.strip()

for line in os.popen("cat codes/List_of_airports_by_IATA_code*"):
    if not re.search(r'^\| *[A-Z]{3} ', line): continue
    parts = [x.strip() for x in line.split("||")]
    code, code4, name, city = parts[:4]
    code = re.search(r'\b[A-Z]{3}\b', code).group()
    name = wikiclean(name)
    city = wikiclean(city)
    airports_dict[code] = {'city':city, 'name':name, 'code':code}

# overrides
airports_dict["BWI"]["name"] = "Baltimore–Washington International Airport"
airports_dict["BWI"]["city"] = "Baltimore/DC"

airports_dict["SEA"]["name"] = "Seattle–Tacoma International Airport"
airports_dict["SEA"]["city"] = "Washington State"

def getname(code):
    if code in carriers_dict:
        return "%s - %s" % (code, carriers_dict[code])

    if code in airports_dict:
        d = airports_dict[code]
        # return "{code} - {name} ({city}, {state})".format(**d)
        return "{code} - {name}, {city}".format(**d)

    return code

