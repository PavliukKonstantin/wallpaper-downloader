# -*- coding: utf-8 -*-

import os

from wallpaper_downloader.downloader import WallpaperDownloader


def test_non_exist_directory(get_temp_directory_path, delete_temp_directory):
    """
    Test '_create_directory' method of WallpaperDownloader class.

    Method is tested with the non exist directory.

    Args:
        get_temp_directory_path (Fixture): fixture that return the absolute
            path to the temporary directory.
        delete_temp_directory (Fixture): fixture that deletes the temporary
            directory after the test.
    """
    test_directory_path = get_temp_directory_path
    downloader = WallpaperDownloader("07-2020")
    downloader._create_directory(test_directory_path)
    assert os.path.isdir(test_directory_path)


def test_exist_directory(
    get_temp_directory_path,
    create_delete_temp_directory,
):
    """
    Test '_create_directory' method of WallpaperDownloader class.

    Method is tested with the exist directory.

    Args:
        get_temp_directory_path (Fixture): fixture that return the absolute
            path to the temporary directory.
        create_delete_temp_directory (Fixture): fixture that create temporary
            directory before the test and delete after the test.
    """
    test_directory_path = get_temp_directory_path
    downloader = WallpaperDownloader("07-2020")
    downloader._create_directory(test_directory_path)
    assert os.path.isdir(test_directory_path)
