class Field:
    '''
    A class for configuring field dimensions

    Use meters as measurement unit
    '''
    def __init__(self,
                 length = 9,
                 width = 6,
                 boundary_width = 0.3,
                 penalty_width = 2,
                 penalty_depth = 1,
                 goal_width = 1,
                 goal_depth = 0.18):
        
        self.length = length
        self.width = width
        self.boundary_width = boundary_width
        self.penalty_width = penalty_width
        self.penalty_depth = penalty_depth
        self.goal_width = goal_width
        self.goal_depth = goal_depth
        
        self.set_field_limits(x_min=-length-boundary_width,
                              x_max=length+boundary_width,
                              y_min=-width-boundary_width,
                              y_max=width+boundary_width)

    def set_field_limits(self, x_min, x_max, y_min, y_max):
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max

        return self
