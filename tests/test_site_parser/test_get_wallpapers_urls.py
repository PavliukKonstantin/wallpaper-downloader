# -*- coding: utf-8 -*-

from wallpaper_downloader import site_parser


def test_with_good_arguments(get_wallpapers_urls_from_file):
    """
    Test '_get_wallpapers_urls' function of site_parser module.

    Function is tested with the correct 'month_year' and
    'resolution' arguments.

    Args:
        get_wallpapers_urls_from_file (Fixture): fixture that return URLs of
            wallpapers in format {'wallpaper_filename': 'wallpaper_url'}.
    """
    expected_wallpapers_urls = get_wallpapers_urls_from_file
    wallpapers_urls = site_parser.get_wallpapers_urls("07-2020", "1920x1080")
    assert wallpapers_urls == expected_wallpapers_urls


def test_with_bad_resolution():
    """
    Test '_get_wallpapers_urls' function of site_parser module.

    Function is tested with the incorrect 'resolution' argument.
    """
    try:
        site_parser.get_wallpapers_urls("07-2020", "1920x10")
    except SystemExit:
        assert True
