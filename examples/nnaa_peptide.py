#!/usr/bin/env python
'''
Example: branched peptide
Input: HELM sequence
SecStr: Predicted with in house protocol
Output: 2D image with local method and PDB structure with 3D coordinates
'''

########################################################################################
# Authorship
########################################################################################

__credits__ = ["Rodrigo Ochoa", "J.B. Brown", "Thomas Fox"]
__license__ = "MIT"
__version__ = "1.0"

########################################################################################
# Modules
########################################################################################

from pyPept.sequence import Sequence
from pyPept.sequence import correct_pdb_atoms
from pyPept.molecule import Molecule
from pyPept.converter import Converter
from pyPept.conformer import Conformer
from pyPept.conformer import SecStructPredictor

# RDKit modules
from rdkit import Chem
from rdkit.Chem import Draw

# Start the Sequence object - convert HELM to BILN
#biln = "N-Iva-F-D-I-meT-N-A-L-W-Y-Aib-K"
helm = "PEPTIDE1{N.[Iva].F.D.I.[meT].N.A.L.W.Y.[Aib].K}$$$$V2.0"
b = Converter(helm=helm)
biln = b.get_biln()

seq = Sequence(biln)
# Correct atom names in the sequence object
seq = correct_pdb_atoms(seq)

# Loop wit the included monomers
mm_list = seq.s_monomers
for i, monomer in enumerate(mm_list):
    mon = monomer['m_romol']

# Generate the RDKit object
mol = Molecule(seq, depiction='local')
romol = mol.get_molecule(fmt='ROMol')
print("The SMILES of the peptide is: {}".format(Chem.MolToSmiles(romol)))
Draw.MolToFile(romol, 'nnaa_peptide.png', size=(1200, 1200))

# Create the peptide conformer with corrected atom names and secondary structure
# Obtain peptide main chain to predict the secondary structure
fasta = Conformer.get_peptide(biln)
secstruct = SecStructPredictor.predict_active_ss(fasta)
# Generate the conformer
romol = Conformer.generate_conformer(romol, secstruct, generate_pdb=True)