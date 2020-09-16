import os
import aiohttp
import pytest

from wallpaper_downloader.downloader import WallpaperDownloader


@pytest.mark.asyncio
async def test_good_wallpaper_url(
    get_wallpaper_path,
    create_delete_temp_directory,
):
    """Test '_download_wallpaper' method of WallpaperDownloader class.

    Method is tested with the URL on which a wallpaper exists.

    Args:
        get_wallpaper_path (Fixture): fixture that return the absolute
            path to the wallpaper.
        create_delete_temp_directory (Fixture): fixture that create temporary
            directory before the test and delete after the test.
    """
    downloader = WallpaperDownloader("07-2020")
    wallpaper_url = (
        "http://files.smashingmagazine.com/wallpapers/july-20/"
        "birdie-july/cal/july-20-birdie-july-cal-1920x1080.png"
    )
    wallpaper_filename = "july-20-birdie-july-cal-1920x1080.png"
    wallpaper_path = get_wallpaper_path(wallpaper_filename)

    async with aiohttp.ClientSession() as session:
        await downloader._download_wallpaper(
            wallpaper_path,
            wallpaper_url,
            session,
        )
    assert os.path.isfile(wallpaper_path) is True


@pytest.mark.asyncio
async def test_bad_wallpaper_url(
    get_wallpaper_path,
    create_delete_temp_directory,
):
    """
    Test '_download_wallpaper' method of WallpaperDownloader class.

    Method is tested with the URL on which a wallpaper non exists.

    Args:
        get_wallpaper_path (Fixture): fixture that return the absolute
            path to the wallpaper.
        create_delete_temp_directory (Fixture): fixture that create temporary
            directory before the test and delete after the test.
    """
    downloader = WallpaperDownloader("07-2020")
    wallpaper_url = "https://www.smashingmagazine.com/category/wallpapers/"
    wallpaper_filename = "july-20-birdie-july-cal-1920x1080.png"
    wallpaper_path = get_wallpaper_path(wallpaper_filename)

    async with aiohttp.ClientSession() as session:
        await downloader._download_wallpaper(
            wallpaper_path,
            wallpaper_url,
            session,
        )
    assert os.path.isfile(wallpaper_path) is False
