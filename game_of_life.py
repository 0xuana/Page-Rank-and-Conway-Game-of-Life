import sys
import numpy as np
import matplotlib.pylab as plt
from matplotlib.animation import FuncAnimation, PillowWriter, FFMpegWriter


def loc_correcting(loc_r, loc_c, matrix):
    """
    This function correcting the out of range problems happens when finding neighbours
    
    Parameters:
    loc_r: The row number of the location
    loc_c: The column number of the location
    matrix (int,int): the matrix of_r and loc_c should locate
    
    Returns:
    (int, int): the correcting location not out of range
    """
    row, column = matrix.shape
    
    if (loc_r < 0):
        loc_r += row
    elif (loc_r >= row):
        loc_r -= row
        
    if (loc_c < 0):
        loc_c += column
    elif (loc_c >= column):
        loc_c -= column
    
    return (loc_r, loc_c)

def alive(loc, matrix):
    """
    This function test wheather the cell given in the location will alive or not in the next generation.
    
    Parameters:
    loc (list: int): The cell location in the matrix
    matrix (n by m numpy.ndarray): Cell survive information carrier
    
    Returns:
    bool: Return the cell will alive or not for the next generation.
    """
    row, column = matrix.shape
    loc_r, loc_c = loc
    
    neigh_alive = matrix[loc_correcting(loc_r + 1, loc_c + 1, matrix)] + matrix[loc_correcting(loc_r + 1, loc_c + 0, matrix)] + matrix[loc_correcting(loc_r + 1, loc_c - 1, matrix)] + matrix[loc_correcting(loc_r + 0, loc_c + 1, matrix)] + matrix[loc_correcting(loc_r + 0, loc_c - 1, matrix)] + matrix[loc_correcting(loc_r - 1, loc_c + 1, matrix)] + matrix[loc_correcting(loc_r - 1, loc_c + 0, matrix)] + matrix[loc_correcting(loc_r - 1, loc_c - 1, matrix)]
    
    if (matrix[loc] and (neigh_alive == 2 or neigh_alive == 3)):
        return True
    elif (not matrix[loc] and neigh_alive == 3):
        return True
    
    return False

def evolve(matrix):
    """
    This function makes the evolve of the Conway's Game Life it generate the next iteration based on the previous matrix.
    
    Parameters:
    matrix (n by m numpy ndarray): the input matrix for the game.
    
    Returns:
    n by m numpy ndarray: The next iter of the matrix.
    """
    row, column = matrix.shape
    next_generation_matrix = matrix.copy()
    
    for i in range(row):
        for j in range(column):
            next_generation_matrix[i,j] = alive((i,j), matrix)
    
    return next_generation_matrix

def plot_bool_matrix(matrix):
    # Sample boolean matrix
    # matrix = np.array([[True, False, True], [False, True, False], [True, True, False]])

    # Convert boolean values to integers for plotting (True->1 and False->0)
    # int_matrix = matrix.astype(int)

    # Create a figure and axis object
    fig, ax = plt.subplots()
    
    # Use the imshow function to visualize the matrix
    # cmap='gray' gives a black and white colormap
    cax = ax.imshow(matrix, cmap='gray_r', interpolation='nearest')    

    # Optionally, you can set x and y ticks to be more clear about matrix indices
    ax.set_xticks(np.arange(len(matrix[0])))
    ax.set_yticks(np.arange(len(matrix)))
    ax.set_xticklabels(np.arange(len(matrix[0])))
    ax.set_yticklabels(np.arange(len(matrix)))

    # Optionally, add grid for clarity
    # ax.grid(which='both', color='lightgray', linewidth=0.5)

    # Remove the grid lines from topmost and rightmost position
    ax.set_xticks(np.arange(len(matrix[0]) + 1) - 0.5, minor=True)
    ax.set_yticks(np.arange(len(matrix) + 1) - 0.5, minor=True)
    ax.grid(which="minor", color="gray", linestyle='-', linewidth=.5)
    ax.tick_params(which="minor", size=0)

    # Show the plot
    # plt.show()
    return plt.gcf()


def main(k):
    # Your game of life logic here
    print(f"Running Game of Life for {k} iterations...")

    # matrix initialize
    matrix = np.zeros((20,20))
    matrix[9,9] = 1
    matrix[10,10] = 1
    matrix[11,10] = 1
    matrix[11,9] = 1
    matrix[11,8] = 1

    plot_bool_matrix(matrix)

    matrices = []
    movies = []
    matrices.append(matrix)
    movies.append(matrix)

    # Generate the movies for k iterstions
    for i in range(k):
        matrices.append(evolve(matrices[-1]))
        if (i % 10 == 0):
            movies.append(matrices[-1])

    def update(frame):
        ax.clear()  # Clear the current plot
        matrix = matrices[frame]  # Get the current matrix

        # Redraw the plot
        cax = ax.imshow(matrix, cmap='gray_r', interpolation='nearest')
        ax.set_xticks(np.arange(len(matrix[0])))
        ax.set_yticks(np.arange(len(matrix)))
        ax.set_xticklabels(np.arange(len(matrix[0])))
        ax.set_yticklabels(np.arange(len(matrix)))
        ax.set_xticks(np.arange(len(matrix[0]) + 1) - 0.5, minor=True)
        ax.set_yticks(np.arange(len(matrix) + 1) - 0.5, minor=True)
        ax.grid(which="minor", color="gray", linestyle='-', linewidth=.5)
        ax.tick_params(which="minor", size=0)

    # Create a figure and axis object
    fig, ax = plt.subplots()

    # Create an animation
    ani = FuncAnimation(fig, update, frames=len(matrices), repeat=False)

    # Save the animation as an MP4 file
    ani.save("bool_matrices_animation.mp4", writer='ffmpeg', fps=10)

    # # Specify writer and its parameters
    # writer = FFMpegWriter(fps=10, metadata=dict(artist='Lingxuan'), bitrate=1800)

    # # Save the animation using the specified writer
    # ani.save("bool_matrices_animation.mp4", writer=writer)

    # Following lines would plot the matrix of each 10 steps (100 pics for 1000 steps)
    # for x in movies: 
    #     plot_bool_matrix(x); 
    #     plt.show

    # Save the final state of the grid
    return_fig = plot_bool_matrix(matrices[-1])
    return_fig.savefig('game_of_life.png', dpi=700)  # saves the figure with a resolution of 300 dots per inch

    
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python game_of_life.py [num_iterations]")
        sys.exit(1)
    
    num_iterations = int(sys.argv[1])  # Convert the argument from string to integer
    main(num_iterations)


