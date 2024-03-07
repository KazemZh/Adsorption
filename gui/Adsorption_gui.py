import tkinter as tk
from tkinter import filedialog
import argparse
import numpy as np
from ase.io import write, read

def read_input_files(surface_file, molecule_file):
    """
    Reads input files for surface and molecule.
    
    Returns:
        surface (ASE Atoms object): The surface structure.
        molecule (ASE Atoms object): The molecule structure.
    """
    try:
        # Read surface and molecule file names
        surface = read(surface_file)
        molecule = read(molecule_file)
    except FileNotFoundError:
        print("Error: File not found.")
        return None, None
    except Exception as e:
        print("Error:", e)
        return None, None
    return surface, molecule

def calculate_molecule_orientation(molecule, origin_index, vertex_index):
    """
    Calculates the orientation of the molecule based on user input.
    
    Args:
        molecule (ASE Atoms object): The molecule structure.
        origin_index (int): Index of the origin atom.
        vertex_index (int): Index of the head atom.
    
    Returns:
        phi (float): Azimuthal angle.
        theta (float): Polar angle.
    """
    try:
        if origin_index < 0 or origin_index >= len(molecule) or vertex_index < 0 or vertex_index >= len(molecule):
            raise ValueError("Invalid atom indices.")
        # Calculate vector along the molecule axis
        origin_coords = molecule[origin_index].position
        second_atom_coords = molecule[vertex_index].position
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
        adsorb_index (int): Index of the atom for adsorption.
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
    root = tk.Tk()
    root.title("Adsorption GUI")

    # Labels
    tk.Label(root, text="Surface File:").grid(row=0, column=0)
    tk.Label(root, text="Molecule File:").grid(row=1, column=0)
    tk.Label(root, text="Origin Index:").grid(row=2, column=0)
    tk.Label(root, text="Vertex Index:").grid(row=3, column=0)
    tk.Label(root, text="Adsorb Index:").grid(row=4, column=0)
    tk.Label(root, text="Height:").grid(row=5, column=0)

    # Input boxes
    surface_entry = tk.Entry(root)
    molecule_entry = tk.Entry(root)
    origin_entry = tk.Entry(root)
    vertex_entry = tk.Entry(root)
    adsorb_entry = tk.Entry(root)
    height_entry = tk.Entry(root)

    surface_entry.grid(row=0, column=1)
    molecule_entry.grid(row=1, column=1)
    origin_entry.grid(row=2, column=1)
    vertex_entry.grid(row=3, column=1)
    adsorb_entry.grid(row=4, column=1)
    height_entry.grid(row=5, column=1)

    def browse_surface():
        surface_file = filedialog.askopenfilename()
        surface_entry.insert(tk.END, surface_file)

    def browse_molecule():
        molecule_file = filedialog.askopenfilename()
        molecule_entry.insert(tk.END, molecule_file)

    # Browse buttons
    surface_button = tk.Button(root, text="Browse", command=browse_surface)
    surface_button.grid(row=0, column=2)
    molecule_button = tk.Button(root, text="Browse", command=browse_molecule)
    molecule_button.grid(row=1, column=2)

    def submit():
        surface_file = surface_entry.get()
        molecule_file = molecule_entry.get()
        origin_index = int(origin_entry.get())
        vertex_index = int(vertex_entry.get())
        adsorb_index = int(adsorb_entry.get())
        height = float(height_entry.get())

        # Read input files
        surface, molecule = read_input_files(surface_file, molecule_file)
        if surface is None or molecule is None:
            return

        # Calculate molecule orientation
        phi, theta = calculate_molecule_orientation(molecule, origin_index, vertex_index)
        if phi is None or theta is None:
            return

        # Rotate molecule 
        rotate_molecule(molecule, phi, theta)

        # Translate molecule to adsorption site
        translate_molecule(molecule, surface, adsorb_index, height)

        # Combine surface and molecule
        interface = surface + molecule

        # Write output file
        write('POSCAR.vasp', interface)
        print("Adsorption completed! Output written to 'POSCAR.vasp'.")

    # Submit button
    submit_button = tk.Button(root, text="Submit", command=submit)
    submit_button.grid(row=6, columnspan=2)

    root.mainloop()

if __name__ == "__main__":
    main()

