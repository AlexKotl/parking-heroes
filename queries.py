from mysql import MySQL

class Queries:
    def __init__(self):
        self.db = MySQL()
        
    def get_all_parking(self):
        return self.db.get_rows("SELECT * FROM parking")

    def add_parking(self, **kwargs):
        data = {
            'car_plate': kwargs['car_plate'],
            'description': kwargs['description']
        }
        return self.db.insert('parking', data)
