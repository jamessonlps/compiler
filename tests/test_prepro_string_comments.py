import unittest

from preprocess import PrePro


class TestPreProStringComments(unittest.TestCase):
    def test_normal_comments_preserve_spaces_and_lf(self):
        source = 'value = 1 # explanation\n# full comment\n\nprintln(value)\n# end'
        expected = 'value = 1 \n\n\nprintln(value)\n'
        self.assertEqual(PrePro.filter(text=source), expected)

    def test_hashes_inside_string_without_final_newline(self):
        source = 'println("a # b ## c")'
        self.assertEqual(PrePro.filter(text=source), source)

    def test_comments_after_multiple_strings(self):
        source = 'println("#first" . "#second") # discard\nprintln("ok") # discard too\n'
        expected = 'println("#first" . "#second") \nprintln("ok") \n'
        self.assertEqual(PrePro.filter(text=source), expected)

    def test_quotes_in_comments_do_not_change_string_state(self):
        source = '# ignored " quote\nprintln("ok") # ignored " quote\nvalue = 2 # done'
        expected = '\nprintln("ok") \nvalue = 2 '
        self.assertEqual(PrePro.filter(text=source), expected)

    def test_comments_preserve_mixed_lf_and_crlf(self):
        source = 'value = 1 # first\r\n# second\n# third\r\nprintln("ok")\r\n'
        expected = 'value = 1 \r\n\n\r\nprintln("ok")\r\n'
        self.assertEqual(PrePro.filter(text=source), expected)
