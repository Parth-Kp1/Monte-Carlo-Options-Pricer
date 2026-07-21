def get_strike_price():
    K = float(input("Enter Strike price: "))
    if K <= 0:
        print("Invalid strike price!")
        K = get_strike_price()
    return K

def get_current_price():
    S_0 = float(input("Enter current price: "))
    if S_0 <= 0:
        print("Invalid current price!")
        S_0 = get_current_price()
    return S_0

def get_volatility():
    sigma = float(input("Enter volatility (per year): "))
    if sigma <= 0:
        print("Invalid volatility.")
        sigma = get_volatility()
    return sigma

def get_time_till_expiry():
    T = float(input("Enter time till expiry (in years): "))
    if T <= 0:
        print("Invalid time!")
        T = get_time_till_expiry()
    return T

def get_risk_free_rate():
    r = float(input("Enter risk-free rate (per year): "))
    if r <= 0:
        print("Invalid rate!")
        r = get_risk_free_rate()
    return r

def is_barrier_option():
    bar_opt = str(input("Barrier option (Yes = '1', No = '2'): "))
    if bar_opt not in ["1", "2"]:
        print("Invalid entry!")
        bar_opt = is_barrier_option()
    return bar_opt

def get_barrier_option_type(bar_opt):
    if bar_opt == "2":
        return "1"
    bar_type = str(input("What type of barrier option (Down and Out = '1', Up and Out = '2', Down and in = '3', Up and in = '4'): "))
    if bar_type not in ["1", "2", "3", "4"]:
        print("Invalid entry!")
        bar_type = get_barrier_option_type(bar_opt)
    return bar_type

def get_barrier_option_price(bar_opt):
    if bar_opt == "2":
        return 1
    bar_price = float(input("Enter price for the barrier: "))
    if bar_price < 0:
        print("Invalid barrier price!")
        bar_price = get_barrier_option_price(bar_opt)
    return bar_price

def get_option_style():
    opt_style = str(input("Enter option style (European = '1', Asian = '2'): "))
    if opt_style not in ["1", "2"]:
        print("Invalid entry!")
        opt_style = get_option_style()
    return opt_style

def get_option_type():
    opt_type = str(input("What is the option type (Call = '1', Put = '2'): "))
    if opt_type not in ["1", "2"]:
        print("Invalid entry!")
        opt_type = get_option_type()
    return opt_type

def get_input_values():
    input_values = {"Strike": get_strike_price(), "Current": get_current_price(), "Volatility": get_volatility(), "Time": get_time_till_expiry(),
                 "Risk-free rate": get_risk_free_rate(), "Barrier option flag": is_barrier_option()} 
    input_values.update({"Barrier option type": get_barrier_option_type(input_values["Barrier option flag"]), 
                     "Barrier option price": get_barrier_option_price(input_values["Barrier option flag"]),
                     "Option style": get_option_style(), "Option type": get_option_type()})
    return input_values

def initialise_inputs():
    program_choice = str(input("Would you like to price an option or compare efficiencies of different pricers "
                                "(Pricing = '1', Efficiencies = '2'): "))
    if program_choice not in ["1", "2"]:
        print("Invalid entry!")
        program_choice = initialise_inputs()
    if program_choice == "1":
        input_values = get_input_values()
    else:
        input_values = {"Strike": 100, "Current": 100, "Volatility": 0.2, 
                        "Time": 1, "Risk-free rate": 0.05, 
                        "Barrier option flag": "2", 
                        "Barrier option type": "1", 
                        "Barrier option price": 1,
                        "Option style": "1", "Option type": "1"}
    input_values["Program choice"] = program_choice
    return input_values