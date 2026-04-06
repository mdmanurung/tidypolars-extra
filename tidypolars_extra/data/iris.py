from pathlib import Path
from ..io import read_data
from ..tibble_df import tibble

DATA_DIR = Path(__file__).parent

def __load_iris__():
    iris = read_data(fn=DATA_DIR / "iris.csv", sep=',', silently=True)
    iris.__doc__ = """
    Edgar Anderson's Iris Data

    ## Description

    This famous (Fisher's or Anderson's) iris data set gives the
    measurements in centimeters of the variables sepal length and
    width and petal length and width, respectively, for 50 flowers
    from each of 3 species of iris. The species are *Iris setosa*,
    *versicolor*, and *virginica*.

    ## Format

    A data frame with 150 observations on 5 variables.

    |--------------|----------------------------------------|
    | Column       | Description                            |
    |==============|========================================|
    | sepal_length | Sepal length in cm                     |
    | sepal_width  | Sepal width in cm                      |
    | petal_length | Petal length in cm                     |
    | petal_width  | Petal width in cm                      |
    | species      | Species (setosa, versicolor, virginica)|
    |--------------|----------------------------------------|

    ## Source

    Fisher, R. A. (1936) The use of multiple measurements in
    taxonomic problems. *Annals of Eugenics*, **7**, Part II, 179–188.

    The data were collected by Anderson, Edgar (1935). The irises of
    the Gaspe Peninsula, *Bulletin of the American Iris Society*,
    **59**, 2–5.
    """
    return tibble(iris)
