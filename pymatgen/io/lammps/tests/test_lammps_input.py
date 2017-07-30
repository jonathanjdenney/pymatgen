# coding: utf-8
# Copyright (c) Pymatgen Development Team.
# Distributed under the terms of the MIT License.

from __future__ import division, print_function, unicode_literals, \
    absolute_import

import os
import unittest

from pymatgen.io.lammps.input import LammpsInput

__author__ = 'Kiran Mathew'
__email__ = 'kmathew@lbl.gov'

test_dir = os.path.join(os.path.dirname(__file__), "..", "..", "..", "..",
                        "test_files", "lammps")


class TestLammpsInput(unittest.TestCase):

    def setUp(self):
        self.template_file = os.path.join(test_dir, "in.peptide.template")
        self.settings = {
            "pair_style": "lj/charmm/coul/long 8.0 10.0 10.0",
            "kspace_style": "pppm 0.0001",
            "fix_1": "1 all nvt temp 275.0 275.0 100.0 tchain 1",
            "fix_2": "2 all shake 0.0001 10 100 b 4 6 8 10 12 14 18 a 31"
        }
        self.lammps_input = LammpsInput.from_file(self.template_file, self.settings)

    def test_as_dict(self):
        d = self.lammps_input.as_dict()
        d_test = {}
        with open(os.path.join(test_dir, "in.peptide.template.with_read_data"), "r") as f:
            d_test["template_string"] = f.read()
        d_test["data_file"] = "data.peptide"
        d_test.update(self.settings)
        self.assertDictEqual(d, d_test)

    def test_direct_setting_vs_from_file(self):
        with open(os.path.join(test_dir, "in.peptide.template"), "r") as f:
            template_string = f.read()
        lammps_input = LammpsInput(template_string, **self.settings)
        self.assertDictEqual(lammps_input.as_dict(), self.lammps_input.as_dict())

    def test_read_data_placeholder(self):
        self.assertIn("data_file", self.lammps_input)
        self.assertEqual(self.lammps_input["data_file"], "data.peptide")

    def test_string_representation(self):
        input_file = os.path.join(test_dir, "in.peptide")
        input_file_lines = str(self.lammps_input).split("\n")
        with open(input_file) as f:
            for l1, l2 in zip(input_file_lines, f.readlines()):
                self.assertEqual(l1.strip(), l2.strip())

if __name__ == "__main__":
    unittest.main()
