from contextlib import closing
from datetime import datetime
from typing import Union

import requests
from bs4 import BeautifulSoup


# TODO write function which parsed images page html
# and return dict of links
def get_images_urls(
    month_year: str,
    resolution: str,
) -> dict:  # TODO think about it
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

    # TODO add this in log
    print("images urls not found")
    raise SystemExit


# TODO write func formating month and year
def format_month_year(month_year: str) -> tuple:
    try:
        date_time = datetime.strptime(month_year, "%m-%Y")
        month = date_time.strftime("%B").lower()
        year = date_time.strftime("%Y")
        return month, year
    except ValueError:
        # TODO add this in log
        print("Please enter data in right format 'mm-yyyy'")
        raise SystemExit


# TODO write the function checking the correctness of response
def _is_good_response(response: requests.models.Response) -> bool:
    """Return True if the response is HTML, False otherwise."""
    content_type = response.headers.get('Content-Type').lower()
    return (
        response.status_code == 200 and
        content_type is not None and
        content_type.find("html") > -1)


# TODO write func get page html
def _get_page_html(url: str) -> BeautifulSoup:
    try:
        with closing(requests.get(url)) as response:
            if _is_good_response(response):
                page_html = BeautifulSoup(response.content, "html.parser")
                return page_html
            # TODO write this in log
            print("Response is not good")
            raise SystemExit
    except requests.exceptions.RequestException:
        # TODO add log here
        print("Can't download page html")
        raise SystemExit


# TODO write func that find url next page
def _find_next_page_url(page_html: BeautifulSoup) -> str:
    next_page_url_tag = page_html.find(
        lambda tag:
        tag.name == "a" and
        tag.parent.name == "li" and
        tag.parent.get("class") and
        "pagination__next" in tag.parent.get("class")
    )

    try:
        next_page_url = next_page_url_tag.get("href")
    except AttributeError:
        # TODO add about this in log
        print("Can't find next page url. Pages is end")
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
        tag.get("title") == title
    )

    if image_urls_tags:
        return [url_tag.get("href") for url_tag in image_urls_tags]
    return None


# TODO write function convert month-year to url
def _get_images_page_url(month_year: str) -> str:
    month, year = format_month_year(month_year)

    base_url = "https://smashingmagazine.com"
    images_url = "/category/wallpapers/"

    page_html = _get_page_html(f"{base_url}{images_url}")

    while True:
        images_page_url = _find_images_page_url(page_html, month, year)
        if images_page_url is not None:
            return f"{base_url}{images_page_url}"

        next_page_url = _find_next_page_url(page_html)

        page_html = _get_page_html(f"{base_url}{next_page_url}")


# TODO write a function that gets images names
def _get_image_names(page_html: BeautifulSoup) -> list:
    name_tags = page_html.find_all(
        lambda tag:
        tag.name == "h3" and
        tag.get("id") and
        tag.get("id") != "Join In Next Month!"
    )

    if name_tags:
        return [tag.text.strip() for tag in name_tags]

    # TODO write in log if images_names don't exist
    print("images not found")
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
                image_name = image_url.split("/")[-1]
                images_urls[image_name] = image_url
        else:
            # TODO write about it in log
            # url for image_name in resolution not found
            pass
    return images_urls
