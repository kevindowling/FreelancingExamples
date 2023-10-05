#import argparse
from itertools import islice
import random
from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
from logging.handlers import RotatingFileHandler



# Define Strategy Functions


def run_martingale_simulation(initial_bankroll, initial_bet, max_spins):
    bankroll = initial_bankroll
    bet = initial_bet
    results = []
    while bankroll > 0:
        result = simulate_spin()
        if result == 'win':
            bankroll += bet
            bet = initial_bet
        else:
            bankroll -= bet
            bet *= 2
        results.append(bankroll)
    return results

def run_reverse_martingale_simulation(initial_bankroll, initial_bet, win_limit, max_spins):
    bankroll = initial_bankroll
    bet = initial_bet
    spins = 1
    results = []
    win_streak = 0
    while bankroll > 0 and spins <= max_spins:
        result = simulate_spin()
        if result == 'win':
            bankroll += bet
            bet *= 2
            win_streak += 1
            if win_streak >= win_limit:
                bet = initial_bet
        else:
            bankroll -= bet
            bet = initial_bet
            win_streak = 0
        results.append(bankroll)
        spins += 1
    return results

def run_dalembert_simulation(initial_bankroll, initial_bet, max_spins):
    bankroll = initial_bankroll
    bet = initial_bet
    results = []
    while bankroll > 0 and bet > 0:
        result = simulate_spin()
        if result == 'win':
            bankroll += bet
            bet -= 1
        else:
            bankroll -= bet
            bet += 1
        results.append(bankroll)
    return results

def run_labouchere_simulation(initial_bankroll, sequence, max_spins):
    # Log the sequence
    app.logger.warning(f"Ladouchere sequence received: {sequence}")
    bankroll = initial_bankroll
    results = []
    while bankroll > 0 and sequence:
        bet = sequence[0] + sequence[-1]
        result = simulate_spin()
        if result == 'win':
            bankroll += bet
            sequence = sequence[1:-1]
        else:
            bankroll -= bet
            sequence.append(bet)
        app.logger.warning(f"Ladouchere result appended: {bankroll}")
        results.append(bankroll)
    return results

def run_fibonacci_simulation(initial_bankroll, initial_bet, max_spins):
    bankroll = initial_bankroll
    results = []
    fib_seq = [1, 1]
    idx = 0
    while bankroll > 0:
        bet = fib_seq[idx] * initial_bet
        result = simulate_spin()
        if result == 'win':
            bankroll += bet
            idx = max(0, idx - 2)
        else:
            bankroll -= bet
            idx += 1
            if idx >= len(fib_seq):
                fib_seq.append(fib_seq[-1] + fib_seq[-2])
        results.append(bankroll)
    return results

def run_oscars_grind_simulation(initial_bankroll, initial_bet, max_spins):
    bankroll = initial_bankroll
    bet = initial_bet
    results = []
    profit = 0
    spins = 0  # to keep track of the number of spins
    
    while bankroll >= initial_bet and spins < max_spins:
        result = simulate_spin()
        spins += 1  # increment the spin count after each spin
        
        if result == 'win':
            bankroll += bet
            profit += bet
            if profit >= initial_bet:
                profit = 0
                bet = initial_bet
        else:
            bankroll -= bet
            profit = 0
            bet = min(bankroll, bet + initial_bet)
            
        results.append(bankroll)
        
        if bankroll < initial_bet or spins >= max_spins:
            break  # break out of the loop if bankroll is less than initial_bet or max_spins is reached
    
    return results


# Define Simulation Spin
def simulate_spin():
    number = random.randint(0, 37)  # 0 to 37 where 37 represents '00' in American roulette
    if number == 0 or number == 37:
        return 'loss'
    return 'win' if number % 2 == 0 else 'loss'


def run_simulation(strategy_func, *args, **kwargs):
    max_spins = kwargs.get('max_spins', 100)  # You can set a default value or manage it differently
    
    strategy_results = strategy_func(*args, **kwargs)
    app.logger.warning(f"run_simulation strategy_results: {strategy_results}")

    results = []
    strategy_iter = iter(strategy_results)  # Create an iterator from strategy_results
    peek_iter = iter(strategy_results)  # Create a second iterator for peeking
    next(peek_iter, None)  # Advance the peek iterator by one

    for spin_count, bankroll in enumerate(strategy_iter, 1):
        peek = next(peek_iter, None)
        app.logger.warning(f"run_simulation peek results: {peek}")

        if spin_count < max_spins:  # First 5 are always printed
            results.append({"spin_count": spin_count, "bankroll": bankroll})
        if spin_count == max_spins or bankroll <= 0 or peek is None:  # Last one is printed
            results.append({"Final": spin_count, "bankroll": bankroll})
        if bankroll <= 0 or spin_count == max_spins or peek is None:
            return results





app = Flask(__name__)
CORS(app, origins=["https://roulette.kevindowling.dev/"])

handler = RotatingFileHandler('/tmp/roulette.log', maxBytes=10000, backupCount=1)
handler.setLevel(logging.WARNING)
app.logger.addHandler(handler)
app.logger.setLevel(logging.WARNING)

@app.errorhandler(Exception)
def handle_exception(e):
    app.logger.error(f"An error occurred: {str(e)}")
    return str(e), 500

@app.before_request
def before_request():
    app.logger.info(f"Received {request.method} request on {request.path} with data: {request.data} and headers: {request.headers}")


@app.route('/api/simulate', methods=['POST'])
def simulate():
    data = request.json
    strategy = data.get('strategy', '').lower()
    initial_bankroll = data.get('bankroll')
    initial_bet = data.get('initialbet')
    max_spins = data.get('maxspins', 100)
    win_limit = data.get('winlimit', 3)
    sequence = [int(x) for x in data.get('sequence', [])]

    
    # Mapping strategy names to corresponding functions
    strategies = {
        'mart': run_martingale_simulation,
        'rev': run_reverse_martingale_simulation,
        'dale': run_dalembert_simulation,
        'labo': run_labouchere_simulation,
        'fibo': run_fibonacci_simulation,
        'osca': run_oscars_grind_simulation
    }
    
    strategy_func = strategies.get(strategy)
    if not strategy_func:
        return jsonify(error=f"Invalid strategy: {strategy}"), 400
    
    # Running the selected strategy with the required parameters
    try:
        if strategy.startswith('mart'):
            results = run_simulation(strategy_func, initial_bankroll, initial_bet, max_spins=max_spins)
        elif strategy.startswith('rev'):
            results = run_simulation(strategy_func, initial_bankroll, initial_bet, win_limit, max_spins=max_spins)
        elif strategy.startswith('dale'):
            results = run_simulation(strategy_func, initial_bankroll, initial_bet, max_spins=max_spins)
        elif strategy.startswith('labo'):
            if not sequence:
                return jsonify(error="Sequence is required for Labouchere System"), 400
            results = run_simulation(strategy_func, initial_bankroll, sequence, max_spins=max_spins)
        elif strategy.startswith('fibo'):
            results = run_simulation(strategy_func, initial_bankroll, initial_bet, max_spins=max_spins)
        elif strategy.startswith('osca'):
            results = run_simulation(strategy_func, initial_bankroll, initial_bet, max_spins=max_spins)
        else:
            return jsonify(error="Something went wrong!"), 500
        
        return jsonify(results=results)
    except Exception as e:
        return jsonify(error=str(e)), 500

if __name__ == "__main__":  
    app.run(debug=True)


