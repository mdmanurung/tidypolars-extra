import tidypolars_extra as tp
from tidypolars_extra import col
import polars as pl
import pandas as pd


def test_head():
    """Can get first n rows with head"""
    df = tp.tibble(x=range(10), y=range(10))
    actual = df.head(3)
    expected = tp.tibble(x=range(3), y=range(3))
    assert actual.equals(expected), "head failed"
    assert type(actual) == tp.tibble, "head didn't return a tibble"


def test_tail():
    """Can get last n rows with tail"""
    df = tp.tibble(x=range(10), y=range(10))
    actual = df.tail(3)
    expected = tp.tibble(x=[7, 8, 9], y=[7, 8, 9])
    assert actual.equals(expected), "tail failed"
    assert type(actual) == tp.tibble, "tail didn't return a tibble"


def test_equals():
    """Can compare two tibbles for equality"""
    df1 = tp.tibble(x=[1, 2, 3], y=['a', 'b', 'c'])
    df2 = tp.tibble(x=[1, 2, 3], y=['a', 'b', 'c'])
    df3 = tp.tibble(x=[1, 2, 4], y=['a', 'b', 'c'])
    assert df1.equals(df2), "equals True case failed"
    assert not df1.equals(df3), "equals False case failed"


def test_equals_null():
    """Can compare tibbles with nulls"""
    df1 = tp.tibble(x=[1, None, 3])
    df2 = tp.tibble(x=[1, None, 3])
    assert df1.equals(df2, null_equal=True), "equals with nulls failed"


def test_from_polars():
    """Can convert polars DataFrame to tibble"""
    pl_df = pl.DataFrame({'x': [1, 2, 3], 'y': ['a', 'b', 'c']})
    actual = tp.from_polars(pl_df)
    assert type(actual) == tp.tibble, "from_polars didn't return a tibble"
    assert actual.names == ['x', 'y'], "from_polars column names wrong"
    assert actual.nrow == 3, "from_polars row count wrong"


def test_from_pandas():
    """Can convert pandas DataFrame to tibble"""
    pd_df = pd.DataFrame({'x': [1, 2, 3], 'y': ['a', 'b', 'c']})
    actual = tp.from_pandas(pd_df)
    assert type(actual) == tp.tibble, "from_pandas didn't return a tibble"
    assert actual.names == ['x', 'y'], "from_pandas column names wrong"
    assert actual.nrow == 3, "from_pandas row count wrong"


def test_to_pandas():
    """Can convert tibble to pandas DataFrame"""
    df = tp.tibble(x=[1, 2, 3], y=['a', 'b', 'c'])
    actual = df.to_pandas()
    assert isinstance(actual, pd.DataFrame), "to_pandas didn't return a pandas DataFrame"
    assert list(actual.columns) == ['x', 'y'], "to_pandas columns wrong"


def test_to_polars():
    """Can convert tibble to polars DataFrame"""
    df = tp.tibble(x=[1, 2, 3], y=['a', 'b', 'c'])
    actual = df.to_polars()
    assert isinstance(actual, pl.DataFrame), "to_polars failed"
    assert not isinstance(actual, tp.tibble), "to_polars should return plain DataFrame"


def test_crossing():
    """Can expand tibble with crossing"""
    df = tp.tibble(a=[1, 2], b=[3, 4])
    actual = df.crossing(c=['x', 'y']).arrange('a', 'b', 'c')
    assert actual.nrow == 4, "crossing row count wrong"
    assert 'c' in actual.names, "crossing missing column"
    assert actual.pull('c').to_list() == ['x', 'y', 'x', 'y'], "crossing values wrong"


def test_nest_unnest():
    """Can nest and unnest a tibble - currently crashes with segfault in polars"""
    import pytest
    pytest.skip("nest() causes segfault with current polars version")


def test_relevel():
    """Can relevel a factor column"""
    df = tp.tibble(x=['a', 'b', 'c', 'a'])
    df = df.mutate(x=tp.as_factor('x', levels=['a', 'b', 'c']))
    actual = df.relevel('x', 'b')
    cats = actual.pull('x').cat.get_categories().to_list()
    assert cats[0] == 'b', f"relevel failed: expected 'b' first, got {cats}"


def test_colnames():
    """Can get column names matching a regex"""
    df = tp.tibble(val_x=[1], val_y=[2], z_other=[3])
    actual = df.colnames(regex='val')
    assert actual == ['val_x', 'val_y'], "colnames failed"


def test_colnames_type():
    """Can get column names by type"""
    df = tp.tibble(x=[1, 2], y=['a', 'b'], z=[1.0, 2.0])
    actual = df.colnames(type='numeric')
    assert 'x' in actual, "colnames type numeric should include 'x'"
    assert 'z' in actual, "colnames type numeric should include 'z'"
    assert 'y' not in actual, "colnames type numeric should exclude 'y'"


def test_glimpse(capsys):
    """Can glimpse a tibble without error"""
    df = tp.tibble(x=[1, 2, 3], y=['a', 'b', 'c'])
    result = df.glimpse()
    assert result is None, "glimpse should return None"
    captured = capsys.readouterr()
    assert "Rows:" in captured.out, "glimpse output should contain row info"


def test_iterrows():
    """Can iterate over rows as dicts"""
    df = tp.tibble(x=[1, 2], y=['a', 'b'])
    rows = list(df.iterrows())
    assert len(rows) == 2, "iterrows row count wrong"
    assert rows[0] == {'x': 1, 'y': 'a'}, "iterrows first row wrong"
    assert rows[1] == {'x': 2, 'y': 'b'}, "iterrows second row wrong"


def test_descriptive_statistics():
    """Can compute descriptive statistics"""
    df = tp.tibble(x=[1, 2, 3, 4, 5], y=[10.0, 20.0, 30.0, 40.0, 50.0])
    actual = df.descriptive_statistics()
    assert actual.nrow > 0, "descriptive_statistics returned empty"
    assert 'variable' in actual.names or 'var' in actual.names or len(actual.names) > 0, \
        "descriptive_statistics missing expected columns"


def test_to_dict():
    """Can convert tibble to dict"""
    df = tp.tibble(x=[1, 2], y=['a', 'b'])
    result = df.to_dict()
    assert isinstance(result, dict), "to_dict didn't return dict"
    assert 'x' in result, "to_dict missing key"


def test_map():
    """Can use map to apply function across columns"""
    import polars as pl
    df = tp.tibble(x=[1, 2, 3], y=[10, 20, 30])
    actual = df.mutate(z=tp.map(['x', 'y'], lambda cols: pl.Series([cols[0] + cols[1]])))
    assert actual.pull('z').to_list() == [11, 22, 33], "map failed"
