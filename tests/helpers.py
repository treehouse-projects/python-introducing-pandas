import collections
import inspect
import io
import sys
import unittest

from IPython.display import display, Markdown, Javascript
import ipywidgets as widgets


registered_tests = {}

Cell = collections.namedtuple('Cell', 'input output')

def register_test(test_text):

    def wrapped(cls):
        global registered_tests
        registered_tests[test_text] = cls

    return wrapped


def cell_matching(module, test_text):
    # In is a list of notebook cell inputs
    # Out is a dictionary of cell outputs
    matching_indices = []
    for index, value in enumerate(module.In):
        if test_text in value:
            matching_indices.append(index)
    if matching_indices:
        # The last entry is the call to `check`
        return Cell(value, module.Out.get(matching_indices[-2]))
    return None, None


def bound_test_class_for(module, test_text):
    cell = cell_matching(module, test_text)
    test_cls = registered_tests[test_text]

    # "Clone" the test
    class BoundTestClass(test_cls):
        pass

    BoundTestClass.cell = cell
    BoundTestClass.__name__ = test_cls.__name__
    BoundTestClass.__qualname__ = test_cls.__qualname__
    BoundTestClass.__doc__ = "Cell Tests for " + test_text
    return BoundTestClass

def execute_all_cells(b):
      display(Javascript('''IPython.notebook.execute_all_cells();'''))


def check(module_name, test_text):
    module = sys.modules[module_name]
    test_class = bound_test_class_for(module, test_text)
    output_stream = io.StringIO()
    runner = unittest.TextTestRunner(stream=output_stream)
    runner.run(unittest.defaultTestLoader.loadTestsFromTestCase(test_class))
    md = '```\n' + output_stream.getvalue() + '\n```'
    button = widgets.Button(description='Run Tests')
    button.on_click(execute_all_cells)
    display(button)
    display(Markdown(md))
