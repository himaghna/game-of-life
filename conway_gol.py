"""
@uthor: Himaghna, 8th August 2019
Description: Implement Conway's game of life
"""

from argparse import ArgumentParser
import json
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np


# parameters
ON = 255
OFF = 0
VALS = [ON, OFF]

def load_config(config_filepath):
    """
    load configurations from config file and return to calling method as dict
    config_filepath: (str) filepath of json  config file
    """
    with open(config_filepath, "r") as config_file:
        config = json.load(config_file)
    return config

def generate_random_grid(N, p_ON):
    """
    generate a random grid of size N8N with ON probability = 0.2
    N: (int) size of grid
    """
    return np.random.choice(VALS, N*N, p=[p_ON, (1-p_ON)]).reshape(N, N)

def add_glider(grid, N):
    """
    add a glider to the top left corener of the grid
    grid: (numpy N*N ndarray) the game board
    N: (int) size of the grid
    """
    glider = np.zeros(5*5).reshape(5,5)
    glider[1,2] = ON
    glider[2,0] = ON
    glider[2,2] = ON
    glider[3,1] = ON
    glider[3,2] = ON
    


def update(frameNum, img, grid, N):
    """
    update function for the animation
    img: pyplot object
    grid: (numpy N*N ndarray) the game board
    N: (int) size of the grid
    """
    new_grid = grid.copy()
    for i in range(N):
        for j in range(N):
            # the x and y axes wrap around
            surround_population = int(
                (grid[i, (j+1)%N] + grid[i, (j-1)%N] +
                grid[(i+1)%N, j] + grid[(i-1)%N, j] +
                grid[(i+1)%N, (j+1)%N] + grid[(i-1)%N, (j-1)%N] +
                grid[(i-1)%N, (j+1)%N] + grid[(i+1)%N, (j-1)%N]) / ON)
            
            # Conway's rules
            if new_grid[i, j] == ON:
                if (surround_population < 2) or (surround_population > 3):
                    new_grid[i,j] = OFF
            else:
                if surround_population == 3:
                    new_grid[i,j] = ON
    grid[:] = new_grid[:]
    img.set_data(grid)
    return img,



def main(): 
  
    # Command line args are in sys.argv[1], sys.argv[2] .. 
    # sys.argv[0] is the script name itself and can be ignored 
    # parse arguments 
    parser = ArgumentParser(description="Runs Conway's Game of Life simulation.") 
  
    # add arguments 
    parser.add_argument('--grid_size', dest='N', required=False) 
    parser.add_argument('--interval', dest='interval', required=False)
    parser.add_argument('--p_on', dest='p_ON', required=False, default=0.15)
    args = parser.parse_args() 
      
    # set grid size 
    N = 100
    if args.N and int(args.N) > 8: 
        N = int(args.N) 
          
    # set animation update interval 
    updateInterval = 50
    if args.interval: 
        updateInterval = int(args.interval)
    
    # declare grid
    grid = np.array([])
    p_ON = 0.15
    if  args.p_ON >= 0 and args.p_ON <=1:
        p_ON = args.p_ON 
    grid = generate_random_grid(N, p_ON)

    # set up animation
    fig, ax = plt.subplots()
    img = ax.imshow(grid, interpolation='nearest')
    ani = animation.FuncAnimation(fig, update, fargs=(img, grid, N,), frames=500, interval=updateInterval)

    plt.show()

if __name__ == '__main__':
    main()

    
    


            
            

