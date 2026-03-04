#synthetic image data sets generation

#import required libraries
import os
import PIL
from PIL import Image
import random
import math
import shapely 
from matplotlib import pyplot
from shapely.geometry import Polygon
from shapely.geometry import Point
from matplotlib.patches import Polygon as MplPolygon
from math import sqrt
from shapely import affinity
import numpy as np

#defining a class for geometric objects, which can contain a shaply object (Point or Polygon), the object's color, its area, its name, its center_point and its rotation
class Geometric_Object: 
	def __init__(self, geom_obj, area, obj_name, center_x, center_y, rotation):
		self.geom_obj = geom_obj
		self.color = '#ffffff'
		self.area = area
		self.obj_name = obj_name
		self.center_x = center_x
		self.center_y = center_y
		self.rotation = rotation
	
	def __str__(self):
		return 'Object Name: ' + self.obj_name + '; center: (' + str(self.center_x) + ', ' + str(self.center_y) + '); area: ' + str(self.area) + '; rotation: ' + str(self.rotation) + '; color: ' + self.color
	
	def get_geom_obj(self):
		return self.geom_obj
	
	def set_geom_obj(self, geom_obj):
		self.geom_obj = geom_obj
	
	def get_color(self):
		return self.color  	

	def set_color(self, color):
		self.color = color
	
	def get_area(self):
		return self.area
	
	def set_rotation(self, rotation):
		self.rotation = rotation
	
	def get_center_x(self):
		return self.center_x
	
	def get_center_y(self):
		return self.center_y
	
	def recalc_center(self):
		obj_bounds = self.geom_obj.bounds #minx, miny, maxx, maxy of the object
		self.center_x = obj_bounds[0] + (self.get_width() / 2)
		self.center_y = obj_bounds[1] + (self.get_height() / 2)
	
	def get_width(self):
		obj_bounds = self.geom_obj.bounds #minx, miny, maxx, maxy of the object
		return obj_bounds[2] - obj_bounds[0]
	
	def get_height(self):
		obj_bounds = self.geom_obj.bounds #minx, miny, maxx, maxy of the object
		return obj_bounds[3] - obj_bounds[1]

#create an equilateral triangle that is centered at position (center_x, center_y) with a given size (in terms of area) and rotation
#input: x coordinate of the triangle's center point
#       y coordinate of the triangle's center point
#       area of the triangle
#       rotation of the triangle
#output: shaply Polygon-object representing the triangle
def create_triangle(center_x, center_y, area, rotation):
	base = math.sqrt(area * 4 / math.sqrt(3))
	height = math.sqrt((base*base) - (base*base/4))
	triangle = Polygon([(center_x-base/2, center_y-height/2), (center_x, center_y+height/2), (center_x+base/2, center_y-height/2)])
	return affinity.rotate(triangle, rotation)

#create a rectangle that is centered at position (center_x, center_y) with a given size (in terms of area) and rotation
#input: x coordinate of the rectangle's center point
#       y coordinate of the rectangle's center point
#       area of the rectangle
#       rotation of the rectangle
#output: shaply Polygon-object representing the rectangle
def create_rectangle(center_x, center_y, area, rotation):
	base = math.sqrt(area)
	rectangle = Polygon([(center_x-base/2, center_y-base/2), (center_x-base/2, center_y+base/2), (center_x+base/2, center_y+base/2), (center_x+base/2, center_y-base/2)])
	return affinity.rotate(rectangle, rotation)
#create a circle that is centered at position (center_x, center_y) with a given size (in terms of area)
#input: x coordinate of the circle's center point
#       y coordinate of the circle's center point
#       area of the circle
#output: shaply Point representing the circle
def create_circle(center_x, center_y, area):
	radius = math.sqrt(area/(2*math.pi))
	circle = Point(center_x, center_y).buffer(radius)
	return circle

#select an object type according to the desired random distribution
#input: list of object names
#output: name of the selected object
def select_object(geometric_objects):
	#if the list of objects to choose from contains two objects each is chosen with probability 1/2
	if(len(geometric_objects) == 2):
		random_number = random.random() #get a random number from [0, 1)
		p_circle = 0.5
		p_triangle = p_circle
		
		if(random_number < p_circle): #is the random number in [0, 0,5)
			return geometric_objects[0]
		if(random_number < p_circle+p_triangle): #is the random number in [0,5, 1)
			return geometric_objects[1]
		print("Error in function \'select_object\'")
		exit()
	
	#if the list of objects to choose from contains three objects circle is chosen with probability 1-0.5^(1/3), triangle and rectangle both are chosen with probability 0.5^(4/3)
	elif(len(geometric_objects) == 3):
		random_number = random.random() #get a random number from [0, 1)
		p_circle = 1 - math.pow(0.5, (1/3))
		p_rectangle = 1/2 * math.pow(0.5, (1/3))
		p_triangle = p_rectangle
		
		if(random_number < p_circle): #is the random number in [0, 1-0.5^(1/3) )
			return geometric_objects[0]
		if(random_number < p_circle+p_rectangle): #is the random number in [1-0.5^(1/3), 1-0.5^(1/3) + 1/2 * 0,5^(1/3) )
			return geometric_objects[1]
		if(random_number < p_circle+p_rectangle+p_triangle): #is the random number in 1-0.5^(1/3) + 1/2 * 0,5^(1/3), 1 )
			return geometric_objects[2]
		print("Error in function \'select_object\'")
		exit()
	
	else:
		print("Error: unexcpected length of \'geometric_objects\'")
		exit()

#create a geometric object, the area is chosen randomly from the interval [60, 80]
#input: list of object names
#output: randomly selected geometric object
def create_object(geometric_objects):
	obj_type = select_object(geometric_objects)
	area = 60 + random.random()*20
	rotation = random.random()*360
	if(obj_type == 'Circle'):
		geom_obj = Geometric_Object(geom_obj = create_circle(0, 0, area), area = area, center_x = 0, center_y = 0, obj_name = obj_type, rotation = 0)
	
	elif(obj_type == 'Rectangle'):
		geom_obj = Geometric_Object(geom_obj = create_rectangle(0, 0, area, rotation), area = area, center_x = 0, center_y = 0, obj_name = obj_type, rotation = rotation)
	
	elif(obj_type == 'Equilateral Triangle'):
		geom_obj = Geometric_Object(geom_obj = create_triangle(0, 0, area, rotation), area = area, center_x = 0, center_y = 0, obj_name = obj_type, rotation = rotation)
		geom_obj.recalc_center()
		geom_obj.set_geom_obj(affinity.translate(geom_obj.get_geom_obj(), xoff=geom_obj.get_center_x()*-1, yoff=geom_obj.get_center_y()*-1, zoff=0.0))
		geom_obj.recalc_center()
	
	return geom_obj

#place an object at a random position in the area [0, 31]x[0, 31] such that the object lays completely within the area
#input: a geometric object 
#output: a repositioned geometric object
def position_object(geom_obj):
	width = geom_obj.get_width()
	height = geom_obj.get_height()
	center_x = (width/2.0) + random.random()*(31.0 - width)
	center_y = (height/2.0) + random.random()*(31.0 - height)
	geom_obj.set_geom_obj(affinity.translate(geom_obj.get_geom_obj(), xoff=center_x-geom_obj.get_center_x(), yoff=center_y-geom_obj.get_center_y(), zoff=0.0))
	geom_obj.recalc_center()
	return geom_obj

#calculate the overlap of objects. Return True if at least two objects overlap more than 1%
#input: list of geometric objects
#       geometric objects to check for overlap
#output: boolean value indicating whether objects overlap
def overlap(geom_obj_list, geom_obj):
	for prev_geom_obj in geom_obj_list:
		a1 = prev_geom_obj.get_area()
		a2 = geom_obj.get_area()
		intersection_obj = prev_geom_obj.get_geom_obj().intersection(geom_obj.get_geom_obj())
		if((intersection_obj.area > 0) and (100/(a1/intersection_obj.area) > 1)):
			return True
		return False

#define limits for images
#input: pyplot subplot
#       min value for x-axis
#       max value for x-axis
#       min value for y-axis
#       max value for y-axis
def set_limits(ax, x0, xN, y0, yN):
	ax.set_xlim(x0, xN)
	ax.set_xticks(range(x0, xN+1))
	ax.set_ylim(y0, yN)
	ax.set_yticks(range(y0, yN+1))
	ax.set_aspect("equal")

#program start 
for k in range(2, 4, 1):

	number_of_objects = k #Iterate over number of objects (valid options: 2 and 3) to be generate per image. The number implies the objects' colors, types and random distribution 
	
	if(number_of_objects == 2): 
		geometric_objects = ['Circle', 'Equilateral Triangle']
		colors = ['#ffffff', '#7f7f7f']
		output_path = "2obj-images/"
	elif(number_of_objects == 3):
		geometric_objects = ['Circle', 'Rectangle', 'Equilateral Triangle']
		colors = ['#ffffff', '#aaaaaa', '#555555']
		output_path = "3obj-images/"
	else:
		print("Error: invalid number of objects selected")
		exit()  
	
	if not os.path.exists(output_path): 
		os.makedirs(output_path)
	if not os.path.exists(output_path + "Class1/"):
		os.makedirs(output_path + "Class1/")
	if not os.path.exists(output_path + "Class2/"):
		os.makedirs(output_path + "Class2/") 
	
	for i in range(2000): #repeat 2000 times to generate 2000 images for training 
		objects = []
		
		colors = np.random.permutation(colors)
		
		#prepare a pyplot plot to draw geometric objects in
		fig = pyplot.figure(1, figsize=(25, 25), dpi=128)
		ax = fig.add_subplot(1, 1, 1)
		ax.axis('off')
		fig.set_facecolor('black')
		set_limits(ax, 0, 31, 0, 31)
		
		#generate geometric objects
		for j in range(number_of_objects): 
			geom_obj = create_object(geometric_objects)
			geom_obj.set_color(colors[j])
			geom_obj = position_object(geom_obj)
			if(j > 0):
				while(overlap(objects, geom_obj)):
					geom_obj = position_object(geom_obj)
			objects.append(geom_obj)
			
			poly = geom_obj.get_geom_obj()
			print("GEOM:", poly) 
			print("TYPE:", type(poly))
            
			#draw geometric object into the plot
			poly = geom_obj.get_geom_obj()
            coords = np.array(poly.exterior.coords)
            patch = MplPolygon(coords, facecolor=geom_obj.get_color(), linewidth=0, alpha=1, zorder=1)
			ax.add_patch(patch)
			
		#determin the image's class
		if(number_of_objects == 2):
			if(objects[0].obj_name == objects[1].obj_name):
				directory = "Class1/"
			else:
				directory = "Class2/"
		else:
			if(objects[0].obj_name == geometric_objects[0] or objects[1].obj_name == geometric_objects[0] or objects[2].obj_name == geometric_objects[0]):
				directory = "Class1/"
			else:
				directory = "Class2/"
			
		#saving the generated image at high resolution
		fig.savefig(output_path + "figure-" + str(i).zfill(4) + ".png",facecolor='black')
		fig.clear()
		
		#resizing the image to 32x32 pixels
		im = Image.open(output_path + "figure-" + str(i).zfill(4) + ".png")
		size=(32,32)
		out = im.resize(size, resample=PIL.Image.NEAREST)
		#save resized image
		out.save(output_path + directory + "figure-small-" + str(i).zfill(4) + ".png")