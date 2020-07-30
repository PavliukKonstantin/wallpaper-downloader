import asyncio
import os
from contextlib import closing
from datetime import datetime
from typing import Union

import aiohttp
import requests
from bs4 import BeautifulSoup
from requests.models import Response


# TODO write the function checking the correctness of response
def is_good_response(response: Response) -> bool:
    """Returns True if the response seems to be HTML, False otherwise."""
    content_type = response.headers.get('Content-Type').lower()
    return (
        response.status_code == 200 and
        content_type is not None and
        content_type.find('html') > -1)


# TODO write func get page html
def get_page_html(url: str) -> BeautifulSoup:
    try:
        with closing(requests.get(url)) as response:
            if is_good_response(response):
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
def find_next_page_url(page_html: BeautifulSoup) -> str:
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
def find_images_page_url(
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
def find_image_urls(
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
def get_images_page_url(month_year: str) -> str:
    month, year = format_month_year(month_year)

    base_url = "https://smashingmagazine.com"
    images_url = "/category/wallpapers/"

    page_html = get_page_html(f"{base_url}{images_url}")

    while True:
        images_page_url = find_images_page_url(page_html, month, year)
        if images_page_url is not None:
            return f"{base_url}{images_page_url}"

        next_page_url = find_next_page_url(page_html)

        page_html = get_page_html(f"{base_url}{next_page_url}")


# TODO write a function that gets images names
def get_image_names(page_html: BeautifulSoup) -> list:
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
def find_images_urls(
    page_html: BeautifulSoup,
    image_names: list,
    resolution: str,
) -> dict:
    images_urls = {}

    for image_name in image_names:
        title = f"{image_name} - {resolution}"
        image_urls = find_image_urls(page_html, title)

        if image_urls:
            for image_url in image_urls:
                name = image_url.split("/")[-1]
                images_urls[name] = image_url
        else:
            # TODO write about it in log
            # url for image_name in resolution not found
            pass
    return images_urls


# TODO write function which parsed images page html
# and return dict of links
def get_images_urls(
    month_year: str,
    resolution: str,
) -> dict:  # TODO think about it
    images_page_url = get_images_page_url(month_year)

    page_html = get_page_html(images_page_url)

    image_names = get_image_names(page_html)

    images_urls = find_images_urls(
        page_html,
        image_names,
        resolution,
    )
    if images_urls:
        return images_urls

    # TODO add this in log
    print("images urls not found")
    raise SystemExit


# print(get_images_urls("04-2020", "1920x1080"))
###############################################################################


def get_folder_path(
    main_folder_path: str,
    month_year: str,
    with_calendar: bool,
) -> str:
    with_without = "with" if with_calendar else "without"
    month, year = format_month_year(month_year)
    return os.path.join(
        main_folder_path,
        f"{month}-{year} ({with_without}-calendar)",
    )


# TODO write func that create 1 folder
def create_folder(folder_path: str) -> None:
    if not os.path.isdir(folder_path):
        try:
            os.mkdir(folder_path)
        except OSError:
            # TODO write in log about it
            raise SystemExit
    tmp_file_path = os.path.join(folder_path, "tmp_file.txt")
    try:
        tmp_file = open(tmp_file_path, "w")
        tmp_file.close()
        os.remove(tmp_file_path)
    except OSError:
        # TODO write in log about it
        raise SystemExit
    # TODO write in log that folder is ok. Or don't write. Think!!!


# TODO write func that create folders for images
def create_folders(main_folder_path: str, month_year: str) -> None:
    # """Check the directory to which the file is copied.

    # Check existence of destination directory and check write permission.
    # If the directory doesn't exist, an attempt is made to create it.
    # """
    abs_main_folder_path = os.path.abspath(main_folder_path)
    folder_to_images_with_calendar = get_folder_path(
        abs_main_folder_path,
        month_year,
        with_calendar=True,
    )
    folder_to_images_without_calendar = get_folder_path(
        abs_main_folder_path,
        month_year,
        with_calendar=False,
    )
    folders_paths = (
        abs_main_folder_path,
        folder_to_images_with_calendar,
        folder_to_images_without_calendar,
    )

    for folder_path in folders_paths:
        create_folder(folder_path)


# TODO write func that write image in file
def write_image(image_data, image_path):
    with open(image_path, "wb") as image:
        image.write(image_data)


# TODO write func that download one image
async def download_image(image_path, image_url, session):
    async with session.get(image_url) as response:
        image_data = await response.read()
        write_image(image_data, image_path)


# TODO write func that download images
async def download_images(images_urls, folder_to_load_into, month_year):
    tasks = []
    connector = aiohttp.TCPConnector(limit=20)

    async with aiohttp.ClientSession(connector=connector) as session:
        for image_name, image_url in images_urls.items():
            image_with_calendar = image_name.find("-cal-") > -1
            image_path = os.path.join(
                get_folder_path(
                    folder_to_load_into,
                    month_year,
                    image_with_calendar,
                ),
                image_name,
            )
            task = asyncio.create_task(
                download_image(image_path, image_url, session)
            )
            tasks.append(task)

        await asyncio.gather(*tasks)


def wallpapers_downloader(
    month_year,
    resolution='1920x1080',
    folder_to_load_into="smashingmagazine",
) -> None:
    images_urls = get_images_urls(month_year, resolution)

    create_folders(folder_to_load_into, month_year)

    asyncio.run(download_images(images_urls, folder_to_load_into, month_year))


start = datetime.now()
wallpapers_downloader("06-2019")
print(datetime.now() - start)
