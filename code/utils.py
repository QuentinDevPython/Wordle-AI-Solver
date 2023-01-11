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
