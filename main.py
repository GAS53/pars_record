from multiprocessing import Queue, Lock, Process
from time import sleep
import os
from requests import Session


class Parser(object):
    """main class for parsing."""
    def __init__(self):
        self.lock = Lock()
        self.q = Queue()
        # self.link = 'http://radio-srv1.11one.ru/record192k.mp3'
        self.link = 'http://radiorecord.hostingradio.ru/rr_main96.aacp'
        self.path_load_files = self.pather()

    def pather(self):
        current_dir = os.getcwd()
        files_path = current_dir+'/'+'songs_fiels/'
        if not os.path.exists(files_path):
            os.mkdir(files_path)
        return files_path

    def run(self):
        p2 = Process(target=self.checker_names, name='downloader')
        p2.start()
        p1 = Process(target=self.name_songs_from_steam, name='get_namer')
        p1.start()
        p1.join()

    def name_songs_from_steam(self):
        session = Session()
        new_song = None
        try:
            while True:
                sleep(1)
                '''# отсылка метатады для того чтобы сервер знал что я могу читать метаданные'''
                connection = session.get(self.link, headers={'Icy-MetaData': '1'}, stream=True)
                bytes_between_metadata = int(connection.headers['icy-metaint']) # сколько данных между метаданными
                stream = connection.raw
                str_data = stream.read(bytes_between_metadata) # Разово получить байты сама песня
                meta_byte = stream.read(1) # получение 1-ого байта до песни где то здесь название
                meta_length = ord(meta_byte) * 16 # перевести в байты длинна байтов
                meta_data = stream.read(meta_length)
                name = self.clean_name(meta_data)
                # print(f'name {name} new_song - {new_song}')
                if name != new_song:
                    print(f' new song {name}')
                    res_check = self.check_files(name)
                    if res_check == 'terminate':
                        self.q.put('terminate')
                    else:
                        self.q.put(name)
                new_song = name
        except Exception as e:
            print(f'error find name - {e}')
        finally:
            session.close()

    def clean_name(self, name):
        name = name.decode()
        li_exept = ['StreamTitle=', "'", ";", '"', "\0", '/', '(Record Mix)']
        for i in li_exept:
            name = name.replace(i, '')
        try:
            name = name.split('-')[1]
        except Exception:
            print(f'name dont have -')
        name.strip()
        return name

    def check_files(self, name):
        print(f'check name {name}')
        li_names = os.listdir(self.path_load_files)
        if name not in li_names or name != 'Radio Record':
            return True
        else:
            print(f'terminate download process')
            return 'terminate'

    def checker_names(self):
        id_process = None
        while True:
            name = self.q.get()
            print(f' q.get - {name}')
            if name != 'terminate':
                print(f'download new song - {name}')
                if id_process:
                    p.terminate()
                p = Process(target=self.file_loader, args=(name,))
                p.start()
                id_process = p.pid
            else:
                print(f' not load {name}')
                p.terminate()

    def file_loader(self, name):
        name = str(name)
        session = Session()
        radio = session.get(self.link, stream=True)
        radio = radio.raw
        path = self.path_load_files+name+'.mp3'
        with open(path, 'wb') as file:
            for i in radio:
                file.write(i)


if __name__ == '__main__':
    P = Parser()
    P.run()
