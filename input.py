import pyxel
from config import *


def handle_input(self):
    if self.gameState == 1:  # only accept player input when game is running
        if pyxel.btn(pyxel.KEY_W) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_A):
            if 90 > self.kmh > 0 and pyxel.frame_count % 5 == 0:
                self.kmh += 6
            if pyxel.frame_count % 5 == 0:
                self.kmh += 2
        if pyxel.btn(pyxel.KEY_S) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_B):
            # Slow down quicker when going slower
            if self.kmh <= 0:
                self.kmh = 0
            if self.kmh > 0 and self.kmh < 50:
                self.kmh -= 10
            if self.kmh >= 50 and self.kmh < 100:
                self.kmh -= 5
            if self.kmh >= 100:
                self.kmh -= 2

        # Turn right
        if pyxel.btn(pyxel.KEY_D) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT):
            if self.kmh > 0:
                # self.playerX += 5
                self.inputX += 5
                self.playerDirection = 2
            else:
                self.playerDirection = 0
        if pyxel.btnr(pyxel.KEY_D):
            self.playerDirection = 0  # reset to straight when key is released

        # Turn left
        if pyxel.btn(pyxel.KEY_A) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT):
            if self.kmh > 0:
                # self.playerX -= 5
                self.inputX -= 5
                self.playerDirection = 1
            else:
                self.playerDirection = 0
        if pyxel.btnr(pyxel.KEY_A):
            self.playerDirection = 0  # reset to straight when key is released

        # Move camera up and down
        if pyxel.btn(pyxel.KEY_UP):
            self.playerY += 100
        if pyxel.btn(pyxel.KEY_DOWN):
            self.playerY -= 100
            # avoid camera going below ground
        if self.playerY < 500:
            self.playerY = 500
            # turbo speed
        if pyxel.btn(pyxel.KEY_TAB):
            self.speed *= 2  # it has to be N integer times the segment length
        if self.kmh < 0:
            self.kmh = 0
        if self.kmh == 0:
            self.speed = 0
        if 50 > self.kmh > 0:
            self.speed = 200
        if 100 > self.kmh > 50:
            self.speed = 400
        if 150 > self.kmh > 100:
            self.speed = 600
        if 200 > self.kmh > 150:
            self.speed = 800
        if 250 > self.kmh > 200:
            self.speed = 1200
        if self.kmh > 250 and pyxel.frame_count % 12 == 0:
            self.kmh = 250

    # Quit if Q pressed
    if pyxel.btn(pyxel.KEY_Q):
        pyxel.quit()

    # Reset game if R pressed
    if pyxel.btn(pyxel.KEY_R):
        self.playerX = 135
        self.kmh = 0
        self.pos = 0
        self.inputX = 0
        self.playerDirection = 0
        self.gameState = 1
        self.gameOverSoundPlayed = False
        self.distanceTraveled = 0
        self.lap = 0
        self.f22x = 300
        self.score = 0
        self.f22SoundPlayed = False
        self.didSave = False

    # Toggle showing the alien
    if pyxel.btn(pyxel.KEY_U):
        if self.easterEgg == False:
            self.easterEgg = True
        else:
            self.easterEgg = False
