import os 
import mysql.connector
import random
import string
from datetime import datetime
connection = mysql.connector.connect(
    host='l',
    user='J',
    password='',
    database=''
)
class Admin:
    def __init__(self,name,password):
        self.name = name
        self.password = password
        cursor = connection.cursor()
        query = "SELECT password_hash FROM admin_info WHERE adminname = %s"
        cursor.execute(query, (self.name,))
        result = cursor.fetchone()
        if result:
                stored_password = result[0]
                if stored_password == self.password:
                        print("Welcome")
                else:
                        print("Try again")
        else:
               print("try again")
    #Display shows
    def displayshow():
        cursor = connection.cursor()
        select_query = "SELECT * FROM shows"
        cursor.execute(select_query)
        rows = cursor.fetchall()
        for i in rows:
            print(i)
    #Display records
    def booking_records(self):
        cursor = connection.cursor()
        select_query = "SELECT * FROM Userrecord"
        cursor.execute(select_query)
        rows = cursor.fetchall()
        for i in rows:
            print(i)
    #Assign Slot
    def slot_assignment(self,screen,title,time,seats):
        self.screen = screen
        self.title = title
        self.time = time
        self.seats = seats
        random_id = ''.join([str(random.randint(0, 9)) for _ in range(10)])
        cursor = connection.cursor()
        slot_data = [
        (random_id, self.screen, self.title, self.time, self.seats)
        ]
        sql_query_slot_assignment = "INSERT INTO shows (id, screenname, title, timing, seats) VALUES (%s, %s, %s, %s, %s)"
        cursor.executemany(sql_query_slot_assignment, slot_data)
        connection.commit()
    #Slot deletion
    def slot_deletion(self,id):
        self.id = id
        cursor = connection.cursor()
        sql_query_slot_deletion = "DELETE FROM shows WHERE id = %s"
        cursor.execute(sql_query_slot_deletion,(self.id,))
        connection.commit()
class User:
    def __init__(self,user,password):
        self.user = user
        self.password = password
        cursor = connection.cursor()
        query = "SELECT password_hash FROM users_info WHERE username = %s"
        cursor.execute(query, (self.user,))
        result = cursor.fetchone()
        cursor.close()
        connection.close()
        if result:
                stored_password = result[0]
                if stored_password == self.password:
                        print("Welcome")
                else:
                        print("Try again")
        else:
               print("try again")
    def bookings(self,name,seat,movie_id):
        self.name = name
        self.seat = seat
        self.movie_id = movie_id
        cursor = connection.cursor()
        alpha_part = ''.join(random.choices(string.ascii_uppercase, k=3))
        numeric_part = ''.join(random.choices(string.digits, k=7))
        random_id = alpha_part + numeric_part
        current_datetime = datetime.now()
        fetch_movie_query = "SELECT title, screenname, timing FROM shows WHERE id = %s"
        cursor.execute(fetch_movie_query, (self.movie_id,))
        movie_details = cursor.fetchone()
        if not movie_details:
                print("Invalid movie_id")
                cursor.close()
                connection.close()
                return
        movie, screen, time = movie_details
        ticket_data = [
        (random_id, self.movie_id, self.name, movie, screen, time, self.seat,current_datetime)
        ]
        sql_insert_user_record = """
        INSERT INTO Userrecord (id, movie_id, username, title, screenname, timing, seat, time_of_booking)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        sql_insert_personal_record = f"""
        INSERT INTO {self.name} (id, movie_id, username, title, screenname, timing, seat, time_of_booking)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.executemany(sql_insert_user_record, ticket_data)
        cursor.executemany(sql_insert_personal_record, ticket_data)
        connection.commit()
        update_query = f"UPDATE shows SET seats = seats - {self.seat} WHERE id = %s"
        cursor.execute(update_query, (self.movie_id,))
        connection.commit()
        print("seat booked")
    def personal_booking_history(self,user):
        self.user = user
        cursor = connection.cursor()
        select_query = f"SELECT * FROM {self.user}"
        cursor.execute(select_query)
        rows = cursor.fetchall()
        for i in rows:
            print(i)
    def ticket_cancellation(self,id,user):
        self.id = id
        self.user = user
        cursor = connection.cursor()
        fetch_details_query = "SELECT movie_id, seat FROM Userrecord WHERE id = %s"
        cursor.execute(fetch_details_query, (self.id,))
        result = cursor.fetchone()
        if not result:
            print("Invalid booking id")
            cursor.close()
            connection.close()
            return
        movie_id, seats = result
        sql_query_ticket_cancellation = f"DELETE FROM {self.user} WHERE id = %s"
        sql_query_userrecord_deletion = "DELETE FROM Userrecord WHERE id = %s"
        cursor.execute(sql_query_ticket_cancellation,(self.id,))
        cursor.execute(sql_query_userrecord_deletion,(self.id,))
        connection.commit()
        connection.commit()
        update_query = f"UPDATE shows SET seats = seats + {seats} WHERE id = %s"
        cursor.execute(update_query, (movie_id,))
        connection.commit()
    def displayshow():
        cursor = connection.cursor()
        select_query = "SELECT * FROM shows"
        cursor.execute(select_query)
        rows = cursor.fetchall()
        for i in rows:
            print(i)
class Sign_up:
     def __init__(self,user,password):
        self.user = user
        self.password = password
        cursor = connection.cursor()
        sql_create_table = f"""
        CREATE TABLE IF NOT EXISTS {self.user}(
                id VARCHAR(50) PRIMARY KEY,
                movie_id VARCHAR(50),
                username VARCHAR(50),
                title VARCHAR(50),
                screenname VARCHAR(50),
                timing VARCHAR(50),
                seat INT,
                time_of_booking DATETIME
        )
        """
        cursor.execute(sql_create_table)
        query = "INSERT INTO users_info (username, password_hash) VALUES (%s, %s)"
        cursor.execute(query, (self.user, self.password))
        connection.commit()