import pyodbc as odbc
import pandas as pd


class DB:
    def __init__(self):

        self.conn = odbc.connect('Driver={SQL Server};'
                            'Server=LAPTOP-<Add Microsoft SQL Server Name>;'
                            'Database=<Add Database Name>;'
                            'Trusted_Connection=yes;')


        self.cursor= self.conn.cursor()

    def fetch_city(self):
        city=[]
        self.cursor.execute("""
            select DISTINCT Source FROM flights
            UNION
            select distinct Destination from flights
                        """)
        
        data = self.cursor.fetchall()

        for i in data:
            city.append(i[0])

        return city
    
    def fetch_flights_details(self, source, destination):
        self.cursor.execute("""
            select Airline, Date_of_Journey, Route, Price from flights 
            where Source= '{}' AND Destination = '{}'
        """.format(source, destination))
        data= self.cursor.fetchall()
        d={}
        airline=[]
        date=[]
        route=[]
        price=[]

        print("Empty Lists Created")
        for i in data:
            airline.append(i[0])
            date.append(i[1])
            route.append(i[2])
            price.append(i[3])

        d["Airline"]=airline
        d["date"]=date
        d["route"]=route
        d["price"]=price

        df= pd.DataFrame(d)
        return df
    
    def fetch_airline_info(self):
        Airline= []
        frequency= []

        self.cursor.execute("""
            select Airline, COUNT(Airline) from flights
                    group by Airline
        """)

        data= self.cursor.fetchall()

        for i in data:
            Airline.append(i[0])
            frequency.append(i[1])

        return Airline, frequency
    
    def busy_airport(self):
        city=[]
        frequency=[]

        self.cursor.execute("""
            select Source, COUNT(*) from (select Source from flights
					union all
					select Destination from flights) t1
                        GROUP BY Source
                        ORDER BY COUNT(*) DESC
        """)

        data= self.cursor.fetchall()
        for i in data:
            city.append(i[0])
            frequency.append(i[1])

        return city, frequency




    