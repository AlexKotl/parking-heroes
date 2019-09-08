from mysql import MySQL

class Queries:
    def __init__(self):
        self.db = MySQL()
        
    def get_all_parking(self):
        return self.db.get_rows("SELECT * FROM parking")
    
    def get_parking_by_plate(self, plate):
        return self.db.get_rows("SELECT * FROM parking WHERE car_plate = %s ORDER BY id DESC", (plate,))

    def add_parking(self, **kwargs):
        data = {
            'car_plate': kwargs['car_plate'],
            'user_id': kwargs['user_id'],
            'user_username': kwargs['user_username'],
            'user_first_name': kwargs['user_first_name'],
            'user_last_name': kwargs['user_last_name'],
        }
        return self.db.insert('parking', data)
