from typing import Sequence, Iterable

from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session
from sqlalchemy import select
from pydantic import BaseModel
from collections import defaultdict

from .. import models
from .. import schemas
from .. import utils


class SyncOrm:

    @staticmethod
    def upsert_aircrafts(conn: Session, data: Iterable[BaseModel]) -> Sequence[models.AircraftModel]:
        mapped_aircrafts = {a.orig_id: a for a in data}

        query = (
            select(models.AircraftModel)
            .filter(models.AircraftModel.orig_id.in_(list(mapped_aircrafts)))
        )

        existed_aircrafts = conn.execute(query).scalars().all()

        for aircraft in existed_aircrafts:
            if aircraft.name != (new_name := mapped_aircrafts[aircraft.orig_id].name):
                aircraft.name = new_name
            mapped_aircrafts.pop(aircraft.orig_id)

        new_aircrafts = [models.AircraftModel(**a.model_dump()) for a in mapped_aircrafts.values()]
        conn.add_all(new_aircrafts)
        conn.commit()

        return list(existed_aircrafts) + new_aircrafts


    @staticmethod
    def upsert_countries(conn: Session, data: Iterable[BaseModel]) -> Sequence[models.CountryModel]:
        mapped_countries = {c.name: c for c in data}

        query = (
            select(models.CountryModel)
            .filter(models.CountryModel.name.in_(list(mapped_countries)))
        )

        existed_countries = conn.execute(query).scalars().all()
        for country in existed_countries:
            if country.region != (new_region := mapped_countries[country.name].region):
                country.region = new_region
            mapped_countries.pop(country.name)

        new_countries = [models.CountryModel(**c.model_dump()) for c in mapped_countries.values()]
        conn.add_all(new_countries)
        conn.commit()

        return list(existed_countries) + new_countries


    @staticmethod
    def upsert_airports(conn: Session, data: Iterable[schemas.AirportSchema]) -> Sequence[models.AirportModel]:
        mapped_airports = {a.iata: a for a in data}

        query = (
            select(models.AirportModel)
            .filter(models.AirportModel.iata.in_(list(mapped_airports)))
        )

        countries = {c.name: c for c in SyncOrm.upsert_countries(conn, [a.country for a in mapped_airports.values()])}

        existed_airports = conn.execute(query).scalars().all()
        update_columns = utils.get_columns(models.AirportModel, exclude={'country_id', 'created_at', 'updated_at'})
        for airport in existed_airports:

            for column in update_columns:
                if getattr(airport, column) != (new_value := getattr(mapped_airports[airport.iata], column)):
                    setattr(airport, column, new_value)

            country_name = mapped_airports[airport.iata].country.name
            airport.country = countries[country_name]

            mapped_airports.pop(airport.iata)

        new_airports = [models.AirportModel(**a.model_dump(exclude='country'), country=countries[a.country.name]) for a in mapped_airports.values()]
        conn.add_all(new_airports)
        conn.commit()

        return list(existed_airports) + new_airports


    @staticmethod
    def upsert_companies(conn: Session, data: Iterable[schemas.CompanySchema]) -> Sequence[models.CompanyModel]:
        mapped_company = {c.iata: c for c in data}

        query = (
            select(models.CompanyModel)
            .filter(models.CompanyModel.iata.in_(list(mapped_company)))
        )

        existed_companies = conn.execute(query).scalars().all()
        update_columns = utils.get_columns(models.CompanyModel, exclude={'created_at', 'updated_at'})
        for company in existed_companies:

            for column in update_columns:
                if getattr(company, column) != (new_value := getattr(mapped_company[company.iata], column)):
                    setattr(company, column, new_value)

            mapped_company.pop(company.iata)

        new_companies = [models.CompanyModel(**c.model_dump()) for c in mapped_company.values()]
        conn.add_all(new_companies)
        conn.commit()

        return list(existed_companies) + new_companies

    @staticmethod
    def upsert_flights(conn: Session, data: Iterable[schemas.FlightSchema]) -> Sequence[models.FlightModel]:
        mapped_flights = {f.orig_id: f for f in data}
        companies, aircrafts, airports = set(), set(), set()

        for flight in mapped_flights.values():
            companies.add(flight.company)
            aircrafts.add(flight.aircraft)
            for i in range(1, 6):
                if getattr(flight, f'mar{i}', None):
                    airports.add(getattr(flight, f'mar{i}'))

        companies_models = {c.iata: c for c in SyncOrm.upsert_companies(conn, companies)}
        aircrafts_models = {a.orig_id: a for a in SyncOrm.upsert_aircrafts(conn, aircrafts)}
        airports_models = {a.iata: a for a in SyncOrm.upsert_airports(conn, airports)}

        query = (
            select(models.FlightModel)
            .filter(models.FlightModel.orig_id.in_(list(mapped_flights)))
        )

        existed_flights = conn.execute(query).scalars().all()
        update_columns = utils.get_columns(models.FlightModel, exclude=(
            'company_id',
            *[f'mar{i}_id' for i in range(1, 6)],
            'aircraft_id',
            'created_at',
            'updated_at',
        ))

        for flight in existed_flights:

            for column in update_columns:
                if getattr(flight, column) != (new_value := getattr(mapped_flights[flight.orig_id], column)):
                    setattr(flight, column, new_value)

            flight_schema = mapped_flights[flight.orig_id]
            flight.company = companies_models[flight_schema.company.iata]
            flight.aircraft = aircrafts_models[flight_schema.aircraft.orig_id]
            for i in range(1, 6):
                attr = f'mar{i}'
                airport_schema = getattr(flight_schema, attr)
                if airport_schema is not None:
                    value = airports_models[airport_schema.iata]
                    setattr(flight, attr, value)

            mapped_flights.pop(flight.orig_id)

        new_flights = [models.FlightModel(**f.model_dump(
            exclude={'company', 'aircraft', *[f'mar{i}' for i in range(1, 6)]}),
                                          company=companies_models[f.company.iata],
                                          aircraft=aircrafts_models[f.aircraft.orig_id],
                                          **{f'mar{i}': airports_models[getattr(f, f'mar{i}').iata] for i in range(1, 6)
                                             if getattr(f, f'mar{i}') is not None}
                                          )
                       for f in mapped_flights.values()]

        conn.add_all(new_flights)
        conn.commit()

        return list(existed_flights) + new_flights

