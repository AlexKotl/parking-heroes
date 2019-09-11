from mysql import MySQL

class Queries:
    def __init__(self):
        self.db = MySQL()
        
    def get_top_parkings(self):
        return self.db.get_rows("SELECT * FROM parking WHERE flag=1 ORDER BY id DESC LIMIT 10")
    
    def get_parking_by_plate(self, plate):
        return self.db.get_rows("SELECT * FROM parking WHERE car_plate = %s AND flag=1 ORDER BY id DESC", (plate,))
    
    def get_latest_parking_by_user(self, id):
        return self.db.get_row("SELECT * FROM parking WHERE user_id = %s AND flag=1 ORDER BY id DESC LIMIT 1", (id,))
        
    def get_overall_stats(self):
        return self.db.get_row("SELECT count(distinct car_plate) as cars_count, count(distinct user_id) as users_count, "\
            "count(id) as records_count, count(distinct photo)-1 as photo_count "\
            "FROM parking WHERE flag=1")

    def add_parking(self, **kwargs):
        data = {
            'car_plate': kwargs['car_plate'],
            'user_id': kwargs['user_id'],
            'user_username': kwargs['user_username'],
            'user_first_name': kwargs['user_first_name'],
            'user_last_name': kwargs['user_last_name'],
            'description': '', # insert empty text at start
        }
        return self.db.insert('parking', data)
        
    def edit_parking(self, id, data):
        return self.db.update('parking', id, data)
