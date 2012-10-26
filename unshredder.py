from PIL import Image
from math import sqrt 

# Load our image and unshred it!
image = Image.open('TokyoPanoramaShredded.png')
shred_count = 20
width, height = image.size
shred_width = width / shred_count

data = image.getdata() # This gets pixel data	

# Get single pixel
def get_pixel(x, y):
    pixel = data[y * width + x]
    return pixel

def distance(p1, p2):
	d = 0
	for pp1, pp2 in zip(p1, p2):
		d += (pp1-pp2)**2
	return d

def column_distance(x1, x2):
	dsum = 0
	for y in range(0,height):
		p1 = get_pixel(x1, y)
		p2 = get_pixel(x2, y)
		d = distance(p1, p2)
		dsum += round(sqrt(d))
	return dsum	

shred_starts = range(0,shred_count*shred_width, shred_width)
shred_ends = range(shred_width-1,width, shred_width)

def best_right_side_fit(shred):
	x_end = shred_ends[shred]
	min_value = 9999999999
	best_shred = -1
	for i in range(shred_count):
		if i != shred:
			x_start = shred_starts[i]
			value = column_distance(x_end, x_start)
			if value < min_value:
				min_value = value
				best_shred = i
	return best_shred, min_value		

def best_left_side_fit(shred):
	x_start = shred_starts[shred]
	min_value = 9999999999
	best_shred = -1
	for i in range(shred_count):
		if i != shred:
			x_end = shred_ends[i]
			value = column_distance(x_end, x_start)
			if value < min_value:
				min_value = value
				best_shred = i
	return best_shred, min_value

def find_first_shred():
	left_fits = []
	for i in range(shred_count):
		left_fits.append(best_left_side_fit(i))
	for i in range(shred_count):
		for j in range(shred_count):
			if i != j:
				if left_fits[i][0] == left_fits[j][0]:
					if left_fits[i][1] > left_fits[j][1]:
						return i
					else:
						return j	

print "Picture size: ", width, height

for s, e in zip(shred_starts, shred_ends):
	print "Shred", s, e

for i in range(shred_count):
	print i, "Best left side ", best_left_side_fit(i), " and right side ", best_right_side_fit(i)

print "First shred: ", find_first_shred()

labels = ("R", "G", "B", "a")

for l, p1, p2 in zip(labels, get_pixel(0,0), get_pixel(0,1)):
    print l, p1, p2

# Print 10 first pixels in column 0
for y in range(10):
    print get_pixel(0, y)

# How to write to the output image
unshredded = Image.new('RGBA', image.size)

shred_index = find_first_shred()

for i in range(shred_count):
	# Crop start
	x1, y1 = shred_starts[shred_index], 0
	# Crop end
	x2, y2 = shred_ends[shred_index]+1, height
	# Crop the first shred
	source_region = image.crop([x1, y1, x2, y2])
	destination_point = (i*shred_width, 0)
	# Paste the shred to the start of the new image
	unshredded.paste(source_region, destination_point)

	shred_index, value = best_right_side_fit(shred_index)

# Output the new image
unshredded.save('unshredded.jpg', 'JPEG')