-- Exported from QuickDBD: https://www.quickdatabasediagrams.com/
-- NOTE! If you have used non-SQL datatypes in your design, you will have to change these here.
DROP TABLE hawaii_measurements,hawaii_stations

CREATE TABLE "hawaii_stations" (
    "station" VARCHAR(255)   NOT NULL,
    "name" VARCHAR(255)   NOT NULL,
    "latitude" FLOAT NOT NULL,
    "longitude" FLOAT  NOT NULL,
    "elevation" FLOAT  NOT NULL,
    CONSTRAINT "pk_hawaii_stations" PRIMARY KEY (
        "station"
     )
);

CREATE TABLE "hawaii_measurements" (
    "station" VARCHAR(255)   NOT NULL,
    "date" DATE  NOT NULL,
    "prcp" FLOAT,
    "tobs" INT  NOT NULL
);

ALTER TABLE "hawaii_measurements" ADD CONSTRAINT "fk_hawaii_measurements_station" FOREIGN KEY("station")
REFERENCES "hawaii_stations" ("station");