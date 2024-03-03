import unittest
import os
import sys
sys.path.append('../')
from Adsorption_v3 import read_input_files, calculate_molecule_orientation, rotate_molecule, translate_molecule

class TestAdsorption(unittest.TestCase):
    def setUp(self):
        # Create temporary files for testing
        with open('test_surface.xyz', 'w') as f:
            f.write("""2
                     surface
                     H 0.0 0.0 0.0
                     O 1.0 1.0 1.0""")
        with open('test_molecule.xyz', 'w') as f:
            f.write("""2
                     molecule
                     H 0.0 0.0 0.0
                     O 1.0 1.0 1.0""")

    def test_read_input_files(self):
        surface, molecule = read_input_files('test_surface.xyz', 'test_molecule.xyz')
        self.assertIsNotNone(surface)
        self.assertIsNotNone(molecule)

    def test_calculate_molecule_orientation(self):
        surface, molecule = read_input_files('test_surface.xyz', 'test_molecule.xyz')
        phi, theta = calculate_molecule_orientation(molecule, 0, 1)
        self.assertAlmostEqual(phi, 45.0)
        self.assertAlmostEqual(theta, 54.735610317245346)

    def test_rotate_molecule(self):
        surface, molecule = read_input_files('test_surface.xyz', 'test_molecule.xyz')
        rotate_molecule(molecule, 45.0, 35.264389682754654)
        # Add assertions to verify rotation

    def test_translate_molecule(self):
        surface, molecule = read_input_files('test_surface.xyz', 'test_molecule.xyz')
        translate_molecule(molecule, surface, 0, 1.0)
        # Add assertions to verify translation

    def tearDown(self):
        # Remove temporary files after testing
        os.remove('test_surface.xyz')
        os.remove('test_molecule.xyz')

if __name__ == '__main__':
    unittest.main()

