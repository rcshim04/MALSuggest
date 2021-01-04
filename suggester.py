"""MALSuggest/suggester
=================================================
suggester.py contains all functions used to
parse, search and suggest a new animanga
"""

import settings as s
from time import sleep
import math

"""
load function
=================================================
Accesses user's animanga list and saves to file
"""
def load():
    print('Started Loading...')

    animangalist = []
    page = 1

    """Loops through all pages of completed entries in decreasing order by score and stores them"""
    while True:
        # Returns and stores completed animanga list as python dictionary
        amlist = s.jikan.user(s.user, s.am + 'list', 'completed', page=page,
                              parameters={'sort': 'desc', 'order_by': 'score'})

        # Checks for last page
        if len(amlist[s.am]) == 0:
            break

        # Appends each entry to list
        for am in amlist[s.am]:
            animangalist.append(am)

        page += 1
        sleep(2)

    """Saves all completed entries to file"""
    with open('data/completedList', 'w', encoding='utf-8') as file:
        for amlist in animangalist:
            file.write('{},{}\n'.format(amlist['mal_id'], amlist['score']))

    animangalist = []
    page = 1

    """Loops through all pages of planned entries and stores them"""
    while True:
        # Returns and stores planned animanga list as python dictionary
        amlist = s.jikan.user(s.user, s.am + 'list', 'ptw', page=page)

        # Checks for last page
        if len(amlist[s.am]) == 0:
            break

        # Appends each entry to list
        for am in amlist[s.am]:
            animangalist.append(am)

        page += 1
        sleep(2)

    """Saves all planned entries to file"""
    with open('data/plannedList', 'w', encoding='utf-8') as file:
        for amlist in animangalist:
            file.write('{}\n'.format(amlist['mal_id']))

    print('Finished Loading')

"""
score function
=================================================
Scores all genres based on user's ratings
"""
def score():
    print('Started Calculating...')

    animangalist = []
    genreTotal = [0] * 43
    genreCount = [0] * 43
    genreAvg = [0] * 43

    """Reads all completed entries from file to list"""
    with open('data/completedList', 'r', encoding='utf-8') as file:
        amlist = file.readlines()
        for aml in amlist:
            animangalist.append(list(aml.strip().split(',')))

    total = len(animangalist)

    if total == 0:
        print('Empty List')
        s.exit()

    print('Length: {}'.format(total))
    print('ET: {} min {} sec'.format((total * 2) // 60, (total * 2) % 60))

    """Loops through completed entries and searches + scores genres"""
    for amlist in animangalist:
        # Returns and stores animanga's genre list as python list
        genrelist = (s.jikan.anime(amlist[0])['genres'] if s.am == 'anime' else s.jikan.manga(amlist[0])['genres'])

        # Stores genre information
        for glist in genrelist:
            id = glist['mal_id']
            genreTotal[id-1] += int(amlist[1])**1.25    # Sum of each score^(5/4)
            genreCount[id-1] += 1   # Counts genre frequency

        sleep(2)

    """Applies a 'weighted average' to the genre's score"""
    for i in range(43):
        genreAvg[i] = (0 if genreCount[i] == 0 else genreTotal[i]/genreCount[i]*(1+math.log10(genreCount[i])))

    # List of genre names
    genres = ['Action', 'Adventure', 'Cars', 'Comedy', 'Dementia', 'Demons', 'Mystery', 'Drama', 'Ecchi', 'Fantasy',
             'Game', 'Hentai', 'Historical', 'Horror', 'Kids', 'Magic', 'Martial Arts', 'Mecha', 'Music', 'Parody',
             'Samurai', 'Romance', 'School', 'Sci Fi', 'Shoujo', 'Shoujo Ai', 'Shounen', 'Shounen Ai', 'Space',
             'Sports', 'Super Power', 'Vampire', 'Yaoi', 'Yuri', 'Harem', 'Slice of Life', 'Supernatural', 'Military',
             'Police', 'Psychological', 'Thriller', 'Seinen', 'Josei']

    """Saves genre scores to file"""
    with open('data/genreScores', 'w', encoding='utf-8') as file:
        for i in range(43):
            file.write('{},{},{}\n'.format(genres[i], i+1, genreAvg[i]))

    print('Finished Calculating.')

"""Object used to handle genre sorting"""
class Genre:
    def __init__(self, name, id, score):
        self.name = name
        self.id = id
        self.score = score

"""Object used to handle animanga sorting"""
class Animanga:
    def __init__(self, name, type, id, score, genres):
        self.name = name
        self.type = type # Anime / Manga
        self.id = id
        self.score = score
        self.genres = genres

"""
search function
=================================================
Searches planned animangas and sorts by rating
"""
def search():
    print('Started Searching...')

    animangas = []
    animangalist = []
    genrelist = []

    """Reads all planned entries from file to list"""
    with open('data/plannedList', 'r', encoding='utf-8') as file:
        amlist = file.readlines()
        for aml in amlist:
            animangas.append(int(aml.strip()))

    total = len(animangas)

    if total == 0:
        print('Empty List')
        s.exit()

    print('Length: {}'.format(total))
    print('ET: {} min {} sec'.format((total * 2) // 60, (total * 2) % 60))

    """Loops through planned entries and searches animangas"""
    for am in animangas:
        # Returns and stores animanga as python dictionary
        animanga = (s.jikan.anime(am) if s.am == 'anime' else s.jikan.manga(am))
        glist = []

        # Stores genres
        for g in animanga['genres']:
            glist.append(g['mal_id'])

        # Stores relevant animanga data as an object
        if animanga['score'] is not None:
            animangalist.append(
                Animanga(animanga['title'], animanga['type'], animanga['mal_id'], animanga['score'], glist))

        sleep(2)

    """Reads all genre scores from file to list"""
    with open('data/genreScores', 'r', encoding='utf-8') as file:
        glist = file.readlines()
        for gl in glist:
            name, id, score = map(str, gl.strip().split(','))
            # Stores relevant genre data as an object
            genrelist.append(Genre(name, int(id), float(score)))

    """Sorts both animangas and genres by score"""
    animangalist.sort(key=lambda am: am.score, reverse=True)
    genrelist.sort(key=lambda g: g.score, reverse=True)

    """Saves animangas and genres to file in order"""
    with open('data/animangaRank', 'w', encoding='utf-8') as file:
        for am in animangalist:
            file.write('{}|{}|{}|{}\n'.format(am.name, am.type, am.id, ','.join(str(e) for e in am.genres)))
    with open('data/genreRank', 'w') as file:
        for g in genrelist:
            file.write('{}\n'.format(g.id))

    """Saves genre rankings to file"""
    with open('topgenres.txt', 'w', encoding='utf-8') as file:
        i = 1
        for g in genrelist:
            file.write('#{:02d}: {} - {}\n'.format(i, g.name, g.score))
            i += 1

    print('Finished Searching...')

"""
suggest function
=================================================
Calculates top 5 animangas based on previous data
"""
def suggest():
    print('Started Suggestion Calculation...')

    animangas = []
    genres = []

    """Reads all ranked animangas and genres from file to list"""
    with open('data/animangaRank', 'r', encoding='utf-8') as file:
        amlist = file.readlines()
        for aml in amlist:
            w, x, y, z = map(str, aml.strip().split('|'))
            animangas.append([w, x, int(y), list(z.split(','))])
    with open('data/genreRank', 'r', encoding='utf-8') as file:
        glist = file.readlines()
        for gl in glist:
            genres.append(gl.strip())

    suggestions = []
    count = 0

    """Stores top 5 animangas from top genres"""
    for am in animangas:
        for g in genres:
            if g in am[3]:
                suggestions.append([am[0], am[1], am[2]])
                count += 1
                break
        if count == 5:
            break

    """Saves 5 suggestions to file as MAL links"""
    with open('suggestions.txt', 'w', encoding='utf-8') as file:
        for sg in suggestions:
            file.write('{} ({}): https://myanimelist.net/{}/{}\n'.format(sg[0], sg[1], s.am, sg[2]))

    print('Finished Suggestion Calculation...')

"""
test function
=================================================
Saves to file a complete ranking of completed
animangas
Displays title, media type, ID, score and genres
Mainly a debugging method
"""
def test():
    print('Started Test Program')

    animangas = []

    with open('data/completedList', 'r', encoding='utf-8') as file:
        alist = file.readlines()
        print('Length: {}'.format(len(alist)))
        print('ET: {} min {} sec'.format((len(alist) * 2) // 60, (len(alist) * 2) % 60))
        for al in alist:
            mal_id, score = map(int, al.strip().split(','))
            animanga = (s.jikan.anime(mal_id) if s.am == 'anime' else s.jikan.manga(mal_id))
            genres = []
            for g in animanga['genres']:
                genres.append(g['name'])
            animangas.append('{} ({}) [{}] ({}/10): {}'.format(animanga['title'], animanga['type'], mal_id, score,
                                                               ', '.join(genres)))
            sleep(2)

    with open('data/test', 'w', encoding='utf-8') as file:
        for a in animangas:
            file.write(a+'\n')

    print('Finished Test Program')