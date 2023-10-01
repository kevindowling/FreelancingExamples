# Word Guessing Game in C

This is a simple word guessing game written in C. The game selects a word from a predefined list, and the user needs to guess it letter by letter. The game keeps running until the user decides to exit or when the word is completely guessed.

## Features

- Allows user to guess one letter at a time.
- Provides a visual representation of the word, displaying correct guesses and hiding unguessed letters.
- User can end the game anytime by entering '#'.
- Offers play again feature.

## Gameplay

- The game will show the word to be guessed as a series of dashes representing unguessed letters.
- The user is prompted to guess one letter at a time.
- If the guessed letter is in the word, it will be revealed in the correct positions.
- The game continues until the user either guesses the whole word or chooses to end the game.
- At the end of each game, the user will be asked if they want to play again.

## Getting Started

### Prerequisites

- A C compiler (like `gcc`) is required to compile and run the program.

### Compilation

To compile the program, navigate to the directory containing the `main.c` file in your terminal and run:

```sh
gcc main.c -o wordguess
