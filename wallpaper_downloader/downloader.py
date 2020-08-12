# -*- coding: utf-8 -*-

import asyncio
import logging
import os

import aiohttp
import click

from wallpaper_downloader import site_parser


class WallpaperDownloader:
    """Download wallpapers from 'smashingmagazine.com'."""

    def __init__(
        self,
        month_year: str,
        resolution: str = '1920x1080',
        destination_directory_path: str = "smashingmagazine",
    ) -> None:
        """Initialize attributes of the class and the console logger.

        Args:
            month_year (str): month and year of downloadable wallpapers
                in format 'mm-yyyy'.
            resolution (str, optional): resolution of downloadable wallpapers.
                Defaults to '1920x1080'.
            destination_directory_path (str, optional): the directory where
                wallpapers will be downloaded.
                Defaults to './smashingmagazine'.
        """
        self.month_year = month_year
        self.resolution = resolution
        self.destination_directory_path = os.path.abspath(
            destination_directory_path,
        )

        # Init console logger.
        self.c_logger = logging.getLogger(__name__)
        self.c_logger.setLevel(logging.INFO)
        self.c_log = logging.StreamHandler()
        self.c_formatter = logging.Formatter("%(levelname)s: %(message)s")
        self.c_log.setFormatter(self.c_formatter)
        self.c_logger.addHandler(self.c_log)

    def _get_directory_path(self, with_calendar: bool) -> str:
        """Get the path to the directory where wallpapers will be downloaded.

        Args:
            with_calendar (bool): defines the name of the directory.

        Returns:
            str: absolute path of directory.
        """
        with_without = "with" if with_calendar else "without"
        month, year = site_parser.format_month_year(self.month_year)
        return os.path.join(
            self.destination_directory_path,
            f"{month}-{year} ({with_without}-calendar)",
        )

    def _get_wallpaper_path(self, wallpaper_name: str) -> str:
        """Get the absolute path where the wallpaper will be created.

        Args:
            wallpaper_name (str): wallpaper name.

        Returns:
            str: absolute wallpaper path.
        """
        wallpaper_with_calendar = wallpaper_name.find("-cal-") > -1
        return os.path.join(
            self._get_directory_path(wallpaper_with_calendar),
            wallpaper_name,
        )

    def _create_directory(self, directory_path: str) -> None:
        """Create the directory.

        Args:
            directory_path (str): absolute directory path.

        Raises:
            SystemExit: if can't create a directory or
                can't create a file in a directory.
        """
        if not os.path.isdir(directory_path):
            try:
                os.mkdir(directory_path)
            except OSError:
                self.c_logger.error(
                    f"Can't create directory with path - '{directory_path}'.",
                )
                raise SystemExit
        tmp_file_path = os.path.join(directory_path, "tmp_file.txt")
        try:
            tmp_file = open(tmp_file_path, "w")
            tmp_file.close()
            os.remove(tmp_file_path)
        except OSError:
            self.c_logger.error(
                f"Can't write in directory with path - '{directory_path}'.",
            )
            raise SystemExit

    def _create_directories(self) -> None:
        """Create directories where wallpapers will be downloaded."""
        directory_to_wallpapers_with_calendar = self._get_directory_path(
            with_calendar=True,
        )
        directory_to_wallpapers_without_calendar = self._get_directory_path(
            with_calendar=False,
        )
        directories_paths = (
            self.destination_directory_path,
            directory_to_wallpapers_with_calendar,
            directory_to_wallpapers_without_calendar,
        )

        for directory_path in directories_paths:
            self._create_directory(directory_path)

    def _write_wallpaper(self, wallpaper_data: bytes, wallpaper_path: str):
        """Write wallpaper in a file.

        Args:
            wallpaper_data (bytes): the raw wallpaper data.
            wallpaper_path (str): the absolute path of the directory where
                the image will be created.
        """
        with open(wallpaper_path, "wb") as wallpaper:
            wallpaper.write(wallpaper_data)

    def _is_good_response(self, response: aiohttp.ClientSession) -> bool:
        """Check the correctness of the response.

        Args:
            response (aiohttp.ClientSession): response of
                aiohttp.ClientSession.get(url).

        Returns:
            bool: True if response is good.
        """
        content_type = response.headers.get('Content-Type').lower()
        response_status_ok = 200
        return (
            response.status == response_status_ok and
            content_type is not None and
            content_type.find("image") > -1
        )

    async def _download_wallpaper(
        self,
        wallpaper_path: str,
        wallpaper_url: str,
        session: aiohttp.ClientSession,
    ) -> None:
        """Download one wallpaper.

        Args:
            wallpaper_path (str): the absolute path of the directory where
                the image will be created.
            wallpaper_url (str): URL for downloading the image.
        """
        async with session.get(wallpaper_url) as response:
            if self._is_good_response(response):
                wallpaper_data = await response.read()
                self._write_wallpaper(wallpaper_data, wallpaper_path)
            else:
                self.c_logger.error(
                    f"Response for '{wallpaper_url}' is wrong. "
                    "Wallpaper not loaded."
                )

    async def _downloader_event_loop(self, wallpapers_urls: dict) -> None:
        """Event loop for async download wallpapers.

        Args:
            wallpapers_urls (dict): wallpapers urls in
                '{wallpaper_name: wallpaper_url}' format.
        """
        tasks = []
        connections_limit = 20
        connector = aiohttp.TCPConnector(limit=connections_limit)

        async with aiohttp.ClientSession(connector=connector) as session:
            for wallpaper_name, wallpaper_url in wallpapers_urls.items():
                wallpaper_path = self._get_wallpaper_path(wallpaper_name)
                task = asyncio.create_task(
                    self._download_wallpaper(
                        wallpaper_path,
                        wallpaper_url,
                        session,
                    ),
                )
                tasks.append(task)

            await asyncio.gather(*tasks)

    def download_wallpapers(self) -> None:
        """Download all wallpapers with initialized parameters."""
        wallpapers_urls = site_parser.get_wallpapers_urls(
            self.month_year,
            self.resolution,
        )

        self._create_directories()

        self.c_logger.info("Downloading of wallpapers is started.")
        asyncio.run(self._downloader_event_loop(wallpapers_urls))
        self.c_logger.info("Downloading of wallpapers is finished.")


if __name__ == "__main__":
    @click.command()
    @click.option(
        "--month-year",
        type=str,
        required=True,
        help="Month and year of downloadable wallpapers",
    )
    @click.option(
        "--resolution",
        type=str,
        default="1920x1080",
        show_default=True,
        help="Resolution of downloadable wallpapers",
    )
    @click.option(
        "--dest_path",
        type=str,
        default="smashingmagazine",
        show_default=True,
        help="Destination path for downloadable wallpapers",
    )
    def download_wallpapers(
        month_year,
        resolution,
        dest_path,
    ) -> None:
        """CLI for download wallpaper from smashingmagazine.com."""
        downloader = WallpaperDownloader(
            month_year,
            resolution,
            dest_path,
        )
        downloader.download_wallpapers()

    download_wallpapers()
