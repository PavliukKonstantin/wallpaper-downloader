# -*- coding: utf-8 -*-

import os

from wallpaper_downloader.downloader import WallpaperDownloader


def test_wallpaper_path_with_calendar():
    """Test '_get_wallpaper_path' method of WallpaperDownloader class.

    Method is tested for the wallpaper with calendar.
    """
    downloader = WallpaperDownloader("07-2020")
    wallpaper_name = "july-20-birdie-july-cal-1920x1080.png"
    wallpaper_path = downloader._get_wallpaper_path(wallpaper_name)

    exist_wallpaper_path = os.path.join(
        downloader._get_directory_path(with_calendar=True),
        wallpaper_name,
    )
    assert wallpaper_path == exist_wallpaper_path


def test_wallpaper_path_without_calendar():
    """Test '_get_wallpaper_path' method of WallpaperDownloader class.

    Method is tested for the wallpaper without calendar.
    """
    downloader = WallpaperDownloader("07-2020")
    wallpaper_name = "july-20-birdie-july-nocal-1920x1080.png"
    wallpaper_path = downloader._get_wallpaper_path(wallpaper_name)

    exist_wallpaper_path = os.path.join(
        downloader._get_directory_path(with_calendar=False),
        wallpaper_name,
    )
    assert wallpaper_path == exist_wallpaper_path
