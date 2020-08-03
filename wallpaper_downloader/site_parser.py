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


# TODO write func formating month and year
def format_month_year(month_year: str) -> tuple:
    try:
        date_time = datetime.strptime(month_year, "%m-%Y")
        month = date_time.strftime("%B").lower()
        year = date_time.strftime("%Y")
        return month, year
    except ValueError:
        c_logger.error(
            f"Month and year - '{month_year}' entered in incorrect format. "
            "Please enter month and year in correct format - 'mm-yyyy'."
        )
        raise SystemExit


# TODO write the function checking the correctness of response
def _is_good_response(response: requests.models.Response) -> bool:
    """Return True if the response is HTML, False otherwise."""
    content_type = response.headers.get('Content-Type').lower()
    response_status_ok = 200
    return (
        response.status_code == response_status_ok and
        content_type is not None and
        content_type.find("html") > -1
    )


# TODO write func get page html
def _get_page_html(page_url: str) -> BeautifulSoup:
    try:
        with closing(requests.get(page_url)) as response:
            if _is_good_response(response):
                return BeautifulSoup(response.content, "html.parser")
            c_logger.error(f"Response for '{page_url}' is wrong.")
            raise SystemExit
    except requests.exceptions.RequestException:
        c_logger.error(f"Can't download page html for - '{page_url}'.")
        raise SystemExit


# TODO write func that find url next page
def _find_next_page_url(page_html: BeautifulSoup, month_year: str) -> str:
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


# TODO write func that find wallpapers page url
def _find_wallpapers_page_url(
    page_html: BeautifulSoup,
    month: str,
    year: str,
) -> Union[str, None]:
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


# TODO write func that find wallpaper url
def _find_wallpaper_urls(
    page_html: BeautifulSoup,
    title: str,
) -> Union[list, None]:
    wallpaper_urls_tags = page_html.find_all(
        lambda tag:
        tag.name == "a" and
        tag.get("title") == title,
    )

    if wallpaper_urls_tags:
        return [url_tag.get("href") for url_tag in wallpaper_urls_tags]
    return None


# TODO write func that find newest wallpapers page url
def _get_newest_wallpapers_month_year(page_html: BeautifulSoup) -> tuple:
    wallpapers_url_tag = page_html.find(
        lambda tag:
        tag.name == 'a' and
        tag.parent.name == "h2" and
        tag.parent.get("class") and
        "tilted-featured-article__title" in tag.parent.get("class")
    )
    if wallpapers_url_tag:
        wallpapers_url = wallpapers_url_tag.get("href")
        month = wallpapers_url.split("-")[-2]
        year = wallpapers_url.split("-")[-1].rstrip("/")
        return month, year

    c_logger.error("Something wrong. Couldn't find url the newest wallpapers.")
    raise SystemExit


# TODO write func that compare request date with newest wallpapers date
def is_month_year_in_future(
    page_html: BeautifulSoup,
    month: str,
    year: str,
) -> bool:
    newest_wallpapers_month_year = _get_newest_wallpapers_month_year(page_html)
    newest_dt = datetime.strptime(
        "-".join(newest_wallpapers_month_year),
        "%B-%Y",
    )
    requested_dt = datetime.strptime(f"{month}-{year}", "%B-%Y")
    return requested_dt > newest_dt


# TODO write function convert month-year to url
def _get_wallpapers_page_url(month_year: str) -> str:
    base_url = "https://smashingmagazine.com"
    wallapper_category_url = "/category/wallpapers/"

    month, year = format_month_year(month_year)
    page_html = _get_page_html(f"{base_url}{wallapper_category_url}")

    if is_month_year_in_future(page_html, month, year):
        c_logger.error(
            f"Wallpapers for '{month}-{year}' doesn't yet exist. "
            "You can't download wallpapers from the future."
        )
        raise SystemExit

    while True:
        wallpapers_page_url = _find_wallpapers_page_url(page_html, month, year)
        if wallpapers_page_url is not None:
            return f"{base_url}{wallpapers_page_url}"

        next_page_url = _find_next_page_url(page_html, month_year)
        page_html = _get_page_html(f"{base_url}{next_page_url}")


# TODO write a function that gets wallpapers names
def _get_wallpapers_names(page_html: BeautifulSoup) -> list:
    name_tags = page_html.find_all(
        lambda tag:
        tag.name == "h3" and
        tag.get("id") and
        tag.get("id") != "Join In Next Month!",
    )

    if name_tags:
        return [tag.text.strip() for tag in name_tags]

    c_logger.error("Wallpapers names not found in page html.")
    raise SystemExit


# TODO write a function that gets wallpapers urls
def _find_wallpapers_urls(
    page_html: BeautifulSoup,
    wallpapers_names: list,
    resolution: str,
) -> dict:
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
                f"Url for '{wallpaper_name}' in resolution "
                f"{resolution} not found."
            )
    return wallpapers_urls


# TODO write function which parsed wallpapers page html
# and return dict of links
def get_wallpapers_urls(
    month_year: str,
    resolution: str,
) -> dict:
    c_logger.info("Site parsing started.")
    wallpapers_page_url = _get_wallpapers_page_url(month_year)
    page_html = _get_page_html(wallpapers_page_url)
    wallpaper_names = _get_wallpapers_names(page_html)
    wallpapers_urls = _find_wallpapers_urls(
        page_html,
        wallpaper_names,
        resolution,
    )
    if wallpapers_urls:
        c_logger.info("Site parsing successfully completed.")
        return wallpapers_urls

    c_logger.info(
        f"Wallpapers for {month_year} with resolution {resolution} not found.",
    )
    raise SystemExit
