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
        'Q': 'Д',
        'Z': 'Ц'
    }
    
    def format_plate(self, plate):
        ''' Clean raw plate number from foreign symbols and convert latin to cyr ''' 
        # convert to upper
        plate = plate.upper()
        
        # convert latin to cyr letters
        plate = self.latin_to_cyr(plate)
        
        # strip not used symbols
        plate = re.sub(r'[^А-Я0-9І]', '', plate)
        
        # test for proper regexp
        if not re.match(r"([А-ЯІ]{0,2})([0-9]{4,5}){1}([А-ЯІ]{0,2})", plate) or len(plate) > 8:
            return False
        
        return plate
    
    def latin_to_cyr(self, str):
        for ch in self.translate_rules.keys():
            if ch in str:
                str = str.replace(ch, self.translate_rules[ch])
        return str

    def cyr_to_latin(self, str):
        for ch in self.translate_rules.values():
            if ch in str:
                to_replace = list(self.translate_rules.keys())[list(self.translate_rules.values()).index(ch)]
                str = str.replace(ch, to_replace)
        return str