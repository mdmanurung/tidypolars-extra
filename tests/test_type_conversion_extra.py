import tidypolars_extra as tp
from tidypolars_extra import col
import polars as pl


def test_as_categorical():
    """Can convert to categorical (unordered factor)"""
    df = tp.tibble(x=['a', 'b', 'c'])
    actual = df.mutate(cat_x=tp.as_categorical('x'))
    assert actual.pull('cat_x').dtype == pl.Categorical, "as_categorical failed"


def test_as_factor_no_levels():
    """Can convert to factor without levels (Categorical)"""
    df = tp.tibble(x=['a', 'b', 'c'])
    actual = df.mutate(fac_x=tp.as_factor('x'))
    assert actual.pull('fac_x').dtype == pl.Categorical, "as_factor without levels failed"


def test_as_factor_with_levels():
    """Can convert to factor with levels (Enum)"""
    df = tp.tibble(x=['a', 'b', 'c'])
    actual = df.mutate(fac_x=tp.as_factor('x', levels=['a', 'b', 'c']))
    assert isinstance(actual.pull('fac_x').dtype, pl.Enum), "as_factor with levels failed"


def test_as_logical():
    """Can convert to boolean/logical"""
    df = tp.tibble(x=[0, 1, 1])
    actual = df.mutate(bool_x=tp.as_logical('x'))
    expected = tp.tibble(x=[0, 1, 1], bool_x=[False, True, True])
    assert actual.equals(expected), "as_logical failed"


def test_as_character():
    """Can convert to character (string)"""
    df = tp.tibble(x=[1, 2, 3])
    actual = df.mutate(str_x=tp.as_character('x'))
    expected = tp.tibble(x=[1, 2, 3], str_x=['1', '2', '3'])
    assert actual.equals(expected), "as_character failed"


def test_cast():
    """Can cast to arbitrary type"""
    df = tp.tibble(x=[1, 2, 3])
    actual = df.mutate(float_x=tp.cast('x', pl.Float32))
    assert actual.pull('float_x').dtype == pl.Float32, "cast failed"
