import tidypolars_extra as tp
from tidypolars_extra import col


def test_rank_dense():
    """Can rank with dense method"""
    df = tp.tibble(x=[10, 20, 20, 30])
    actual = df.mutate(rank_x=tp.rank('x'))
    expected = tp.tibble(x=[10, 20, 20, 30], rank_x=[1, 2, 2, 3])
    assert actual.equals(expected), "rank dense failed"


def test_rank_ordinal():
    """Can rank with ordinal method"""
    df = tp.tibble(x=[10, 20, 20, 30])
    actual = df.mutate(rank_x=tp.rank('x', method='ordinal'))
    expected = tp.tibble(x=[10, 20, 20, 30], rank_x=[1, 2, 3, 4])
    assert actual.equals(expected), "rank ordinal failed"


def test_rank_min():
    """Can rank with min method"""
    df = tp.tibble(x=[10, 20, 20, 30])
    actual = df.mutate(rank_x=tp.rank('x', method='min'))
    expected = tp.tibble(x=[10, 20, 20, 30], rank_x=[1, 2, 2, 4])
    assert actual.equals(expected), "rank min failed"


def test_scale():
    """Can scale (standardize) a column"""
    df = tp.tibble(x=[10.0, 20.0, 30.0])
    actual = df.mutate(scaled=tp.scale('x'))
    # mean=20, std=10 => [-1, 0, 1]
    expected = df.mutate(scaled=(col('x') - col('x').mean()) / col('x').std())
    assert actual.equals(expected), "scale failed"


def test_length():
    """Can get length of a column"""
    df = tp.tibble(x=[1, 2, None])
    actual = df.summarize(len_x=tp.length('x'))
    # length counts non-null values (uses .count())
    expected = tp.tibble(len_x=[2])
    assert actual.equals(expected), "length failed"


def test_cor_invalid_method():
    """Raises ValueError for invalid correlation method"""
    import pytest
    df = tp.tibble(x=[1, 2, 3], y=[3, 2, 1])
    with pytest.raises(ValueError, match="must be either"):
        df.summarize(c=tp.cor('x', 'y', method='invalid'))
