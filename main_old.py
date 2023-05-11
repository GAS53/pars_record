from multiprocessing import Queue, Lock, Process

import os


class Parser(object):
    """main class for parsing."""

    def __init__(self):
        self.lock = Lock()
        self.q = Queue()
        # self.link = 'http://radio-srv1.11one.ru/record192k.mp3'
        self.link = "http://radiorecord.hostingradio.ru/rr_main96.aacp"
        self.path_load_files = self.pather()

    def pather(self):
        current_dir = os.getcwd()
        files_path = current_dir + "/" + "songs_fiels/"
        if not os.path.exists(files_path):
            os.mkdir(files_path)
        return files_path

    def run(self):
        p2 = Process(target=self.checker_names, name="downloader")
        p2.start()
        p1 = Process(target=self.name_songs_from_steam, name="get_namer")
        p1.start()
        p1.join()

    def checker_names(self):
        id_process = None
        while True:
            name = self.q.get()
            print(f" q.get - {name}")
            if name != "terminate":
                print(f"download new song - {name}")
                if id_process:
                    p.terminate()
                p = Process(target=self.file_loader, args=(name,))
                p.start()
                id_process = p.pid
            else:
                print(f" not load {name}")
                p.terminate()

    def file_loader(self, name):
        name = str(name)
        session = Session()
        radio = session.get(self.link, stream=True)
        radio = radio.raw
        path = self.path_load_files + name + ".mp3"
        with open(path, "wb") as file:
            for i in radio:
                file.write(i)


if __name__ == "__main__":
    P = Parser()
    P.run()
