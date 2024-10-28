import numpy as np
from pwem.emlib.image import ImageHandler

# read volume
# volume is of type xmipp.Image
volume = ImageHandler().read('mask.mrc')
# volAray is of type np.array
volArray = volume.getData()
# get center of coordinates, aka origin
#self.xmippOrigin = np.array((volArray.shape[0] / 2,
#                             volArray.shape[1] / 2,
#                             volArray.shape[2] / 2))

#compute mask


# save mask?
# there is a setDAta but I do not think we need it
# volume.write('pp.mrc')
# ImageHandler.write(volArray, location)



# Parameters for the cone
size_x = size_y = size_z = volArray.shape[0]  # Dimensions of the 3D grid

radius_bottom = 16                   # Radius at the base (bottom of the truncated cone)
radius_top = 120                        # Radius at the top 
x_min = -30                            # Lower bound for z (start of the truncated cone)
x_max = 90                            # Upper bound for z (end of the truncated cone)
# cap_height = 55                          # Height of the spherical cap

# Create the 3D grid of indices
x = np.arange(-size_x // 2, size_x // 2)
y = np.arange(-size_y // 2, size_y // 2)
z = np.arange(-size_z // 2, size_z // 2)
X, Y, Z = np.meshgrid(x, y, z, indexing='ij')


# Define the truncated cone
radius_x = radius_bottom + (radius_top - radius_bottom) * (X - x_min) / (x_max - x_min)
cone = (Y**2 + Z**2 <= radius_x**2) & (X >= x_min) & (X <= x_max)

# Define the inverted spherical cap
# Place the sphere center at `z_max + radius_top` to ensure it only starts above `z_max`
cap_center_x = x_min # x_max - radius_top + 30
cap = (Y**2 + Z**2 + (X - cap_center_x)**2 <= (radius_top + 50)**2) & (X >= x_max)

# Combine the cone and cap using logical OR
truncated_cone_with_cap = cone | cap
# truncated_cone_with_cap = cap

# Convert boolean array to integers if needed
cone_with_cap_array = truncated_cone_with_cap.astype(float)


# Now cone_array is a 3D array with values 1 inside the cone and 0 outside
volume.setData(cone_with_cap_array)
volume.write('pp9.mrc')
