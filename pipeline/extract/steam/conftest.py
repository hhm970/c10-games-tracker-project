"""Conftest file for test_extract_steam."""
import pytest

from bs4 import BeautifulSoup


@pytest.fixture
def steam_rating_soup() -> BeautifulSoup:
    '''Returns an example of html for the number of reviews.'''
    return BeautifulSoup(""" <div class="review_ctn"> 
                         <label for="review_type_positive">Positive&nbsp;<span class="user_reviews_count">(105)</span></label><br> 
                         <label for="review_type_negative">Negative&nbsp;<span class="user_reviews_count">(103)</span></label>
                         </div>""", features='html.parser')


@pytest.fixture
def steam_no_rating_soup() -> BeautifulSoup:
    '''Returns an example of html for no reviews.'''
    return BeautifulSoup(""" <div class="review_ctn"> 
                        "There are no reviews for this product"
                         </div>""", features='html.parser')


@pytest.fixture
def steam_rating_soup_positive_only() -> BeautifulSoup:
    '''Returns an example of html for the number of reviews,
    when there are only positive reviews.'''
    return BeautifulSoup(""" <div class="review_ctn"> 
                         <label for="review_type_positive">Positive&nbsp;<span class="user_reviews_count">(105)</span></label><br> 
                         </div>""", features='html.parser')


@pytest.fixture
def steam_rating_soup_negative_only() -> BeautifulSoup:
    '''Returns an example of html for the number of reviews,
    when there are only negative reviews.'''
    return BeautifulSoup(""" <div class="review_ctn"> 
                         <label for="review_type_negative">Negative&nbsp;<span class="user_reviews_count">(103)</span></label>
                         </div>""", features='html.parser')


@pytest.fixture
def steam_tags_good():
    '''Returns an example of html for game tags.'''
    return BeautifulSoup(""" <a href="https://store.steampowered.com/tags/en/Horror/?snr=1_5_9__409" class="app_tag" style="display: none;"> Horror	</a>
                         <a href="https://store.steampowered.com/tags/en/Atmospheric/?snr=1_5_9__409" class="app_tag" style="display: none;">Atmospheric</a>""",
                         features='html.parser')


@pytest.fixture
def steam_tags_none():
    '''Returns an example of html for the tags, when there are none.'''
    return BeautifulSoup("""<div class="review_ctn"> 
                         <label for="review_type_negative">Negative&nbsp;<span class="user_reviews_count">(103)</span></label>
                         </div>""",
                         features='html.parser')


@pytest.fixture
def steam_developer_good():
    '''Returns an example of html for the developer.'''
    return BeautifulSoup("""</div>
<div class="dev_row">
<div class="subtitle column">Developer:</div>
<div class="summary column" id="developers_list">
<a href="https://store.steampowered.com/search/?developer=SCLITIFY%20IT&amp;snr=1_5_9__2000">SCLITIFY IT</a> </div>
</div>""", features='html.parser')


@pytest.fixture
def steam_developer_none():
    '''Returns an example of html for the developer,
    when there is none.'''
    return BeautifulSoup("""<div class="review_ctn"> 
                         <label for="review_type_negative">Negative&nbsp;<span class="user_reviews_count">(103)</span></label>
                         </div>""",
                         features='html.parser')


@pytest.fixture
def steam_publisher_good():
    '''Returns an example of html for the publisher.'''
    return BeautifulSoup("""[<div class="dev_row">
<div class="subtitle column">Developer:</div>
<div class="summary column" id="developers_list">
<a href="https://store.steampowered.com/search/?developer=Inoaames&amp;snr=1_5_9__2000">Inoa Games</a> </div>
</div>, <div class="dev_row">
<div class="subtitle column">Publisher:</div>
<div class="summary column">
<a href="https://store.steampowered.com/search/?publisher=Inoames&amp;snr=1_5_9__422">Inoa Forever</a> </div>
</div>, <div class="dev_row">
<b>Developer:</b>
<a href="https://store.steampowered.com/search/?developer=Inoames&amp;snr=1_5_9__408">Inoa Games</a>
</div>, <div class="dev_row">
<b>Publisher:</b>
<a href="https://store.steampowered.com/search/?publisher=Inoames&amp;snr=1_5_9__422">Inoa Forever</a>
</div>, <div class="dev_row">
<b>Franchise:</b>
<a href="https://store.steampowered.com/search/?franchise=DNA&amp;snr=1_5_9__408">DNA</a>
</div>]""", features='html.parser')


@pytest.fixture
def search_result():
    '''Returns an example of html for general information about a game.'''
    return BeautifulSoup("""<span class="title">Culling of Normality</span>
<div class="discount_final_price free">Free</div>
<div class="col search_released responsive_secondrow"> 24 Apr, 2024</div>""", features='html.parser')
