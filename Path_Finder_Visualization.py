# used for creating GUI for games, animations, sound effects etc
import pygame
# used for generating random stuff like seq of numbers etc where randomness of input output are required
import random
import pygame.font
import pygame.mixer


# setting the sound variables
pygame.mixer.init()
sound1=pygame.mixer.Sound("sound1.wav")
sound2=pygame.mixer.Sound("sound2.wav")
search=pygame.mixer.Sound("search_sound.wav")
bonus=pygame.mixer.Sound("bonus_alert.wav")
default_volume=0.8
sound1.set_volume(default_volume)


class Gui():

    
    # gui constants
    FPS = 60
    # defines the size of gui window
    WIDTH = 800
    
    # constructor which is called on itself when class object is created, it will initialize class to self and coords is passed as a paramenter
    # which represents instances of coOrdinates class
    def __init__(self, coords):

        # gui variables
        self.grid_size = 20
        self.box_width = self.WIDTH/self.grid_size
        # used for giving class access to co-ordinates for making changs to GUI by making changes to data stored in coOrdinates
        self.coords = coords
        self.placing_walls = False
        self.removing_walls = False
        self.animation_speed = 10
        
  # initialize the maize attribute of coords to a 2d list containing 0's
        self.coords.maze = [
            [0 for x in range(self.grid_size)] for y in range(self.grid_size)]

        # start pygame application
        pygame.init()
        # setting window
        self.win = pygame.display.set_mode((self.WIDTH, self.WIDTH))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Pathfinding Algorithms")

    
    # main function for gui
    def main(self, running=False):
        
        # controls the frame rate of gui limiting it to FPS to create smooth animation and perfomance
        self.clock.tick(self.FPS)

        # take the co-ordinates of cursor by using pygame.mouse.get_pos() and assigning it self.mouse_x and self.mouse_y
        self.mouse_x, self.mouse_y = pygame.mouse.get_pos()
                
        # if the mouse button was pressed down continue placing walls
        # before placing/removing the walls the gui should not be in running state
        if not running:
            # user is placing walls call method place_wall()
            if self.placing_walls == True:
                self.place_wall()
            # user is removing walls call method remove()
            elif self.removing_walls == True:
                self.remove()

        # get mouse and key presses
        # handles mouse and key board events
        self.event_handle(running)

        # redraw and update the display
        self.redraw()
        pygame.display.update()
        

    # handles key and mouse presses
    # takes a boolean parameter running indicating whether the GUI is 
    # currently in running state

    def event_handle(self, running):
        # list containing the list of run_key used for running the searching algo
        # and checkpoint_keys to create check points
        run_keys = {"a", "b", "d", "k"}
        checkpoint_keys = {"1", "2", "3", "4", "5", "6", "7", "8", "9"}

        # gets key presses,iterating  over events in event queue( used for executing events
        # in a FIFO fashion)
        for event in pygame.event.get():
            
            #  If the user quits the program by closing the window, 
            # this block of code ensures that the pygame module is properly
            # uninitialized before exiting the program.
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            # checks key presses 
            elif event.type == pygame.KEYDOWN:
                # retrives the character representation of the key
                key = chr(event.key)


            #  Checks if the GUI is not currently running. If not, it proceeds to 
            # handle key presses related to various actions.
                if running == False:

                    # run algorithm 
                    # If the pressed key corresponds to one of the keys defined in run_keys,
                    # it calls the run_algorithm() method with the pressed key as an argument.
                    if key in run_keys: # a , k , b, d
                        self.run_algorithm(key)              
                    
                    # If the pressed key is "x", it calls the remove_all() method
                    # of the coords object to clear the entire board.
                    elif key == "x":
                        self.coords.remove_all()
                        
                    # remove everything except the things placed by the user
                    # If the pressed key is "z", it calls the remove_last() method of the
                    # coords object to remove the last placed item.
                    elif key == "z":
                        self.coords.remove_last()
                        
                    # place checkpoints with number keys
                    #If the pressed key is in checkpoint_keys, it calls the place_check_point()
                    # method with the pressed key as an argument to place a checkpoint.
                    elif key in checkpoint_keys: # 1-9
                        self.place_check_point(key)
                        
                    # If the pressed key is a front slash, it calls the generate_random_maze() 
              # method of the coords object to generate a random maze.
                    elif key == "/":
                          self.coords.generate_random_maze(gui)


                # increase speed of the pathfinding
                #If the pressed key is "p" or "P", and the animation speed is greater than 0, it increases the animation speed. 
                # The animation speed is capped at a minimum of 1 and is halved if it is greater than 2.
                elif (key == "p" or key == "P") and self.animation_speed > 0:
                    if self.animation_speed <= 2:
                        self.animation_speed = 1
                    else:
                        self.animation_speed = int(self.animation_speed * 0.5) + 1

                # decrease speed of pathfinding
                # If the pressed key is "m" or "M", it decreases the 
                # animation speed by doubling it and adding 1.B
                elif key == "m" or key=="M":
                    self.animation_speed = int(self.animation_speed * 2) + 1
              
              # If none of the above conditions are met,
              # it prints the pressed key (useful for debugging).
                else:
                    print(key)


            # mouse button down i.e if mouse button is pressed
            elif event.type == pygame.MOUSEBUTTONDOWN:
              # check if the gui is in not running state first
                if running == False:
                  
                  # left click or button 1 place wall
                    # place walls
                    if event.button == 1: # left down
                        self.placing_walls = True

                  # right click or button 3 remove wall
                    # remove walls
                    elif event.button == 3: # right down
                        self.removing_walls = True

                # zoom in
                if event.button == 4: # scroll up
                    self.grid_size -= 1
                    self.box_width = self.WIDTH/self.grid_size
                    # effect: box width inc as grid size dec

                # zoom out
                elif event.button == 5: # scroll down
                    self.grid_size += 1
                    self.box_width = self.WIDTH/self.grid_size
                    # effect: box width dec as grid size inc

            # mouse button up, when the click is released 
            elif event.type == pygame.MOUSEBUTTONUP:
            # if the mouse button is released stop whatever action that was being 
            # performed
                # stop placing walls
              if event.button == 1: # left up
                self.placing_walls = False

                # stop removing walls
              elif event.button == 3: # right up
                self.removing_walls = False

      
    # redraws the gui
    def redraw(self):
      # filling gui with white color
        self.win.fill((255,182,193))
      # responsible for drawing various elements such as nodes, walls and
      # check points
        self.draw_points()
      # draws grid again
        self.draw_grid()

    # draw the grid lines
    #  the draw_grid method is responsible for drawing grid lines on the 
    #  window to visually divide it into smaller sections, providing a 
    #  structured layout for the elements displayed on the GUI.Where (0,0,0)
    # refers to the black colored grid
    def draw_grid(self):
        for i in range(self.grid_size-1):
            pygame.draw.rect(self.win, (0, 0, 0),
                             (((i+1)*self.box_width)-2, 0, 4, self.WIDTH))
            pygame.draw.rect(self.win, (0, 0, 0),
                             (0,((i+1)*self.box_width)-2, self.WIDTH, 4))

    # draws all the squares for the walls, checkpoints ect
    def draw_points(self):

        # nodes in open list are candidates for further expansion marked oranage
        for node in self.coords.open_list:
            self.draw_box(node.position, (255, 255, 0))

        # already explored and not considered for further expansion blue color
        for node in self.coords.closed_list:
            self.draw_box(node.position, (255, 0, 0))

        # used for tracing the final path pink in color
        for wall in self.coords.final_path:
            self.draw_box(wall, (0, 255, 0))
        # draw a box black in color in the wall position
        for wall in self.coords.walls:
            self.draw_box(wall, (110, 38, 14))
            
        #place check points at positions by drawing a box red in color plus
        #inserting the text inside it, i+1 converted to string given white color
        # centered and box width provided
        for i,point in enumerate(self.coords.check_points):
            if point != "None":
                self.draw_box(point, (0, 0, 255))
                self.display_text(str(i+1), (255, 255, 255),
                                  self.box_center(point), int(self.box_width))
        
        if self.coords.start != None:
            self.draw_box(self.coords.start, (255, 0, 0))
            self.display_text("S", (255, 255, 255),
                              self.box_center(self.coords.start), int(self.box_width))

            
        if self.coords.end != None:
            self.draw_box(self.coords.end, (255, 0, 0))
            self.display_text("E", (255, 255, 255),
                              self.box_center(self.coords.end), int(self.box_width))

    
    # gets the center point of a node
    def box_center(self, box):
        boxX, boxY = box
        center = ((boxX*self.box_width+(self.box_width/2)),
                  (boxY*self.box_width+(self.box_width/2)))
        return center


    # used to draw the boxed given colours and position
    def draw_box(self, box, colour):
        boxX, boxY = box
        pygame.draw.rect(self.win, colour,
                        (boxX*self.box_width, boxY*self.box_width,
                         self.box_width, self.box_width))


    # gets the box coordinates given a mouse position
    # This get_box_coords method is responsible 
    # for converting the mouse position on the GUI window to the
    # corresponding grid coordinates,some approximation is involved.
    def get_box_coords(self):
        boxX = int((self.mouse_x + 2) / self.box_width)
        boxY = int((self.mouse_y + 2) / self.box_width)
        return (boxX, boxY)


    # placing checkpoints
    # index represents the check point to be place
    def place_check_point(self, index):
      # takes the co-ordinates of mouse and converts to grid co-ordinates
        coords = self.get_box_coords()
      # ensures that the checkpoint is not placed at start and end and on walls and on the place
      # of other check points
        if (coords != self.coords.start and coords != self.coords.end
                and coords not in self.coords.walls and coords
                not in self.coords.check_points):
            # This snippet ensures that the list of checkpoints has enough space to
            # accommodate a new checkpoint at a specified index. If the list is not
            # long enough, it adds placeholder values ("None") until 
            # it reaches the required length. Then, it places the new checkpoint at
            # the specified index.

            sound2.play()
            while len(self.coords.check_points) <= int(index)-1:
                self.coords.check_points.append("None")
                self.coords.check_points[int(index)-1] = coords

    
    # placing walls 
    # This function allows the user to place walls on the grid. 
    # It checks if the current coordinates are not already 
    # occupied by the start point, end point, other walls, or checkpoints. 
    # If the conditions are met, it adds the current coordinates to 
    # the list of walls. This prevents the user from placing walls on invalid positions.
    def place_wall(self):
        coords = self.get_box_coords()
        if (coords != self.coords.start and coords != self.coords.end
                and coords not in self.coords.walls and coords
                not in self.coords.check_points):
            self.coords.walls.append(coords)
            sound2.play()


    # removing nodes such as walls checkpoints ect
    def remove(self):
        coords = self.get_box_coords()
        if coords in self.coords.walls:
            self.coords.walls.remove(coords)
        elif coords in self.coords.check_points:
            self.coords.check_points.remove(coords)
        elif coords == self.coords.start:
            self.coords.start = None
        elif coords == self.coords.end:
            self.coords.end = None


    # function that prepares for a pathfind and runs pathfind function
    def run_algorithm(self, key):
        self.placing_walls == False
        self.removing_walls == False
        self.coords.remove_last()

        # if we have 2 or more checkpoints
        if len(self.coords.check_points) > 1:

            # create the maze array and remove missed checkpoint numbers
            self.coords.create_maze(gui)
            # removes any none values in the check point  list
            check_points = self.coords.check_points[:]
            # filtering only valid(not-none) checkpoints
            check_points = [point for point in check_points if point != "None"]

            # iterate through every checkpoint and pathfind to it
            for i,point in enumerate(check_points):
                if i != len(check_points)-1:
                    
                    start = point
                    end = check_points[i+1]

                    new_path = pathfind(self.coords.maze, start, end,self, self.coords, key)
                    # The condition if new_path == None checks if a path was not found
                    # or if it's None, indicating that no valid path exists 
                    # between the given start and end points. 
                    # In such cases, it initializes new_path as an empty list [].
                    if new_path == None:
                        new_path = []
                    # if valid path is found extend the final path by adding new_path
                    self.coords.final_path.extend(new_path)


    # displays text given text, colour and position/size responsible for styling of text
    def display_text(self, txt, colour, center, size):
        font = pygame.font.Font(None, size)
        text_surf = font.render(txt, True, colour)
        text_rect = text_surf.get_rect()
        text_rect.center = (center)
        self.win.blit(text_surf, text_rect)

class CoOrdinates():
    '''
    class containing all coordinates and functions for calculations todo with them
    '''

    # removing all elements associated with the instance of the class
    def __init__(self):
        self.remove_all()

    # remove_all(self): This method removes all elements associated with the instance.
    # It sets various attributes such as start, end, walls, maze, open_list, closed_list,
    # final_path, and check_points to None or empty lists, effectively clearing them.
    def remove_all(self):
        self.start = None
        self.end = None
        self.walls = []
        self.maze = []
        self.open_list = []
        self.closed_list = []
        self.final_path = []
        self.check_points = []

 # remove_last(self): This method specifically removes elements related
 # to the pathfinding process. It clears the attributes maze, open_list, 
 # closed_list, and final_path, which are likely used during pathfinding
 # and need to be reset before initiating a new pathfinding operation.
    def remove_last(self):
        self.maze = []
        self.open_list = []
        self.closed_list = []
        self.final_path = []

    # this starts from (0,0) and checks for the largest co-ordinate having checkpoint or
    # walls furthest from the starting point, this ensures that we have a largest distance value
    # returned which is tuple, giving info about the size of grid req to accomdate all 
    # check points and walls.Returning distance 1 greater than co-ordinate value accounting
    # for zero based indexing
    # gets the furthest distance of a node from the (0, 0)
    def largest_distance(self):
        largest = 0
        for wall in self.walls:
            if wall[0] > largest: largest = wall[0]
            if wall[1] > largest: largest = wall[1]
        for point in self.check_points:
            if point[0] > largest: largest = point[0]
            if point[1] > largest: largest = point[1]
        return largest + 1


    # creates a 2d array of the maze and its walls
    def create_maze(self, giu):
        
        largest_distance = self.largest_distance()
        
        # makes sure the size of the maze if either the size of the gui
        # or the size of the maze made using the walls and checkpoints
        if gui.grid_size > largest_distance:
            largest = gui.grid_size
        else:
            largest = largest_distance
            
        self.maze = [[0 for x in range(largest)] for y in range(largest)]
        for wall in self.walls:
            try:
                wall_x, wall_y = wall
                self.maze[wall_x][wall_y] = 1
            except:
                pass

# this generates random walls 

    def generate_random_maze(self, gui):
      print("Printing the positions where walls are added: ")
      self.walls = []
      for i in range(gui.grid_size*gui.grid_size):
        # Walls will be placed in only 30% of the cases
          if random.random() > 0.7:
            wall = (random.randint(0, gui.grid_size-1),
                    random.randint(0, gui.grid_size-1))
            if wall not in self.walls:
                self.walls.append(wall)
                print(f"Added wall at {wall}")
    
      
      print("Total walls generated:", len(self.walls))


# function for pathfinding using dfs, bfs, dijkstra and astar
# Returns a list of tuples as a path from the given start to the given end in the given maze
def pathfind(maze, start, end, gui, coords, key):
    
   # initializing the start and end nodes using start and end 
   # provided by user on the maze

    start_node = Node(None, start)
   # In the line start_node.g = start_node.h = start_node.f = 0,
   # the properties g, h, and f of the start_node are all initialized
   # to 0, indicating the initial cost, heuristic value, and combined 
   # cost from the start node.
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0

    # Initialize both open and closed list
    # initializes two lists: open_list and closed_list. The open_list
    # contains nodes that are candidates for further exploration, and
    # the closed_list contains nodes that have already been evaluated.
    open_list = []
    closed_list = []

    # Add the start node
    open_list.append(start_node)

    count = 0
   
   # while we have further nodes to explore loop
    while len(open_list) > 0:

        # skip pathfinding to create a wait effect. Ajustable speed
        if count >= gui.animation_speed:
            sound1.play()
            count = 0

            # Get the current node

            if key == "d": # dfs, get the latest node
                current_node = open_list[-1]
                current_index = len(open_list)-1
                
            elif key == "b": # bfs, get the newest node
                current_node = open_list[0]
                current_index = 0               
                
            elif key == "a": # a*, get the node with the lowest f value
                current_node = open_list[0]
                current_index = 0
                for index, item in enumerate(open_list):
                    if item.f < current_node.f:
                        current_node = item
                        current_index = index
                        
            elif key == "k": # dijkstra, get the node with the lowest g value
                current_node = open_list[0]
                current_index = 0
                for index, item in enumerate(open_list):
                    if item.g < current_node.g:
                        current_node = item
                        current_index = index

            # Pop current off open list, add to closed list
            open_list.pop(current_index)
            closed_list.append(current_node)

            # Found the goal
            if current_node == end_node:
               
                # Display time taken on the GUI
                
                sound1.stop()
                bonus.play()
               
                path = []
                current = current_node
                while current is not None:
                    path.append(current.position)
                    current = current.parent
                coords.open_list = open_list
                coords.closed_list = closed_list
                return path # Return path

            # Generate children
            # left, down, right, up. Which makes dfs go in up, right, down, left order
            for new_pos in [(-1, 0), (0, 1), (1, 0), (0, -1),(1,1),(1,-1),(-1,1),(-1,-1)]: # Adjacent squares

                # Get node position
                node_pos = (current_node.position[0] + new_pos[0],
                            current_node.position[1] + new_pos[1])

                # Make sure within range
                if (node_pos[0] > (len(maze) - 1) or node_pos[0] < 0
                        or node_pos[1] > (len(maze[len(maze)-1]) -1)
                        or node_pos[1] < 0):
                    continue

                # Make sure walkable terrain
                if maze[node_pos[0]][node_pos[1]] != 0:
                    continue

                if Node(current_node, node_pos) in closed_list:
                    continue

                # Create new node
                child = Node(current_node, node_pos)

                # Child is on the closed list
                passList = [False for closed_child in closed_list if child == closed_child]
                if False in passList:
                    continue

                # for dfs and bfs we dont add anything to the node values
                
                if key == "k": # dijkstra, add one to g value
                    child.g = current_node.g + 1
                    
                elif key == "a": # a*, calculate f value
                    child.g = current_node.g + 1
                    # distance to end point
                    # the reason the h distance is powered by 0.6 is because
                    #it makes it prioritse diagonal paths over straight ones
                    # even though they are technically the same g distance, this makes a* look better
                    child.h = (((abs(child.position[0] - end_node.position[0]) ** 2) +
                                (abs(child.position[1] - end_node.position[1]) ** 2)) ** 0.6)
                    child.f = child.g + child.h

                # Child is already in the open list
                
                for open_node in open_list:
                    # check if the new path to children is worst or equal 
                    # than one already in the open_list (by measuring g)
                    if child == open_node and child.g >= open_node.g:
                        break
                    
                else:
                      # Add the child to the open list
                      open_list.append(child)

     # if skipped just update the gui
        else:

              coords.open_list = open_list
              coords.closed_list = closed_list
              gui.main(True)

        count += 1

class Node():
    '''
    node class for containing position, parent and costs
    '''
    
    def __init__(self, parent, position):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position

# main loop
if __name__ == "__main__":
            gui = Gui(CoOrdinates())
            while True:
                gui.main()