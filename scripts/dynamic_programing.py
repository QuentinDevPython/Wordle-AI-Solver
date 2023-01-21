import terminal_display
"""
This approach aims to re-implement the work from Bertsimas and Paskov
in their paper: "An Exact and Interpretable Solution to Wordle".
"""

"""
1. State:
    .first definition: 
        unordered collection of the guesses and corresponding tilecolorings seen
        so far.
    .equivalent solution:
        a collection of words, which represents the set of all possible solutions
        that are valid, given the information presented to the player.
    therefore the initial state S0 contains the 12,972 possible words
"""

def load_english_words(file_name):
    file = open(file_name,'r')
    words = file.read().split()
    file.close()
    return words

initial_state = load_english_words('dictionary_words_5.txt')

"""
2. Control: We define an action as a word in the set of all possible valid guesses A, which contains
12,972 words.
"""
for word in initial_state:
    #find the best move
    print (word)
"""
3. Cost function: : We define the cost of a guess as 1, and the cost of losing
  the game as ∞. As such, ct(s, a) = 1, ∀t ≤ 5, and c6(s) = ∞
"""


"""
4. Tansition function: For a given state st and guess a, denote P(st, a)  as the
collection of all states we can transition into, given that we are in st and guess a
"""
def is_valid_solution(action,tile_coloring,temp_solution):
    if tile_coloring==22222:
        return True
    else :
        return False

def get_transition_information(state,action):
    transition_info= dict()
    for solution in state:
        tile_coloring=terminal_display.check_word(action,solution)
        temp_state=set()
        for temp_solution in state:
            if is_valid_solution(action,tile_coloring,temp_solution):
                temp_state.add(solution)
        transition_info[temp_state]+=1/len(state)
    return transition_info


def optimal_value(state,t,dictionary):
    if t==6 or t==5 and len(state)>1:
        return float("inf")
    elif t==5:
        return 1
    elif len(state)==1:
        return 1
    elif len(state)==2:
        return 1.5
    elif (state,t) in dictionary:
        return dictionary[(state,t)]
    state_value=float("inf")
    for action in initial_state:
        temp=1
        next_states=get_transition_information(state,action)
        if next_states.size ==1 and state in next_states:
            continue
        for next_state in next_states:
            temp=temp+(2*len(next_state)-1)/len(next_state)
        for next_state in next_states:
            if temp >= state_value:
                break
            elif next_state == action:
                continue
            temp_dict={
                "pair":(next_state,t+1),
                "value":state_value

            }
            new_dictionary=dictionary.append(temp_dict)
            temp = temp+optimal_value(next_state,t+1,new_dictionary)
        if temp <state_value:
            state_value=temp
    return state_value

