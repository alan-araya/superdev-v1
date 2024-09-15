CREATE TABLE flight_booking (
    id SERIAL PRIMARY KEY,
    flight_number INT NOT NULL,
    seat VARCHAR(10) NOT NULL UNIQUE,
    is_free BOOLEAN DEFAULT TRUE,
    booking_date TIMESTAMP
);
