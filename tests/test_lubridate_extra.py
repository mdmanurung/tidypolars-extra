import tidypolars_extra as tp
from tidypolars_extra import col


def test_as_datetime():
    """Can convert string to datetime"""
    df = tp.tibble(x=['2021-01-01 12:30:45', '2021-06-15 08:00:00'])
    actual = df.mutate(dt=tp.as_datetime(col('x'), fmt='%Y-%m-%d %H:%M:%S'))
    assert actual.pull('dt').dtype == tp.Datetime, "as_datetime failed"


def test_hour():
    """Can extract hour from datetime"""
    df = tp.tibble(x=['2021-01-01 12:30:45', '2021-01-01 08:15:00'])
    df = df.mutate(dt=tp.as_datetime('x', fmt='%Y-%m-%d %H:%M:%S'))
    actual = df.mutate(h=tp.hour('dt'))
    assert actual.pull('h').to_list() == [12, 8], "hour failed"


def test_minute():
    """Can extract minute from datetime"""
    df = tp.tibble(x=['2021-01-01 12:30:45', '2021-01-01 08:15:00'])
    df = df.mutate(dt=tp.as_datetime('x', fmt='%Y-%m-%d %H:%M:%S'))
    actual = df.mutate(m=tp.minute('dt'))
    assert actual.pull('m').to_list() == [30, 15], "minute failed"


def test_second():
    """Can extract second from datetime"""
    df = tp.tibble(x=['2021-01-01 12:30:45', '2021-01-01 08:15:30'])
    df = df.mutate(dt=tp.as_datetime('x', fmt='%Y-%m-%d %H:%M:%S'))
    actual = df.mutate(s=tp.second('dt'))
    assert actual.pull('s').to_list() == [45, 30], "second failed"


def test_make_datetime():
    """Can create a datetime from components"""
    df = tp.tibble(y=[2021], m=[12], d=[1])
    actual = df.mutate(dt=tp.make_datetime(col('y'), col('m'), col('d'), 10, 30, 0))
    assert actual.pull('dt').dtype == tp.Datetime, "make_datetime failed"


def test_month():
    """Can extract month from date"""
    df = tp.tibble(x=['2021-03-15', '2021-11-01'])
    df = df.mutate(date=tp.as_date('x'))
    actual = df.mutate(m=tp.month('date'))
    assert actual.pull('m').to_list() == [3, 11], "month failed"


def test_dt_round():
    """Can round datetime"""
    df = tp.tibble(x=['2021-01-01 12:34:56'])
    df = df.mutate(dt=tp.as_datetime('x', fmt='%Y-%m-%d %H:%M:%S'))
    actual = df.mutate(rounded=tp.dt_round('dt', 'h', 1))
    # 12:34:56 rounded to nearest hour should be 13:00:00
    assert actual.pull('rounded').dt.hour().to_list() == [13], "dt_round failed"
