# -*- coding: utf-8 -*-

from wallpaper_downloader import site_parser


def test_page_with_newest_wallpapers_month_year(get_page_html_from_file):
    """
    Test '_get_newest_wallpapers_month_year' function of site_parser module.

    Function is tested with the page HTML where
    the newest wallpapers header is exists.

    Args:
        get_page_html_from_file (Fixture): fixture that return page HTML.
    """
    page_html = get_page_html_from_file("first_main_page.html")
    month, year = site_parser._get_newest_wallpapers_month_year(page_html)
    expected_month = "august"
    expected_year = "2020"
    assert (month, year) == (expected_month, expected_year)


def test_page_without_newest_wallpapers_month_year(get_page_html_from_file):
    """
    Test '_get_newest_wallpapers_month_year' function of site_parser module.

    Function is tested with the HTML where
    the newest wallpapers header is not exists.

    Args:
        get_page_html_from_file (Fixture): fixture that return HTML.
    """
    page_html = get_page_html_from_file("page_with_wallpapers.html")
    try:
        site_parser._get_newest_wallpapers_month_year(page_html)
    except SystemExit:
        assert True
    else:
        assert False
