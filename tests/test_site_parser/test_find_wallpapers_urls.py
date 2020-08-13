# -*- coding: utf-8 -*-

from wallpaper_downloader import site_parser


def test_page_with_wallpapers_urls(
    get_page_html_from_file,
    get_wallpapers_urls_from_file,
    get_wallpapers_names_from_file,
):
    """
    Test '_find_wallpapers_urls' function of site_parser module.

    Function is tested with the HTML where URLs of wallpapers are exist.

    Args:
        get_page_html_from_file (Fixture): fixture that return HTML.
        get_wallpapers_urls_from_file (Fixture): fixture that return URLs of
            wallpapers in format {'wallpaper_filename': 'wallpaper_url'}.
        get_wallpapers_names_from_file (Fixture): fixture that return
            names of wallpapers.
    """
    page_html = get_page_html_from_file("page_with_wallpapers.html")
    wallpapers_names = get_wallpapers_names_from_file
    wallpapers_urls = site_parser._find_wallpapers_urls(
        page_html,
        wallpapers_names,
        "1920x1080",
    )
    expected_wallpapers_urls = get_wallpapers_urls_from_file
    assert wallpapers_urls == expected_wallpapers_urls


def test_page_without_wallpapers_urls(
    get_page_html_from_file,
    get_wallpapers_names_from_file,
):
    """
    Test '_find_wallpapers_urls' function of site_parser module.

    Function is tested with the HTML where URLs of wallpapers are not exist.

    Args:
        get_page_html_from_file (Fixture): fixture that return HTML.
        get_wallpapers_names_from_file (Fixture): fixture that return
            names of wallpapers.
    """
    page_html = get_page_html_from_file("first_main_page.html")
    wallpapers_names = get_wallpapers_names_from_file
    wallpapers_urls = site_parser._find_wallpapers_urls(
        page_html,
        wallpapers_names,
        "1920x1080",
    )
    assert wallpapers_urls == {}
