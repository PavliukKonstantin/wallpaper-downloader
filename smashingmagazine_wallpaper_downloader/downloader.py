import asyncio
import time
from datetime import datetime
from typing import Union
from contextlib import closing

import aiohttp
import requests
from bs4 import BeautifulSoup
from requests.models import Response

# TODO write func that parse request responce
# def get


# TODO: write function download wallpapers html page
# def get_page_html(url) -> BeautifulSoup:
#     wallpapers_page = requests.get(url)
#     # TODO add check correctness month_year (not here)
#     try:
#         wallpapers_page.raise_for_status()
#         page_html = BeautifulSoup(wallpapers_page.text, "html.parser")
#         return page_html
#     except requests.HTTPError:
#         # TODO add log here
#         # TODO think about it
#         print("Can't download page html")
#         raise SystemExit


def is_good_response(response: Response) -> bool:
    # """
    # Returns True if the response seems to be HTML, False otherwise.
    # """
    content_type = response.headers.get('Content-Type').lower()
    return (
        response.status_code == 200 and
        content_type is not None and
        content_type.find('html') > -1)


def get_page_html(url) -> BeautifulSoup:
    try:
        with closing(requests.get(url)) as response:
            # response = requests.get(url)
            if is_good_response(response):
                page_html = BeautifulSoup(response.text, "html.parser")
                return page_html
            print("Response is not good")
            raise SystemExit
    except requests.exceptions.RequestException:
        # TODO add log here
        # TODO think about it
        print("Can't download page html")
        raise SystemExit


# TODO write the function checking the correctness of html


# TODO write func that find url next page
def find_next_page_url(page_html: BeautifulSoup) -> str:
    next_page_url_tag = page_html.find(
        lambda tag:
        tag.name == "a" and
        tag.parent.name == "li" and
        tag.parent.get("class") and
        "pagination__next" in tag.parent.get("class")
    )

    try:
        return next_page_url_tag.get("href")
    except AttributeError:
        # TODO add about this in log
        print("Can't find next page url. Pages is end")
        raise SystemExit


# TODO write func that find wallpapers page url
def find_wallpapers_page_url(
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


# TODO write func that find wallpaper url
def find_wallpaper_urls(
    page_html: BeautifulSoup,
    title: str,
) -> Union[list, None]:
    wallpaper_urls_tags = page_html.find_all(
        lambda tag:
        tag.name == 'a' and
        tag.get("title") == title
    )

    if wallpaper_urls_tags:
        return [url_tag.get("href") for url_tag in wallpaper_urls_tags]


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


# TODO write function convert month-year to url
def get_wallpapers_page_url(month_year: str) -> str:
    month, year = format_month_year(month_year)

    base_url = "https://smashingmagazine.com"
    wallpapers_url = "/category/wallpapers/"

    page_html = get_page_html(f"{base_url}{wallpapers_url}")

    while True:
        wallpapers_page_url = find_wallpapers_page_url(page_html, month, year)
        if wallpapers_page_url is not None:
            return f"{base_url}{wallpapers_page_url}"

        next_page_url = find_next_page_url(page_html)

        page_html = get_page_html(f"{base_url}{next_page_url}")
        # time.sleep(1)  # this so that we are not banned


# TODO write a function that gets wallpapers names
def get_wallpaper_names(page_html: BeautifulSoup) -> list:
    name_tags = page_html.find_all(
        lambda tag:
        tag.name == "h3" and
        tag.get("id") and
        tag.get("id") != "Join In Next Month!"
    )

    if name_tags:
        return [tag.text.strip() for tag in name_tags]

    # TODO write in log if wallpapers_names don't exist
    print("Wallpapers not found")
    raise SystemExit


# TODO write a function that gets wallpapers urls
def find_wallpapers_urls(
    page_html: BeautifulSoup,
    wallpaper_names: list,
    resolution: str,
) -> dict:
    wallpapers_urls = {}

    for wallpaper_name in wallpaper_names:
        title = f"{wallpaper_name} - {resolution}"
        wallpaper_urls = find_wallpaper_urls(page_html, title)

        if wallpaper_urls:
            for wallpaper_url in wallpaper_urls:
                name = wallpaper_url.split("/")[-1]
                wallpapers_urls[name] = wallpaper_url
        else:
            # TODO write about it in log
            # url for wallpaper_name in resolution not found
            pass
    return wallpapers_urls


# TODO write function which parsed wallpapers page html
# and return dict of links
def get_wallpapers_urls(
    month_year: str,
    resolution: str = '1920x1080',
) -> dict:  # TODO think about it
    wallpapers_page_url = get_wallpapers_page_url(month_year)

    page_html = get_page_html(wallpapers_page_url)

    wallpaper_names = get_wallpaper_names(page_html)

    wallpapers_urls = find_wallpapers_urls(
        page_html,
        wallpaper_names,
        resolution,
    )
    if wallpapers_urls:
        return wallpapers_urls

    # TODO add this in log
    print("Wallpapers urls not found")
    raise SystemExit


print(get_wallpapers_urls("04-2020"))

# TODO write func that download wallpapers

# TODO write func that write wallpaper in file
