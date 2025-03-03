from datetime import date, datetime
from typing import Optional, List

from pydantic import BaseModel, Field

from database.models.movies import MovieStatusEnum
from schemas.examples.movies import (
    country_schema_example,
    language_schema_example,
    genre_schema_example,
    actor_schema_example,
    movie_item_schema_example,
    movie_list_response_schema_example,
    movie_create_schema_example,
    movie_detail_schema_example,
    movie_update_schema_example
)


class LanguageSchema(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class CountrySchema(BaseModel):
    id: int
    name: str
    code: str

    class Config:
        from_attributes = True


class GenreSchema(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class ActorSchema(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class MovieSchema(BaseModel):
    id: int
    title: str
    description: str
    release_date: date
    rating: float
    status: MovieStatusEnum
    country: CountrySchema
    language: LanguageSchema
    genres: List[GenreSchema]
    actors: List[ActorSchema]

    class Config:
        from_attributes = True


class CreateMovieSchema(BaseModel):
    title: str
    description: str
    release_date: date
    rating: float
    status: MovieStatusEnum
    country_id: int
    language_id: int
    genre_ids: List[int]
    actor_ids: List[int]
