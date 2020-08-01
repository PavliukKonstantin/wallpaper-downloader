import asyncio
import logging
import os
from datetime import datetime

import aiohttp

from wallpaper_downloader import site_parser


class WallpaperDownloader():
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

    def download_images(self) -> None:
        images_urls = site_parser.get_images_urls(
            self.month_year,
            self.resolution,
        )

        self._create_folders()

        asyncio.run(self._downloader_event_loop(images_urls))

    def _get_folder_path(self, with_calendar: bool) -> str:
        with_without = "with" if with_calendar else "without"
        month, year = site_parser.format_month_year(self.month_year)
        return os.path.join(
            self.destination_folder_path,
            f"{month}-{year} ({with_without}-calendar)",
        )

    def _get_image_path(self, image_name: str) -> str:
        image_with_calendar = image_name.find("-cal-") > -1
        return os.path.join(
            self._get_folder_path(
                image_with_calendar,
            ),
            image_name,
        )

    # TODO write func that create 1 folder
    def _create_folder(self, folder_path: str) -> None:
        if not os.path.isdir(folder_path):
            try:
                os.mkdir(folder_path)
            except OSError:
                self.c_logger.error(
                    f"Can't create folder with path - '{folder_path}''",
                )
                raise SystemExit
        tmp_file_path = os.path.join(folder_path, "tmp_file.txt")
        try:
            tmp_file = open(tmp_file_path, "w")
            tmp_file.close()
            os.remove(tmp_file_path)
        except OSError:
            self.c_logger.error(
                f"Can't write in folder with path - '{folder_path}'",
            )
            raise SystemExit

    # TODO write func that create folders for images
    def _create_folders(self) -> None:
        # """Check the directory to which the file is copied.

        # Check existence of destination directory and check write permission.
        # If the directory doesn't exist, an attempt is made to create it.
        # """
        folder_to_images_with_calendar = self._get_folder_path(
            with_calendar=True,
        )
        folder_to_images_without_calendar = self._get_folder_path(
            with_calendar=False,
        )
        folders_paths = (
            self.destination_folder_path,
            folder_to_images_with_calendar,
            folder_to_images_without_calendar,
        )

        for folder_path in folders_paths:
            self._create_folder(folder_path)

    # TODO write func that write image in file
    def _write_image(self, image_data: bytes, image_path: str):
        with open(image_path, "wb") as image:
            image.write(image_data)

    # TODO write the function checking the correctness of response
    def _is_good_response(self, response: aiohttp.ClientSession) -> bool:
        """Return True if the response seems to be 'image', False otherwise."""
        content_type = response.headers.get('Content-Type').lower()
        response_status_ok = 200
        return (
            response.status == response_status_ok and
            content_type is not None and
            content_type.find("image") > -1
        )

    # TODO write func that download one image
    async def _download_image(
        self,
        image_path: str,
        image_url: str,
        session: aiohttp.ClientSession,
    ) -> None:
        async with session.get(image_url) as response:
            if self._is_good_response(response):
                image_data = await response.read()
                self._write_image(image_data, image_path)
            else:
                self.c_logger.error(
                    f"Response for '{image_url}' is wrong. Image not loaded",
                )

    # TODO write func that download images
    async def _downloader_event_loop(self, images_urls: dict) -> None:
        tasks = []
        connections_limit = 20
        connector = aiohttp.TCPConnector(limit=connections_limit)

        async with aiohttp.ClientSession(connector=connector) as session:
            for image_name, image_url in images_urls.items():
                image_path = self._get_image_path(
                    image_name,
                )
                task = asyncio.create_task(
                    self._download_image(image_path, image_url, session),
                )
                tasks.append(task)

            await asyncio.gather(*tasks)


start = datetime.now()
downloader = WallpaperDownloader("05-2020")
downloader.download_images()
print(datetime.now() - start)
