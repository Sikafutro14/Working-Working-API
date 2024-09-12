import psycopg2

# Step 1: Connect to your database like a responsible adult
conn = psycopg2.connect(
    dbname="postgres",       # default database
    user="postgres",         # default username
    password="password",     # You gotta protect your neck, and your database
    host="localhost",        # If your database ain't local, you better know what you're doing
    port="5432"              # Default port, 'cause why mess with success?
)

# Step 2: Get yourself a cursor to start running commands
cur = conn.cursor()

# Step 3: Drop the tables if they already exist (like it's hot)
cur.execute("DROP TABLE IF EXISTS customers CASCADE;")
cur.execute("DROP TABLE IF EXISTS vip_customers CASCADE;")

# Step 4: Create the 'customers' table. It's simple, but powerful.
cur.execute("""
CREATE TABLE IF NOT EXISTS customers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    vip_id INTEGER
);
""")

# Step 5: Create the 'vip_customers' table. This is where the real money is.
cur.execute("""
CREATE TABLE IF NOT EXISTS vip_customers (
    id SERIAL PRIMARY KEY,
    level VARCHAR(255) NOT NULL,
    service TEXT
);
""")

# Step 6: Populate the 'customers' table with some iconic names
cur.execute("""
INSERT INTO customers (name, vip_id) VALUES
('Spongebob', NULL),
('Batman', 1),
('Ironman', 2),
('Jesus', NULL);
""")

# Step 7: Populate the 'vip_customers' table with some VIP packages that even Bruce Wayne might consider
cur.execute("""
INSERT INTO vip_customers (level, service) VALUES
('Premium', 'do all he wants or get beaten to a pulp man srsly'),
('Premium Platinum', 'just pray man he can literally vaporize you without effort'),
('SUPER PLATINUM PREMIUM PRESTIGE', 'not even listed in db because of privacy but let''s just say he wears a big S and can end existence on earth without dropping one alien drop of sweat'),
('EXTRA MEGA SUPER MEGA SUPER EXTRA SUPER EXTRA MEGA PLATIPREMIUSTIGE +', 'saving this entry for when kim jong un decides to join corp');
""")

# Commit those changes, so they actually stick (remember, autocommit is False by default in psycopg2)
conn.commit()

# Clean up after yourself, 'cause leaving a mess is just rude.
cur.close()
conn.close()









