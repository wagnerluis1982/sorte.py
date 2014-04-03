import sys
import os

from unittest import TestCase

# preparando path do projeto para os testes
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))


class BaseTestCase(TestCase):
    longMessage = True

    # asserts com nomes mais legais
    is_instance = TestCase.assertIsInstance
    eq = TestCase.assertEqual
    not_eq = TestCase.assertNotEqual
    ok = TestCase.assertTrue
