'''A conftest file that defines functions used in test_epic.py.'''

import pytest


@pytest.fixture
def epic_game_post_response() -> dict:
    '''Returns an example post response.'''
    return {
        "data": {
            "Catalog": {
                "searchStore": {
                    "elements": [
                        {
                            "title": "Vengeance of Mr. Peppermint",
                            "releaseDate": "2024-04-24T16:00:00.000Z",
                            "description": "Long ago, they killed his sister. Now, he will kill them.",
                            "publisherDisplayName": "Freedom Games",
                            "developerDisplayName": "Hack The Publisher",
                            "currentPrice": 1999,
                            "seller": {
                                "name": "Freedom Games"
                            },
                            "tags": [
                                {
                                    "name": "Action",
                                    "groupName": "genre"
                                },
                                {
                                    "name": "Action-Adventure",
                                    "groupName": "genre"
                                },
                                {
                                    "name": "Single Player",
                                    "groupName": "feature"
                                },
                                {
                                    "name": "Windows",
                                    "groupName": "platform"
                                },
                                {
                                    "name": "Indie",
                                    "groupName": "genre"
                                },
                                {
                                    "name": "Mac OS",
                                    "groupName": "platform"
                                }
                            ],
                            "categories": [
                                {
                                    "path": "games/edition/base"
                                },
                                {
                                    "path": "games/edition"
                                },
                                {
                                    "path": "games"
                                }
                            ]
                        }]
                }
            }
        }
    }


@pytest.fixture
def epic_game_data_game_obj() -> Dict:
    '''Returns an example post response.'''
    return {
        "title": "Vengeance of Mr. Peppermint",
        "releaseDate": "2024-04-24T16:00:00.000Z",
        "description": "Long ago, they killed his sister. Now, he will kill them.",
        "publisherDisplayName": "Freedom Games",
        "developerDisplayName": "Hack The Publisher",
        "currentPrice": 1999,
        "seller": {
                                "name": "Freedom Games"
        },
        "tags": [
            {
                "name": "Action",
                "groupName": "genre"
            },
            {
                "name": "Action-Adventure",
                "groupName": "genre"
            },
            {
                "name": "Single Player",
                "groupName": "feature"
            },
            {
                "name": "Windows",
                "groupName": "platform"
            },
            {
                "name": "Indie",
                "groupName": "genre"
            },
            {
                "name": "Mac OS",
                "groupName": "platform"
            }
        ],
        "categories": [
            {
                "path": "games/edition/base"
            },
            {
                "path": "games/edition"
            },
            {
                "path": "games"
            }
        ]
    }


@pytest.fixture
def epic_empty_post_request() -> Dict:
    '''Returns an empty post response.'''
    return {
        "data": {
            "Catalog": {
                "searchStore": {
                    "elements": [
                    ]
                }
            }
        }
    }
