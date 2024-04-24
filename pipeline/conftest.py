import pytest


@pytest.fixture
def epic_game_data_ideal_post_response():
    return {
        "data": {
            "Catalog": {
                "searchStore": {
                    "elements": [
                        {
                            "title": "Vengeance of Mr. Peppermint",
                            "releaseDate": "2024-04-24T16:00:00.000Z",
                            "description": "Long ago, they killed his sister. Now, he will kill them. Join a hard-boiled detective as he murders his way through the criminal underworld to find and punish those responsible for his sister's death...before his mind unravels and his vengeance completely destroys him.",
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
def epic_game_data_game_obj():
    return {
        "title": "Vengeance of Mr. Peppermint",
        "releaseDate": "2024-04-24T16:00:00.000Z",
        "description": "Long ago, they killed his sister. Now, he will kill them. Join a hard-boiled detective as he murders his way through the criminal underworld to find and punish those responsible for his sister's death...before his mind unravels and his vengeance completely destroys him.",
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
def epic_empty_post_request():
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
