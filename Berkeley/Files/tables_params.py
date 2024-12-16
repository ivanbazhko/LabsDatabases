def getTableParams(name):
    if name == 'Airlines' or name == 'airlines':
        return airlines
    elif name == 'Airplanes' or name == 'airplanes':
        return airplanes
    elif name == 'Passengers' or name == 'passengers':
        return passengers
    elif name == 'Destinations' or name == 'destinations':
        return destinations
    elif name == 'Flights' or name == 'flights':
        return flights
    elif name == 'Flights-Passengers' or name == 'flightspassengers':
        return flightspassengers
    elif name == 'Flights-Destinations' or name == 'flightsdestinations':
        return flightsdestinations
    else:
        return flights

# name, expandable (many-to-many), notnull, foreign, (table, field), validation, type, unique

airlines = (
    'airlines',
    ('code', 0, 1, 0, ('', ''), 1, 'c2', 1),
    ('name', 0, 1, 0, ('', ''), 0, '', 0),
    ('country', 0, 1, 0, ('', ''), 0, '', 0),
    1,
    3
)

airplanes = (
    'airplanes',
    ('code', 0, 1, 0, ('', ''), 0, '', 1),
    ('name', 0, 1, 0, ('', ''), 0, '', 0),
    ('manufacturer', 0, 1, 0, ('', ''), 0, '', 0),
    ('capacity', 0, 1, 0, ('', ''), 1, 'i', 0),
    ('width', 0, 1, 0, ('', ''), 1, 'i', 0),
    1,
    5
)

passengers = (
    'passengers',
    ('passport_number', 0, 1, 0, ('', ''), 0, '', 1),
    ('first_name', 0, 1, 0, ('', ''), 0, '', 0),
    ('last_name', 0, 1, 0, ('', ''), 0, '', 0),
    ('email', 0, 1, 0, ('', ''), 1, 'em', 0),
    1,
    4
)

destinations = (
    'destinations',
    ('code', 0, 1, 0, ('', ''), 1, 'c3', 1),
    ('name', 0, 1, 0, ('', ''), 0, '', 0),
    ('country', 0, 1, 0, ('', ''), 0, '', 0),
    1,
    3
)

flights = (
    'flights',
    ('flight_number', 0, 1, 0, ('', ''), 0, '', 1),
    ('airline', 0, 1, 1, ('airlines', 'name'), 0, '', 0),
    ('airplane', 0, 1, 1, ('airplanes', 'code'), 0, '', 0),
    ('days', 0, 1, 0, ('', ''), 1, 'ds', 0),
    ('arrival_time', 0, 0, 0, ('', ''), 1, 't', 0),
    ('departure_time', 0, 0, 0, ('', ''), 1, 't', 0),
    1,
    6
)

flightspassengers = (
    'flightspassengers',
    ('flight', 0, 1, 1, ('flights', 'flight_number'), 0, '', 0),
    ('passenger', 0, 1, 1, ('passengers', 'passport_number'), 0, '', 0),
    0,
    2
)

flightsdestinations = (
    'flightsdestinations',
    ('flight', 0, 1, 1, ('flights', 'flight_number'), 0, '', 0),
    ('destination', 0, 1, 1, ('destinations', 'code'), 0, '', 0),
    0,
    2
)