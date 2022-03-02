
create_users_table = """CREATE TABLE IF NOT EXISTS users(
       id INT PRIMARY KEY,
       fname TEXT,
       lname TEXT,
       username TEXT,
       sdate INTEGER );
    """

insert_user = "INSERT OR REPLACE INTO users VALUES (?, ?, ?, ?, ?)"
