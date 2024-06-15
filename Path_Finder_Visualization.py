# used for creating GUI for games,animation and sound effects etc
import pygame
# used for generating random stuff like seq of numbers etc where randomness in input is required
import random
# used for rendering fonts in pygame
import pygame.font
# mixer is used for loading and playing sounds
import pygame.mixer

# setting the sound variables

# pygame.mixer.init(): Initializes the Pygame sound mixer. This is necessary 
# to use sound functionalities in Pygame.
pygame.mixer.init()

sound1=pygame.mixer.Sound("sound1.wav")
sound2=pygame.mixer.Sound("sound2.wav")
search=pygame.mixer.Sound("search_sound.wav")
bonus=pygame.mixer.Sound("bonus_alert.wav")
# set the volume to 60%
default_volume=0.6
# setting the max volume of sound1 to default volume of 60 % of sound
# that pygame can produce
sound1.set_volume(default_volume)

class Gui():

    # defines the no. of frames per seconds which enables smooth animations
    FPS=60
    # for the width of GUI window( and height as the window is square) which is 800px in this case
    WIDTH=800

     # constructor which is called on itself when class object is created, it will initialize class to self and coords is passed as a paramenter
     # which represents instances of coOrdinates class

    def __init__(self,coords):
        
        # no of squares in every row and column of grid(Grid is a square)
        self.grid_size=20
        # it is the width of every small box(here 800/20 = 40)
        self.box_width=self.WIDTH/self.grid_size

        # self.coords: This stores an instance of the CoOrdinates class, which presumably holds and manages data related to the coordinates used in the GUI.
        # This allows the Gui class to interact with and modify the coordinate data.
        self.coords=coords
        # Following indicate a boolean variable each which tells whether the 
        # user is placing/removing walls and the animation speed set
        self.placing_walls=False
        self.removing_walls=False
        self.animation_speed = 10

        # initialize a 2d list( list of lists ) with 0 of dimension grid_size(20)
        # initializes a 20 x 20 grid with all elements set to zero
        self.coords.maze=[
            [0 for x in range(self.grid_size)] for y in range(self.grid_size)]

        # pygame.init(): Initializes all the Pygame modules. This is required before using any Pygame functionalities.
        pygame.init()
        # initializing a window of WIDTH=800(window 800 x 800)
        self.win=pygame.display.set_mode((self.WIDTH,self.WIDTH))
        # creating clock object of pygame to handle frame rate of applications
        self.clock=pygame.time.Clock()
        # This sets the title of the Pygame window to "Pathfinding Algorithms".
        pygame.display.set_caption("PATHFINDING ALGORITHMS VISUALIZER")



    # main function for gui
    def  main(self,running=False):
        
        # self.clock.tick(self.FPS): This line ensures that the loop runs at a
        #  consistent frame rate defined by FPS (Frames Per Second). 
        # The tick method of the clock object pauses the loop to maintain 
        # the frame rate, creating smooth animations and consistent performance.
        self.clock.tick(self.FPS)
        # get the co-ordinates of the cursor
        self.mouse_x, self.mouse_y= pygame.mouse.get_pos()
        
        # if the GUI is in not running state
        if not running:
            
            # user is placing walls call method place_wall()
            if self.placing_walls==True:
                self.place_wall()
            
            # user in removing walls call method remove()
            elif self.removing_walls==True:
                 self.remove()
        # calls the event_handle method to respond to mouse and keyboard events
        # the current state of gui is also passed for method to know the current
        # state of GUI
        self.event_handle(running)

        # this line redraws the grid to reflect any changes made like walls, checkpoints etc
        self.redraw()
        # updates the display to render all the changes made using redraw()
        pygame.display.update()

    def event_handle(self,running):
        # list containing the list of run_key used for running the searching algo
        # and checkpoint_keys to create check points

        run_keys={"a","b","d","k"}
        checkpoint_keys={"1","2","3","4","5","6","7","8","9"}

        # gets key presses,iterating  over events in event queue( used for executing events
        # in a FIFO fashion)
        for event in pygame.event.get():
          
        #  If the user quits the program by closing the window, 
        # this block of code ensures that the pygame module is properly
        # uninitialized before exiting the program.
            if event.type==pygame.QUIT:
              pygame.quit()
              exit()
              
        # checks key presses   
            elif event.type==pygame.KEYDOWN:
        # retrive char representation of the key
              key=chr(event.key)

        #  Checks if the GUI is not currently running. If not, it proceeds to 
        # handle key presses related to various actions.
              if running == False:
                  # a,k,b,d

        # if the key is present in run_keys list  (a,b,d,k)
        # it calls the run_algorithm() method with the pressed key as an argument.
                if key in run_keys:
                    self.run_algorithm(key)
        # If the pressed key is "x", it calls the remove_all() method
        # of the coords object to clear the entire board.
                elif key== "x":
                    self.coords.remove_all()
        # If the pressed key is "z", it calls the remove_last() method of the
        # coords object to remove the last placed item.
                elif key=="z":
                    self.coords.remove_last()
        # place checkpoints with number keys
        # If the pressed key is in checkpoint_keys, it calls the place_check_point()
        # method with the pressed key as an argument to place a checkpoint.
                elif key in checkpoint_keys:# 1-9
                    self.place_check_point(key)
        # If the pressed key is a front slash, it calls the generate_random_maze() 
        # method of the coords object to generate a random maze.
                elif key=="/":
                        self.coords.generate_random_maze(gui)
        # a lower animation speed value means a faster animation as it represents the delay
        # in seconds, if animation speed is less or equal to 2, then set it to one so that
        # it does not end up negative else half the speed and add 1
                elif(key=="p" or key=="P") and self.animation_speed>0 :
                        if self.animation_speed <=2:
                            self.animation_speed=1
              
                        else:
                            self.animation_speed=int(self.animation_speed * 0.5) + 1
        # increased value of animation speed means a increased delay 
                elif key=="m" or key=="M":
                    self.animation_speed=int(self.animation_speed*2)+1
        # For debugging print the key on screen if none of the above conditions matcch
                else:
                    print(key)

        # if a mouse button is pressed
            elif event.type == pygame.MOUSEBUTTONDOWN:
        # ensure that the gui is in not running state
                if running==False:
        # 1 = left_click then place wall
                    if event.button==1:
                      self.placing_walls = True
        # 3 = right_clilck then remove wall
                    elif event.button==3:
                      self.removing_walls= True

        # 4 = scroll up , zoom in       
                if event.button==4:
        # no. of boxes on grid will decrease
                    self.grid_size-=1
        # since size dec, the width of evey box will increase
                    self.box_width=self.WIDTH/self.grid_size
        # 5 = scroll down, zoom out   
                elif event.button==5:
        # no of boxes will increase,effective size of every box will increase
                    self.grid_size +=1
                    self.box_width=self.WIDTH/self.grid_size
        # if the pressed mouse keys are released
            elif event.type==pygame.MOUSEBUTTONUP:
        # if the first button is released stop placing the walls
                if event.button==1:
                    self.placing_walls=False
        # if third button = right click, is released then  stop removing walls      
                elif event.button==3:
                    self.removing_walls=False


    # for redrawing the gui

    def redraw(self):
        
        # fill light pinkishish color into gui window
        self.win.fill((255,182,193))
        # responsible for drawing various elements such as nodes,walls and check points
        self.draw_points()
        # draws the grid again
        self.draw_grid()

    # draw the grid lines
    #  the draw_grid method is responsible for drawing grid lines on the 
    #  window to visually divide it into smaller sections, providing a 
    #  structured layout for the elements displayed on the GUI.Where (0,0,0)
    # refers to the black colored grid
    def draw_grid(self):
        for i in range(self.grid_size-1):
            pygame.draw.rect(self.win,(0,0,0),(((i+1)*self.box_width)-2,0,4,self.WIDTH))
            pygame.draw.rect(self.win,(0,0,0),(0,((i+1)*self.box_width)-2,self.WIDTH,4))


    # draws all the squares for the walls,checkpoints etc.
    def draw_points(self):

        # nodes in openlist are candidates for further expansion marked yellow 
        for node in self.coords.open_list:
            self.draw_box(node.position,(255,255,0))

        # already explored and not considered for further expansion: red color
        for node in self.coords.closed_list:
            self.draw_box(node.position,(255,0,0))

        # used for tracing the final path green in color
        for path in self.coords.final_path:
            self.draw_box(path,(0,255,0))

        # draw a box brown in color in the wall position
        for wall in self.coords.walls:
            self.draw_box(wall,(110,38,14))

        # place check points at positions by drawing a box blue in color plus
        # inserting the text inside it,i+1 converted to string given white color
        # centered and box width provided

        for i,point in enumerate(self.coords.check_points):
            if point != "None":
                self.draw_box(point,(0,0,255))
                self.display_text(str(i+1),(255,255,255),self.box_center(point),int(self.box_width))

    # The box_center method calculates the center coordinates of a box in the grid by:
    # Calculating the top-left corner of the box.
    # Adding half the box width to the top-left coordinates to find the center.
    def box_center(self,box):
        boxX,boxY=box
        center = ((boxX*self.box_width + (self.box_width/2)),  (boxY*self.box_width+(self.box_width/2)))

        return center
    # used to draw the box given colours and positions
    def draw_box(self,box,colour):
        boxX,boxY=box
        pygame.draw.rect(self.win,colour,
                         (boxX*self.box_width,boxY*self.box_width,
                          self.box_width,self.box_width))
        
    # gets the box coordinates given a mouse position
    # This get_box_coords method is responsible 
    # for converting the mouse position on the GUI window to the
    # corresponding grid coordinates,some approximation is involved.

    def get_box_coords(self):
        boxX=int((self.mouse_x+2)/self.box_width)
        boxY=int((self.mouse_y+2)/self.box_width)
        return (boxX,boxY)
    
    # placing checkpoints
    # index represents the check point to be placed
    def place_check_point(self,index):

        # mouse co-ordinates converted to box co-ordinates
        coords=self.get_box_coords()
        # ensures that the check point is not placed at start, end and on walls and where
        # other check points are placed

        if(coords not in self.coords.walls and coords not in self.coords.check_points):
            
            # indicates that checkpoint is placed successfully!
            sound2.play()
            # This snippet ensures that the list of checkpoints has enough space to
            # accommodate a new checkpoint at a specified index. If the list is not
            # long enough, it adds placeholder values ("None") until 
            # it reaches the required length. Then, it places the new checkpoint at
            # the specified index.
            while len(self.coords.check_points)<=int(index)-1:
                self.coords.check_points.append("None")
                self.coords.check_points[int(index)-1]=coords

    # This function allows the user to place walls on the grid. 
    # It checks if the current coordinates are not already 
    # occupied by the start point, end point, other walls, or checkpoints. 
    # If the conditions are met, it adds the current coordinates to 
    # the list of walls. This prevents the user from placing walls on invalid positions.
    def place_wall(self):
        coords=self.get_box_coords()
        if(coords not in self.coords.walls and coords not in self.coords.check_points):
            self.coords.walls.append(coords)
            sound2.play()

    # for removing nodes such as walls checkpoints etc
    def remove(self):
        coords=self.get_box_coords()
    
        if coords in self.coords.walls:
            self.coords.walls.remove(coords)
        
        elif coords in self.coords.check_points:
            self.coords.check_points.remove(coords)


    # function that prepare for and executes path finding
    def run_algorithm(self,key):
        # when the algorithm is running lock placing and removing of walls
        self.placing_walls=False
        self.removing_walls=False
        self.coords.remove_last()

        # for more than one checkpoints
        if len(self.coords.check_points) > 1:

            # create the maze array and remove missed checkpoint number
            self.coords.create_maze(gui)
            # removes any none values in the check point list
            check_points = self.coords.check_points[:]
            check_points=[point for point in check_points if point != "None"]
            # iterate through every checkpoint and pathfind to it
            for i,point in enumerate(check_points):
                if i != len(check_points)-1:
                    start = point
                    end=check_points[i+1]

                    new_path= pathfind(self.coords.maze,start,end,self,self.coords,key)

                    # The condition if new_path == None checks if a path was not found
                    # or if it's None, indicating that no valid path exists 
                    # between the given start and end points. 
                    # In such cases, it initializes new_path as an empty list [].
                    
                    if new_path == None:
                        new_path=[]
                    
                    # if valid path is found extend the final path by adding new_path
                    self.coords.final_path.extend(new_path)


    # The display_text method takes text, color, center position, and size as input.
    # It creates a font object and renders the text onto a surface.
    # It then positions this surface so that its center aligns with the given coordinates.
    # Finally, it draws the text surface onto the Pygame window.
    def display_text(self,txt,colour,center,size):
        # create font object
        font=pygame.font.Font(None,size)
        # font rendered on text_surf
        text_surf=font.render(txt,True,colour)
        # rectangular area of text_surf extracted
        text_rect=text_surf.get_rect()
        # rectangle centered around specified center point
        text_rect.center=(center)
        # changes reflected on pygame window
        self.win.blit(text_surf,text_rect)



class CoOrdinates():
    # class containing all the co-ordinates and the functions to do calculations with them

    # removing all elements associated with the instance of the class
    def __init__(self):
        self.remove_all()

    # remove_all(self): This method removes all elements associated with the instance.
    # It sets various attributes such as start, end, walls, maze, open_list, closed_list,
    # final_path, and check_points to None or empty lists, effectively clearing them.
    # This happens after the user presses 'x'
    def remove_all(self):
        self.start=None
        self.end=None
        self.walls=[]
        self.maze=[]
        self.open_list=[]
        self.closed_list=[]
        self.final_path=[]
        self.check_points=[]

    # Specifically removes the elements related to pathfinding process meaning those
    # which affect the path finding process, this is executed after the user press 'z'
    # or remove last, reintializes the window before a new pathfinding process to begin

    def remove_last(self):
        self.maze=[]
        self.open_list=[]
        self.closed_list=[]
        self.final_path=[]

    # this starts from (0,0) and checks for the largest co-ordinate( x or y) having checkpoint or
    # walls furthest from the starting point, this ensures that we have a largest distance value
    # returned which is tuple, giving info about the size of grid req to accomdate all 
    # check points and walls.Returning distance 1 greater than co-ordinate value accounting
    # for zero based indexing

    # in short gets the magnitude of largest co-ordinate(x or y) of a node from the (0, 0)


    def largest_distance(self):
        largest=0
        for wall in self.walls:
            if wall[0] > largest: largest=wall[0]
            if wall[1]> largest: largest=wall[1]

        for point in self.check_points:
            if point[0] > largest:largest=point[0]
            if point[1] > largest:largest=point[1]
        
        return largest+1
    
    # create a 2D array of the maze and its walls
    def create_maze(self,gui):

        largest_distance= self.largest_distance()

        # makes sure the size of the maze is either the size of the gui
        # or the size of the maze made using the walls and checkpoints. Ensuring that the 
        # the maze can accomdate all walls and check points

        largest = max(largest_distance,gui.grid_size)

        self.maze=[[0 for x in range(largest)] for y in range(largest)]
        for wall in self.walls:
            try:
                wall_x,wall_y=wall
                self.maze[wall_x][wall_y]=1
            except:
                pass

    
    # this is going to generate random walls on the maze and this happens when 
    # the user presses '/'

    def generate_random_maze(self,gui):
        print("Printing the positions where walls are added: ")
        self.walls=[]

        for i in range(gui.grid_size*gui.grid_size):
            
            if random.random() > 0.7:
                # only 30% of cases where value will be between 0.7 to 1
                wall=(random.randint(0,gui.grid_size-1),random.randint(0,gui.grid_size-1))
                # if the wall is not present at the generated position
                if wall not in self.walls:
                    self.walls.append(wall)
                    print(f"Added wall at {wall}")

        print("Total walls generated: ",len(self.walls))


# function for pathfinding using dfs, bfs, dijkstra and astar returns a list of 
# tuples as a path from the given start to the given end in the given maze
def pathfind(maze,start,end,gui,coords,key):
        
    # initializing the start and end nodes using start and end 
    # provided by user on the maze

        start_node = Node(None,start)
        end_node=Node(None,end)

    # In the line start_node.g = start_node.h = start_node.f = 0,
    # the properties g, h, and f of the start_node are all initialized
    # to 0, indicating the initial cost, heuristic value, and combined 
    # cost from the start node.

        start_node.g=start_node.h=start_node.f=0
        end_node.g=end_node.h=end_node.f=0

    # Initialize both open and closed list
    # initializes two lists: open_list and closed_list. The open_list
    # contains nodes that are candidates for further exploration, and
    # the closed_list contains nodes that have already been evaluated.

        open_list=[]
        closed_list=[]
    # Add start node to the open list 
        open_list.append(start_node)
        count=0

    # Till the time we have nodes in the open list: loop
        while len(open_list)>0:

    # To create a wait effect and control animation speed
            if count>=gui.animation_speed:
                sound1.play()
                count=0

    # Get the current node

                if key == "d": # dfs, get the latest node, stack or LIFO order
                    current_node=open_list[-1]
                    current_index=len(open_list)-1

                elif key=="b": # bfs, get the node in FIFO sequence
                    current_node=open_list[0]
                    current_index=0

                elif key == "a": # a*, get the node with the lowest f value
                    current_node=open_list[0]
                    current_index=0
                    for index,item in enumerate(open_list):
                        if item.f < current_node.f:
                            current_node=item
                            current_index=index

                elif key=="k": # dijkstra, get the node with the lowest g value
                    current_node=open_list[0]
                    current_index=0
                    for index,item in enumerate(open_list):
                        if item.g < current_node.g:
                            current_node=item
                            current_index=index

    # Pop current off open list, add to closed list

                open_list.pop(current_index)
                closed_list.append(current_node)
    
    # Found the goal

                if current_node == end_node:

                    sound1.stop()
                    bonus.play()

                    path=[]
                    current=current_node

                    while current is not None:
                        path.append(current.position)
                        current=current.parent
                    
                    coords.open_list=open_list
                    coords.closed_list=closed_list

    # Return the path

                    return path
                
    # Generate children
    # left, down, right, up. Which makes dfs go in up, right, down, left order
                for new_pos in [(-1, 0), (0, 1), (1, 0), (0, -1),(1,1),(1,-1),(-1,1),(-1,-1)]:

                    # get the node position
                    node_pos = (current_node.position[0] + new_pos[0], current_node.position[1]+new_pos[1])

                    # make sure within the range
                    if(node_pos[0] > (len(maze)-1) or node_pos[0] < 0 or node_pos[1]>(len(maze[len(maze)-1])-1) or node_pos[1]<0):
                        continue
                    
                    # Make sure that there is no wall
                    if maze[node_pos[0]][node_pos[1]]!=0:
                        continue
                    
                    # if node already visited
                    if Node(current_node,node_pos) in closed_list:
                        continue
                    
                    # create new child node
                    child=Node(current_node,node_pos)

                    passList=[False for closed_child in closed_list if child == closed_child]
                    if False in passList:
                        continue

                     # for dfs and bfs we dont add anything to the node values

                    if key=="k": # dijkstra, add one to g value
                        child.g=current_node.g+1

                    elif key=="a": # a*, calculate f value
                        child.g=current_node.g+1

                    # distance to end point
                    # the reason the h distance is powered by 0.6 is because
                    # it makes it prioritse diagonal paths over straight ones
                    # even though they are technically the same g distance, this makes a* look better

                        child.h=(((abs(child.position[0]-end_node.position[0]) ** 2) +
                                  (abs(child.position[1] - end_node.position[1])**2)) ** 0.6)
                        
                        child.f=child.g + child.h

                    
                    # Child is already in the open list
                    for open_node in open_list:

                    # check if the new path to children is worst or equal 
                    # than one already in the open_list (by measuring g)
                    
                        if child == open_node and child.g>= open_node.g:
                            break

                    else:
                        open_list.append(child)

            # if skipped just update the gui
            else:

                coords.open_list=open_list
                coords.closed_list=closed_list
                gui.main(True)
                count+=1


class Node():
    # node class for containing position, parent and costs
    
    def __init__(self,parent,position):
        self.parent=parent
        self.position=position
                
        self.g=0
        self.h=0
        self.f=0

            
    def __eq__(self,other):
        return self.position == other.position
            
# main loop
if __name__ == "__main__":
    gui=Gui(CoOrdinates())
    while True:
        gui.main()
