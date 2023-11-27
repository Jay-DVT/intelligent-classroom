from db_conn import conn

cur = conn.cursor()

cur.execute(f"""
            CREATE TABLE IF NOT EXISTS profesor (
            id INTEGER PRIMARY KEY,
            first_name TEXT NOT NULL,
            last_name TEXT
            )
            """)
conn.commit()


cur.execute(f"""
            CREATE TABLE IF NOT EXISTS class (
            id INTEGER PRIMARY KEY,
            serial TEXT NOT NULL,
            name TEXT NOT NULL,
            module INTEGER
            )
            """)
conn.commit()

cur.execute(f"""
            CREATE TABLE IF NOT EXISTS assigned_class (
            professor_id INTEGER,
            class_id INTEGER,
            FOREIGN KEY(professor_id) REFERENCES professor(id)
            FOREIGN KEY(class_id) REFERENCES class(id)
            );
            """)
conn.commit()

cur.execute(f"""
            CREATE TABLE IF NOT EXISTS instruction (
            id INTEGER PRIMARY KEY,
            step_number INTEGER,
            component TEXT,
            parameter TEXT,
            class_id INTEGER,
            FOREIGN KEY(class_id) REFERENCES class(id) 
            )
            """)
conn.commit()

cur.execute(f"""
            CREATE TABLE IF NOT EXISTS log (
            id INTEGER PRIMARY KEY,
            timestamp DATE,
            result TEXT,
            instruction_id INTEGER,
            FOREIGN KEY(instruction_id) REFERENCES instruction(id) 
            )
            """)
