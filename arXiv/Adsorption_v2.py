"""
Author: Kazem Zhour

Date: 26.04.2024

Description: Adsorption of molecules on surfaces.
	This Python script facilitates the adsorption of molecules onto surfaces, offering the flexibility to
	manipulate both the adsorption position and the orientation of the molecule.

Usage: This script requires input files for the surface and the molecule. The user will be prompted 
	to enter the filenames for these input files. Additionally, the script prompts the user to 
	specify the origin and head atoms for defining the direction along the molecule, the angle 
	for rotating the molecule around the z-axis, the atom of the slab on which to adsorb the 
	molecule, and the desired adsorption height.

Dependencies: This script requires the Atomic Simulation Environment (ASE) library for reading and 
	writing structure files. ASE can handle various file formats such as POSCAR, xyz, and cif.

Example:
    $ python adsorption.py

    Enter the name of your surface file: surface.xyz
    Enter the name of your molecule file: molecule.xyz
    Enter the index of the origin atom of the molecule: 0
    Enter the index of the head atom of the molecule: 1
    Enter the index of the atom of the slab for adsorption: 10
    Enter the height at which you want to adsorb your molecule: 2.5
    
    This example demonstrates how to use the script to perform adsorption of a molecule on a surface. 
    The user is prompted to input the filenames of the surface and molecule files, as well as the indices 
    of the atoms defining the direction of the molecule. Then, the user specifies the index of the atom on 
    the surface for adsorption and the desired adsorption height. The script generates an output containing 
    the combined structure of the surface and the adsorbed molecule.
"""
import numpy as np
from ase.io import write, read

def read_input_files():
    """
    Reads input files for surface and molecule.
    
    Returns:
        surface (ASE Atoms object): The surface structure.
        molecule (ASE Atoms object): The molecule structure.
    """
    print("Please enter the filenames of the surface and molecule structures.")
    try:
    	# Input and read surface and molecule file names
        surface_file = input("Enter the name of your surface file: ")
        surface = read(surface_file)
        molecule_file = input("Enter the name of your molecule file: ")
        molecule = read(molecule_file)
    except FileNotFoundError:
        print("Error: File not found.")
        return None, None
    except Exception as e:
        print("Error:", e)
        return None, None
    return surface, molecule
def calculate_molecule_orientation(molecule):
    """
    Calculates the orientation of the molecule based on user input.
    
    Args:
        molecule (ASE Atoms object): The molecule structure.
    
    Returns:
        phi (float): Azimuthal angle.
        theta (float): Polar angle.
    """
    print("\nPlease enter the indices of the atoms defining the orientation of the molecule.")

    try:
    	# Prompt user to input indices of origin and head atoms
        origine = int(input("Enter the index of the origin atom of the molecule: "))
        vertex = int(input("Enter the index of the head atom of the molecule: "))
        if origine < 0 or origine >= len(molecule) or vertex < 0 or vertex >= len(molecule):
            raise ValueError("Invalid atom indices.")
        # Calculate vector along the molecule axis
        origin_coords = molecule[origine].position
        second_atom_coords = molecule[vertex].position
        vector = second_atom_coords - origin_coords
        # Calculate spherical coordinates
        r = np.linalg.norm(vector)
        phi = np.arctan2(vector[1], vector[0]) * 180 / np.pi
        theta = np.arccos(vector[2] / r) * 180 / np.pi
    except ValueError as e:
        print("Error:", e)
        return None, None
    except Exception as e:
        print("Error:", e)
        return None, None
    return phi, theta

def rotate_molecule(molecule, phi, theta):
    """
    Rotates the molecule to align with the calculated orientation.
    
    Args:
        molecule (ASE Atoms object): The molecule structure.
        phi (float): Azimuthal angle.
        theta (float): Polar angle.
    """
    try:
        if len(molecule) < 2:
            raise ValueError("Molecule must have at least two atoms for rotation.")
        # Shift molecule to the origin
        molecule.positions -= molecule.positions[0]
        # Rotate molecule around z and y axes
        molecule.rotate(-phi, 'z', center=(0, 0, 0))
        molecule.rotate(-theta, 'y', center=(0, 0, 0))
    except ValueError as e:
        print("Error:", e)

def translate_molecule(molecule, surface, adsorb_index, height):
    """
    Translates the molecule to the adsorption site on the surface.
    
    Args:
        molecule (ASE Atoms object): The molecule structure.
        surface (ASE Atoms object): The surface structure.
        adsorb_index (int): Index of the adsorption site atom in the surface.
        height (float): Height of adsorption.
    """
    try:
        if adsorb_index < 0 or adsorb_index >= len(surface):
            raise ValueError("Invalid adsorption site index.")
        # Calculate adsorption site coordinates
        x_ad, y_ad, z_ad = surface[adsorb_index].x, surface[adsorb_index].y, surface[adsorb_index].z + height
        # Translate molecule to adsorption site
        molecule.positions += np.array([x_ad, y_ad, z_ad])
    except ValueError as e:
        print("Error:", e)

def main():
    """
    Main function to perform adsorption of molecules on surfaces.
    """
    print("Welcome to the Molecule Adsorption Tool!")
    # Read input files
    surface, molecule = read_input_files()
    if surface is None or molecule is None:
        return
    # Calculate molecule orientation
    phi, theta = calculate_molecule_orientation(molecule)
    if phi is None or theta is None:
        return
    # Rotate molecule 
    rotate_molecule(molecule, phi, theta)
    # Prompt user to input adsorption site index and height   
    adsorb_index = int(input("Enter the index of the atom of the slab for adsorption: "))
    height = float(input("Enter the height at which you want to adsorb your molecule: "))
    # Translate molecule to adsorption site
    translate_molecule(molecule, surface, adsorb_index, height)
    # Combine surface and molecule
    interface = surface + molecule
    # Write output file
    write('POSCAR.vasp', interface)

if __name__ == "__main__":
    main()
