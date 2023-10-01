#include <stdio.h>
#include <string.h>

// Word list and settings
const char* words[] = {
    "compartmentalizations",
    "counterrevolutionists",
    "establishmentarianism",
    "incomprehensibilities",
    "indistinguishableness",
    "ultraminiaturizations"
};

const int wordSize = 21;
const int numGuesses = 26;

// Function to print the current game status
void printStatus(const char pattern[], int remainingGuesses) {
    printf("The word pattern is: %s\n", pattern);
    printf("Number of guesses remaining: %d\n", remainingGuesses);
}

int main() {
    char playAgain = 'y';
    do {
        char pattern[wordSize + 1]; // +1 for null terminator
        memset(pattern, '-', wordSize); // Fill the pattern with dashes
        pattern[wordSize] = '\0'; // Null terminate the pattern string
        int remainingGuesses = numGuesses;
        
        // Welcome message and game settings
        printf("Welcome to the Word Guessing Game!\n\n");
        printf("Game Settings:\n  Word Size = %d\n  Number of Guesses = %d\n  View Word List Mode = OFF\n\n", wordSize, numGuesses);

        // You can randomly choose a word from the list
        const char *chosenWord = words[2]; // This is an example. Replace with your word choosing logic

        while(remainingGuesses > 0) {
            printStatus(pattern, remainingGuesses);
            printf("Guess a letter (# to end game): ");
            char guess;
            scanf(" %c", &guess); // Space before %c is to consume any whitespace

            if (guess == '#') break; // End game if user enters #

            // Handle user's guess here: update pattern and remainingGuesses
            int found = 0;
            for(int i = 0; i < wordSize; i++) {
                if(chosenWord[i] == guess) {
                    pattern[i] = guess;
                    found = 1;
                }
            }

            if(!found) {
                printf("Oops, there are no %c's. You used a guess.\n", guess);
                remainingGuesses--;
            }

            // Check for win condition
            if(strcmp(pattern, chosenWord) == 0) {
                printf("Congratulations! You've guessed the word: %s\n", chosenWord);
                break;
            }
        }

        // Ask user if they want to play again
        printf("Do you want to play again? (y/n): ");
        scanf(" %c", &playAgain);

    } while(playAgain == 'y' || playAgain == 'Y');

    printf("Thanks for playing! See you next time.\n");

    return 0;
}
