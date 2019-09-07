import re

class Plate:
    # latin to cyr translation
    translate_rules = {
        'C': 'С',
        'B': 'В',
        'E': 'Е',
        'T': 'Т',
        'I': 'І',
        'O': 'О',
        'P': 'Р',
        'A': 'А',
        'H': 'Н',
        'K': 'К',
        'X': 'Х',
        'M': 'М',
    }
    
    def format_plate(self, plate):
        ''' Clean raw plate number from foreign symbols and convert latin to cyr ''' 
        
        # strip not used symbols
        plate = re.sub(r'[^а-яА-Я0-9І]', '', plate)
        
        return plate
        
    def is_plate(self, str):
        ''' Check if string is car plate format '''
        pass
        
    