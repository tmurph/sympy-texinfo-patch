# tests/test_extension.py

import pytest
from docutils import nodes
from sphinx.testing.util import SphinxTestApp
from pathlib import Path
import tempfile
import shutil


@pytest.fixture
def test_app(tmp_path):
    """Create a Sphinx app for testing."""
    src_dir = tmp_path / "source"
    src_dir.mkdir()

    # Copy test docs
    test_docs = Path(__file__).parent / "test_docs" / "source"
    shutil.copytree(test_docs, src_dir, dirs_exist_ok=True)

    app = SphinxTestApp(
        buildername='texinfo',
        srcdir=src_dir,
        builddir=tmp_path / "build"
    )
    yield app
    app.cleanup()


def test_no_duplicate_sections_in_texi_output(test_app):
    """Test that duplicate 'Introductory Tutorial' sections are merged."""
    test_app.build()

    # Read the generated .texi file
    texi_file = test_app.outdir / f"{test_app.config.project.replace(' ', '')}.texi"
    content = texi_file.read_text()

    # Count occurrences of "@node Introductory Tutorial"
    node_count = content.count("@node Introductory Tutorial")

    # Should only have one node for "Introductory Tutorial", not two
    assert node_count == 1, f"Expected 1 'Introductory Tutorial' node, found {node_count}"

    # Should not have the <2> suffix that indicates duplication
    assert "@node Introductory Tutorial<2>" not in content


def test_preserves_section_content(test_app):
    """Test that the actual tutorial content is preserved after merging."""
    test_app.build()

    texi_file = test_app.outdir / f"{test_app.config.project.replace(' ', '')}.texi"
    content = texi_file.read_text()

    # The actual tutorial content should be present
    assert "This tutorial aims to give an introduction" in content

    # The intermediate description should be removed or incorporated
    # (not duplicated as a separate section)
    description = "If you are new to SymPy, start here"
    desc_count = content.count(description)
    assert desc_count <= 1, f"Description appears {desc_count} times, should appear at most once"


def test_handles_multiple_ref_sections(test_app):
    """Test handling of multiple :ref: sections with a single hidden toctree."""
    # Add a more complex test document
    (test_app.srcdir / "reference.rst").write_text("""
.. _reference:

API Reference
=============

Overview of the API.

:ref:`Basics <basics>`
----------------------

Basic functionality.

:ref:`Advanced <advanced>`
--------------------------

Advanced functionality.

.. toctree::
   :hidden:

   basics
   advanced
""")

    (test_app.srcdir / "basics.rst").write_text("""
.. _basics:

Basics
======

Basic content here.
""")

    (test_app.srcdir / "advanced.rst").write_text("""
.. _advanced:

Advanced
========

Advanced content here.
""")

    # Add to index
    index_content = (test_app.srcdir / "index.rst").read_text()
    (test_app.srcdir / "index.rst").write_text(index_content + "\n   reference")

    test_app.build()

    texi_file = test_app.outdir / f"{test_app.config.project.replace(' ', '')}.texi"
    content = texi_file.read_text()

    # Should have single nodes for Basics and Advanced, not duplicates
    assert content.count("@node Basics") == 1
    assert content.count("@node Advanced") == 1
    assert "@node Basics<2>" not in content
    assert "@node Advanced<2>" not in content
