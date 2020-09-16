from wallpaper_downloader import site_parser


def test_with_month_year_in_future(get_page_html_from_file):
    """
    Test '_is_month_year_in_future' function of site_parser module.

    Function is tested with the month and year more than the newest
    month and year in the HTML.

    Args:
        get_page_html_from_file (Fixture): fixture that return HTML.
    """
    page_html = get_page_html_from_file("first_main_page.html")
    month_year_in_future = site_parser.is_month_year_in_future(
        page_html,
        "september",
        "2020",
    )
    assert month_year_in_future is True


def test_with_month_year_in_past(get_page_html_from_file):
    """
    Test '_is_month_year_in_future' function of site_parser module.

    Function is tested with the month and year less than the newest
    month and year in the HTML.

    Args:
        get_page_html_from_file (Fixture): fixture that return HTML.
    """
    page_html = get_page_html_from_file("first_main_page.html")
    month_year_in_future = site_parser.is_month_year_in_future(
        page_html,
        "july",
        "2020",
    )
    assert month_year_in_future is False
