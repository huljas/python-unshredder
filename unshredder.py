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

# Pixel is a tuple of (R,G,B,A)
print get_pixel(0, 0)

print "B", get_pixel(0,0)[2]

print zip(get_pixel(0,0), get_pixel(0,1))

labels = ("R", "G", "B", "a")

for l, p1, p2 in zip(labels, get_pixel(0,0), get_pixel(0,1)):
    print l, p1, p2

# Print 10 first pixels in column 0
for y in range(10):
    print get_pixel(0, y)

# How to write to the output image
unshredded = Image.new('RGBA', image.size)

# Crop start
x1, y1 = 0, 0
# Crop end
x2, y2 = shred_width, height
# Crop the first shred
source_region = image.crop([x1, y1, x2, y2])
destination_point = (0, 0)
# Paste the shred to the start of the new image
unshredded.paste(source_region, destination_point)

# Output the new image
unshredded.save('unshredded.jpg', 'JPEG')