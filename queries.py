from mysql import MySQL

class Queries:
    def __init__(self):
        self.db = MySQL()
        
    def get_all_parking(self):
        return self.db.get_rows("SELECT * FROM parking")
    
    def get_parking_by_plate(self, plate):
        return self.db.get_rows("SELECT * FROM parking WHERE car_plate = %s ORDER BY id DESC", {"car_plate": plate})

    def add_parking(self, **kwargs):
        data = {
            'car_plate': kwargs['car_plate'],
            'description': kwargs['description']
        }
        return self.db.insert('parking', data)
