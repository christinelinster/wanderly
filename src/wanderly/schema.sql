
CREATE TABLE users(
    id SERIAL PRIMARY KEY,
    full_name varchar(255) NOT NULL, 
    email varchar(255) UNIQUE NOT NULL,
    password text NOT NULL,
    created_at date NOT NULL DEFAULT now()
);

-- ADD A DATES TABLE? 

CREATE TABLE trips(
    id serial PRIMARY KEY,
    destination text NOT NULL, 
    depart_date date,
    return_date date,
    user_id integer NOT NULL REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE plans(
    id serial PRIMARY KEY,
    at_date date,
    activity text NOT NULL,
    cost numeric CHECK (cost > 0),
    note text,
    vacation_id integer NOT NULL REFERENCES vacations(id) ON DELETE CASCADE
);

