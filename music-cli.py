title = f"""

████     ████   ██        ██   ███████████  ██████████  ███████████   ██          ██████████                          
██ ██   ██ ██   ██        ██   ██               ██      ██            ██              ██
██  ██ ██  ██   ██        ██   ██               ██      ██            ██              ██
██   ██    ██   ██        ██   ███████████      ██      ██            ██              ██
██         ██   ██        ██            ██      ██      ██            ██              ██
██         ██   ██        ██            ██      ██      ██            ██              ██
██         ██   ████████████   ███████████  ██████████  ███████████   ██████████  ██████████

A Command Line Interference to play in song in your computer and download from the web!!. Made with \033[31m♥️\033[0m!!!

Created by \033[36msamispro\033[0m,created in \033[33mpython\033[0m!!
"""

import sys
import os
import time
import argparse
import subprocess
import platform

try:
    import yt_dlp as youtube_dl
    from rich.console import Console
    from rich.table import Table
    from colorama import Fore, init
    import inquirer
    import tqdm

    os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'
    import pygame

except ImportError:
    print("Try to run the setup script!! \n Script: python music-cli.py --install")


#variable ground [global]- starts
init()

__version__ = '1.0'

SONG_END = pygame.USEREVENT + 1
pygame.mixer.music.set_endevent(SONG_END)

console = Console()

#variable ground [global]- Ends

class clrscr:
    def __init__(self):
        os.system('cls' if os.name == 'nt' else 'clear')

class OfflineMode:
    def __init__(self):

        pygame.init()
        pygame.mixer.init()   

        self.path:any = None
        self.playlist = []
        self.current_song = self.current_index = 0
        self.status_autoplay: bool = False
        self.loop_count: str| any | None | int = "None"
        self.fade_input: int | None = 0
        self.volume: int = 100
        self.selection: any | None = "Not Selected Yet"

    def load_playlist(self, playlist_file):
        try:
            with open(playlist_file, 'r') as file:
                self.playlist = file.readlines()
                self.playlist = [line.strip() for line in self.playlist if line.strip()]
                if not self.playlist:
                    raise ValueError("Playlist is empty.")
        except Exception as e:
            print(f"Error loading playlist: {e}")

    def add_music(self, target_path):
        if target_path:
            os.chdir(target_path)
            songs = os.listdir(target_path)
            self.playlist.extend([song for song in songs if song.lower().endswith(".mp3")])

    def autoplay(self):
        if self.status_autoplay and self.current_index < len(self.playlist) - 1:
            next_song_path = self.playlist[self.current_index + 1]
            pygame.mixer.music.queue(next_song_path)

    def play_music(self, music_opt):
        full_path = os.path.join(self.path, music_opt)
        self.current_index_raw = music_opt

        print("Full Path:", full_path)
        try:
            if full_path.lower().endswith('.mp3'):
                pygame.mixer.music.load(full_path)
                pygame.mixer.music.play()

                # Check if autoplay is enabled and there's a current song
                if self.status_autoplay and self.current_song:
                    print("Autoplay enabled. Music will continue playing automatically.")
                    pygame.mixer.music.queue(self.current_song)  # Queue the next song
                else:
                    print("Music playback started.")
            else:
                raise ValueError("Unsupported audio format. Supported format: MP3")
        except Exception as e:
            print("Error playing music, Error:", e)

    def next_song(self):
        # Check if the playlist is empty, if so, print a message and return
        if not self.playlist:
            print("No songs in the playlist.")
            return
        
        # Get the next song from the playlist
        print(self.current_index_raw)
        self.current_index = self.playlist.index(self.current_index_raw) + 1
        temp_list = []
        temp_list.append(self.current_index)
        new_path = list(map(self.playlist.__getitem__, temp_list))
        self.new_path = os.path.join(self.path, *new_path)
        if self.new_path:
            self.play_music(self.new_path)
            temp_list.clear()
            self.current_index_raw = (new_path[0])
        if self.new_path and self.selection:
            self.selection:str = new_path[0]
    
    def toggle_autoplay(self):
        menu = [
                inquirer.List("Autoplay",
                            message="Navigation: Player -> Toggle AutoPlay",
                            choices=["Back","Enable AutoPlay", "Disable AutoPlay"],
                            default="Disable AutoPlay",
                            carousel=True)
                ]
        answers = inquirer.prompt(menu)
        if answers["Autoplay"] == "Back":
            clrscr()
        elif answers["Autoplay"] == "Enable AutoPlay":
            self.status_autoplay = True
            clrscr()
        elif answers["Autoplay"] == "Disable AutoPlay":
            self.status_autoplay = False
            clrscr()

    def NextSong(self):     #This is for pure usage for the autoplay functionality
        if not self.playlist:
            print("No Song in the Playlist")
            return
        
        self.current_index = (self.current_index + 1) % len(self.playlist)
        next_song_path = self.playlist[self.current_index]
        self.play_music(next_song_path)

        # Check if autoplay is enabled and there's a current song
        if self.status_autoplay:
            next_next_song_index = (self.current_index + 1) % len(self.playlist)
            next_next_song_path = self.playlist[next_next_song_index]
            self.play_music(next_next_song_path)

    def previous_song(self):
        if self.current_index > 0:
            self.current_index -= 1
        else:
            self.current_index = len(self.playlist) - 1  # Go to the end of the playlist
        self.play_music(self.playlist[self.current_index])

    def toggle_loop(self, file_path):
        full_path = os.path.join(self.path, file_path)
        if full_path:
            menu = [
                inquirer.List(
                    "Options",
                    message="Player Settings: Navigation : Select desired loop style",
                    choices=["Back","Loop Indefinitely", "Loop Once", "Set your Loop count"],
                )
            ]
            options = inquirer.prompt(menu)
            try:
                if options["Options"] == "Back":
                    clrscr()
                    return
                if options["Options"] == "Loop Indefinitely":
                    clrscr()
                    pygame.mixer.music.play(loops=-1)
                    self.loop_count = "Infinite"
                if options["Options"] == "Loop Once":
                    clrscr()
                    pygame.mixer.music.play(loops=0)
                    self.loop_count = "Loop Once"
                if options["Options"] == "Set your Loop count":
                    clrscr()
                    loop_count = inquirer.text(message="Enter your loop count:")
                    pygame.mixer.music.play(loops=int(loop_count))
                    self.loop_count = f"[Finite] Looping:{loop_count}"
                    clrscr()
                    print(f"The song is selected to loop [{loop_count}] time(s)")
            except Exception as e:
                print(f"Error playing music: {e}")

    def InformationPlayer(self):
        info_table = Table(title="Information - Musicli", title_justify='center', caption="Made in python!! Created by samispro.",caption_justify='left')
        info_table.add_column("Content",style="cyan", no_wrap=True)
        info_table.add_column("Value",style="yellow", no_wrap=True)
        # info_table.add_row("Current Song", self.current_song)
        # info_table.add_row("Current Index", self.current_index)
        info_table.add_row("Current Path", self.path)
        info_table.add_row("(Status) Autoplay", "Not Enabled" if self.status_autoplay == False else "Enabled")
        info_table.add_row("(Status) Loop",f"{self.loop_count if self.loop_count or self.loop_count != 'None' else "Not Enabled"}")
        console.print(info_table)
    
    def offline_mode(self):
        print("Playing Offline")
        status_ = pygame.mixer.music.get_endevent()
        if status_ == SONG_END:
            if self.status_autoplay == True:
                self.NextSong()
        while True: 
            clrscr()
            questions_offline = [
                inquirer.Text("path", message="Enter a file path:"),
                inquirer.Confirm("confirm", message="Is this the correct path?", default=True)
            ]
            print(f"{title}\n")
            print("Playing Offline")
            print("Songs will be played from this path for this session!!. Each session can hold only one path\n")
            answers_offline = inquirer.prompt(questions_offline)
            if answers_offline["confirm"]:
                print("Songs will play from this path for this session")
                self.path = answers_offline["path"]
                print(f"Path Selected: {self.path}")
                self.add_music(self.path)
                playlist_cmd_list = [
                    inquirer.List("Playlist",
                                  "Choose a music",
                                  choices=self.playlist,
                                  carousel=True)
                ]
                answers_playlist = inquirer.prompt(playlist_cmd_list)
                selection = answers_playlist["Playlist"]
                if selection:
                    self.selection: str = selection
                    while True:
                        clrscr()
                        print(f"Selected Directory: {self.path}")
                        print(f"Playing: {self.selection}")
                        print("\n")
                        menu = [inquirer.List(
                            "player",
                            message="Navigation: Player",
                            choices=["Play the current", "Stop the current",
                                     "Pause Music", "Resume Music",
                                     "Previous", "Next",
                                     "Player Settings",
                                      "Exit"],
                                    carousel=True)
                                      ]
                        option = inquirer.prompt(menu)
                        self.player_option = option["player"]
                        if option and self.player_option == "Play the current":
                            self.play_music(selection)
                            clrscr()
                        elif option and self.player_option == "Stop the current":
                            pygame.mixer.music.stop()
                            clrscr()
                        elif option and self.player_option == "Pause Music":
                            pygame.mixer.music.pause()
                            clrscr()
                        elif option and self.player_option == "Resume Music":
                            pygame.mixer.music.unpause()
                            clrscr()
                        elif option and self.player_option == "Previous":
                            self.previous_song()
                            clrscr()
                        elif option and self.player_option == "Next":
                            self.next_song()
                            clrscr()
                        elif option and self.player_option == "Player Settings":
                            clrscr()
                            smenu = [inquirer.List(
                                "player",
                                message="Navigation: Player -> Player Settings",
                                choices=["Volume", "Toggle AutoPlay", "Toggle Loop", "Set Fadeout","Reselect the Directory", "Show Player Information"],
                                carousel=True)]
                            soption = inquirer.prompt(smenu)
                            self.suboption = soption["player"]
                            if soption and self.suboption == "Volume":
                                clrscr()
                                print("[\033[1;33;40m?\033[0m]Navigation: Player -> Player Settings -> Volume")
                                vol_input = int(input("Enter the Desired Volume from [1-100]\n Volume: "))
                                if vol_input:
                                    final = float(vol_input / 100)
                                    self.vol = str(vol_input) + "%"
                                    if final: 
                                        print(f"setting volume to: {vol_input}%")
                                        pygame.mixer.music.set_volume(float(final))
                                        continue                                       
                            elif soption and self.suboption == "Toggle AutoPlay": 
                                self.toggle_autoplay()
                                self.autoplay()  # Call autoplay after toggling
                            elif soption and self.suboption == "Toggle Loop":
                                self.toggle_loop(selection)
                            elif soption and self.suboption == "Reselect the Directory":
                                clrscr()
                                self.selection = "Not Selected yet!!!"
                                print("Reselecting Directory...")
                                self.offline_mode()
                                clrscr()
                            elif soption and self.suboption == "Show Player Information":
                                clrscr()
                                self.InformationPlayer()
                                exit_input = [inquirer.Confirm("exit", message="Do you want to exit?", default=True)]
                                answers_exit = inquirer.prompt(exit_input)
                                if answers_exit["exit"]: clrscr()
                            elif soption and self.suboption == "Set Fadeout":
                                clrscr()
                                print("Fadeout will immediately start to fade the music away.")
                                question_fade = [inquirer.Text("fade", message="Enter your fadeout time in seconds")]
                                answers_fade = inquirer.prompt(question_fade)
                                if answers_fade["fade"]:
                                    self.fade_input = float(answers_fade["fade"])
                                    fade_input = int(answers_fade["fade"])
                                    fade_time = fade_input * 1000
                                    pygame.mixer.music.fadeout(int(fade_time))  
                        elif option and self.player_option == "Exit":
                            clrscr()
                            print("Exiting from the player...")
                            sys.exit()
class OnlinePlayer:
    def __init__(self):
        self.song_ = ''
        self.current_song = None
        self.console = Console()
        self.loop_mode = 'None'
        self.status_dispfo = False
        pygame.mixer.init()

    def clrscr(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def download_audio_from_youtube(self, video_url):
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': '%(title)s.%(ext)s',
            'noplaylist': True,
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_url, download=True)
            audio_file = ydl.prepare_filename(info_dict).replace('.webm', '.mp3').replace('.m4a', '.mp3')
            self.song = audio_file
            self.current_song = info_dict
        return audio_file

    def search_youtube(self, query):
        ydl_opts = {
            'default_search': 'ytsearch5',
            'quiet': True,
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            search_result = ydl.extract_info(query, download=False)
        return search_result['entries']

    def display_results(self, results):
        table = Table(title="YouTube Search Results")
        table.add_column("Number", justify="right", style="cyan", no_wrap=True)
        table.add_column("Title", style="magenta")
        table.add_column("URL", style="green")

        for idx, result in enumerate(results, start=1):
            table.add_row(str(idx), result['title'], result['webpage_url'])

        self.console.print(table)

    def display_info(self):
        table = Table(title="Current Song Information and Settings")
        table.add_column("Attribute", style="magenta")
        table.add_column("Value", style="green")

        if self.current_song:
            table.add_row("Title", self.current_song['title'])
            table.add_row("Uploader", self.current_song['uploader'])
            table.add_row("Duration", str(self.current_song['duration']) + " seconds")

        table.add_row("Loop Mode", self.loop_mode)

        self.console.print(table)

    def play_song(self, file_path):
        if self.loop_mode == 'Once':
            loops = 0
        elif self.loop_mode == 'Indefinite':
            loops = -1
        elif self.loop_mode.startswith('Definite'):
            loops = int(self.loop_mode.split(':')[1])
        else:
            loops = 0

        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play(loops=loops)

    def pause_song(self):
        pygame.mixer.music.pause()

    def resume_song(self):
        pygame.mixer.music.unpause()

    def stop_song(self):
        pygame.mixer.music.stop()

    def set_volume(self):
        self.clrscr()
        print("[\033[1;33;40m?\033[0m] Navigation: Player -> Player Settings -> Volume")
        vol_input = int(input("Enter the Desired Volume from [1-100]\n Volume: "))
        if vol_input:
            final = float(vol_input / 100)
            if final: 
                print(f"Setting volume to: {vol_input}%")
                pygame.mixer.music.set_volume(float(final))

    def online_player(self):
        self.clrscr()
        print(title)
        print("\n\nWelcome to the Online Player!!!")
        print("Songs will be accessed by {Fore.RED}YouTube{Fore.RESET}!!\n")
        questions = [
            inquirer.Text('target', message="Please Enter the Song")
        ]
        answers = inquirer.prompt(questions)
        if answers["target"]:
            self.song_ = answers["target"]
            results = self.search_youtube(self.song_ + " (Song)")
            
            self.display_results(results)
            choices = [f"{idx+1}. {result['title']}" for idx, result in enumerate(results)]
            questions = [
                inquirer.List('song_choice',
                              message="Select the song to download",
                              choices=choices,
                              carousel=True)
            ]
            answers = inquirer.prompt(questions)
            if answers['song_choice']:
                selected_index = int(answers['song_choice'].split('.')[0]) - 1
                selected_song = results[selected_index]
                audio_file = self.download_audio_from_youtube(selected_song['webpage_url'])
                print(f"Downloaded: {audio_file}")
                self.loop_mode = 'None'
                self.play_song(audio_file)
                
                while True:
                    self.clrscr()
                    print(audio_file)
                    self.display_info() if self.status_dispfo else ""
                    questions = [
                        inquirer.List('control',
                                      message="Controls: Select an action",
                                      choices=['Pause', 'Resume', 'Stop', 'Volume', 'Loop Once', 'Loop Indefinite', 'Set Definite Loops', 'Show Information', 'Reselect Music', 'Exit'],
                                      carousel=True)
                    ]
                    answers = inquirer.prompt(questions)
                    control = answers['control'].lower()
                    
                    if control == 'pause':
                        self.pause_song()
                    elif control == 'resume':
                        self.resume_song()
                    elif control == 'stop':
                        self.stop_song()
                    elif control == 'volume':
                        self.set_volume()
                    elif control == 'show information':
                        self.status_dispfo = not self.status_dispfo
                    elif control == 'reselect music':
                        self.stop_song()
                        break
                    elif control == 'loop once':
                        self.loop_mode = 'Once'
                        self.play_song(audio_file)
                    elif control == 'loop indefinite':
                        self.loop_mode = 'Indefinite'
                        self.play_song(audio_file)
                    elif control == 'set definite loops':
                        questions = [
                            inquirer.Text('loops', message="Enter the number of loops")
                        ]
                        answers = inquirer.prompt(questions)
                        if answers['loops'].isdigit():
                            self.loop_mode = f"Definite:{answers['loops']}"
                            self.play_song(audio_file)
                        else:
                            print("Invalid number of loops!")
                    elif control == 'exit':
                        self.stop_song()
                        while pygame.mixer.music.get_busy():
                            time.sleep(0.1)
                        questions = [
                            inquirer.Confirm('keep_file', message="Do you want to keep the downloaded file?", default=False)
                        ]
                        pygame.mixer.music.unload()
                        answers = inquirer.prompt(questions)
                        if not answers['keep_file']:
                            print("Deleting the file...")
                            for i in tqdm.tqdm(range(100), desc="Deleting..."):
                                time.sleep(0.01)
                            time.sleep(1)
                            os.remove(audio_file)
                        print("Exiting...")
                        sys.exit()

class CommandHubLogic:
    def __init__(self) -> None:
        parser = argparse.ArgumentParser(description="Commands for music cli")
        parser.add_argument("--setup", action="store_true", help="Installs required modules, initialize the paths.")
        parser.add_argument("--info", action="store_true", help="Shows the current information of the musicli.")
        args = parser.parse_args()

        if args.setup:
            self.app_setup()
        elif args.info:
            self.app_info()

    def app_setup(self):
        try:
            subprocess.run("python -m pip install pygame inquirer rich yt-dlp tqdm", shell=True)
            print("\n\n Installed required modules sucessfully")
        except Exception:
            print("\nFailed to install due to PATH restriction. Install the packages and try to run the code manually")
            print("\n\t SCRIPT: python -m pip install pygame inquirer rich yt-dlp tqdm ")
        finally:
            sys.exit()

    def app_info(self):
        info_table = Table(title="Information - Musicli",title_justify="center")
        info_table.add_column("Name", style="cyan", no_wrap=True)
        info_table.add_column("Value", style="magenta")
        info_table.add_row("Version", f"{__version__}")
        info_table.add_row("Author", "samispro")
        info_table.add_row("User", f"{os.getlogin()}")
        info_table.add_row("Python", f"{sys.version}")
        info_table.add_row("OS", f"{platform.system()} {platform.release()}")
        console.print(info_table)
        sys.exit()

class MainLogic():
    def __init__(self):
        
        # Prompt user for mode selection
        clrscr()
        print(title)
        print("\n\n Welcome to the 𝕞𝕦𝕤𝕚𝕔𝕝𝕚, user! \n ")
        questions_mode = [
            inquirer.List(
                "Option",
                message="Which mode are you in?",
                choices=["Offline mode (Local Storage)", "Online mode (Youtube)", "Exit"],
                carousel=True
            ),
        ]

        answers_mode = inquirer.prompt(questions_mode)

        if answers_mode["Option"] == "Offline mode (Local Storage)":
            OfflineMode().offline_mode()
        elif answers_mode["Option"] == "Online mode (Youtube)":
            OnlinePlayer().online_player()
        else:
            print("Exiting from the player...")
            clrscr()
            sys.exit()

def main():
    CommandHubLogic()
    MainLogic()

if __name__ == '__main__':
    main()