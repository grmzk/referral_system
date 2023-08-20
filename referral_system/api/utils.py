import random
import string

from referral_system.settings import INVITE_CODE_LENGTH


def generate_invite_code():
    symbols = string.digits + string.ascii_letters + '~!@#$%^&*()_-+'
    return ''.join(random.choice(symbols) for i in range(INVITE_CODE_LENGTH))
