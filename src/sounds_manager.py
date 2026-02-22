import pygame
import os

class SoundManager:
    def __init__(self):
        pygame.mixer.init()

        self.music_channel = pygame.mixer.Channel(0)
        self.battle_channel = pygame.mixer.Channel(1)
        self.sfx_channel = pygame.mixer.Channel(2)  

        self.sounds = {}
        self._load_sounds()

        self.current_state = None

    def _load_sounds(self):
        """upload all sounds files"""
        files = {
            "menu":   "assets/sounds/menu.mp3",
            "battle": "assets/sounds/battle.mp3",
            "add":    "assets/sounds/add.mp3",
        }
        for key, path in files.items():
            if os.path.exists(path):
                try:
                    self.sounds[key] = pygame.mixer.Sound(path)
                except Exception as e:
                    print(f"[SoundManager] Uploading impossible {path} : {e}")
            else:
                print(f"[SoundManager] File not found : {path}")


    def play_menu(self):
        """start in loop menu.mp3"""
        if self.music_channel.get_busy():
            return 
        self._play_loop(self.music_channel, "menu")
        self.current_state = "menu"

    def play_battle(self):
        """start battle.mp3 in loop then interupt menu.mp3"""
        if self.current_state == "battle":
            return
        self.music_channel.stop()
        self._play_loop(self.battle_channel, "battle")
        self.current_state = "battle"

    def stop_battle(self):
        """stop battle.mp3 and restart menu.mp3"""
        self._stop_battle()
        self.current_state = "menu"
  
        if not self.music_channel.get_busy():
            self._play_loop(self.music_channel, "menu")

    def play_add_sfx(self):
        """play add.mp3 without interrupting menu.mp3"""
        if "add" in self.sounds:
            self.sfx_channel.play(self.sounds["add"], loops=0)

    def stop_all(self):
        """Stop all songs"""
        self.music_channel.stop()
        self.battle_channel.stop()
        self.sfx_channel.stop()
        self.current_state = None

    def _play_loop(self, channel, key):
        if key in self.sounds:
            channel.play(self.sounds[key], loops=-1)

    def _stop_battle(self):
        self.battle_channel.stop()