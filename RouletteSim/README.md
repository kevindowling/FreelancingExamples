# Roulette Simulation Web Application

This repository houses a web-based Roulette simulation as part of the FreelancingExamples project. The live version of the app is hosted [here](https://roulette.kevindowling.dev).

## Description

The simulation allows users to experiment with various betting strategies in a Roulette game scenario. The available betting strategies are:

- Martingale
- Reverse Martingale
- D'Alembert
- Labouchère
- Fibonacci
- Oscar's Grind

### Betting Strategies

#### Martingale

In the Martingale strategy, players double their bet after each loss. Once a bet is won, the player resets their bet to the initial amount.

#### Reverse Martingale

The Reverse Martingale strategy involves doubling the bet after each win and resetting to the initial bet amount after a loss.

#### D'Alembert

In the D'Alembert strategy, players increase their bet by a fixed amount after a loss and decrease it by the same amount after a win.

#### Labouchère

The Labouchère strategy requires players to decide on an amount they wish to win, then write down a list of positive numbers that sum to that amount. The player bets the sum of the first and last number in the list. If they win, they cross off the numbers, and if they lose, they add the sum to the end of the list.

#### Fibonacci

The Fibonacci strategy involves betting by following the Fibonacci sequence (0, 1, 1, 2, 3, 5, 8, 13, etc.), increasing the bet to the next number in the sequence after a loss and moving back two numbers in the sequence after a win.

#### Oscar's Grind

In the Oscar's Grind strategy, players aim to win a single unit at a time. They start by betting one unit and increase their bet by one unit only after a win, resetting to one unit after a loss or when a cycle ends.

## Running Locally

Refer to the README under `RouletteSimLocal` for instructions on how to run the command line version of this simulation on your machine.

## Contributing

Feel free to fork this repository and submit pull requests for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE.md file for details.
