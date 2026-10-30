import pyodbc
import pandas as pd

from pathlib import Path

conn =pyodbc.connect(
    r"DRIVER={ODBC Driver 18 for SQL Server};"
    r"SERVER=AVEE\SQLEXPRESS;"
    r"DATABASE=master;"
    r"Trusted_Connection=yes;"
    r"TrustServerCertificate=yes;",
    autocommit=True
)
conn.autocommit = True

print ("SQl server connected sucessfully")
cursor = conn.cursor()
cursor.execute("""select db_id('UserActivity')""")
database_id = cursor.fetchone()[0]

if database_id is None:
    cursor.execute("CREATE DATABASE UserActivity")
    print("Database created successfully")

# Select the database whether it is new or already exists
cursor.execute("USE UserActivity")
print("Existing table columns:")




# Create the table if it does not already exist
cursor.execute("""IF OBJECT_ID('dbo.Users', 'U') IS NULL
BEGIN
    CREATE TABLE dbo.Users(
        User_id  VARCHAR(32), 
        country VARCHAR(100), 
        Channel VARCHAR(32)
    )
END
""")
cursor.execute("""
IF OBJECT_ID('dbo.UsersActivitys', 'U') IS NULL
BEGIN
    CREATE TABLE dbo.UsersActivitys (
        user_id VARCHAR(32),
        event_name VARCHAR(100),
        event_timestamp DATETIME2,
        event_date DATE
    )
END
""")
print("Table created or already exists")

columns = [
    "user_id",
    "country",
    "channel"]
columns2 = [
    "user_id",
    "event_name",
    "event_timestamp",
    "event_date",

]
def insert_data(df1):
    data = df1.loc[:, columns].copy()
    insert_sql =""" INSERT INTO dbo.Users(
                        user_id,
                        country,
                        channel 
                        )
                        values (?,?,?)
                        """

    row =list(data.itertuples(index=False, name=None))
    insert_cursor = conn.cursor()
    insert_cursor.executemany(insert_sql, row)
    print("Inserting data", len(row))
    insert_cursor.close()

def insert_data2 (df2):
    data2 = df2.loc[:, columns2].copy()
    insert_sql2 = """ INSERT INTO dbo.UsersActivitys(
                           user_id,
                           event_name,
                           event_timestamp,
                            event_date
                           )values(?,?,?,?)
                       """
    row2 = list(data2.itertuples(index=False, name=None))
    insert_cursor2 = conn.cursor()
    insert_cursor2.executemany(insert_sql2, row2)
    print("Inserting :", len(row2))
    insert_cursor2.close()

project_dir = Path(__file__).resolve().parent.parent
data_dir = project_dir / "data"

file_path = data_dir / "users.csv"
df1 = pd.read_csv(file_path)


file_path2 = data_dir / "events.csv"
df2 = pd.read_csv(file_path2)

cursor.execute("TRUNCATE TABLE dbo.UsersActivitys")
cursor.execute("TRUNCATE TABLE dbo.Users")
insert_data(df1)
insert_data2(df2)

cursor.execute("SELECT COUNT(*) FROM dbo.Users")
print("Total user rows:", cursor.fetchone()[0])
cursor.execute("SELECT COUNT(*) FROM dbo.UsersActivitys")
print("Total event rows:", cursor.fetchone()[0])


conn.commit()
cursor.close()
conn.close()
print("Database is ready.")
