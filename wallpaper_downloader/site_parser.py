# -*- coding: utf-8 -*-

import logging
from contextlib import closing
from datetime import datetime
from typing import Union

import requests
from bs4 import BeautifulSoup

# Init console logger.
c_logger = logging.getLogger(__name__)
c_logger.setLevel(logging.INFO)
c_log = logging.StreamHandler()
c_formatter = logging.Formatter("%(levelname)s: %(message)s")
c_log.setFormatter(c_formatter)
c_logger.addHandler(c_log)


def format_month_year(month_year: str) -> tuple:
    """Convert month and year in correct format for parsing.

    Args:
        month_year (str): month and year in 'mm-yyyy' format.

    Raises:
        SystemExit: if month_year has incorrect format.

    Returns:
        tuple: month and year in ('july', '2020') format.
    """
    try:
        date_time = datetime.strptime(month_year, "%m-%Y")
        month = date_time.strftime("%B").lower()
        year = date_time.strftime("%Y")
        return month, year
    except ValueError:
        c_logger.error(
            f"Month and year '{month_year}' were entered in incorrect format. "
            "Please enter month and year in correct format - 'mm-yyyy'."
        )
        raise SystemExit


def _is_good_response(response: requests.models.Response) -> bool:
    """Check the correctness of response.

    Args:
        response (requests.models.Response): response of request.get(url)

    Returns:
        bool: True if response is OK.
    """
    content_type = response.headers.get('Content-Type').lower()
    response_status_ok = 200
    return (
        response.status_code == response_status_ok and
        content_type is not None and
        content_type.find("html") > -1
    )


def _get_page_html(page_url: str) -> BeautifulSoup:
    """Get HTML for URL.

    Args:
        page_url (str): URL of the page.

    Raises:
        SystemExit: response is not OK or raise RequestException.

    Returns:
        BeautifulSoup: HTML from the page.
    """
    try:
        with closing(requests.get(page_url)) as response:
            if not _is_good_response(response):
                c_logger.error(f"Response for '{page_url}' is wrong.")
                raise SystemExit
    except requests.exceptions.RequestException:
        c_logger.error(f"Can't download HTML from - '{page_url}'.")
        raise SystemExit
    else:
        return BeautifulSoup(response.content, "html.parser")


def _find_next_page_url(page_html: BeautifulSoup, month_year: str) -> str:
    """Parse HTML and search the URL of the next page.

    Args:
        page_html (BeautifulSoup): HTML for parsing.
        month_year (str): month and year in 'mm-yyyy' format.

    Raises:
        SystemExit: if the URL of the next page does not exist.

    Returns:
        str: URL of the next page.
    """
    next_page_url_tag = page_html.find(
        lambda tag:
        tag.name == "a" and
        tag.parent.name == "li" and
        tag.parent.get("class") and
        "pagination__next" in tag.parent.get("class"),
    )

    try:
        next_page_url = next_page_url_tag.get("href")
    except AttributeError:
        c_logger.error(
            "Couldn't find wallpapers page for "
            f"'{month_year}' month and year."
        )
        raise SystemExit
    else:
        return next_page_url


def _find_wallpapers_page_url(
    page_html: BeautifulSoup,
    month: str,
    year: str,
) -> Union[str, None]:
    """Parse HTML and search the URL of the page with wallpapers.

    Args:
        page_html (BeautifulSoup): HTML for parsing.
        month (str): month in full name format ('august').
        year (str): year in four-digit format ('2020').

    Returns:
        Union[str, None]: URL of wallpapers page or
            'None' if URL does not exist.
    """
    wallpapers_page_url_tag = page_html.find(
        lambda tag:
        tag.name == "a" and
        tag.parent.name in {"h1", "h2"} and
        tag.get("href") and
        f"{month}-{year}" in tag.get("href")
    )
    if wallpapers_page_url_tag:
        return wallpapers_page_url_tag.get("href")
    return None


def _find_wallpaper_urls(
    page_html: BeautifulSoup,
    title: str,
) -> Union[list, None]:
    """Parse HTML and search URLs of the wallpaper.

    One wallpaper has two URLs. For wallpapers with and without calendar.

    Args:
        page_html (BeautifulSoup): HTML for parsing.
        title (str): title in 'Wallpaper name - resolution' format.
            Example - 'Beautiful image - 1920x1080'.

    Returns:
        Union[list, None]: URLs of wallpapers or
            'None' if URLs of wallpapers does not exist.
    """
    wallpaper_urls_tags = page_html.find_all(
        lambda tag:
        tag.name == "a" and
        tag.get("title") == title,
    )

    if wallpaper_urls_tags:
        return [url_tag.get("href") for url_tag in wallpaper_urls_tags]
    return None


def _get_newest_wallpapers_month_year(page_html: BeautifulSoup) -> tuple:
    """Parse HTML and search month and year of the newest wallpapers.

    Args:
        page_html (BeautifulSoup): HTML for parsing.

    Raises:
        SystemExit: if the URL of the newest wallpapers does not exist.

    Returns:
        tuple: month and year the newest wallpapers
            in format ('july', '2020').
    """
    wallpapers_url_tag = page_html.find(
        lambda tag:
        tag.name == 'a' and
        tag.parent.name == "h2" and
        tag.parent.get("class") and
        "tilted-featured-article__title" in tag.parent.get("class")
    )
    if wallpapers_url_tag:
        wallpapers_url = wallpapers_url_tag.get("href")
        divided_wallpapers_url = wallpapers_url.split("-")
        month = divided_wallpapers_url[-2]
        year = divided_wallpapers_url[-1].rstrip("/")
        return month, year

    c_logger.error(
        "Something went wrong. Couldn't find url the newest wallpapers.",
    )
    raise SystemExit


def is_month_year_in_future(
    page_html: BeautifulSoup,
    month: str,
    year: str,
) -> bool:
    """Return result of compare request date to the newest wallpapers date.

    Args:
        page_html (BeautifulSoup): HTML for parsing.
        month (str): month in full name format ('august').
        year (str): year in four-digit format ('2020').

    Returns:
        bool: True if requested date newer than the newest wallpapers date.
    """
    newest_wallpapers_month_year = _get_newest_wallpapers_month_year(page_html)
    newest_dt = datetime.strptime(
        "-".join(newest_wallpapers_month_year),
        "%B-%Y",
    )
    requested_dt = datetime.strptime(f"{month}-{year}", "%B-%Y")
    return requested_dt > newest_dt


def _get_wallpapers_page_url(month_year: str) -> str:
    """Search in 'smashingmagazine.com' URL with requested wallpapers.

    Args:
        month_year (str): month and year in 'mm-yyyy' format.

    Raises:
        SystemExit: if the URL of wallpapers does not exist.

    Returns:
        str: URL of the page with wallpapers.
    """
    base_url = "https://smashingmagazine.com"
    wallapper_category_url = "/category/wallpapers/"

    month, year = format_month_year(month_year)
    page_html = _get_page_html(f"{base_url}{wallapper_category_url}")

    if is_month_year_in_future(page_html, month, year):
        c_logger.error(
            f"Wallpapers for '{month}-{year}' does not exist yet. "
            "You can't download wallpapers from the future."
        )
        raise SystemExit

    while True:
        wallpapers_page_url = _find_wallpapers_page_url(page_html, month, year)
        if wallpapers_page_url is not None:
            return f"{base_url}{wallpapers_page_url}"

        next_page_url = _find_next_page_url(page_html, month_year)
        page_html = _get_page_html(f"{base_url}{next_page_url}")


def _find_wallpapers_names(page_html: BeautifulSoup) -> list:
    """Parse HTML and search wallpapers names.

    Args:
        page_html (BeautifulSoup): HTML for parsing.

    Raises:
        SystemExit: if wallpapers names does not exist.

    Returns:
        list: wallpapers names
    """
    name_tags = page_html.find_all(
        lambda tag:
        tag.name == "h3" and
        tag.get("id") and
        tag.text.find("Join In Next Month!") == -1
    )

    if name_tags:
        return [tag.text.strip() for tag in name_tags]

    c_logger.error("Wallpapers names weren't found in the HTML.")
    raise SystemExit


def _find_wallpapers_urls(
    page_html: BeautifulSoup,
    wallpapers_names: list,
    resolution: str,
) -> dict:
    """Parse HTML and search wallpapers URLs.

    Args:
        page_html (BeautifulSoup): HTML for parsing.
        wallpapers_names (list): wallpapers names.
        resolution (str): wallpapers resolution in 'width'x'height' format.
            Example - '1920x1080'.

    Returns:
        dict: URLs of wallpapers in '{wallpaper_name: wallpaper_url}' format.
    """
    wallpapers_urls = {}

    for wallpaper_name in wallpapers_names:
        title = f"{wallpaper_name} - {resolution}"
        wallpaper_urls = _find_wallpaper_urls(page_html, title)

        if wallpaper_urls:
            for wallpaper_url in wallpaper_urls:
                name = wallpaper_url.split("/")[-1]
                wallpapers_urls[name] = wallpaper_url
        else:
            c_logger.warning(
                f"URL for '{wallpaper_name}' in resolution "
                f"{resolution} not found."
            )
    return wallpapers_urls


def get_wallpapers_urls(
    month_year: str,
    resolution: str,
) -> dict:
    """Return URLs of wallpapers found in the HTML.

    Args:
        month_year (str): month and year in 'mm-yyyy' format.
        resolution (str): wallpapers resolution in 'width'x'height' format.
            Example - '1920x1080'

    Raises:
        SystemExit: if URLs of wallpapers with requested parameters
            does not exist.

    Returns:
        dict: URLs of wallpapers in
            '{wallpaper_filename: wallpaper_url}' format.
    """
    c_logger.info("Site parsing started.")
    wallpapers_page_url = _get_wallpapers_page_url(month_year)
    page_html = _get_page_html(wallpapers_page_url)
    wallpaper_names = _find_wallpapers_names(page_html)
    wallpapers_urls = _find_wallpapers_urls(
        page_html,
        wallpaper_names,
        resolution,
    )
    if wallpapers_urls:
        c_logger.info("Parsing successfully completed.")
        return wallpapers_urls

    c_logger.info(
        f"Wallpapers for {month_year} with resolution {resolution} not found.",
    )
    raise SystemExit
