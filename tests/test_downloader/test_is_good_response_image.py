# -*- coding: utf-8 -*-

import pytest

from wallpaper_downloader.downloader import WallpaperDownloader


@pytest.mark.asyncio
async def test_good_response(get_async_response_from_url):
    """
    Test '_is_good_response' method of WallpaperDownloader class.

    Method is tested with the good response.

    Args:
        get_async_response_from_url (Fixture): fixture that return
            the response of aiohttp.ClientSession().get(page_url).
    """
    downloader = WallpaperDownloader("07-2020")
    response = await get_async_response_from_url(
        "http://files.smashingmagazine.com/wallpapers/july-17/"
        "summer-cannonball/cal/july-17-summer-cannonball-cal-320x480.png"
    )
    result = downloader._is_good_response(response)
    assert result is True


@pytest.mark.asyncio
async def test_bad_response(get_async_response_from_url):
    """
    Test '_is_good_response' method of WallpaperDownloader class.

    Method is tested with the bad response.

    Args:
        get_async_response_from_url (Fixture): fixture that return
            the response of aiohttp.ClientSession().get(page_url).
    """
    downloader = WallpaperDownloader("07-2020")
    response = await get_async_response_from_url(
        "https://www.smashingmagazine.com/category/wallpaper/",
    )
    result = downloader._is_good_response(response)
    assert result is False


@pytest.mark.asyncio
async def test_response_with_non_image_content(get_async_response_from_url):
    """
    Test '_is_good_response' method of WallpaperDownloader class.

    Method testing with the good response to not HTML content.

    Args:
        get_async_response_from_url (Fixture): fixture that return
            the response of aiohttp.ClientSession().get(page_url).
    """
    downloader = WallpaperDownloader("07-2020")
    response = await get_async_response_from_url(
        "https://www.smashingmagazine.com/category/wallpapers/",
    )
    result = downloader._is_good_response(response)
    assert result is False
