# -*- coding: utf-8 -*-

from wallpaper_downloader import site_parser


def test_good_month_year_format():
    """Test '_format_month_year' function of site_parser module.

    Function is tested with the month and year in good format.
    """
    result = site_parser.format_month_year("07-2020")
    assert result == ("july", "2020")


def test_bad_month_year_format():
    """Test '_format_month_year' function of site_parser module.

    Function is tested with the month and year in bad format.
    """
    try:
        site_parser.format_month_year("07-20")
    except SystemExit:
        assert True
