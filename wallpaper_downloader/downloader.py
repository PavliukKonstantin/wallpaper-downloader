import asyncio
import os
from datetime import datetime

import aiohttp

from wallpaper_downloader import site_parser


def wallpapers_downloader(
    month_year,
    resolution='1920x1080',
    folder_to_load_into="smashingmagazine",
) -> None:
    images_urls = site_parser.get_images_urls(month_year, resolution)

    _create_folders(folder_to_load_into, month_year)

    asyncio.run(_download_images(images_urls, folder_to_load_into, month_year))


def _get_folder_path(
    main_folder_path: str,
    month_year: str,
    with_calendar: bool,
) -> str:
    with_without = "with" if with_calendar else "without"
    month, year = site_parser.format_month_year(month_year)
    return os.path.join(
        main_folder_path,
        f"{month}-{year} ({with_without}-calendar)",
    )


def _get_image_path(
    image_name: str,
    folder_to_load_into: str,
    month_year: str,
) -> str:
    image_with_calendar = image_name.find("-cal-") > -1
    return os.path.join(
        _get_folder_path(
            folder_to_load_into,
            month_year,
            image_with_calendar,
        ),
        image_name,
    )


# TODO write func that create 1 folder
def _create_folder(folder_path: str) -> None:
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


# TODO write func that create folders for images
def _create_folders(main_folder_path: str, month_year: str) -> None:
    # """Check the directory to which the file is copied.

    # Check existence of destination directory and check write permission.
    # If the directory doesn't exist, an attempt is made to create it.
    # """
    abs_main_folder_path = os.path.abspath(main_folder_path)
    folder_to_images_with_calendar = _get_folder_path(
        abs_main_folder_path,
        month_year,
        with_calendar=True,
    )
    folder_to_images_without_calendar = _get_folder_path(
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
        _create_folder(folder_path)


# TODO write func that write image in file
def _write_image(image_data, image_path):
    with open(image_path, "wb") as image:
        image.write(image_data)


# TODO write the function checking the correctness of response
def _is_good_response(
    response: aiohttp.ClientSession,
) -> bool:
    """Return True if the response seems to be 'image', False otherwise."""
    content_type = response.headers.get('Content-Type').lower()
    return (
        response.status == 200 and
        content_type is not None and
        content_type.find("image") > -1)


# TODO write func that download one image
async def _download_image(
    image_path: str,
    image_url: str,
    session: aiohttp.ClientSession,
) -> None:
    async with session.get(image_url) as response:
        if _is_good_response(response):
            image_data = await response.read()
            _write_image(image_data, image_path)
        # TODO else write about it in log


# TODO write func that download images
async def _download_images(
    images_urls: dict,
    folder_to_load_into: str,
    month_year: str,
) -> None:
    tasks = []
    connector = aiohttp.TCPConnector(limit=20)

    async with aiohttp.ClientSession(connector=connector) as session:
        for image_name, image_url in images_urls.items():
            image_path = _get_image_path(
                image_name,
                folder_to_load_into,
                month_year,
            )
            task = asyncio.create_task(
                _download_image(image_path, image_url, session),
            )
            tasks.append(task)

        await asyncio.gather(*tasks)


start = datetime.now()
wallpapers_downloader("06-2020")
print(datetime.now() - start)
