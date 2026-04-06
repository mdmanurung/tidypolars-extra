# Installation

## Requirements

- Python 3.9 or later

## Install from PyPI

```bash
pip install tidypolars-extra
```

## Install from Source

```bash
pip install git+https://github.com/mdmanurung/tidypolars-extra.git
```

## Dependencies

tidypolars-extra automatically installs the following dependencies:

| Package | Purpose |
|---------|---------|
| [polars](https://docs.pola.rs/) | High-performance DataFrame engine |
| [numpy](https://numpy.org/) | Numerical computing |
| [pandas](https://pandas.pydata.org/) | DataFrame interoperability |
| [pyarrow](https://arrow.apache.org/docs/python/) | Arrow columnar format support |
| [pyreadr](https://github.com/ofajardo/pyreadr) | Read R data files (RDS, Rdata) |
| [pyreadstat](https://github.com/Roche/pyreadstat) | Read Stata (.dta) and SPSS (.sav) files |

## Verify Installation

```python
import tidypolars_extra as tp

print(tp.__version__)
```
