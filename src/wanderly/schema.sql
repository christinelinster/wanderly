CREATE TABLE vacations(
    id serial PRIMARY KEY,
    destination text NOT NULL, 
    depart_date date,
    return_date date
);

CREATE TABLE plans(
    id serial PRIMARY KEY,
    at_date date,
    activity text NOT NULL,
    cost numeric CHECK (cost > 0),
    note text,
    vacation_id integer NOT NULL REFERENCES vacations(id) ON DELETE CASCADE
);