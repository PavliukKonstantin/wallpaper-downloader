# -*- coding: utf-8 -*-

import json
import os
import shutil
from contextlib import closing

import aiohttp
import pytest
import requests
from bs4 import BeautifulSoup
from requests.models import Response


@pytest.fixture()
def get_page_html_from_file():
    """
    Fixture. Get the HTML from the file.

    Name of the directory is constant. Only file name can be specified.

    Args:
        page_file_name (str): the name of the file that
            contains the HTML for parsing.

    Returns:
        BeautifulSoup: HTML of the page.
    """
    def inner(page_file_name: str) -> BeautifulSoup:
        page_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "files_for_tests",
            page_file_name,
        )
        with open(page_path) as page:
            return BeautifulSoup(page.read(), "html.parser")
    return inner


@pytest.fixture()
def get_sync_response_from_url():
    """
    Fixture. Get response for URL.

    Args:
        page_url (str): the URL of the page from which
            the response will be received.

    Returns:
        Response: response of requests.get(page_url).
    """
    def inner(page_url: str) -> Response:
        with closing(requests.get(page_url)) as response:
            return response
    return inner


@pytest.fixture()
def get_wallpapers_urls_from_file() -> dict:
    """
    Fixture. Get URLs of the wallpapers from file.

    Name of the directory and the filename are constants.

    Returns:
        dict: URLs of wallpapers in format
            {'wallpaper_filename': 'wallpaper_url'}.
    """
    file_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "files_for_tests",
        "wallpapers_urls.json",
    )
    with open(file_path) as wallpapers_urls_file:
        return json.load(wallpapers_urls_file)


@pytest.fixture()
def get_wallpapers_names_from_file() -> dict:
    """
    Fixture. Get names of wallpapers from file.

    Name of the directory and filename are constants.

    Returns:
        dict: names of wallpapers in format ['name1', 'name2',...].
    """
    file_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "files_for_tests",
        "wallpapers_names.json",
    )
    with open(file_path) as wallpapers_names_file:
        return json.load(wallpapers_names_file).get("wallpapers_names")


@pytest.fixture()
def get_wallpapers_filenames(get_wallpapers_urls_from_file) -> tuple:
    """
    Fixture. Get names of wallpapers files.

    Args:
        get_wallpapers_urls_from_file (Fixture): fixture that return
            names and URLs of the wallpapers as a dict.

    Returns:
        tuple: tuple of lists with filenames of wallpapers.
            One list contains filenames of wallpapers with calendar.
            Second list contains filenames of wallpapers without calendar.
    """
    wallpapers_files_names = get_wallpapers_urls_from_file.keys()
    with_calendar_wallpapers_files_names = []
    without_calendar_wallpapers_files_names = []
    for wallapper_file_name in wallpapers_files_names:
        if "-cal-" in wallapper_file_name:
            with_calendar_wallpapers_files_names.append(wallapper_file_name)
        else:
            without_calendar_wallpapers_files_names.append(wallapper_file_name)
    return (
        with_calendar_wallpapers_files_names.sort(),
        without_calendar_wallpapers_files_names.sort(),
    )


@pytest.fixture()
def get_async_response_from_url():
    """
    Fixture. Get response for URL.

    Args:
        page_url (str): the URL of the page from which
            the response will be received.

    Returns:
        Response: response of aiohttp.ClientSession().get(page_url).
    """
    async def inner(page_url: str):
        async with aiohttp.ClientSession().get(page_url) as response:
            return response
    return inner


@pytest.fixture()
def get_temp_directory_path():
    """
    Fixture. Get the path of the temporary directory.

    The directory is used as temporary storage of files for tests.

    Returns:
        str: absolute path to temporary directory.
    """
    return os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "test_downloader",
        "temp_directory",
    )


@pytest.fixture()
def get_wallpaper_path(get_temp_directory_path):
    """
    Fixture. Get the path to the wallpaper.

    Args:
        get_temp_directory_path (Fixture): fixture that return the absolute
            path to the temporary directory.
        wallpaper_filename (str): wallpaper filename.

    Returns:
        str: absolute path to wallpaper.
    """
    def inner(wallpaper_filename):
        return os.path.join(get_temp_directory_path, wallpaper_filename)
    return inner


@pytest.fixture()
def create_delete_temp_directory(get_temp_directory_path):
    """
    Fixture. Create temporary directory before test and delete after test.

    Args:
        get_temp_directory_path (Fixture): fixture that return the absolute
            path to the temporary directory.
    """
    temp_directory_path = get_temp_directory_path
    if not os.path.isdir(temp_directory_path):
        os.mkdir(temp_directory_path)

    yield

    shutil.rmtree(temp_directory_path)


@pytest.fixture()
def delete_temp_directory(get_temp_directory_path):
    """
    Fixture. Delete temporary directory after test.

    Args:
        get_temp_directory_path (Fixture): fixture that return the absolute
            path to the temporary directory.
    """
    temp_directory_path = get_temp_directory_path

    yield

    shutil.rmtree(temp_directory_path)
