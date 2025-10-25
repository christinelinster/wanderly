
CREATE TABLE users(
    id SERIAL PRIMARY KEY,
    full_name varchar(255) NOT NULL, 
    email varchar(255) UNIQUE NOT NULL,
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
    at_time time,
    activity text NOT NULL,
    cost numeric CHECK (cost >= 0.00),
    note text,
    trip_id integer NOT NULL,
    FOREIGN KEY (trip_id) REFERENCES trips(id) ON DELETE CASCADE,
);


