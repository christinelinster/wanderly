
CREATE TABLE users(
    id SERIAL PRIMARY KEY,
    first_name varchar(100) NOT NULL,
    last_name varchar(100) NOT NULL, 
    username varchar(100) UNIQUE NOT NULL,
    password text NOT NULL,
    created_at date NOT NULL DEFAULT now()
);

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

