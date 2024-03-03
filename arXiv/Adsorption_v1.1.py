"""
Author: Kazem Zhour
Date: 24.04.2024
Description: Adsorption of molecules on surfaces.

This Python script is about adsorbing molecules on top of any surface with the ability to manupulate the adsoprtion position and the orientationn of the molecule.

"""

from ase.io import write, read
import numpy as np

# Input file names (ASE can read and rite many fiel formats like POSCAR, xyz, cif ..., for more information you can check the ASE website, at this 
#momnet this link "https://wiki.fysik.dtu.dk/ase/ase/io/io.html").

# Import surface file:
surface_file = input("Enter the name of your surface file: ")
# Import molecule file:
molecule_file = input("Enter the name of your molecule file: ")

# Read structures
surface = read(surface_file)
molecule = read(molecule_file)

# Define coordinates for the axis of the molecule
origine = input("Enter the index of the origin of the verctor defining the direction along your molecule (the counting start from 0): ")
# Convert the input to an integer
try:
    a = int(origine)
except ValueError:
    print("Error: Please enter a valid integer.")
vertex = input("Enter the index of the head of the verctor defining the direction along your molecule : ")
try:
    b = int(vertex)
except ValueError:
    print("Error: Please enter a valid integer.")

origin_coords = molecule[a].position
second_atom_coords = molecule[b].position

# Calculate vector
vector = second_atom_coords - origin_coords
# Calculate spherical coordinates
r = np.linalg.norm(vector)
phi = np.arctan2(vector[1], vector[0]) * 180 / np.pi  # Azimuthal angle
theta = np.arccos(vector[2] / r) * 180 / np.pi  # Polar angle

# Shift molecule
molecule.positions -= origin_coords

# Rotate molecule
molecule.rotate(-phi, 'z', center=(0, 0, 0))
molecule.rotate(-theta, 'y', center=(0, 0, 0))  # Adjust rotation direction if needed
# Rotate molecule along z axis
teta = input("Enter the angle for rotating the molecule arround the z axis: ")
try:
    t = float(teta)
except ValueError:
    print("Error: Please enter a valid integer.")
molecule.rotate(-t, 'z', center=(0, 0, 0))

# Define adsorption site coordinates
adsorb = input("Enter the index of the atom of the slab on which you want to adsorb your molecule: ")
try:
    d = int(adsorb)
except ValueError:
    print("Error: Please enter a valid integer.")
height = input("Enter the height at which you want to adsorb your molecule: ")
try:
    h = float(height)
except ValueError:
    print("Error: Please enter a valid integer.")
# adsorb_position = surface[d].position
x_ad = surface[d].x
y_ad = surface[d].y
z_ad = surface[d].z + h

# Translate molecule to adsorption site
molecule.positions += np.array([x_ad, y_ad, z_ad])

# Determine interface bounds
#z_min = surface.positions[:, 2].min()
#z_max = surface.positions[:, 2].max()

# Combine slab and molecule
interface = surface + molecule

# Write output file
write('POSCAR.vasp', interface)
