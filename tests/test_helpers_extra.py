import tidypolars_extra as tp
from tidypolars_extra import col
import polars as pl


def test_matches():
    """Can select columns matching a regex pattern"""
    df = tp.tibble(val_x=range(3), val_y=range(3), z_other=range(3))
    actual = df.select(tp.matches('val'))
    expected = tp.tibble(val_x=range(3), val_y=range(3))
    assert actual.equals(expected), "matches failed"


def test_matches_ignore_case():
    """Can match with case insensitivity"""
    df = tp.tibble(Name=range(3), AGE=range(3))
    actual = df.select(tp.matches('name', ignore_case=True))
    expected = tp.tibble(Name=range(3))
    assert actual.equals(expected), "matches ignore_case failed"


def test_desc():
    """Can use desc for descending arrange"""
    df = tp.tibble(x=['a', 'b', 'c'], y=[1, 2, 3])
    actual = df.arrange(tp.desc('y'))
    expected = tp.tibble(x=['c', 'b', 'a'], y=[3, 2, 1])
    assert actual.equals(expected), "desc failed"


def test_across_with_prefix():
    """Can use across with names_prefix"""
    df = tp.tibble(x=[1, 2, 3], y=[4, 5, 6])
    actual = df.mutate(tp.across(['x', 'y'], lambda c: c * 2, names_prefix='double_'))
    assert 'double_x' in actual.names, "across names_prefix failed"
    assert 'double_y' in actual.names, "across names_prefix failed"
    assert actual.pull('double_x').to_list() == [2, 4, 6], "across values failed"


def test_across_with_suffix():
    """Can use across with names_suffix"""
    df = tp.tibble(x=[1, 2, 3], y=[4, 5, 6])
    actual = df.mutate(tp.across(['x', 'y'], lambda c: c * 2, names_suffix='_doubled'))
    assert 'x_doubled' in actual.names, "across names_suffix failed"
    assert 'y_doubled' in actual.names, "across names_suffix failed"


def test_lag_function():
    """Can use lag function from helpers"""
    df = tp.tibble(x=[1, 2, 3])
    actual = df.mutate(lag_x=tp.lag('x'))
    expected = tp.tibble(x=[1, 2, 3], lag_x=[None, 1, 2])
    assert actual.equals(expected, null_equal=True), "lag function failed"


def test_lag_with_default():
    """Can use lag function with default value"""
    df = tp.tibble(x=[1, 2, 3])
    actual = df.mutate(lag_x=tp.lag('x', default=0))
    expected = tp.tibble(x=[1, 2, 3], lag_x=[0, 1, 2])
    assert actual.equals(expected), "lag with default failed"


def test_where_numeric():
    """Can select numeric columns with where"""
    df = tp.tibble(x=[1, 2, 3], y=['a', 'b', 'c'], z=[1.0, 2.0, 3.0])
    actual = df.select(tp.where('numeric'))
    assert actual.names == ['x', 'z'], "where numeric failed"


def test_where_string():
    """Can select string columns with where"""
    df = tp.tibble(x=[1, 2, 3], y=['a', 'b', 'c'])
    actual = df.select(tp.where('string'))
    assert actual.names == ['y'], "where string failed"


def test_where_integer():
    """Can select integer columns with where"""
    df = tp.tibble(x=[1, 2, 3], y=[1.0, 2.0, 3.0], z=['a', 'b', 'c'])
    actual = df.select(tp.where('integer'))
    assert actual.names == ['x'], "where integer failed"


def test_where_float():
    """Can select float columns with where"""
    df = tp.tibble(x=[1, 2, 3], y=[1.0, 2.0, 3.0])
    actual = df.select(tp.where('float'))
    assert actual.names == ['y'], "where float failed"
