# find path to given location

map = {'A': {'B': 192, 'D': 447},
       'B': {'A': 192, 'C': 215, 'D': 371, 'G': 532},
       'C': {'B': 215, 'E': 257, 'F': 343, 'L': 549},
       'D': {'A': 447, 'B': 371},
       'E': {'C': 257, 'H': 448},
       'F': {'C': 343, 'J': 336, 'L': 473},
       'G': {'B': 532, 'J': 590},
       'H': {'E': 448, 'I': 245, 'L': 218},
       'I': {'H': 245, 'O': 190},
       'J': {'F': 336, 'G': 590, 'K': 491, 'M': 160},
       'K': {'J': 491, 'O': 376},
       'L': {'C': 549, 'F': 473, 'H': 218},
       'M': {'J': 160, 'N': 130},
       'N': {'M': 130, 'O': 226},
       'O': {'I': 190, 'K': 376, 'N': 226}}