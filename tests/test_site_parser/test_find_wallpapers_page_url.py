# -*- coding: utf-8 -*-

import os

from wallpaper_downloader import site_parser


def test_with_wallpapers_page_url(get_page_html_from_file):
    """
    Test '_find_wallpapers_page_url' function of site_parser module.

    Function is tested with the HTML where URL the wallpapers is exists.

    Args:
        get_page_html_from_file (Fixture): fixture that return HTML.
    """
    page_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "files_for_tests",
        "first_main_page.html",
    )
    page_html = get_page_html_from_file(page_path)
    page_url = site_parser._find_wallpapers_page_url(
        page_html,
        "august",
        "2020"
    )
    expected_page_url = ("/2020/07/desktop-wallpaper-calendars-august-2020/")
    assert page_url == expected_page_url


def test_without_wallpapers_page_url(get_page_html_from_file):
    """
    Test '_find_wallpapers_page_url' function of site_parser module.

    Function is tested with the HTML where URL the wallpapers is not exists.

    Args:
        get_page_html_from_file (Fixture): fixture that return HTML.
    """
    page_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "files_for_tests",
        "second_main_page.html",
    )
    page_html = get_page_html_from_file(page_path)
    page_url = site_parser._find_wallpapers_page_url(
        page_html,
        "august",
        "2020"
    )
    assert page_url is None
