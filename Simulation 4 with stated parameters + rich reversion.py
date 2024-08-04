import random

class Individual:
    def __init__(self, type, income, initially_rich=False):
        self.type = type  # 'type1', 'type2', or 'rich'
        self.income = income
        self.savings = 0
        self.initially_rich = initially_rich

    def update_income(self):
        if self.type == 'type2' or (self.type == 'rich' and not self.initially_rich):
            # Accumulate savings from the previous period's income
            self.savings += 0.2 * self.income  
            # Calculate income for the next period
            self.income = 100 + self.savings * 1.06  
            if self.type == 'rich' and self.income < 1000 and not self.initially_rich:
                self.type = 'type2'  # Revert to type 2 if income drops below 1000 for newly rich individuals
        elif self.type == 'type1':
            self.income = 100  # Type 1 income resets every period

    def adjust_income(self, loss):
        self.income -= loss
        if self.income < 1000 and self.type == 'rich' and not self.initially_rich:
            self.type = 'type2'
            # Do not reset income or savings

def interact(individuals, round):
    total = len(individuals)
    type1_count = sum(1 for x in individuals if x.type == 'type1')
    type2_count = sum(1 for x in individuals if x.type == 'type2')
    rich_count = sum(1 for x in individuals if x.type == 'rich' and x.initially_rich)
    newly_rich_count = sum(1 for x in individuals if x.type == 'rich' and not x.initially_rich)

    for person in individuals:
        if person.type == 'type1':
            other = random.choice(individuals)
            if round == 1:  # First round interactions
                if other.type == 'rich' and random.random() < rich_count / total:
                    if random.random() < 0.2:  # 20% chance to mimic investment behavior of type 2 and become type 2
                        person.type = 'type2'
                        person.income = 100
                elif other.type == 'type1':
                    continue  # Explicitly noting that type 1 remains type 1
            else:  # Subsequent rounds
                if other.type in ['rich', 'type2', 'rich' and not other.initially_rich] and random.random() < (rich_count + type2_count + newly_rich_count) / total:
                    if random.random() < 0.2:  # 20% chance to mimic investment behavior of type 2 and become type 2
                        person.type = 'type2'
                        person.income = 100
                elif other.type == 'type1':
                    continue  # Maintaining type 1 status
        elif person.type == 'type2':
            other = random.choice(individuals)
            if other.type in ['rich', 'type2', 'rich' and not other.initially_rich] and random.random() < (rich_count + type2_count + newly_rich_count) / total:
                continue  # Maintaining type 2 status
            if other.type == 'type1' and random.random() < type1_count / total:
                if random.random() < 0.1:  # 10% chance to revert to type 1
                    person.type = 'type1'
                    person.income = 100  # Reverting to initial income of Type 1
            if person.income > 1000:  # Check if person becomes rich
                person.type = 'rich'
                person.initially_rich = False  # Mark as newly rich
        
        elif person.type == 'rich' and  not person.initially_rich: # Only apply to newly rich
            other = random.choice(individuals)            
            if other.type == 'type1' and random.random() < type1_count / total:
                if random.random() < 0.05:
                    person.adjust_income(100)  # Lose 100 when meeting type 1 because copies consumption behavior of type 1
            elif other.type == 'type2' and random.random() < type2_count / total:
                if random.random() < 0.05:
                    person.adjust_income(80)  # Lose 80 when meeting type 2 because copies consumption behavior of type 2
            # Check for reversion to type 2 if income drops below 1000
            if person.income < 1000:
                person.type = 'type2'
        
    # Check for individuals becoming newly rich
    for person in individuals:
        if person.income >= 1000 and person.type == 'type2':
            person.type = 'rich'
            person.initially_rich = False  # Mark as newly rich


def simulate_neighborhood(num_periods):
    # Initialize the population with type1 and rich individuals only
    individuals = [Individual('type1', 100) for _ in range(100)] + [Individual('rich', 1000, True) for _ in range(30)]
    history = []

    for current_round in range(num_periods):
        for ind in individuals:
            ind.update_income()  # Update income based on type

        # Correctly handle interactions for the day
        interact(individuals, current_round + 1)  # Pass current round number, adjusted for 1-based counting

        # Record the state after today's interactions and updates
        type1_count = sum(1 for x in individuals if x.type == 'type1')
        type2_count = sum(1 for x in individuals if x.type == 'type2')
        rich_count = sum(1 for x in individuals if x.type == 'rich' and x.initially_rich)
        newly_rich_count = sum(1 for x in individuals if x.type == 'rich' and not x.initially_rich)
        newly_rich_incomes = [(ind.income) for ind in individuals if ind.type == 'rich' and not ind.initially_rich]  # Collect newly rich incomes
        type2_incomes = [(ind.income) for ind in individuals if ind.type == 'type2']  # Collect Type 2 incomes
        history.append((type1_count, type2_count, rich_count, newly_rich_count, type2_incomes, newly_rich_incomes)) # Store counts and incomes

    return history, individuals

# Run the simulation for 30 periods
history, individuals = simulate_neighborhood(30)

# Print results
for day, (type1, type2, rich, newly_rich, type2_incomes, newly_rich_incomes) in enumerate(history, start=1):
    print(f"Day {day}: Type 1 - {type1}, Type 2 - {type2}, Rich - {rich}, Newly Rich - {newly_rich}")
    print(f"  Type 2 Incomes for Day {day}: {type2_incomes}")
    print(f"  Newly Rich Incomes for Day {day}: {newly_rich_incomes}")

