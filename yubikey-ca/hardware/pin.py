import os
import getpass
import functools

@functools.lru_cache()
def get_pin():
    pin = os.getenv('PIN', '123456')
    if pin == 'ask':
        pin = getpass.getpass('PIN: ')
    return pin
