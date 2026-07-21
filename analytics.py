import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt

def black_scholes_pricer(r, sigma, T, S_0, K):
    d2 = ((r - 0.5 * (sigma ** 2)) * T + np.log(S_0 / K)) / (sigma * np.sqrt(T))
    d1 = d2 + sigma * np.sqrt(T)
    analytic_price = S_0 * stats.norm.cdf(d1) - K * np.exp(-r * T) * stats.norm.cdf(d2)
    return analytic_price

def normal_pricer(S_0, sigma, r, n_paths, T, K):
    Z = np.random.standard_normal(size = n_paths)
    drift = (r - 0.5 * (sigma**2)) * T
    shocks = sigma * np.sqrt(T) * Z
    S_T = S_0 * np.exp(drift + shocks)
    normal_payoffs = np.maximum(S_T - K, 0)
    return np.mean(normal_payoffs) * np.exp(-r * T)

def antithetic_pricer(S_0, sigma, r, n_paths, T, K):
    Z_1 = np.random.standard_normal(size = int(n_paths / 2))
    Z_2 = -Z_1
    Z = np.concatenate((Z_1, Z_2), axis = 0)
    drift = (r - 0.5 * (sigma**2)) * T
    shocks = sigma * np.sqrt(T) * Z
    S_T = S_0 * np.exp(drift + shocks)
    antithetic_payoffs = np.maximum(S_T - K, 0)
    return np.mean(antithetic_payoffs) * np.exp(-r * T)

def control_variate_pricer(S_0, sigma, r, n_paths, T, K):
    Z = np.random.standard_normal(size = n_paths)
    drift = (r - 0.5 * (sigma**2)) * T
    shocks = sigma * np.sqrt(T) * Z
    S_T = S_0 * np.exp(drift + shocks)
    payoffs = np.maximum(S_T - K, 0) * np.exp(-r * T)
    cov = np.cov(S_T * np.exp(-r * T), payoffs) [1,0]
    control_payoffs = payoffs - (cov / np.var(S_T * np.exp(-r * T))) * (S_T * np.exp(-r * T) - S_0)
    return np.mean(control_payoffs)

def convergence_plot(r, sigma, T, S_0, K, path_counts, std_dev_dict):
    analytic_price = black_scholes_pricer(r, sigma, T, S_0, K)
    normal_prices = []
    antithetic_prices = []
    control_prices = []
    for n_paths in path_counts:
        normal_prices.append(normal_pricer(S_0, sigma, r, n_paths, T, K))
        antithetic_prices.append(antithetic_pricer(S_0, sigma, r, n_paths, T, K))
        control_prices.append(control_variate_pricer(S_0, sigma, r, n_paths, T, K))
    plt.figure(figsize = (10,6))
    plt.axhline(y = analytic_price, linestyle = '--', label = 'Black-Scholes exact')
    plt.errorbar(path_counts, normal_prices, yerr = 2 * np.array(std_dev_dict["Normal MC Pricer"]), fmt = 'o-', capsize = 5, 
                label='Standard MC (95% CI)')
    plt.errorbar(path_counts, antithetic_prices, yerr = 2 * np.array(std_dev_dict["Antithetic MC Pricer"]), fmt = 'o-', capsize = 5, 
                label='Antithetic MC (95% CI)')
    plt.errorbar(path_counts, control_prices, yerr = 2 * np.array(std_dev_dict["Control Variate MC Pricer"]), fmt = 'o-', capsize = 5, 
                label='Control MC (95% CI)')
    plt.xscale('log')
    plt.title('Monte Carlo convergence: standard vs. antithetic variates')
    plt.xlabel('Number of simulated paths')
    plt.ylabel('Estimated call price')
    plt.legend()
    plt.savefig('convergence_plot.png', dpi = 150, bbox_inches='tight')
    plt.show()


def analytics(S_0, sigma, r, T, K):
    std_dev_dict = {"Normal MC Pricer": [],
                    "Antithetic MC Pricer": [],
                    "Control Variate MC Pricer": []}
    path_counts = [100, 1000, 10000, 100000]
    
    for n_paths in path_counts:
        normal_sims = []
        antithetic_sims = []
        control_sims = []
        for n in range(100):
            normal_sims.append(normal_pricer(S_0, sigma, r, n_paths, T, K))
            antithetic_sims.append(antithetic_pricer(S_0, sigma, r, n_paths, T, K))
            control_sims.append(control_variate_pricer(S_0, sigma, r, n_paths, T, K))
        std_dev_dict["Normal MC Pricer"].append(np.std(normal_sims, ddof = 1))
        std_dev_dict["Antithetic MC Pricer"].append(np.std(antithetic_sims, ddof = 1))
        std_dev_dict["Control Variate MC Pricer"].append(np.std(control_sims, ddof = 1))

    plt.figure(figsize = (10, 6))
    log_n = np.log10(path_counts)
    for label, std_devs in std_dev_dict.items():
        std_devs = np.array(std_devs)
        gradient, intercept = np.polyfit(log_n, np.log10(std_devs), 1)
        variance = std_devs[-1] ** 2 * path_counts[-1]
        plt.plot(path_counts, std_devs, marker = "o",
                label = f"{label}, Gradient={gradient:.2f}, y-intercept={intercept:.2f}, variance={variance:.2f}")
    plt.xscale("log")
    plt.yscale("log")
    plt.xlabel("Number of paths")
    plt.ylabel("Standard deviation")
    plt.title("Standard deviation of MC value against number of paths simulated")
    plt.legend()
    plt.savefig("efficiency_comparison.png", dpi = 150)
    plt.show()

    convergence_plot(r, sigma, T, S_0, K, path_counts, std_dev_dict)