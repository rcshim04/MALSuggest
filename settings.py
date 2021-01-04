"""MALSuggest/settings
=================================================
settings.py contains the Jikan unoffical MAL API
and reads MAL username and media type from file
"""

from jikanpy import Jikan
import sys

def exit():
    sys.exit()

jikan = Jikan()
user = ''
am = ''
error = False

"""Reads reads username and media type from file"""
with open('user.txt', 'r') as file:
    user = file.readline().strip()
    am = file.readline().strip().lower()

"""Checks if user exists"""
try:
    jikan.user(user, 'profile')
except ConnectionError:
    print('Connection error')
    exit()
except:
    user = None

if user is None:
    print('Invalid user')
    error = True
if am != 'anime' and am != 'manga':
    print('Invalid media type')
    error = True
if error:
    exit()

print(user)
print(am.capitalize())