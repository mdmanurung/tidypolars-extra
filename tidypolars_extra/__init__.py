try:
    from importlib.metadata import version, PackageNotFoundError
    __version__ = version("tidypolars-extra")
except (ImportError, PackageNotFoundError):
    __version__ = ""


from .io import *
from .funs import *
from .forcats import *
from .helpers import *
from .lubridate import *
from .reexports import *
from .stringr import *
from .stats import *
from .tibble_df import *
from .type_conversion import *
from .utils import *

API_labels = {
    "tibble_df":'Tibble',
    'funs' : "Special Functions",
    'forcats' : "Factor Manipulation",
    'helpers' : "Helpers",
    'io' : "Read Files",
    'stats': "Statistics",
    'type_conversion':'Type Conversion'
}


