import unittest
from parser import parse_tracert_output

class TestParser(unittest.TestCase):

    def test_parse_valid_output(self):
        output = """\
 1     1 ms     1 ms     1 ms  192.168.1.1
 2     5 ms     6 ms     6 ms  10.0.0.1
 3    10 ms    11 ms    11 ms  8.8.8.8
"""
        result = parse_tracert_output(output)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0]['ip'], '192.168.1.1')
        self.assertEqual(result[1]['rtts'], [5, 6, 6])

    def test_parse_with_missing_ip(self):
        output = """\
 1     *        *        *     Request timed out.
"""
        result = parse_tracert_output(output)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['ip'], '*')
        self.assertEqual(result[0]['rtts'], ['*', '*', '*'])
    def test_parse_empty_output(self):
        output = ""
        result = parse_tracert_output(output)
        self.assertEqual(result, [])

    def test_parse_non_traceroute_lines(self):
        output = """Tracing route to google.com...
over a maximum of 30 hops:"""
        result = parse_tracert_output(output)
        self.assertEqual(result, [])

    def test_parse_mixed_lines(self):
        output = """\
Tracing route to google.com...
 1     *        *        *     Request timed out.
 2     5 ms     6 ms     7 ms  10.0.0.1
"""
        result = parse_tracert_output(output)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['ip'], '*')
        self.assertEqual(result[1]['ip'], '10.0.0.1')
    
    def test_basic_parsing(self):
        output = """
        1    <1 ms    <1 ms    <1 ms  192.168.1.1
        2     5 ms     6 ms     5 ms  10.0.0.1
        3     8 ms     9 ms     7 ms  172.16.0.1
        """
        parsed = parse_tracert_output(output)
        self.assertEqual(len(parsed), 3)
        self.assertEqual(parsed[0]['hop'], 1)
        self.assertEqual(parsed[0]['ip'], "192.168.1.1")
        self.assertEqual(parsed[0]['rtts'], [1, 1, 1])  # <1 ms becomes 1 (stripped to int)

    def test_all_asterisks_line(self):
        output = """
        1     *        *        *     Request timed out.
        2     8 ms     7 ms     9 ms  8.8.8.8
        """
        parsed = parse_tracert_output(output)
        self.assertEqual(len(parsed), 2)
        self.assertEqual(parsed[0]['rtts'], ["*", "*", "*"])
        self.assertEqual(parsed[0]['ip'], "*")

    def test_line_with_bracket_ip(self):
        output = """
        1    1 ms    2 ms    1 ms  example.com [93.184.216.34]
        """
        parsed = parse_tracert_output(output)
        self.assertEqual(parsed[0]['ip'], "93.184.216.34")
        self.assertEqual(parsed[0]['rtts'], [1, 2, 1])

    def test_non_matching_lines_ignored(self):
        output = """
        Tracing route to example.com over a maximum of 30 hops

        1    1 ms    1 ms    1 ms  192.168.1.1
        """
        parsed = parse_tracert_output(output)
        self.assertEqual(len(parsed), 1)
        self.assertEqual(parsed[0]['hop'], 1)

    
if __name__ == '__main__':
    unittest.main()

# Run it using: python -m unittest tests/test_parser.py