"""MALSuggest/main
=================================================
main.py contains the driver code
"""

import suggester as s

try:
    s.load()
    s.score()
    s.search()
    s.suggest()

    s.test() # Debugging method / Optional

except ConnectionResetError:
    print('Connection Reset')
except ConnectionAbortedError:
    print('Connection Aborted')
except ConnectionError:
    print('Connection Error')
