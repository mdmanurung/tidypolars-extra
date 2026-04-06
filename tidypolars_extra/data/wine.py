from pathlib import Path
from ..io import read_data
from ..tibble_df import tibble

DATA_DIR = Path(__file__).parent

def __load_wine__():
    wine = read_data(fn=DATA_DIR / "wine.csv", sep=',', silently=True)
    wine.__doc__ = """
    UCI Wine Recognition Data

    ## Description

    These data are the results of a chemical analysis of wines
    grown in the same region in Italy but derived from three
    different cultivars. The analysis determined the quantities
    of 13 constituents found in each of the three types of wines.

    ## Format

    A data frame with 178 observations on 14 variables.

    |-------------------------------|-----------------------------------------------|
    | Column                        | Description                                   |
    |===============================|===============================================|
    | class                         | Wine cultivar class (1, 2, or 3)              |
    | alcohol                       | Alcohol content                               |
    | malic_acid                    | Malic acid                                    |
    | ash                           | Ash                                           |
    | alcalinity_of_ash             | Alcalinity of ash                             |
    | magnesium                     | Magnesium                                     |
    | total_phenols                 | Total phenols                                 |
    | flavanoids                    | Flavanoids                                    |
    | nonflavanoid_phenols          | Nonflavanoid phenols                          |
    | proanthocyanins               | Proanthocyanins                               |
    | color_intensity               | Color intensity                               |
    | hue                           | Hue                                           |
    | od280_od315_of_diluted_wines  | OD280/OD315 of diluted wines                  |
    | proline                       | Proline                                       |
    |-------------------------------|-----------------------------------------------|

    ## Source

    Forina, M. et al. (1988). UCI Machine Learning Repository.
    https://archive.ics.uci.edu/ml/datasets/wine

    Original owners: Stefan Aeberhard, email: stefan@coral.cs.jcu.edu.au
    """
    return tibble(wine)
