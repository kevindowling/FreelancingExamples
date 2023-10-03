# Roulette Simulation CLI (Command Line Interface)

This folder contains the command line version of the Roulette Simulation as part of the FreelancingExamples project.

## Description

The CLI application allows users to simulate various betting strategies in a Roulette game scenario. The available betting strategies are:

- Martingale (`mart`)
- Reverse Martingale (`rev`)
- D'Alembert (`dale`)
- Labouchère (`labo`)
- Fibonacci (`fibo`)
- Oscar's Grind (`osca`)

## Getting Started

### Dependencies

* Ensure you have Python 3.x installed on your machine.
* Install the required packages using pip:

```bash
pip install argparse itertools random
```

### Running the Simulation
1. Clone the repository to your local machine.
2. Navigate to the `RouletteSimLocal` directory.
3. Run the simulation using the command line arguments as explained below.

### Usage: 
``roulette.py [-h] -s STRATEGY -b BANKROLL -bet INITIAL_BET [-m MAX_SPINS] [-w WIN_LIMIT] [-seq [SEQUENCE [SEQUENCE ...]]]``

### optional arguments:
*  -h, --help
*  -s, --strategy      | STRATEGY  Name of the strategy to simulate (required)
*  -b, --bankroll      | BANKROLL  Initial bankroll (required)
*  -bet, --initial_bet | INITIAL_BET  Initial bet amount (required)
*  -m, --max_spins     | MAX_SPINS  Maximum number of spins (default: 100)
*  -w, --win_limit     | WIN_LIMIT  Win limit for Reverse Martingale Strategy (default: 3)
*  -seq, --sequence    | [SEQUENCE [SEQUENCE ...]]  List of numbers for Labouchere System (default: [1,2,3])


### Example Usage
```python roulette.py -s mart -b 1000 -bet 10```


### Contributing
Feel free to fork this repository and submit pull requests for any enhancements or bug fixes.

### License
This project is licensed under the MIT License. See the LICENSE.md file for details.

