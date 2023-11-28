import pyxel
import math
import random
from config import *
from helpers import *
from input import *
from line import *


class GameWindow:
    playerY: int

    def __init__(self):
        self.score = 0
        self.highScore = 0
        self.didSave = False
        self.pos = 0
        self.playerX = 135  # player start at the center of the road
        self.playerY = 1800  # camera height offset
        self.playerDirection = 0  # 0 = straight, 1 = left, 2 = right
        self.gameState = 1  # 0 = menu, 1 = game, 2 = crashed, 3 = game over
        self.inputX = 0
        self.gameOverSoundPlayed = False
        self.f22SoundPlayed = False
        self.distanceTraveled = 0
        self.lap = 0
        self.f22x = 300
        self.alienx = 135
        self.easterEgg = False

        self.speed = 0
        self.kmh = 0
        self.backgroundx = 0
        self.background2x = 0
        self.linespr = 0

        # Randomize enemy spawn points
        # Lower numbers = more enemies
        self.leftLaneEnemyRate = random.randint(100, 1000)
        self.rightLaneEnemyRate = random.randint(200, 1500)
        if DEBUG_MODE:
            print(
                f"leftLaneEnemyRate: {self.leftLaneEnemyRate}, rightLaneEnemyRate: {self.rightLaneEnemyRate}"
            )
            print(f"Using CORNER_RAND_VALUE_1 = {CORNER_RAND_VALUE_1}")
            print(f"Using CORNER_RAND_VALUE_2 = {CORNER_RAND_VALUE_2}")
            print(f"Using CORNER_RAND_VALUE_3 = {CORNER_RAND_VALUE_3}")
            print(f"Using CORNER_RAND_VALUE_4 = {CORNER_RAND_VALUE_4}")
            print(f"Using DISTANCE_RAND_VALUE_1 = {DISTANCE_RAND_VALUE_1}")
            print(f"Using DISTANCE_RAND_VALUE_2 = {DISTANCE_RAND_VALUE_2}")
            print(f"Using DISTANCE_RAND_VALUE_3 = {DISTANCE_RAND_VALUE_3}")
            print(f"Using DISTANCE_RAND_VALUE_4 = {DISTANCE_RAND_VALUE_4}")

        # set up Pyxel
        pyxel.init(WINDOW_WIDTH, WINDOW_HEIGHT, fps=30, title="Groom Lake")
        pyxel.load("assets/models.pyxres")

        # pyxel.sound(1).set(
        #     # "e2e2c2g1 g1g1c2e2 d2d2d2g2 g2g2rr" "c2c2a1e1 e1e1a1c2 b1b1b1e2 e2e2rr",
        #     "g3g3a3g3e3rr g3g3a3g3f3rr g3g3g4e3c3rr c4b3b3b3b3rr",
        #     "s",
        #     "6",
        #     "vffn fnff vffs vfnn",
        #     25,
        # )

        pyxel.sound(1).set_notes(
            "C2D2E-2F2G2A-2B-2C3D3E-3D3C3B-2A-2G2F2E-2D2C2R C2D2E-2F2G2A-2B-2C3D3E-3D3C3B-2A-2G2F2E-2D2C2R C2D2E-2F2G2A-2B-2C3D3E-3D3C3B-2A-2G2F2E-2D2C2R E-2D2C2B-2A-2G2F2E-2D2C2B-2A-2G2F2E-2D2C2R C2D2E-2F2G2A-2B-2C3D3E-3D3C3B-2A-2G2F2E-2D2C2R C2D2E-2F2G2A-2B-2C3D3E-3D3C3B-2A-2G2F2E-2D2C2R C2D2E-2F2G2A-2B-2C3D3E-3D3C3B-2A-2G2F2E-2D2C2R E-2D2C2B-2A-2G2F2E-2D2C2B-2A-2G2F2E-2D2C2R"
        )
        # pyxel.sound(1).set_notes(
        #     "E3D3E3G3E3C3R G3B2C3E3D3C3R E3D3E3G3E3C3R G3B2C3E3D3C3R E3F3G3C4B3A3R A3G3F3E3F3G3R C4E3D3C3D3E3R F3G3A3B3C4R C4C4B3C4D4E4G4G4F#4E4D4C4B3A3B3C4E4D4E4G4E4C4R E4D4E4G4E4C4R G4B3C4E4D4C4R E4D4E4G4E4C4R G4B3C4E4D4C4R E4F4G4C4R A4G4F4E4F4G4R C4E4D4C4D4E4R F4G4A4B4C4R C4C4B4C4D4E4G4G4F#4E4D4C4B4A4B4C4E4D4E4G4E4C4R"
        # ) # spangle
        # pyxel.sound(1).set_notes(
        #     "C4C4G4G4A4A4G4F4F4E4E4D4D4C4R R R G4G4F4F4E4E4D4G4G4F4F4E4E4D4R R R"
        # )  # twinkle
        # pyxel.sound(1).set_tones("S")
        pyxel.sound(1).set_volumes("6")
        pyxel.sound(1).set_effects("F")
        pyxel.sound(1).speed = 20
        # pyxel.sound(2).set(
        #     "r a1b1c2 b1b1c2d2 g2g2g2g2 c2c2d2e2" "f2f2f2e2 f2e2d2c2 d2d2d2d2 g2g2r r ",
        #     "s",
        #     "6",
        #     "nnff vfff vvvv vfff svff vfff vvvv svnn",
        #     20,
        # )

        # pyxel.play(2, [1, 1], loop=True)  # background music
        # pyxel.play(3, [2, 2], loop=True)

        # load highScore from highScore.txt
        try:
            with open("highScore.txt", "r") as f:
                self.highScore = int(f.read())
        except FileNotFoundError:
            self.highScore = 0

        pyxel.run(self.update, self.draw)

    def draw_background(self):
        # origin https://github.com/ChazyChazZz/PyxelRoadDemo/blob/master/main.py#L222
        pyxel.blt(self.background2x, 80, 2, 0, 177, 256, 32, 6)
        pyxel.blt(self.background2x + WINDOW_WIDTH, 80, 2, 0, 144, 256, 32, 6)
        pyxel.blt(self.background2x - WINDOW_WIDTH, 80, 2, 0, 144, 256, 32, 6)

        pyxel.blt(self.backgroundx, 95, 2, 0, 233, 256, 23, 6)
        pyxel.blt(self.backgroundx + WINDOW_WIDTH, 95, 2, 0, 209, 256, 24, 6)
        pyxel.blt(self.backgroundx - WINDOW_WIDTH, 95, 2, 0, 209, 256, 24, 6)

        pyxel.blt(self.backgroundx, 115, 2, 0, 233, 256, -23, 6)
        pyxel.blt(self.backgroundx + WINDOW_WIDTH, 116, 2, 0, 209, 256, -24, 6)
        pyxel.blt(self.backgroundx - WINDOW_WIDTH, 116, 2, 0, 209, 256, -24, 6)

    def handle_offroad(self):
        if self.playerX > 200 + self.linespr * 2:
            # print(f"off the road, linespr: {self.linespr}")
            if self.kmh > 0:  # dont come to a complete stop
                self.kmh -= 4
        if self.playerX < -0 + self.linespr * 2:
            if self.kmh > 0:
                self.kmh -= 4

        # Set game state to crashed if they go off the road too far
        if self.playerX > 250:
            self.gameState = 2  # player crashed
            print("Player crashed")
            self.kmh = 0
        if self.playerX < -150:
            self.gameState = 2  # player crashed
            print("Player crashed")
            self.kmh = 0

    def update(self):
        # React to key presses
        handle_input(self)

        # This allows the player to get sent off the track if they dont steer enough
        # otherwise it auto follows the track direction
        # self.playerX = self.playerX - self.linespr * (self.kmh * 0.05)
        update_player_position(self)

        # Check if player is off the road, and reduce speed / eventually show crash animations
        # TODO: Fix to handle offroad positions changing with curve
        # maybe move to update_player_position function
        self.handle_offroad()

        self.pos += self.speed

        # reset f22 position every 4 laps
        if self.lap % 4 == 0 or self.lap == 0:
            if self.pos / 200 > F22_APPEAR_AT:
                if not self.f22SoundPlayed:
                    self.f22SoundPlayed = True
                    pyxel.play(0, 3)  # play the f22 sound effect
                self.f22x -= (
                    self.speed * 0.020 + 1
                )  # move the f22 to the left, +1 ensures it moves even when player speed is 0
        else:
            self.f22x = 300  # reset f22 position once it has passed the player
            self.f22SoundPlayed = False

        # handle player crashing
        if self.gameState == 2:  # stop moving when crashed
            self.speed = 0
            # Play the explosion sound effect only once
            if not self.gameOverSoundPlayed:
                self.gameOverSoundPlayed = True
                pyxel.play(0, 0)

    def draw(self):
        pyxel.cls(5)

        # Call the draw_background function
        self.draw_background()

        # create road lines for each segment
        lines = []

        # Build the track
        for i in range(LAP_LENGTH):
            line = Line(i)
            line.z = (
                i * SEGMENT_LENGTH + 0.00001
            )  # adding a small value avoids Line.project() errors

            # change color at every other 3 lines (int floor division)
            grass_color = LIGHT_GRASS if (i // 40) % 2 else DARK_GRASS
            rumble_color = WHITE_RUMBLE
            road_color = DARK_ROAD
            stripe_color = (
                DARK_ROAD if (i // 15) % 2 else WHITE_RUMBLE
            )  # this is what makes the center lines

            line.grass_color = grass_color
            line.rumble_color = rumble_color
            line.road_color = road_color
            line.stripe_color = stripe_color

            if 40 < i < 50:
                # change road color to show start of track
                line.road_color = 4
                line.stripe_color = 4

            # right curve
            if 200 < i < 200 + DISTANCE_RAND_VALUE_1:
                # line.curve = 2.2
                # line.curve = 2
                line.curve = CORNER_RAND_VALUE_1

            # TODO; Add some math here to take the track length figure out how many curves to add based on
            # a given distance between each curve

            # left curve
            if 400 < i < 400 + DISTANCE_RAND_VALUE_2:
                # line.curve = -2
                line.curve = CORNER_RAND_VALUE_2

            # # uphill and downhill
            # if LAP_LENGTH > i > 750:
            #     line.y = (
            #         pyxel.sin((i / 30.0) * 180 / 3.14159265358979323846) * 1000
            #     )  # was 1500

            # left curve
            if 1000 < i < 1000 + DISTANCE_RAND_VALUE_3:
                # line.curve = -0.7
                line.curve = CORNER_RAND_VALUE_3

            if 1700 < i < 1500 + DISTANCE_RAND_VALUE_4:
                line.curve = CORNER_RAND_VALUE_4

            # Draws trees
            if i % 80 == 0:
                line.spriteX = -6
                line.sprite = 1  # enable sprite drawing
                # line.enemy = 1  # enable enemy drawing
                # line.enemyX = -1.5  # left lane

            if i % 125 == 0:
                line.spriteX = -7
                line.sprite = 1  # enable sprite drawing

            if i % 65 == 0:
                line.spriteX = 6
                line.sprite = 1  # enable sprite drawing

            # Draw enemies
            if i % self.rightLaneEnemyRate == 0:
                line.enemy = 1  # enable enemy drawing
                line.enemyX = 1.7  # right lane
                self.score += 1

            if i % self.leftLaneEnemyRate == 0:
                line.enemy = 1  # enable enemy drawing
                line.enemyX = -1.7  # left lane
                self.score += 1

            # Sprites segments
            lines.append(line)

        N = len(lines)

        self.distanceTraveled = self.pos / 200 + (LAP_LENGTH * self.lap)

        # loop the circut from start to finish
        while self.pos >= N * SEGMENT_LENGTH:
            self.pos -= N * SEGMENT_LENGTH
            self.lap += 1
            # increase frequency of enemies every lap
            self.leftLaneEnemyRate = int(self.leftLaneEnemyRate / 1.2)
            self.rightLaneEnemyRate = int(self.rightLaneEnemyRate / 1.2)
            if DEBUG_MODE:
                print(
                    f"leftLaneEnemyRate: {self.leftLaneEnemyRate}, rightLaneEnemyRate: {self.rightLaneEnemyRate}"
                )
        while self.pos < 0:
            self.pos += N * SEGMENT_LENGTH
        startPos = self.pos // SEGMENT_LENGTH

        x = dx = 0.0  # curve offset on x axis

        camH = lines[startPos].y + self.playerY
        maxy = WINDOW_HEIGHT

        # Move the background
        if self.speed > 0:
            self.backgroundx -= lines[startPos].curve * 0.5
        elif self.speed < 0:
            self.backgroundx += lines[startPos].curve * 0.5
        if self.speed > 0:
            self.background2x -= lines[startPos].curve * 0.05
        elif self.speed < 0:
            self.background2x += lines[startPos].curve * 0.05

        self.linespr = lines[startPos].curve

        # draw road / environment
        for n in range(startPos, startPos + SHOW_N_SEGMENTS):
            current = lines[n % N]
            # loop the circut from start to finish = pos - (N * SEGMENT_LENGTH if n >= N else 0)
            current.project(
                self.playerX - x, camH, self.pos - (N * SEGMENT_LENGTH if n >= N else 0)
            )
            x += dx

            dx += current.curve

            current.clip = maxy

            # don't draw "above ground"
            if current.Y >= maxy:
                continue
            maxy = current.Y

            prev = lines[(n - 1) % N]  # previous line

            drawQuad(
                current.grass_color,
                0,
                prev.Y,
                WINDOW_WIDTH,
                0,
                current.Y,
                WINDOW_WIDTH,
            )

            drawQuad(
                current.rumble_color,
                prev.X,
                prev.Y,
                prev.W * 1.05,
                current.X,
                current.Y,
                current.W * 1.05,
            )

            drawQuad(
                current.road_color,
                prev.X,
                prev.Y,
                prev.W,
                current.X,
                current.Y,
                current.W,
            )

            drawQuad(
                current.stripe_color,
                prev.X,
                prev.Y,
                prev.W * 0.025,
                current.X,
                current.Y,
                current.W * 0.025,
            )

        for n in range(startPos + SHOW_N_SEGMENTS, startPos + 1, -1):
            lines[n % N].drawSprite()
            lines[n % N].draw_ufos()

            # Draw the enemy and check for collision
            collisionCheck = lines[n % N].drawEnemy(
                self.playerX, self.playerY, self.kmh
            )
            if collisionCheck:
                self.gameState = 2
            # else:
            #     self.score += 1

        debug_info(self)

        if self.gameState == 1:  # only draw car when game is running
            draw_car(self)
            draw_f22(self)

        if self.lap > 0 and self.lap % 3 == 0:
            draw_alien_dagnabbit()

        if self.easterEgg:
            draw_alien_dagnabbit()

        draw_speedometer(self)

        if self.gameState == 2:
            if not self.didSave:  # save high score to file
                if self.lap > self.highScore:
                    self.didSave = True
                    self.highScore = self.lap
                    with open("highScore.txt", "w") as f:
                        f.write(str(self.highScore))

            # draw the explosion animation
            draw_explosion(self)
            # draw game over text in middle of screen
            pyxel.text(100, 100, "    GAME OVER", 7)
            pyxel.text(100, 110, "Press R to restart", 7)


GameWindow()
