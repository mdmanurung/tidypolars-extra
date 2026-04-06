import polars as pl
from .utils import _col_expr

__all__ = [
    "as_date",
    "as_datetime",
    "ceiling_date",
    "days",
    "difftime",
    "floor_date",
    "hour",
    "hours",
    "make_date",
    "make_datetime",
    "mday",
    "microseconds",
    "milliseconds",
    "minute",
    "minutes",
    "month",
    "now",
    "quarter",
    "dt_round",
    "second",
    "seconds",
    "today",
    "wday",
    "week",
    "weeks",
    "yday",
    "year"
]

def as_date(x, fmt = None):
    """
    Convert a string to a Date

    Parameters
    ----------
    x : Expr, Series
        Column to operate on
    fmt: str
        "yyyy-mm-dd"

    Examples
    --------
    >>> df = tp.tibble(x = ['2021-01-01', '2021-10-01'])
    >>> df.mutate(date_x = tp.as_date(col('x')))
    """
    x = _col_expr(x)
    return x.str.strptime(pl.Date, format = fmt)

def as_datetime(x, fmt = None):
    """
    Convert a string to a Datetime

    Parameters
    ----------
    x : Expr, Series
        Column to operate on
    fmt: str
        "yyyy-mm-dd"

    Examples
    --------
    >>> df = tp.tibble(x = ['2021-01-01', '2021-10-01'])
    >>> df.mutate(date_x = tp.as_datetime(col('x')))
    """
    x = _col_expr(x)
    return x.str.strptime(pl.Datetime, format = fmt)

def hour(x):
    """
    Extract the hour from a datetime

    Parameters
    ----------
    x : Expr, Series
        Column to operate on

    Examples
    --------
    >>> df.mutate(hour = tp.hour(col('x')))
    """
    x = _col_expr(x)
    return x.dt.hour()

def mday(x):
    """
    Extract the month day from a date from 1 to 31.

    Parameters
    ----------
    x : Expr, Series
        Column to operate on

    Examples
    --------
    >>> df.mutate(monthday = tp.mday(col('x')))
    """
    x = _col_expr(x)
    return x.dt.day()

def make_date(year = 1970, month = 1, day = 1):
    """
    Create a date object

    Parameters
    ----------
    year : Expr, str, int
        Column or literal
    month : Expr, str, int
        Column or literal
    day : Expr, str, int
        Column or literal

    Examples
    --------
    >>> df.mutate(date = tp.make_date(2000, 1, 1))
    """
    return pl.date(year, month, day)

def make_datetime(year = 1970, month = 1, day = 1, hour = 0, minute = 0, second = 0):
    """
    Create a datetime object

    Parameters
    ----------
    year : Expr, str, int
        Column or literal
    month : Expr, str, int
        Column or literal
    day : Expr, str, int
        Column or literal
    hour : Expr, str, int
        Column or literal
    minute : Expr, str, int
        Column or literal
    second : Expr, str, int
        Column or literal

    Examples
    --------
    >>> df.mutate(date = tp.make_datetime(2000, 1, 1))
    """
    return pl.datetime(year, month, day, hour, minute, second)

def minute(x):
    """
    Extract the minute from a datetime

    Parameters
    ----------
    x : Expr, Series
        Column to operate on

    Examples
    --------
    >>> df.mutate(hour = tp.minute(col('x')))
    """
    x = _col_expr(x)
    return x.dt.minute()

def month(x):
    """
    Extract the month from a date

    Parameters
    ----------
    x : Expr, Series
        Column to operate on

    Examples
    --------
    >>> df.mutate(year = tp.month(col('x')))
    """
    x = _col_expr(x)
    return x.dt.month()

def quarter(x):
    """
    Extract the quarter from a date

    Parameters
    ----------
    x : Expr, Series
        Column to operate on

    Examples
    --------
    >>> df.mutate(quarter = tp.quarter(col('x')))
    """
    x = _col_expr(x)
    return ((x.dt.month() - 1) // 3) + 1

def dt_round(x, rule, n):
    """
    Round the datetime

    Parameters
    ----------
    x : Expr, Series
        Column to operate on
    rule : str
        Units of the downscaling operation.
        Any of:
        ``"month"``, ``"week"``, ``"day"``, ``"hour"``, ``"minute"``, ``"second"``.
    n : int
        Number of units (e.g. 5 "day", 15 "minute".

    Examples
    --------
    >>> df.mutate(monthday = tp.mday(col('x')))
    """
    x = _col_expr(x)
    return x.dt.round(f"{n}{rule}")

def second(x):
    """
    Extract the second from a datetime

    Parameters
    ----------
    x : Expr, Series
        Column to operate on

    Examples
    --------
    >>> df.mutate(hour = tp.minute(col('x')))
    """
    x = _col_expr(x)
    return x.dt.second()

def wday(x):
    """
    Extract the weekday from a date from sunday = 1 to saturday = 7.

    Parameters
    ----------
    x : Expr, Series
        Column to operate on

    Examples
    --------
    >>> df.mutate(weekday = tp.wday(col('x')))
    """
    x = _col_expr(x)
    return x.dt.weekday() + 1

def week(x):
    """
    Extract the week from a date

    Parameters
    ----------
    x : Expr, Series
        Column to operate on

    Examples
    --------
    >>> df.mutate(week = tp.week(col('x')))
    """
    x = _col_expr(x)
    return x.dt.week()

def yday(x):
    """
    Extract the year day from a date from 1 to 366.

    Parameters
    ----------
    x : Expr, Series
        Column to operate on

    Examples
    --------
    >>> df.mutate(yearday = tp.yday(col('x')))
    """
    x = _col_expr(x)
    return x.dt.ordinal_day()

def year(x):
    """
    Extract the year from a date

    Parameters
    ----------
    x : Expr, Series
        Column to operate on

    Examples
    --------
    >>> df.mutate(year = tp.year(col('x')))
    """
    x = _col_expr(x)
    return x.dt.year()

def today():
    """
    Return the current date as a polars literal

    Returns
    -------
    Expr
        A literal expression with today's date.

    Examples
    --------
    >>> df.mutate(today = tp.today())
    """
    from datetime import date
    return pl.lit(date.today())

def now():
    """
    Return the current datetime as a polars literal

    Returns
    -------
    Expr
        A literal expression with the current datetime.

    Examples
    --------
    >>> df.mutate(now = tp.now())
    """
    from datetime import datetime
    return pl.lit(datetime.now())

def difftime(x, y, units = 'days'):
    """
    Compute time differences in specified units

    Parameters
    ----------
    x : Expr, str
        Start date/datetime column
    y : Expr, str
        End date/datetime column
    units : str
        Units for the result: 'days', 'hours', 'minutes', 'seconds', 'weeks'

    Returns
    -------
    Expr
        Numeric expression with the time difference.

    Examples
    --------
    >>> df.mutate(diff = tp.difftime('date1', 'date2', units='days'))
    """
    x = _col_expr(x)
    y = _col_expr(y)
    diff = (x - y).dt.total_microseconds()
    divisors = {
        'seconds': 1_000_000,
        'minutes': 60_000_000,
        'hours': 3_600_000_000,
        'days': 86_400_000_000,
        'weeks': 604_800_000_000,
    }
    if units not in divisors:
        raise ValueError(f"`units` must be one of {list(divisors.keys())}")
    return diff / divisors[units]

def _unit_to_polars(unit):
    """Convert unit name to polars duration string"""
    mapping = {
        'year': '1y', 'month': '1mo', 'week': '1w', 'day': '1d',
        'hour': '1h', 'minute': '1m', 'second': '1s',
    }
    if unit not in mapping:
        raise ValueError(f"`unit` must be one of {list(mapping.keys())}")
    return mapping[unit]

def floor_date(x, unit = 'month'):
    """
    Round date down to the nearest unit

    Parameters
    ----------
    x : Expr, str
        Date/datetime column
    unit : str
        Unit to round to: 'year', 'month', 'week', 'day', 'hour', 'minute', 'second'

    Returns
    -------
    Expr
        Date/datetime rounded down.

    Examples
    --------
    >>> df.mutate(month_start = tp.floor_date('date', 'month'))
    """
    x = _col_expr(x)
    return x.dt.truncate(_unit_to_polars(unit))

def ceiling_date(x, unit = 'month', change_on_boundary = False):
    """
    Round date up to the nearest unit

    Parameters
    ----------
    x : Expr, str
        Date/datetime column
    unit : str
        Unit to round to: 'year', 'month', 'week', 'day', 'hour', 'minute', 'second'
    change_on_boundary : bool
        If False (default), dates already at a boundary are unchanged.
        If True, boundary dates are bumped to the next unit.

    Returns
    -------
    Expr
        Date/datetime rounded up.

    Examples
    --------
    >>> df.mutate(month_end = tp.ceiling_date('date', 'month'))
    """
    x = _col_expr(x)
    pl_unit = _unit_to_polars(unit)
    floored = x.dt.truncate(pl_unit)
    ceiled = x.dt.offset_by(pl_unit).dt.truncate(pl_unit)
    if change_on_boundary:
        return ceiled
    # If already at boundary, keep as-is
    return pl.when(x == floored).then(x).otherwise(ceiled)

def days(n = 1):
    """
    Create a duration of n days

    Parameters
    ----------
    n : int
        Number of days

    Returns
    -------
    Expr
        A duration literal.

    Examples
    --------
    >>> df.mutate(tomorrow = col('date') + tp.days(1))
    """
    return pl.duration(days=n)

def weeks(n = 1):
    """
    Create a duration of n weeks

    Parameters
    ----------
    n : int
        Number of weeks

    Returns
    -------
    Expr
        A duration literal.

    Examples
    --------
    >>> df.mutate(next_week = col('date') + tp.weeks(1))
    """
    return pl.duration(weeks=n)

def hours(n = 1):
    """
    Create a duration of n hours

    Parameters
    ----------
    n : int
        Number of hours

    Returns
    -------
    Expr
        A duration literal.

    Examples
    --------
    >>> df.mutate(later = col('datetime') + tp.hours(2))
    """
    return pl.duration(hours=n)

def minutes(n = 1):
    """
    Create a duration of n minutes

    Parameters
    ----------
    n : int
        Number of minutes

    Returns
    -------
    Expr
        A duration literal.

    Examples
    --------
    >>> df.mutate(later = col('datetime') + tp.minutes(30))
    """
    return pl.duration(minutes=n)

def seconds(n = 1):
    """
    Create a duration of n seconds

    Parameters
    ----------
    n : int
        Number of seconds

    Returns
    -------
    Expr
        A duration literal.

    Examples
    --------
    >>> df.mutate(later = col('datetime') + tp.seconds(10))
    """
    return pl.duration(seconds=n)

def milliseconds(n = 1):
    """
    Create a duration of n milliseconds

    Parameters
    ----------
    n : int
        Number of milliseconds

    Returns
    -------
    Expr
        A duration literal.
    """
    return pl.duration(milliseconds=n)

def microseconds(n = 1):
    """
    Create a duration of n microseconds

    Parameters
    ----------
    n : int
        Number of microseconds

    Returns
    -------
    Expr
        A duration literal.
    """
    return pl.duration(microseconds=n)
