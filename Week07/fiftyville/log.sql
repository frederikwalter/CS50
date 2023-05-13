-- Keep a log of any SQL queries you execute as you solve the mystery.

-- Find all crime reports for the date on Humphrey Street
SELECT description
  FROM crime_scene_reports
 WHERE year = '2021'
   AND month = '7'
   AND day = '28'
   AND street = 'Humphrey Street';
-- Theft of the CS50 duck took place at 10:15am at the Humphrey Street bakery. Interviews were conducted today with three witnesses who were present at the time – each of their interview transcripts mentions the bakery.

-- Look into the interviews
SELECT name, transcript
  FROM interviews
 WHERE year = '2021'
   AND month = '7'
   AND day = '28'
   AND transcript LIKE '%bakery%';
-- Ruth:    Sometime within ten minutes of the theft, I saw the thief get into a car in the bakery parking lot and drive away. If you have security footage from the bakery parking lot, you might want to look for cars that left the parking lot in that time frame.
-- Eugene:  I don't know the thief's name, but it was someone I recognized. Earlier this morning, before I arrived at Emma's bakery, I was walking by the ATM on Leggett Street and saw the thief there withdrawing some money.
-- Raymond: As the thief was leaving the bakery, they called someone who talked to them for less than a minute. In the call, I heard the thief say that they were planning to take the earliest flight out of Fiftyville tomorrow. The thief then asked the person on the other end of the phone to purchase the flight ticket.

-- Find the people belonging the cars from the security footages within ten minutes from the theft
SELECT name
  FROM people
 WHERE license_plate IN
       (SELECT license_plate
          FROM bakery_security_logs
         WHERE year = '2021'
           AND month = '7'
           AND day = '28'
           AND hour = '10'
           AND minute BETWEEN 14 AND 26
           AND activity = 'exit');
-- Vanessa, Barry, Iman, Sofia, Luca, Diana, Kelsey, Bruce

-- Find relevant withdrawings from ATM in Leggett Street
SELECT *
  FROM atm_transactions
 WHERE year = '2021'
       AND month = '7'
       AND day = '28'
       AND atm_location = 'Leggett Street'
       AND transaction_type = 'withdraw';

-- Find people withdrawing money from the ATM
SELECT name
  FROM people
 WHERE id IN
       (
        SELECT person_id
          FROM bank_accounts
         WHERE account_number IN
               (
                SELECT account_number
                  FROM atm_transactions
                 WHERE year = '2021'
                   AND month = '7'
                   AND day = '28'
                   AND atm_location = 'Leggett Street'
                   AND transaction_type = 'withdraw'
               )
       );
-- Kenny, Iman, Benista, Taylor, Brooke, Luca, Diana, Bruce

-- Find the phone calls with less than 60 seconds on that day
SELECT *
  FROM phone_calls
 WHERE year = '2021'
       AND month = '7'
       AND day = '28'
       AND duration < 60;

-- Find persons making phone calls that day
SELECT name
  FROM people
 WHERE phone_number IN
       (SELECT caller
          FROM phone_calls
         WHERE year = '2021'
           AND month = '7'
           AND day = '28'
           AND duration < 60);
-- Kenny, Sofia, Benista, Taylor, Diana, Kelsey, Bruce, Carina

-- Find destination of first flight out of Fiftyville on the next day
SELECT city
  FROM airports
 WHERE id =
       (
          SELECT destination_airport_id
            FROM flights
           WHERE year = '2021'
             AND month = '7'
             AND day = '29'
             AND origin_airport_id =
                 (
                  SELECT id
                  FROM airports
                  WHERE city = 'Fiftyville'
                 )
        ORDER BY hour, minute
           LIMIT 1
       );
-- New York City


-- Find passengers on the first flight out of Fiftyville the next morning
SELECT name
  FROM people
 WHERE passport_number IN
       (
        SELECT passport_number
          FROM passengers
         WHERE flight_id =
               (
                SELECT id
                  FROM flights
                 WHERE year = '2021'
                   AND month = '7'
                   AND day = '29'
                   AND origin_airport_id =
                       (
                        SELECT id
                          FROM airports
                         WHERE city = 'Fiftyville'
                       )
              ORDER BY hour, minute
                 LIMIT 1
               )
       );
-- Kenny, Sofia, Taylor, Luca, Kelsey, Edward, Bruce, Doris

-- Find person who fulfills all criteria: left the bakery in the car, withdraw money from ATM, makes phone call and is on the flight out of Fiftyville
SELECT name
  FROM people
 WHERE license_plate IN
       ( -- get everyone who exited the parking lot in the 10 minutes after the theft
        SELECT license_plate
          FROM bakery_security_logs
         WHERE year = '2021'
           AND month = '7'
           AND day = '28'
           AND hour = '10'
           AND minute BETWEEN 14 AND 26
           AND activity = 'exit'
       )
   AND id IN
       ( -- get everyone withdrawing money that day
        SELECT person_id
          FROM bank_accounts
         WHERE account_number IN
               ( -- get all account numbers of people withdrawing money that day
                SELECT account_number
                  FROM atm_transactions
                 WHERE year = '2021'
                   AND month = '7'
                   AND day = '28'
                   AND atm_location = 'Leggett Street'
                   AND transaction_type = 'withdraw'
               )
       )
   AND phone_number IN
       ( -- get everyone calling someone that day
        SELECT caller
          FROM phone_calls
         WHERE year = '2021'
           AND month = '7'
           AND day = '28'
           AND duration < 60
       )
   AND passport_number IN
       ( -- get everyone on the first flight out of Fiftyville the next day
        SELECT passport_number
          FROM passengers
         WHERE flight_id =
               ( -- get the first flight out of Fiftyville the next day
                SELECT id
                  FROM flights
                 WHERE year = '2021'
                   AND month = '7'
                   AND day = '29'
                   AND origin_airport_id =
                       ( --  get the airport id of Fiftyville
                        SELECT id
                          FROM airports
                         WHERE city = 'Fiftyville'
                       )
              ORDER BY hour, minute
                 LIMIT 1
               )
       );
-- Bruce

-- Find the person Bruce talked to on the phone
SELECT name
  FROM people
 WHERE phone_number IN
       (
        SELECT receiver
          FROM phone_calls
         WHERE year = '2021'
           AND month = '7'
           AND day = '28'
           AND duration < 60
           AND caller =
               (
                SELECT phone_number
                  FROM people
                 WHERE name = 'Bruce'
               )
       );
-- Robin


-- Overall query to find the accomplice
SELECT name
  FROM people
 WHERE phone_number IN
       ( -- find the receiver of the phone call
        SELECT receiver
          FROM phone_calls
         WHERE year = '2021'
           AND month = '7'
           AND day = '28'
           AND duration < 60
           AND caller =
               ( -- find the phone number of the caller who is the thief
                SELECT phone_number
                  FROM people
                 WHERE name =
                       ( -- Find the thief
                        SELECT name
                          FROM people
                         WHERE license_plate IN
                               ( -- get everyone who exited the parking lot in the 10 minutes after the theft
                                SELECT license_plate
                                  FROM bakery_security_logs
                                 WHERE year = '2021'
                                   AND month = '7'
                                   AND day = '28'
                                   AND hour = '10'
                                   AND minute BETWEEN 14 AND 26
                                   AND activity = 'exit'
                               )
                           AND id IN
                               ( -- get everyone withdrawing money that day
                                SELECT person_id
                                  FROM bank_accounts
                                 WHERE account_number IN
                                       ( -- get all account numbers of people withdrawing money that day
                                        SELECT account_number
                                          FROM atm_transactions
                                         WHERE year = '2021'
                                           AND month = '7'
                                           AND day = '28'
                                           AND atm_location = 'Leggett Street'
                                           AND transaction_type = 'withdraw'
                                       )
                               )
                           AND phone_number IN
                               ( -- get everyone calling someone that day
                                SELECT caller
                                  FROM phone_calls
                                 WHERE year = '2021'
                                   AND month = '7'
                                   AND day = '28'
                                   AND duration < 60
                               )
                           AND passport_number IN
                               ( -- get everyone on the first flight out of Fiftyville the next day
                                SELECT passport_number
                                  FROM passengers
                                 WHERE flight_id =
                                       ( -- get the first flight out of Fiftyville the next day
                                        SELECT id
                                          FROM flights
                                         WHERE year = '2021'
                                           AND month = '7'
                                           AND day = '29'
                                           AND origin_airport_id =
                                               ( --  get the airport id of Fiftyville
                                                SELECT id
                                                  FROM airports
                                                 WHERE city = 'Fiftyville'
                                               )
                                      ORDER BY hour, minute
                                         LIMIT 1
                                       )
                               )
                       )
               )
       );
-- Robin

