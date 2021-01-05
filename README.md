# MALSuggest
 
An anime/manga suggester. Suggests 5 animangas based on watched/read animanga on [MyAnimeList](https://myanimelist.net/).

Runs on [Jikan API](https://jikan.moe/), an unofficial MyAnimeList API. The API is rate limited, so the program may take a long time depending on the data set size.

## Usage

MALSuggest is a program written in Python.

To run, open main.py in an IDE (Ex. [PyCharm](https://www.jetbrains.com/pycharm/download/)) or install the following dependency with pip:

`
pip install jikanpy
`

Open `user.txt` and type the MAL username on line 1 and the media type (anime/manga) on line 2.

When main.py is finished running, 5 suggestions will be in `suggustions.txt` in the form of MAL links. The user's genres will be listed by score in `topgenres.txt`. Note that the assigned scores do not correspond to MAL scores. A list of all completed animanga with their genres sorted by user assigned scores can be found in `data/test`.

Written in Python with the JikanPy Python Wrapper library.
