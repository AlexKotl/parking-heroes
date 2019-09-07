import unittest
from plate import Plate

class TestPlate(Plate, unittest.TestCase):
    def test_format(self):
        self.assertEqual(self.format_plate('АА 2203 ІК'), 'АА2203ІК')
        self.assertEqual(self.format_plate('- АА2203ІК,'), 'АА2203ІК')
        self.assertEqual(self.format_plate('2203'), '2203')
        self.assertEqual(self.format_plate('К 2203 НН'), 'К2203НН') # old format
        self.assertEqual(self.format_plate('12345 КН'), '12345КН') # another old format
        self.assertEqual(self.format_plate('hm...'), False)
    
    def test_cyr(self):
        self.assertEqual(self.format_plate('BB3333KK'), 'ВВ3333КК') # to cyr
        
if __name__ == '__main__':
    unittest.main()