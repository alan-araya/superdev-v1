DROP TABLE IF EXISTS flight_booking;

CREATE TABLE flight_booking (
    id SERIAL PRIMARY KEY,
    flight_number INT NOT NULL,
    seat VARCHAR(10) NOT NULL UNIQUE,
    seat_type VARCHAR(30) NOT NULL,
    is_free BOOLEAN NOT NULL DEFAULT TRUE,
    booking_date TIMESTAMP
);
