import pyxel
import math
import time
from array_data import tree_pixels, enemy_pixels, ufo_pixels
from config import *


def update_player_position(self):
    # Define constants for player input and road curvature influence on movement
    player_input_influence = 0.7  # Adjust this factor for sensitivity to player input
    road_curvature_influence = 0  # Adjust this factor for sensitivity to road curvature

    # Calculate the total movement influence (player input + road curvature)
    total_influence = (
        player_input_influence * self.inputX + road_curvature_influence * self.linespr
    )

    # if DEBUG_MODE:
    #     print(
    #         f"linespr: {self.linespr}, inputX: {self.inputX}, playerX: {self.playerX}"
    #     )

    # Adjust player movement based on the relationship between input and road curvature
    if self.inputX == 0:
        if self.speed > 0:
            if (self.inputX > 0 and self.linespr < 0) or (
                self.inputX < 0 and self.linespr > 0
            ):
                # If input and road curvature are in opposite directions, reduce the effect of road curvature
                total_influence *= 0.1  # Adjust the factor to control how much road curvature is reduced, default 0.5

            # Nudge the player off the track if not following the road curvature
            if self.linespr > 0 and self.inputX <= 0:
                # Road is turning right, player is not turning, push car off to the left
                self.playerX -= 10
            elif self.linespr < 0 and self.inputX >= 0:
                # Road is turning left, player is not turning, push car off to the right
                self.playerX += 10

    # Update player position based on the calculated influence
    self.playerX += total_influence
    self.inputX = 0


def rescale_generic(n, nx, ny, size, pixel_data):
    for y in range(int(size * n)):
        for x in range(int(size * n)):
            if pixel_data[int(y / n)][int(x / n)] != 8:
                pyxel.pset(x + nx, y + ny, pixel_data[int(y / n)][int(x / n)])


def rescalem_generic(n, nx, ny, size, pixel_data):
    n = round(n * 2) / 2
    for y in range(size):
        for x in range(size):
            if pixel_data[int(y)][int(x)] != 8:
                pyxel.rect(
                    (x * n) + nx, (y * n) + ny, 1 * n, 1 * n, pixel_data[int(y)][int(x)]
                )
    return n


def drawQuad(
    color: int,
    x1: int,
    y1: int,
    w1: int,
    x2: int,
    y2: int,
    w2: int,
):
    points = [(x1 - w1, y1), (x2 - w2, y2), (x2 + w2, y2), (x1 + w1, y1)]
    color = color
    draw_polygon(points, color)


def draw_polygon(points, color):
    # Triangulate the polygon using the ear clipping algorithm
    triangles = []
    remaining_points = points.copy()
    while len(remaining_points) >= 3:
        # Find an "ear" triangle
        for i in range(len(remaining_points)):
            prev = remaining_points[(i - 1) % len(remaining_points)]
            curr = remaining_points[i]
            next = remaining_points[(i + 1) % len(remaining_points)]
            if is_ear(prev, curr, next, remaining_points):
                triangles.append((prev, curr, next))
                remaining_points.remove(curr)
                break

    # Draw each triangle with the specified color
    for triangle in triangles:
        x1, y1 = triangle[0]
        x2, y2 = triangle[1]
        x3, y3 = triangle[2]
        pyxel.tri(x1, y1, x2, y2, x3, y3, col=color)


def is_ear(p1, p2, p3, polygon):
    # Check if the triangle formed by p1, p2, p3 is an "ear"
    if not is_ccw(p1, p2, p3):
        return False
    for point in polygon:
        if point in (p1, p2, p3):
            continue
        if is_inside_triangle(p1, p2, p3, point):
            return False
    return True


def is_ccw(p1, p2, p3):
    # Check if the points p1, p2, p3 are in counter-clockwise order
    # using the cross product method
    return (p2[0] - p1[0]) * (p3[1] - p1[1]) > (p2[1] - p1[1]) * (p3[0] - p1[0])


def is_inside_triangle(p1, p2, p3, point):
    # Check if the point is inside the triangle formed by p1, p2, p3
    # using the barycentric coordinate method
    u = (
        (p2[0] - p1[0]) * (point[1] - p1[1]) - (p2[1] - p1[1]) * (point[0] - p1[0])
    ) / ((p2[1] - p1[1]) * (p3[0] - p2[0]) - (p2[0] - p1[0]) * (p3[1] - p2[1]))
    v = (
        (p3[0] - p2[0]) * (point[1] - p2[1]) - (p3[1] - p2[1]) * (point[0] - p2[0])
    ) / ((p2[1] - p1[1]) * (p3[0] - p2[0]) - (p2[0] - p1[0]) * (p3[1] - p2[1]))
    return 0 <= u <= 1 and 0 <= v <= 1 and u + v <= 1


def debug_info(self):
    if DEBUG_MODE:
        # draw the test palette
        for n in range(16):
            pyxel.rect(6 * n, 4, 6, 6, n)

        # overlay the debug info
        pyxel.text(1, 14, f"{self.kmh} km/h debug", 0)
        pyxel.text(1, 21, f"{self.linespr} correct player X debug", 0)
        pyxel.text(1, 28, f"{int(self.pos / 200)} player pos", 0)
        pyxel.text(1, 35, f"{int(self.playerY / 200)} player Y", 0)
        pyxel.text(1, 42, f"{int(self.playerX / 200)} player X", 0)
        pyxel.text(1, 49, f"{int(self.playerX)} player X raw", 0)
        pyxel.text(1, 56, f"{self.speed} game speed", 0)
        pyxel.text(1, 63, f"{int(self.distanceTraveled)} distance", 0)
        # pyxel.text(1, 70, f"{self.lap} laps", 0)
        # pyxel.text(1, 77, f"{self.score} current score", 0)


def draw_speedometer(self):
    # draw the speedo at the bottom right of the screen
    pyxel.circ(225, 225, 25, 1)

    # draw a needle for the speedo that sweeps over the speedo in a clockwise direction relative to the speed
    angle = (
        self.kmh * 0.6 - 160
    )  # Calculate the angle, subtract 180 degrees (π/2 radians) for starting from the left
    needle_x = 225 + 20 * pyxel.cos(angle)
    needle_y = 225 + 20 * pyxel.sin(angle)
    pyxel.line(224, WINDOW_HEIGHT - 5, needle_x, needle_y, 7)

    # draw the speedo text
    # convert self.kmh to miles per hour
    pyxel.text(214, 210, f"{int(self.kmh * 0.621371)} mph", 7)

    # display laps on bottom left of screen
    pyxel.text(10, 210, f"Laps: {self.lap}", 7)

    # display highScore above the laps
    pyxel.text(10, 200, f"Highscore: {self.highScore}", 7)


def draw_car(self):
    if self.playerDirection == 0:
        car_v_coord = 0
    elif self.playerDirection == 1:
        car_v_coord = 68
    elif self.playerDirection == 2:
        car_v_coord = 34
    pyxel.blt(
        self.playerX,
        WINDOW_HEIGHT / 2 + 64,
        1,  # image bank
        0,  # u coordinate
        car_v_coord,  # v coordinate, 0 for straight, 34 for right, 68 for left
        64,  # width
        32,  # height
        10,  # color key / transparent color
    )


def draw_explosion(self):
    # Define explosion constants
    EXPLOSION_SIZE = 16  # Number of explosion frames
    EXPLOSION_RADIUS = 40  # Radius of the explosion
    EXPLOSION_LAYERS = 4  # Number of layers of the explosion

    # fill red center of screen
    pyxel.fill(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2, 8)

    # Draw explosion effect
    for j in range(EXPLOSION_LAYERS):
        for i in range(EXPLOSION_SIZE * j):
            angle = (i / EXPLOSION_SIZE) * 2 * math.pi  # Angle in radians

            # Calculate x and y offsets using trigonometry to form a circle
            x_offset = int(EXPLOSION_RADIUS * math.cos(angle) * j)
            y_offset = int(EXPLOSION_RADIUS * math.sin(angle) * j)

            # Draw explosion at the calculated position around the center
            pyxel.blt(
                WINDOW_WIDTH // 2 + x_offset,
                WINDOW_HEIGHT // 2 + y_offset,
                0,
                16,
                80,
                32,
                32,
                0,
            )


def draw_f22(self):
    f22_u_coord = 0
    f22_v_coord = 40
    pyxel.blt(
        self.f22x,
        WINDOW_HEIGHT / 2 - 100,
        0,  # image bank
        f22_u_coord,  # u coordinate
        f22_v_coord,  # v coordinate
        32,  # width
        24,  # height
        0,  # color key / transparent color
    )


def draw_alien_dagnabbit():
    alien_u_coord = 0
    alien_v_coord = 105

    # Generate random coordinates for no reason wtf is this
    alien_x = random.randint(0, 250 - 64)  # Adjust the x of the alien
    alien_y = random.randint(0, 150 - 100)  # Adjust the y of the alien

    pyxel.blt(
        alien_x,
        alien_y,
        1,  # image bank
        alien_u_coord,  # u coordinate
        alien_v_coord,  # v coordinate
        64,  # width
        240,  # height
        0,  # color key / transparent color
    )

    pyxel.play(2, 4)  # play the alien sound
