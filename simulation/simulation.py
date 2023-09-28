import random
import time
import matplotlib.pyplot as plt

import matplotlib.animation as animation

import numpy as np

#Agent-definition
class Agent:
    def __init__(self, agent_id, health, hunger, stamina, food, damage, money, x, y):
        self.agent_id = agent_id
        self.health = health
        self.hunger = hunger
        self.stamina = stamina
        self.food = food
        self.damage = damage
        self.money = money
        self.num_movements = 0
        self.sleep_time = 0
        self.is_alive = True
        self.x = x  # Agent's x-coordinate in the virtual space
        self.y = y  # Agent's y-coordinate in the virtual space

        # Interaction history to track rewards
        self.interaction_history = {"trade": 0, "attack": 0, "ignore": 0}
        self.health_history = []  # List to record health over time
        self.hunger_history = []  # List to record hunger over time
        self.stamina_history = []  # List to record stamina over time
        self.food_history = []  # List to record food over time
        self.damage_history = []  # List to record damage over time
        self.money_history = []  # List to record money over time
        self.stamina_zero_days = 0  # Count of consecutive days with zero stamina



    def update_history(self):
        # Record the current values of agent attributes
        self.health_history.append(self.health)
        if(self.health == 0 or (self.stamina == 0 )):
            self.health_history.append(0)
            self.is_alive == False
            self.hunger_history.append(0)
            self.food_history.append(0)
            self.damage_history.append(0)
            self.money_history.append(0)
            self.stamina_history.append(0)

        else:

            self.hunger_history.append(self.hunger)
            self.food_history.append(self.food)
            self.damage_history.append(self.damage)
            self.money_history.append(self.money)
            self.stamina_history.append(self.stamina) 

        


    def take_damage(self, damage):
        if damage > 0:
            self.health -= damage
            if self.health <= 0:
                self.health = 0
                self.is_alive = False

    def eat(self):
        if self.food > 0 and self.hunger>=0:
            self.hunger -= self.food * 0.3
            self.stamina += self.food * 0.4

            self.food -= 1

    def rest(self):
        if self.is_alive:
            # Modify stamina and health based on sleep time
            sleep_time = 3  # Agent can only sleep up to their current stamina
            self.stamina += sleep_time * 0.5
            self.health += sleep_time * 0.2  # Sleeping restores health

    def move(self):
        if not self.is_alive or self.stamina == 0:
            return  # Don't move if the agent is dead or has zero stamina

        # Randomly update the agent's position with some bounds
        self.x += random.uniform(-1, 1)
        self.y += random.uniform(-1, 1)
        self.x = max(0, min(self.x, 99))  # Ensure agents stay within the virtual space bounds (0 to 99)
        self.y = max(0, min(self.y, 99))

        self.stamina -=1
        self.num_movements += 1


        if self.stamina == 0:
            self.health = 0
            self.is_alive = False

    def move_or_rest(self):
        if(self.agent_id == 1):
            self.move()

        #Raw decision-making base on random behaviour
        choice = random.choice(["move","rest"])
        if(self.stamina >=100):
            self.move()
        elif(self.stamina == 0):
            self.rest() 


        elif (choice == "move"):
            self.move()
        elif(choice == "rest"): 
            self.rest()
            self.eat()

        

    
    def attack(self, other_agent):
        if self.is_alive and other_agent.is_alive:
            damage = random.randint(5, 20)
            other_agent.take_damage(damage)
            print(f"Agent {self.agent_id} attacked Agent {other_agent.agent_id} for {damage} damage.")

    def trade(self, other_agent):
        if self.is_alive and other_agent.is_alive:
        # Check if there's enough food and money to trade
            max_food_to_trade = min(self.food, other_agent.food)
            max_money_to_trade = min(self.money, other_agent.money)

            if max_food_to_trade > 0 and max_money_to_trade > 0:
                food_to_trade = random.randint(1, max_food_to_trade)
                money_to_trade = random.randint(1, max_money_to_trade)

                self.food -= food_to_trade
                self.money += money_to_trade

                other_agent.food -= food_to_trade
                other_agent.money += money_to_trade


                print(f"Trade between Agent {self.agent_id} and Agent {other_agent.agent_id}:\n"
                    f"Agent {self.agent_id} gave {money_to_trade} food and received {food_to_trade} money.\n"
                    f"Agent {other_agent.agent_id} gave {food_to_trade} money and received {money_to_trade} food.")
            else:
                print("Trade cannot occur due to insufficient resources.")

            

    def ignore(self, other_agent):
        print(f"Agent {self.agent_id} ignored Agent {other_agent.agent_id}.")

    def plot_agent(self, ax):
        # Plot the agent as a point on the virtual space
        ax.plot(self.x, self.y, marker='o', markersize=8, label=f'Agent {self.agent_id}')


def calculate_distance(agent1, agent2):
    # Calculate the Euclidean distance between two agents in the virtual space
    return ((agent1.x - agent2.x) ** 2 + (agent1.y - agent2.y) ** 2) ** 0.5

def animate_simulation(agents,simulation_duration):
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)

    def update(frame):
        ax.clear()
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)
        ax.set_xlabel('X Coordinate')
        ax.set_ylabel('Y Coordinate')
        ax.set_title(f'Simulation Day: {frame + 1}')

        for agent in agents:
            agent.update_history()
            agent.move_or_rest()
            agent.plot_agent(ax)

    ani = animation.FuncAnimation(fig, update, frames=simulation_duration, repeat=False)
    plt.show()

def agent_interaction(agent1, other_agent):
    distance = calculate_distance(agent1, other_agent)

    if distance <= 2:
        
            # Determine the type of encounter
        encounter_type = random.choice(["trade", "attack", "ignore"])
        agent1.interaction_history[encounter_type] += 1
        other_agent.interaction_history[encounter_type] += 1

        if encounter_type == "trade":
            agent1.trade(other_agent)
        elif encounter_type == "attack":
            agent1.attack(other_agent)
        else:
            agent1.ignore(other_agent)


      



def generate_random_agents(num_agents, virtual_space_size):
    agents = []
    for agent_id in range(1, num_agents + 1):
        health = random.randint(50, 100)
        hunger = random.randint(30, 70)
        stamina = random.randint(60, 90)
        food = random.randint(5, 20)
        damage = random.randint(10, 30)
        money = random.randint(0, 5)
        x = random.randint(0, virtual_space_size - 1)  # Random initial x-coordinate within the virtual space bounds
        y = random.randint(0, virtual_space_size - 1)  # Random initial y-coordinate within the virtual space bounds
        agent = Agent(agent_id, health, hunger, stamina, food, damage, money, x, y)
        agents.append(agent)
    return agents

def initialize_virtual_space(virtual_space_size):
    virtual_space = [[None for _ in range(virtual_space_size)] for _ in range(virtual_space_size)]
    return virtual_space

def place_agents_in_virtual_space(agents, virtual_space):
    for agent in agents:
        virtual_space[int(agent.x)][int(agent.y)] = agent
    return virtual_space


def visualize_interactions(agent):
    interaction_types = list(agent.interaction_history.keys())
    interaction_counts = list(agent.interaction_history.values())

    plt.figure(figsize=(10, 5))
    plt.bar(interaction_types, interaction_counts)
    plt.xlabel('Interaction Type')
    plt.ylabel('Frequency')
    plt.title(f'Agent {agent.agent_id} Interaction History')
    plt.grid(axis='y')
    plt.show()



def calculate_mean_interactions(agents):
    interaction_history = {"trade": 0, "attack": 0, "ignore": 0}
    num_agents = len(agents)

    for agent in agents:
        for interaction_type, count in agent.interaction_history.items():
            interaction_history[interaction_type] += count

    for interaction_type in interaction_history:
        interaction_history[interaction_type] /= num_agents

    return interaction_history


def count_alive(agents):
    num_alive = 0
    num_dead = 0


    for agent in agents:
        if(agent.is_alive == True):
            num_alive +=1
        elif(agent.is_alive == False):
            num_dead += 1

    return num_alive,num_dead


def plot_agent_attributes_over_time(agents):

    for agent in agents:
    
        plt.figure(figsize=(15, 10))

        plt.plot(agent.health_history, label=f'Agent {agent.agent_id} Health')
        plt.plot(agent.hunger_history, label=f'Agent {agent.agent_id} Hunger')
        plt.plot(agent.stamina_history, label=f'Agent {agent.agent_id} Stamina')
        plt.plot(agent.food_history, label=f'Agent {agent.agent_id} Food')
        plt.plot(agent.damage_history, label=f'Agent {agent.agent_id} Damage')
        plt.plot(agent.money_history, label=f'Agent {agent.agent_id} Money')

        plt.xlabel('Time (Days)')
        plt.ylabel('Value')
        plt.title('Agent Attributes Over Time')
        plt.legend()
        plt.grid(True)
        plt.show()

import csv

def save_interaction_history_to_csv(agents):
    with open('interaction_history_ignore.csv', mode='w', newline='') as csv_file:
        fieldnames = ['Agent_ID', 'Is_Alive', 'Trade_Count', 'Attack_Count', 'Ignore_Count','Num_Movements']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        writer.writeheader()
        for agent in agents:
            writer.writerow({
                'Agent_ID': agent.agent_id,
                'Is_Alive': agent.is_alive,
                'Trade_Count': agent.interaction_history['trade'],
                'Attack_Count': agent.interaction_history['attack'],
                'Ignore_Count': agent.interaction_history['ignore'],
                'Num_Movements':agent.num_movements
            })


def run_simulation():
    num_agents = 5000
    virtual_space_size = 500  # Size of the virtual space (matrix)
    agents = generate_random_agents(num_agents, virtual_space_size)
    virtual_space = initialize_virtual_space(virtual_space_size)
    virtual_space = place_agents_in_virtual_space(agents, virtual_space)


    interactions_over_time = []
    deaths_over_time = []
    
    simulation_duration = 60  # 60 seconds (1 minute) total simulation time
    days_per_second = 10     # 10 days per second
    start_time = time.time()



    while time.time() - start_time < simulation_duration:
        elapsed_time = time.time() - start_time
        current_day = int(elapsed_time * days_per_second)

        interactions = 0
        deaths = 0

        print(f"Day {current_day + 1}:")
        for agent1 in agents:
            
            agent1.update_history()


            for agent2 in agents:
                if agent1 != agent2:  # Ensure agents don't interact with themselves
                    agent_interaction(agent1, agent2)
                    

            # Move agents
            agent1.move_or_rest()

            if not agent1.is_alive:
                deaths += 1

        interactions_over_time.append(interactions)
        deaths_over_time.append(deaths)


        
        

        time.sleep(1 / days_per_second)  # Sleep for 1 day's duration

    print("Simulation completed.")

    print("Number of agents alive",count_alive(agents))
        
    

    mean_interactions = calculate_mean_interactions(agents)
    print("Mean Interaction Counts:")
    for interaction_type, mean_count in mean_interactions.items():
        print(f"{interaction_type}: {mean_count:.2f}")

    plt.figure(figsize=(10, 5))
    plt.plot(range(1, len(interactions_over_time) + 1), interactions_over_time, label='Interactions')
    plt.xlabel('Day')
    plt.ylabel('Number of Interactions')
    plt.title('Interactions Between Agents Over Time')
    plt.legend()
    plt.grid(True)
    plt.show()

    # Plot deaths over time
    plt.figure(figsize=(10, 5))
    plt.plot(range(1, len(deaths_over_time) + 1), deaths_over_time, label='Deaths')
    plt.xlabel('Day')
    plt.ylabel('Number of Deaths')
    plt.title('Agent Deaths Over Time')
    plt.legend()
    plt.grid(True)
    plt.show()
    #======================================================================

    # Plot agent attributes over time
    save_interaction_history_to_csv(agents)
    #animate_simulation(agents, int(simulation_duration * days_per_second))
    #plot_agent_attributes_over_time(agents)
    



# Run the simulation
if __name__ == "__main__":
    run_simulation()
