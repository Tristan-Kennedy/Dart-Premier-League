def throws_to_win(target_score):
    # Define available throws
    available_throws = [
        [20, 3], [19, 3], [18, 3], [17, 3], [16, 3], [15, 3],
        [14, 3], [13, 3], [12, 3], [11, 3], [10, 3], [9, 3],
        [8, 3], [7, 3], [6, 3], [5, 3], [4, 3], [3, 3],
        [2, 3], [1, 3],
        [25, 2], [20, 2], [19, 2], [18, 2], [17, 2], [16, 2], [15, 2],
        [14, 2], [13, 2], [12, 2], [11, 2], [10, 2], [9, 2],
        [8, 2], [7, 2], [6, 2], [5, 2], [4, 2], [3, 2],
        [2, 2], [1, 2],
        [25, 1], [20, 1], [19, 1], [18, 1], [17, 1], [16, 1], [15, 1],
        [14, 1], [13, 1], [12, 1], [11, 1], [10, 1], [9, 1],
        [8, 1], [7, 1], [6, 1], [5, 1], [4, 1], [3, 1],
        [2, 1], [1, 1],
    ] #throws are stored as their value + the multiplier 
    
    throw_types = {1: 'single', 2: 'double', 3: 'triple'} #dictionary mapping multiplier to their literal 
    
    #memo table speeds things up tremendously 
    memo = {} #intialize the memo table 
    memo[0] = []
    
    for score in range(1, target_score + 1): #iterate through the score 
        best_combination = None #intialize our best combo 
        
        # Try all possible throws and update the best combination for the current score
        for throw, multiplier in available_throws:
            if score - throw * multiplier >= 0:
                if memo[score - throw * multiplier] is not None:
                    combination = memo[score - throw * multiplier] + [(throw, multiplier)] #big time saver: check the memo table to see if we  already have an entry for that remaining score have an entry for the current
                    
                    if score == target_score and multiplier != 2: #you can only win on a double as far as I know. So if the last throw isn't a double, skip it 
                        continue
                    if best_combination is None or len(combination) < len(best_combination): 
                        best_combination = combination
        memo[score] = best_combination #store the results in the memo table for future reference 
    
    # Return the best combination for the target score
    return memo[target_score]
