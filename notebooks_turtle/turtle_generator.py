"""Define turtle object and helper object that defines mazes"""


class create_maze:

  nx = None            # Number of squares in the grid horizontally 
  ny = None            # Number of squares in the grid vertically
  ax = None            # plotting axes for maze
  maze_number = None   # True or False, controlling whether the maze is plotted
  pond_location = None # The pond will be centered at this grid location
  maze_path = []       # path defining the maze
  maze_goal = None     # Location (x,y) of the maze goal, where the turtle wants to goal
  shortest_path_length = None # Length of shortest path from (0,0) to maze goal, while staying inside maze
  
  def __init__(self, ax, nx, ny, maze_number=False, pond_location=False):
    '''
    Creates a maze for plotting, technically we could call this a maze object.
    To use, you'll have to first create the maze, and then give the command to 
    draw the maze,

    Parameters
    ----------
    ax : graphical/plotting axes, generated with
        fig, ax = plt.subplots()

    nx : integer
      Number of squares in the grid horizontally (in the x-dimension)

    ny : integer
      Number of squares in the grid vertically (in the y-dimension)

    maze_number : False or integer
      Controls which maze to plot 
      If False, no maze is plotted.  If a number, then the maze corresponding to
      that number is plotted.

    pond_location :  False or grid coordinate (tuple)
      If False, then do not plot pond.  If a tuple like (12,12), then plot the
      pond at that location

    Returns
    -------
    A new maze for plotting (technicall, we call this a maze object)

    Example
    -------
    from matplotlib import pyplot as plt
    fig, ax = plt.subplots()
    nx = 14
    ny = 14
    maze_number = 1
    maze = create_maze(ax, nx, ny, maze_number)
    maze.draw()

    '''
    self.ax = ax
    self.nx = nx
    self.ny = ny
    self.maze_number = maze_number
    self.pond_location = pond_location
    self.maze_path = []

    if (self.maze_number != False):
      if (self.maze_number == 1):
        self.maze_path, self.maze_goal, self.shortest_path_length = self.generate_maze1()
      else:
        raise ValueError("Invalid Maze Number")

  def is_location_on_grid(self, location):
      '''
      Decide if location is a point on the grid.  First location is tested to 
      see if it's a tuple, then to see if location is inside the grid
      
      Parameters
      ----------
      location : location is a pair of numbers (technially called a tuple), 
      like (12, 12) or (5,6)

      Returns
      -------
      True or False (technically called a Boolean)
      True is returned if location is inside the grid
      False if the location is outside the grid
      '''
      
      # Note, that we accept points from -0.5 to nx-0.5, because we draw the maze 
      # from -0.5 to nx-0.5.  The same is true for the y-axis.
      if (type(location) == tuple)  and (len(location) == 2)       and \
         (location[0]%0.5 == 0)     and (location[1]%0.5 == 0) and \
         (location[0] >= -0.5)      and (location[0] <= self.nx-0.5)    and \
         (location[1] >= -0.5)      and (location[1] <= self.ny-0.5):
        return True
      else:
        return False

  def draw_line(self, point1, point2, linestyle):
    '''
    Draw a line from point1 to point 2

    Parameters
    ----------
    point1 : (x,y) pair   (technically called a tuple)
      Defines the first point for the line

    point1 : (x,y) pair   (technically called a tuple)
      Defines the second point for the line

    linestyle : 'light' or 'dark'
      Controls how dark and thick the line is

    Returns
    -------
    The plot corresponding to self.ax has a new line plotted in it
    '''
    
    if not self.is_location_on_grid(point1):
      print("Invalid point given to draw_line: " + str(point1) + ". Skipping drawing this line.")
      return
    if not self.is_location_on_grid(point2):
      print("Invalid point given to draw_line: " + str(point2) + ". Skipping drawing this line.")
      return
    
    if linestyle == 'light':
      self.ax.plot([point1[0], point2[0]], [point1[1], point2[1]], color=(0.6, 0.6, 0.6), linewidth=1)
    elif linestyle == 'dark':
      self.ax.plot([point1[0], point2[0]], [point1[1], point2[1]], color=(0.0, 0.0, 0.0), linewidth=3.5)
    else:
      print("No line drawn!  linestyle should be 'light' or 'dark' ")

  def draw_grid(self):
    '''
    Draw a background grid of size (nx, ny)

    Parameters
    ----------
    ax : graphical/plotting axes, generated with
        fig, ax = plt.subplots()

    nx : integer
      Number of squares in the grid horizontally (in the x-dimension)

    ny : integer
      Number of squares in the grid vertically (in the y-dimension)

    Returns
    -------
    The plot corresponding to self.ax has a background grid plotted on it
    '''
    import numpy as np

    # Plot all the vertical lines
    for i in np.arange(-0.5, self.nx, 1):
      point1 = (i, -0.5)
      point2 = (i, self.ny-0.5)
      self.draw_line(point1, point2, 'light')

    # Plot all the horizontal lines
    for j in np.arange(-0.5, self.ny, 1):
      point1 = (-0.5, j)
      point2 = (self.nx-0.5, j)
      self.draw_line(point1, point2, 'light')

  def draw_maze(self):
    '''
    Draw maze corresponding to the maze number given when the maze was created. 
    Maze is stored internally at self.maze_path.  See generate_maze1 for 
    description of how the maze is stored.

    Parameters
    ----------
    None

    Returns
    -------
    The plot corresponding to self.ax has the maze plotted on it

    '''
    
    for point, borders in self.maze_path:
      x_loc = point[0]
      y_loc = point[1]
      
      # Draw a borth on the top, bottom, left, or right (t, b, l, r)
      for border in borders:
        if border == 't':
          self.draw_line( (x_loc-0.5, y_loc+0.5), (x_loc+0.5, y_loc+0.5), 'dark')
        elif border == 'b':
          self.draw_line( (x_loc-0.5, y_loc-0.5), (x_loc+0.5, y_loc-0.5), 'dark')
        elif border == 'l':
          self.draw_line( (x_loc-0.5, y_loc-0.5), (x_loc-0.5, y_loc+0.5), 'dark')
        elif border == 'r':
          self.draw_line( (x_loc+0.5, y_loc-0.5), (x_loc+0.5, y_loc+0.5), 'dark')

  def draw_pond(self):
    '''
    Draw pond at location (12,12)

    Parameters
    ----------
    None

    Returns
    -------
    The plot corresponding to self.ax has the pond plotted on it

    '''
    # Draw pond centered at self.pond_location with radius 1
    import numpy as np
    pond_x = self.pond_location[0]
    pond_y = self.pond_location[1]
    x = np.linspace(pond_x-1, pond_x+1, 100)
    y1 = np.sqrt(1 - (x - pond_x)**2) + pond_y
    y2 = -np.sqrt(1 - (x - pond_x)**2) + pond_y
    self.ax.fill_between(x, y1, y2, color=(0.1176, 0.5647, 1.0) )

  def draw(self):
    '''
    Draw the maze
    Note the maze drawn is the one specified when you first created this maze
    with create_maze(...)

    Parameters
    ----------
    None

    Returns
    -------
    The plot corresponding to self.ax has the maze plotted on it

    '''
    self.draw_grid()
    if self.pond_location != False:
      self.draw_pond()
    if self.maze_number != False:
      self.draw_maze()

  def get_shortest_path_length(self):
    '''
    Return the length of the shortest path in the maze from (0,0) to the goal
    
    Parameters
    ----------
    None
    
    Returns
    -------
    Shortest path length in the maze from (0,0) to the goal
    '''
    return self.shortest_path_length
    
  def check_path_stays_on_maze(self, movements):
    '''
    Return True or False (technically called a Boolean vlaue), whether or not the list of movements stays inside the maze
      
    Parameters
    ----------
    None
    
    Returns
    -------
    True or False (technically called a Boolean value)
    True is returned if all movements stay inside the maze
    False is returned if some move in movements leaves the maze
    '''

    for move in movements:
      stayed = False
      for point, borders in self.maze_path:
        if move == point:
          stayed = True
          break
      if stayed == False:
        print("Movement to square " + str(move) + " left the maze path.")
        return False
      
    return True
  
  def check_path_includes_goal(self, movements):
    '''
    Return True or False (technically called a Boolean vlaue), whether or not the list of movements includes the goal 
      
    Parameters
    ----------
    None
    
    Returns
    -------
    True or False (technically called a Boolean value)
    True is returned if movements contains (that is reaches) the goal
    False is returned if movements does not contain (never reaches) the goal
    '''

    for move in movements:
      if move == self.maze_goal:
        return True
        
    return False

  def generate_maze1(self):
    '''
    Generate Maze 1 using a stored design.  This simplest maze leads to the 
    pond in a direct way.

    Parameters
    ----------

    Returns
    -------
    Three values are returned
      First:  maze_path defining maze 1 (list type, see Notes for details on how the maze is represented)
      Second: maze_goal location (x,y), that is, where the turtle wants to go
      Third:  shortest_path_length, that is, the length of the shortest maze path from (0,0) to the maze_goal
    
    Notes
    -----
    The maze_path is stored as list, with each list element defining one block of the maze
    For example, if maze_path[k] = ( (3,4), ('l', 'r') ),
       then this maze part is at point (3,4), with a border to the left and to the right
       And, if maze_path[k] = ( (6,2), ('t', 'b') ),
       then this maze part is at point (6,2), with a border on the top and on the bottom
    Any mixture of 'l', 'r', 't', 'b' is supported for each maze part.
    '''
    
    path = []
    path.append( ((0,0), ('t', 'b')) )
    path.append( ((1,0), ('t', 'b')) )
    path.append( ((2,0), ('t', 'b')) )
    path.append( ((3,0), ('t', 'b')) )
    path.append( ((4,0), ('t', 'b')) )
    path.append( ((5,0), ('b', 'r')) )
    
    path.append( ((5,1), ('l', 'r')) )
    path.append( ((5,2), ('l', 'r')) )
    path.append( ((5,3), ('l', 'r')) )
    path.append( ((5,4), ('l', 'r')) )
    path.append( ((5,5), ('l', 'r')) )
    path.append( ((5,6), ('l', 't')) )

    path.append( ((6,6),  ('t', 'b')) )
    path.append( ((7,6),  ('t', 'b')) )
    path.append( ((8,6),  ('t', 'b')) )
    path.append( ((9,6),  ('t', 'b')) )
    path.append( ((10,6), ('t', 'b')) )
    path.append( ((11,6), ('t', 'b')) )
    path.append( ((12,6), ('b', 'r')) )

    path.append( ((12,7),  ('l', 'r')) )
    path.append( ((12,8),  ('l', 'r')) )
    path.append( ((12,9),  ('l', 'r')) )
    path.append( ((12,10), ('l', 'r')) )
    path.append( ((12,11), ('l', 'r')) )
    path.append( ((12,12), ('l', 'r', 't')) )


    maze_goal = (12,12) 
    shortest_path_length = 25

    return path, maze_goal, shortest_path_length

  # insert maze 2, 3, 4, and so on...
  
  
##
# Begin Turtle Class (uses maze class)
##
  
class turtle_generator:

  nx = None             # Number of squares in the grid horizontally
  ny  = None            # Number of squares in the grid vertically
  start_location = None # The turtle starts at this grid location
  maze_number = None    # True or False, controlling whether the maze is plotted
  pond_location = None  # The pond will be centered at this grid location
  movements = None      # List of spatial locations for turtle to move through
  leave_trail = None    # List of same length as movements, boolean values, if True, 
                        #  turtle leaves a trail in that square for plotting, else, not trail is left

  def __init__(self, nx=14, ny=14, start_location=(0,0), maze_number=False,
               pond_location=False):
    '''
    Creates a turtle object, can use other function to move it on the grid and
    plot the background grid and maze for the turtle to explore

    Parameters
    ----------

    nx : integer
      Number of squares in the grid horizontally (in the x-dimension)

    ny : integer
      Number of squares in the grid vertically (in the y-dimension)

    start_location : pair of numbers (technically called a tuple)
      This defines the starting location for the turtle, like (0,0), or (2,2)
      This location should be on the grid, and not outside the grid.

    maze_number : If maze_number is False, then no maze is plotted.
      If maze_number is a number (like 1 or 2), then the maze corresponding to
      that number is used and plotted

    pond_location : If pond_location is False, then no pond is plotted.
      If pond_location is a pair of numbers (technially called a tuple), then
      this defines the pond location on the grid, like (12, 12) or (5,6).
      This location should be on the grid, and not outside the grid.

    Returns
    -------
    A new turtle for moving around (technically, we call this a turtle object)

    Example
    -------
    turtle = turtle_generator()

    '''

    # Set nx: check that the user's desired nx value is a positive integer
    if (type(nx) == int) and (nx > 0):
      self.nx = nx
    else:
      self.nx = 14
      print("Invalid nx value given. nx should be a positive integer. Using default nx=14 instead")

    # Set ny: check that the user's desired ny value is a positive integer
    if (type(ny) == int) and (ny > 0):
      self.ny = ny
    else:
      self.ny = 14
      print("Invalid ny value given. ny should be a positive integer. Using default ny=14 instead")

    # Set start_location: check that user's desired start_location is a valid location on the grid
    if self.is_location_on_grid(start_location):
      self.start_location = start_location
    else:
      self.start_location = (0,0)
      print("Invalid start location given. start should be coordinates inside the grid like (0,0) or (2,2). Using default value (0,0) instead.")

    # Set maze_number: check that value is either False (for no maze) or a value maze number
    if (maze_number == False) or (maze_number == 1) or (maze_number == 2) or (maze_number == 3):
      self.maze_number = maze_number
    else:
      self.maze_number = False
      print("Invalid maze_number, should be either False (for no maze), or a supported maze number.  Currently, we support three mazes, maze_number = 1 or 2 or 3. Using default value False instead.")

    # Set pond_location: check that value is either False (for no pond) or a valid pond location
    if (pond_location == False) or self.is_location_on_grid(pond_location):
      self.pond_location = pond_location
    else:
      self.pond_location = False
      print("Invalid pond_location value, should be either False (for no pond), or coordinates inside the grid like (0,0) or (2,2). Using default value False instead.")

    # Set up plotting environment for animation
    import matplotlib.pyplot as plt
    plt.rcParams['figure.dpi'] = 80
    plt.rcParams["animation.html"] = "jshtml" # javascript html writer
    plt.ioff() # Turn interactive mode off
    plt.rcParams["figure.figsize"] = [7, 7]
    plt.rcParams["figure.autolayout"] = True

  def is_location_on_grid(self, location):
      '''
      Decide if location is a point on the grid.  First location is tested to 
      see if it's a tuple, then to see if location is inside the grid
      
      Parameters
      ----------
      location : location is a pair of numbers (technially called a tuple), 
      like (12, 12) or (5,6)

      Returns
      -------
      True or False (technically called a Boolean)
      True is returned if location is inside the grid
      False if the location is outside the grid
      '''
      if (type(location) == tuple)  and (len(location) == 2)       and \
        (type(location[0]) == int) and (type(location[1]) == int) and \
        (location[0] >= 0)          and (location[0] <= self.nx)    and \
        (location[1] >= 0)          and (location[1] <= self.ny):
        return True
      else:
        return False

  def download_turtle_image(self):
    '''
    This function should download a little image of a turtle into your current
    folder.  The turtle is used for our animations.

    Parameters
    ----------
    None

    Returns
    ------
    Downloads turtle image to current folder (i.e., present working directory)
    If there is a problem downloading, this function prints a message
    '''
    
    # We skip using the google drive location, as Google blocks downloads of PNGs after around 50 downloads 
    #import subprocess
    #result = subprocess.run(['curl -L "https://drive.google.com/uc?export=download&id=1LZBRk31Jan7yPgE44spPkxIK8rNc_dcU" > turtle.png;'], shell=True, capture_output=True)
    import os
    from urllib.request import urlretrieve
    (file1, message1) = urlretrieve('https://raw.githubusercontent.com/jbschroder/CS108/main/notebooks_turtle/turtle.png', 'turtle.png')

    OK = os.path.isfile('./turtle.png')
    if(OK == False):
      print("Something went wrong with downloading turtle image")

  def start_new_journey(self):
    '''
    Get the turtle all ready to start a new journey beginning at the turtle's
    start location

    Parameters
    ----------
    None

    Returns
    -------
    The turtle is updated internally for a new journey beginning at
    the turtle's start location
    '''
    self.movements = [self.start_location]
    self.leave_trail = [False]

  def move_left(self, leave_trail=False):
    '''
    Move turtle to the left by one square

    Parameters
    ----------
    leave_trail : True or False (technically called a Boolean)
    True: will leave a marked trail by the turtle
    False: will not leave a market trail here by the turtle

    Returns
    -------
    This turtle's list of movements is modified by adding a new location at
    the end, such that the turtle will move one square to the left

    Example
    --------
    If       turtle.movements = [(2,2)]
    Then     turtle.move_left()
    Updates  turtle.movements = [(2,2), (1,2)]
    '''
    try:
      last_x, last_y = self.movements[-1]
      new_location = (last_x-1, last_y)
      if self.is_location_on_grid(new_location):
        self.movements.append(new_location)
        self.leave_trail.append(leave_trail)
      else:
        print("You tried to move off the grid to location " + str(new_location) + ".  Ignoring this move.")
    except:
      raise ValueError("You need to call start_new_journey first")

  def move_right(self, leave_trail=False):
    '''
    Move turtle to the right by one square

    Parameters
    ----------
    leave_trail : True or False (technically called a Boolean)
    True: will leave a marked trail by the turtle
    False: will not leave a market trail here by the turtle

    Returns
    -------
    This turtle's list of movements is modified by adding a new location at
    the end, such that the turtle will move one square to the right

    Example
    --------
    If       turtle.movements = [(2,2)]
    Then     turtle.move_right()
    Updates  turtle.movements = [(2,2), (3,2)]
    '''
    try:
      last_x, last_y = self.movements[-1]
      new_location = (last_x+1, last_y)
      if self.is_location_on_grid(new_location):
        self.movements.append(new_location)
        self.leave_trail.append(leave_trail)
      else:
        print("You tried to move off the grid to location " + str(new_location) + ".  Ignoring this move.")
    except:
      raise ValueError("You need to call start_new_journey first")

  def move_up(self, leave_trail=False):
    '''
    Move turtle up by one square

    Parameters
    ----------
    leave_trail : True or False (technically called a Boolean)
    True: will leave a marked trail by the turtle
    False: will not leave a market trail here by the turtle

    Returns
    -------
    This turtle's list of movements is modified by adding a new location at
    the end, such that the turtle will move one square up

    Example
    --------
    If       turtle.movements = [(2,2)]
    Then     turtle.move_up()
    Updates  turtle.movements = [(2,2), (2,3)]
    '''
    try:
      last_x, last_y = self.movements[-1]
      new_location = (last_x, last_y+1)
      if self.is_location_on_grid(new_location):
        self.movements.append(new_location)
        self.leave_trail.append(leave_trail)
      else:
        print("You tried to move off the grid to location " + str(new_location) + ".  Ignoring this move.")
    except:
      raise ValueError("You need to call start_new_journey first")

  def move_down(self, leave_trail=False):
    '''
    Move turtle down by one square

    Parameters
    ----------
    leave_trail : True or False (technically called a Boolean)
    True: will leave a marked trail by the turtle
    False: will not leave a market trail here by the turtle


    Returns
    -------
    This turtle's list of movements is modified by adding a new location at
    the end, such that the turtle will move one square donw

    Example
    --------
    If       turtle.movements = [(2,2)]
    Then     turtle.move_down()
    Updates  turtle.movements = [(2,2), (2,1)]
    '''
    try:
      last_x, last_y = self.movements[-1]
      new_location = (last_x, last_y-1)
      if self.is_location_on_grid(new_location):
        self.movements.append(new_location)
        self.leave_trail.append(leave_trail)
      else:
        print("You tried to move off the grid to location " + str(new_location) + ".  Ignoring this move.")
    except:
      raise ValueError("You need to call start_new_journey first")

  def show_starting_position(self):
    '''
    Plot the turtle on the starting grid, no animation, just show how everything starts

    Parameters
    ----------
    None

    Returns
    -------
    A plot is made showing the turtle at it's starting position
    '''
    import matplotlib.pyplot as plt
    import numpy as np
    from matplotlib.offsetbox import OffsetImage, AnnotationBbox
    
    # Turn on interactive (inline plotting) for notebook
    plt.ion()
    
    # Create our blank plot
    fig, ax = plt.subplots()

    # Download turtle image for plotting, and then load that image into Python
    self.download_turtle_image()
    image = OffsetImage(plt.imread('./turtle.png', format="png"), zoom=0.1)

    ab = AnnotationBbox(image, self.start_location, frameon=False)
    ax.add_artist(ab)

    # Create maze and draw it
    maze = create_maze(ax, self.nx, self.ny, self.maze_number, self.pond_location)
    maze.draw()

    # Add axes ticks
    plt.xticks(range(self.nx), fontsize=15)
    plt.yticks(range(self.ny), fontsize=15)


  def check_stayed_on_maze_path(self):
    '''
    Check whether turtle stayed on maze path

    Parameters
    --------
    None

    Returns
    --------
    True or False (technically called a Boolean)
    True is returned if the turtle always stayed on the maze path. 
    False is returned if the turtle stepped off the path at some point

    Example
    -------
    turtle.check_stayed_on_maze_path()
    '''
    
    # Check that the turtle has been initialized and moved
    if (not hasattr(self, 'movements')) or (self.movements == []) or (self.movements == None):
      print("You don't have any movements yet!\n Try doing\n turtle.start_new_journey(), followed by some movements like\n turtle.move_up()")
      return
    
    if self.maze_number == False:
      print("You did not give a maze number when creating this turtle, so you can't check whether the turtle stayed on maze path.")
      return None
    
    # Note, we don't plot the maze, so we pass in None for the ax
    maze = create_maze(None, self.nx, self.ny, self.maze_number, self.pond_location)
    
    return maze.check_path_stays_on_maze(self.movements)
    
  def check_reached_maze_goal(self):
    '''
    Check whether turtle reaches the maze goal, for instance, reaches the pond or food

    Parameters
    --------
    None

    Returns
    --------
    True or False (technically called a Boolean)
    True is returned if the turtle reaches the maze goal, for instance, reaches the pond or food
    False is returned if the turtle never reaches the goal 

    Example
    -------
    turtle.check_reached_maze_goal()
    '''
    
    # Check that the turtle has been initialized and moved
    if (not hasattr(self, 'movements')) or (self.movements == []) or (self.movements == None):
      print("You don't have any movements yet!\n Try doing\n turtle.start_new_journey(), followed by some movements like\n turtle.move_up()")
      return
    
    if self.maze_number == False:
      print("You did not give a maze number when creating this turtle, so you can't check whether the turtle reached the maze goal.")
      return None
    
    # Note, we don't plot the maze, so we pass in None for the ax
    maze = create_maze(None, self.nx, self.ny, self.maze_number, self.pond_location)
    
    return maze.check_path_includes_goal(self.movements)  

  def check_continuous_movements(self):
    '''
    Check whether turtle's movements are all continuous, i.e., the movements 
    don't skip or jump over squares (which would not be fair)
    

    Parameters
    --------
    None

    Returns
    --------
    True or False (technically called a Boolean)
    True is returned if the turtle's movements are all continuous and don't skip any squares 
    False is returned if some square(s) are skipped over

    Example
    -------
    turtle.check_continuous_movements()
    '''
    
    # Check that the turtle has been initialized and moved
    if (not hasattr(self, 'movements')) or (self.movements == []) or (self.movements == None):
      print("You don't have any movements yet!\n Try doing\n turtle.start_new_journey(), followed by some movements like\n turtle.move_up()")
      return
    
    movements_continuous = True
    old_movement = self.movements[0]
    for new_movement in self.movements[1:]:
      
      # check step size is only one square
      step_size = abs(old_movement[0] - new_movement[0]) + abs(old_movement[1] - new_movement[1])
      if (step_size != 1) and (step_size != 0):
        movements_continuous = False
        print("Movement not continuous from " + str(old_movement) + " to " + str(new_movement) + ". You probably jumped a square.")
        break
      
      old_movement = new_movement

    return movements_continuous

  def check_maze_completed(self):
    '''
    Check whether turtle completed the maze

    Parameters
    --------
    None

    Returns
    --------
    True or False (technically called a Boolean)
    True is returned if the turtle successfully completes the maze by doing the following:
      Stay inside maze path
      Uses continuous movements from start to finish (no skipping squares or cheating)
      Reaches the maze goal
    
    False is returned if the turtle fails either of the above conditions

    Example
    -------
    turtle.check_maze_completed()
    '''
    
    # Check that the turtle has been initialized and moved
    if (not hasattr(self, 'movements')) or (self.movements == []) or (self.movements == None):
      print("You don't have any movements yet!\n Try doing\n turtle.start_new_journey(), followed by some movements like\n turtle.move_up()")
      return
    
    if self.maze_number == False:
      print("You did not give a maze number when creating this turtle, so you can't check whether the turtle finished the maze.")
      return None
    
    if self.check_continuous_movements():
      if self.check_reached_maze_goal():
        if self.check_stayed_on_maze_path():
          return True
        else:
          print("Turtle did not stay on maze path")
      else:
        print("Turtle did not reach maze goal")
    else:
      print("Turtle did not use continuous movement, that is, some squares were skipped over")
    
    return False
    

  def check_maze_completed_with_shortest_path(self):
    '''
    Check whether turtle completed the maze using the shortest path and a starting position of (0,0)

    Parameters
    --------
    None

    Returns
    --------
    True or False (technically called a Boolean)
    True is returned if the turtle successfully completes the maze by doing the following:
      Uses continuous movements from start to finish (no skipping squares or cheating)
      Reaches the maze goal
      Starts at position (0,0)
      Uses the shortest path from (0,0) to the maze goal
    
    False is returned if the turtle fails any of the above conditions

    Example
    -------
    turtle.check_maze_completed_with_shortest_path()
    '''
    
    # Check that the turtle has been initialized and moved
    if (not hasattr(self, 'movements')) or (self.movements == []) or (self.movements == None):
      print("You don't have any movements yet!\n Try doing\n turtle.start_new_journey(), followed by some movements like\n turtle.move_up()")
      return
    
    if self.maze_number == False:
      print("You did not give a maze number when creating this turtle, so you can't check whether the turtle finished the maze.")
      return None    
    
    if self.check_maze_completed():
      if self.movements[0] == (0,0):
        # Note, we don't plot the maze, so we pass in None for the ax
        maze = create_maze(None, self.nx, self.ny, self.maze_number, self.pond_location)
        if len(self.movements) == maze.get_shortest_path_length():
          return True
        else:
          print("Did not use shortest path.  Your path was length " + str(len(self.movements)) + ". The shortest path was " + str(maze.get_shortest_path_length()))
      else:
        print("Starting position was incorrect.  Should use (0,0), you instead used " + str(self.movements[0]) )
    
    return False

  def plot_trail(self, ax, t):
    '''
    Plot the turtle's trail at all the locations specified by a move_* command

    Parameters
    ----------
    ax : graphical/plotting axes, generated with
        fig, ax = plt.subplots()
    t : number, indicating the number of total movements where we plot a trail

    Returns
    -------
    Plot corresponding to ax has turtle trail plotted

    '''
    if type(t) != int:
      print("Must request integer number of movements when plotting a trail")
      return None
    if t > len(self.movements) or t > len(self.leave_trail):
      print("You have requested too many movements to plot a trail for.  You only have " + str(len(self.movements)) + " stored movements")

    for i in range(t):
      if self.leave_trail[i]:
        move = self.movements[i]
        x_loc = move[0]
        y_loc = move[1]
        ax.fill_between([x_loc-0.5, x_loc+0.5], [y_loc-0.5, y_loc-0.5], [y_loc+0.5, y_loc+0.5], color='green')

  def is_pond_above(self):
    '''
    Return True or False, whether the pond is above the current turtle location

    Parameters
    ----------
    None

    Returns
    -------
    True or False (technically called a Boolean)
      True is returned if the pond is above you
      False is returned if the pond is not above you
    '''
    
    # Check that the turtle has been initialized and moved
    if (not hasattr(self, 'movements')) or (self.movements == []) or (self.movements == None):
      print("You don't have any movements yet!\n Try doing\n turtle.start_new_journey(), followed by some movements like\n turtle.move_up()")
      return
    
    # Check that the pond location is set
    if self.pond_location == False or self.pond_location == None:
      print("You didn't specify a pond location when creating the turtle.  So, I can't answer this question about the pond.") 
      return

    current_loc = self.movements[-1]
    pond_loc = self.pond_location

    if current_loc[1] < pond_loc[1]:
      return True
    else:
      return False
  
  def is_pond_below(self):
    '''
    Return True or False, whether the pond is below the current turtle location

    Parameters
    ----------
    None

    Returns
    -------
    True or False (technically called a Boolean)
      True is returned if the pond is below you
      False is returned if the pond is not below you
    '''
    
    # Check that the turtle has been initialized and moved
    if (not hasattr(self, 'movements')) or (self.movements == []) or (self.movements == None):
      print("You don't have any movements yet!\n Try doing\n turtle.start_new_journey(), followed by some movements like\n turtle.move_up()")
      return
    
    # Check that the pond location is set
    if self.pond_location == False or self.pond_location == None:
      print("You didn't specify a pond location when creating the turtle.  So, I can't answer this question about the pond.") 
      return

    current_loc = self.movements[-1]
    pond_loc = self.pond_location

    if current_loc[1] > pond_loc[1]:
      return True
    else:
      return False

  def is_pond_to_right(self):
    '''
    Return True or False, whether the pond is to the right of the current turtle location

    Parameters
    ----------
    None

    Returns
    -------
    True or False (technically called a Boolean)
      True is returned if the pond is to the right of you
      False is returned if the pond is to the right of you
    '''
    
    # Check that the turtle has been initialized and moved
    if (not hasattr(self, 'movements')) or (self.movements == []) or (self.movements == None):
      print("You don't have any movements yet!\n Try doing\n turtle.start_new_journey(), followed by some movements like\n turtle.move_up()")
      return
    
    # Check that the pond location is set
    if self.pond_location == False or self.pond_location == None:
      print("You didn't specify a pond location when creating the turtle.  So, I can't answer this question about the pond.") 
      return

    current_loc = self.movements[-1]
    pond_loc = self.pond_location

    if current_loc[0] < pond_loc[0]:
      return True
    else:
      return False

  def is_pond_to_left(self):
    '''
    Return True or False, whether the pond is to the left of the current turtle location

    Parameters
    ----------
    None

    Returns
    -------
    True or False (technically called a Boolean)
      True is returned if the pond is to the left of you
      False is returned if the pond is to the left of you
    '''
    
    # Check that the turtle has been initialized and moved
    if (not hasattr(self, 'movements')) or (self.movements == []) or (self.movements == None):
      print("You don't have any movements yet!\n Try doing\n turtle.start_new_journey(), followed by some movements like\n turtle.move_up()")
      return
    
    # Check that the pond location is set
    if self.pond_location == False or self.pond_location == None:
      print("You didn't specify a pond location when creating the turtle.  So, I can't answer this question about the pond.") 
      return

    current_loc = self.movements[-1]
    pond_loc = self.pond_location

    if current_loc[0] > pond_loc[0]:
      return True
    else:
      return False


  def watch_me_move(self):
    '''
    Finalize and create animation

    Parameters
    --------
    None

    Returns
    --------
    anim : animation object
      anim stores a full, complete animation

    Example
    -------
    Let turtle.movements = [(2,2), (3,3)]
    Then the animation will be a turtle that goes from square (2,2) to
    square (3,3) on the grid
    '''
    import matplotlib.pyplot as plt
    import numpy as np
    from matplotlib.offsetbox import OffsetImage, AnnotationBbox
    import matplotlib.animation

    # Check that we have actual movements to plot
    if (not hasattr(self, 'movements')) or (self.movements == []) or (self.movements == None):
      print("You don't have any movements yet!\n Try doing\n turtle.start_new_journey(), followed by some movements like\n turtle.move_up()")
      return

    # Create our blank plot
    fig, ax = plt.subplots()

    # Download turtle image for plotting, and then load that image into Python
    self.download_turtle_image()
    image = OffsetImage(plt.imread('./turtle.png', format="png"), zoom=0.1)

    # Define helper function for animation, which draws each animation frame
    def animate(t):
      plt.cla()
      ab = AnnotationBbox(image, self.movements[t], frameon=False)
      ax.add_artist(ab)
      
      # plot trail up to and including movement t
      self.plot_trail(ax, t+1)

      # Create maze and draw it
      maze = create_maze(ax, self.nx, self.ny, self.maze_number, self.pond_location)
      maze.draw()

      # Add axes ticks
      plt.xticks(range(self.nx), fontsize=15)
      plt.yticks(range(self.ny), fontsize=15)

    #ax.axis('equal')
    anim = matplotlib.animation.FuncAnimation(fig, animate, frames=len(self.movements), interval=400, repeat=False)

    return anim

