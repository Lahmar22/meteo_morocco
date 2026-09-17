from sqlalchemy import String, Float, Date
from datetime import date as date_type
from sqlalchemy.orm import Mapped, mapped_column

from connectionDB import Base, engine


class City(Base):
    __tablename__ = "cities"

    id: Mapped[int] = mapped_column(primary_key=True)
    city: Mapped[str] = mapped_column(String(100))
    lat: Mapped[float] = mapped_column(Float)
    lng: Mapped[float] = mapped_column(Float)

class Meteo(Base):
    __tablename__ = "meteo"

    id: Mapped[int] = mapped_column(primary_key=True)
    city: Mapped[str] = mapped_column(String(100))
    latitude: Mapped[float] = mapped_column(Float)
    longitude: Mapped[float] = mapped_column(Float)
    date: Mapped[date_type] = mapped_column(Date)
    temp_max: Mapped[float] = mapped_column(Float)
    temp_min: Mapped[float] = mapped_column(Float)
    precipitation: Mapped[float] = mapped_column(Float)
    precip_probability: Mapped[float] = mapped_column(Float)
    wind_speed: Mapped[float] = mapped_column(Float)
    wind_gusts: Mapped[float] = mapped_column(Float)
    weather_code: Mapped[float] = mapped_column(Float)

class MeteoCategories(Base):
    __tablename__ = "meteo_categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    city: Mapped[str] = mapped_column(String(100))
    latitude: Mapped[float] = mapped_column(Float)
    longitude: Mapped[float] = mapped_column(Float)
    date: Mapped[date_type] = mapped_column(Date)
    temp_max: Mapped[float] = mapped_column(Float)
    temp_min: Mapped[float] = mapped_column(Float)
    precipitation: Mapped[float] = mapped_column(Float)
    precip_probability: Mapped[float] = mapped_column(Float)
    wind_speed: Mapped[float] = mapped_column(Float)
    wind_gusts: Mapped[float] = mapped_column(Float)
    weather_code: Mapped[float] = mapped_column(Float)
    temperature_category: Mapped[str] = mapped_column(String(100))
    precipitation_category: Mapped[str] = mapped_column(String(100))
    wind_category: Mapped[str] = mapped_column(String(100))
    score: Mapped[float] = mapped_column(Float)
    danger: Mapped[str] = mapped_column(String(100))


Base.metadata.create_all(engine)

print("Table créée avec succès !")