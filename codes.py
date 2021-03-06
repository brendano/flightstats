# -*- encoding: utf-8 -*-
import re
import os

# from some random website
carriers1 = """
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
EV	ExpressJet Airlines
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
MQ	Envoy Air
MU	China Eastern
MX	Mexicana
NH	ANA
NK	Spirit
NW	Northwest
NZ	Air New Zealand
OO	SkyWest Airlines
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

# from https://en.wikipedia.org/wiki/List_of_airline_codes copy and pasted 2015-08-16
# airlinename is a wikipedia link
# COLUMNS:  IATA ICAO Airlinename Callsign Country Comments
carriers2 = """
0A	GNT	Amber Air	GINTA	Lithuania	
0B	BMS	Blue Air	BLUE MESSANGER	Romania	
0C	IBL	IBL Aviation	CATOVAIR	Mauritius	
0D	DWT	Darwin Airline	DARWIN	Switzerland	
0J	JCS	Jetclub	JETCLUB	Switzerland	
1A	AGT	Amadeus Global Travel Distribution	AMADEUS	Spain	
1B		Abacus International		Singapore	Computer reservation system
1C		Electronic Data Systems		Switzerland	
1D		Radixx Solutions International		United States	
1E		Travelsky Technology		China	
1F		INFINI Travel Information		Japan	Computer Reservation System
1G		Galileo International		United States	
1H		Siren-Travel		Russia	
1I		Pegasus Hava Tasimaciligi	Sunturk	Turkey	
1I		Sierra Nevada Airlines		United States	
1I	AMB	Deutsche Rettungsflugwacht	CIVIL AIR AMBULANCE	Germany	
1I	EJA	NetJets	EXECJET	United States	
1I	NVR	Novair	NAVIGATOR	Sweden	
1I	PZR	Sky Trek International Airlines	PHAZER	United States	
1K		Southern Cross Distribution		Australia	
1K		Sutra		United States	
1L	OSY	Open Skies Consultative Commission	OPEN SKIES	United States	
1M		JSC Transport Automated Information Systems		Russia	
1N		Navitaire		United States	
1P		Worldspan		United States	
1Q		Sirena		Russia	
1R		Hainan Phoenix Information Systems		China	
1S		Sabre		United States	
1T	BUC	Bulgarian Air Charter	BULGARIAN CHARTER	Bulgaria	
1T	RNX	1Time Airline	NEXTIME	South Africa	airline defunct
1U		ITA Software		United States	Computer reservation system
1U		Polyot Sirena		Russia	
1W	WON	Wings Air	WINGS ABADI	Indonesia	Subsidiary of Lion Air
1Y		Electronic Data Systems		United States	
1Z	APD	Sabre Pacific		Australia	
2A		Deutsche Bahn		Germany	
2B	ARD	Aerocondor	AEROCONDOR	Portugal	defunct
2C		SNCF		France	
2D	AOG	Aero VIP	AVIP	Argentina	defunct
2F	FTA	Frontier Flying Service	FRONTIER-AIR	United States	
2G	CRG	Cargoitalia	WHITE PELICAN	Italy	
2G*	MRR	San Juan Airlines	MARINER	United States	
2H		Thalys		Belgium	Not an airline (train).
2J	VBW	Air Burkina	BURKINA	Burkina Faso	
2K	GLG	Aerogal	AEROGAL	Ecuador	Aerolíneas Galápagos SA
2L	OAW	Helvetic Airways	HELVETIC	Switzerland	
2M	MDV	Moldavian Airlines	MOLDAVIAN	Moldova	
2N	NTJ	NextJet	NEXTJET	Sweden	
2N	UMK	Yuzhmashavia	YUZMASH	Ukraine	
2O	RNE	Air Salone	AIR SALONE	Sierra Leone	
2P	GAP	Air Philippines	ORIENT PACIFIC	Philippines	
2Q	SNC	Air Cargo Carriers	NIGHT CARGO	United States	
2R		Via Rail Canada		Canada	
2S		Star Equatorial Airlines		Guinea	
2S	SDY	Island Express	SANDY ISLE	United States	
2S	TGR	Satgur Air Transport	SATGURAIR	Liberia	defunct
2T	HAM	Haiti Ambassador Airlines		Haiti	
2U	GIP	Air Guinee Express	FUTURE EXPRESS	Guinea	
2V*		Amtrak		United States	Train services only
2W	WLC	Welcome Air	WELCOMEAIR	Austria	
2Z	CGN	Chang An Airlines	CHANGAN	China	
3B	CCG	Central Connect Airlines		Czech Republic	
3C	CEA	RegionsAir	CORP-X	United States	formerly Corporate Airlines
3C	CMV	Calima Aviación	CALIMA	Spain	
3G	AYZ	Atlant-Soyuz Airlines	ATLANT-SOYUZ	Russia	defunct
3J	AAQ	Air Alliance	LIAISON	Canada	defunct
3J	WZP	Zip	ZIPPER	Canada	ICAO Code and callsign no longer allocated
3K	JSA	Jetstar Asia Airways	JETSTAR ASIA	Singapore	
3L	ISK	Intersky	INTERSKY	Austria	
3N	URG	Air Urga	URGA	Ukraine	
3O	MAC	Air Arabia Maroc	ARABIA MAROC	Morocco	This ICAO designator was previously used by Malta Air Charter
3P	TNM	Tiara Air	TIARA	Aruba	
3Q	CYH	China Yunnan Airlines	YUNNAN	China	defunct
3R	GAI	Moskovia Airlines	GROMOV AIRLINE	Russia	JSC
3S	BOX	Aerologic	GERMAN CARGO	Germany	
3S*	AEN	Aeroland Airways		Greece	defunct, ICAO code no longer allocated
3T	URN	Turan Air	TURAN	Azerbaijan	
3U	CSC	Sichuan Airlines	SI CHUAN	China	
3V	TAY	TNT Airways	QUALITY	Belgium	
3W	EMX	Euromanx Airways	EUROMANX	Austria	
3W*	VNR	Wan Air	WANAIR	French Polynesia	defunct
3X	JAC	Japan Air Commuter	COMMUTER	Japan	
4A	AKL	Air Kiribati		Kiribati	
4C	ARE	Aires, Aerovías de Integración Regional, S.A.	AIRES	Colombia	renamed to LAN Colombia
4D	ASD	Air Sinai	AIR SINAI	Egypt	
4F	ECE	Air City	AIRCITY	Germany	
4G	GZP	Gazpromavia	GAZPROMAVIA	Russia	
4G*		Advance Leasing Company		United States	
4H	UBD	United Airways	UNITED BANGLADESH	Bangladesh	
4K*	AAS	Askari Aviation	AL-ASS	Pakistan	
4M	DSM	Aero 2000	LAN AR	Argentina	
4N	ANT	Air North Charter - Canada	AIR NORTH	Canada	
4R	HHI	Hamburg International	HAMBURG JET	Germany	
4S	FNC	Finalair Congo	FINALAIR CONGO	Republic of the Congo	
4T	BHP	Belair Airlines	BELAIR	Switzerland	
4U	GWI	Germanwings	GERMAN WINGS	Germany	
4Y	RBU	Airbus France	AIRBUS FRANCE	France	
4Y	UYA	Yute Air Alaska		United States	
5A	AIP	Alpine Air Express	ALPINE AIR	United States	
5C	ICL	CAL Cargo Air Lines	CAL	Israel	
5D	SLI	Aerolitoral	COSTERA	Mexico	
5D	UDC	DonbassAero	DONBASS AERO	Ukraine	
5F	CIR	Arctic Circle Air Service	AIR ARCTIC	United States	
5G	SSV	Skyservice Airlines	SKYTOUR	Canada	defunct
5J	CEB	Cebu Pacific	CEBU	Philippines	
5K	HFY	Hi Fly	SKY FLYER	Portugal	
5L	RSU	AeroSur	AEROSUR	Bolivia	
5M	MNT	Montserrat Airways	MONTSERRAT	Montserrat	
5M	SIB	Sibaviatrans	SIBAVIA	Russia	
5N	AUL	Nordavia	ARCHANGELSK AIR	Russia	
5O	FPO	Europe Airpost	FRENCH POST	France	
5T	MPE	Canadian North	EMPRESS	Canada	Air Norterra
5V	UKW	Lviv Airlines	UKRAINE WEST	Ukraine	
5W	AEU	Astraeus	FLYSTAR	United Kingdom	defunct, ICAO code no longer allocated
5X	UPS	United Parcel Service	UPS	United States	
5Y	GTI	Atlas Air	GIANT	United States	
5Z	AFX	Airfreight Express		United Kingdom	Ceased operations 08/03/2002
5Z	BML	Bismillah Airlines	BISMILLAH	Bangladesh	
5Z	VVC	VivaColombia	VivaColombia	Colombia	Commenced operations on May 25, 2012
6A	CHP	Aviacsa	AVIACSA	Mexico	
6B	BLX	TUIfly Nordic	BLUESCAN	Sweden	
6E	IGO	IndiGo Airlines	IFLY	India	Interglobe Aviation
6G	AWW	Air Wales	RED DRAGON	United Kingdom	defunct, ICAO code no longer allocated
6H	ISR	Israir	ISRAIR	Israel	
6I	IBZ	International Business Air	INTERBIZ	Sweden	was U5
6J	JUB	Jubba Airways	JUBBA	Somalia	
6J	SNJ	Skynet Asia Airways	NEWSKY	Japan	
6K	RIT	Asian Spirit	ASIAN SPIRIT	Philippines	
6N	NRD	Nordic Regional	NORTH RIDER	Sweden	
6P	ISG	Club Air	CLUBAIR	Italy	
6Q	SLL	Slovak Airlines	SLOV LINE	Slovakia	
6R	DRU	Alrosa Air Company	MIRNY	Russia	
6U	ACX	Air Cargo Germany	LOADMASTER	Germany	defunct
6U	UKR	Air Ukraine	AIR UKRAINE	Ukraine	
6V	AXY	Axis Airways	AXIS	France	defunct
6V	MRW	Mars RK	AVIAMARS	Ukraine	
6V	VGA	Air Vegas	AIR VEGAS	United States	defunct
6W	SOV	Saratov Airlines Joint Stock Company	SARATOV AIR	Russia	
6Y	ART	Smartlynx Airlines	SMART LYNX	Latvia	
6Z	UKS	Ukrainian Cargo Airways	CARGOTRANS	Ukraine	
7A		Aztec Worldwide Airlines		United States	
7B	KJC	Krasnojarsky Airlines	KRASNOJARSKY AIR	Russia	defunct
7C	COY	Coyne Aviation	COYNE AIR	United Kingdom	
7C	JJA	Jeju Air	JEJU AIR	Republic of Korea	
7E	AWU	Sylt Air GmbH	SYLT-AIR	Germany	
7F	FAB	First Air	FIRST AIR	Canada	
7G	SFJ	Star Flyer	STARFLYER	Japan	
7K	KGL	Kogalymavia Air Company	KOGALYM	Russia	
7L	ERO	Sun D'Or	ECHO ROMEO	Israel	
7M	MSA	Mistral Air	AIRMERCI	Italy	
7N	CNA	Centavia		Serbia	
7N	PWD	PAWA Dominicana		Dominican Republic	
7O	GAL	Galaxy Air	GALAXY	Kyrgyzstan	
7O[26]	TVL	Travel Service	TRAVEL SERVICE	Hungary	
7R	BRB	BRA-Transportes Aéreos	BRA-TRANSPAEREOS	Brazil	
7S	RCT	Ryan Air Service	ARCTIC TRANSPORT	United States	
7T	AGV	Air Glaciers	AIR GLACIERS	Switzerland	
7T	TOB	Tobruk Air	TOBRUK AIR	Libya	
7W		Wayraperú	WAYRAPERÚ	Peru	
8A	BMM	Atlas Blue	ATLAS BLUE	Morocco	defunct
8B	GFI	Caribbean Star Airlines	CARIB STAR	Antigua and Barbuda	
8C	ATN	Air Transport International	AIR TRANSPORT	United States	
8C	CXI	Shanxi Airlines	SHANXI	China	
8C	HZT	Air Horizon	HORIZON TOGO	Togo	
8D		Servant Air		United States	
8D	EXV	FitsAir	EXPOAVIA	Sri Lanka	
8D*	SUW	Astair		Russian Federation	Name changed to Interavia Airlines
8E	BRG	Bering Air	BERING AIR	United States	
8F	FFR	Fischer Air	FISCHER	Czech Republic	
8H	HFR	Heli France	HELIFRANCE	France	
8I		Myway Airlines		Italy	
8J	KMV	Komiinteravia	KOMIINTER	Russia	
8L	CGP	Cargo Plus Aviation		United Arab Emirates	
8L	RHC	Redhill Aviation	REDAIR	United Kingdom	
8M	MMA	Myanmar Airways International	MYANMAR	Myanmar	
8M	MXL	Maxair	MAXAIR	Sweden	
8N	NKF	Barents AirLink	NORDFLIGHT	Sweden	previously Nordkalottflyg
8O	YWZ	West Coast Air	COAST AIR	Canada	
8P	PCO	Pacific Coastal Airlines	PASCO	Canada	
8Q		Princess Air			no longer assigned
8Q	OHY	Onur Air	ONUR AIR	Turkey	
8Q*	BAJ	Baker Aviation	RODEO	United States	
8S		Scorpio Aviation			
8T	TID	Air Tindi		Canada	
8U	AAW	Afriqiyah Airways	AFRIQIYAH	Libya	
8V	ACP	Astral Aviation	ASTRAL CARGO	Kenya	
8V	WRF	Wright Air Service	WRIGHT FLYER	United States	
8W	PWF	Private Wings Flugcharter	PRIVATE WINGS	Germany	
8W?		BAX Global			
8Y	CYZ	China Postal Airlines	CHINA POST	China	
8Y	PBU	Air Burundi	AIR-BURUNDI	Burundi	
8Z	WVL	Wizz Air Bulgaria	WIZZBUL	Bulgaria	
9A	EZX	Eagle Express Air Charter	EAGLEXPRESS	Malaysia	
9C	CQH	Spring Airlines	AIR SPRING	China	
9E	FLG	Pinnacle Airlines	FLAGSHIP	United States	
9I	HTA	Helitrans	SCANBIRD	Norway	
9I	TKY	Thai Sky Airlines	THAI SKY	Thailand	
9K	KAP	Cape Air	CAIR	United States	
9L	CJC	Colgan Air	COLGAN	United States	
9M	GLR	Central Mountain Air	GLACIER	Canada	
9O		National Airways Cameroon		Cameroon	
9Q	PBA	PB Air	PEEBEE AIR	Thailand	
9R	VAP	Phuket Air	PHUKET AIR	Thailand	
9T	ABS	Transwest Air	ATHABASKA	Canada	
9U	MLD	Air Moldova	AIR MOLDOVA	Moldova	
9V	VPA	Vipair Airlines	VIAIR	Kazakhstan	defunct
9W	JAI	Jet Airways	JET AIRWAYS	India	
9Y	FGE	Fly Georgia	GEORGIA WING	Georgia	
A2	CIU	Cielos Airlines	CIELOS	Peru	
A3	AEE	Aegean Airlines	AEGEAN	Greece	
A4	SWD	Southern Winds Airlines	SOUTHERN WINDS	Argentina	
A5	HOP	Hop!	AIR HOP	France	
A5	RLA	Airlinair	AIRLINAIR	France	
A6	LPV	Air Alps Aviation	ALPAV	Austria	
A7	MPD	Air Plus Comet	RED COMET	Spain	
A8	BGL	Benin Golf Air	BENIN GOLF	Benin	
A8	XAU	Aerolink Uganda	PEARL	Uganda	
A9	TGZ	Georgian Airways	TAMAZI	Georgia	
AA	AAL	American Airlines	AMERICAN	United States	
AB	BER	Air Berlin	AIR BERLIN	Germany	
AC	ACA	Air Canada	AIR CANADA	Canada	
AD	AZU	Azul Linhas Aéreas Brasileiras	Azul	Brazil	
AD	PRZ	Air Paradise International	RADISAIR	Indonesia	Defunct 2005
AE	AE	Air Ceylon		Sri Lanka	defunct
AE	MDA	Mandarin Airlines	MANDARIN	Taiwan	
AF	AFR	Air France	AIRFRANS	France	
AH	DAH	Air Algérie	AIR ALGERIE	Algeria	
AI	AIC	Air India Limited	AIRINDIA	India	
AJ	NIG	Aero Contractors	AEROLINE	Nigeria	
AK	ABR	Air Bridge Carriers	AIRBRIDGE	United Kingdom	defunct
AK	AXM	AirAsia	RED CAP	Malaysia	ICAO code no longer allocated
AL	SYX	Skywalk Airlines	SKYWAY-EX	United States	(Astral Aviation)
AL	TXC	TransAVIAexport Airlines	TRANSEXPORT	Belarus	
AM	AMX	Aeroméxico	AEROMEXICO	Mexico	
AN	AAA	Ansett Australia	ANSETT	Australia	defunct
AO	AUZ	Australian Airlines	AUSTRALIAN	Australia	Subsidiary merged with QANTAS
AP	ADH	Air One	HERON	Italy	
AP	AIB	Airbus Industrie	AIRBUS INDUSTRIE	France	
AQ	AAH	Aloha Airlines	ALOHA	United States	Ceased operations; former IATA code: TS
AQ	MPJ	MAP-Management and Planung	MAPJET	Austria	
AR	ARG	Aerolíneas Argentinas	ARGENTINA	Argentina	
AS	ASA	Alaska Airlines, Inc.	ALASKA	United States	
AT	RAM	Royal Air Maroc	ROYALAIR MAROC	Morocco	
AU	AUT	Austral Líneas Aéreas	AUSTRAL	Argentina	
AV	AVA	Avianca - Aerovías del Continente Americano S.A.	AVIANCA	Colombia	
AW	AFW	Africa World Airlines	BLACKSTAR	Ghana	
AW	DIR	Dirgantara Air Service	DIRGANTARA	Indonesia	
AW	SCH	CHC Airways	SCHREINER	Netherlands	formerly Schreiner Airways
AX	LOF	Trans States Airlines	WATERSKI	United States	
AY	FIN	Finnair	FINNAIR	Finland	
AZ	AZA	Alitalia	ALITALIA	Italy	
B2	BRU	Belavia Belarusian Airlines	BELARUS AVIA	Belarus	
B3	BLV	Bellview Airlines	BELLVIEW AIRLINES	Nigeria	
B4	BCF	BACH Flugbetriebsges	BACH	Austria	
B4	BKA	Bankair	BANKAIR	United States	
B5	FLT	Flightline	FLIGHTLINE	United Kingdom	defunct
B6	JBU	JetBlue Airways	JETBLUE	United States	
B8	ERT	Eritrean Airlines	ERITREAN	Eritrea	
B9	BGD	Air Bangladesh	AIR BANGLA	Bangladesh	defunct
BA	BAW	British Airways	SPEEDBIRD	United Kingdom	
BB	SBS	Seaborne Airlines	SEABORNE	United States	
BC	SKY	Skymark Airlines	SKYMARK	Japan	
BD	BMA	BMI	MIDLAND	United Kingdom	Ceased operations
BE	BEE	Flybe	JERSEY	United Kingdom	
BF	BBD	Bluebird Cargo	BLUE CARGO	Iceland	
BF	RSR	Aero-Service	CONGOSERV	Republic of the Congo	
BG	BBC	Biman Bangladesh Airlines	BANGLADESH	Bangladesh	
BH		Hawkair		Canada	
BI	RBA	Royal Brunei Airlines	BRUNEI	Brunei	
BJ	LBT	Nouvel Air Tunisie	NOUVELAIR	Tunisia	
BK	PDC	Potomac Air	DISTRICT	United States	
BL	PIC	Pacific Airlines	PACIFIC AIRLINES	Vietnam	
BM		Air Sicilia		Italy	
BM	BMR	BMI Regional	MIDLAND	United Kingdom	
BN		Forward Air International Airlines		United States	
BN	BNF	Braniff International Airways	Braniff	United States	defunct
BN	HZA	Horizon Airlines	HORIZON	Australia	defunct
BO	BOU	Bouraq Indonesia Airlines	BOURAQ	Indonesia	
BP	BOT	Air Botswana	BOTSWANA	Botswana	
BQ	BTL	Baltia Air Lines	BALTIA	United States	Callsign changed from "BALTIA FLIGHT" in 2015[5]
BQ	ROM	Aeromar Lineas Aereas Dominicanas	BRAVO QUEBEC	Dominican Republic	defunct
BR	EVA	EVA Air	EVA	Taiwan	
BS	BIH	British International Helicopters	BRINTEL	United Kingdom	
BT	BTI	Air Baltic	AIRBALTIC	Latvia	
BU	BUN	Buryat Airlines Aircompany	BURAL	Russia	
BV	BPA	Blue Panorama Airlines	BLUE PANOROMA	Italy	
BW	BWA	Caribbean Airlines	CARIBBEAN	Trinidad and Tobago	
BX	ABL	Air Busan		Republic of Korea	
BX	CST	Coast Air	COAST CENTER	Norway	
BY	TOM	Thomson Airways	TOMSON	United Kingdom	
BZ	BDA	Blue Dart Aviation	BLUE DART	India	
BZ	KEE	Keystone Air Service	KEYSTONE	Canada	
C3	IPR	Independent Carrier (ICAR)	ICAR	Ukraine	
C4	IMX	Zimex Aviation	ZIMEX	Switzerland	
C5	UCA	CommutAir	COMMUTAIR	United States	
C6	CJA	CanJet	CANJET	Canada	
C7	CIN	Cinnamon Air	CINNAMON	Sri Lanka	
C7	RLE	Rico Linhas Aéreas	RICO	Brazil	
C8	ICV	Cargolux Italia	CARGO MED	Italy	
C8	WDY	Chicago Express Airlines	WINDY CITY	United States	defunct
C9	RUS	Cirrus Airlines	CIRRUS AIR	Germany	defunct
CA	CCA	Air China	AIR CHINA	China	
CB*	KFS	Kalitta Charters II	KALITTA	United States	Operates B727-200's & DC9's
CC	ABD	Air Atlanta Icelandic	ATLANTA	Iceland	
CC	MCK	Macair Airlines		Australia	
CD	CND	Corendon Dutch Airlines	DUTCH CORENDON	Netherlands	
CD	LLR	Alliance Air	ALLIED	India	
CE	NTW	Nationwide Airlines	NATIONWIDE	South Africa	
CF	SDR	City Airline	SWEDESTAR	Sweden	
CG	TOK	Airlines PNG	BALUS	Papua New Guinea	
CH	BMJ	Bemidji Airlines	BEMIDJI	United States	
CI	CAL	China Airlines	DYNASTY	Taiwan	
CJ	CBF	China Northern Airlines	CHINA NORTHERN	China	defunct.
CJ	CFE	CityFlyer Express	FLYER	United Kingdom	
CK	CKK	China Cargo Airlines	CARGO KING	China	
CL	CLH	Lufthansa CityLine	HANSALINE	Germany	
CM	CMP	Copa Airlines	COPA	Panama	
CN		Islands Nationair		Papua New Guinea	
CN	WWD	Westward Airways	WESTWARD	United States	
CO		Continental Express	JETLINK	United States	
CO	COA	Continental Airlines	CONTINENTAL	United States	ICAO Code and callsign withdrawn
CP	CDN	Canadian Airlines	CANADIAN	Canada	defunct
CP	CPC	Canadian Pacific Airlines	EMPRESS	Canada	ICAO Code and callsign no longer allocated
CP	CPZ	Compass Airlines	Compass	United States	
CQ	CCW	Central Charter	CENTRAL CHARTER	Czech Republic	
CQ	EXL	Sunshine Express Airlines		Australia	
CR	ABC	OAG		United Kingdom	
CS	CMI	Continental Micronesia	AIR MIKE	United States	
CT	CAT	Civil Air Transport	Mandarin	Taiwan	defunct
CU	CUB	Cubana de Aviación	CUBANA	Cuba	
CV	CLX	Cargolux	CARGOLUX	Luxembourg	
CV	CVA	Air Chathams	CHATHAM	New Zealand	
CW	CWM	Air Marshall Islands	AIR MARSHALLS	Marshall Islands	
CX	CPA	Cathay Pacific	CATHAY	Hong Kong	
CY	CYP	Cyprus Airways	CYPRUS	Cyprus	
CZ	CSN	China Southern Airlines	CHINA SOUTHERN	China	
D2	SSF	Severstal Air Company	SEVERSTAL	Russia	
D3	DAO	Daallo Airlines	DALO AIRLINES	Djibouti	
D4	LID	Alidaunia	ALIDA	Italy	
D5	DAU	Dauair	DAUAIR	Germany	
D6	ILN	Interair South Africa	INLINE	South Africa	
D7	XAX	AirAsia X	XANADU	Malaysia	
D7	XFA	FlyAsianXpress	FAX AIR	Malaysia	
D8	DJB	Djibouti Airlines	DJIBOUTI AIR	Djibouti	
D8	IBK	Norwegian Air International Ltd.	NORTRANS	Ireland	
D9	DNV	Donavia	DONAVIA	Russia	formerly Aeroflot-Don
DA	GRG	Air Georgia	AIR GEORGIA	Georgia	
DB	BZH	Brit Air	BRITAIR	France	
DC	GAO	Golden Air	GOLDEN	Sweden	
DD	NOK	Nok Air	NOK AIR	Thailand	
DE	CFG	Condor Flugdienst	CONDOR	Germany	
DG	SRQ	Tigerair Philippines	SEATIGER	Philippines	Formerly SEAir and to be renamed to Go! Air
DH	DVA	Discovery Airways	DISCOVERY AIRWAYS	United States	
DH	IDE	Independence Air	INDEPENDENCE AIR	United States	defunct
DI	BAG	Dba	SPEEDWAY	Germany	Merged into Air Berlin
DJ	PBN	Pacific Blue	BLUEBIRD	New Zealand	Controlled Dupe IATA with Virgin Australia
DJ	PLB	Polynesian Blue	POLYBLUE	New Zealand	Controlled Dupe IATA, Code reserved but not in use, PBN (Bluebird) used.
DJ	VBH	Virgin Blue Holdings	BLUEY	Australia	Code used for Virgin Australia wet-leased operations.
DJ	VOZ	Virgin Australia	VELOCITY	Australia	
DK	ELA	Eastland Air		Australia	
DL	DAL	Delta Air Lines	DELTA	United States	
DM		Maersk		Denmark	Defunct
DO	DOA	Dominicana de Aviación	DOMINICANA	Dominican Republic	defunct
DP	FCA	First Choice Airways	JETSET	United Kingdom	
DQ		Coastal Air	U.S. Virgin Islands	United States	
DS	EZS	easyJet Switzerland	TOPSWISS	Switzerland	
DT	DTA	TAAG Angola Airlines	DTA	Angola	
DU	NLH	Norwegian Long Haul	NORSTAR	Norway	
DV	ACK	Nantucket Airlines	ACK AIR	United States	WAS 9k
DV	LTF	Lufttaxi Fluggesellschaft	Garfield	Germany	
DW	UCR	Aero-Charter Ukraine	CHARTER UKRAINE	Ukraine	
DX	DTR	DAT Danish Air Transport	DANISH	Denmark	
DY	NAX	Norwegian Air Shuttle	NOR SHUTTLE	Norway	
Denmark	
E0	ESS	Eos Airlines	NEW DAWN	United States	
E1		Everbread		United Kingdom	
E2	GRN	Rio Grande Air	GRANDE	United States	defunct
E2	KMP	Kampuchea Airlines	KAMPUCHEA	Cambodia	IATA was KT
E3	DMO	Domodedovo Airlines	DOMODEDOVO	Russia	defunct
E4	RSO	Aero Asia International	AERO ASIA	Pakistan	defunct
E5	BRZ	Samara Airlines	BERYOZA	Russia	defunct
E6		Bringer Air Cargo Taxi Aéreo		Brazil	
E7	EAF	European Aviation Air Charter	EUROCHARTER	United Kingdom	
E7	ESF	Estafeta Carga Aérea		Mexico	
E8	ELG	Alpi Eagles	ALPI EAGLES	Italy	defunct, ICAO code no longer allocated
E9	CXS	Boston-Maine Airways	CLIPPER CONNECTION	United States	Pan Am Clipper Connection Pan Am III
EA	EAL	Eastern Air Lines	EASTERN	United States	defunct
EA	EAL	European Air Express	STAR WING	Germany	
EC	TWN	Avialeasing Aviation Company	TWINARROW	Uzbekistan	
ED*	ABQ	Airblue	PAKBLUE	Pakistan	
EE	EAY	Aero Airlines	REVAL	Estonia	defunct
EF	EFA	Far Eastern Air Transport	Far Eastern	Taiwan	
EG	JAA	Japan Asia Airways	ASIA	Japan	defunct
EH	AKX	Air Nippon Network Co. Ltd.	ALFA WING	Japan	
EH	SET	SAETA	SAETA	Ecuador	
EI	EIN	Aer Lingus	SHAMROCK	Ireland	
EJ	NEA	New England Airlines	NEW ENGLAND	United States	
EK	UAE	Emirates Airline	EMIRATES	United Arab Emirates	
EL	ANK	Air Nippon	ANK AIR	Japan	merged into All Nippon Airways, ICAO code no longer allocated
EM	CFS	Empire Airlines	EMPIRE AIR	United States	
EM*	AEB	Aero Benin	AEROBEN	Benin	defunct
EN	DLA	Air Dolomiti	DOLOMITI	Italy	
EO	ALX	Hewa Bora Airways	ALLCONGO	Democratic Republic of the Congo	
EO	LHN	Express One International	LONGHORN	United States	defunct
EP	IRC	Iran Aseman Airlines	ASEMAN	Iran	
EQ	TAE	TAME	TAME	Ecuador	Transporte Aéreos Militares Ecuatorianos
ER	DHL	Astar Air Cargo	D-H-L	United States	defunct, DHL
ES	DHX	DHL International	DILMUN	Bahrain	
ET	ETH	Ethiopian Airlines	ETHIOPIAN	Ethiopia	
EU	EEA	Empresa Ecuatoriana De Aviación	ECUATORIANA	Ecuador	
EV	ASQ	Atlantic Southeast Airlines	ACEY	United States	Merged into ExpressJet Airlines
EV	ASQ	ExpressJet	ACEY	United States	
EW	EWG	Eurowings	EUROWINGS	Germany	
EX	BJK	Atlantic Airlines	BLACKJACK	United States	
EX	SDO	Air Santo Domingo	AERO DOMINGO	Dominican Republic	
EY	EFL	Eagle Air	FLYING EAGLE	Tanzania	
EY	ETD	Etihad Airways	ETIHAD	United Arab Emirates	
EZ	EIA	Evergreen International Airlines	EVERGREEN	United States	
EZ	SUS	Sun Air of Scandinavia	SUNSCAN	Denmark	
F2	FLM	Fly Air	FLY WORLD	Turkey	
F3	FSW	Faso Airways	FASO	Burkina Faso	
F4	NBK	Albarka Air	AL-AIR	Nigeria	
F5	COZ	Cosmic Air	COSMIC AIR	Nepal	
F6	RCK	Faroejet	ROCKROSE	Faroe Islands	
F7	BBO	Flybaboo	BABOO	Switzerland	
F9	FFT	Frontier Airlines	FRONTIER FLIGHT	United States	
FA	SFR	Safair	CARGO	South Africa	
FB	LZB	Bulgaria Air	FLYING BULGARIA	Bulgaria	
FC	WBA	Finncomm Airlines	WESTBIRD	Finland	
FD	AIQ	Thai AirAsia	THAI ASIA	Thailand	
FE	WCP	Primaris Airlines	WHITECAP	United States	
FF		Airshop		Netherlands	
FG	AFG	Ariana Afghan Airlines	ARIANA	Afghanistan	
FH	FHY	Freebird Airlines	FREEBIRD AIR	Turkey	
FH	FUA	Futura International Airways	FUTURA	Spain	defunct
FI	ICE	Icelandair	ICEAIR	Iceland	
FJ	FJI	Fiji Airways	PACIFIC	Fiji	
FK	KEW	Keewatin Air	BLIZZARD	Canada	
FK	WTA	Africa West	WEST TOGO	Togo	
FL	TRS	AirTran Airways	CITRUS	United States	defunct, last flight 12/30/2014, now part of Southwest Airlines
FM	CSH	Shanghai Airlines	SHANGHAI AIR	China	
FN	RGL	Regional Air Lines	MAROC REGIONAL	Morocco	
FO	ATM	Airlines of Tasmania	AIRTAS	Australia	
FP	AND	Servicios Aereos De Los Andes	SERVI ANDES	Peru	2014[1]
FP	FRE	Freedom Air	FREEDOM	United States	Aviation Services
FR	RYR	Ryanair	RYANAIR	Ireland	
FS	ACL	Itali Airlines	SPADA	Italy	Former name: Transporti Aerei Italiani; former IATA Code: 9X*; former ICAO code: ACO
FS	STU	Servicios de Transportes Aéreos Fueguinos	FUEGUINO	Argentina	ICAO and call sign not current
FT	SRH	Siem Reap Airways	SIEMREAP AIR	Cambodia	
FV	PLK	Pulkovo Aviation Enterprise	PULKOVO	Russia	defunct merged into Rossiya (airline)
FV	SDM	Rossiya	RUSSIA	Russia	Airline merged with Pulkovo Aviation Enterprise and renamed to Rossiya
FW	IBX	Ibex Airlines	IBEX	Japan	
FX	FDX	Federal Express	FEDEX	United States	
FY	FFM	Firefly	FIREFLY	Malaysia	
FY	NWR	Northwest Regional Airlines		Australia	
FZ	FDB	Flydubai	SKYDUBAI	UAE	
G0	GHB	Ghana International Airlines	GHANA AIRLINES	Ghana	
G1		Gorkha Airlines	GORKHA AIRLINES	Nepal	?ICAO
G2	VXG	Avirex	AVIREX-GABON	Gabon	
G3	CIX	City Connexion Airlines	CONNEXION	Burundi	defunct
G3	GLO	Gol Transportes Aéreos	GOL TRANSPORTE	Brazil	Brazilian low-cost airline.
G4	AAY	Allegiant Air	ALLEGIANT	United States	
G5	HXA	China Express Airlines	CHINA EXPRESS	China	
G6	BSR	Guine Bissaur Airlines	BISSAU AIRLINES	Guinea-Bissau	
G6	WLG	Air Volga	GOUMRAK	Russia	
G7	GJS	GoJet Airlines	LINDBERGH	United States	
G7	GNF	Gandalf Airlines	Gandalf	Italy	
G8	AGB	Air Service Gabon		Gabon	defunct
G8	ENK	Enkor JSC	ENKOR	Russia	
G8	GOW	GoAir	GOAIR	India	
G8	GUJ	Gujarat Airways	GUJARATAIR	India	
G9	ABY	Air Arabia	ARABIA	United Arab Emirates	
GA	GIA	Garuda Indonesia	INDONESIA	Indonesia	
GB	ABX	ABX Air	ABEX	United States	August 15, 2003 Air operations of former Airborne Express
GB	ABX	Airborne Express	ABEX	United States	August 14, 2003 merged into DHL
GC	GNR	Gambia International Airlines	GAMBIA INTERNATIONAL	Gambia	
GD	AHA	Air Alpha Greenland	AIR ALPHA	Denmark	sold to Air Greenland
GE	TNA	TransAsia Airways		Taiwan	
GF	GBA	Gulf Air Bahrain	GULF BAHRAIN	Bahrain	
GG	GGC	Cargo 360	LONG-HAUL	United States	
GG	GUY	Air Guyane	GREEN BIRD	French Guiana	
GG	HAH	Air Comores International	AIR COMORES	Comoros	
GH	GHA	Ghana Airways	GHANA	Ghana	
GI	IKA	Itek Air	ITEK-AIR	Kyrgyzstan	?ICAO confirmed; IATA not
GJ	CDC	CDI Cargo Airlines	HUALONG	China	
GJ	EEZ	Eurofly	E-FLY	Italy	
GJ	MXC	Compania Mexicargo	MEXICARGO	Mexico	
GK		Go One Airways		United Kingdom	Defunct?
GK		JetStar Japan		Japan	
GL	BSK	Miami Air International	BISCAYNE	United States	
GL	GRL	Air Greenland	GREENLAND	Denmark	
GL	GRL	Air Greenland	GREENLAND	Greenland
GM	SVK	Air Slovakia	SLOVAKIA	Slovakia	ICAO code no longer allocated
GN	AGN	Air Gabon	GOLF NOVEMBER	Gabon	defunct
GO	KZU	Kuzu Airlines Cargo	KUZU CARGO	Turkey	
GP	GES	Gestair	GESTAIR	Spain	
GP	PTP	Palau Trans Pacific Airlines	TRANS PACIFIC	Palau	
GQ	BSY	Big Sky Airlines	BIG SKY	United States	
GR	AUR	Aurigny Air Services	AYLINE	United Kingdom	
GR	GCO	Gemini Air Cargo	GEMINI	United States	
GS	GUN	Grant Aviation	HOOT	United States	
GS	UPA	Air Foyle	FOYLE	United Kingdom	defunct, ICAO code no longer allocated
GT	GBL	GB Airways	GEEBEE AIRWAYS	United Kingdom	
GV	ARF	Aero Flight	Aero Fox	Germany	defunct
GW	KIL	Kuban Airlines	AIR KUBAN	Russia	
GW	SGR	SkyGreece Airlines	SKYGREECE	Greece	
GX		Pacificair		Philippines	
GX	GBC	Guangxi Beibu Gulf Airlines		China	
GX	JXX	JetX Airlines	JETBIRD	Iceland	
GY		Guyana Airways 2000			
GY	TMG	Tri-MG Intra Asia Airlines	TRILINES	Indonesia	
GZ	RAR	Air Rarotonga	AIR RAROTONGA	Cook Islands	
H2	SKU	Sky Airline	AEROSKY	Chile	
H4		Héli Sécurité Helicopter Airlines		France	
H4	IIN	Inter Island Airways		Cape Verde	
H5	HOA	Hola Airlines	HOLA	Spain	
H5	MVL	Mavial Magadan Airlines	Mavial	Russia	
H6	HAG	Hageland Aviation Services	HAGELAND	United States	
H7	EGU	Eagle Air	AFRICAN EAGLE	Uganda	
H8	KHB	Dalavia	DALAVIA	Russia	
H9	HAD	Air D'Ayiti	HAITI AVIA	Haiti	
H9	IZM	Izair	IZMIR	Turkey	
HA	HAL	Hawaiian Airlines	HAWAIIAN	United States	
HB	HAR	Harbor Airlines	HARBOR	United States	
HC		Iceland Express		Iceland	Ceased operations 2012
HC	ATI	Aero-Tropics Air Services		Australia	defunct
HC	HCC	Holidays Czech Airlines	CZECH HOLIDAYS	Czech Republic	
HD	ADO	AIRDO	AIR DO	Japan	
HD	HLN	Air Holland	ORANGE	Netherlands	defunct
HE	LGW	Luftfahrtgesellschaft Walter	WALTER	Germany	
HF	HLF	Hapagfly	HAPAG LLOYD	Germany	TUIfly
HG	NLY	Niki	FLYNIKI	Austria	
HH		Hope Air	HOPE AIR	Canada	
HJ	AXF	Asian Express Airlines	FREIGHTEXPRESS	Australia	[citation needed]
HJ	HEJ	Hellas Jet	HELLAS JET	Greece	ceased operation in 2010
HK	FSC	Four Star Aviation / Four Star Cargo	FOUR STAR	United States	Virgin Islands
HM	SEY	Air Seychelles	SEYCHELLES	Seychelles	
HN	HVY	Heavylift Cargo Airlines	HEAVY CARGO	Australia	
HO	DJA	Antinea Airlines	ANTINEA	Algeria	defunct
HO	DKH	Juneyao Airlines	JUNEYAO AIRLINES	China	
HP		Hawaiian Pacific Airlines		United States	defunct
HP		Phoenix Airways		Switzerland	
HP	AWE	America West Airlines	CACTUS	United States	Merged with US Airways
HP	HPA	Pearl Airways	PEARL AIRWAYS	Haiti	IATA code withdrawn
HQ	HMY	Harmony Airways	HARMONY	Canada	
HQ	TCW	Thomas Cook Airlines	THOMAS COOK	Belgium	
HR	HHN	Hahn Air	ROOSTER	Germany	
HT	AHW	Aeromist-Kharkiv	AEROMIST	Ukraine	defunct
HU	CHH	Hainan Airlines	HAINAN	China	
HV	TRA	Transavia Holland	TRANSAVIA	Netherlands	
HW	FHE	Hello	FLYHELLO	Switzerland	
HW	NWL	North-Wright Airways	NORTHWRIGHT	Canada	
HX	CRK	Hong Kong Airlines	BAUHINIA	Hong Kong	
HY	UZB	Uzbekistan Airways	UZBEK	Uzbekistan	
HZ	SHU	Sakhalinskie Aviatrassy (SAT)	SATAIR	Russia	
HZ	SOZ	Sat Airlines	SATCO	Kazakhstan	
I2	IBS	Iberia Express	IBEREXPRESS	Spain	Charter service, low cost carrier for EU flights of Iberia operating only A320's
I4	FWA	Interstate Airlines	FREEWAYAIR	Netherlands	
I5	IAD	AirAsia India	ARIYA	India	Founded 28. Mar 2013
I6	SEQ	Sky Eyes	SKY EYES	Thailand	
I7	PMW	Paramount Airways	PARAWAY	India	
I9	IBU	Indigo	INDIGO BLUE	United States	
I9*	AEY	Air Italy	AIR ITALY	Italy	merged into Meridiana
IA	IAW	Iraqi Airways	IRAQI	Iraq	
IB	IBE	Iberia Airlines	IBERIA	Spain	
IC	IAC	Indian Airlines	INDAIR	India	
ID	ITK	Interlink Airlines	INTERLINK	South Africa	
IE	SOL	Solomon Airlines	SOLOMON	Solomon Islands	
IF	ISW	Islas Airways	PINTADERA	Spain	
IG	ISS	Meridiana	MERIDIANA	Italy	Callsign was MERAIR
IH		Falcon Aviation		Sweden	
IH	MZA	Irtysh Air	IRTYSH AIRLINES	Kazakhstan	Old IATA code: IT; old ICAO code: IRT
II	CSQ	IBC Airways	CHASQUI	United States	
IJ	GWL	Great Wall Airlines	GREAT WALL	China	
IJ	SJO	Spring Airlines Japan	JEY SPRING	Japan	
IK	KAR	Ikar	IKAR	Russian Federation	
IK	LKN	Lankair	Lankair	Sri Lanka	
IM	MNJ	Menajet	MENAJET	Lebanon	
IN	MAK	MAT Macedonian Airlines	MAKAVIO	Macedonia	
IO	IAA	Indonesian Airlines	INDO LINES	Indonesia	
IP	JOL	Atyrau Air Ways	EDIL	Kazakhstan	
IQ	AUB	Augsburg Airways	AUGSBURG-AIR	Germany	defunct
IR	IRA	Iran Air	IRANAIR	Iran	Was B9
IT	KFR	Kingfisher Airlines	KINGFISHER	India	
IT	TTW	Tigerair Taiwan	SMART CAT	Taiwan	
IV	JET	Wind Jet	GHIBLI	Italy	
IW	AOM	AOM French Airlines	French Lines	France	defunct
IX	AXB	Air India Express	EXPRESS INDIA	India	
IY	IYE	Yemenia	YEMENI	Yemen	
IZ	AIZ	Arkia Israel Airlines	ARKIA	Israel	
J2	AHY	Azerbaijan Airlines	AZAL	Azerbaijan	
J3	PLR	Northwestern Air	POLARIS	Canada	
J4	BFL	Buffalo Airways	BUFFALO	Canada	
J4	JCI	Jordan International Air Cargo		Jordan	
J6	AOC	AVCOM	AERO AVCOM	Russia	
J7	CVC	Centre-Avia	AVIACENTRE	Russia	
J7	DNM	Denim Air	DENIM	Netherlands	
J7	VJA	ValuJet Airlines	CRITTER	United States	Now operating as AirTran Airways. J7 Reassigned.
J8	BVT	Berjaya Air	BERJAYA	Malaysia	
J9	GIF	Guinee Airlines	GUINEE AIRLINES	Guinea	defunct
J9	JZR	Jazeera Airways	JAZEERA	Kuwait	
JA	BON	B&H Airlines	Air Bosna	Bosnia and Herzegovina	
JB	JBA	Helijet	HELIJET	Canada	
JC	JEX	JAL Express	JANEX	Japan	
JE	MNO	Mango	TULCA	South Africa	
JF	JAA	Jet Asia Airways	JET ASIA	Thailand	
JF	LAB	L.A.B. Flying Service	LAB	United States	
JH	NES	Nordeste Linhas Aéreas Regionais	NORDESTE	Brazil	
JI	JAE	Jade Cargo International	JADE CARGO	China	
JI	MDW	Midway Airlines (1993–2003)	MIDWAY	United States	defunct
JJ	AGX	Aviogenex	GENEX	Serbia	
JJ	TAM	TAM Brazilian Airlines	TAM	Brazil	
JK	JKK	Spanair	SPANAIR	Spain	defunct
JL	JAL	Japan Airlines	JAPANAIR	Japan	Japan Airlines International
JL	JAL	Japan Airlines Domestic	J-BIRD	Japan	defunct
JM	AJM	Air Jamaica	JAMAICA	Jamaica	
JM	JKT	Jetstar Hong Kong Airways	KAITAK	China	
JN	XLA	Excel Airways	EXPO	United Kingdom	
JO	JAZ	JALways	JALWAYS	Japan	
JO	JTG	Jettime	JETTIME	Denmark	
JP	ADR	Adria Airways	ADRIA	Slovenia	
JQ	JST	Jetstar Airways	JETSTAR	Australia	
JR	SER	Aero California	AEROCALIFORNIA	Mexico	
JS	KOR	Air Koryo	AIR KORYO	Democratic People's Republic of Korea	
JT	LNI	Lion Mentari Airlines	LION INTER	Indonesia	
JU	ASL	Air Serbia	AIR SERBIA	Serbia	formally JAT
JU	JAT	Jat Airways	JAT	Serbia	Name changed to Air Serbia
JV	BLS	Bearskin Lake Air Service	BEARSKIN	Canada	
JW	APW	Arrow Air	BIG A	United States	defunct
JW	VNL	Vanilla Air	VANILLA	Japan	
JX	JEC	Jett8 Airlines Cargo		Singapore	
JY	IWY	Air Turks and Caicos	ISLANDWAYS	Turks and Caicos Islands	Name changed from Interisland Airways Limited
JY	TCI	Air Turks and Caicos	KERRMONT	Turks and Caicos Islands	ICAO code no longer allocated
JZ	SKX	Avia Express	SKY EXPRESS	Sweden	Former names: AMA-Flyg I Goteborg; Salair; former ICAO code: AAX
JZ	SKX	Skyways Express	SKY EXPRESS	Sweden	Ceased operations 2012; Operations continue as Avia Express
K2	ELO	Eurolot	EUROLOT	Poland	
K4	CKS	Kalitta Air	CONNIE	United States	Operates 747-200's & -400's
K5	SQH	SeaPort Airlines	SASQUATCH	United States	Former airline: Wings of Alaska now part of SeaPort Airlines. Alternative callsign: WINGS (for VFR flights only). Former ICAO code: WAK.
K6	KHV	Angkor Air	AIR ANGKOR	Cambodia	
K6	KHV	Cambodia Angkor Air	ANGKOR AIR	Cambodia	
K8	ZAK	Airlink Zambia		Zambia	Zambia Skyways Limited
K9	KFS	Kalitta Charters	KALITTA	United States	Operates Lear 20's & 30's, Falcon 20's, & King Airs
K9	KRI	Krylo Airlines	Krylo	Russia	
KA	HDA	Dragonair, Hong Kong Dragon Airlines	DRAGON	Hong Kong	
KB	DRK	Druk Air	ROYAL BHUTAN	Bhutan	
KC	KZR	Air Astana	ASTANALINE	Kazakhstan	
KD	AEN	Air Enterprise	AIR ENTERPRISE	France	defunct
KD	KNI	KD Avia	KALININGRAD AIR	Russia	
KE	KAL	Korean Air	KOREANAIR	South Korea	
KF	BLF	Blue1	BLUEFIN	Finland	
KG	BNX	LAI - Línea Aérea IAACA	AIR BARINAS	Venezuela	
KH	AAH	Aloha Air Cargo	ALOHA	United States	
KI	AAG	Air Atlantique	ATLANTIC	United Kingdom	Former name: Atlantic Air Transport; former IATA codes: 7M, DG, transferred to Atlantic Flight Training in 2014.
KI	DHI	Adam Air	ADAM SKY	Indonesia	defunct
KJ	AAZ	Asian Air		Kyrgyzstan	
KJ	LAJ	British Mediterranean Airways	BEE MED	United Kingdom	
KK	KKK	Atlasjet	ATLASJET	Turkey	
KL	KLM	KLM	KLM	Netherlands	
KM	AMC	Air Malta	AIR MALTA	Malta	
KN	CUA	China United Airlines	LIANHANG	China	
KO	AER	Alaska Central Express	ACE AIR	United States	
KP	KIA	Kiwi International Air Lines	KIWI AIR	United States	
KQ	KQA	Kenya Airways	KENYA	Kenya	
KR	CWK	Comores Airlines	CONTICOM	Comoros	
KS	PEN	Peninsula Airways	PENINSULA	United States	
KU	KAC	Kuwait Airways	KUWAITI	Kuwait	
KV	MVD	Kavminvodyavia	AIR MINVODY	Russia	
KW	KHK	Kharkiv Airlines	SUNRAY	Ukraine	
KW	WAN	Wataniya Airways	WATANIYA	Kuwait	
KX	CAY	Cayman Airways	CAYMAN	Cayman Islands	
KY	EQL	Air São Tomé and Príncipe	EQUATORIAL	São Tomé and Príncipe	defunct
KZ	NCA	Nippon Cargo Airlines	NIPPON CARGO	Japan	
L1		Lufthansa Systems		Germany	
L2	LYC	Lynden Air Cargo	LYNDEN	United States	
L3	JOS	DHL de Guatemala		Guatemala	
L3	LTO	LTU Austria	BILLA TRANSPORT	Austria	
L4	SSX	Lynx Aviation	SHASTA	United States	Part of Frontier Airlines
L5		Línea Aérea Cuencana		Ecuador	
L5	LTR	Lufttransport	LUFT TRANSPORT	Norway	
L6	VNZ	Tbilaviamsheni	TBILAVIA	Georgia	
L7	LNP	Línea Aérea SAPSA	SAPSA	Chile	
L7	LPN	Laoag International Airlines	LAOAG AIR	Philippines	
L8	LXG	Air Luxor GB	LUXOR GOLF	Guinea-Bissau	
L9	BTZ	Bristow U.S. LLC	BRISTOW	United States	
L9	MLI	Air Mali	AIR MALI	Mali	defunct
L9	TLW	Teamline Air	Teamline	Austria	
LA	LAN	LAN Airlines	LAN CHILE	Chile	
LB	LLB	Lloyd Aéreo Boliviano	LLOYDAEREO	Bolivia	
LC	LOG	Loganair	LOGAN	United Kingdom	
LC	VLO	Varig Logística	VELOG	Brazil	
LD	AHK	Air Hong Kong	AIR HONG KONG	Hong Kong	
LD	TUY	Línea Turística Aereotuy	AEREOTUY	Venezuela	
LF	NDC	FlyNordic	NORDIC	Sweden	
LG	LGL	Luxair	LUXAIR	Luxembourg	
LH	DLH	Lufthansa	LUFTHANSA	Germany	
LH	GEC	Lufthansa Cargo	LUFTHANSA CARGO	Germany	
LI	LIA	Leeward Islands Air Transport	LIAT	Antigua and Barbuda	
LJ	SLA	Sierra National Airlines	SELAIR	Sierra Leone	
LK	LXR	Air Luxor	AIRLUXOR	Portugal	ICAO code no longer allocated
LL	GRO	Allegro	ALLEGRO	Mexico	defunct
LM	LVG	Livingston	LIVINGSTON	Italy	
LN	LAA	Libyan Arab Airlines	LIBAIR	Libya	
LO	LOT	LOT Polish Airlines	POLLOT	Poland	
LP	LPE	LAN Peru	LANPERU	Peru	
LQ	LAQ	Lebanese Air Transport	LAT	Lebanon	
LR	LRC	LACSA	LACSA	Costa Rica	
LS	EXS	Jet2.com	CHANNEX	United Kingdom	
LT	LTU	LTU International	LTU	Germany	
LU	LXP	LAN Express	LANEX	Chile	
LV	LBC	Albanian Airlines	ALBANIAN	Albania	
LW	FDY	Sun Air International	FRIENDLY	United States	
LW	NMI	Pacific Wings	TSUNAMI	United States	
LX	SWR	Swiss International Air Lines	SWISS	Switzerland	
LX	SWU	Swiss European Air Lines	EUROSWISS	Switzerland	
LY	ELY	El Al Israel Airlines	ELAL	Israel	
LZ		Balkan Bulgarian Airlines		Bulgaria	defunct
M2	MZS	Mahfooz Aviation	MAHFOOZ	Gambia	
M3	NFA	North Flying	NORTH FLYING	Denmark	
M3	SPJ	Air Service	AIR SKOPJE	Macedonia	
M3	TUS	ABSA Cargo	Turismo	Brazil	
M5	KEN	Kenmore Air	KENMORE	United States	
M6	AJT	Amerijet International	AMERIJET	United States	
M7	MAA	MasAir	MAS CARGA	Mexico	
M7	MSL	Marsland Aviation	MARSLANDAIR	Sudan	
M7	TBG	Tropical Airways		Haiti	
M8	MKN	Mekong Airlines	MEKONG AIRLINES	Cambodia	Defunct
M9	MSI	Motor Sich	MOTOR SICH	Ukraine	
MA	MAH	Malév Hungarian Airlines	MALEV	Hungary	
MB	EXA	Execair Aviation	CANADIAN EXECAIRE	Canada	
MB	MNB	MNG Airlines	BLACK SEA	Turkey	
MC	RCH	Air Mobility Command	REACH	United States	United States Air Force
MD	MDG	Air Madagascar	AIR MADAGASCAR	Madagascar	
ME	MEA	Middle East Airlines	CEDAR JET	Lebanon	
MF	CXA	Xiamen Airlines	XIAMEN AIR	China	
MG	CCP	Champion Air	CHAMPION AIR	United States	
MH	MAS	Malaysia Airlines	MALAYSIAN	Malaysia	
MH	MWG	MASwings	MASWINGS	Malaysia	
MI	SLK	SilkAir	SILKAIR	Singapore	
MJ	LPR	Líneas Aéreas Privadas Argentinas	LAPA	Argentina	defunct
MJ	MLR	Mihin Lanka	MIHIN LANKA	Sri Lanka	
MK	MAU	Air Mauritius	AIRMAURITIUS	Mauritius	
ML	BIE	Air Mediterranee	MEDITERRANEE	France	
ML	ETC	African Transport Trading and Investment Company	TRANATTICO	Sudan	
ML	MDW	Midway Airlines (1976–1991)	MIDWAY	United States	defunct
MM	MMZ	EuroAtlantic Airways	EUROATLANTIC	Portugal	
MM	SAM	SAM Colombia	SAM	Colombia	Sociedad Aeronáutica De Medellín
MN	CAW	Comair	COMMERCIAL	South Africa	
MO	AUH	Abu Dhabi Amiri Flight	SULTAN	United Arab Emirates	Presidential flight
MO	CAV	Calm Air	CALM AIR	Canada	
MP	MPH	Martinair	MARTINAIR	Netherlands	
MQ	EGF	American Eagle Airlines	EAGLE FLIGHT	United States	Renamed Envoy Air, ICAO Code and Callsign withdrawn in 2014
MR	MRT	Air Mauritanie	MIKE ROMEO	Mauritania	
MS	MSR	Egyptair	EGYPTAIR	Egypt	
MT	JMC	JMC Airlines	JAYEMMSEE	United Kingdom	
MT	TCX	Thomas Cook Airlines	KESTREL	United Kingdom	Formerly "TOP JET"
MU	CES	China Eastern Airlines	CHINA EASTERN	China	
MV	RML	Armenian International Airways	ARMENIA	Armenia	defunct
MW	MUL	Mokulele Airlines	MUKULELE	United States	Callsign and code changed from BUG/SPEEDBUGGY in 2013
MW	MYD	Maya Island Air	MYLAND	Belize	
MX	MXA	Mexicana de Aviación	MEXICANA	Mexico	
MY	MWA	Midwest Airlines (Egypt)		Egypt	
MY	MXJ	Maxjet Airways	MAX-JET	United States	Defunct
MZ	MNA	Merpati Nusantara Airlines	MERPATI	Indonesia	
N2	DAG	Dagestan Airlines	DAGAL	Russia	
N2	QNK	Kabo Air	KABO	Nigeria	
N3	OMS	Omskavia Airline	OMSK	Russia	
N4	MTC	Mountain Air Company	MOUNTAIN LEONE	Sierra Leone	
N4	NCN	National Airlines		Chile	
N4	NWS	Nordwind Airlines	NORDLAND	Russia	
N5		Norfolk Air		Norfolk Island	
N5	KGZ	Kyrgyz Airlines	BERMET	Kyrgyzstan	
N5	SGY	Skagway Air Service	SKAGWAY AIR	United States	
N6	ACQ	Nuevo Continente	AERO CONTINENTE	Peru	Operating license revoked by Chile 10/06/2002; Ceased operations 2005; Former name: Aero Continente
N6	JEV	Lagun Air		Spain	
N7	ROK	National Airlines	RED ROCK	United States	defunct
N8	HGK	Fika Salaama Airlines	SALAAMA	Uganda	
N8	NCR	National Air Cargo dba National Airlines	NATIONAL CARGO	United States	
N9		North Coast Aviation		Papua New Guinea	
NA	NAL	National Airlines	NATIONAL	United States	defunct
NA	NAO	North American Airlines	NORTH AMERICAN	United States	
NB	SNB	Sterling Airlines	STERLING	Denmark	
NC	NAC	Northern Air Cargo	YUKON	United States	
NC	NJS	National Jet Systems	NATIONAL JET	Australia	
NE	ESK	SkyEurope	RELAX	Slovakia	Defunct
NF	AVN	Air Vanuatu	AIR VAN	Vanuatu	
NG	LDA	Lauda Air	LAUDA AIR	Austria	
NH	ANA	All Nippon Airways	ALL NIPPON	Japan	
NI		LANICA		Nicaragua	
NI	PGA	Portugalia	PORTUGALIA	Portugal	
NK	NKS	Spirit Airlines	SPIRIT WINGS	United States	
NL	SAI	Shaheen Air International	SHAHEEN AIR	Pakistan	
NM	DRD	Air Madrid	ALADA AIR	Spain	defunct
NM	NZM	Mount Cook Airlines	MOUNTCOOK	New Zealand	
NN	MOV	VIM Airlines	MOV AIR	Russia	
NO	AUS	Aus-Air		Australia	defunct
NO	NOS	Neos	MOONFLOWER	Italy	
NQ	AJX	Air Japan	AIR JAPAN	Japan	
NR	PIR	Pamir Airways	PAMIR	Afghanistan	
NT	IBB	Binter Canarias	BINTER	Spain	
NU	JTA	Japan Transocean Air	JAI OCEAN	Japan	
NV	CRF	Air Central	AIR CENTRAL	Japan	Ceased operations 2010
NW	NWA	Northwest Airlines	NORTHWEST	United States	defunct
NX	AMU	Air Macau	AIR MACAO	Macao	
NY	FXI	Air Iceland	FAXI	Iceland	
NZ	ANZ	Air New Zealand	NEW ZEALAND	New Zealand	
NZ	EAG	Eagle Airways	EAGLE	New Zealand	
O2		Oceanic Airlines		Guinea	
O4	ABV	Antrak Air	ANTRAK	Ghana	
O6	ONE	Avianca Brazil	OCEANAIR	Brazil	formerly Oceanair
O7	OZJ	Ozjet Airlines	AUSJET	Australia	
O8	OHK	Oasis Hong Kong Airlines	OASIS	Hong Kong	Defunct
O9	NOV	Nova Airline	NOVANILE	Sudan	
OA	OAL	Olympic Air	OLYMPIC	Greece	
OA	OAL	Olympic Airlines	OLYMPIC	Greece	Defunct
OB	AAN	Oasis International Airlines	OASIS	Spain	Ceased operations
OB	AAT	Austrian Airtransport	AUSTRIAN CHARTER	Austria	defunct; former IATA code: U8, OG; former ICAO code: AUC
OB	ASZ	Astrakhan Airlines	AIR ASTRAKHAN	Russia	defunct
OD	MXD	Malindo Airways	MALINDO EXPRESS	Malaysia	
OE	AOT	Asia Overnight Express	ASIA OVERNIGHT	Philippines	
OF	ENT	Enter Air	ENTER	Poland	
OF	FIF	Air Finland	AIR FINLAND	Finland	
OF	TML	Transports et Travaux Aériens de Madagascar	TAM AIRLINE	Madagascar	
OH	COM	Comair	COMAIR	United States	
OJ	FJM	Fly Jamaica Airways	GREENHEARTH	Jamaica	
OJ	OLA	Overland Airways	OVERLAND	Nigeria	
OK	CSA	Czech Airlines	CSA	Czech Republic	
OL	OLT	OLT Express Germany	OLTRA	Germany	
OM	MGL	MIAT Mongolian Airlines	MONGOL AIR	Mongolia	
ON	RON	Our Airline	OUR AIRLINE	Nauru	formerly Air Nauru
OO	SKW	SkyWest Airlines	SKYWEST	United States	
OP	CHK	Chalk's International Airlines	CHALKS	United States	
OR	TFL	Arkefly	ARKEFLY	Netherlands	
OS	AUA	Austrian Airlines	AUSTRIAN	Austria	
OT	PEL	Aeropelican Air Services	PELICAN	Australia	
OU	CTN	Croatia Airlines	CROATIA	Croatia	
OV	ELL	Estonian Air	ESTONIAN	Estonia	
OW	EXK	Executive Airlines	EXECUTIVE EAGLE	United States	American Eagle
OX	OEA	Orient Thai Airlines	ORIENT THAI	Thailand	
OY	ANS	Andes Líneas Aéreas	AEROANDES	Argentina	
OY	OAE	Omni Air International	OMNI-EXPRESS	United States	
OZ	AAR	Asiana Airlines	ASIANA	Republic of Korea	
OZ	OZR	Ozark Air Lines	OZARK	United States	Defunct
P0	PFZ	Proflight Zambia	PROFLIGHT-ZAMBIA	Zambia	
P3	PTB	Passaredo Transportes Aéreos	PASSAREDO	Brazil	
P5	RPB	AeroRepública	AEROREPUBLICA	Colombia	
P6	PVG	Privilege Style Líneas Aéreas	PRIVILEGE	Spain	
P7	ESL	Russian Sky Airlines	RADUGA	Russia	
P8		Air Mekong		Vietnam	defunct
P8	PTN	Pantanal Linhas Aéreas	PANTANAL	Brazil	
P9		Nas Air		Mali	
P9	PGP	Perm Airlines	PERM AIR	Russia	
P9	PVN	Peruvian Airlines		Peru	
PA	FCL	Florida Coastal Airlines	FLORIDA COASTAL	United States	
PA	PAA	Pan American Airways		United States	defunct
PA	PAA	Pan American World Airways	CLIPPER	United States	
PC	FAJ	Air Fiji	FIJIAIR	Fiji	defunct
PC	PGT	Pegasus Airlines	SUNTURK	Turkey	WAS 1I, H9
PC	PVV	Continental Airways	CONTAIR	Russia	
PD	POE	Porter Airlines	PORTER	Canada	
PE	AEL	Air Europe Italy	AIR EUROPE	Italy	defunct
PE	PEV	People's Viennaline	PEOPLES	Switzerland	Previously used by Pegaviation
PF	PNW	Palestinian Airlines	PALESTINIAN	Egypt	
PG	BKP	Bangkok Airways	BANGKOK AIR	Thailand	
PH	PAO	Polynesian Airlines	POLYNESIAN	Samoa	
PI	PDT	Piedmont Airlines (1948-1989)	PIEDMONT	United States	defunct
PI	SUF	Sun Air (Fiji)	SUNFLOWER	Fiji	
PJ	SPM	Air Saint Pierre	SAINT-PIERRE	France	
PK	PIA	Pakistan International Airlines	PAKISTAN	Pakistan	
PL	ASE	Airstars	MOROZOV	Russia	defunct
PL	PLI	Aeroperú	Aeroperu	Peru	defunct
PM	TOS	Tropic Air	TROPISER	Belize	
PN		Pan American Airways		United States	defunct
PO	PAC	Polar Air Cargo	POLAR	United States	
PP	PJS	Jet Aviation	JETAVIATION	Switzerland	
PQ		AirAsia Philippines		Philippines	
PR	PAL	Philippine Airlines	PHILIPPINE	Philippines	
PS	AUI	Ukraine International Airlines	UKRAINE INTERNATIONAL	Ukraine	
PT	CCI	Capital Cargo International Airlines	CAPPY	United States	Allocation deleted 2013
PT	SWN	West Air Sweden	AIR SWEDEN	Sweden	
PU	PUA	PLUNA	PLUNA	Uruguay	
PV	PNR	PAN Air	SKYJET	Spain	
PV	SBU	St Barth Commuter	BLACK FIN	France	
PW	PRF	Precision Air	PRECISION AIR	Tanzania	
PX	ANG	Air Niugini	NUIGINI	Papua New Guinea	
PY	SLM	Surinam Airways	SURINAM	Suriname	
PZ	LAP	TAM Mercosur	PARAGUAYA	Paraguay	
Q3	MBN	Zambian Airways	ZAMBIANA	Zambia	
Q4		Mastertop Linhas Aéreas		Brazil	
Q4	SWX	Swazi Express Airways	SWAZI EXPRESS	Swaziland	
Q4	TLK	Starlink Aviation	STARLINK	Canada	
Q5	MLA	40-Mile Air	MILE-AIR	United States	
Q6	CDP	Aero Condor Peru	CONDOR-PERU	Peru	
Q8	PEC	Pacific East Asia Cargo Airlines	PAC-EAST CARGO	Philippines	
Q9	AFU	Afrinat International Airlines	AFRINAT	Gambia	defunct, ICAO code no longer allocated
QB	AAJ	Air Alma	AIR ALMA	Canada	Ceased operations 10/01/2002; former IATA code: 4L
QB	GFG	Georgian National Airlines	NATIONAL	Georgia	
QC	CRD	Air Corridor	AIR CORRIDOR	Mozambique	defunct
QD	QCL	Air Class Líneas Aéreas	ACLA	Uruguay	
QE	ECC	Crossair Europe	Cigogne	Switzerland	
QF	EAQ	Eastern Australia Airlines	EASTERN	Australia	IATA dupe with parent QANTAS. Also uses 2 letter ICAO EA.
QF	QFA	Qantas	QANTAS	Australia	
QF	SSQ	Sunstate Airlines	SUNSTATE	Australia	Uses IATA of parent QANTAS.
QH	FLA	Air Florida	PALM	United States	relaunching
QH	FLZ	Aero Leasing	AIR FLORIDA	United States	dba Air Florida
QH	LYN	Air Kyrgyzstan	ALTYN AVIA	Kyrgyzstan	Name changed from Kyrgyzstan
QH	LYN	Kyrgyzstan	ALTYN AVIA	Kyrgyzstan	Name changed to Air Kyrgyzstan
QI	CIM	Cimber Sterling	CIMBER	Denmark	
QJ		Jet Airways		United States	
QK	JZA	Air Canada Jazz	JAZZ	Canada	
QL	LER	Línea Aérea de Servicio Ejecutivo Regional	LASER	Venezuela	
QL	RLN	Aero Lanka	AERO LANKA	Sri Lanka	
QL	RLN	Lankan Cargo	AERO LANKA	Sri Lanka	
QM	AML	Air Malawi	MALAWI	Malawi	
QN	ARR	Air Armenia	AIR ARMENIA	Armenia	
QO	MPX	Aeromexpress	AEROMEXPRESS	Mexico	
QO	OGN	Origin Pacific Airways	ORIGIN	New Zealand	
QQ	ROA	Reno Air	RENO AIR	United States	defunct
QQ	UTY	Alliance Airlines	UNITY	Australia	
QR	QTR	Qatar Airways	QATARI	Qatar	
QS	QSC	African Safari Airways	ZEBRA	Kenya	
QS	TVS	Travel Service	SKYTRAVEL	Czech Republic	
QT	TPA	TAMPA	TAMPA	Colombia	
QU	UGA	Uganda Airlines	UGANDA	Uganda	Ceased operations 2001
QU	UTN	UTair-Ukraine	UT Ukraine	Ukraine	
QV	LAO	Lao Airlines	LAO	Lao Peoples Democratic Republic	
QW	BWG	Blue Wings	BLUE WINGS	Germany	defunct
QX	QXE	Horizon Air	HORIZON AIR	United States	
QY	BCS	European Air Transport	EUROTRANS	Belgium	
QZ	AWQ	Indonesia AirAsia	WAGON AIR	Indonesia	
R0	RPK	Royal Airlines	ROYAL PAKISTAN	Pakistan	
R1		Sirin			
R2	ORB	Orenburg Airlines	ORENBURG	Russia	
R3	RME	Armenian Airlines	ARMENIAN	Armenia	defunct
R3	SYL	Aircompany Yakutia	AIR YAKUTIA	Russia	
R5	JAV	Jordan Aviation	JORDAN AVIATION	Jordan	
R5	MAC	Malta Air Charter	MALTA CHARTER	Malta	Defunct?
R6		RACSA		Guatemala	
R7	OCA	Aserca Airlines	AROSCA	Venezuela	
R8	KGA	Kyrgyzstan Airlines	KYRGYZ	Kyrgyzstan	
R9	CAM	Camai Air	AIR CAMAI	United States	Village Aviation
RA	RNA	Nepal Airlines	ROYAL NEPAL	Nepal	was Royal Nepal Airlines
RB	SBK	Air Srpska	Air Srpska	Bosnia and Herzegovina	defunct
RB	SYR	Syrian Arab Airlines	SYRIANAIR	Syrian Arab Republic	
RC	FLI	Atlantic Airways	FAROELINE	Faroe Islands	
RD	RYN	Ryan International Airlines	RYAN INTERNATIONAL	United States	
RE	REA	Aer Arann	AER ARANN	Ireland	
RE	STK	Stobart Air	STOBART	Ireland	
RF	FWL	Florida West International Airways	FLO WEST	United States	
RG	VRN	VRG Linhas Aéreas	VARIG	Brazil	
RH	RPH	Republic Express Airlines	PUBLIC EXPRESS	Indonesia	
RI	MDL	Mandala Airlines	MANDALA	Indonesia	
RJ	RJA	Royal Jordanian	JORDANIAN	Jordan	
RK	RKH	Royal Khmer Airlines	KHMER AIR	Cambodia	
RL	PPW	Royal Phnom Penh Airways	PHNOM-PENH AIR	Cambodia	
RL	RIO	Rio Linhas Aéreas	RIO	Brazil	
RO	ROT	Tarom	TAROM	Romania	
RP*	CHQ	Chautauqua Airlines	CHAUTAUQUA	United States	Was US*
RQ	KMF	Kam Air	KAMGAR	Afghanistan	
RR	RFR	Royal Air Force	RAFAIR	United Kingdom	
RS	ICT	Intercontinental de Aviación	CONTAVIA	Colombia	
RS	MJN	Royal Air Force of Oman	MAJAN	Oman	
RS	SKV	Sky Regional Airlines	MAPLE	Canada	
RU	ABW	AirBridge Cargo	AIRBRIDGE CARGO	Russia	Former IATA: BO
RU	SKI	SkyKing Turks and Caicos Airways	SKYKING	Turks and Caicos Islands	IATA was QW
RV	CPN	Caspian Airlines	CASPIAN	Iran	
RV	ROU	Air Canada Rouge	ROUGE	Canada	
RV*	AFI	Africaone	AFRICAWORLD	The Gambia	
RW	RPA	Republic Airlines	BRICKYARD	United States	
RX	AEH	Aviaexpress	AVEX	Hungary	defunct
RZ		Euro Exec Express		Sweden	
S0	OKS	Slok Air Gambia	SLOK GAMBIA	Gambia	
S2	RSH	Air Sahara	SAHARA	India	renamed to Jetlite
S3	BBR	Santa Barbara Airlines	SANTA BARBARA	Venezuela	
S4	RZO	SATA International	AIR AZORES	Portugal	
S5	TCF	Shuttle America	MERCURY	United States	
S5	TSJ	Trast Aero	TRAST AERO	Kyrgyzstan	
S6		Star Air		Denmark	
S6	SRR	Star Air	WHITESTAR	Denmark	
S7	SBI	S7 Airlines	SIBERIAN AIRLINES	Russia	
S8	CSU	Chari Aviation Services	CHARI SERVICE	Chad	
S8	SWW	Shovkoviy Shlyah	WAY AERO	Ukraine	
S8	SWZ	Skywise Airline	SKYWISE	South Africa	
S9	HSA	East African Safari Air	DUMA	Kenya	
SA	SAA	South African Airways	SPRINGBOK	South Africa	
SB	ACI	Air Caledonie International	AIRCALIN	France	
SC	CDG	Shandong Airlines	SHANDONG	China	
SD	SUD	Sudan Airways	SUDANAIR	Sudan	
SE	SEU	XL Airways France	STARWAY	France	
SF	DTH	Tassili Airlines	TASSILI AIR	Algeria	
SG	JGO	JetsGo	JETSGO	Canada	defunct
SG	SEJ	Spicejet	SPICEJET	India	
SH	FLY	Fly Me Sweden	FLYBIRD	Sweden	
SI	SIH	Skynet Airlines	BLUEJET	Ireland	
SJ	FOM	Freedom Air	FREE AIR	New Zealand	
SK	CNO	SAS Braathens	SCANOR	Norway	
SK	SAS	Scandinavian Airlines	SCANDINAVIAN	Sweden, Denmark and Norway	
SL	RSL	Rio Sul Serviços Aéreos Regionais	RIO SUL	Brazil	defunct
SM	AAW	Aberdeen Airways		United Kingdom	defunct; subsidiary of Air Provence
SM	SRL	Swedline Express	Starline	Sweden	Ceased operations 2006
SN	BEL	Brussels Airlines	BEE-LINE	Belgium	
SN	BXI	Brussels International Airlines	XENIA	Belgium	
SO	AAS	Sunshine Airlines			defunct
SO	HKA	Superior Aviation	SPEND AIR	United States	
SO	OSL	Sosoliso Airlines	SOSOLISO	Nigeria	
SP	SAT	SATA Air Acores	SATA	Portugal	
SQ	SIA	Singapore Airlines	SINGAPORE	Singapore	
SQ	SQC	Singapore Airlines Cargo	SINGCARGO	Singapore	
SR	SWR	Swissair	SWISSAIR	Switzerland	defunct
SS	CRL	Corsairfly	CORSAIR	France	
ST	GMI	Germania	GERMANIA	Germany	
SU	AFL	Aeroflot Russian Airlines	AEROFLOT	Russia	
SV	SVA	Saudia	SAUDIA	Saudi Arabia	
SW	NMB	Air Namibia	NAMIBIA	Namibia	
SX	SKB	Skybus Airlines	SKYBUS	United States	defunct
SX	SRK	Sky Work Airlines	SKYFOX	Switzerland	
SY	SCX	Sun Country Airlines	SUN COUNTRY	United States	
SZ	WOW	Air Southwest	SWALLOW	United Kingdom	defunct
T2	TCG	Thai Air Cargo	THAI CARGO	Thailand	
T3	EZE	Eastern Airways	EASTFLIGHT	United Kingdom	
T4	TIB	TRIP Linhas Aéreas	TRIP	Brazil	IATA code 8R changed to T4 (2010)
T6	TVR	Tavrey Airlines	TAVREY	Ukraine	
T7	TJT	Twin Jet	TWINJET	France	
T9	TRZ	TransMeridian Airlines	TRANS-MERIDIAN	United States	Defunct
T9	TSX	Thai Star Airlines	THAI STAR	Thailand	
TC	ATC	Air Tanzania	TANZANIA	Tanzania	
TD	LUR	Atlantis European Airways		Armenia	
TD	TLP	Tulip Air	TULIPAIR	Netherlands	
TE	IGA	Skytaxi	IGUANA	Poland	
TE	LIL	FlyLal	LITHUANIA AIR	Lithuania	defunct
TF	SCW	Malmö Aviation	SCANWING	Sweden	
TG	THA	Thai Airways International	THAI	Thailand	
TH		BA Connect		United Kingdom	
TH	TSE	Transmile Air Services	TRANSMILE	Malaysia	
TI	TOL	Tol-Air Services	TOL AIR	United States	
TJ	GPD	Tradewind Aviation	GOODSPEED	United States	
TK	THY	Turkish Airlines	TURKISH	Turkey	
TL	ANO	Airnorth	TOPEND	Australia	
TL	TMA	Trans Mediterranean Airlines	TANGO LIMA	Lebanon	
TM	LAM	Linhas Aéreas de Moçambique	MOZAMBIQUE	Mozambique	
TN	THT	Air Tahiti Nui	TAHITI AIRLINES	France	
TO	PSD	President Airlines		Cambodia	
TO	TVF	Transavia France	FRANCE SOLEIL	France	
TP	TAP	TAP Portugal	AIR PORTUGAL	Portugal	
TQ	TDM	Tandem Aero	TANDEM	Moldova	
TR	TBA	Transbrasil	TRANSBRASIL	Brazil	defunct
TR	TGW	Tigerair Singapore	GO CAT	Singapore	
TS	TSC	Air Transat	AIR TRANSAT	Canada	
TT	KLA	Air Lithuania	KAUNAS	Lithuania	defunct
TT	TGW	Tigerair Australia	GO CAT	Australia	
TU	TAR	Tunisair	TUNAIR	Tunisia	
TV	VEX	Virgin Express	VIRGIN EXPRESS	Belgium	
TW	TWB	T'way Air	TWAYAIR	Republic of Korea	
TX	FWI	Air Caraïbes	FRENCH WEST	France	
TX	TAN	Transportes Aéreos Nacionales		Honduras	Defunct
TY	IWD	Iberworld	IBERWORLD	Spain	
TY	TPC	Air Calédonie	AIRCAL	France	
TZ	AMT	ATA Airlines	AMTRAN	United States	defunct
TZ	SCO	Scoot	SCOOTER	Singapore	
TZ	TWG	air-taxi Europe	TWINGOOSE	Germany	
U2	EZY	easyJet	EASY	United Kingdom	
U2	UFS	United Feeder Service	FEEDER EXPRESS	United States	formerly part of United Express
U3	AIA	Avies	AVIES	Estonia	
U4	PMT	PMTair	MULTITRADE	Cambodia	Progress Multitrade
U5	GWY	USA3000 Airlines	GETAWAY	United States	
U6	SVR	Ural Airlines	SVERDLOVSK AIR	Russia	
U7		Northern Dene Airways		Canada	
U7	JUS	USA Jet Airlines	JET USA	United States	
U7	UGA	Air Uganda	UGANDA	Uganda	
U8	RNV	Armavia	ARMAVIA	Armenia	defunct, ICAO code no longer allocated
UA	UAL	United Airlines	UNITED	United States	
UB	UBA	Myanma Airways	UNIONAIR	Myanmar	
UD	HER	Hex'Air	HEX AIRLINE	France	
UE	NAS	Nasair	NASAIRWAYS	Eritrea	
UE	TEP	Transeuropean Airlines	TRANSEURLINE	Russia	
UF	UKM	UM Airlines	UKRAINE MEDITERRANEE	Ukraine	Ukraine Mediterranean Airlines
UG	SEN	SevenAir	S-BAR	United States	
UG	TUI	Tuninter		Tunisia	
UH		US Helicopter Corporation		United States	
UH	USH	US Helicopter	US-HELI	United States	
UI	ECA	Eurocypria Airlines	EUROCYPRIA	Cyprus	
UL	ALK	SriLankan Airlines	SRILANKAN	Sri Lanka	
UM	AZW	Air Zimbabwe	AIR ZIMBABWE	Zimbabwe	
UN	TSO	Transaero Airlines	TRANSOVIET	Russia	
UO	HKE	Hong Kong Express Airways	HONGKONG SHUTTLE	Hong Kong	
UP	BHS	Bahamasair	BAHAMAS	Bahamas	
UQ	OCM	O'Connor Airlines	OCONNOR	Australia	Defunct - Bankrupt
US		Unavia Suisse		Switzerland	
US	AWE	US Airways	CACTUS	United States	
US	USA	US Airways	CACTUS	United States	
UT	UTA	UTair Aviation	UTAIR	Russia	WAS P2 till 2006
UU	REU	Air Austral	REUNION	France	
UX	AEA	Air Europa	EUROPA	Spain	
UY	UYC	Cameroon Airlines	CAM-AIR	Cameroon	defunct
UZ	BRQ	El-Buraq Air Transport	BURAQAIR	Libya	
Used for codesharing
V0	VCV	Conviasa	CONVIASA	Venezuela	
V2	AKT	Karat	AVIAKARAT	Russia	
V2	RBY	Vision Airlines	RUBY	United States	Charter Airline and Las Vegas Tours
V3	KRP	Carpatair	CARPATAIR	Romania	
V4	REK	Reem Air	REEM AIR	Kyrgyzstan	
V5	RYL	Royal Aruban Airlines	ROYAL ARUBAN	Aruba	
V5	VLI	Avolar Aerolíneas	AEROVOLAR	Mexico	defunct
V5	VPA	DanubeWings	VIP TAXI	Slovakia	Former names VIP Air and VIP Wings
V7	SNG	Air Senegal International	AIR SENEGAL	Senegal	defunct
V7	VOE	Volotea			
V8	IAR	Iliamna Air Taxi	ILIAMNA AIR	United States	
V8	VAS	ATRAN Cargo Airlines	ATRAN	Russian Federation	
V9	BTC	BAL Bashkirian Airlines	BASHKIRIAN	Russia	
V9	HCW	Star1 Airlines	STAR1	Lithuania	defunct
VA		Viasa		Venezuela	IATA Code transferred to Virgin Australia
VA	VOZ	Virgin Australia Airlines	VELOCITY	Australia	PREVIOUSLY USED: KANGA, AURORA, VEE-OZ
VB	VIV	Aeroenlaces Nacionales	AEROENLACES	Mexico	Former ICAO code: AEN
VB	VIV	VIVA Aerobus	AEROENLACES	Mexico	
VC	VAL	Voyageur Airways	VOYAGEUR	Canada	
VC	VCX	Ocean Airlines	OCEANCARGO	Italy	
VD	BBB	SwedJet Airways	BLACKBIRD	Sweden	
VD	KPA	Kunpeng Airlines	KUNPENG	China	
VD	LIB	Air Liberté	AIR LIBERTE	France	defunct
VE	AVE	Avensa	AVENSA	Venezuela	defunct
VE	EUJ	EUjet	UNION JET	Ireland	defunct
VE	VLE	C.A.I. Second	VOLA	Italy	
VF	VLU	Valuair	VALUAIR	Singapore	
VG	VLM	VLM Airlines	RUBENS	Belgium	
VH	ALV	Aeropostal Alas de Venezuela	AEROPOSTAL	Venezuela	
VI	VDA	Volga-Dnepr Airlines	VOLGA-DNEPR	Russia	
VJ	AFF	Africa Airways	AFRIWAYS	Benin	
VJ	JTY	Jatayu Airlines	JATAYU	Indonesia	
VK	VGN	Virgin Nigeria Airways	VIRGIN NIGERIA	Nigeria	
VL	VIM	Air VIA		Bulgaria	
VM	VOA	Viaggio Air	VIAGGIO	Bulgaria	
VN	HVN	Vietnam Airlines	VIET NAM AIRLINES	Vietnam	was XV?
VO	TYR	Tyrolean Airways	TYROLEAN	Austria	Renamed from Austrian Arrows
VP	VSP	VASP	VASP	Brazil	defunct
VQ	NVQ	Novo Air	NOVO AIR	Bangladesh	
VR	TCV	TACV	CABOVERDE	Cape Verde	
VS	VIR	Virgin Atlantic Airways	VIRGIN	United Kingdom	
VT	VTA	Air Tahiti	AIR TAHITI	French Polynesia	
VU	VUN	Air Ivoire	AIRIVOIRE	Ivory Coast	defunct
VV	AEW	Aerosvit Airlines	AEROSVIT	Ukraine	defunct
VW	TAO	Aeromar	TRANS-AEROMAR	Mexico	
VX	AES	ACES Colombia	ACES	Colombia	defunct
VX	VRD	Virgin America	REDWOOD	United States	
VY	FOS	Formosa Airlines		Taiwan	defunct
VY	VLG	Vueling Airlines	VUELING	Spain	
VZ	MYT	MyTravel Airways	KESTREL	United Kingdom	Defunct, callsign now used by Thomas Cook Airlines
W1	WDL	WDL Aviation	WDL	Germany	
W2	CWA	Canadian Western Airlines	CANADIAN WESTERN	Canada	
W3	FYH	Flyhy Cargo Airlines	FLY HIGH	Thailand	
W3	SCL	Switfair Cargo	SWIFTAIR	Canada	
W4	BES	Aero Services Executive	BIRD EXPRESS	France	
W5	IRM	Mahan Air	MAHAN AIR	Iran	
W6	WZZ	Wizz Air	WIZZAIR	Hungary	
W7	SAH	Sayakhat Airlines	SAYAKHAT	Kazakhstan	
W8	CJT	Cargojet Airways	CARGOJET	Canada	
W9	AAB	Abelag Aviation	ABG	Belgium	
W9	JAB	Air Bagan	AIR BAGAN	Myanmar	
W9	SGR	Eastwind Airlines	STINGER	United States	defunct
WA	KLC	KLM Cityhopper	KLM	Netherlands	
WA	WAL	Western Airlines	WESTERN	United States	defunct
WB	RWD	Rwandair Express	RWANDAIR	Rwanda	
WC	ISV	Islena De Inversiones		Honduras	
WD	DSR	DAS Air Cargo	DAIRAIR	Uganda	
WD*	AAN	Amsterdam Airlines	AMSTEL	Netherlands	Former IATA code: FH*
WE	CWC	Centurion Air Cargo	CHALLENGE CARGO	United States	
WF	WIF	Widerøe	WIDEROE	Norway	
WG	SWG	Sunwing Airlines	SUNWING	Canada	
WH	CNW	China Northwest Airlines	CHINA NORTHWEST	China	defunct
WH	WEB	WebJet Linhas Aéreas	WEB-BRASIL	Brazil	
WK	AFB	American Falcon	AMERICAN FALCON	Argentina	defunct
WK	EDW	Edelweiss Air	EDELWEISS	Switzerland	
WN	SWA	Southwest Airlines	SOUTHWEST	United States	
WO	WOA	World Airways	WORLD	United States	
WR	HRH	Royal Tongan Airlines	TONGA ROYAL	Tonga	
WS	WEN	WestJet Encore	ENCORE	Canada	
WS	WJA	WestJet	WESTJET	Canada	
WT	WSG	Wasaya Airways	WASAYA	Canada	
WV	SWV	Swe Fly	FLYING SWEDE	Sweden	
WW	BMI	Bmibaby	BABY	United Kingdom	Ceased operations
WW	WOW	WOW air	WOW air	Iceland	
WX	BCY	CityJet	CITY JET	Ireland	
WX	BCY	CityJet	CITY-IRELAND	Ireland	
WY	OMA	Oman Air	OMAN AIR	Oman	
WZ	WSF	West African Airlines		Benin	
X3	HLX	Hapag-Lloyd Express (TUIfly)	YELLOW CAB	Germany	
X7	CHF	Chitaavia	CHITA	Russia	
X9	NVD	Avion Express	NORDVIND	Lithuania	Name changed from Nordic Solutions Air
XC	CAI	Corendon Airlines	CORENDON	Turkey	Turistik Hava Tasimacilik
XF	VLK	Vladivostok Air	VLADAIR	Russia	
XJ	MES	Mesaba Airlines	MESABA	United States	
XK	CCM	Corse Méditerranée	CORSICA	France	Name changed to Air Corsica
XL	LNE	Aerolane	AEROLANE	Ecuador	Líneas Aéreas Nacionales Del Ecuador
XM		J-Air	J AIR	Japan	
XO	CXH	China Xinhua Airlines	XINHUA	China	
XO	LTE	LTE International Airways	FUN JET	Spain	
XP	CXP	Western	RUBY MOUNTAIN	United States	defunct
XP	CXP	Xtra Airways	CASINO EXPRESS	United States	
XQ	SXS	SunExpress	SUNEXPRESS	Turkey	
XS	SIT	SITA		Belgium	
XT	AXL	Air Exel	EXEL COMMUTER	Netherlands	defunct
XT	SKT	SkyStar Airways	SKY YOU	Thailand	
Y0	EMJ	Yellow Air Taxi/Friendship Airways		United States	
Y2	AFJ	Alliance Air	JAMBO	Uganda	Ceased operations 08/10/2000
Y2	GSM	Flyglobespan	GLOBESPAN	United Kingdom	defunct
Y4	VOI	Volaris	VOLARIS	Mexico	
Y5	GMR	Golden Myanmar Airlines	GOLDEN MYANMAR	Myanmar	
Y5	PCE	Pace Airlines	PACE	United States	
Y6	BTV	Batavia Air	BATAVIA	Indonesia	As of June 1, 2010, IATA code changed to Y6.
Y8	YZR	Yangtze River Express	YANGTZE RIVER	China	
Y9	IRK	Kish Air	KISHAIR	Iran	
YD	CAT	Cologne Air Transport GmbH		Germany	defunct since 1996
YE	ACQ	Aryan Cargo Express		India	
YH	WCW	West Caribbean Airways	WEST	Colombia	
YK	KYV	Cyprus Turkish Airlines	AIRKIBRIS	Turkey	Ceased operations 2010
YL	LLM	Yamal Airlines	YAMAL	Russia	
YM	MGX	Montenegro Airlines	MONTENEGRO	Montenegro	former callsign was "MONTAIR"
YS	RAE	Régional Compagnie Aérienne Européenne	REGIONAL EUROPE	France	
YT	TGA	Air Togo	AIR TOGO	Togo	defunct
YU	ADM	Dominair	DOMINAIR	Dominican Republic	defunct; former IATA code: SS; former name: Aerolíneas Dominicanas, ICAO code no longer allocated
YV	ASH	Mesa Airlines	AIR SHUTTLE	United States	
YW	ANE	Air Nostrum	AIR NOSTRUM	Spain	
YX	MEP	Midwest Airlines	MIDEX	United States	
Z3	SMJ	Avient Aviation	AVAVIA	Zimbabwe	
Z4	OOM	Zoom Airlines	ZOOM	Canada	defunct, ICAO Code and callsign no longer allocated
Z5	GMG	GMG Airlines	GMG	Bangladesh	
Z7*	ADK	ADC Airlines	ADCO	Nigeria	defunct; former name: Aviation Development Company
Z8	AZN	Línea Aérea Amaszonas		Bolivia	
ZA	CYD	AccessAir	CYCLONE	United States	defunct
ZA	SUW	Interavia Airlines	ASTAIR	Russia	
ZB	BUB	Air Bourbon	BOURBON	Reunion	defunct
ZB	MON	Monarch Airlines	MONARCH	United Kingdom	
ZE	AZE	Arcus-Air Logistic	ARCUS AIR	Germany	
ZE	ESR	Eastar Jet	EASTAR	South Korea	
ZE	LCD	Líneas Aéreas Azteca	LINEAS AZTECA	Mexico	defunct
ZG	VVM	Viva Macau	JACKPOT	Macao	
ZH	CSZ	Shenzhen Airlines	SHENZHEN AIR	China	
ZI	AAF	Aigle Azur	AIGLE AZUR	France	Former name: Lucas Aigle Azur; former IATA code: LK
ZK	GLA	Great Lakes Airlines	LAKES AIR	United States	
ZL	RXA	Regional Express	REX	Australia	
ZP	AZQ	Silk Way Airlines	SILK LINE	Azerbaijan	
ZS	AZI	Azzurra Air	AZZURRA	Italy	defunct
ZS	SMY	Sama Airlines	NAJIM	Saudi Arabia	
ZT	AWC	Titan Airways	ZAP	United Kingdom	
ZU	HCY	Helios Airways	HELIOS	Cyprus	
ZV	AMW	Air Midwest	AIR MIDWEST	United States	defunct
ZW	AWI	Air Wisconsin	AIR WISCONSIN	United States	
ZX	ABL	Air BC	AIRCOACH	Canada	Merged into Air Canada Jazz
ZX	GGN	Air Georgian	GEORGIAN	Canada	
ZY	SHY	Sky Airlines	ANTALYA BIRD	Turkey	
merged with Delta Air Lines
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

# carriers_dict = dict(L.strip().split("\t") for L in carriers.strip().split("\n"))

carriers_dict = {}
for L in carriers2.strip().split("\n"):
    parts = L.split("\t")
    if len(parts)<3:
        # print parts
        continue
    iata, _, name = parts[:3]
    assert iata.strip()==iata
    if not re.search(r'^[A-Z0-9]{2}$', iata):
        # these all look fine actually
        # print parts  
        pass
    assert name.strip()==name
    carriers_dict[iata] = {'code':iata, 'name': name}


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
        # return "%s - %s" % (code, carriers_dict[code])
        return carriers_dict[code]['name']


    if code in airports_dict:
        d = airports_dict[code]
        # return "{code} - {name} ({city}, {state})".format(**d)
        # return "{code} - {name}, {city}".format(**d)
        return "{name} - {city}".format(**d)

    return code

