from typing import Sequence, Iterable

from sqlalchemy.orm import Session, joinedload, noload
from sqlalchemy import select
from pydantic import BaseModel

from .. import models, schemas, utils


class SyncOrm:

    @staticmethod
    def upsert_aircrafts(conn: Session, data: Iterable[BaseModel]) -> Sequence[models.AircraftModel]:
        mapped_aircrafts = {a.name: a for a in data}

        query = (
            select(models.AircraftModel)
            .filter(models.AircraftModel.name.in_(list(mapped_aircrafts)))
        )

        existed_aircrafts = conn.execute(query).scalars().all()

        for aircraft in existed_aircrafts:
            if aircraft.orig_id != (new_orig_id := mapped_aircrafts[aircraft.name].orig_id):
                aircraft.orig_id = new_orig_id
            mapped_aircrafts.pop(aircraft.name)

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
    def upsert_cities(conn: Session, data: Iterable[BaseModel]) -> Sequence[models.CityModel]:
        mapped_cities = {c.name: c for c in data}

        countries = {
            country.name: country
            for country
            in SyncOrm.upsert_countries(conn=conn, data=[c.country for c in mapped_cities.values()])
        }

        query = (
            select(models.CityModel)
            .filter(models.CityModel.name.in_(list(mapped_cities)))
        )

        existed_cities = conn.execute(query).scalars().all()
        update_columns = utils.get_columns(models.CityModel, exclude={'country_name', 'created_at', 'updated_at'})

        for city in existed_cities:
            for column in update_columns:
                if getattr(city, column) != (new_value := getattr(mapped_cities[city.name], column)):
                    setattr(city, column, new_value)

            country_name = mapped_cities[city.name].country.name
            city.country = countries[country_name]

            mapped_cities.pop(city.name)

        new_cities = [models.CityModel(**c.model_dump(exclude='country'), country=countries[c.country.name]) for c in mapped_cities.values()]
        conn.add_all(new_cities)
        conn.commit()

        return list(existed_cities) + new_cities

    @staticmethod
    def upsert_airports(conn: Session, data: Iterable[schemas.AirportSchema]) -> Sequence[models.AirportModel]:
        mapped_airports = {a.iata: a for a in data}

        query = (
            select(models.AirportModel)
            .filter(models.AirportModel.iata.in_(list(mapped_airports)))
        )

        cities = {c.name: c for c in SyncOrm.upsert_cities(conn, [a.city for a in mapped_airports.values()])}

        existed_airports = conn.execute(query).scalars().all()
        update_columns = utils.get_columns(models.AirportModel, exclude={'city_name', 'created_at', 'updated_at'})

        for airport in existed_airports:
            for column in update_columns:
                if getattr(airport, column) != (new_value := getattr(mapped_airports[airport.iata], column)):
                    setattr(airport, column, new_value)

            city_name = mapped_airports[airport.iata].city.name
            airport.city = cities[city_name]

            mapped_airports.pop(airport.iata)

        new_airports = [models.AirportModel(**a.model_dump(exclude='city'), city=cities[a.city.name]) for a in mapped_airports.values()]
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
        aircrafts_models = {a.name: a for a in SyncOrm.upsert_aircrafts(conn, aircrafts)}
        airports_models = {a.iata: a for a in SyncOrm.upsert_airports(conn, airports)}

        query = (
            select(models.FlightModel)
            .filter(models.FlightModel.orig_id.in_(list(mapped_flights)))
        )

        existed_flights = conn.execute(query).scalars().all()
        update_columns = utils.get_columns(models.FlightModel, exclude=(
            'company_iata',
            *[f'mar{i}_iata' for i in range(1, 6)],
            'aircraft_name',
            'created_at',
            'updated_at',
        ))
        flights_changelog = []

        for flight in existed_flights:

            for column in update_columns:
                if (old_value := getattr(flight, column)) != (new_value := getattr(mapped_flights[flight.orig_id], column)):
                    setattr(flight, column, new_value)
                    flights_changelog.append(
                        models.FlightsChangelogModel(field=column, old_value=old_value, flight=flight))

            flight_schema = mapped_flights[flight.orig_id]
            flight.company = companies_models[flight_schema.company.iata]
            flight.aircraft = aircrafts_models[flight_schema.aircraft.name]
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
                                          aircraft=aircrafts_models[f.aircraft.name],
                                          **{f'mar{i}': airports_models[getattr(f, f'mar{i}').iata] for i in range(1, 6)
                                             if getattr(f, f'mar{i}') is not None}
                                          )
                       for f in mapped_flights.values()]

        conn.add_all(new_flights)
        conn.add_all(flights_changelog)
        conn.commit()

        return list(existed_flights) + new_flights

    @staticmethod
    def get_flight_ids(conn: Session, params: schemas.FlightsGetParamsSchema) -> Sequence[models.FlightModel.id]:
        query = (
            select(models.FlightModel.__table__.c.id)
            .order_by(models.FlightModel.sked_local.asc())
            .filter(models.FlightModel.direction == params.direction)
            .filter(models.FlightModel.sked_local >= params.date_start,
                    models.FlightModel.sked_local <= params.date_end)
        )
        if params.company is not None:
            query = query.filter(models.FlightModel.company_iata == params.company)
        if params.gate_id is not None:
            query = query.filter(models.FlightModel.gate_id == params.gate_id)
        if params.destination is not None:
            other_airport_mar = {'arrival': 1, 'departure': 2}[params.direction]
            attr = getattr(models.FlightModel, f'mar{other_airport_mar}_iata')
            query = query.filter(attr == params.destination)

        flight_ids = conn.execute(query).scalars().all()
        return flight_ids

    @staticmethod
    def get_flights_by_ids(conn: Session, ids: Sequence[int], changelog: bool = False) -> Sequence[models.FlightModel]:
        loadmethod = joinedload if changelog is True else noload
        query = (
            select(models.FlightModel)
            .options(loadmethod(models.FlightModel.changelog))
            .order_by(models.FlightModel.sked_local.asc())
            .filter(models.FlightModel.id.in_(ids))
        )
        flights = conn.execute(query).scalars().unique().all()

        return flights
