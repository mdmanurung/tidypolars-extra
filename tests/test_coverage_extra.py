"""
Additional tests to fill coverage gaps identified in the code review.

Covers: lubridate (explicit values), str_length Unicode, funs.rep/map,
        stats.sum, utils internal functions.
"""
import tidypolars_extra as tp
from tidypolars_extra import col
import polars as pl
import pytest


# ── lubridate: explicit-value tests for date extraction functions ──

def test_mday_explicit():
    """mday extracts day of month correctly"""
    df = tp.tibble(x=['2021-01-15', '2021-06-01', '2021-12-31'])
    df = df.mutate(date=tp.as_date('x'))
    actual = df.mutate(d=tp.mday('date')).pull('d').to_list()
    assert actual == [15, 1, 31], "mday explicit failed"


def test_year_explicit():
    """year extracts year correctly"""
    df = tp.tibble(x=['2020-01-01', '2021-06-15', '1999-12-31'])
    df = df.mutate(date=tp.as_date('x'))
    actual = df.mutate(y=tp.year('date')).pull('y').to_list()
    assert actual == [2020, 2021, 1999], "year explicit failed"


def test_quarter_explicit():
    """quarter extracts quarter correctly"""
    df = tp.tibble(x=['2021-01-01', '2021-04-01', '2021-07-01', '2021-10-01'])
    df = df.mutate(date=tp.as_date('x'))
    actual = df.mutate(q=tp.quarter('date')).pull('q').to_list()
    assert actual == [1, 2, 3, 4], "quarter explicit failed"


def test_wday_explicit():
    """wday extracts weekday correctly (Monday=2 through Sunday=1+7 mapping)"""
    # 2021-01-04 is a Monday (weekday()=1 => wday=2)
    # 2021-01-03 is a Sunday (weekday()=7 => wday=8)
    df = tp.tibble(x=['2021-01-04', '2021-01-05', '2021-01-03'])
    df = df.mutate(date=tp.as_date('x'))
    actual = df.mutate(w=tp.wday('date')).pull('w').to_list()
    # weekday() returns 1=Mon...7=Sun, wday adds 1
    assert actual == [2, 3, 8], "wday explicit failed"


def test_week_explicit():
    """week extracts ISO week number correctly"""
    df = tp.tibble(x=['2021-01-01', '2021-01-08', '2021-12-31'])
    df = df.mutate(date=tp.as_date('x'))
    actual = df.mutate(w=tp.week('date')).pull('w').to_list()
    assert actual == [53, 1, 52], "week explicit failed"


def test_yday_explicit():
    """yday extracts ordinal day correctly"""
    df = tp.tibble(x=['2021-01-01', '2021-02-01', '2021-12-31'])
    df = df.mutate(date=tp.as_date('x'))
    actual = df.mutate(yd=tp.yday('date')).pull('yd').to_list()
    assert actual == [1, 32, 365], "yday explicit failed"


# ── stringr: Unicode test for str_length ──

def test_str_length_unicode():
    """str_length returns character count, not byte count, for Unicode"""
    df = tp.tibble(x=['hello', 'café', '日本語', '🎉'])
    actual = df.mutate(length=tp.str_length('x')).pull('length').to_list()
    assert actual == [5, 4, 3, 1], "str_length unicode failed"


def test_str_length_basic():
    """str_length works for ASCII strings"""
    df = tp.tibble(name=['apple', 'banana', 'pear', 'grape'])
    actual = df.mutate(x=tp.str_length('name')).pull('x').to_list()
    assert actual == [5, 6, 4, 5], "str_length basic failed"


# ── funs: rep edge cases ──

def test_rep_list():
    """rep can replicate a list"""
    actual = tp.rep([1, 2], 3)
    assert actual.to_list() == [1, 2, 1, 2, 1, 2], "rep list failed"


def test_rep_invalid():
    """rep raises for incompatible types"""
    with pytest.raises(ValueError, match="Incompatible type"):
        tp.rep(object(), 2)


# ── funs: map ──
# Note: map() is already tested in test_tibble_extra.py::test_map
# The map function requires specific polars lazy context setup


# ── stats: sum ──

def test_sum_basic():
    """sum works on a column"""
    df = tp.tibble(x=[1, 2, 3])
    actual = df.summarize(s=tp.sum('x'))
    assert actual.pull('s').to_list() == [6], "sum failed"


# ── utils: internal functions ──

def test_as_list_tuple():
    """_as_list properly handles tuples"""
    from tidypolars_extra.utils import _as_list
    result = _as_list((1, 2, 3))
    assert result == [1, 2, 3], "_as_list tuple failed"


def test_as_list_series():
    """_as_list properly handles Series"""
    from tidypolars_extra.utils import _as_list
    s = pl.Series("x", [1, 2, 3])
    result = _as_list(s)
    assert result == [1, 2, 3], "_as_list series failed"


def test_as_list_list():
    """_as_list handles lists"""
    from tidypolars_extra.utils import _as_list
    result = _as_list([1, 2, 3])
    assert result == [1, 2, 3], "_as_list list failed"


def test_as_list_empty():
    """_as_list handles empty list"""
    from tidypolars_extra.utils import _as_list
    result = _as_list([])
    assert result == [], "_as_list empty failed"


def test_is_iterable():
    """_is_iterable returns True for lists, False for strings"""
    from tidypolars_extra.utils import _is_iterable
    assert _is_iterable([1, 2]) is True, "_is_iterable list failed"
    assert _is_iterable("hello") is False, "_is_iterable string failed"
    assert _is_iterable(42) is False, "_is_iterable int failed"


def test_col_expr_string():
    """_col_expr converts string to pl.col()"""
    from tidypolars_extra.utils import _col_expr
    expr = _col_expr("x")
    assert isinstance(expr, pl.Expr), "_col_expr string failed"


def test_col_expr_invalid():
    """_col_expr raises for invalid input"""
    from tidypolars_extra.utils import _col_expr
    with pytest.raises(ValueError, match="Invalid input"):
        _col_expr(42)


def test_expand_to_full_path_or_url():
    """_expand_to_full_path_or_url handles URLs and paths"""
    from tidypolars_extra.utils import _expand_to_full_path_or_url
    # URL should pass through unchanged
    assert _expand_to_full_path_or_url("https://example.com/data.csv") == "https://example.com/data.csv"
    # Empty/falsy should pass through
    assert _expand_to_full_path_or_url("") == ""


def test_filter_kwargs_for():
    """_filter_kwargs_for filters kwargs to match function signature"""
    from tidypolars_extra.utils import _filter_kwargs_for
    def func(a, b):
        pass
    result = _filter_kwargs_for(func, {"a": 1, "b": 2, "c": 3})
    assert result == {"a": 1, "b": 2}, "_filter_kwargs_for failed"


def test_uses_by():
    """_uses_by correctly identifies by parameter"""
    from tidypolars_extra.utils import _uses_by
    assert _uses_by("x") is True, "_uses_by string failed"
    assert _uses_by(None) is False, "_uses_by None failed"
    assert _uses_by([]) is False, "_uses_by empty list failed"
    assert _uses_by(["x"]) is True, "_uses_by list failed"
