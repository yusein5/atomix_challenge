import random
import simpy

#Initialising the class with constructor, attributes and methods.
class LendingPlatform:
    def __init__(self, env):
        self.env = env
        self.borrowers = []
        self.investors = []
        self.reserve_pool = 0
        self.total_borrowed = 0
        self.total_invested = 0

    def add_borrower(self, amount, duration):
        self.borrowers.append((amount, duration))
        self.total_borrowed += amount
        self.reserve_pool += amount

    def add_investor(self, amount, duration):
        self.investors.append((amount, duration))
        self.total_invested += amount

    def remove_borrower(self, amount):
        self.borrowers.remove(amount)
        self.reserve_pool -= amount

    def remove_investor(self, amount):
        self.investors.remove(amount)

    def process_borrower(self, amount, duration):
        yield self.env.timeout(duration)
        self.remove_borrower((amount, duration))
        print(f"Borrower repaid £{amount:.2f} after {duration} months")

    def process_investor(self, amount, duration):
        yield self.env.timeout(duration * 30)  # Random investment period in days
        self.remove_investor((amount, duration))
        print(f"Investor withdrew £{amount:.2f} after {duration} months")

    def simulate(self, num_years):
        num_days = num_years * 365

        for day in range(num_days):
            # Randomly determine the number of new borrowers and investors for the day
            num_new_borrowers = random.randint(0, 4)
            num_new_investors = random.randint(0, 4)

            # Add new borrowers
            for _ in range(num_new_borrowers):
                amount_borrowed = round(random.uniform(0.5, 1.5) * 80000, 2)
                duration = random.randint(1, 12)
                self.add_borrower(amount_borrowed, duration)
                self.env.process(self.process_borrower(amount_borrowed, duration))
                print(f"A new borrower joined: borrowed £{amount_borrowed:.2f} for {duration} months")

            # Add new investors
            for _ in range(num_new_investors):
                amount_invested = round(random.uniform(0.8, 1.2) * 100000, 2)
                duration = random.randint(1, 12)
                self.add_investor(amount_invested, duration)
                self.env.process(self.process_investor(amount_invested, duration))
                print(f"A new investor joined: invested £{amount_invested:.2f} for {duration} months")

            # Print global statistics
            print(f"Total amount borrowed: £{self.total_borrowed:.2f}")
            print(f"Total amount invested: £{self.total_invested:.2f}")
            print(f"Reserve pool: £{self.reserve_pool:.2f}\n")

# Create simulation environment
env = simpy.Environment()

# Create an instance of the LendingPlatform class
lending_platform = LendingPlatform(env)


# Ask the user for the duration and then run the simulation
duration_unit = input("Enter the duration unit (days/months/years): ")

# Ask the user for the duration value
duration_value = int(input(f"Enter the number of {duration_unit} for the simulation: "))

# Convert the duration to the equivalent number of days
if duration_unit.lower() == "months":
    num_days = duration_value * 30
elif duration_unit.lower() == "years":
    num_days = duration_value * 365
else:
    num_days = duration_value

# Run the simulation for the specified duration
lending_platform.simulate(num_days)

