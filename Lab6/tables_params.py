def getTableParams(name):
    if name == 'Авиакомпании':
        return airlines
    elif name == 'Билеты':
        return tickets
    elif name == 'Должности':
        return jobs
    elif name == 'Допуски к направлениям':
        return destinationaccess
    elif name == 'Допуски к самолётам':
        return airplaneaccess
    elif name == 'Направления':
        return destinations
    elif name == 'Пассажиры':
        return passengers
    elif name == 'Рейсы':
        return flights
    elif name == 'Самолёты':
        return airplanes
    elif name == 'Сотрудники':
        return employees
    else:
        return airlines
    
# st - string +
# s2 - string(2) +
# nt - ticket number +
# n4 - number < 10000 +
# np - passport number +
# fl - float +
# s3 - string(3) +
# nu - number +
# wd - days of week +
# tm - time +

airlines = (
    'Авиакомпании',
    ('Название', 40, 0, 'st'),
    ('Код', 10, 1, 's2'),
    ('Страна', 30, 0, 'st'),
    3
)

tickets = (
    'Билеты',
    ('Номер билета', 15, 1, 'nt'),
    ('Авиакомпания', 30, 0, 's2'),
    ('Номер рейса', 15, 0, 'n4'),
    ('Пассажир', 15, 0, 'np'),
    4
)

jobs = (
    'Должности',
    ('Название', 50, 1, 'st'),
    ('Оклад', 20, 0, 'fl'),
    ('Описание', 105, 0, 'st'),
    3
)

destinationaccess = (
    '"Допуски к направлениям"',
    ('Сотрудник', 15, 1, 'np'),
    ('Направление', 15, 1, 's3'),
    2
)

airplaneaccess = (
    '"Допуски к самолётам"',
    ('Сотрудник', 15, 1, 'np'),
    ('Самолёт', 30, 1, 'st'),
    2
)

destinations = (
    'Направления',
    ('Название', 30, 0, 'st'),
    ('Код', 10, 1, 's3'),
    ('Страна', 30, 0, 'st'),
    ('Расстояние', 20, 0, 'nu'),
    4
)

passengers = (
    'Пассажиры',
    ('Фамилия', 30, 0, 'st'),
    ('Имя', 30, 0, 'st'),
    ('Отчество', 30, 0, 'st'),
    ('Номер паспорта', 20, 1, 'np'),
    ('Бонусы', 10, 0, 'nu'),
    5
)

flights = (
    'Рейсы',
    ('Авиакомпания', 15, 1, 's2'),
    ('Номер', 10, 1, 'n4'),
    ('Самолёт', 25, 0, 'st'),
    ('Направление', 15, 0, 's3'),
    ('Дни недели', 15, 0, 'wd'),
    ('Время', 15, 0, 'tm'),
    6
)

airplanes = (
    'Самолёты',
    ('Название', 40, 1, 'st'),
    ('Производитель', 40, 0, 'st'),
    ('Вместимость', 20, 0, 'nu'),
    3
)

employees = (
    'Сотрудники',
    ('Фамилия', 30, 0, 'st'),
    ('Имя', 30, 0, 'st'),
    ('Отчество', 30, 0, 'st'),
    ('Должность', 50, 0, 'st'),
    ('Номер паспорта', 20, 1, 'np'),
    5
)
