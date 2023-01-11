class WordDictionary:
    """A class that loads words from a file and make them available for other class"""

    def __init__(self):
        pass

    def load_words(self, file_name):
        """Loads words from a text file and stores them as a list

        Args:
            file_name (str): the path to the text file containing the words

        Returns:
            list: a list of strings containing the words
        """
        with open(file_name) as file:
            words = file.readlines()
        words = [word.strip() for word in words]
        return words


def check_word(word, guess):
    # 2 : Position correcte
    # 1 : Lettre dans le mot mais position incorrecte
    # 0 : Lettre pas dans le mot
    # Deux mots égaux si uniquement des 2
    rslt = []
    for idx, letter in enumerate(guess):
        if letter == word[idx]:
            rslt.append(2)
        elif letter in word:
            n_target = word.count(letter)
            n_correct = 0
            n_occurrence = 0
            
            for i, g in enumerate(guess):
                if g == letter:
                    if i <= idx:
                        n_occurrence += 1
                    if letter == word[i]:
                        n_correct += 1

            if n_target - n_correct - n_occurrence >= 0:
                rslt.append(1)
            else:
                rslt.append(0)
        else:
            rslt.append(0)
    return rslt



def respect_constraint(word, letters_count,  known_position, known_bad_position):
    '''
    Vérifie si un mot pourrait être le mot cible en fct de 3 contraintes :
    - letters_count : un dictionnaire lettre -> nombre d'occurence de la lettre
    - known_position : une liste de la longueur du mot. 
                        Chaque élément est soit une chaine vide soit une lettre à la bonne position.
                        (en gros les 2)
    - known_bad_position : une liste de la longueur du mot. 
                        Chaque élément est soit None soit une liste de lettre qui ne peuvent pas aller à cette position.
                        (en gros les 1)
    '''

    new_letters_count = letters_count.copy()

    for letter, good_letter, bad_letter in zip(word,known_position, known_bad_position):
        count = letters_count.get(letter)

        if good_letter and good_letter != letter :
            # Mauvaise lettre à cette position : le mot n'est pas bon
            return False
        if count==None:
            #Aucune info sur cette lettre, on passe
            continue
        if count==0:
            # La lettre ne devrait pas être présente, le mot n'est pas bon
            return False
        # La lettre est présente >=1 fois dans le mot cible
        if bad_letter!=None and letter in bad_letter :
            # Lettre présente dans le mot mais pas à cette position: le mot n'est pas bon
            return False
            
        new_letters_count[letter] -= 1
    for c in new_letters_count.values():
        if c>0:
            # Il manque des lettres
            return False
    return True

def reduce_words(words, letters_count,  known_position, known_bad_position):
    '''
    Réduit une liste de mot à l'aide de la fonction respect_constraint
    '''
    words = [w for w in words if respect_constraint(w,letters_count,known_position,known_bad_position)]
    return words