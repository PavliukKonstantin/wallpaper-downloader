import os

from wallpaper_downloader.downloader import WallpaperDownloader


def test_with_good_arguments(
    get_wallpapers_filenames,
    get_temp_directory_path,
    create_delete_temp_directory,
):
    """
    Test 'download_wallpapers' method of WallpaperDownloader class.

    Method is tested with the good parameters and
    checks the actual download of the files.

    Args:
        get_wallpapers_filenames (Fixture): fixture that return tuple
            of lists with wallpapers filenames.
        get_temp_directory_path (Fixture): fixture that return the absolute
            path to the temporary directory.
        create_delete_temp_directory (Fixture): fixture that create temporary
            directory before the test and delete after the test.
    """
    expected_files_names = get_wallpapers_filenames
    expected_filenames_with_calendar = expected_files_names[0]
    expected_filenames_without_calendar = expected_files_names[1]

    main_directory_path = get_temp_directory_path
    directory_path_to_wallpapers_with_calendar = os.path.join(
        main_directory_path,
        "july-2020 (with-calendar)",
    )
    directory_path_to_wallpapers_without_calendar = os.path.join(
        main_directory_path,
        "july-2020 (without-calendar)",
    )

    downloader = WallpaperDownloader(
        "07-2020",
        destination_directory_path=main_directory_path,
    )

    downloader.download_wallpapers()

    filenames_with_calendar = os.listdir(
        directory_path_to_wallpapers_with_calendar,
    ).sort()
    filenames_without_calendar = os.listdir(
        directory_path_to_wallpapers_without_calendar,
    ).sort()

    assert expected_filenames_with_calendar == filenames_with_calendar
    assert expected_filenames_without_calendar == filenames_without_calendar
