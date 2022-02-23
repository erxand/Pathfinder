"""
File: pathfinder.py
Author: Xander Hunt
Purpose: Using arcade display a grid, user clicks start and end points, and draws barriers if desired. Program finds
fastest way from start to finish.
CSE 111 final project
"""
import arcade
import time
from arcade.color import BLACK, CANDY_APPLE_RED, BRIGHT_GREEN, CANARY_YELLOW, WHITE

# Grid options
SCREEN_WIDTH = 512
SCREEN_HEIGHT = SCREEN_WIDTH
CELL_AMOUNT = 32
CELL_AREA_SIZE = SCREEN_HEIGHT / CELL_AMOUNT
OFFSET = CELL_AREA_SIZE / 2
CELL_WIDTH_HEIGHT = CELL_AREA_SIZE - 1


class Cell():
    """ This class manages each cell in the grid. """

    def __init__(self, position_x, position_y, width, height, color):
        """ Constructor. """
        # Take the parameters of the init function above, and create instance variables out of them.
        self.position_x = position_x
        self.position_y = position_y
        self.width = width
        self.height = height
        self.color = color


    def draw(self):
        """ Draw the cells with the instance variables we have. """
        arcade.draw_rectangle_filled(self.position_x, self.position_y, self.width, self.height, self.color)
    

    def cell_details(self):
        """ Return all details about the individual cell. """
        return [self.position_x, self.position_y, self.width, self.height, self.color]


class MyGame(arcade.Window):

    def __init__(self, width, height, title):

        # Call the parent class's init function
        super().__init__(width, height, title)
        arcade.set_background_color(arcade.color.BLACK)

        # Create a list for the cells
        self.cell_list = []
        self.cell_list_coords = []
        self.found_paths = []

        # Create a bunch of black squares spaced out evenly across the window
        for x in range(CELL_AMOUNT):
            temp_list = []
            temp_list_coords = []
            for y in range(CELL_AMOUNT):
                temp_list.append(Cell((CELL_AREA_SIZE * x + OFFSET), (CELL_AREA_SIZE * y + OFFSET), CELL_WIDTH_HEIGHT, CELL_WIDTH_HEIGHT, BLACK))
                coordinates = [(x * CELL_AREA_SIZE + OFFSET), (y * CELL_AREA_SIZE + OFFSET)]
                temp_list_coords.append(coordinates)
            self.cell_list.append(temp_list)
            self.cell_list_coords.append(temp_list_coords)
        
        counter = 0
        for x_list in self.cell_list_coords:
            counter += 1


    def on_draw(self):
        """ Called whenever we need to draw the window. """
        arcade.start_render()
    
        # Use a "for" loop to pull each cell from the list, then call the draw method on that cell.

        for list in self.cell_list:
            for item in list:
                item.draw()
    

    def find_closest_cell(self, x, y):
        x_distance = 5000
        y_distance = 5000
        x_coord = 0
        y_coord = 0
        # for x_list in self.cell_list_coords:
        #     for y_list in x_list:
        #         if abs(y_list[0] - x) < x_distance:
        #             x_distance = abs(y_list[0] - x)
        #             x_coord = y_list[0]
        #         if abs(y_list[1] - y) < y_distance:
        #             y_distance = abs(y_list[1] - y)
        #             y_coord = y_list[1]
        for list in self.cell_list:
            for item in list:
                cell_deets = item.cell_details()
                cell_x_position = cell_deets[0]
                cell_y_position = cell_deets[1]
                if abs(cell_x_position - x) < x_distance:
                    x_distance = abs(cell_x_position - x)
                    x_coord = cell_x_position
                if abs(cell_y_position - y) < y_distance:
                    y_distance = abs(cell_y_position - y)
                    y_coord = cell_y_position

        return [x_coord, y_coord]
    

    click_counter = 0
    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        self.click_counter += 1

        closest_cell_coords = self.find_closest_cell(x, y) # get coordinates of the closest cell
        cell_id = [int((closest_cell_coords[0] - OFFSET) / CELL_AREA_SIZE), int((closest_cell_coords[1] - OFFSET) / CELL_AREA_SIZE)] # get list id of cell

        closest_cell = self.cell_list[cell_id[0]][cell_id[1]] # create duplicate cell for editing
        cell_details = Cell.cell_details(closest_cell) # pull details of individual cell

        if self.click_counter == 1:
            new_cell = Cell(cell_details[0], cell_details[1], cell_details[2], cell_details[3], BRIGHT_GREEN) # change individual cell's to green
        elif self.click_counter == 2:
            new_cell = Cell(cell_details[0], cell_details[1], cell_details[2], cell_details[3], CANDY_APPLE_RED) # change individual cell's color to red
        elif cell_details[4] == WHITE:
            new_cell= Cell(cell_details[0], cell_details[1], cell_details[2], cell_details[3], BLACK) # change individual cell's color to black
        else:
            new_cell = Cell(cell_details[0], cell_details[1], cell_details[2], cell_details[3], WHITE) # change individual cell's color to white
        self.cell_list[cell_id[0]][cell_id[1]] = new_cell

        pass


    def on_mouse_drag(self, x: float, y: float, dx: float, dy: float, buttons: int, modifiers: int):
        # Make it draw a bunch of yellow cells
        closest_cell_coords = self.find_closest_cell(x, y) # get coordinates of the closest cell
        cell_id = [int((closest_cell_coords[0] - OFFSET) / CELL_AREA_SIZE), int((closest_cell_coords[1] - OFFSET) / CELL_AREA_SIZE)] # get list id of cell

        closest_cell = self.cell_list[cell_id[0]][cell_id[1]] # create duplicate cell for editing
        cell_details = Cell.cell_details(closest_cell) # pull details of individual cell

        if cell_details[4] == BLACK:
            new_cell = Cell(cell_details[0], cell_details[1], cell_details[2], cell_details[2], WHITE) # change individual cell's color to white
            self.cell_list[cell_id[0]][cell_id[1]] = new_cell
        # elif cell_details[4] == WHITE:
        #     new_cell = Cell(cell_details[0], cell_details[1], cell_details[2], cell_details[2], BLACK) # change individual cell's color to black
        # self.cell_list[cell_id[0]][cell_id[1]] = new_cell
        
        pass


    def find_start(self): # Return the coordinates in the cell_list of the green cell
        x = 0
        for list in self.cell_list:
            y = 0
            for cell in list:
                cell_deets = cell.cell_details()
                if cell_deets[4] == BRIGHT_GREEN:
                    print([x, y])
                    return [x, y]
                y += 1
            x += 1
        pass


    def on_key_press(self, key, modifiers):
        if key == arcade.key.SPACE:
            end_not_found = True
            list_of_paths = []
            starting_coords = self.find_start() # [green_x, green_y]
            starting_coords.append(0) # [green_x, green_y, 0]
            starting_path = [starting_coords] # [[green_x, green_y, 0]] This might not be a list of a list?
            list_of_paths.append(starting_path) # [[[green_x, green_y, 0]]]

            lengths_of_path_lists = [] # Created to check the progression of the length of the list of paths
            list_of_list_of_paths = [] # Use this to print each iteration of paths individually
            while_counter = 0 # Help me see if it's looping and not displaying anything or not

            while end_not_found:
                while_counter += 1 # Help me see if it's looping and not displaying anything or not
                path_counter = 0
                print("While loop started, #", while_counter) # Help me see if it's looping and not displaying anything or not

                new_list_of_paths = []

                """ Ideas that could fix the program:
                - Print all of the paths in the lengths_of_path_lists individually, get something that lets
                    you see the paths being drawn not just when they're done being drawn
                """

                for path in list_of_paths:
                    path_counter += 1
                    print(f"Loop #{while_counter}, Path #{path_counter}")
                    last_index = len(path) - 1 # Get the index of the last coordinates of the path
                    path_end = [path[last_index][0], path[last_index][1]] # Get the coordinates of the end of the path

                    # Get options for up, down, and sideways
                    options_horizontal = self.check_straight_options(path_end[0], path_end[1], list_of_paths, new_list_of_paths)
                    if options_horizontal != []:
                        for option in options_horizontal: # Duplicate the path in the bigger for loop, add the new option on the end
                            temp_path = path
                            temp_path.append(option)
                            new_list_of_paths.append(temp_path)

                    # Get options for diagonals
                    options_diagonal = self.check_diagonal_options(path_end[0], path_end[1], list_of_paths, new_list_of_paths)
                    if options_diagonal != []:
                        for option in options_diagonal: # Duplicate the path in the bigger for loop, add the new option on the end
                            temp_path = path
                            temp_path.append(option)
                            new_list_of_paths.append(temp_path)
                    
                    # """ Display all created paths """
                    # for path in list_of_paths:
                    #     for coords in path:
                    #         x = coords[0]
                    #         y = coords[1]
                    #         cell = self.cell_list[x][y]
                    #         cell_deets = cell.cell_details()
                    #         if cell_deets[4] == BLACK:
                    #             self.cell_list[x][y] = Cell(cell_deets[0], cell_deets[1], cell_deets[2], cell_deets[3], CANARY_YELLOW)
                    # """ Display all created paths """
                
                """ Print paths, return number of paths """
                # for path in list_of_paths:
                #     print(path)
                lengths_of_path_lists.append(len(list_of_paths)) # Add to the progression of the length of the list of paths
                """ Print paths, return number of paths """

                # Set the main list of paths to the updated list
                if new_list_of_paths != []:
                    list_of_paths = new_list_of_paths
                    list_of_list_of_paths.append(list_of_paths)

                # Check for paths that found the end
                valid_solutions = self.check_if_end_found(list_of_paths)
                if valid_solutions != []:
                    end_not_found = False
                    for path in valid_solutions:
                        self.found_paths.append(path)

                # Stop the while loop if it runs too many times
                if len(list_of_paths) > 999:
                    break

                # Stop the while loop if it is continuing all the paths outside of the window
                num_wrong_paths = 0
                for path in list_of_paths:
                    last_index = len(path) - 1 # Get the index of the last coordinates of the path
                    path_end = [path[last_index][0], path[last_index][1]] # Get the coordinates of the end of the path
                    x = path_end[0]
                    y = path_end[1]
                    if (x < 0 or x > CELL_AMOUNT) or (y < 0 or y > CELL_AMOUNT):
                        num_wrong_paths += 1
                if num_wrong_paths >= len(list_of_paths):
                    print("While loop stopped, all paths being drawn outside of window.")
                    break

                # """ Display all created paths """
                # for path in list_of_paths:
                #     for coords in path:
                #         x = coords[0]
                #         y = coords[1]
                #         cell = self.cell_list[x][y]
                #         cell_deets = cell.cell_details()
                #         if cell_deets[4] == BLACK:
                #             self.cell_list[x][y] = Cell(cell_deets[0], cell_deets[1], cell_deets[2], cell_deets[3], CANARY_YELLOW)
                # """ Display all created paths """

            """ Iterate through all paths and growth of said paths """
            for list in list_of_list_of_paths:
                for path in list:
                    for coords in path:
                        x = coords[0]
                        y = coords[1]
                        cell = cell = self.cell_list[x][y]
                        cell_deets = cell.cell_details()
                        if cell_deets[4] == BLACK:
                            self.cell_list[x][y] = Cell(cell_deets[0], cell_deets[1], cell_deets[2], cell_deets[3], CANARY_YELLOW)
                time.sleep(0.1)
            """ Iterate through all paths and growth of said paths """

            # If a valid path is found, print said path to the screen
            if self.found_paths != []:
                first_path = self.found_paths[0]
                for coords in first_path:
                    x = coords[0]
                    y = coords[1]
                    cell = self.cell_list[x][y]
                    cell_deets = cell.cell_details()
                    self.cell_list[x][y] = Cell(cell_deets[0], cell_deets[1], cell_deets[2], cell_deets[3], CANARY_YELLOW)
        
            """ Show the progression of the length of the list of paths """
            print("For each iteration of the while loop, here are the lengths of the list_of_paths")
            print(lengths_of_path_lists)
            """ Show the progression of the length of the list of paths """


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
            if ((0 <= option[0]) and (option[0] < CELL_AMOUNT)) and ((0 <= option[1]) and (option[1] < CELL_AMOUNT)):
                cell = self.cell_list[option[0]][option[1]]
                cell_deets = cell.cell_details()
                color_available = False
                if cell_deets[4] == BLACK:
                    color_available = True
                option_available_in_main = False
                option_available_in_temp = False
                for path in main_list:
                    for coords in path:
                        if option[0] != coords[0] or option[1] != coords[1]:
                            option_available_in_main = True
                for path in temp_list:
                    for coords in path:
                        if option[0] != coords[0] or option[1] != coords[1]:
                            option_available_in_temp = True
                if option_available_in_main and option_available_in_temp and color_available:
                    final_list_of_options.append(option)
                elif option_available_in_main and temp_list == [] and color_available:
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
            if 0 <= option[0] < CELL_AMOUNT and 0 <= option[1] < CELL_AMOUNT:
                cell = self.cell_list[option[0]][option[1]]
                cell_deets = cell.cell_details()
                color_available = False
                if cell_deets[4] == BLACK:
                    color_available = True
                option_available_in_main = False
                option_available_in_temp = False
                for path in main_list:
                    for coords in path:
                        if option[0] != coords[0] or option[1] != coords[1]:
                            option_available_in_main = True
                for path in temp_list:
                    for coords in path:
                        if option[0] != coords[0] or option[1] != coords[1]:
                            option_available_in_temp = True
                if option_available_in_main and option_available_in_temp and color_available:
                    final_list_of_options.append(option)
                elif option_available_in_main and temp_list == [] and color_available:
                    final_list_of_options.append(option)

        return final_list_of_options


    def check_if_end_found(self, list_of_paths):
        index_of_path = 0
        valid_paths = []
        for path in list_of_paths:
            last_index = len(path) - 1 # Get the length of the path
            path_end = [path[last_index][0], path[last_index][1]] # Get index of the last coordinates in the path
            cell = self.cell_list[path_end[0]][path_end[1]] # Pull the cell at the index above
            cell_deets = cell.cell_details() # Pull details of said cell
            if cell_deets[4] == CANDY_APPLE_RED:
                 valid_paths.append(path)
            index_of_path += 1
        return valid_paths


def main():
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, "Pathfinder")
    arcade.run()


if __name__ == "__main__":
    main()