# tests/test_extension.py

import pytest

from sphinx.testing.util import SphinxTestApp


@pytest.fixture
def texi_contents(app: SphinxTestApp) -> str:
    app.build()
    filename = f"{app.config.project.replace(' ', '').lower()}.texi"
    return (app.outdir / filename).read_text()


# because of the way that sphinx hard-codes things, this `testroot`
# param needs to match up with a directory f'test-{testroot}' under the
# `rootdir` directory provided in conftest.py
@pytest.mark.sphinx('texinfo', testroot='basic', copy_test_root=True)
def test_no_duplicate_sections_in_texi_output(texi_contents) -> None:
    """Test that duplicate 'Introductory Tutorial' sections are merged."""

    # Count occurrences of "@node Introductory Tutorial"
    node_count = texi_contents.count("@node Introductory Tutorial")

    # Should only have one node for "Introductory Tutorial", not two
    assert node_count == 1, f"Expected 1 'Introductory Tutorial' node, found {node_count}"

    # Should not have the <2> suffix that indicates duplication
    assert "@node Introductory Tutorial<2>" not in texi_contents


@pytest.mark.sphinx('texinfo', testroot='basic', copy_test_root=True)
def test_preserves_section_content(texi_contents):
    """Test that the actual tutorial content is preserved after merging."""

    # The actual tutorial content should be present
    assert "This tutorial aims to give an introduction" in texi_contents

    # The intermediate description should be removed or incorporated
    # (not duplicated as a separate section)
    description = "If you are new to SymPy, start here"
    desc_count = texi_contents.count(description)
    assert desc_count <= 1, f"Description appears {desc_count} times, should appear at most once"


@pytest.mark.sphinx('texinfo', testroot='multiple', copy_test_root=True)
def test_handles_multiple_ref_sections(texi_contents):
    """Test handling of multiple :ref: sections with a single hidden toctree."""

    # Should have single nodes for Basics and Advanced, not duplicates
    assert texi_contents.count("@node Basics") == 1
    assert texi_contents.count("@node Advanced") == 1
    assert "@node Basics<2>" not in texi_contents
    assert "@node Advanced<2>" not in texi_contents


@pytest.mark.sphinx('texinfo', testroot='empty-contents', copy_test_root=True)
def test_contents_section_with_only_toctree_is_eliminated(texi_contents):
    """Test that a 'Contents' section containing only a toctree is eliminated."""
    # The "Contents" section should not appear as a node
    assert "@node Contents" not in texi_contents

    # The toctree entries should appear directly under the main section
    # Check that "Examples from Westers Article" appears without Contents as parent
    assert "@node Examples from Westers Article" in texi_contents
