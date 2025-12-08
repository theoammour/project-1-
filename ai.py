import pygame
import random

class AI:
    def __init__(self, game_box, difficulty_settings):
        self.game_box = game_box
        self.settings = difficulty_settings
        self.move_queue = []
        self.timer = 0
        self.last_action_time = 0
        self.active = False
        
        # Actions
        self.ACTION_LEFT = 0
        self.ACTION_RIGHT = 1
        self.ACTION_INVERT = 2
        self.ACTION_DOWN = 3
        
        # Timings (ms)
        self.waiting_time = self.settings.get('waitingIATime', 1000)
        self.move_interval = self.settings.get('keyFirstMoveTime', 500)

    def start(self):
        self.active = True
        self.last_action_time = pygame.time.get_ticks()
        self.plan_moves()

    def stop(self):
        self.active = False
        self.move_queue = []

    def plan_moves(self):
        # Simple AI: Random moves for now, or logic to solve the column
        # The original game's AI seems to follow a pre-determined or reactive path.
        # For this port, let's make it try to reduce the highest column.
        
        # This is a placeholder for the actual solving logic.
        # In a real game, the AI would analyze the board.
        # Here we just queue some random valid moves to simulate activity.
        if not self.move_queue:
            for _ in range(5):
                action = random.choice([self.ACTION_LEFT, self.ACTION_RIGHT, self.ACTION_INVERT])
                self.move_queue.append(action)
            self.move_queue.append(self.ACTION_DOWN)

    def update(self, current_time):
        if not self.active:
            return

        if current_time - self.last_action_time > self.move_interval:
            if self.move_queue:
                action = self.move_queue.pop(0)
                self.execute_action(action)
                self.last_action_time = current_time
            else:
                self.plan_moves()

    def execute_action(self, action):
        if action == self.ACTION_LEFT:
            self.game_box.rotate_left()
        elif action == self.ACTION_RIGHT:
            self.game_box.rotate_right()
        elif action == self.ACTION_INVERT:
            self.game_box.invert_key()
        elif action == self.ACTION_DOWN:
            self.game_box.apply_key()
