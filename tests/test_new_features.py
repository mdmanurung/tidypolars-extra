import tidypolars4sci as tp
from tidypolars4sci import col
import polars as pl


# ===== Join Tests =====

def test_right_join():
    """Can perform right join"""
    df1 = tp.tibble({'x': [1, 2], 'y': ['a', 'b']})
    df2 = tp.tibble({'x': [2, 3], 'z': ['c', 'd']})
    actual = df1.right_join(df2, on='x')
    assert actual.nrow == 2
    assert 3 in actual.pull('x').to_list()
    assert type(actual) == tp.tibble

def test_right_join_auto_on():
    """Right join auto-detects common columns"""
    df1 = tp.tibble({'x': [1, 2], 'y': ['a', 'b']})
    df2 = tp.tibble({'x': [2, 3], 'z': ['c', 'd']})
    actual = df1.right_join(df2)
    assert actual.nrow == 2

def test_semi_join():
    """Can perform semi join"""
    df1 = tp.tibble({'x': [1, 2, 3], 'y': ['a', 'b', 'c']})
    df2 = tp.tibble({'x': [1, 3]})
    actual = df1.semi_join(df2, on='x')
    assert actual.nrow == 2
    assert set(actual.pull('x').to_list()) == {1, 3}
    assert 'y' in actual.names
    assert type(actual) == tp.tibble

def test_anti_join():
    """Can perform anti join"""
    df1 = tp.tibble({'x': [1, 2, 3], 'y': ['a', 'b', 'c']})
    df2 = tp.tibble({'x': [1, 3]})
    actual = df1.anti_join(df2, on='x')
    assert actual.nrow == 1
    assert actual.pull('x').to_list() == [2]
    assert type(actual) == tp.tibble

def test_cross_join():
    """Can perform cross join"""
    df1 = tp.tibble({'x': [1, 2]})
    df2 = tp.tibble({'y': ['a', 'b']})
    actual = df1.cross_join(df2)
    assert actual.nrow == 4
    assert actual.ncol == 2
    assert type(actual) == tp.tibble


# ===== Slice Variant Tests =====

def test_slice_min():
    """Can slice minimum rows"""
    df = tp.tibble({'x': [3, 1, 2, 4], 'g': ['a', 'a', 'b', 'b']})
    actual = df.slice_min('x', n=2, with_ties=False)
    assert actual.nrow == 2
    assert set(actual.pull('x').to_list()) == {1, 2}
    assert type(actual) == tp.tibble

def test_slice_min_grouped():
    """Can slice minimum rows by group"""
    df = tp.tibble({'x': [3, 1, 4, 2], 'g': ['a', 'a', 'b', 'b']})
    actual = df.slice_min('x', n=1, by='g', with_ties=False)
    assert actual.nrow == 2

def test_slice_max():
    """Can slice maximum rows"""
    df = tp.tibble({'x': [3, 1, 2, 4], 'g': ['a', 'a', 'b', 'b']})
    actual = df.slice_max('x', n=2, with_ties=False)
    assert actual.nrow == 2
    assert set(actual.pull('x').to_list()) == {3, 4}
    assert type(actual) == tp.tibble

def test_slice_sample():
    """Can sample rows"""
    df = tp.tibble({'x': range(100)})
    actual = df.slice_sample(n=10, seed=42)
    assert actual.nrow == 10
    assert type(actual) == tp.tibble

def test_slice_sample_prop():
    """Can sample rows by proportion"""
    df = tp.tibble({'x': range(100)})
    actual = df.slice_sample(prop=0.1, seed=42)
    assert actual.nrow == 10


# ===== Set Operation Tests =====

def test_union():
    """Can union two tibbles"""
    df1 = tp.tibble({'x': [1, 2], 'y': ['a', 'b']})
    df2 = tp.tibble({'x': [2, 3], 'y': ['b', 'c']})
    actual = df1.union(df2)
    assert actual.nrow == 3
    assert type(actual) == tp.tibble

def test_union_all():
    """Can union_all two tibbles (keeps duplicates)"""
    df1 = tp.tibble({'x': [1, 2], 'y': ['a', 'b']})
    df2 = tp.tibble({'x': [2, 3], 'y': ['b', 'c']})
    actual = df1.union_all(df2)
    assert actual.nrow == 4

def test_intersect():
    """Can intersect two tibbles"""
    df1 = tp.tibble({'x': [1, 2, 3], 'y': ['a', 'b', 'c']})
    df2 = tp.tibble({'x': [2, 3, 4], 'y': ['b', 'c', 'd']})
    actual = df1.intersect(df2)
    assert actual.nrow == 2

def test_setdiff():
    """Can setdiff two tibbles"""
    df1 = tp.tibble({'x': [1, 2, 3], 'y': ['a', 'b', 'c']})
    df2 = tp.tibble({'x': [2, 3, 4], 'y': ['b', 'c', 'd']})
    actual = df1.setdiff(df2)
    assert actual.nrow == 1
    assert actual.pull('x').to_list() == [1]


# ===== Additional dplyr Verb Tests =====

def test_transmute():
    """Can transmute"""
    df = tp.tibble({'x': [1, 2, 3], 'y': [4, 5, 6]})
    actual = df.transmute(z=col('x') + col('y'))
    assert actual.names == ['z']
    assert actual.pull('z').to_list() == [5, 7, 9]
    assert type(actual) == tp.tibble

def test_rename_with():
    """Can rename with a function"""
    df = tp.tibble({'x': [1], 'y': [2]})
    actual = df.rename_with(str.upper)
    assert actual.names == ['X', 'Y']
    assert type(actual) == tp.tibble

def test_rename_with_subset():
    """Can rename with a function on subset of columns"""
    df = tp.tibble({'x': [1], 'y': [2], 'z': [3]})
    actual = df.rename_with(str.upper, cols=['x', 'y'])
    assert actual.names == ['X', 'Y', 'z']

def test_add_count():
    """Can add count"""
    df = tp.tibble({'x': ['a', 'a', 'b'], 'y': [1, 2, 3]})
    actual = df.add_count('x')
    assert actual.nrow == 3
    assert actual.ncol == 3
    assert 'n' in actual.names
    assert type(actual) == tp.tibble

def test_tally():
    """Can tally"""
    df = tp.tibble({'x': [1, 2, 3]})
    actual = df.tally()
    assert actual.pull('n').to_list() == [3]

def test_uncount():
    """Can uncount"""
    df = tp.tibble({'x': ['a', 'b'], 'n': [2, 3]})
    actual = df.uncount('n')
    assert actual.nrow == 5
    assert 'n' not in actual.names
    assert actual.pull('x').to_list() == ['a', 'a', 'b', 'b', 'b']
    assert type(actual) == tp.tibble


# ===== tidyr Function Tests =====

def test_complete():
    """Can complete with all combinations"""
    df = tp.tibble({'x': [1, 1, 2], 'y': ['a', 'b', 'a'], 'val': [10, 20, 30]})
    actual = df.complete('x', 'y')
    assert actual.nrow == 4  # 2 x values * 2 y values
    assert type(actual) == tp.tibble

def test_complete_with_fill():
    """Can complete with fill values"""
    df = tp.tibble({'x': [1, 2], 'y': ['a', 'b'], 'val': [10, 20]})
    actual = df.complete('x', 'y', fill={'val': 0})
    assert actual.nrow == 4
    # The filled values should be 0 instead of null
    vals = actual.arrange('x', 'y').pull('val').to_list()
    assert 0 in vals

def test_expand():
    """Can expand to all combinations"""
    df = tp.tibble({'x': [1, 1, 2], 'y': ['a', 'b', 'a']})
    actual = df.expand('x', 'y')
    assert actual.nrow == 4
    assert actual.ncol == 2

def test_separate_rows():
    """Can separate rows"""
    df = tp.tibble({'x': ['a,b', 'c,d'], 'y': [1, 2]})
    actual = df.separate_rows('x', sep=',')
    assert actual.nrow == 4
    assert set(actual.pull('x').to_list()) == {'a', 'b', 'c', 'd'}
    assert type(actual) == tp.tibble

def test_extract():
    """Can extract regex groups"""
    df = tp.tibble({'x': ['a-1', 'b-2', 'c-3']})
    actual = df.extract('x', into=['letter', 'number'], regex=r'(\w)-(\d)')
    assert 'letter' in actual.names
    assert 'number' in actual.names
    assert 'x' not in actual.names
    assert actual.pull('letter').to_list() == ['a', 'b', 'c']
    assert type(actual) == tp.tibble

def test_drop_na_alias():
    """drop_na is alias for drop_null"""
    df = tp.tibble({'x': [1, None, 3], 'y': [4, 5, None]})
    actual = df.drop_na()
    assert actual.nrow == 1

def test_replace_na_alias():
    """replace_na is alias for replace_null"""
    df = tp.tibble({'x': [1, None, 3]})
    actual = df.replace_na({'x': 0})
    assert None not in actual.pull('x').to_list()

def test_ungroup():
    """ungroup returns plain tibble"""
    df = tp.tibble({'x': ['a', 'a', 'b'], 'y': [1, 2, 3]})
    assert type(df.ungroup()) == tp.tibble


# ===== Ranking Function Tests =====

def test_dense_rank():
    """Can compute dense rank"""
    df = tp.tibble({'x': [10, 20, 20, 30]})
    actual = df.mutate(r=tp.dense_rank('x'))
    assert actual.pull('r').to_list() == [1, 2, 2, 3]

def test_min_rank():
    """Can compute min rank"""
    df = tp.tibble({'x': [10, 20, 20, 30]})
    actual = df.mutate(r=tp.min_rank('x'))
    assert actual.pull('r').to_list() == [1, 2, 2, 4]

def test_percent_rank():
    """Can compute percent rank"""
    df = tp.tibble({'x': [10, 20, 30]})
    actual = df.mutate(r=tp.percent_rank('x'))
    vals = actual.pull('r').to_list()
    assert vals[0] == 0.0
    assert vals[2] == 1.0

def test_cume_dist():
    """Can compute cumulative distribution"""
    df = tp.tibble({'x': [10, 20, 30]})
    actual = df.mutate(cd=tp.cume_dist('x'))
    vals = actual.pull('cd').to_list()
    assert abs(vals[0] - 1/3) < 0.01
    assert vals[2] == 1.0

def test_ntile():
    """Can compute ntile"""
    df = tp.tibble({'x': [1, 2, 3, 4]})
    actual = df.mutate(q=tp.ntile('x', 2))
    assert set(actual.pull('q').to_list()) == {1, 2}

def test_nth():
    """Can get nth value"""
    df = tp.tibble({'x': [10, 20, 30]})
    actual = df.summarize(second=tp.nth('x', 1))
    assert actual.pull('second').to_list() == [20]

def test_cumall():
    """Can compute cumulative all"""
    df = tp.tibble({'x': [True, True, False, True]})
    actual = df.mutate(ca=tp.cumall('x'))
    assert actual.pull('ca').to_list() == [True, True, False, False]

def test_cumany():
    """Can compute cumulative any"""
    df = tp.tibble({'x': [False, False, True, False]})
    actual = df.mutate(ca=tp.cumany('x'))
    assert actual.pull('ca').to_list() == [False, False, True, True]

def test_cummean():
    """Can compute cumulative mean"""
    df = tp.tibble({'x': [2, 4, 6]})
    actual = df.mutate(cm=tp.cummean('x'))
    vals = actual.pull('cm').to_list()
    assert vals[0] == 2.0
    assert vals[1] == 3.0
    assert vals[2] == 4.0


# ===== Conditional Function Tests =====

def test_case_match():
    """Can case_match"""
    df = tp.tibble({'x': [1, 2, 3]})
    actual = df.mutate(
        label=tp.case_match(col('x'),
                            1, 'one',
                            2, 'two',
                            _default='other')
    )
    assert actual.pull('label').to_list() == ['one', 'two', 'other']

def test_case_match_list():
    """Can case_match with list values"""
    df = tp.tibble({'x': [1, 2, 3, 4]})
    actual = df.mutate(
        label=tp.case_match(col('x'),
                            [1, 2], 'low',
                            [3, 4], 'high')
    )
    assert actual.pull('label').to_list() == ['low', 'low', 'high', 'high']

def test_na_if():
    """Can na_if"""
    df = tp.tibble({'x': [1, 0, 3, 0]})
    actual = df.mutate(x=tp.na_if(col('x'), 0))
    assert actual.pull('x').null_count() == 2

def test_consecutive_id():
    """Can compute consecutive_id"""
    df = tp.tibble({'x': ['a', 'a', 'b', 'b', 'a']})
    actual = df.mutate(id=tp.consecutive_id('x'))
    assert actual.pull('id').to_list() == [1, 1, 2, 2, 3]


# ===== Helper Tests =====

def test_if_all():
    """Can use if_all"""
    df = tp.tibble({'x': [1, -1, 3], 'y': [2, 3, -1]})
    actual = df.filter(tp.if_all(['x', 'y'], lambda c: c > 0))
    assert actual.nrow == 1

def test_if_any():
    """Can use if_any"""
    df = tp.tibble({'x': [1, -1, -1], 'y': [-1, -1, 1]})
    actual = df.filter(tp.if_any(['x', 'y'], lambda c: c > 0))
    assert actual.nrow == 2


# ===== expand_grid and nesting Tests =====

def test_expand_grid():
    """Can expand_grid"""
    actual = tp.expand_grid(x=[1, 2], y=['a', 'b'])
    assert actual.nrow == 4
    assert actual.ncol == 2
    assert type(actual) == tp.tibble

def test_nesting():
    """Can create nesting"""
    actual = tp.nesting(x=[1, 1, 2], y=['a', 'a', 'b'])
    assert actual.nrow == 2
    assert type(actual) == tp.tibble


# ===== TibbleGroupBy Tests =====

def test_groupby_ungroup():
    """Can ungroup"""
    df = tp.tibble({'x': ['a', 'a', 'b'], 'y': [1, 2, 3]})
    grouped = df.group_by('x')
    ungrouped = grouped.ungroup()
    assert type(ungrouped) == tp.tibble
    assert ungrouped.nrow == 3

def test_groupby_n_groups():
    """Can get number of groups"""
    df = tp.tibble({'x': ['a', 'a', 'b'], 'y': [1, 2, 3]})
    grouped = df.group_by('x')
    assert grouped.n_groups() == 2

def test_groupby_group_keys():
    """Can get group keys"""
    df = tp.tibble({'x': ['a', 'a', 'b'], 'y': [1, 2, 3]})
    grouped = df.group_by('x')
    keys = grouped.group_keys()
    assert keys.nrow == 2
    assert 'x' in keys.names

def test_groupby_group_split():
    """Can split by groups"""
    df = tp.tibble({'x': ['a', 'a', 'b'], 'y': [1, 2, 3]})
    grouped = df.group_by('x')
    parts = grouped.group_split()
    assert len(parts) == 2
    assert all(type(p) == tp.tibble for p in parts)


# ===== Math function Tests =====

def test_log():
    """Can compute log"""
    df = tp.tibble({'x': [1.0, 2.718281828]})
    actual = df.mutate(l=tp.log('x'))
    vals = actual.pull('l').to_list()
    assert abs(vals[0] - 0.0) < 0.01
    assert abs(vals[1] - 1.0) < 0.01

def test_log10():
    """Can compute log10"""
    df = tp.tibble({'x': [1.0, 10.0, 100.0]})
    actual = df.mutate(l=tp.log10('x'))
    vals = actual.pull('l').to_list()
    assert abs(vals[0] - 0.0) < 0.01
    assert abs(vals[1] - 1.0) < 0.01
    assert abs(vals[2] - 2.0) < 0.01

def test_sqrt():
    """Can compute sqrt"""
    df = tp.tibble({'x': [4.0, 9.0, 16.0]})
    actual = df.mutate(s=tp.sqrt('x'))
    vals = actual.pull('s').to_list()
    assert abs(vals[0] - 2.0) < 0.01
    assert abs(vals[1] - 3.0) < 0.01


# ===== Edge Case Tests =====

def test_slice_min_with_ties():
    """slice_min with_ties returns all tied values"""
    df = tp.tibble({'x': [1, 1, 2, 3, 4]})
    actual = df.slice_min('x', n=2)
    assert sorted(actual.pull('x').to_list()) == [1, 1, 2]

def test_slice_max_with_ties():
    """slice_max with_ties returns all tied values"""
    df = tp.tibble({'x': [1, 2, 3, 3, 4]})
    actual = df.slice_max('x', n=2)
    assert sorted(actual.pull('x').to_list()) == [3, 3, 4]

def test_slice_max_grouped_with_ties():
    """slice_max grouped with_ties works correctly"""
    df = tp.tibble({'x': [3, 1, 4, 2], 'g': ['a', 'a', 'b', 'b']})
    actual = df.slice_max('x', n=1, by='g')
    assert sorted(actual.pull('x').to_list()) == [3, 4]

def test_uncount_with_zero():
    """uncount drops rows with weight 0"""
    df = tp.tibble({'x': ['a', 'b', 'c'], 'n': [2, 0, 3]})
    actual = df.uncount('n')
    assert actual.nrow == 5
    assert 'b' not in actual.pull('x').to_list()

def test_case_match_validation():
    """case_match raises error on odd number of args"""
    df = tp.tibble({'x': [1, 2, 3]})
    try:
        df.mutate(label=tp.case_match(col('x'), 1, 'one', 2))
        assert False, "Should have raised ValueError"
    except ValueError:
        pass

def test_case_match_no_args():
    """case_match raises error with no args"""
    df = tp.tibble({'x': [1, 2, 3]})
    try:
        df.mutate(label=tp.case_match(col('x')))
        assert False, "Should have raised ValueError"
    except ValueError:
        pass

def test_nth_with_default():
    """nth returns default for out-of-bounds index"""
    df = tp.tibble({'x': [10, 20, 30]})
    actual = df.summarize(val=tp.nth('x', 10, default=-1))
    assert actual.pull('val').to_list() == [-1]

def test_consecutive_id_multiple_cols():
    """consecutive_id tracks changes across multiple columns"""
    df = tp.tibble({'x': ['a', 'a', 'b', 'b'], 'y': [1, 2, 2, 2]})
    actual = df.mutate(id=tp.consecutive_id('x', 'y'))
    assert actual.pull('id').to_list() == [1, 2, 3, 3]

def test_na_if_string():
    """na_if works with string columns"""
    df = tp.tibble({'x': ['a', 'b', 'c']})
    actual = df.mutate(x=tp.na_if(col('x'), 'b'))
    assert actual.pull('x').null_count() == 1
    assert actual.pull('x').to_list() == ['a', None, 'c']
