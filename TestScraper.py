import unittest
from scraper import *

class TestIsValid(unittest.TestCase):
    def test_valid_ics_url(self):
        self.assertTrue(is_valid("https://ics.uci.edu/~dillenco/compsci161/readings/"))

    def test_valid_ics_url_subdomain(self):
        self.assertTrue(is_valid("https://algorithms.ics.uci.edu/~dillenco/compsci161/"))

    def test_valid_cs_url(self):
        self.assertTrue(is_valid("https://cs.uci.edu/~dillenco/compsci161/"))

    def test_valid_informatics_url(self):
        self.assertTrue(is_valid("https://informatics.uci.edu/~dillenco/compsci161/"))

    def test_valid_stat_url(self):
        self.assertTrue(is_valid("https://stat.uci.edu/~dillenco/compsci161/"))

    def test_invalid_file_extension(self):
        self.assertFalse(is_valid("https://ics.uci.edu/~dillenco/compsci161/readings/document.pdf"))

    def test_invalid_domain(self):
        self.assertFalse(is_valid("https://unrelateddomain.com/~dillenco/compsci161/readings/"))

    def test_invalid_scheme(self):
        self.assertFalse(is_valid("ftp://ics.uci.edu/~dillenco/compsci161/readings/"))

    def test_invalid_usage_of_allowed_domain_in_query(self):
        self.assertFalse(is_valid("https://example.com/?redirect=https://ics.uci.edu"))


if __name__ == '__main__':
    unittest.main()
