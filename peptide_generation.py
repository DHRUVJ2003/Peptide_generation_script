"""
/******************************************************************************
  This source file is part of the Avogadro project.
  This source code is released under the New BSD License, (the "License").
******************************************************************************/
"""
import argparse
import json
import sys
# PyPept modules
from pyPept.sequence import Sequence
from pyPept.sequence import correct_pdb_atoms
from pyPept.molecule import Molecule
from pyPept.conformer import Conformer
from pyPept.converter import Converter

debug = True


def getOptions():
    userOptions = {}
    userOptions['Format'] = {
        'label': 'Peptide Format',
        'type': 'stringList',
        'values': ["biln", "helm", "fasta"],
        'default': 'biln'
    }
    userOptions['Sequence'] = {
        'label': 'Peptide Sequence',
        'type': 'string',
        'default': "ac-D-T-H-F-E-I-A-am"
    }

    userOptions['secondary_structure'] = {
        'label': 'Secondary Structure',
        'type': 'stringList',
        'values': ['B', 'H', 'E', 'S', 'T', 'G'],
        'default': 'B',
    }

    opts = {'userOptions': userOptions}

    return opts


def peptide_generation(opts):
    format = opts['Format']
    sequence = opts['Sequence']
    secondary_structure = opts['secondary_structure']

    if format == "helm":
        b = Converter(helm=sequence)
        sequence = b.get_biln()

    if format == "fasta":
        sequence = "-".join(sequence)

    seq = Sequence(sequence)
    seq = correct_pdb_atoms(seq)
    mol = Molecule(seq)
    romol = mol.get_molecule(fmt='ROMol')
    romol = Conformer.generate_conformer(romol, secondary_structure, generate_pdb=True)


def runCommand():
    # Read options from stdin
    stdinStr = sys.stdin.read()
    # Parse the JSON strings
    opts = json.loads(stdinStr)
    peptide_generation(opts)


if __name__ == "__main__":
    parser = argparse.ArgumentParser('Replace atoms of elements')
    parser.add_argument('--debug', action='store_true')
    parser.add_argument('--print-options', action='store_true')
    parser.add_argument('--run-command', action='store_true')
    parser.add_argument('--display-name', action='store_true')
    parser.add_argument('--menu-path', action='store_true')
    parser.add_argument('--lang', nargs='?', default='en')
    args = vars(parser.parse_args())

    debug = args['debug']

    if args['display_name']:
        print("Peptide Generation")
    if args['menu_path']:
        print("&Build")
    if args['print_options']:
        print(json.dumps(getOptions()))
    elif args['run_command']:
        print(json.dumps(runCommand()))
