import unittest
from plate import Plate

class TestPlate(Plate, unittest.TestCase):
    def test_format(self):
        self.assertEqual(self.format_plate('АА 2203 ІК'), 'АА2203ІК')
        self.assertEqual(self.format_plate('аа 2203 аа'), 'АА2203АА')
        self.assertEqual(self.format_plate('- АА2203ІК,'), 'АА2203ІК')
        self.assertEqual(self.format_plate('2203'), '2203')
        self.assertEqual(self.format_plate('К 2203 НН'), 'К2203НН') # old format
        self.assertEqual(self.format_plate('12345 КН'), '12345КН') # another old format
    
    def test_cyr_to_latin(self):
        self.assertEqual(self.cyr_to_latin('ВВ3333КК'), 'BB3333KK') # to latin 
        self.assertEqual(self.cyr_to_latin('М3222ДЦ'), 'M3222QZ')
        
    def test_latin_to_cyr(self):
        self.assertEqual(self.format_plate('BB3333KK'), 'ВВ3333КК') # to cyr
        
    def test_incorrect_strings(self):
        self.assertEqual(self.format_plate('...hm...'), False)
        self.assertEqual(self.format_plate('1123287738479'), False)
        self.assertEqual(self.format_plate('test 123'), False)
        self.assertEqual(self.format_plate('123'), False)
        self.assertEqual(self.format_plate('TEST'), False)
        
if __name__ == '__main__':
    unittest.main()