"""
File: pathfinder_v2.py
Author: Xander Hunt
Purpose: Using the arcade library display a grid, user clicks start and end points and draws barriers if desired. Program finds
fastest way from start to finish.
CSE 111 final project
Items to change:
    Make the system not start pathfinding until a beginning and end have been selected
    Fix it so it actually ends if ending isn't found, this would kinda mitigate this ^ problem
    ^ when these are implemented remove kind error message
    Add functionality to watch the path grow
    While watching path grow, create color gradient to show how far the end is
"""

import arcade
import time
from arcade.color import BLACK, CANDY_APPLE_RED, BRIGHT_GREEN, CANARY_YELLOW, WHITE

# Grid settings
SCREEN_WIDTH = 512
SCREEN_HEIGHT = SCREEN_WIDTH
CELL_AMOUNT = 32
CELL_AREA_SIZE = SCREEN_HEIGHT / CELL_AMOUNT
OFFSET = CELL_AREA_SIZE / 2
CELL_WIDTH_HEIGHT = CELL_AREA_SIZE - 1

# Global variables
cell_list = []
found_paths = []
while_counter = 0


class Cell(): # Ready to go. [position_x, position_y, width, height, color]
    """ This class manages each cell in the grid. """

    def __init__(self, position_x, position_y, width, height, color): # Ready to go.
        """ Constructor. """
        # Take the parameters of the init function above, and create instance variables out of them.
        self.position_x = position_x
        self.position_y = position_y
        self.width = width
        self.height = height
        self.color = color


    def draw(self): # Ready to go.
        """ Draw the cells with the instance variables we have. """
        arcade.draw_rectangle_filled(self.position_x, self.position_y, self.width, self.height, self.color)
    

    def cell_details(self): # Ready to go.
        """ Return all details about the individual cell. """
        return [self.position_x, self.position_y, self.width, self.height, self.color]
    
    
    def cell_x(self): # Ready to go.
        """ Return x and y coordinates of individual cell. """
        return self.position_x


    def cell_width(self):
        return self.width
    
    
    def cell_height(self):
        return self.height

    
    def cell_y(self):
        """ Return x and y coordinates of individual cell. """
        return self.position_y
    

    def cell_color(self): # Ready to go.
        """ Return color of individual cell. """
        return self.color


class Path():
    """ This class manages each path in the program. """

    def __init__(self, list_of_datapoints):
        """ Constructor. """
        # Take the parameters of the init function above, and create instance variables out of them.
        # Path datapoint: [x, y, length]
        self.list_of_datapoints = list_of_datapoints

    
    def full_path(self):
        """ Return the entire list of coordinates. """
        return self.list_of_datapoints
    

    def length(self):
        """ Return how long the path is. """
        distance = 0
        for datapoint in self.list_of_datapoints:
            distance += datapoint[2]
        return distance
    

    def last_coords(self):
        """ Return the x and y values of the last datapoint. """
        id = len(self.list_of_datapoints) - 1
        last_coordinates = self.list_of_datapoints[id]
        x = last_coordinates[0]
        y = last_coordinates[1]
        return [x, y]
    

    def add_point(self, x, y, distance):
        self.list_of_datapoints.append([x, y, distance])


class MyGame(arcade.Window):
    click_counter = 0
    list_of_paths = []

    def __init__(self, width, height, title):
        # Call the parent class's init function
        super().__init__(width, height, title)
        arcade.set_background_color(arcade.color.BLACK)

        # Create lists for the cells
        # self.cell_list = []
        # self.found_paths = []

        # Create a bunch of black squares spaced out evenly across the window
        for x in range(CELL_AMOUNT):
            temp_list = []
            for y in range(CELL_AMOUNT):
                temp_list.append(Cell((CELL_AREA_SIZE * x + OFFSET), (CELL_AREA_SIZE * y + OFFSET), CELL_WIDTH_HEIGHT, CELL_WIDTH_HEIGHT, BLACK))
            cell_list.append(temp_list)


    def on_draw(self): # Ready to go.
        """ Called whenever we need to draw the window. """
        arcade.start_render()
    
        # Use a "for" loop to pull each cell from the list, then call the draw method on that cell.
        for list in cell_list:
            for item in list:
                item.draw()


    def find_closest_cell(self, x, y): # Ready to go.
        x_distance = 5000
        y_distance = 5000
        x_coord = 0
        y_coord = 0
        for list in cell_list:
            for item in list:
                if abs(item.cell_x() - x) < x_distance:
                    x_distance = abs(item.cell_x() - x)
                    x_coord = item.cell_x()
                if abs(item.cell_y() - y) < y_distance:
                    y_distance = abs(item.cell_y() - y)
                    y_coord = item.cell_y()

        return [x_coord, y_coord]


    def on_mouse_press(self, x, y, button, modifiers): # Ready to go.
        self.click_counter += 1

        closest_cell_coords = self.find_closest_cell(x, y) # get coordinates of the closest cell
        cell_id = [int((closest_cell_coords[0] - OFFSET) / CELL_AREA_SIZE), int((closest_cell_coords[1] - OFFSET) / CELL_AREA_SIZE)] # get list id of cell

        closest_cell = cell_list[cell_id[0]][cell_id[1]] # create duplicate cell for editing
        cell = cell_list[cell_id[0]][cell_id[1]] # create duplicate cell for editing, use this if you wanna change all the below to make more sense
        cell_details = Cell.cell_details(closest_cell) # pull details of individual cell

        if self.click_counter == 1 and cell_details[4] == BLACK:
            new_cell = Cell(cell_details[0], cell_details[1], cell_details[2], cell_details[3], BRIGHT_GREEN) # change individual cell's to green
            cell_list[cell_id[0]][cell_id[1]] = new_cell
        elif self.click_counter == 2 and cell_details[4] == BLACK:
            new_cell = Cell(cell_details[0], cell_details[1], cell_details[2], cell_details[3], CANDY_APPLE_RED) # change individual cell's color to red
            cell_list[cell_id[0]][cell_id[1]] = new_cell
        elif cell_details[4] == WHITE:
            new_cell= Cell(cell_details[0], cell_details[1], cell_details[2], cell_details[3], BLACK) # change individual cell's color to black
            cell_list[cell_id[0]][cell_id[1]] = new_cell
        elif cell_details[4] == BLACK:
            new_cell = Cell(cell_details[0], cell_details[1], cell_details[2], cell_details[3], WHITE) # change individual cell's color to white
            cell_list[cell_id[0]][cell_id[1]] = new_cell


    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers): # Ready to go.
        closest_cell_coords = self.find_closest_cell(x, y) # get coordinates of the closest cell
        cell_id = [int((closest_cell_coords[0] - OFFSET) / CELL_AREA_SIZE), int((closest_cell_coords[1] - OFFSET) / CELL_AREA_SIZE)] # get list id of cell

        closest_cell = cell_list[cell_id[0]][cell_id[1]] # create duplicate cell for editing
        cell_details = Cell.cell_details(closest_cell) # pull details of individual cell

        if cell_details[4] == BLACK:
            new_cell = Cell(cell_details[0], cell_details[1], cell_details[2], cell_details[2], WHITE) # change individual cell's color to white
            cell_list[cell_id[0]][cell_id[1]] = new_cell


    def on_key_press(self, key, modifiers):
        if key == arcade.key.SPACE:
            self.pathfinder_loop()
    

    def find_start(self): # This will need a list of cells passed in if the global variable doesn't work as planned
        x = 0
        for list in cell_list:
            y = 0
            for cell in list:
                if cell.cell_color() == BRIGHT_GREEN:
                    return [x, y, 0]
                y += 1
            x += 1

    
    def check_straight_options(self, x, y, main_list, temp_list):
        # Create a list of coordinates above, below, and to the sides of the original coordinates.
        list_of_options = []
        list_of_options.append([x, y + 1, 1])
        list_of_options.append([x + 1, y, 1])
        list_of_options.append([x, y - 1, 1])
        list_of_options.append([x - 1, y, 1])

        # Create a list of options that aren't taken on the board and in other paths
        final_list_of_options = []
        for option in list_of_options:
            if ((0 <= option[0]) and (option[0] < CELL_AMOUNT)) and ((0 <= option[1]) and (option[1] < CELL_AMOUNT)): # Check if x and y are onscreen
                cell = cell_list[option[0]][option[1]]
                color_available = False
                available_in_main = False
                available_in_temp = False
                if cell.cell_color() == BLACK or cell.cell_color() == CANDY_APPLE_RED: # Check if the cell is available by color
                    color_available = True
                coords_counter_a = 0 # These make sure that every space is available in the paths, otherwise the boolean doesn't help at all
                coords_counter_b = 0
                for path in main_list:
                    for coords in path.full_path(): # This is resetting the available_in_main thing, probably happening below too
                        coords_counter_a += 1
                        if option[0] != coords[0] or option[1] != coords[1]: # Check if the cell is available in the main list
                            coords_counter_b += 1
                if coords_counter_a == coords_counter_b:
                    available_in_main = True
                coords_counter_a = 0 # These make sure that every space is available in the paths, otherwise the boolean doesn't help at all
                coords_counter_b = 0
                for path in temp_list:
                    for coords in path.full_path():
                        coords_counter_a += 1
                        if option[0] != coords[0] or option[1] != coords[1]: # Check if the cell is available in the temporary list
                            coords_counter_b += 1
                if coords_counter_a == coords_counter_b:
                    available_in_temp = True
                if available_in_main and available_in_temp and color_available: # If all criteria are met, add to list of options
                    final_list_of_options.append(option)
                elif available_in_main and temp_list == [] and color_available: # If all criteria are met and temp_list is empty, add to list of options
                    final_list_of_options.append(option)
        return final_list_of_options


    def check_diagonal_options(self, x, y, main_list, temp_list):
        # Create a list of coordinates above, below, and to the sides of the original coordinates.
        list_of_options = []
        list_of_options.append([x - 1, y + 1, 1.4142])
        list_of_options.append([x + 1, y + 1, 1.4142])
        list_of_options.append([x + 1, y - 1, 1.4142])
        list_of_options.append([x - 1, y - 1, 1.4142])

        # Create a list of options that aren't taken on the board and in other paths
        final_list_of_options = []
        for option in list_of_options:
            if ((0 <= option[0]) and (option[0] < CELL_AMOUNT)) and ((0 <= option[1]) and (option[1] < CELL_AMOUNT)): # Check if x and y are onscreen
                cell = cell_list[option[0]][option[1]]
                color_available = False
                available_in_main = False
                available_in_temp = False
                if cell.cell_color() == BLACK or cell.cell_color() == CANDY_APPLE_RED: # Check if the cell is available by color
                    color_available = True
                coords_counter_a = 0 # These make sure that every space is available in the paths, otherwise the boolean doesn't help at all
                coords_counter_b = 0
                for path in main_list:
                    for coords in path.full_path():
                        coords_counter_a += 1
                        if option[0] != coords[0] or option[1] != coords[1]: # Check if the cell is available in the main list
                            coords_counter_b += 1
                if coords_counter_a == coords_counter_b:
                    available_in_main = True
                coords_counter_a = 0 # These make sure that every space is available in the paths, otherwise the boolean doesn't help at all
                coords_counter_b = 0
                for path in temp_list:
                    for coords in path.full_path():
                        coords_counter_a += 1
                        if option[0] != coords[0] or option[1] != coords[1]: # Check if the cell is available in the temporary list
                            coords_counter_b += 1
                if coords_counter_a == coords_counter_b:
                    available_in_temp = True
                if available_in_main and available_in_temp and color_available: # If all criteria are met, add to list of options
                    final_list_of_options.append(option)
                elif available_in_main and temp_list == [] and color_available: # If all criteria are met and temp_list is empty, add to list of options
                    final_list_of_options.append(option)
        return final_list_of_options


    def check_if_end_found(self, list_of_paths):
        valid_paths = []
        for path in list_of_paths:
            path_end = path.last_coords() # Get index of the last coordinates in the path
            cell = cell_list[path_end[0]][path_end[1]] # Pull the cell at the index above
            if cell.cell_color() == CANDY_APPLE_RED:
                 valid_paths.append(path)
        return valid_paths


    def pathfinder_loop(self): # Don't forget to call this in on_key_press
        end_not_found = True
        global while_counter
        starting_datapoint = self.find_start() # [green_x, green_y, 0]
        starting_path = Path([starting_datapoint]) # [[green_x, green_y, 0]]
        if while_counter == 0:
            self.list_of_paths.append(starting_path) # [[[green_x, green_y, 0]]]
        
        while end_not_found:
            """ Track while loop iterations. """
            # global while_counter
            while_counter += 1
            path_counter = 0
            """ Track while loop iterations. """

            new_list_of_paths = []

            for path in self.list_of_paths:
                """ Track for loop iterations. """
                path_counter += 1
                print("Layer:", while_counter, " Path:", path_counter)
                """ Track for loop iterations. """

                path_end = path.last_coords()

                # Get options for up, down, and sideways
                options_horizontal = self.check_straight_options(path_end[0], path_end[1], self.list_of_paths, new_list_of_paths)
                # Check the check_straight_options function, I think it's finding stuff it shouldn't? Look at debugger
                if options_horizontal != []:
                    for option in options_horizontal: # Duplicate the path in the bigger for loop, add the new option on the end
                        temp_path_list = path.full_path().copy()
                        temp_path = Path(temp_path_list)
                        temp_path.add_point(option[0], option[1], option[2])
                        new_list_of_paths.append(temp_path)

                # Get options for diagonals
                options_diagonal = self.check_diagonal_options(path_end[0], path_end[1], self.list_of_paths, new_list_of_paths)
                if options_diagonal != []:
                    for option in options_diagonal: # Duplicate the path in the bigger for loop, add the new option on the end
                        temp_path_list = path.full_path().copy()
                        temp_path = Path(temp_path_list)
                        temp_path.add_point(option[0], option[1], option[2])
                        new_list_of_paths.append(temp_path)
            
            if new_list_of_paths != []:
                self.list_of_paths = new_list_of_paths.copy() # Change old list of paths to new, it's the same but expanded out a layer
                
                valid_solutions = self.check_if_end_found(self.list_of_paths) # Check to see if the end was found, if so call the loop to end
                if valid_solutions != []:
                    end_not_found = False
                    print("End found.")
                    for path in valid_solutions:
                        found_paths.append(path)
                    break
            else: # If there weren't any new paths this iteration there won't be next iteration. End the while loop
                print("No new paths. While loop ended.")
                break
            
            if while_counter > 128:
                print("Either you made too long of a maze, you didn't choose an end, or you blocked the end in.")
                print("Please try again, and be a little nicer to my program.")
                print("Pathfinding loop ended.")
                break
            
        # self.display_all_paths(self.list_of_paths)
        shortest_path_length = 99999
        shortest_path = None
        for path in valid_solutions:
            path_length = path.length()
            if path_length < shortest_path_length:
                shortest_path_length = path_length
                shortest_path_list = path.full_path().copy()
                shortest_path = Path(shortest_path_list)
        if shortest_path != None:
            self.display_path(shortest_path)

    
    def display_path(self, path):
        for coords in path.full_path():
            x = coords[0]
            y = coords[1]
            cell = cell_list[x][y]
            if cell.cell_color() == BLACK:
                cell_list[x][y] = Cell(cell.cell_x(), cell.cell_y(), CELL_WIDTH_HEIGHT, CELL_WIDTH_HEIGHT, CANARY_YELLOW)
    

    def display_all_paths(self, list_of_paths):
        for path in list_of_paths:
            self.display_path(path)


def main(): # Ready to go.
    print("""
    To start the game, click at least twice on the screen.
    The first click will be green, this is where the path will start.
    The second click will be red, that is where the path wants to end.
    Every time you click after that will put up an obstacle to the path.
    Make sure that there is a possible path, and that it's not too long.
    Python is slow, if your path is too long the program will end it before the path is found.
    When you are ready for the pathfinding to start, simply press the spacebar.""")
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, "Pathfinder")
    arcade.run()
if __name__ == "__main__": # Ready to go.
    main()