from wallpaper_downloader import site_parser


def test_good_response(get_sync_response_from_url):
    """
    Test '_is_good_response' function of site_parser module.

    Function is tested with the good response.

    Args:
        get_sync_response_from_url (Fixture): fixture that return
            the response of requests.get(page_url).
    """
    response = get_sync_response_from_url(
        "https://www.smashingmagazine.com/category/wallpapers/",
    )
    result = site_parser._is_good_response(response)
    assert result is True


def test_bad_response(get_sync_response_from_url):
    """
    Test '_is_good_response' function of site_parser module.

    Function is tested with the bad response.

    Args:
        get_sync_response_from_url (Fixture): fixture that return
            the response of requests.get(page_url).
    """
    response = get_sync_response_from_url(
        "https://www.smashingmagazine.com/category/wallpaper/",
    )
    result = site_parser._is_good_response(response)
    assert result is False


def test_response_with_non_html_content(get_sync_response_from_url):
    """
    Test '_is_good_response' function of site_parser module.

    Function is tested with the good response with not image content.

    Args:
        get_sync_response_from_url (Fixture): fixture that return
            the response of requests.get(page_url).
    """
    response = get_sync_response_from_url(
        "http://files.smashingmagazine.com/wallpapers/july-17/"
        "summer-cannonball/cal/july-17-summer-cannonball-cal-320x480.png"
    )
    result = site_parser._is_good_response(response)
    assert result is False
