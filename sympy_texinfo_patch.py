# src/sympy_texinfo_patch/extension.py

from __future__ import annotations

from typing import TYPE_CHECKING

from docutils import nodes
from sphinx import addnodes
import logging

if TYPE_CHECKING:
    from sphinx.application import Sphinx

logger = logging.getLogger(__name__)


def _print_tree(node: nodes.Node, indent=0) -> None:
    # Print node info
    node_type = type(node).__name__
    prefix = "  " * indent

    if hasattr(node, 'astext'):
        text = node.astext()[:50]
        if len(node.astext()) > 50:
            text += "..."
        logger.info(f"{prefix}{node_type}: '{text}'")
    else:
        logger.info(f"{prefix}{node_type}")

    # Print children
    if hasattr(node, 'children'):
        for child in node.children:
            _print_tree(child, indent + 1)


def print_doctree(app: Sphinx, doctree: nodes.document) -> None:
    """Inspect each parsed doctree."""
    logger.info("Starting new doctree")
    _print_tree(doctree)


def print_resolved(app: Sphinx, doctree: nodes.document, docname: str) -> None:
    """Inspect the final doctree."""
    logger.info(f"Beginning final doctree pass for '{docname}'")
    _print_tree(doctree)


def remove_texinfo_ref_sections(app: Sphinx, doctree: nodes.document) -> None:
    """Strip out the sections that contain a ref in their title."""
    for xref in list(doctree.findall(addnodes.pending_xref)):
        title: nodes.title = xref.parent
        section: nodes.section = title.parent
        if isinstance(title, nodes.title) and isinstance(section, nodes.section):
            # In any case, this doctree must always get rebuilt
            app.env.note_reread()
            # In the texinfo case, strip out the offending sections.
            if app.builder.format == 'texinfo':
                # TODO: is the compound-toctree *always* at the same level?
                if (toctree := title.next_node(nodes.compound, descend=False,
                                               siblings=True)):
                    section.replace_self(toctree)
                else:
                    section.parent.remove(section)


def remove_texinfo_empty_contents_sections(app: Sphinx, doctree: nodes.document) -> None:
    """Strip out placeholder 'Contents' sections."""
    filter = lambda node: isinstance(node, nodes.title) and node.astext().lower() == 'contents'
    for title in list(doctree.findall(filter)):
        section: nodes.section = title.parent
        if isinstance(section, nodes.section):
            # In any case, this doctree must always get rebuilt
            app.env.note_reread()
            # In the texinfo case, strip out the offending sections.
            if app.builder.format == 'texinfo':
                if (toctree := title.next_node(nodes.compound, descend=False,
                                               siblings=True)):
                    section.replace_self(toctree)
                else:
                    section.parent.remove(section)


def setup(app: Sphinx):
    """Setup function for Sphinx extension."""
    # app.connect('doctree-read', print_doctree)
    # app.connect('doctree-resolved', print_resolved)
    app.connect('doctree-read', remove_texinfo_ref_sections)
    app.connect('doctree-read', remove_texinfo_empty_contents_sections)

    return {
        'version': '0.8',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
