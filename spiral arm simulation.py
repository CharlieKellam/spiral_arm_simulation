import numpy as np
import matplotlib.pyplot as plt

Nr = 110 # Number of rings
time = 30  # Number of time steps
v = 3  # Velocity
spread_prob = 0.314  # Probability that an "on" cell activates a neighbor

# Initialize with random active cells at t=0 (favoring "off")
active_cells = {}
for i in range(Nr):
    Nc = 6 * (i + 1) - 2  # Number of cells in this ring
    active_cells[i] = np.random.choice([0, 1], size=Nc, p=[0.99, 0.01])  # 1% chance of being "on"

# Function to update states (one-time activation per cell)
def update_states(active_cells):
    new_active_states = {}  # Only store new activations

    for i in range(Nr):
        Nc = 6 * (i + 1) - 2  # Number of cells in this ring
        new_active_states[i] = np.zeros(Nc, dtype=int)  # Start fresh

        for j in range(Nc):
            if active_cells[i][j] == 1:  # If this cell is "on", spread activation
                
                # Same-ring neighbors
                left = (j - 1) % Nc
                right = (j + 1) % Nc
                if np.random.rand() < spread_prob:
                    new_active_states[i][left] = 1
                if np.random.rand() < spread_prob:
                    new_active_states[i][right] = 1

                # Inner-ring neighbors
                if i > 0:
                    inner_Nc = 6 * i - 2
                    inner_j = int(j * inner_Nc / Nc)
                    inner_neighbors = [inner_j, (inner_j + 1) % inner_Nc]
                    for k in inner_neighbors:
                        if np.random.rand() < spread_prob:
                            new_active_states[i - 1][k] = 1

                # Outer-ring neighbors
                if i < Nr - 1:
                    outer_Nc = 6 * (i + 2) - 2
                    outer_j = int(j * outer_Nc / Nc)
                    outer_neighbors = [outer_j, (outer_j + 1) % outer_Nc]

                    if i + 1 not in new_active_states:
                        new_active_states[i + 1] = np.zeros(outer_Nc, dtype=int)

                    for k in outer_neighbors:
                        if 0 <= k < outer_Nc and np.random.rand() < spread_prob:
                            new_active_states[i + 1][k] = 1  # Activate outer neighbor

    return new_active_states  # Only return new activations

# Run simulation
for t in range(time):
    plt.figure(figsize=(6, 6), dpi=100)
    ax = plt.subplot(111, projection='polar')

    circle_data = {}

    for i in range(Nr):
        r = i + 1
        dtheta = t / r
        Nc = 6 * (i + 1) - 2
        cell = np.linspace(0, 2 * np.pi, Nc, endpoint=False)
        theta = cell + v * dtheta
        r_values = np.full_like(theta, r)
        on_off_values = active_cells[i]  # Only show active cells

        circle_data[f"circle_{r}"] = (theta, r_values, on_off_values)

    # Plot active cells
    for key, (theta, r, on_off) in circle_data.items():
        theta_on = theta[on_off == 1]
        r_on = r[on_off == 1]
        ax.scatter(theta_on, r_on, color='k', s=10)

    ax.grid(False)
    plt.title("Time="+str(t)+"  Velocity="+str(v)+"  Spread prob="+str(spread_prob), fontsize=18) 
    plt.show(block=False)
    
    # Update to only show new activations
    active_cells = update_states(active_cells)
