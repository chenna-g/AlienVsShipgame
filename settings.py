class Settings:
    def __init__(self):
        self.screen_width = 800
        self.screen_height = 600
        self.bg_color = (230, 230, 230)
        # making the ship speed factor

        self.ship_speed_factor = 10
        self.ship_limit=3

        # bullet settings
        self.bullet_speed_factor = 5
        self.bullet_height = 5
        self.bullet_width = 8
        self.bullet_color = 60, 60, 60
        self.bullets_allowed = 5

        # alien settings
        self.alien_speed_factor = 1
        self.fleet_drop_speed = 60
        self.fleet_direction = 1
        #how quickly the game speeds up
        self.speedup_scale=1.1
        self.initialize_dynamic_settings()
        self.score_scale=1.5

    def initialize_dynamic_settings(self):
        self.ship_speed_factor=1.5
        self.bullet_speed_factor=3
        self.alien_speed_factor=1
        # fleet direction 1 right and -1 left
        self.fleet_direction=1
        self.alien_points=50

    def increase_speed(self):
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)
        print(self.alien_points)
