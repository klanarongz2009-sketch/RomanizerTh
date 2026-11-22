import unittest

from romanizer_th import CHAR_MAP, romanize


class RomanizerTests(unittest.TestCase):
    def test_supplied_examples(self):
        examples = {
            "วันจันทร์": "wanjantr",
            "สวัสดี": "swasde",
            "อะไรใหม่": "oairihmm",
            "ดีๆ": "dee",
            "สามารถ": "samart",
            "เป็น": "apn",
            "คำ": "kum",
            "ฤดี": "hruede",
        }
        for source, expected in examples.items():
            with self.subTest(source=source):
                self.assertEqual(romanize(source), expected)

    def test_mapping_groups(self):
        self.assertEqual(CHAR_MAP["ก"], "g")
        self.assertEqual(CHAR_MAP["ข"], "k")
        self.assertEqual(CHAR_MAP["ง"], "ng")
        self.assertEqual(CHAR_MAP["ช"], "ch")
        self.assertEqual(CHAR_MAP["ต"], "th")
        self.assertEqual(CHAR_MAP["ณ"], "n")
        self.assertEqual(CHAR_MAP["๕"], "n")
        self.assertEqual(CHAR_MAP["ฤ"], "rue")

    def test_spaces_punctuation_and_unknown_characters_are_preserved(self):
        self.assertEqual(romanize("ก, ข!"), "g, k!")
        self.assertEqual(romanize("Hello 123"), "Hello 123")

    def test_tone_marks_are_ignored(self):
        self.assertEqual(romanize("ก่"), "g")

    def test_rejects_non_string(self):
        with self.assertRaises(TypeError):
            romanize(None)


if __name__ == "__main__":
    unittest.main()
