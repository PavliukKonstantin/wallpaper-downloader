import asyncio
import logging
import os

import aiohttp
import click

from wallpaper_downloader import site_parser


class WallpaperDownloader:
    def __init__(
        self,
        month_year: str,
        resolution: str = '1920x1080',
        destination_folder_path: str = "smashingmagazine",
    ) -> None:
        self.month_year = month_year
        self.resolution = resolution
        self.destination_folder_path = os.path.abspath(destination_folder_path)

        # Init console logger.
        self.c_logger = logging.getLogger(__name__)
        self.c_logger.setLevel(logging.INFO)
        self.c_log = logging.StreamHandler()
        self.c_formatter = logging.Formatter("%(levelname)s: %(message)s")
        self.c_log.setFormatter(self.c_formatter)
        self.c_logger.addHandler(self.c_log)

    def _get_folder_path(self, with_calendar: bool) -> str:
        with_without = "with" if with_calendar else "without"
        month, year = site_parser.format_month_year(self.month_year)
        return os.path.join(
            self.destination_folder_path,
            f"{month}-{year} ({with_without}-calendar)",
        )

    def _get_wallpaper_path(self, wallpaper_name: str) -> str:
        wallpaper_with_calendar = wallpaper_name.find("-cal-") > -1
        return os.path.join(
            self._get_folder_path(
                wallpaper_with_calendar,
            ),
            wallpaper_name,
        )

    # TODO write func that create 1 folder
    def _create_folder(self, folder_path: str) -> None:
        if not os.path.isdir(folder_path):
            try:
                os.mkdir(folder_path)
            except OSError:
                self.c_logger.error(
                    f"Can't create folder with path - '{folder_path}'.",
                )
                raise SystemExit
        tmp_file_path = os.path.join(folder_path, "tmp_file.txt")
        try:
            tmp_file = open(tmp_file_path, "w")
            tmp_file.close()
            os.remove(tmp_file_path)
        except OSError:
            self.c_logger.error(
                f"Can't write in folder with path - '{folder_path}'.",
            )
            raise SystemExit

    # TODO write func that create folders for wallpapers
    def _create_folders(self) -> None:
        # """Check the directory to which the file is copied.

        # Check existence of destination directory and check write permission.
        # If the directory doesn't exist, an attempt is made to create it.
        # """
        folder_to_wallpapers_with_calendar = self._get_folder_path(
            with_calendar=True,
        )
        folder_to_wallpapers_without_calendar = self._get_folder_path(
            with_calendar=False,
        )
        folders_paths = (
            self.destination_folder_path,
            folder_to_wallpapers_with_calendar,
            folder_to_wallpapers_without_calendar,
        )

        for folder_path in folders_paths:
            self._create_folder(folder_path)

    # TODO write func that write wallpaper in file
    def _write_wallpaper(self, wallpaper_data: bytes, wallpaper_path: str):
        with open(wallpaper_path, "wb") as wallpaper:
            wallpaper.write(wallpaper_data)

    # TODO write the function checking the correctness of response
    def _is_good_response(self, response: aiohttp.ClientSession) -> bool:
        """Return True if the response seems to be 'wallpaper'."""
        content_type = response.headers.get('Content-Type').lower()
        response_status_ok = 200
        return (
            response.status == response_status_ok and
            content_type is not None and
            content_type.find("image") > -1
        )

    # TODO write func that download one wallpaper
    async def _download_wallpaper(
        self,
        wallpaper_path: str,
        wallpaper_url: str,
        session: aiohttp.ClientSession,
    ) -> None:
        async with session.get(wallpaper_url) as response:
            if self._is_good_response(response):
                wallpaper_data = await response.read()
                self._write_wallpaper(wallpaper_data, wallpaper_path)
            else:
                self.c_logger.error(
                    f"Response for '{wallpaper_url}' is wrong. "
                    "Wallpaper not loaded."
                )

    # TODO write func that download wallpapers
    async def _downloader_event_loop(self, wallpapers_urls: dict) -> None:
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
        wallpapers_urls = site_parser.get_wallpapers_urls(
            self.month_year,
            self.resolution,
        )

        self._create_folders()

        self.c_logger.info("Download wallpapers started.")
        asyncio.run(self._downloader_event_loop(wallpapers_urls))
        self.c_logger.info("Download wallpapers finished.")


if __name__ == "__main__":
    @click.command()
    @click.option(
        "--month-year",
        type=str,
        required=True,
        help="Month and year downloadable wallpapers",
    )
    @click.option(
        "--resolution",
        type=str,
        default="1920x1080",
        show_default=True,
        help="Resolution of downloadable wallpapers",
    )
    @click.option(
        "--destination_folder_path",
        type=str,
        default="smashingmagazine",
        show_default=True,
        help="Download wallpapers destination path",
    )
    def download_wallpapers(
        month_year,
        resolution,
        destination_folder_path,
    ):
        downloader = WallpaperDownloader(
            month_year,
            resolution,
            destination_folder_path)
        downloader.download_wallpapers()

    download_wallpapers()
