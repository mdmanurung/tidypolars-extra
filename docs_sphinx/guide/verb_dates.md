# Date & Time Operations

tidypolars-extra provides `lubridate`-style functions for working with dates
and times.

## Setup

```python
import tidypolars_extra as tp
from tidypolars_extra import col
from tidypolars_extra import (
    as_date, as_datetime, make_date, make_datetime,
    year, month, mday, hour, minute, second,
    wday, week, yday, quarter, dt_round
)
```

## Creating Dates

```python
# From string
df = tp.tibble(date_str=["2024-01-15", "2024-06-20", "2024-12-25"])
df.mutate(date=as_date("date_str"))

# From components
df = tp.tibble(y=[2024, 2024], m=[1, 6], d=[15, 20])
df.mutate(date=make_date("y", "m", "d"))
```

## Creating Datetimes

```python
# From string
df = tp.tibble(dt_str=["2024-01-15 10:30:00", "2024-06-20 14:45:00"])
df.mutate(dt=as_datetime("dt_str"))

# From components
df = tp.tibble(
    y=[2024], m=[1], d=[15],
    h=[10], mi=[30], s=[0]
)
df.mutate(dt=make_datetime("y", "m", "d", "h", "mi", "s"))
```

## Extracting Components

```python
df = tp.tibble(
    date=["2024-01-15", "2024-06-20", "2024-12-25"]
)
df = df.mutate(date=as_date("date"))

df.mutate(
    y=year("date"),
    m=month("date"),
    d=mday("date"),
    day_of_week=wday("date"),
    day_of_year=yday("date"),
    wk=week("date"),
    q=quarter("date")
)
```

## Datetime Components

```python
df = tp.tibble(
    timestamp=["2024-01-15 10:30:45"]
)
df = df.mutate(timestamp=as_datetime("timestamp"))

df.mutate(
    h=hour("timestamp"),
    m=minute("timestamp"),
    s=second("timestamp")
)
```

## Rounding Dates

```python
# Round to nearest month
df.mutate(month_start=dt_round("date", every="1mo"))
```

## Available Functions

| Function | Description |
|----------|-------------|
| `as_date(col)` | Convert string to date |
| `as_datetime(col)` | Convert string to datetime |
| `make_date(year, month, day)` | Create date from components |
| `make_datetime(y, m, d, h, mi, s)` | Create datetime from components |
| `year(col)` | Extract year |
| `month(col)` | Extract month |
| `mday(col)` | Extract day of month |
| `hour(col)` | Extract hour |
| `minute(col)` | Extract minute |
| `second(col)` | Extract second |
| `wday(col)` | Extract day of week |
| `week(col)` | Extract week number |
| `yday(col)` | Extract day of year |
| `quarter(col)` | Extract quarter |
| `dt_round(col, every)` | Round date/time |
