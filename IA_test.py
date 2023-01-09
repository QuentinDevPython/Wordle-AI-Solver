class IATest:
    previous_results:dict

    def __init__(self):
        self.previous_results = {}

    def save_results(self, word, rslt):
        self.previous_results[word] = rslt
    
    def guess(self):
        # rslts = self.previous_results
        print(self.previous_results)
        return "AAAAA"