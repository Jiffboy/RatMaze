import pygame
from pygame import mixer

from vars.direction import Direction
from vars.globals import frame_rate
from vars.resources import rat_idle_right_lookup, \
    rat_idle_left_lookup, \
    rat_walking_right_lookup, \
    rat_walking_left_lookup, \
    rat_cheese_right_lookup, \
    rat_cheese_left_lookup, \
    rat_jump_right_lookup, \
    rat_jump_left_lookup, \
    rat_idle_fps, \
    rat_walking_fps, \
    rat_cheese_fps, \
    rat_jump_fps


class Rat:
    def __init__(self, size):
        self.x = 0
        self.y = 0
        self.dest_x = 0
        self.dest_y = 0
        self.origin_x = 0
        self.origin_y = 0
        self.fps = rat_idle_fps
        self.curr_frame = 0
        self.next_sprite = 0
        self.size = size
        self.speed_boost = False
        self.can_jump = False
        self.animation_locked = False
        self.moving = False
        self.eating = False
        self.celebrating = False
        self.walking_cycles = 2
        self.dest_time = 0
        self.origin_time = 0
        self.facing = Direction.RIGHT
        self.sprite_lookup = rat_idle_right_lookup
        self.image = self.sprite_lookup[self.next_sprite]

    def get_x(self):
        if not self.moving:
            return self.x
        else:
            return self.origin_x

    def get_y(self):
        if not self.moving:
            return self.y
        else:
            return self.origin_y

    def do_frame(self):
        next_update = frame_rate / self.fps
        self.curr_frame += 1
        if self.curr_frame >= next_update:
            self.curr_frame = 0
            self.update_sprite()
        if self.moving:
            now = pygame.time.get_ticks()
            if now >= self.dest_time:
                self.stop()
            else:
                full_time = self.dest_time - self.origin_time
                curr_time = now - self.origin_time
                increment = curr_time / full_time
                self.x = self.origin_x + (increment * (self.dest_x - self.origin_x))
                self.y = self.origin_y + (increment * (self.dest_y - self.origin_y))
        if self.eating:
            if self.next_sprite == 1 and self.curr_frame == 0:
                self.eating = False
                self.animation_locked = False
                mixer.music.load("resources/audio/cheese.mp3")
                mixer.music.play()
                self.celebrate()
        elif self.celebrating:
            if self.next_sprite == 1 and self.curr_frame == 0:
                self.celebrating = False
                self.set_idle()

    def draw(self, screen):
        x_pos = self.x * self.size
        y_pos = self.y * self.size
        screen.blit(self.image, (x_pos, y_pos))

    def set_position(self, x, y):
        self.x = x
        self.y = y

    def move_to(self, x, y):
        if not self.animation_locked:
            x_diff = x - self.x
            self.animation_locked = True
            self.moving = True
            self.dest_x = x
            self.dest_y = y
            self.origin_x = self.x
            self.origin_y = self.y
            self.origin_time = pygame.time.get_ticks()
            self.dest_time = self.origin_time + ((len(rat_walking_right_lookup) / rat_walking_fps) * 1000)

            if x_diff > 0:
                self.facing = Direction.RIGHT

            elif x_diff < 0:
                self.facing = Direction.LEFT

            if self.facing == Direction.RIGHT:
                self.sprite_lookup = rat_walking_right_lookup
            elif self.facing == Direction.LEFT:
                self.sprite_lookup = rat_walking_left_lookup

            self.fps = rat_walking_fps if not self.speed_boost else rat_walking_fps * 2
            self.reset_sprite()

    def jump_to(self, x, y):
        self.dest_x = x
        self.dest_y = y
        self.stop()

    def stop(self):
        self.moving = False
        self.x = self.dest_x
        self.y = self.dest_y
        self.set_idle()

    def set_idle(self):
        self.animation_locked = False
        if self.facing == Direction.RIGHT:
            self.sprite_lookup = rat_idle_right_lookup
        elif self.facing == Direction.LEFT:
            self.sprite_lookup = rat_idle_left_lookup
        self.fps = rat_idle_fps
        self.reset_sprite()

    def eat_cheese(self):
        if not self.animation_locked:
            self.animation_locked = True
            self.eating = True
            if self.facing == Direction.RIGHT:
                self.sprite_lookup = rat_cheese_right_lookup
            elif self.facing == Direction.LEFT:
                self.sprite_lookup = rat_cheese_left_lookup
            self.fps = rat_cheese_fps
            self.reset_sprite()
            mixer.music.load("resources/audio/eating.mp3")
            mixer.music.play()

    def celebrate(self):
        if not self.animation_locked:
            self.animation_locked = True
            self.celebrating = True
            if self.facing == Direction.RIGHT:
                self.sprite_lookup = rat_jump_right_lookup
            elif self.facing == Direction.LEFT:
                self.sprite_lookup = rat_jump_left_lookup
            self.fps = rat_jump_fps
            self.reset_sprite()

    def reset_sprite(self):
        self.next_sprite = 0
        self.curr_frame = 0
        self.update_sprite()

    def update_sprite(self):
        self.image = pygame.transform.scale(self.sprite_lookup[self.next_sprite], (self.size, self.size))
        self.next_sprite += 1
        if self.next_sprite >= len(self.sprite_lookup):
            self.next_sprite = 0

    def set_size(self, size):
        self.size = size
        self.image = pygame.transform.scale(self.image, (self.size, self.size))

    def reset_buffs(self):
        self.speed_boost = False
        self.can_jump = False
