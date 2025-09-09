from animated_zombie import AnimatedZombie
class BlueZombie(AnimatedZombie):
    BASE_SPEED_RANGE = (2, 3)
    SPEED_PER_DAY = 0.7
    BASE_HEALTH = 40
    HEALTH_PER_DAY = 7
    DETECTION_RADIUS = 800
    DAMAGE = 6
    REWARD = 15

    FRAMES = [
        "assets/images/гт1ле.png",
        "assets/images/гт2ле.png",
        "assets/images/гт3ле.png",
    ]
    FRAMES_LEFT = [
         "assets/images/гт1пр.png",
         "assets/images/гт2пр.png",
         "assets/images/гт3пр.png",
     ]
    FRAME_TIME = 0.12

class GreenZombie(AnimatedZombie):
    BASE_SPEED_RANGE = (2, 3)
    SPEED_PER_DAY = 0.3
    BASE_HEALTH = 40
    HEALTH_PER_DAY = 7
    DETECTION_RADIUS = 350
    DAMAGE = 3
    REWARD = 10
    FRAMES = [
        "assets/images/з1ле.png",
        "assets/images/з2ле.png",
        "assets/images/з3ле.png",
    ]
    FRAMES_LEFT = [
         "assets/images/з1пр.png",
         "assets/images/з2пр.png",
         "assets/images/з3пр.png",
     ]
    FRAME_TIME = 0.12

class PurpleZombie(AnimatedZombie):
    BASE_SPEED_RANGE = (1, 2)
    SPEED_PER_DAY = 0.7
    BASE_HEALTH = 100
    HEALTH_PER_DAY = 10
    DETECTION_RADIUS = 300
    DAMAGE = 6
    REWARD = 40
    FRAMES = [
        "assets/images/ф1ле.png",
        "assets/images/ф2ле.png",
        "assets/images/ф3ле.png",
    ]
    FRAMES_LEFT = [
         "assets/images/ф1пр.png",
         "assets/images/ф2пр.png",
         "assets/images/ф3пр.png",
     ]
    FRAME_TIME = 0.12

class RedZombie(AnimatedZombie):
    BASE_SPEED_RANGE = (1, 2)
    SPEED_PER_DAY = 0.7
    BASE_HEALTH = 100
    HEALTH_PER_DAY = 10
    DETECTION_RADIUS = 300
    DAMAGE = 6
    REWARD = 40
    FRAMES = [
        "assets/images/к1ле.png",
        "assets/images/к2ле.png",
        "assets/images/к3ле.png",
    ]
    FRAMES_LEFT = [
         "assets/images/к1пр.png",
         "assets/images/к2пр.png",
         "assets/images/к3пр.png",
     ]
    FRAME_TIME = 0.12

class LimeZombie(AnimatedZombie):
    BASE_SPEED_RANGE = (2, 3)
    SPEED_PER_DAY = 0.3
    BASE_HEALTH = 40
    HEALTH_PER_DAY = 7
    DETECTION_RADIUS = 350
    DAMAGE = 3
    REWARD = 10
    FRAMES = [
        "assets/images/с1ле.png",
        "assets/images/с2ле.png",
        "assets/images/с3ле.png",
    ]
    FRAMES_LEFT = [
         "assets/images/с1пр.png",
         "assets/images/с2пр.png",
         "assets/images/с3пр.png",
     ]
    FRAME_TIME = 0.12

class HatZombie(AnimatedZombie):
    BASE_SPEED_RANGE = (3, 4)
    SPEED_PER_DAY = 0.8
    BASE_HEALTH = 20
    HEALTH_PER_DAY = 5
    DETECTION_RADIUS = 350
    DAMAGE = 10
    REWARD = 30
    FRAMES = [
        "assets/images/шл1ле.png",
        "assets/images/шл2ле.png",
        "assets/images/шл3ле.png",
    ]
    FRAMES_LEFT = [
         "assets/images/шл1пр.png",
         "assets/images/шл2пр.png",
         "assets/images/шл3пр.png",
     ]
    FRAME_TIME = 0.12

class CyanZombie(AnimatedZombie):
    BASE_SPEED_RANGE = (3, 4)
    SPEED_PER_DAY = 0.6
    BASE_HEALTH = 70
    HEALTH_PER_DAY = 7
    DETECTION_RADIUS = 600
    DAMAGE = 7
    REWARD = 35
    FRAMES = [
        "assets/images/ц1ле.png",
        "assets/images/ц2ле.png",
        "assets/images/ц3ле.png",
    ]
    FRAMES_LEFT = [
         "assets/images/ц1пр.png",
         "assets/images/ц2пр.png",
         "assets/images/ц3пр.png",
     ]
    FRAME_TIME = 0.12

class VioletZombie(AnimatedZombie):
    BASE_SPEED_RANGE = (1, 2)
    SPEED_PER_DAY = 0.7
    BASE_HEALTH = 75
    HEALTH_PER_DAY = 15
    DETECTION_RADIUS = 1000
    DAMAGE = 3
    REWARD = 25
    FRAMES = [
        "assets/images/л1ле.png",
        "assets/images/л2ле.png",
        "assets/images/л3ле.png",
    ]
    FRAMES_LEFT = [
         "assets/images/л1пр.png",
         "assets/images/л2пр.png",
         "assets/images/л3пр.png",
     ]
    FRAME_TIME = 0.12
