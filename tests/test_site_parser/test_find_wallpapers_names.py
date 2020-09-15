# -*- coding: utf-8 -*-

from wallpaper_downloader import site_parser


def test_page_with_wallpapers_names(
    get_page_html_from_file,
    get_wallpapers_names_from_file,
):
    """
    Test '_find_wallpapers_names' function of site_parser module.

    Function is tested with the HTML where names of wallpapers are exist.

    Args:
        get_page_html_from_file (Fixture): fixture that return HTML.
        get_wallpapers_names_from_file (Fixture): fixture that return
            names of wallpapers.
    """
    page_html = get_page_html_from_file("page_with_wallpapers.html")
    wallpapers_names = site_parser._find_wallpapers_names(page_html)
    expected_wallpapers_names = get_wallpapers_names_from_file
    assert wallpapers_names == expected_wallpapers_names


def test_page_without_wallpapers_names(get_page_html_from_file):
    """
    Test '_find_wallpapers_names' function of site_parser module.

    Function is tested with the HTML where names of wallpapers are not exist.

    Args:
        get_page_html_from_file (Fixture): fixture that return HTML.
        get_wallpapers_names_from_file (Fixture): fixture that return
            names of wallpapers.
    """
    page_html = get_page_html_from_file("first_main_page.html")
    try:
        site_parser._find_wallpapers_names(page_html)
    except SystemExit:
        assert True
    else:
        assert False
