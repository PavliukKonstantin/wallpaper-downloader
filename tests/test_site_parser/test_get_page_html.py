# -*- coding: utf-8 -*-

from wallpaper_downloader import site_parser
from bs4 import BeautifulSoup


def test_good_page_url():
    """Test '_get_page_html' function of site_parser module.

    Function is tested with the good URL of the page.
    """
    page_html = site_parser._get_page_html(
        "https://www.smashingmagazine.com/category/wallpapers/",
    )
    assert type(page_html) == BeautifulSoup


def test_bad_page_url():
    """Test '_get_page_html' function of site_parser module.

    Function is tested with the good URL of the page.
    """
    try:
        site_parser._get_page_html(
            "https://www.smashingmagazine.com/category/wallpaper/",
        )
    except SystemExit:
        assert True
