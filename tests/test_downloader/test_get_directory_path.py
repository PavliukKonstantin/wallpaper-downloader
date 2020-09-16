import os

from wallpaper_downloader.downloader import WallpaperDownloader


def test_directory_path_with_calendar():
    """
    Test '_get_directory_path' method of WallpaperDownloader class.

    Method is tested for the directory with calendar.
    """
    downloader = WallpaperDownloader("08-2020")
    directory_path = downloader._get_directory_path(with_calendar=True)
    exist_directory_path = os.path.join(
        downloader.destination_directory_path,
        "august-2020 (with-calendar)",
    )
    assert directory_path == exist_directory_path


def test_directory_path_without_calendar():
    """
    Test '_get_directory_path' method of WallpaperDownloader class.

    Method is tested for the directory without calendar.
    """
    downloader = WallpaperDownloader("08-2020")
    directory_path = downloader._get_directory_path(with_calendar=False)
    exist_directory_path = os.path.join(
        downloader.destination_directory_path,
        "august-2020 (without-calendar)",
    )
    assert directory_path == exist_directory_path
