import argparse
from itertools import islice
import random





def run_martingale_simulation(initial_bankroll, initial_bet):
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

def run_dalembert_simulation(initial_bankroll, initial_bet):
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
        results.append(bankroll)

    return results

def run_fibonacci_simulation(initial_bankroll, initial_bet):
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
    number = random.randint(0, 36)
    return 'win' if number % 2 == 0 else 'loss'

def run_simulation(strategy_func, *args, **kwargs):
    max_spins = kwargs.get('max_spins', 100)  # You can set a default value or manage it differently
    
    strategy_results = strategy_func(*args, **kwargs)  # Store the result of strategy_func in a separate variable
    
    # Initialize results list to store the dictionaries
    results = []
    for spin_count, bankroll in enumerate(strategy_results, 1):
        peek = next(islice(strategy_results, 1, 2), None)
        if spin_count < 5: #First 5 are always printed
            results.append({"spin_count": spin_count, "bankroll": bankroll})
            print(f"Spin {spin_count}: {bankroll}")
        if spin_count % 10 == 0: #Every 10th is printed
            results.append({"spin_count": spin_count, "bankroll": bankroll})
            print(f"Spin {spin_count}: {bankroll}")
        if spin_count == max_spins or bankroll <= 0: #Last one is printed
            results.append({"spin_count": spin_count, "bankroll": bankroll})
            print(f"Spin {spin_count}: {bankroll}")
        if bankroll <= 0 or spin_count == max_spins or not peek:
            return results
        






def main():
    print("Main Called")
    parser = argparse.ArgumentParser(description='Roulette Strategy Simulation')
    parser.add_argument('-s', '--strategy', type=str, required=True, help='Name of the strategy to simulate')
    parser.add_argument('-b', '--bankroll', type=int, required=True, help='Initial bankroll')
    parser.add_argument('-bet', '--initial_bet', type=int, required=True, help='Initial bet amount')
    parser.add_argument('-m', '--max_spins', type=int, default=100, help='Maximum number of spins')
    parser.add_argument('-w', '--win_limit', type=int, default=3, help='Win limit for Reverse Martingale Strategy')
    parser.add_argument('-seq', '--sequence', nargs='+', type=int, default= [1,2,3], help='List of numbers for Labouchere System')
    
    args = parser.parse_args()
    strategy = args.strategy.lower()
    
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
        print(f"Invalid strategy: {strategy}")
        return
    
    # Running the selected strategy with the required parameters
    if strategy.startswith('mart'):
        run_simulation(strategy_func, args.bankroll, args.initial_bet, max_spins=args.max_spins)
    elif strategy.startswith('rev'):
        run_simulation(strategy_func, args.bankroll, args.initial_bet, args.win_limit, max_spins=args.max_spins)
    elif strategy.startswith('dale'):
        run_simulation(strategy_func, args.bankroll, args.initial_bet, max_spins=args.max_spins)
    elif strategy.startswith('labo'):
        if not args.sequence:
            print("Sequence is required for Labouchere System")
            return
        run_simulation(strategy_func, args.bankroll, args.sequence, max_spins=args.max_spins)
    elif strategy.startswith('fibo'):
        run_simulation(strategy_func, args.bankroll, args.initial_bet, max_spins=args.max_spins)
    elif strategy.startswith('osca'):
        run_simulation(strategy_func, args.bankroll, args.initial_bet, max_spins=args.max_spins)
    else:
        print("Something went wrong!")

if __name__ == "__main__":
    main()