from sys import argv
from copy import deepcopy

def input_analysis():
    """read the input file and pull the prices of cost1(if no sinkhole one hop away),cost2(if there is at least one sinkhole in diagonal axis and there is not in horizontal,vertical
    axis one hop away), cost3(if there is at least one sinkhole in horizontal,vertical axis one hop away) and path information"""
    with open(argv[1],"r") as f1:
        costs = f1.readline().split()
        cost_list = []
        for element in costs:
            cost_list.append(int(element))
        #Take string lines consisting of 1 and 0 as ‘1’ ‘0’ with split one by one and convert them integers with the map function and collect them in path list.
        path = []
        for line in f1:
            path.append(list(map(int,line.split())))
    return cost_list, path

def create_output(path,cost,true_false_map):
    """Create the desired output file. If there is no route to reach any right in the path then write there is no possible route' to the file. If there is a route , write the price of the lowest cost
     to the file and show the first lowest cost route with mark the route with X in the file"""
    if cost == float("inf"):
        with open(argv[2],"w") as f2:
            f2.write("There is no possible route!")
    else:
        with open(argv[2],"w") as f2:
            f2.write("Cost of the route: {}\n".format(cost))
            rows_length, columns_length = len(path), len(path[0])
            #this loops control the passed points in the lowest cost path and mark them with X
            for y in range(rows_length):
                for x in range(columns_length):
                    if true_false_map[y][x]:
                        path[y][x] = "X"
            #the enumerate approach is to handle the problem of extra one character in the output
            for i,my_list in enumerate(path):
                for j,element in enumerate(my_list):
                    f2.write(str(element) + " ") if j < len(my_list) - 1 else f2.write(str(element))
                f2.write("\n") if i < len(path) - 1 else f2.close()

def calculate_the_cost(path,x,y,cost_list):
    """This function take the path,current x and y coordinate and costs' values then checks whether the current cell's 8 possible neighbour cells and assigns the 0's and 1's of the neighbour cells to the diagonal list
    if they are in the diagonal neighbour cells,or to the horizontal-vertical list if they are in the horizontal or vertical neighbour cells. If there are no 0's in the lists then cost1 is returned.
    If there is at least one zero in the diagonal list and there is no 0 in the horizontal-vertical list, cost2 is returned. If there is at least one zero in the horizontal-vertical list,cost3 is returned."""
    rows_length, columns_length = len(path), len(path[0])
    diagonal_list = []
    horizontal_and_vertical_list = []
    if 0 <= x + 1 < columns_length:
        horizontal_and_vertical_list.append(path[y][x+1])
        if 0 <= y + 1 < rows_length:
            diagonal_list.append(path[y+1][x+1])
        if 0 <= y - 1 < rows_length:
            diagonal_list.append(path[y-1][x+1])
    if 0 <= x - 1 < columns_length:
        horizontal_and_vertical_list.append(path[y][x-1])
        if 0 <= y + 1 < rows_length:
            diagonal_list.append(path[y+1][x-1])
        if 0 <= y - 1 < rows_length:
            diagonal_list.append(path[y-1][x-1])
    if 0 <= y - 1 < rows_length:
        horizontal_and_vertical_list.append(path[y-1][x])
    if 0 <= y + 1 < rows_length:
        horizontal_and_vertical_list.append(path[y+1][x])

    if 0 in horizontal_and_vertical_list:
        return cost_list[2]
    elif 0 in diagonal_list:
        return cost_list[1]
    else:
        return cost_list[0]

def find_lowest_cost_path(path, cost_list, x, y, passed_point, total_cost, information_of_lowest_cost_path, path_memory):
    """Recursive function to find the lowest cost path and assign the cost of this path and passed points on the lowest cost path."""
    rows_length, columns_length = len(path), len(path[0])
    #Base case:if we are the rightmost side of the path , control the cost if this is lower than previous cases , change the lowest_cost's information and finish this process else only finish this process
    if x == (columns_length - 1):
        if total_cost < information_of_lowest_cost_path[0]:
            information_of_lowest_cost_path[0] = total_cost
            passed_point_copy = deepcopy(passed_point)
            information_of_lowest_cost_path[1] = passed_point_copy
        return
    if (x,y) in path_memory and path_memory[(x,y)] <= total_cost: #if there is a path to the same cell with less or equal cost, we finish this process for optimisation(because we need lowest value,this process just waste)
        return
    path_memory[(x,y)] = total_cost # put the current position with current cost to the memory dictionary
    if information_of_lowest_cost_path[0] <= total_cost: # if current cost is bigger than or equal to the lowest_cost then finish the process for optimisation(because we need lowest value, this process just waste)
        return
    """Recursion case:Looks all necessary possible paths from the current cell to the rightmost edge using recursion with the following order: right,upper,lower,left.
        Every necessary valid movement is evaluated for its cost, and the function backtracks after find each path to ensure all necessary possibilities are considered."""
    possible_steps = [(1,0),(0,-1),(0,1),(-1,0)] #Next step priority: right, upper, lower, left
    for change_of_x,change_of_y in possible_steps:
        new_x, new_y = x + change_of_x , y + change_of_y
        if 0 <= new_x < columns_length and 0 <= new_y < rows_length and path[new_y][new_x] == 1 and passed_point[new_y][new_x] == False: #Do it if the move is in valid coordinates,in a place without a sinkhole and in a place that has not been crossed before
            passed_point[new_y][new_x] = True #mark as passed(because we are continue with this step)
            cost = calculate_the_cost(path,new_x,new_y,cost_list)
            find_lowest_cost_path(path, cost_list, new_x, new_y, passed_point, total_cost + cost, information_of_lowest_cost_path, path_memory) #do it same things for this step
            passed_point[new_y][new_x] = False #mark as didn't pass(because we are going to the previous step)

def handle_the_problems_of_the_route_finder():
    """Handles the main problems of the route finder algorithm.Bring the costs and path from the input file.Create necessary arguments(information_of_lowest_cost_path list,path_memory dictionary,
    passed point list etc.) and consider all possible starting points with iteration and finally bring total_cost of the lowest cost path and lowest cost path and create the desired output"""
    cost_list, path = input_analysis() #bring the cost_list and path from input_analysis function
    rows_length, columns_length = len(path),len(path[0])
    information_of_lowest_cost_path = [float("inf"),None]
    #Start from the top left corner and go lower one by one
    for start_point in range(rows_length):
        if path[start_point][0] == 1:
            path_memory = {} #Create a dictionary to keep coordinates and their lowest_cost(for optimization)
            #Create passed point map and assign False to every cell in the beginning
            passed_point = []
            for number in range(rows_length):
                passed_point.append([False] * columns_length)
            passed_point[start_point][0] = True #Do the starting point True
            total_cost = calculate_the_cost(path,0,start_point,cost_list)
            find_lowest_cost_path(path,cost_list,0,start_point,passed_point,total_cost,information_of_lowest_cost_path,path_memory)
    create_output(path,information_of_lowest_cost_path[0],information_of_lowest_cost_path[1])

def main():
    handle_the_problems_of_the_route_finder()

if __name__ == "__main__":
    main()