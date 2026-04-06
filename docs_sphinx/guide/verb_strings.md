# String Operations

tidypolars-extra provides `stringr`-style functions for string manipulation.
These work inside `mutate()` and `filter()` expressions.

## Setup

```python
import tidypolars_extra as tp
from tidypolars_extra import col
from tidypolars_extra import (
    str_detect, str_replace, str_replace_all,
    str_extract, str_remove, str_remove_all,
    str_to_upper, str_to_lower, str_trim,
    str_sub, str_length, str_starts, str_ends,
    paste, paste0, str_c
)

df = tp.tibble(
    name=["Alice Smith", "Bob Jones", "Carol Lee"],
    email=["alice@eng.com", "bob@sales.com", "carol@eng.com"]
)
```

## Detecting Patterns

```python
# Filter rows where name contains "o"
df.filter(str_detect("name", "o"))

# Check if email starts with a pattern
df.mutate(is_eng=str_ends("email", "eng.com"))
```

## Replacing Text

```python
# Replace first occurrence
df.mutate(name=str_replace("name", "Smith", "Johnson"))

# Replace all occurrences
df.mutate(email=str_replace_all("email", r"\.com", ".org"))
```

## Extracting Substrings

```python
# Extract first word
df.mutate(first_name=str_extract("name", r"^\w+"))

# Substring by position
df.mutate(initial=str_sub("name", 0, 1))
```

## Removing Patterns

```python
# Remove first match
df.mutate(name=str_remove("name", r"\s\w+$"))

# Remove all matches
df.mutate(email=str_remove_all("email", r"[aeiou]"))
```

## Changing Case

```python
df.mutate(
    upper=str_to_upper("name"),
    lower=str_to_lower("name")
)
```

## Trimming Whitespace

```python
messy = tp.tibble(text=["  hello  ", " world ", "  foo"])
messy.mutate(clean=str_trim("text"))
```

## Concatenating Strings

```python
df = tp.tibble(
    first=["Alice", "Bob"],
    last=["Smith", "Jones"]
)

# With separator
df.mutate(full=paste("first", "last", sep=" "))

# Without separator
df.mutate(code=paste0("first", "last"))
```

## String Length

```python
df.mutate(name_len=str_length("name"))
```

## Available Functions

| Function | Description |
|----------|-------------|
| `str_detect(col, pattern)` | Test if pattern matches |
| `str_extract(col, pattern)` | Extract first match |
| `str_replace(col, pattern, replacement)` | Replace first match |
| `str_replace_all(col, pattern, replacement)` | Replace all matches |
| `str_remove(col, pattern)` | Remove first match |
| `str_remove_all(col, pattern)` | Remove all matches |
| `str_to_upper(col)` | Convert to uppercase |
| `str_to_lower(col)` | Convert to lowercase |
| `str_trim(col)` | Trim whitespace |
| `str_sub(col, start, end)` | Extract substring |
| `str_length(col)` | String length |
| `str_starts(col, pattern)` | Test if starts with |
| `str_ends(col, pattern)` | Test if ends with |
| `str_c(*cols, sep)` | Concatenate strings |
| `paste(*cols, sep)` | Concatenate with separator |
| `paste0(*cols)` | Concatenate without separator |
