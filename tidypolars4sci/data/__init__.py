from pathlib import Path
from .diamonds import __load_diamonds__
from .mtcars import __load_mtcars__
from .starwars import __load_starwars__
from .vote import __load_vote__

__all__ = (
    "diamonds",
    "mtcars",
    "starwars",
    "vote",
)

DATA_DIR = Path(__file__).parent

mtcars = __load_mtcars__()
diamonds = __load_diamonds__()
try:
    starwars = __load_starwars__()
except (ImportError, Exception):
    starwars = None
vote = __load_vote__()
