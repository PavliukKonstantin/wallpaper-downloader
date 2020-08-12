# -*- coding: utf-8 -*-

from wallpaper_downloader import site_parser


def test_page_with_next_page_url(get_page_html_from_file):
    """Test '_find_next_page_url' function of site_parser module.

    Function is tested with the HTML where URL of the next page is exists.

    Args:
        get_page_html_from_file (Fixture): fixture that return page HTML.
    """
    page_html = get_page_html_from_file("first_main_page.html")
    next_page_url = site_parser._find_next_page_url(page_html, "07-2020")
    expected_next_page_url = ("/categories/wallpapers/page/2/")
    assert next_page_url == expected_next_page_url


def test_page_without_next_page_url(get_page_html_from_file):
    """Test '_find_next_page_url' function of site_parser module.

    Function is tested with the HTML where URL of the next page is not exists.

    Args:
        get_page_html_from_file (Fixture): fixture that return HTML.
    """
    page_html = get_page_html_from_file("last_main_page.html")
    try:
        site_parser._find_next_page_url(page_html, "07-2020")
    except SystemExit:
        assert SystemExit
