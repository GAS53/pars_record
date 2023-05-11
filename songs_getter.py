import pyautogui

from settings import FILE_SONGS_NAMES, get_pictures

class Main():
    def __init__(self) -> None:
        self.pictures_di = get_pictures()
        
        ...
    def get_songs(self):
        with open(FILE_SONGS_NAMES, 'r') as file:
            res = file.readlines()
        return res
    
    def send_song(self, song):
        find_music = pyautogui.locateCenterOnScreen(self.pictures_di['find_music.png'], confidence = 0.7)
        pyautogui.moveTo(find_music)
        pyautogui.click()
        pyautogui.write(song)
        from time import sleep
        sleep(1)
        all_songs = pyautogui.locateCenterOnScreen(self.pictures_di['all_songs.png'], confidence = 0.7)
        pyautogui.moveTo(all_songs)
        pyautogui.moveRel(0, -20)
        pyautogui.click()

    def del_song(self):
        song = pyautogui.locateCenterOnScreen(self.pictures_di['del_song.png'], confidence = 0.7)
        pyautogui.moveTo(song)
        pyautogui.click()


    def run(self):
        # for song in self.get_songs():
        #     self.send_song(song)
        #     break
        self.del_song()  # работает
        # print(self.get_song())
        # print('откройте контакт')
        # input('контакт открыт')
        # while True:
        print()
        

if __name__ == '__main__':
    m = Main()
    m.run()
