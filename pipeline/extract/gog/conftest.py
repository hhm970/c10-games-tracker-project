'''A conftest file that defines functions used in test_extract_gog.py.'''

import pytest

from bs4 import BeautifulSoup


@pytest.fixture
def gog_fake_links() -> list[BeautifulSoup]:
    '''Returns an example of href links to find publisher.'''
    return [BeautifulSoup(
        '<a href="/gam">seven</a>', features='html.parser').find('a'), BeautifulSoup(
        '<a href="/games?publishers=Bethesda">publisher1</a>', features='html.parser').find('a'), BeautifulSoup(
        '<a href="/shers=Bethesda">word2</a>', features='html.parser').find('a'), BeautifulSoup(
        '<a href="/games?developers=Bethesda">dev</a>', features='html.parser').find('a')]


@pytest.fixture
def gog_fake_links_bad() -> list[BeautifulSoup]:
    '''Returns badly formatted hrefs.'''
    return [BeautifulSoup(
        '<a href="/gamesubliesda">publisher1</a>', features='html.parser').find('a'), BeautifulSoup(
        '<a href="/gam">seven</a>', features='html.parser').find('a'), BeautifulSoup(
        '<a href="/shers=Bethesda">word2</a>', features='html.parser').find('a')]


@pytest.fixture
def gog_tags() -> BeautifulSoup:
    '''Returns an example of a Soup of game tags.'''
    return BeautifulSoup(
        '''<span class="details__link-text">tag7</span>
        <span class="details__link-text">tag72</span>''', features='html.parser')


@pytest.fixture
def gog_tags_bad() -> BeautifulSoup:
    '''Returns a bad example of a Soup of game tags.'''
    return BeautifulSoup(
        '''<span class="detail">tag7</span>
        <span class="detailt">tag72</span>''', features='html.parser')


@pytest.fixture
def gog_title() -> BeautifulSoup:
    '''Returns an example of a game title.'''
    return BeautifulSoup(
        '''<div class="product-tile__title" title='goodtitle'>tag7</div>
        <span class="details__link-text">tag72</span>''', features='html.parser')


@pytest.fixture
def gog_description() -> BeautifulSoup:
    '''Returns an example of a game description.'''
    return BeautifulSoup(
        '''<div class="description" >a very nice really thorough description </div>''', features='html.parser')


@pytest.fixture
def gog_time():
    '''Returns an example of release dates.'''
    return BeautifulSoup(
        '''<div class="details__content table__row-content" >
        <span>{{"2024-05-24T09:55:00+03:00"}} </span>
        </div>
        <div class="details__content table__row-content" >
        <span>{{"2024-10-24T09:55:00+03:00"}} </span>
        </div>
        <div class="details__content table__row-content" >
        <span>{{"2024-04-04T09:55:00+03:00"}} </span>
        </div>
        <div class="details__content table__row-content" >
        <span>{{"2023-04-24T09:55:00+03:00"}} </span>
        </div>
        <div class="details__content table__row-content" >
        <span>{{"202400"}} </span>
        </div>
        <div class="details__content table__row-content" >
        <span>{{"2024-04-24T09:55:00+03:00"}} </span>
        </div>''', features='html.parser')
