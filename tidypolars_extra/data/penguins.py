from pathlib import Path
from ..io import read_data
from ..tibble_df import tibble

DATA_DIR = Path(__file__).parent

def __load_penguins__():
    penguins = read_data(fn=DATA_DIR / "penguins.csv", sep=',', silently=True)
    penguins.__doc__ = """
    Palmer Penguins

    ## Description

    Size measurements for adult foraging penguins near Palmer
    Station, Antarctica. Includes measurements for penguin species
    Adelie, Chinstrap, and Gentoo, collected from 2007 to 2009 by
    Dr. Kristen Gorman with the Palmer Station Long Term Ecological
    Research Program.

    ## Format

    A data frame with 344 observations on 8 variables.

    |-------------------|------------------------------------------------|
    | Column            | Description                                    |
    |===================|================================================|
    | species           | Penguin species (Adelie, Chinstrap, Gentoo)    |
    | island            | Island in Palmer Archipelago                   |
    |                   | (Biscoe, Dream, Torgersen)                     |
    | bill_length_mm    | Bill length (mm)                               |
    | bill_depth_mm     | Bill depth (mm)                                |
    | flipper_length_mm | Flipper length (mm)                            |
    | body_mass_g       | Body mass (g)                                  |
    | sex               | Penguin sex (male, female)                     |
    | year              | Study year (2007, 2008, 2009)                  |
    |-------------------|------------------------------------------------|

    ## Source

    Horst AM, Hill AP, Gorman KB (2020). palmerpenguins: Palmer
    Archipelago (Antarctica) penguin data. R package version 0.1.0.
    https://allisonhorst.github.io/palmerpenguins/

    Gorman KB, Williams TD, Fraser WR (2014). Ecological sexual
    dimorphism and environmental variability within a community of
    Antarctic penguins (genus *Pygoscelis*). *PLoS ONE*, **9**(3),
    e90081.
    """
    return tibble(penguins)
