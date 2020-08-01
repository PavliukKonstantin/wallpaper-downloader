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


# TODO write function which parsed images page html
# and return dict of links
def get_images_urls(
    month_year: str,
    resolution: str,
) -> dict:
    images_page_url = _get_images_page_url(month_year)

    page_html = _get_page_html(images_page_url)

    image_names = _get_image_names(page_html)

    images_urls = _find_images_urls(
        page_html,
        image_names,
        resolution,
    )
    if images_urls:
        return images_urls

    c_logger.info(
        f"Images for {month_year} with resolution {resolution} not found",
    )
    raise SystemExit


# TODO write func formating month and year
def format_month_year(month_year: str) -> tuple:
    try:
        date_time = datetime.strptime(month_year, "%m-%Y")
        month = date_time.strftime("%B").lower()
        year = date_time.strftime("%Y")
        return month, year
    except ValueError:
        text = (
            f"Month and year - '{month_year}' entered in incorrect format. ",
            "Please enter month and year in correct format - 'mm-yyyy'",
        )
        c_logger.error("".join(text))
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
            c_logger.error(f"Response for '{page_url}' is wrong")
            raise SystemExit
    except requests.exceptions.RequestException:
        c_logger.error(f"Can't download page html for - '{page_url}'")
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
            f"Couldn't find wallpaper page for '{month_year}' month and year",
        )
        raise SystemExit
    else:
        return next_page_url


# TODO write func that find images page url
def _find_images_page_url(
    page_html: BeautifulSoup,
    month: str,
    year: str,
) -> Union[str, None]:
    images_page_url_tag = page_html.find(
        lambda tag:
        tag.name == "a" and
        tag.parent.name in {"h1", "h2"} and
        tag.get("href") and
        f"{month}-{year}" in tag.get("href")
    )
    if images_page_url_tag:
        return images_page_url_tag.get("href")
    return None


# TODO write func that find image url
def _find_image_urls(
    page_html: BeautifulSoup,
    title: str,
) -> Union[list, None]:
    image_urls_tags = page_html.find_all(
        lambda tag:
        tag.name == 'a' and
        tag.get("title") == title,
    )

    if image_urls_tags:
        return [url_tag.get("href") for url_tag in image_urls_tags]
    return None


# TODO write function convert month-year to url
def _get_images_page_url(month_year: str) -> str:
    month, year = format_month_year(month_year)

    base_url = "https://smashingmagazine.com"
    wallapper_category_url = "/category/wallpapers/"

    page_html = _get_page_html(f"{base_url}{wallapper_category_url}")

    while True:
        images_page_url = _find_images_page_url(page_html, month, year)
        if images_page_url is not None:
            return f"{base_url}{images_page_url}"

        next_page_url = _find_next_page_url(page_html, month_year)

        page_html = _get_page_html(f"{base_url}{next_page_url}")


# TODO write a function that gets images names
def _get_image_names(page_html: BeautifulSoup) -> list:
    name_tags = page_html.find_all(
        lambda tag:
        tag.name == "h3" and
        tag.get("id") and
        tag.get("id") != "Join In Next Month!",
    )

    if name_tags:
        return [tag.text.strip() for tag in name_tags]

    c_logger.error("Images names not found in page html")
    raise SystemExit


# TODO write a function that gets images urls
def _find_images_urls(
    page_html: BeautifulSoup,
    image_names: list,
    resolution: str,
) -> dict:
    images_urls = {}

    for image_name in image_names:
        title = f"{image_name} - {resolution}"
        image_urls = _find_image_urls(page_html, title)

        if image_urls:
            for image_url in image_urls:
                name = image_url.split("/")[-1]
                images_urls[name] = image_url
        else:
            text = (
                f"Url for '{image_name} in resolution ",
                f"{resolution}' not found",
            )
            c_logger.info("".join(text))
    return images_urls
