import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import select, func
from connectionDB import SessionLocal
from models import MeteoCategories, City

def getCity():
    with SessionLocal() as session:
        result = session.execute(
            select(func.count(City.city))
        )

        count_city = result.scalar()

    return count_city


def city_temp_max():
    with SessionLocal() as session:
        result = session.execute(
            select(
                MeteoCategories.city,
                func.max(MeteoCategories.temp_max).label("temperature_max")
            )
            .group_by(MeteoCategories.city)
            .order_by(func.max(MeteoCategories.temp_max).desc())
        )

        # for row in result:
        #     print(row.city, row.temperature_max)
    return result

def city_precipitation():
    with SessionLocal() as session:
        result = session.execute(
            select(
                MeteoCategories.city,
                func.sum(MeteoCategories.precipitation).label("total_precipitation")
            )
            .group_by(MeteoCategories.city)
            .order_by(func.sum(MeteoCategories.precipitation).desc())
        )

        for row in result:
            print(row.city, row.total_precipitation)


def city_score():
    with SessionLocal() as session:
        result = session.execute(
            select(
                MeteoCategories.city,
                func.avg(MeteoCategories.score).label("risque_moyen")
            )
            .group_by(MeteoCategories.city)
            .order_by(func.avg(MeteoCategories.score).desc())
        )

        for row in result:
            print(row.city, round(row.risque_moyen, 2))


