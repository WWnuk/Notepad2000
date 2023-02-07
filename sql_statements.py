drop_table_users = """
DROP TABLE Users
"""
create_users_table = """
CREATE TABLE IF NOT EXISTS tUsers (
  Worker_ID INTEGER PRIMARY KEY AUTOINCREMENT,
  Username TEXT NOT NULL,
  Password TEXT NOT NULL,
  Name TEXT NOT NULL,
  Surname TEXT NOT NULL,
  Office_Location
);
"""