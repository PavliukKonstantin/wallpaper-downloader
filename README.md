# Smashing Wallpaper Downloader

Еще одна проба пера на найденном в интернете тестовом задании.

Задание:

Есть прекрасный сайт Smashing Magazine, который каждый месяц выкладывает отличные обои для десктопа. Заходить каждый месяц и проверять, что там нового дело не благородное, поэтому давайте попробуем автоматизировать эту задачу. Требуется написать cli утилиту, которая будет качать все обои в требуемом разрешение за указанный месяц-год в текущую директорию пользователя. Вот [тут](https://www.smashingmagazine.com/category/wallpapers) находятся все обои, а [здесь](https://www.smashingmagazine.com/2017/04/desktop-wallpaper-calendars-may-2017/) находятся обои за май 2017.

Условия:

- Python 3.5+
- Любые сторонние библиотеки
- PEP8
- Если останется время, то можете покрыть её тестами с помощью py.test.


### Инструкция по запуску:

1) Для установки виртуального окружения и зависимостей выполнить команду:

        $ poetry install

2) Для загрузки изображений написан CLI. Ниже представлен вывод команды **--help**.

        $ python downloader.py --help

        Usage: downloader.py [OPTIONS]

        CLI for download wallpaper from smashingmagazine.com.

        Options:
        --month-year TEXT  Month and year of downloadable wallpapers
                           [required]

        --resolution TEXT  Resolution of downloadable wallpapers
                           [default: 1920x1080]

        --dest_path TEXT   Destination path for downloadable wallpapers  
                           [default: smashingmagazine]

        --help             Show this message and exit.

3) Параметр **--month-year** является обязательным и определяет за какой месяц и год будут скачаны изображения. Месяц и год необходимо вводить в формате **mm-yyyy**.  
Например, чтобы скачать изображения за август 2020 года необходимо ввести команду:

        $ python downloader.py --month-year=08-2020

    Параметр **--resolution** является необязательным. Он определяет разрешение скачиваемых изображений. Вводится в формате двух чисел разделенных латинской буквой **x**.  
    По умолчанию изображения скачиваются с разрешением 1920x1080.  
    Например, чтобы скачать изображения за август 2020 в разрешении 2560x1440 необходимо ввести команду:

        $ python downloader.py --month-year=08-2020 --resolution=2560x1440

    Параметр **--destination_directory_path** является необязательным. Он определяет путь к директории в которую будут загружены изображения. Путь может быть введен как в форме абсолютного так и относительного пути.  
    По умолчанию изображения скачиваются в директорию **./smashingmagazine/**.  
    Например, чтобы скачать изображения за август 2020 года в директорию **/home/username/wallpapers/** необходимо ввести команду:

        $ python downloader.py --month-year=08-2020 --dest_path=/home/username/wallpapers/

1) Тесты написаны на **pytest**. Для запуска всех тестов необходимо выполнить команду:

         $ pytest
