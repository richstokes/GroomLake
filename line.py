import pyxel
import random
from array_data import tree_pixels, enemy_pixels, ufo_pixels
from config import *
from helpers import *


class Line:
    def __init__(self, i):
        self.i = i
        self.x = self.y = self.z = 0.0  # game position (3D space)
        self.X = self.Y = self.W = 0.0  # game position (2D projection)
        self.scale = 0.0  # scale from camera position
        self.curve = 0.0  # curve radius
        self.spriteX = 0.0  # sprite position X
        self.clip = 0.0  # correct sprite Y position
        self.sprite = None
        self.enemy = None
        self.enemyX = 0  # enemy position X
        self.enemy2X = 0.6  # 2nd enemy position X

        self.grass_color = 0
        self.rumble_color = 0
        self.road_color = 0

    def project(self, camX, camY, camZ):
        self.scale = CAMERA_DEPTH / (self.z - camZ)
        self.X = (1 + self.scale * (self.x - camX)) * WINDOW_WIDTH / 2
        self.Y = (1 - self.scale * (self.y - camY)) * WINDOW_HEIGHT / 2
        self.W = self.scale * ROAD_WIDTH * WINDOW_WIDTH / 2

    def drawSprite(self):
        if self.sprite is None:
            return

        w = 160
        h = 160
        destX = self.X + self.scale * self.spriteX * WINDOW_WIDTH / 2
        destY = self.Y + 4
        destW = w * self.W / 266
        destH = h * self.W / 266

        destX += destW * self.spriteX
        destY += destH * -1

        clipH = destY + destH - self.clip
        if clipH < 0:
            clipH = 0
        if clipH >= destH:
            return

        # avoid scalling up images which causes lag
        scale = destW / w * 10

        # Draw stuff on side of road
        if 0 < destX < WINDOW_WIDTH and destY < WINDOW_HEIGHT and clipH > 0:
            if scale > 1:
                rescalem_generic(scale, destX, destY, 16, tree_pixels)
            else:
                rescale_generic(scale, destX, destY, 16, tree_pixels)

    def drawEnemy(self, playerX, playerY, kmh):
        if self.enemy is None:
            return

        w = 80  # make sure this matches the array data size
        h = 80
        destX = self.X + self.scale * self.enemyX * WINDOW_WIDTH / 2  # from drawSprite

        # destX = WINDOW_WIDTH / 2 - 32
        destY = self.Y + 4
        destW = w * self.W / 266
        destH = h * self.W / 266

        destX += destW * self.enemyX  #
        # destX += destW - 10  # testing
        destY += destH * -1

        clipH = destY + destH - self.clip
        if clipH < 0:
            clipH = 0
        if clipH >= destH:
            return

        # avoid scaling up images which causes lag
        scale = destW / w * 10

        # Draw enemies
        if 0 < destX < WINDOW_WIDTH and destY < WINDOW_HEIGHT and clipH > 0:
            if scale > 1:
                rescalem_generic(
                    scale,
                    destX,
                    destY,
                    8,
                    enemy_pixels,
                )
            else:
                rescale_generic(scale, destX, destY, 8, enemy_pixels)

        # Detect if player collides with enemy
        # if DEBUG_MODE:
        #     print(
        #         f"playerX: {int(playerX)}, playerY: {int(playerY)}, destX: {int(destX)}, destY: {int(destY)}, destH: {int(destH)}, clipH: {int(clipH)}, kmh: {kmh}"
        #     )

        # Check if the horizontal distance between destX and playerX is within 20 pixels and if destY meets the threshold for collision detection.
        enemy_x_threshold = 20
        enemy_y_threshold = 160  # 140 is the Y coordinate of the enemy at which we would like to detect a collision

        # play enemy sound effect/chirp
        if int(destY) >= enemy_y_threshold:
            pyxel.play(2, 2)  # play the enemy sound effect

        if (
            abs(destX - playerX) <= enemy_x_threshold
            and int(destY) >= enemy_y_threshold
        ):
            # print("Collided!!!")
            pyxel.stop(2)
            # TODO: fix. only call this if the player is not already dead / gamestate is not 2
            return True  # Disable for testing
            return False
        else:
            return False

    def draw_ufos(self):
        if self.sprite is None:
            return
        w = 320
        h = 3200

        destX = self.X + self.scale * WINDOW_WIDTH / 2
        destY = self.Y + 4
        destW = w * self.W / 500
        destH = h * self.W / 600

        destX += destW * self.spriteX
        destY += destH * -1
        # destY = 60

        clipH = destY + destH - 10  # - self.clip
        # if clipH < 0:
        #     clipH = 0
        # if clipH >= destH:
        #     return

        # avoid scalling up images which causes lag
        scale = destW / w * 10

        # Draw ufos
        if 0 < destX < WINDOW_WIDTH and destY < WINDOW_HEIGHT and clipH > 0:
            if scale > 1:
                rescalem_generic(scale, destX, destY, 16, ufo_pixels)
            else:
                rescale_generic(scale, destX, destY, 16, ufo_pixels)
