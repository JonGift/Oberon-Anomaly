import math

class Circle:
    def __init__(self, radius):
        self.measurement = radius
        self.shape_type = 'Circle'
        self.line_type = 'Radius'
    
    def area(self):
        return ((self.measurement * self.measurement) * (math.pi))
        
class Square:
    def __init__(self, side):
        self.measurement = side
        self.shape_type = 'Square'
        self.line_type = 'Side'
        
    def area(self):
            return self.measurement * self.measurement
            
class NiceShapePrinter:
    def __init__(self, shape):
        self.shape = shape
        
    def print_area(self):
        return 'Area from ' + self.shape.shape_type + ' of ' + self.shape.line_type + ' ' + str(self.shape.measurement) + ' is equal to ' + str(self.shape.area()) + '.'
		
test_circle = Circle(3)
test_square = Square(4)
test_dat_circle = NiceShapePrinter(test_circle)
test_dat_square = NiceShapePrinter(test_square)

print(test_dat_circle.print_area())
print(test_dat_square.print_area())
#print(test_dat_circle.shape.area())