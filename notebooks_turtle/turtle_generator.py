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
      self.ax.plot([point1[0], point2[0]], [point1[1], point2[1]], color=(0.0, 0.0, 0.0), linewidth=3)
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

  def find_open_directions(self, location):
    '''
    Given a location on the maze path, return which directions are open in the maze: 'l', 'r', 't', 'b'
    
    Parameters
    ----------
    location : (x,y) pair   (technically called a tuple)
      location on the maze path

    Returns
    -------
    List of directions that are open in the maze path at this location, 
      For example, ['l', 'r', 't'] would indicated that the maze path is open
      to the left, right, and top of the current location.  If 'b' were present,
      this represents below.

    Notes
    -----
    If the location is not on the maze, False is returned
    '''

    for point, borders in self.maze_path:
      if (point[0] == location[0]) and (point[1] == location[1]):
        open_directions = []
        for direction in ['l', 'r', 't', 'b']:
          if direction not in borders:
            open_directions.append(direction)
        #
        return open_directions

    # This location not found on the maze, so returning False
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
    path.append( ((0,0), ('t', 'b','l')) )
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
# Begin helper class that defines a simple individual turtle
##
  
class turtle:

  start_location = None    # The turtle starts at this grid location
  movements = None         # List of spatial locations for turtle to move through
  leave_trail = None       # List of same length as movements, boolean values, if True, 
                           #  turtle leaves a trail in that square for plotting, else, no trail is left

  def __init__(self, start_location=(0,0)):
    '''
    Creates a simple individual turtle object. Individual turtles are controlled and 
    managed through the turtle_generator object

    Parameters
    ----------

    start_location : pair of numbers (technically called a tuple)
      This defines the starting location for the turtle, like (0,0), or (2,2)
      This location should be on the grid, and not outside the grid.

    Returns
    -------
    A new single turtle for moving around 

    Example
    -------
    turtle = turtle()

    '''

    # Initialize starting location
    self.start_location = start_location

    # Initialize list of movements and turtle trail markings.
    self.movements = [ start_location ]
    self.leave_trail = [ False ]

  def current_location(self):
    '''
    Return the turtle's current location

    Parameters
    ----------
    None

    Returns
    -------
    Current location for this turtle in terms of (x,y) coordinates
      For instance, if (4,5) is returned, then the turtle is at location 4 in
      the x-direction and 5 in the y-direction
    '''

    return tuple(self.movements[-1])

  def undo_last_move(self):
    '''
    Undo the last move by this turtle

    Parameters
    ----------
    None

    Returns
    -------
    Updates the turtle's movements internally to undo (erase) the last move
    '''
    if (len(self.movements) == 0) or (len(self.leave_trail) == 0):
      print("You don't have any more moves to undo!  Skipping this")
      return

    self.movements.pop()
    self.leave_trail.pop()

  def get_movements_and_trail(self):
    '''
    Return copy of the turtle's movements and trail

    Parameters
    ----------
    None

    Returns
    -------
    Two values, movemements and trail
      movements is a list of all the spatial locations the turtle has moved
      through, like [(0,0), (1,0), (2,0), (3,0)] represents moving in a 
      horizontal line
      
      trail is a list of True and False values, like [False, True, True,
      False].  Here, the turtle has left a visible trail in the second and
      third squares, but not the initial or final square.
    '''

    return list(self.movements), list(self.leave_trail) 


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

    last_x, last_y = self.movements[-1]
    new_location = (last_x-1, last_y)
    self.movements.append(new_location)
    self.leave_trail.append(leave_trail)
    
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
    last_x, last_y = self.movements[-1]
    new_location = (last_x+1, last_y)
    self.movements.append(new_location)
    self.leave_trail.append(leave_trail)

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
    last_x, last_y = self.movements[-1]
    new_location = (last_x, last_y+1)
    self.movements.append(new_location)
    self.leave_trail.append(leave_trail)

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
    last_x, last_y = self.movements[-1]
    new_location = (last_x, last_y-1)
    self.movements.append(new_location)
    self.leave_trail.append(leave_trail)

  def check_continuous_movements(self):
    '''
    Check whether the turtle's movements are all continuous, i.e., the movements 
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

  
##
# Begin Turtle Class (manages using multiple turtles, and uses maze class)
##
  
class turtle_generator:

  nx = None                # Number of squares in the grid horizontally
  ny  = None               # Number of squares in the grid vertically
  start_location = None    # The turtle starts at this grid location
  maze_number = None       # True or False, controlling whether the maze is plotted
  pond_location = None     # The pond will be centered at this grid location
  turtles = None           # List of individual turtles
  number_of_turtles = None # Number of turtles to model (currently tested for only a couple)a
  turtle_tape = None       # List indicating which turtle moved, when, e.g., [0, 0, 1] indicates
                           #   that turtle 0 moved twice, and then turtle 1 moved once
  plotting_offsets = None  # Offsets for plotting multiple turtles in a square
  turtle_scaling = None    # Estimate on how much to scale each turtle as it's plotted on different grid sizes

  def __init__(self, nx=14, ny=14, start_location=(0,0), maze_number=False,
               pond_location=False, number_of_turtles=1):
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
    
    number_of_turtles : single number (like 1, 2 or 3), this number sets the 
      number of turtles to model

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

    # Set number of turtles: check that the user's desired number_of_turtles is a positive integer
    if (type(number_of_turtles) == int) and (number_of_turtles > 0):
      self.number_of_turtles = number_of_turtles
    else:
      self.number_of_turtles = 1
      print("Invalid number_of_turtles value given; number_of_turtles should be a positive integer. Using default value of 1 instead")

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
      print("Invalid maze_number, should be either False (for no maze), or a supported maze number.\nCurrently, we support three mazes, maze_number = 1 or 2 or 3. Using default value False instead.")

    # Set pond_location: check that value is either False (for no pond) or a valid pond location
    if (pond_location == False) or self.is_location_on_grid(pond_location):
      self.pond_location = pond_location
    else:
      self.pond_location = False
      print("Invalid pond_location value, should be either False (for no pond), or coordinates inside the grid like (0,0) or (2,2). Using default value False instead.")

    # Set plotting offsets for multiple turtles
    if self.number_of_turtles == 1:
      self.plotting_offsets = [ (0,0) ]
    elif self.number_of_turtles == 2:
      self.plotting_offsets = [ (-0.09,0.09), (0.09,-0.09) ]
    elif self.number_of_turtles == 3:
      self.plotting_offsets = [ (-0.105,0.105), (0.105,0.105), (-0.105, -0.105) ]
    elif self.number_of_turtles == 4:
      self.plotting_offsets = [ (-0.12,0.12), (-0.12,-0.12), (0.12, -0.12), (0.12,0.12) ]
    else:
      raise ValueError("Only up to 4 turtles supported")

    # Set up plotting environment for animation
    import matplotlib.pyplot as plt
    try:
      # if in a notebook, do inline
      get_ipython().run_line_magic('matplotlib', 'inline')
    except:
      pass
    plt.rcParams['figure.dpi'] = 72
    plt.rcParams["animation.html"] = "jshtml" # javascript html writer
    plt.ioff() # Turn interactive mode off
    plt.rcParams["figure.figsize"] = [7, 7]
    #plt.rcParams["figure.autolayout"] = True

    # Set the scaling factor so that each turtle is the right number of pixels across
    # assumes (7,7) figsize and 72 dpi, and a turtle image that is 285 pixels across
    # pixel_size_per_square = (image_size_in_inches * dpi / number_of_squares ) * factor to account for size of axes and labels
    pixel_size_per_square = (7.*72. / max(self.nx, self.ny))*.76
    self.turtle_scaling = pixel_size_per_square/285.   

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
        (location[0] >= 0)          and (location[0] < self.nx)    and \
        (location[1] >= 0)          and (location[1] < self.ny):
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
    (file2, message2) = urlretrieve('https://raw.githubusercontent.com/jbschroder/CS108/main/notebooks_turtle/turtle_left.png', 'turtle_left.png')
    (file3, message3) = urlretrieve('https://raw.githubusercontent.com/jbschroder/CS108/main/notebooks_turtle/turtle_right.png', 'turtle_right.png')
 
    for fname in ['./turtle.png', './turtle_left.png', './turtle_right.png']:
      OK = os.path.isfile(fname)
      if(OK == False):
        print("Something went wrong with downloading turtle image " + fname)

  def start_new_journey(self):
    '''
    Get all the turtles ready to start a new journey, beginning at the
    start location

    Parameters
    ----------
    None

    Returns
    -------
    The turtle generator is updated internally so that each turtle is ready 
    for a new journey beginning at the start location
    '''
    
    self.turtles = [ turtle(self.start_location) for k in range(self.number_of_turtles) ]
    self.turtle_tape = []

  def move_left(self, leave_trail=False, which_turtle=0):
    '''
    Move turtle to the left by one square

    Parameters
    ----------
    which_turtle : number (such as 1, 2, or 3), which specifies which turtle 
      is starting a new journey
    
    leave_trail : True or False (technically called a Boolean)
      True: will leave a marked trail by the turtle
      False: will not leave a market trail here by the turtle

    Returns
    -------
    The turtle numbered "which_turtle" is moved one square to the left
      For example, if the turtle was at location (2,2), then it would move to location (1,2) 
    '''
    
    if (type(which_turtle) != int) or (which_turtle < 0) or (which_turtle > self.number_of_turtles-1):
      print("which_turtle must equal a valid turtle number. You have " + str(self.number_of_turtles) + \
            " total turtles to work with, numbered starting at 0.  You entered " + str(which_turtle) + \
            " thus this operation cannot be completed.")

    try:
      self.turtles[which_turtle].move_left(leave_trail=leave_trail)
      new_location = self.turtles[which_turtle].current_location()
      if not self.is_location_on_grid(new_location):
        self.turtles[which_turtle].undo_last_move()
        print("You tried to move off the grid to location " + str(new_location) + ".  Ignoring this move.")
      else:
        self.turtle_tape.append(which_turtle)
    except:
      raise ValueError("You need to call start_new_journey first")

  def move_right(self, leave_trail=False, which_turtle=0):
    '''
    Move turtle to the right by one square

    Parameters
    ----------
    which_turtle : number (such as 1, 2, or 3), which specifies which turtle 
      is starting a new journey
    
    leave_trail : True or False (technically called a Boolean)
      True: will leave a marked trail by the turtle
      False: will not leave a market trail here by the turtle

    Returns
    -------
    The turtle numbered "which_turtle" is moved one square to the right
      For example, if the turtle was at location (2,2), then it would move to location (3,2) 
    '''
    
    if (type(which_turtle) != int) or (which_turtle < 0) or (which_turtle > self.number_of_turtles-1):
      print("which_turtle must equal a valid turtle number. You have " + str(self.number_of_turtles) + \
            " total turtles to work with, numbered starting at 0.  You entered " + str(which_turtle) + \
            " thus this operation cannot be completed.")

    try:
      self.turtles[which_turtle].move_right(leave_trail=leave_trail)
      new_location = self.turtles[which_turtle].current_location()
      if not self.is_location_on_grid(new_location):
        self.turtles[which_turtle].undo_last_move()
        print("You tried to move off the grid to location " + str(new_location) + ".  Ignoring this move.")
      else:
        self.turtle_tape.append(which_turtle)
    except:
      raise ValueError("You need to call start_new_journey first")

  def move_up(self, leave_trail=False, which_turtle=0):
    '''
    Move turtle up by one square

    Parameters
    ----------
    which_turtle : number (such as 1, 2, or 3), which specifies which turtle 
      is starting a new journey
    
    leave_trail : True or False (technically called a Boolean)
      True: will leave a marked trail by the turtle
      False: will not leave a market trail here by the turtle

    Returns
    -------
    The turtle numbered "which_turtle" is moved one square to the right
      For example, if the turtle was at location (2,2), then it would move to location (2,3) 
    '''
    
    if (type(which_turtle) != int) or (which_turtle < 0) or (which_turtle > self.number_of_turtles-1):
      print("which_turtle must equal a valid turtle number. You have " + str(self.number_of_turtles) + \
            " total turtles to work with, numbered starting at 0.  You entered " + str(which_turtle) + \
            " thus this operation cannot be completed.")

    try:
      self.turtles[which_turtle].move_up(leave_trail=leave_trail)
      new_location = self.turtles[which_turtle].current_location()
      if not self.is_location_on_grid(new_location):
        self.turtles[which_turtle].undo_last_move()
        print("You tried to move off the grid to location " + str(new_location) + ".  Ignoring this move.")
      else:
        self.turtle_tape.append(which_turtle)
    except:
      raise ValueError("You need to call start_new_journey first")

  def move_down(self, leave_trail=False, which_turtle=0):
    '''
    Move turtle down by one square

    Parameters
    ----------
    which_turtle : number (such as 1, 2, or 3), which specifies which turtle 
      is starting a new journey
    
    leave_trail : True or False (technically called a Boolean)
      True: will leave a marked trail by the turtle
      False: will not leave a market trail here by the turtle

    Returns
    -------
    The turtle numbered "which_turtle" is moved one square to the right
      For example, if the turtle was at location (2,2), then it would move to location (2,1) 
    '''
    
    if (type(which_turtle) != int) or (which_turtle < 0) or (which_turtle > self.number_of_turtles-1):
      print("which_turtle must equal a valid turtle number. You have " + str(self.number_of_turtles) + \
            " total turtles to work with, numbered starting at 0.  You entered " + str(which_turtle) + \
            " thus this operation cannot be completed.")

    try:
      self.turtles[which_turtle].move_down(leave_trail=leave_trail)
      new_location = self.turtles[which_turtle].current_location()
      if not self.is_location_on_grid(new_location):
        self.turtles[which_turtle].undo_last_move()
        print("You tried to move off the grid to location " + str(new_location) + ".  Ignoring this move.")
      else:
        self.turtle_tape.append(which_turtle)
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
    # Shrink turtle if more than one
    zoom = self.turtle_scaling * (1.0 / (1.0 + (self.number_of_turtles-1)*0.2))
    image = OffsetImage(plt.imread('./turtle.png', format="png"), zoom=zoom)

    for k in range(self.number_of_turtles):
      plot_location = ( self.start_location[0] + self.plotting_offsets[k][0], self.start_location[1] + self.plotting_offsets[k][1])
      ab = AnnotationBbox(image, plot_location , frameon=False)
      ax.add_artist(ab)

    # Create maze and draw it
    maze = create_maze(ax, self.nx, self.ny, self.maze_number, self.pond_location)
    maze.draw()

    # Add axes ticks
    plt.xticks(range(self.nx), fontsize=15)
    plt.yticks(range(self.ny), fontsize=15)


  def check_stayed_on_maze_path(self, which_turtle=0):
    '''
    Check whether turtle stayed on maze path

    Parameters
    --------
    which_turtle : number (such as 1, 2, or 3), which specifies the turtle to check 

    Returns
    --------
    True or False (technically called a Boolean)
      True is returned if the turtle always stayed on the maze path. 
      False is returned if the turtle stepped off the path at some point

    Example
    -------
    turtle.check_stayed_on_maze_path()
    '''
    
    # Check that some turtles have been initialized
    if (self.turtles == []) or (self.turtles == None):
      print("You don't have any turtles yet!\n Try doing calling turtle.start_new_journey(), followed by some movements like\n turtle.move_up()")
      return
    
    if self.maze_number == False:
      print("You did not give a maze number when creating this turtle, so you can't check whether the turtle stayed on maze path.")
      return None
    
    # Note, we don't plot the maze, so we pass in None for the ax
    maze = create_maze(None, self.nx, self.ny, self.maze_number, self.pond_location)
    
    movements, trail = self.turtles[which_turtle].get_movements_and_trail()
    return maze.check_path_stays_on_maze(movements)
    
  def check_reached_maze_goal(self, which_turtle=0):
    '''
    Check whether turtle reaches the maze goal, for instance, reaches the pond or food

    Parameters
    --------
    which_turtle : number (such as 1, 2, or 3), which specifies the turtle to check 

    Returns
    --------
    True or False (technically called a Boolean)
      True is returned if the turtle reaches the maze goal, for instance, reaches the pond or food
      False is returned if the turtle never reaches the goal 

    Example
    -------
    turtle.check_reached_maze_goal()
    '''
    
    # Check that some turtles have been initialized
    if (self.turtles == []) or (self.turtles == None):
      print("You don't have any turtles yet!\n Try doing calling turtle.start_new_journey(), followed by some movements like\n turtle.move_up()")
      return
    
    if self.maze_number == False:
      print("You did not give a maze number when creating this turtle, so you can't check whether the turtle reached the maze goal.")
      return None
    
    # Note, we don't plot the maze, so we pass in None for the ax
    maze = create_maze(None, self.nx, self.ny, self.maze_number, self.pond_location)
    
    movements, trail = self.turtles[which_turtle].get_movements_and_trail()
    return maze.check_path_includes_goal(movements)  

  def check_continuous_movements(self, which_turtle=0):
    '''
    Check whether turtle's movements are all continuous, i.e., the movements 
    don't skip or jump over squares (which would not be fair)
    

    Parameters
    --------
    which_turtle : number (such as 1, 2, or 3), which specifies the turtle to check 

    Returns
    --------
    True or False (technically called a Boolean)
      True is returned if the turtle's movements are all continuous and don't skip any squares 
      False is returned if some square(s) are skipped over

    Example
    -------
    turtle.check_continuous_movements()
    '''
    
    # Check that some turtles have been initialized
    if (self.turtles == []) or (self.turtles == None):
      print("You don't have any turtles yet!\n Try doing calling turtle.start_new_journey(), followed by some movements like\n turtle.move_up()")
      return
    
    return self.turtles[which_turtle].check_continuous_movements()

  def check_maze_completed(self, which_turtle=0):
    '''
    Check whether turtle completed the maze

    Parameters
    --------
    which_turtle : number (such as 1, 2, or 3), which specifies the turtle to check 

    Returns
    --------
    True or False (technically called a Boolean)
      True is returned if the turtle successfully completes the maze by doing the following:
       - Stay inside maze path
       - Uses continuous movements from start to finish (no skipping squares or cheating)
       - Reaches the maze goal
    
      False is returned if the turtle fails either of the above conditions

    Example
    -------
    turtle.check_maze_completed()
    '''
    
    # Check that some turtles have been initialized
    if (self.turtles == []) or (self.turtles == None):
      print("You don't have any turtles yet!\n Try doing calling turtle.start_new_journey(), followed by some movements like\n turtle.move_up()")
      return
    
    if self.maze_number == False:
      print("You did not give a maze number when creating this turtle, so you can't check whether the turtle finished the maze.")
      return None
    
    if self.check_continuous_movements(which_turtle):
      if self.check_reached_maze_goal(which_turtle):
        if self.check_stayed_on_maze_path(which_turtle):
          return True
        else:
          print("Turtle did not stay on maze path")
      else:
        print("Turtle did not reach maze goal")
    else:
      print("Turtle did not use continuous movement, that is, some squares were skipped over")
    
    return False
    

  def check_maze_completed_with_shortest_path(self, which_turtle=0):
    '''
    Check whether turtle completed the maze using the shortest path and a starting position of (0,0)

    Parameters
    --------
    which_turtle : number (such as 1, 2, or 3), which specifies the turtle to check 

    Returns
    --------
    True or False (technically called a Boolean)
      True is returned if the turtle successfully completes the maze by doing the following:
        - Uses continuous movements from start to finish (no skipping squares or cheating)
        - Reaches the maze goal
        - Starts at position (0,0)
        - Uses the shortest path from (0,0) to the maze goal
      
      False is returned if the turtle fails any of the above conditions

    Example
    -------
    turtle.check_maze_completed_with_shortest_path()
    '''
    
    # Check that some turtles have been initialized
    if (self.turtles == []) or (self.turtles == None):
      print("You don't have any turtles yet!\n Try doing calling turtle.start_new_journey(), followed by some movements like\n turtle.move_up()")
      return
    
    if self.maze_number == False:
      print("You did not give a maze number when creating this turtle, so you can't check whether the turtle finished the maze.")
      return None    
    
    if self.check_maze_completed(which_turtle):
      if not self.do_turtles_collide():
        movements, trail = self.turtles[which_turtle].get_movements_and_trail()
        
        if movements[0] == (0,0):
          # Note, we don't plot the maze, so we pass in None for the ax
          maze = create_maze(None, self.nx, self.ny, self.maze_number, self.pond_location)
          if len(movements) == maze.get_shortest_path_length():
            return True
          else:
            print("Did not use shortest path.  Your path was length " + str(len(movements)) + ". The shortest path was " + str(maze.get_shortest_path_length()))
        else:
          print("Starting position was incorrect.  Should use (0,0), you instead used " + str(movements[0]) )
      
      else:
        # turtles collide prints error message
        pass

    return False

  def plot_trail(self, ax, t, which_turtle=0):
    '''
    Plot the turtle's trail at all the locations specified by a move_* command

    Parameters
    ----------
    ax : graphical/plotting axes, generated with
        fig, ax = plt.subplots()

    t : number, indicating the number of total movements where we plot a trail

    which_turtle : number (such as 1, 2, or 3), which specifies the turtle to plot

    Returns
    -------
    Plot corresponding to ax has turtle trail plotted

    '''
    if type(t) != int:
      print("Must request integer number of movements when plotting a trail")
      return None
    

    colors = [(0.4, 0.804, 0.6666), (0.804, 0.2, 0.2), (0.271, 0.545, 0), (0.604, 0.196, 0.804)]
    color = colors[which_turtle]

    # retrieve this turtle's list of movements
    movements, leave_trail = self.turtles[which_turtle].get_movements_and_trail()

    if t > len(movements) or t > len(leave_trail):
      print("You have requested too many movements to plot a trail for.  You only have " + str(len(movements)) + " stored movements")

    for i in range(t):
      if leave_trail[i]:
        move = movements[i]
        x_loc = move[0]
        y_loc = move[1]
        ax.fill_between([x_loc-0.5, x_loc+0.5], [y_loc-0.5, y_loc-0.5], [y_loc+0.5, y_loc+0.5], color=color)

  def is_pond_above(self, which_turtle=0):
    '''
    Return True or False, whether the pond is above the current turtle location

    Parameters
    ----------
    which_turtle : number (such as 1, 2, or 3), which specifies the turtle to check about the pond location

    Returns
    -------
    True or False (technically called a Boolean)
      True is returned if the pond is above you
      False is returned if the pond is not above you
    '''
    
    # Check that some turtles have been initialized
    if (self.turtles == []) or (self.turtles == None):
      print("You don't have any turtles yet!\n Try doing calling turtle.start_new_journey(), followed by some movements like\n turtle.move_up()")
      return
    
    # Check that the pond location is set
    if self.pond_location == False or self.pond_location == None:
      print("You didn't specify a pond location when creating the turtle.  So, I can't answer this question about the pond.") 
      return

    current_loc = self.turtles[which_turtle].current_location()
    pond_loc = self.pond_location

    if current_loc[1] < pond_loc[1]:
      return True
    else:
      return False
  
  def is_pond_below(self, which_turtle=0):
    '''
    Return True or False, whether the pond is below the current turtle location

    Parameters
    ----------
    which_turtle : number (such as 1, 2, or 3), which specifies the turtle to check about the pond location

    Returns
    -------
    True or False (technically called a Boolean)
      True is returned if the pond is below you
      False is returned if the pond is not below you
    '''
    
    # Check that some turtles have been initialized
    if (self.turtles == []) or (self.turtles == None):
      print("You don't have any turtles yet!\n Try doing calling turtle.start_new_journey(), followed by some movements like\n turtle.move_up()")
      return
    
    # Check that the pond location is set
    if self.pond_location == False or self.pond_location == None:
      print("You didn't specify a pond location when creating the turtle.  So, I can't answer this question about the pond.") 
      return

    current_loc = self.turtles[which_turtle].current_location()
    pond_loc = self.pond_location

    if current_loc[1] > pond_loc[1]:
      return True
    else:
      return False

  def is_pond_to_right(self, which_turtle=0):
    '''
    Return True or False, whether the pond is to the right of the current turtle location

    Parameters
    ----------
    which_turtle : number (such as 1, 2, or 3), which specifies the turtle to check about the pond location

    Returns
    -------
    True or False (technically called a Boolean)
      True is returned if the pond is to the right of you
      False is returned if the pond is not to the right of you
    '''
    
    # Check that some turtles have been initialized
    if (self.turtles == []) or (self.turtles == None):
      print("You don't have any turtles yet!\n Try doing calling turtle.start_new_journey(), followed by some movements like\n turtle.move_up()")
      return
    
    # Check that the pond location is set
    if self.pond_location == False or self.pond_location == None:
      print("You didn't specify a pond location when creating the turtle.  So, I can't answer this question about the pond.") 
      return

    current_loc = self.turtles[which_turtle].current_location()
    pond_loc = self.pond_location

    if current_loc[0] < pond_loc[0]:
      return True
    else:
      return False

  def is_pond_to_left(self, which_turtle=0):
    '''
    Return True or False, whether the pond is to the left of the current turtle location

    Parameters
    ----------
    which_turtle : number (such as 1, 2, or 3), which specifies the turtle to check about the pond location

    Returns
    -------
    True or False (technically called a Boolean)
      True is returned if the pond is to the left of you
      False is returned if the pond is not to the left of you
    '''
    
    # Check that some turtles have been initialized
    if (self.turtles == []) or (self.turtles == None):
      print("You don't have any turtles yet!\n Try doing calling turtle.start_new_journey(), followed by some movements like\n turtle.move_up()")
      return
    
    # Check that the pond location is set
    if self.pond_location == False or self.pond_location == None:
      print("You didn't specify a pond location when creating the turtle.  So, I can't answer this question about the pond.") 
      return

    current_loc = self.turtles[which_turtle].current_location()
    pond_loc = self.pond_location

    if current_loc[0] > pond_loc[0]:
      return True
    else:
      return False

  def is_path_below(self, which_turtle=0):
    '''
    Return True or False, whether the maze path leads below from the current turtle location.
    Note that the maze path can be open in multiple directions

    Parameters
    ----------
    which_turtle : number (such as 1, 2, or 3), which specifies the turtle to check about the path location

    Returns
    -------
    True or False (technically called a Boolean)
      True is returned if the maze path leads below from the current turtle location
      False is returned if the maze path does not below above from the current turtle location
    '''
    
    # Check that some turtles have been initialized
    if (self.turtles == []) or (self.turtles == None):
      print("You don't have any turtles yet!\n Try doing calling turtle.start_new_journey(), followed by some movements like\n turtle.move_up()")
      return
    
    # Check that a maze has been chosen
    if self.maze_number == False:
      print("You did not give a maze number when creating this turtle, so you can't ask questions about how to follow a maze path.")

    # Get current location and current maze
    current_loc = self.turtles[which_turtle].current_location()
    # Note, we don't plot the maze, so we pass in None for the ax
    maze = create_maze(None, self.nx, self.ny, self.maze_number, self.pond_location)

    open_directions = maze.find_open_directions(current_loc)
    
    if open_directions == False:
      print("Your turtle has left the maze path, so you can't ask questions about how to follow the maze path")
      return None

    for direction in open_directions:
      # 'b' stands for below (bottom)
      if direction == 'b':
        return True
    
    return False


  def is_path_above(self, which_turtle=0):
    '''
    Return True or False, whether the maze path leads above from the current turtle location.
    Note that the maze path can be open in multiple directions

    Parameters
    ----------
    which_turtle : number (such as 1, 2, or 3), which specifies the turtle to check about the path location

    Returns
    -------
    True or False (technically called a Boolean)
      True is returned if the maze path leads above from the current turtle location
      False is returned if the maze path does not lead above from the current turtle location
    '''
    
    # Check that some turtles have been initialized
    if (self.turtles == []) or (self.turtles == None):
      print("You don't have any turtles yet!\n Try doing calling turtle.start_new_journey(), followed by some movements like\n turtle.move_up()")
      return
    
    # Check that a maze has been chosen
    if self.maze_number == False:
      print("You did not give a maze number when creating this turtle, so you can't ask questions about how to follow a maze path.")

    # Get current location and current maze
    current_loc = self.turtles[which_turtle].current_location()
    # Note, we don't plot the maze, so we pass in None for the ax
    maze = create_maze(None, self.nx, self.ny, self.maze_number, self.pond_location)

    open_directions = maze.find_open_directions(current_loc)
    
    if open_directions == False:
      print("Your turtle has left the maze path, so you can't ask questions about how to follow the maze path")
      return None

    for direction in open_directions:
      # 't' stands for open above (top)
      if direction == 't':
        return True
    
    return False


  def is_path_to_right(self, which_turtle=0):
    '''
    Return True or False, whether the maze path leads to the right of the current turtle location.
    Note that the maze path can be open in multiple directions

    Parameters
    ----------
    which_turtle : number (such as 1, 2, or 3), which specifies the turtle to check about the path location

    Returns
    -------
    True or False (technically called a Boolean)
      True is returned if the maze path leads to the right of the current turtle location.
      False is returned if the maze path does not lead to the right of the current turtle location.
    '''
    
    # Check that some turtles have been initialized
    if (self.turtles == []) or (self.turtles == None):
      print("You don't have any turtles yet!\n Try doing calling turtle.start_new_journey(), followed by some movements like\n turtle.move_up()")
      return
    
    # Check that a maze has been chosen
    if self.maze_number == False:
      print("You did not give a maze number when creating this turtle, so you can't ask questions about how to follow a maze path.")

    # Get current location and current maze
    current_loc = self.turtles[which_turtle].current_location()
    # Note, we don't plot the maze, so we pass in None for the ax
    maze = create_maze(None, self.nx, self.ny, self.maze_number, self.pond_location)

    open_directions = maze.find_open_directions(current_loc)
    
    if open_directions == False:
      print("Your turtle has left the maze path, so you can't ask questions about how to follow the maze path")
      return None

    for direction in open_directions:
      # 'r' stands for right
      if direction == 'r':
        return True
    
    return False


  def is_path_to_left(self, which_turtle=0):
    '''
    Return True or False, whether the maze path leads to the left of the current turtle location.
    Note that the maze path can be open in multiple directions

    Parameters
    ----------
    which_turtle : number (such as 1, 2, or 3), which specifies the turtle to check about the path location

    Returns
    -------
    True or False (technically called a Boolean)
      True is returned if the maze path leads to the left of the current turtle location.
      False is returned if the maze path does not lead to the left of the current turtle location.
    '''
    
    # Check that some turtles have been initialized
    if (self.turtles == []) or (self.turtles == None):
      print("You don't have any turtles yet!\n Try doing calling turtle.start_new_journey(), followed by some movements like\n turtle.move_up()")
      return
    
    # Check that a maze has been chosen
    if self.maze_number == False:
      print("You did not give a maze number when creating this turtle, so you can't ask questions about how to follow a maze path.")

    # Get current location and current maze
    current_loc = self.turtles[which_turtle].current_location()
    # Note, we don't plot the maze, so we pass in None for the ax
    maze = create_maze(None, self.nx, self.ny, self.maze_number, self.pond_location)

    open_directions = maze.find_open_directions(current_loc)
    
    if open_directions == False:
      print("Your turtle has left the maze path, so you can't ask questions about how to follow the maze path")
      return None

    for direction in open_directions:
      # 'l' stands for left
      if direction == 'l':
        return True
    
    return False

  
  def do_turtles_collide(self):
    '''
    Check if any of the turtles collide, that is, occupy the same square at the
    same time.  The one exception, is that the turtles are allowed to all start
    on the same square

    Parameters
    --------
    None

    Returns
    --------
    True or False (technically called a Boolean)
      True is returned if no turtles ever collide (occupy the same square at the same time)
      False is returned if two turtles collide, at some point

    '''

    # Check that some turtles have been initialized
    if (self.turtles == []) or (self.turtles == None):
      print("You don't have any turtles yet!\n Try doing calling turtle.start_new_journey(), followed by some movements like\n turtle.move_up()")
      return

    # Strategy: Replay all the turtle moves, checking to see if two turtles are ever in the same location

    # use this to track the current location of each turtle during the animation
    current_location = [ self.turtles[k].movements[0] for k in range(self.number_of_turtles) ]

    # use this to track the current move of each turtle during the animation
    current_moves = [ 0 for k in range(self.number_of_turtles) ]

    # note, we don't plot the maze, so we pass in None for the ax
    maze = create_maze(None, self.nx, self.ny, self.maze_number, self.pond_location)
    # grab goal location (collisions there are OK)
    maze_goal = maze.maze_goal

    # loop over all moves
    for t in range( len(self.turtle_tape)):
      
      # decide which turtle is moving next, and increment it's move counter
      next_turtle = self.turtle_tape[t]
      current_moves[next_turtle] = current_moves[next_turtle] + 1
      # get new location for this turtle
      next_turtle_new_location = self.turtles[next_turtle].movements[ current_moves[next_turtle] ]
      current_location[next_turtle] = next_turtle_new_location
      
      # check that no turtle is at the same location
      for i in range(self.number_of_turtles):
        if (i != next_turtle):
          turtle_i_loc = current_location[i]
          if (turtle_i_loc == next_turtle_new_location) and (turtle_i_loc != maze_goal):
            print("Turtle " + str(i) + " and turtle " + str(next_turtle) + " are at the same location, " + \
                  str(turtle_i_loc) + ", which happens after move " + str(t) + "\n  (note we start counting moves at 0)" )
            return False
    
    return True

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
    If you have one turtle and it's list of movements is [(2,2), (3,3)]
    Then the animation will be a turtle that goes from square (2,2) to
    square (3,3) on the grid
    '''
    import matplotlib.pyplot as plt
    import numpy as np
    from matplotlib.offsetbox import OffsetImage, AnnotationBbox
    import matplotlib.animation

    # Check that some turtles have been initialized
    if (self.turtles == []) or (self.turtles == None):
      print("You don't have any turtles yet!\n Try doing calling turtle.start_new_journey(), followed by some movements like\n turtle.move_up()")
      return

    # Create our blank plot
    fig, ax = plt.subplots()

    # Download turtle image for plotting, and then load that image into Python
    self.download_turtle_image()
    
    # Shrink turtle if more than one
    zoom = self.turtle_scaling * (1.0 / (1.0 + (self.number_of_turtles-1)*0.2))
    image = OffsetImage(plt.imread('./turtle.png', format="png"), zoom=zoom)
    image_left = OffsetImage(plt.imread('./turtle_left.png', format="png"), zoom=zoom)
    image_right = OffsetImage(plt.imread('./turtle_right.png', format="png"), zoom=zoom)

    # Use this to track the current move of each turtle during the animation
    current_moves = [ 0 for k in range(self.number_of_turtles) ]

    # Define helper function for animation, which draws each animation frame
    def animate(t):
      plt.cla()
      
      # decide which turtle is moving next (skip t == 0, as we want to plot the starting position)
      if t > 0:
        # note we use (t-1) because we animate the first frame differently
        next_turtle = self.turtle_tape[int((t-1)/3)]
        if ((t-1)%3) == 0:
          # increment this turtle's move counter
          current_moves[next_turtle] = current_moves[next_turtle] + 1
      else:
        next_turtle = -1 # do nothing for initial frame
      
      # Plot each individual turtle
      for k in range(self.number_of_turtles):
        if k == next_turtle:
          # We plot intermediate frames for the turtle moving
          old_loc = self.turtles[k].movements[ current_moves[k]-1 ]
          current_loc = self.turtles[k].movements[ current_moves[k] ]
          scale = (((t-1)%3)+1)/3.0
          interp_loc = ((1-scale)*old_loc[0] + scale*current_loc[0], (1-scale)*old_loc[1] + scale*current_loc[1])
          plot_loc = ( interp_loc[0] + self.plotting_offsets[k][0], interp_loc[1] + self.plotting_offsets[k][1])
          if (t%3) == 0:
            ab = AnnotationBbox(image, plot_loc, frameon=False)
          elif (t%3) == 1:
            ab = AnnotationBbox(image_left, plot_loc, frameon=False)
          elif (t%3) == 2:
            ab = AnnotationBbox(image_right, plot_loc, frameon=False)
          ax.add_artist(ab)

        else:
          # Normal turtle plot
          current_loc = self.turtles[k].movements[ current_moves[k] ]
          plot_loc = ( current_loc[0] + self.plotting_offsets[k][0], current_loc[1] + self.plotting_offsets[k][1])
          ab = AnnotationBbox(image, plot_loc, frameon=False)
          ax.add_artist(ab)
      
      for k in range(self.number_of_turtles):
        # plot trail up to and including the last move by this turtle
        self.plot_trail(ax, current_moves[k]+1, which_turtle=k)

      # Create maze and draw it
      maze = create_maze(ax, self.nx, self.ny, self.maze_number, self.pond_location)
      maze.draw()

      # Add axes ticks
      plt.xticks(range(self.nx), fontsize=15)
      plt.yticks(range(self.ny), fontsize=15)

    #ax.axis('equal')

    # Note that we plot one extra frame len(self.turtle_tape)+1, so that we can show the starting position
    anim = matplotlib.animation.FuncAnimation(fig, animate, frames=3*len(self.turtle_tape)+1, interval=140, repeat=False)

    return anim

