Usage
=====

To use the Adsorption script, run it from the command line with the following syntax:

.. code-block:: shell

    python Adsorption.py surface_file.vasp molecule_file.xyz --origine 0 --vertex 1 --adsorb_index 2 --height 3.5

This command performs adsorption of a molecule on a surface. You need to provide the filenames of the surface and molecule files, as well as the indices of the atoms defining the direction of the molecule. Additionally, specify the index of the atom on the surface for adsorption and the desired adsorption height.

