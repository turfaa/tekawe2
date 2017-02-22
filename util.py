import string
import random

def randomString(length = 6, chars = string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(length))

def shuffleString(strIn):
    return ''.join(random.sample(strIn, len(strIn)))
