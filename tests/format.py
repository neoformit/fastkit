"""Test validation."""

import subprocess
from unittest import TestCase


class TestValidation(TestCase):
    """Test validation functions."""

    def test_strip_header_spaces(self):
        """Test stripping spaces from FASTA headers."""
        args = [
            'python',
            'fastkit/format.py',
            'tests/data/spaces.fas',
        ]
        r = subprocess.run(args, capture_output=True)
        self.assertEqual(r.returncode, 0)
        self.assertIn(
            "contig_16 some bacterial sequence",
            r.stdout.decode('utf-8'),
        )
        args.append('--strip-header-space',)
        r = subprocess.run(args, capture_output=True)
        self.assertEqual(r.returncode, 0)
        self.assertIn(
            "contig_16_some_bacterial_sequence",
            r.stdout.decode('utf-8'),
        )
        self.assertIn(
            "contig_17_another_bacterial_sequence",
            r.stdout.decode('utf-8'),
        )

    def test_uppercase(self):
        """Test convert FASTA sequences to uppercase."""
        args = [
            'python',
            'fastkit/format.py',
            'tests/data/lower.fas',
        ]
        r = subprocess.run(args, capture_output=True)
        self.assertEqual(r.returncode, 0)
        self.assertIn(
            "TGAttggta",
            r.stdout.decode('utf-8'),
        )
        args.append('--uppercase')
        r = subprocess.run(args, capture_output=True)
        self.assertEqual(r.returncode, 0)
        self.assertIn(
            "TGATTGGTA",
            r.stdout.decode('utf-8'),
        )
