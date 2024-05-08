"""
As tag formatting differs between gaming websites, this file stores all 
possible exception cases where this can occur. Due to the low number of cases 
where this occurs, as well as a wide range of irregularities in the length of tags 
and the frequency of differences, we use a dictionary mapping to navigate the 
tag inconsistencies.
"""


def tag_exception_dict() -> dict:
    """Returns a dict object containing a mapping of all tag exceptions
    between gaming websites."""

    return {'Single Player': 'Singleplayer', 'Rogue-Lite': 'Roguelite'}
