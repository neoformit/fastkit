"""Test validation."""

import subprocess
from unittest import TestCase


class TestValidation(TestCase):
    """Test validation functions."""

    def setUp(self):
        """Create required data."""
        return

    def test_sequence_count_limit(self):
        """Test maximum FASTA sequence limit."""
        args = [
            'python',
            'fastkit/validate.py',
            'tests/data/spaces.fas',
            '--sequence-count', '1',
        ]
        r = subprocess.run(args, capture_output=True)
        self.assertEqual(r.returncode, 1)
        self.assertIn(
            "ValidationError: A maximum of 1 sequences is permitted",
            r.stderr.decode('utf-8'),
        )
        args = [
            'python',
            'fastkit/validate.py',
            'tests/data/spaces.fas',
            '--sequence-count', '2',
        ]
        r = subprocess.run(args, capture_output=True)
        self.assertEqual(r.returncode, 0)

    def test_iupac_dna(self):
        """Test DNA sequence validation."""
        args = [
            'python',
            'fastkit/validate.py',
            'tests/data/invalid-dna.fas',
            '--dna',
        ]
        r = subprocess.run(args, capture_output=True)
        self.assertEqual(r.returncode, 1)
        self.assertIn(
            "ValidationError: Sequence is not valid DNA",
            r.stderr.decode('utf-8'),
        )
        args = [
            'python',
            'fastkit/validate.py',
            'tests/data/n-dna.fas',
            '--dna',
        ]
        r = subprocess.run(args, capture_output=True)
        self.assertEqual(r.returncode, 0)

    def test_iupac_dna_not_null(self):
        """Test DNA validated against not-null chars."""
        args = [
            'python',
            'fastkit/validate.py',
            'tests/data/n-dna.fas',
            '--dna',
            '--no-unknown',
        ]
        r = subprocess.run(args, capture_output=True)
        self.assertEqual(r.returncode, 1)
        self.assertIn(
            "ValidationError: Unknown DNA residues are not permitted.",
            r.stderr.decode('utf-8'),
        )

    def test_iupac_protein(self):
        """Test protein sequence validation."""
        args = [
            'python',
            'fastkit/validate.py',
            'tests/data/invalid-protein.fas',
            '--protein',
        ]
        r = subprocess.run(args, capture_output=True)
        self.assertEqual(r.returncode, 1)
        self.assertIn(
            "ValidationError: Sequence is not valid protein",
            r.stderr.decode('utf-8'),
        )
        args = [
            'python',
            'fastkit/validate.py',
            'tests/data/n-protein.fas',
            '--protein',
        ]
        r = subprocess.run(args, capture_output=True)
        self.assertEqual(r.returncode, 0)

    def test_iupac_protein_not_null(self):
        """Test protein validated against not-null chars."""
        args = [
            'python',
            'fastkit/validate.py',
            'tests/data/n-protein.fas',
            '--protein',
            '--no-unknown',
        ]
        r = subprocess.run(args, capture_output=True)
        self.assertEqual(r.returncode, 1)
        self.assertIn(
            "ValidationError: Unknown amino acid residues are not permitted.",
            r.stderr.decode('utf-8'),
        )
        args = [
            'python',
            'fastkit/validate.py',
            'tests/data/protein.fas',
            '--protein',
            '--no-unknown',
        ]
        r = subprocess.run(args, capture_output=True)
        self.assertEqual(r.returncode, 0)
