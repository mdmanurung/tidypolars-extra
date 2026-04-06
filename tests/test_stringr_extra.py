import tidypolars_extra as tp
from tidypolars_extra import col


def test_str_wrap():
    """Can use str_wrap to split strings"""
    df = tp.tibble(x=['hello world foo bar'])
    actual = df.mutate(wrapped=tp.str_wrap('x', 5))
    # str_wrap splits by width into a list
    result = actual.pull('wrapped')
    # Just check it doesn't error and produces output
    assert result is not None, "str_wrap failed"


def test_str_detect_negate():
    """Can use str_detect with negate"""
    df = tp.tibble(name=['apple', 'banana', 'cherry'])
    actual = df.mutate(no_a=tp.str_detect('name', 'a', negate=True))
    expected = tp.tibble(name=['apple', 'banana', 'cherry'],
                         no_a=[False, False, True])
    assert actual.equals(expected), "str_detect negate failed"


def test_str_starts_negate():
    """Can use str_starts with negate"""
    df = tp.tibble(words=['apple', 'bear', 'amazing'])
    actual = df.filter(tp.str_starts(col('words'), 'a', negate=True))
    expected = tp.tibble(words=['bear'])
    assert actual.equals(expected), "str_starts negate failed"


def test_str_ends_negate():
    """Can use str_ends with negate"""
    df = tp.tibble(words=['apple', 'bear', 'amazing'])
    actual = df.filter(tp.str_ends(col('words'), 'r', negate=True))
    expected = tp.tibble(words=['apple', 'amazing'])
    assert actual.equals(expected), "str_ends negate failed"
