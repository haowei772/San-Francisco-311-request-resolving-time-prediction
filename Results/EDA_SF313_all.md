***********df shape**************
(2092917, 16)
**********Number of features***************
16
**********features***************
['CaseID' 'Opened' 'Closed' 'Updated' 'Status' 'Status Notes'
 'Responsible Agency' 'Category' 'Request Type' 'Request Details' 'Address'
 'Supervisor District' 'Neighborhood' 'Point' 'Source' 'Media URL']
*******head of df******************
   CaseID                  Opened                  Closed  \
0  322571  11/30/2008 11:53:00 PM  12/01/2008 03:19:00 PM
1  322568  11/30/2008 11:13:00 PM  07/21/2009 04:24:00 PM
2  322567  11/30/2008 11:07:00 PM  12/27/2008 06:07:00 AM
3  322566  11/30/2008 10:56:00 PM  07/21/2009 04:24:00 PM
4  322565  11/30/2008 10:46:00 PM  12/13/2008 10:50:00 AM

                  Updated  Status Status Notes  \
0  12/01/2008 03:19:00 PM  Closed          NaN
1  07/21/2009 04:24:00 PM  Closed          NaN
2  12/27/2008 06:07:00 AM  Closed          NaN
3  07/21/2009 04:24:00 PM  Closed          NaN
4  12/13/2008 10:50:00 AM  Closed          NaN

                Responsible Agency                      Category  \
0         PUC - Electric/Power - G              General Requests
1                    DPW Ops Queue              Illegal Postings
2                    DPW Ops Queue              Illegal Postings
3                    DPW Ops Queue  Street and Sidewalk Cleaning
4  RPD Park Service Area GGP Queue         Rec and Park Requests

                                   Request Type  \
0          puc - electric - request_for_service
1  Illegal Postings - Posting_Too_Large_in_Size
2         Illegal Postings - Affixed_Improperly
3                             Sidewalk_Cleaning
4                 Park - Structural_Maintenance

                         Request Details  \
0   puc - electric - request_for_service
1  Posting_Too_Large_in_Size on Sidewalk
2         Affixed_Improperly on Sidewalk
3                                Garbage
4                                  Other

                                      Address  Supervisor District  \
0         Intersection of 21ST ST and CAPP ST                  9.0
1    Intersection of BUSH ST and VAN NESS AVE                  3.0
2  Intersection of EUCLID AVE and MASONIC AVE                  2.0
3      1566 HYDE ST, SAN FRANCISCO, CA, 94109                  3.0
4     GGP Panhandle, SAN FRANCISCO, CA, 94117                  5.0

       Neighborhood                                  Point    Source Media URL
0           Mission  (37.7571008516766, -122.417811874214)  Voice In       NaN
1          Nob Hill  (37.7884895281133, -122.421948485141)  Voice In       NaN
2  Western Addition  (37.7850837365507, -122.447620029034)  Voice In       NaN
3          Nob Hill         (37.795328529, -122.418067787)  Voice In       NaN
4    Haight Ashbury           (37.772204762, -122.4487004)  Voice In       NaN
*******info of df******************
<class 'pandas.core.frame.DataFrame'>
Int64Index: 2092917 entries, 0 to 2092916
Data columns (total 16 columns):
CaseID                 int64
Opened                 object
Closed                 object
Updated                object
Status                 object
Status Notes           object
Responsible Agency     object
Category               object
Request Type           object
Request Details        object
Address                object
Supervisor District    float64
Neighborhood           object
Point                  object
Source                 object
Media URL              object
dtypes: float64(1), int64(1), object(14)
memory usage: 271.5+ MB
None
********description of df*****************
             CaseID  Supervisor District
count  2.092917e+06         2.082120e+06
mean   3.501797e+06         6.095616e+00
std    2.189488e+06         3.109422e+00
min    1.855800e+05        -1.000000e+00
25%    1.053734e+06         3.000000e+00
50%    3.813822e+06         6.000000e+00
75%    5.495766e+06         9.000000e+00
max    6.909918e+06         1.100000e+01
*********number of unique values**********
CaseID   2092917
Opened   2029272
Closed   1485294
Updated   1570351
Status   2
Status Notes   348637
Responsible Agency   409
Category   28
Request Type   1419
Request Details   133593
Address   199413
Supervisor District   14
Neighborhood   126
Point   217287
Source   9
Media URL   377721
*********number of missing values**********
CaseID   0
Opened   0
Closed   99549
Updated   0
Status   0
Status Notes   662894
Responsible Agency   0
Category   0
Request Type   15320
Request Details   79412
Address   52
Supervisor District   10797
Neighborhood   136020
Point   74700
Source   38
Media URL   1712026

************ Status value counts ***********
Closed    1993368
Open        99549
Name: Status, dtype: int64
************ Responsible Agency value counts ***********
DPW Ops Queue                                                    884244
Recology_Abandoned                                               217178
DPT Abandoned Vehicles Work Queue                                146732
DPW BSM Queue                                                     91698
DPT Meter_Bike Queue                                              67812
PUC Sewer Ops                                                     60794
MUNI Work Queue                                                   44286
311 HA SR Queue                                                   36079
311 Supervisor Queue                                              32717
DPW BSSR Queue                                                    31007
Housing Authority SR Queue                                        29834
PG and E - Streetlights Queue                                     28624
PUC Streetlights Queue                                            25239
Clear Channel - Transit Queue                                     21431
311 Service Request Queue - Hold                                  21295
PUC - Water - G                                                   20443
Recology_Overflowing                                              15243
DPH - Environmental Health - G                                    13503
DPW - Bureau of Street Environmental Services - G                 12915
DPT SignShop Surveyed - Area 1 Queue                              12830
SSP - MTA Feedback Queue                                          12606
DPT SignShop Surveyed - Area 2 Queue                              12252
SFMTA - Temporary Sign Request Queue                              10758
DPT Signal Queue                                                  10339
SFMTA - Parking Enforcement - G                                   10109
DPW - Bureau of Street Use and Mapping - G                         9905
Police - Homeless Concerns Queue                                   9711
SFMTA - Temporary Sign Request Installation/Enforcement Queue      9599
Treasurer/Tax Collector - G                                        8946
311 Service Request Queue                                          8459
                                                                  ...  
Risk Management - G                                                   1
PUC - Billing - G - Hold                                              1
Clerk of the Board Queue - RCalonsag                                  1
Board of Supervisors - District 1 - G - Hold                          1
Mayors Office on Disability - G - Hold                                1
Rapid Deploy Queue                                                    1
Treasurer/Tax Collector - PIN Reset Queue                             1
DPT - Accessible Pedestrian Signal - G - Hold                         1
zzRPD Cement Masons Queue - DO NOT USE                                1
Board of Supervisors - District 3 - G - Hold                          1
Assessor - Transactions - Hold                                        1
Assessor - Public Service/Exemptions - Hold                           1
HSA - Other - G - Hold                                                1
PUC - SCSR Queue                                                      1
zzRPD Painters Queue - DO NOT USE                                     1
DPH - Homeless Outreach Team - G                                      1
Convention Facilities - G - Hold                                      1
Art Commission - G - Hold                                             1
zzRPD - Other - G - Hold - DO NOT USE                                 1
Board of Supervisors - District 11 - G                                1
Assessor - Business Personal Property - Hold                          1
zzSFMTA - Abandoned Vehicles - G - Hold - DO NOT USE                  1
Rent Board - G - Hold                                                 1
Office of Citizens Complaints - G - Hold                              1
RPD - Park Patrol - G - Hold                                          1
zzRPD Planning Queue - DO NOT USE                                     1
Labor Standards Enforcement - G - Hold                                1
Human Resources - G - Hold                                            1
Board of Supervisors - Clerk of the Board - G - Hold                  1
Board of Supervisors - District 7 - G - Hold                          1
Name: Responsible Agency, dtype: int64
************ Category value counts ***********
Street and Sidewalk Cleaning    752397
Graffiti Public Property        200624
General Requests                156015
Graffiti Private Property       145932
Abandoned Vehicle               145778
Damaged Property                 77393
SFHA Requests                    65899
Sewer Issues                     64119
MUNI Feedback                    56238
Streetlights                     54066
Tree Maintenance                 50347
Street Defects                   44978
Litter Receptacles               41281
Illegal Postings                 39424
Sign Repair                      36176
Rec and Park Requests            34554
Temporary Sign Request           31338
Sidewalk or Curb                 30570
311 External Request             17678
Blocked Street or SideWalk       16990
Residential Building Request      8846
Color Curb                        6492
Catch Basin Maintenance           5446
Noise Report                      5288
Construction Zone Permits         2650
Interdepartmental Request         1618
Unpermitted Cab Complaint          393
DPW Volunteer Programs             387
Name: Category, dtype: int64
************ Neighborhood value counts ***********
Mission                     216458
South of Market             146095
NaN                         136020
Western Addition             67911
Inner Richmond               60007
Bayview                      58427
Outer Sunset                 57177
Bernal Heights               56859
Tenderloin                   51006
Excelsior                    50752
Outer Richmond               49534
Downtown/Civic Center        48180
Potrero Hill                 42753
Haight Ashbury               41302
Nob Hill                     38546
Mission Dolores              37085
Chinatown                    35476
North Beach                  31539
Financial District           28871
Civic Center                 28807
Visitacion Valley            27957
Russian Hill                 27722
Inner Sunset                 27578
Lower Nob Hill               26196
Parkside                     26178
Pacific Heights              25897
Portola                      24198
Outer Mission                23429
Castro/Upper Market          22600
Noe Valley                   22451
                             ...  
Lake Street                   2596
Stonestown                    2579
Clarendon Heights             2371
Forest Hill                   2290
Little Hollywood              2221
Ingleside Terraces            2215
McLaren Park                  2163
Laguna Honda                  2031
Merced Manor                  1959
Westwood Park                 1954
Anza Vista                    1915
Midtown Terrace               1898
Aquatic Park / Ft. Mason      1636
India Basin                   1516
Sherwood Forest               1350
Forest Knolls                 1342
Parkmerced                    1298
Mt. Davidson Manor            1090
St. Francis Wood               834
Balboa Terrace                 810
Candlestick Point SRA          632
Treasure Island                562
Presidio National Park         556
Presidio                       555
Westwood Highlands             500
Lincoln Park / Ft. Miley       455
Monterey Heights               374
Treasure Island/YBI            110
Yerba Buena Island              71
Lake Shore                       1
Name: Neighborhood, dtype: int64
************ Source value counts ***********
Voice In             1219344
Open311               464107
Web Self Service      294763
Integrated Agency      85860
Twitter                23723
Other Department        4080
e-mail In                998
NaN                       38
Mail In                    4
Name: Source, dtype: int64
