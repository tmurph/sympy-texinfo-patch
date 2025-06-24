# src/sympy_texinfo_patch/extension.py

from sphinx.application import Sphinx
from sphinx.writers.texinfo import TexinfoTranslator
from docutils import nodes
from sphinx import addnodes
import logging

logger = logging.getLogger(__name__)


class PatchedTexinfoTranslator(TexinfoTranslator):
    """Patched TexinfoTranslator that prevents duplicate sections from refs."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._ref_sections = set()  # Track sections created from refs
        self._in_hidden_toctree = False

    def visit_reference(self, node):
        # Check if this reference is followed by section markup
        if 'refid' in node:
            parent = node.parent
            if isinstance(parent, nodes.paragraph):
                # Check if paragraph parent is followed by a transition
                grandparent = parent.parent
                if grandparent:
                    try:
                        idx = grandparent.index(parent)
                        if idx + 1 < len(grandparent):
                            next_node = grandparent[idx + 1]
                            if isinstance(next_node, nodes.transition):
                                # This ref becomes a section
                                self._ref_sections.add(node.astext())
                    except (ValueError, IndexError):
                        pass

        super().visit_reference(node)

    def visit_toctree(self, node):
        if node.get('hidden', False):
            self._in_hidden_toctree = True
        super().visit_toctree(node)

    def depart_toctree(self, node):
        if node.get('hidden', False):
            self._in_hidden_toctree = False
        super().depart_toctree(node)

    def visit_section(self, node):
        # Get section title
        title = ""
        if node.children and isinstance(node.children[0], nodes.title):
            title = node.children[0].astext()

        # If we're in a hidden toctree and this section matches a ref section, skip it
        if self._in_hidden_toctree and title in self._ref_sections:
            raise nodes.SkipNode

        # Check if parent is start_of_file (toctree-included content)
        parent = node.parent
        if isinstance(parent, addnodes.start_of_file):
            # This is content from a toctree inclusion
            # If the title matches a ref section, skip it
            if title in self._ref_sections:
                raise nodes.SkipNode

        super().visit_section(node)


def setup(app: Sphinx):
    """Setup function for Sphinx extension."""
    app.set_translator('texinfo', PatchedTexinfoTranslator, override=True)

    return {
        'version': '0.6',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
