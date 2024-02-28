def throws_to_win(score_to_win):
    # Initialize a list to store the minimum number of throws needed to reach each score
    throws_needed = [float('inf')] * (score_to_win + 1)
    # Initialize the first score (0) to be reachable with 0 throws
    throws_needed[0] = 0
    
    # Loop through all possible scores up to the target score
    for score in range(1, score_to_win + 1):
        # Check all possible throws
        for dart_throw in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
                           21, 22, 24, 26, 27, 28, 30, 32, 33, 34, 36, 38, 39, 40, 42, 45, 48,
                           51, 54, 57, 60]:
            if score >= dart_throw:
                # Update throws_needed[score] if the current throw reduces the number of throws needed
                throws_needed[score] = min(throws_needed[score], throws_needed[score - dart_throw] + 1)

    # Reconstruct the optimal sequence of throws
    optimal_throws = []
    score = score_to_win
    while score > 0:
        for dart_throw in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
                           21, 22, 24, 26, 27, 28, 30, 32, 33, 34, 36, 38, 39, 40, 42, 45, 48,
                           51, 54, 57, 60]:
            if score >= dart_throw and throws_needed[score] == throws_needed[score - dart_throw] + 1:
                optimal_throws.append(dart_throw)
                score -= dart_throw
                break

    return optimal_throws

# Example usage
score_to_win = 170
optimal_throws = throws_to_win(score_to_win)
print(optimal_throws)
