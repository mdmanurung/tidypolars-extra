from pathlib import Path
from .diamonds import __load_diamonds__
from .flights import __load_flights__
from .iris import __load_iris__
from .mtcars import __load_mtcars__
from .penguins import __load_penguins__
from .starwars import __load_starwars__
from .vote import __load_vote__
from .wine import __load_wine__

__all__ = (
    "diamonds",
    "flights",
    "iris",
    "mtcars",
    "penguins",
    "starwars",
    "vote",
    "wine",
)

DATA_DIR = Path(__file__).parent

diamonds = __load_diamonds__()
flights = __load_flights__()
iris = __load_iris__()
mtcars = __load_mtcars__()
penguins = __load_penguins__()
starwars = __load_starwars__()
vote = __load_vote__()
wine = __load_wine__()
