from time import sleep
import threading
import os
import re
import logging
import logging.config

from requests import Session

import settings


logging.config.dictConfig(settings.LOG_CONFIG)
log = logging.getLogger(settings.NAME_LOGGER)


def run():
    log.info(f"start pars {settings.NAME_PARSER}")
    check_file()
    p2 = threading.Thread(target=name_songs_from_steam)
    p2.start()
    p2.join()


def clean_name(name):
    name = name.decode()
    name = re.findall(r"'.*'", name)
    name = name[0][1:-1]
    return name


def name_songs_from_steam():
    session = Session()
    new_song = None
    try:
        while True:
            sleep(settings.CHECK_TIMEOUT)
            """отсылка метатады для того чтобы сервер знал что я могу читать метаданные"""
            connection = session.get(
                settings.SOURCE_LINK, headers={"Icy-MetaData": "1"}, stream=True
            )
            bytes_between_metadata = int(
                connection.headers["icy-metaint"]
            )  # сколько данных между метаданными
            stream = connection.raw
            str_data = stream.read(
                bytes_between_metadata
            )  # Разово получить байты сама песня

            meta_byte = stream.read(
                1
            )  # получение 1-ого байта до песни где то здесь название

            meta_length = ord(meta_byte) * 16  # перевести в байты длинна байтов
            meta_data = stream.read(meta_length)
            name = clean_name(meta_data)

            if name != new_song:
                songs = check_songs(name)
                if not name in settings.EXECUTE_NAMES and not name in songs:
                    log.info(f"name {name} new_song - {new_song}")
                    save_song(name)

    except Exception as e:
        log.error(f"error find name - {e}")
    finally:
        session.close()


def check_file():
    if not os.path.exists(settings.FILE_SONGS_NAMES):
        with open(settings.FILE_SONGS_NAMES, "w"):
            ...


def save_song(name, new_name, is_append=True):
    name = clean_song(name)
    log.info(f"save song {name}")
    if is_append:
        is_append = "a"
    else:
        is_append = "w"
    if new_name:
        with open(f"{settings.FILE_SONGS_NAMES[:-9]}{new_name}", "a") as file:
            file.write(f"{name}\n")
    else:
        with open(settings.FILE_SONGS_NAMES, is_append) as file:
            file.write(f"{name}\n")


def clean_row_songs(li):
    li = [i.strip() for i in li]
    return li


def clean_song(name):
    return name.strip()


def get_songs():
    with open(settings.FILE_SONGS_NAMES, "r") as file:
        songs = file.readlines()
    return songs


def clean_file():
    songs = get_songs()
    songs = [f"{song.strip()}\n" for song in songs]
    st = set(songs)
    with open(settings.FILE_SONGS_NAMES, "w") as file:
        file.writelines(st)


if __name__ == "__main__":
    run()
    # print(check_songs())
    # clean_file()
