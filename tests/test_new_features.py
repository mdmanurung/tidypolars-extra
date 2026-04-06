import tidypolars_extra as tp
from tidypolars_extra import col, lit
import polars as pl
import pytest
from datetime import date, datetime


# ============================================================
# Tibble: Joins
# ============================================================

class TestSemiJoin:
    def test_basic(self):
        df1 = tp.tibble(x=[1, 2, 3], y=['a', 'b', 'c'])
        df2 = tp.tibble(x=[1, 3], z=[10, 30])
        result = df1.semi_join(df2, on='x')
        expected = tp.tibble(x=[1, 3], y=['a', 'c'])
        assert result.equals(expected)

    def test_auto_detect_on(self):
        df1 = tp.tibble(x=[1, 2, 3], y=['a', 'b', 'c'])
        df2 = tp.tibble(x=[2], w=[99])
        result = df1.semi_join(df2)
        assert result.nrow == 1
        assert result.pull('x').to_list() == [2]

    def test_no_match(self):
        df1 = tp.tibble(x=[1, 2, 3])
        df2 = tp.tibble(x=[4, 5])
        result = df1.semi_join(df2, on='x')
        assert result.nrow == 0


class TestAntiJoin:
    def test_basic(self):
        df1 = tp.tibble(x=[1, 2, 3], y=['a', 'b', 'c'])
        df2 = tp.tibble(x=[1, 3], z=[10, 30])
        result = df1.anti_join(df2, on='x')
        expected = tp.tibble(x=[2], y=['b'])
        assert result.equals(expected)

    def test_auto_detect_on(self):
        df1 = tp.tibble(x=[1, 2, 3])
        df2 = tp.tibble(x=[1, 2, 3])
        result = df1.anti_join(df2)
        assert result.nrow == 0


class TestCrossJoin:
    def test_basic(self):
        df1 = tp.tibble(x=[1, 2])
        df2 = tp.tibble(y=['a', 'b'])
        result = df1.cross_join(df2)
        assert result.nrow == 4
        assert result.ncol == 2
        assert 'x' in result.names
        assert 'y' in result.names


# ============================================================
# Tibble: Pipe & Transmute
# ============================================================

class TestPipe:
    def test_basic(self):
        df = tp.tibble(x=[1, 2, 3])
        result = df.pipe(lambda d: d.filter(col('x') > 1))
        assert result.nrow == 2

    def test_with_args(self):
        def add_col(df, name, value):
            return df.mutate(**{name: lit(value)})
        df = tp.tibble(x=[1, 2])
        result = df.pipe(add_col, 'y', 10)
        assert 'y' in result.names


class TestTransmute:
    def test_basic(self):
        df = tp.tibble(a=[1, 2, 3], b=[4, 5, 6])
        result = df.transmute(c=col('a') + col('b'))
        assert result.names == ['c']
        assert result.pull('c').to_list() == [5, 7, 9]

    def test_with_by(self):
        df = tp.tibble(g=['a', 'a', 'b'], x=[1, 2, 3])
        result = df.transmute(total=col('x').sum(), by='g')
        assert 'g' in result.names
        assert 'total' in result.names
        assert 'x' not in result.names


# ============================================================
# Tibble: Clean Names
# ============================================================

class TestCleanNames:
    def test_snake_case(self):
        df = tp.tibble(**{"First Name": [1], "Last.Name": [2], "AGE": [30]})
        result = df.clean_names()
        assert 'first_name' in result.names
        assert 'last_name' in result.names
        assert 'age' in result.names

    def test_camel_to_snake(self):
        df = tp.tibble(**{"firstName": [1], "lastName": [2]})
        result = df.clean_names()
        assert 'first_name' in result.names
        assert 'last_name' in result.names

    def test_upper(self):
        df = tp.tibble(x=[1], y=[2])
        result = df.clean_names(case='upper')
        assert result.names == ['X', 'Y']

    def test_lower(self):
        df = tp.tibble(**{"X_COL": [1]})
        result = df.clean_names(case='lower')
        assert result.names == ['x_col']


# ============================================================
# Tibble: Sample
# ============================================================

class TestSample:
    def test_sample_n(self):
        df = tp.tibble(x=range(100))
        result = df.sample_n(10, seed=42)
        assert result.nrow == 10

    def test_sample_frac(self):
        df = tp.tibble(x=range(100))
        result = df.sample_frac(0.1, seed=42)
        assert result.nrow == 10

    def test_sample_reproducible(self):
        df = tp.tibble(x=range(100))
        r1 = df.sample_n(5, seed=1)
        r2 = df.sample_n(5, seed=1)
        assert r1.equals(r2)


# ============================================================
# Tibble: Complete
# ============================================================

class TestComplete:
    def test_basic(self):
        df = tp.tibble(x=[1, 1, 2], y=['a', 'b', 'a'], val=[10, 20, 30])
        result = df.complete('x', 'y')
        assert result.nrow == 4  # 2 x values * 2 y values
        # The missing combination (2, 'b') should have null val
        missing_row = result.filter((col('x') == 2) & (col('y') == 'b'))
        assert missing_row.pull('val').to_list() == [None]

    def test_with_fill(self):
        df = tp.tibble(x=[1, 2], y=['a', 'b'], val=[10, 20])
        result = df.complete('x', 'y', fill={'val': 0})
        missing_vals = result.filter(col('val') == 0)
        assert missing_vals.nrow == 2  # two filled rows


# ============================================================
# Tibble: Describe
# ============================================================

class TestDescribe:
    def test_basic(self):
        df = tp.tibble(x=[1, 2, 3], y=['a', 'b', 'c'])
        result = df.describe()
        assert 'column' in result.names
        assert 'dtype' in result.names
        assert 'count' in result.names
        assert 'null_count' in result.names
        assert 'n_unique' in result.names
        assert 'mean' in result.names
        assert result.nrow == 2

    def test_numeric_stats(self):
        df = tp.tibble(x=[1.0, 2.0, 3.0])
        result = df.describe()
        assert result.pull('mean').to_list()[0] == 2.0


# ============================================================
# Tibble: Replace NA
# ============================================================

class TestReplaceNa:
    def test_basic(self):
        df = tp.tibble(x=[1, None, 3], y=['a', None, 'c'])
        result = df.replace_na({'x': 0, 'y': 'missing'})
        assert result.pull('x').to_list() == [1, 0, 3]
        assert result.pull('y').to_list() == ['a', 'missing', 'c']

    def test_no_replace(self):
        df = tp.tibble(x=[1, 2, 3])
        result = df.replace_na(None)
        assert result.equals(df)


# ============================================================
# Tibble: Get Dupes
# ============================================================

class TestGetDupes:
    def test_basic(self):
        df = tp.tibble(x=[1, 1, 2, 2, 3], y=['a', 'a', 'b', 'b', 'c'])
        result = df.get_dupes('x')
        assert result.nrow == 4  # rows with x=1 (2) and x=2 (2)
        assert 'dupe_count' in result.names

    def test_no_dupes(self):
        df = tp.tibble(x=[1, 2, 3])
        result = df.get_dupes('x')
        assert result.nrow == 0


# ============================================================
# Tibble: Assertions
# ============================================================

class TestAssertions:
    def test_assert_no_nulls_pass(self):
        df = tp.tibble(x=[1, 2, 3])
        result = df.assert_no_nulls('x')
        assert result.equals(df)

    def test_assert_no_nulls_fail(self):
        df = tp.tibble(x=[1, None, 3])
        with pytest.raises(AssertionError, match="null values"):
            df.assert_no_nulls('x')

    def test_assert_unique_pass(self):
        df = tp.tibble(x=[1, 2, 3])
        result = df.assert_unique('x')
        assert result.equals(df)

    def test_assert_unique_fail(self):
        df = tp.tibble(x=[1, 1, 2])
        with pytest.raises(AssertionError, match="duplicate"):
            df.assert_unique('x')


# ============================================================
# Tibble: To Markdown
# ============================================================

class TestToMarkdown:
    def test_basic(self):
        df = tp.tibble(x=[1, 2], y=['a', 'b'])
        md = df.to_markdown()
        assert '| x | y |' in md
        assert '| --- | --- |' in md
        assert '| 1 | a |' in md


# ============================================================
# Stats: Cumulative Functions
# ============================================================

class TestCumulativeStats:
    def test_cumsum(self):
        df = tp.tibble(x=[1, 2, 3])
        result = df.mutate(cs=tp.cumsum('x'))
        assert result.pull('cs').to_list() == [1, 3, 6]

    def test_cumprod(self):
        df = tp.tibble(x=[1, 2, 3])
        result = df.mutate(cp=tp.cumprod('x'))
        assert result.pull('cp').to_list() == [1, 2, 6]

    def test_cummax(self):
        df = tp.tibble(x=[1, 3, 2])
        result = df.mutate(cm=tp.cummax('x'))
        assert result.pull('cm').to_list() == [1, 3, 3]

    def test_cummin(self):
        df = tp.tibble(x=[3, 1, 2])
        result = df.mutate(cm=tp.cummin('x'))
        assert result.pull('cm').to_list() == [3, 1, 1]


# ============================================================
# Stats: Ranking Functions
# ============================================================

class TestRankingFunctions:
    def test_percent_rank(self):
        df = tp.tibble(x=[1, 2, 3, 4])
        result = df.mutate(pr=tp.percent_rank('x'))
        vals = result.pull('pr').to_list()
        assert vals[0] == 0.0  # min value
        assert abs(vals[-1] - 1.0) < 1e-10  # max value

    def test_ntile(self):
        df = tp.tibble(x=[1, 2, 3, 4])
        result = df.mutate(q=tp.ntile('x', 2))
        vals = result.pull('q').to_list()
        assert 1 in vals
        assert 2 in vals

    def test_cume_dist(self):
        df = tp.tibble(x=[1, 2, 3, 4])
        result = df.mutate(cd=tp.cume_dist('x'))
        vals = result.pull('cd').to_list()
        assert vals[-1] == 1.0  # last value is 100%


# ============================================================
# Stats: Extra Functions
# ============================================================

class TestExtraStats:
    def test_weighted_mean(self):
        df = tp.tibble(x=[1.0, 2.0, 3.0], w=[1.0, 2.0, 1.0])
        result = df.summarize(wm=tp.weighted_mean('x', 'w'))
        assert abs(result.pull('wm').item() - 2.0) < 1e-10

    def test_mode(self):
        df = tp.tibble(x=[1, 2, 2, 3, 3, 3])
        result = df.summarize(m=tp.mode('x'))
        assert result.pull('m').item() == 3

    def test_iqr(self):
        df = tp.tibble(x=[1.0, 2.0, 3.0, 4.0, 5.0])
        result = df.summarize(i=tp.iqr('x'))
        assert result.pull('i').item() > 0

    def test_mad(self):
        df = tp.tibble(x=[1.0, 2.0, 3.0, 4.0, 5.0])
        result = df.summarize(m=tp.mad('x'))
        assert result.pull('m').item() == 1.0

    def test_zscore(self):
        df = tp.tibble(x=[1.0, 2.0, 3.0])
        result = df.mutate(z=tp.zscore('x'))
        # Mean of z-scores should be ~0
        mean_z = result.pull('z').mean()
        assert abs(mean_z) < 1e-10


# ============================================================
# Stringr: New Functions
# ============================================================

class TestNewStringr:
    def test_str_count(self):
        df = tp.tibble(x=['aabba', 'bbb', 'a'])
        result = df.mutate(n=tp.str_count('x', 'a'))
        assert result.pull('n').to_list() == [3, 0, 1]

    def test_str_pad_left(self):
        df = tp.tibble(x=['a', 'bb', 'ccc'])
        result = df.mutate(p=tp.str_pad('x', 5))
        assert result.pull('p').to_list() == ['    a', '   bb', '  ccc']

    def test_str_pad_right(self):
        df = tp.tibble(x=['a'])
        result = df.mutate(p=tp.str_pad('x', 4, side='right'))
        assert result.pull('p').to_list() == ['a   ']

    def test_str_split(self):
        df = tp.tibble(x=['a-b-c', 'd-e'])
        result = df.mutate(parts=tp.str_split('x', '-'))
        vals = result.pull('parts').to_list()
        assert vals[0] == ['a', 'b', 'c']
        assert vals[1] == ['d', 'e']

    def test_str_squish(self):
        df = tp.tibble(x=['  hello   world  ', 'a  b'])
        result = df.mutate(s=tp.str_squish('x'))
        assert result.pull('s').to_list() == ['hello world', 'a b']

    def test_str_to_title(self):
        df = tp.tibble(x=['hello world', 'foo bar'])
        result = df.mutate(t=tp.str_to_title('x'))
        assert result.pull('t').to_list() == ['Hello World', 'Foo Bar']

    def test_str_dup(self):
        df = tp.tibble(x=['ab', 'cd'])
        result = df.mutate(d=tp.str_dup('x', 3))
        assert result.pull('d').to_list() == ['ababab', 'cdcdcd']

    def test_str_extract_all(self):
        df = tp.tibble(x=['abc123def456', 'no_digits'])
        result = df.mutate(nums=tp.str_extract_all('x', r'\d+'))
        vals = result.pull('nums').to_list()
        assert vals[0] == ['123', '456']
        assert vals[1] == []


# ============================================================
# Forcats
# ============================================================

class TestForcats:
    def test_fct_recode(self):
        df = tp.tibble(x=['a', 'b', 'c', 'a'])
        result = df.mutate(x2=tp.fct_recode('x', good='a', bad='b'))
        assert result.pull('x2').to_list() == ['good', 'bad', 'c', 'good']

    def test_fct_collapse(self):
        df = tp.tibble(x=['a', 'b', 'c', 'd'])
        result = df.mutate(x2=tp.fct_collapse('x', ab=['a', 'b'], cd=['c', 'd']))
        assert result.pull('x2').to_list() == ['ab', 'ab', 'cd', 'cd']

    def test_fct_rev(self):
        df = tp.tibble(x=['a', 'b', 'c'])
        result = df.mutate(x2=tp.fct_rev('x'))
        assert result.pull('x2').to_list() == ['a', 'b', 'c']  # values same, type changes

    def test_fct_infreq(self):
        df = tp.tibble(x=['a', 'b', 'a', 'a', 'b', 'c'])
        result = df.mutate(x2=tp.fct_infreq('x'))
        assert result.nrow == 6


# ============================================================
# Lubridate: New Functions
# ============================================================

class TestNewLubridate:
    def test_today(self):
        df = tp.tibble(x=[1])
        result = df.mutate(d=tp.today())
        assert result.pull('d').dtype == pl.Date

    def test_now(self):
        df = tp.tibble(x=[1])
        result = df.mutate(d=tp.now())
        assert result.pull('d').dtype == pl.Datetime

    def test_difftime(self):
        df = tp.tibble(
            d1=[date(2024, 1, 10)],
            d2=[date(2024, 1, 1)]
        )
        result = df.mutate(diff=tp.difftime('d1', 'd2', units='days'))
        assert result.pull('diff').to_list()[0] == 9.0

    def test_floor_date(self):
        df = tp.tibble(d=[date(2024, 3, 15)])
        result = df.mutate(fd=tp.floor_date('d', 'month'))
        assert result.pull('fd').to_list()[0] == date(2024, 3, 1)

    def test_days(self):
        df = tp.tibble(d=[date(2024, 1, 1)])
        result = df.mutate(d2=col('d') + tp.days(5))
        assert result.pull('d2').to_list()[0] == date(2024, 1, 6)

    def test_weeks(self):
        df = tp.tibble(d=[date(2024, 1, 1)])
        result = df.mutate(d2=col('d') + tp.weeks(1))
        assert result.pull('d2').to_list()[0] == date(2024, 1, 8)


# ============================================================
# Funs: n_missing, pct_missing
# ============================================================

class TestMissingFuns:
    def test_n_missing(self):
        df = tp.tibble(x=[1, None, None, 4])
        result = df.summarize(m=tp.n_missing('x'))
        assert result.pull('m').item() == 2

    def test_pct_missing(self):
        df = tp.tibble(x=[1, None, None, 4])
        result = df.summarize(p=tp.pct_missing('x'))
        assert result.pull('p').item() == 50.0

    def test_n_missing_zero(self):
        df = tp.tibble(x=[1, 2, 3])
        result = df.summarize(m=tp.n_missing('x'))
        assert result.pull('m').item() == 0
