import numpy as np
import scipy.stats as stats
from inputs import initialise_inputs
from analytics import analytics


input_values = initialise_inputs()
K = input_values["Strike"]
S_0 = input_values["Current"]
sigma = input_values["Volatility"]
T = input_values["Time"]
r = input_values["Risk-free rate"]
bar_opt = input_values["Barrier option flag"]
bar_type = input_values["Barrier option type"]
bar_price = input_values["Barrier option price"]
opt_style = input_values["Option style"]
opt_type = input_values["Option type"]
program_choice = input_values["Program choice"]

n_steps = int(252*T)
dt = 1/252

def EuropeanCall(paths, K):
    payoffs = np.maximum(paths[:,-1] - K, 0)
    return payoffs

def EuropeanPut(paths, K):
    payoffs = np.maximum(K - paths[:,-1], 0)
    return payoffs

def AsianCall(paths, K):
    payoffs = np.maximum(np.mean(paths, axis=1) - K, 0)
    return payoffs

def AsianPut(paths, K):
    payoffs = np.maximum(K - np.mean(paths, axis=1), 0)
    return payoffs

def simulate_price_paths(S_0, sigma, r, n_paths, n_steps, dt):
    Z = np.random.standard_normal(size = (n_paths, n_steps))
    drift = (r - 0.5 * (sigma**2)) * dt
    shocks = sigma * np.sqrt(dt) * Z
    S_T = S_0 * np.exp(np.cumsum(drift + shocks, axis = 1))
    paths = np.zeros((n_paths, n_steps + 1))
    paths[:, 0] = S_0
    paths[:, 1:] = S_T
    return paths

def find_payoffs(opt_style, opt_type, paths, K):
    if opt_style == "1":
        if opt_type == "1":
            payoffs = EuropeanCall(paths, K)
        elif opt_type == "2":
            payoffs = EuropeanPut(paths, K)
    elif opt_style == "2":
        if opt_type == "1":
            payoffs = AsianCall(paths, K)
        elif opt_type == "2":
            payoffs = AsianPut(paths, K)
    return payoffs

def barrier_option_payoffs(bar_type, paths, bar_price, payoffs):
    if bar_type == "1":
        crossed_values = np.any(paths <= bar_price, axis=1)
        payoffs[crossed_values] = 0
    elif bar_type == "2":
        crossed_values = np.any(paths >= bar_price, axis=1)
        payoffs[crossed_values] = 0
    elif bar_type == "3":
        crossed_values = np.all(paths > bar_price, axis=1)
        payoffs[crossed_values] = 0
    elif bar_type == "4":
        crossed_values = np.all(paths < bar_price, axis=1)
        payoffs[crossed_values] = 0
    return payoffs

if program_choice == "1":
    n_paths = 100000
    paths = simulate_price_paths(S_0, sigma, r, n_paths, n_steps, dt)
    payoffs = find_payoffs(opt_style, opt_type, paths, K)
    if bar_opt == "1":
        payoffs = barrier_option_payoffs(bar_type, paths, bar_price, payoffs)
    print("Option should be priced at:", str(np.exp(-r * T) * np.mean(payoffs)))

if program_choice == "2":
    analytics(S_0, sigma, r, T, K)