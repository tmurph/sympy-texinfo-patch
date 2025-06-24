# tests/test_extension.py

import pytest
from sphinx.testing.util import SphinxTestApp


def texi_contents(app: SphinxTestApp) -> str:
    filename = f"{app.config.project.replace(' ', '').lower()}.texi"
    return (app.outdir / filename).read_text()


# because of the way that sphinx hard-codes things, this `testroot`
# param needs to match up with a directory f'test-{testroot}' under the
# `rootdir` directory provided in conftest.py
@pytest.mark.sphinx('texinfo', testroot='basic', copy_test_root=True)
def test_no_duplicate_sections_in_texi_output(app: SphinxTestApp) -> None:
    """Test that duplicate 'Introductory Tutorial' sections are merged."""
    app.build()

    # Read the generated .texi file
    content = texi_contents(app)

    # Count occurrences of "@node Introductory Tutorial"
    node_count = content.count("@node Introductory Tutorial")

    # Should only have one node for "Introductory Tutorial", not two
    assert node_count == 1, f"Expected 1 'Introductory Tutorial' node, found {node_count}"

    # Should not have the <2> suffix that indicates duplication
    assert "@node Introductory Tutorial<2>" not in content


@pytest.mark.sphinx('texinfo', testroot='basic', copy_test_root=True)
def test_preserves_section_content(app):
    """Test that the actual tutorial content is preserved after merging."""
    app.build()

    content = texi_contents(app)

    # The actual tutorial content should be present
    assert "This tutorial aims to give an introduction" in content

    # The intermediate description should be removed or incorporated
    # (not duplicated as a separate section)
    description = "If you are new to SymPy, start here"
    desc_count = content.count(description)
    assert desc_count <= 1, f"Description appears {desc_count} times, should appear at most once"


@pytest.mark.sphinx('texinfo', testroot='basic', copy_test_root=True)
def test_handles_multiple_ref_sections(app):
    """Test handling of multiple :ref: sections with a single hidden toctree."""
    # Add a more complex test document
    (app.srcdir / "reference.rst").write_text("""
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

    (app.srcdir / "basics.rst").write_text("""
.. _basics:

Basics
======

Basic content here.
""")

    (app.srcdir / "advanced.rst").write_text("""
.. _advanced:

Advanced
========

Advanced content here.
""")

    # Add to index
    index_content = (app.srcdir / "index.rst").read_text()
    (app.srcdir / "index.rst").write_text(index_content + "\n   reference")

    app.build()

    content = texi_contents(app)

    # Should have single nodes for Basics and Advanced, not duplicates
    assert content.count("@node Basics") == 1
    assert content.count("@node Advanced") == 1
    assert "@node Basics<2>" not in content
    assert "@node Advanced<2>" not in content
