from pydantic import BaseModel
from typing import Optional, List


class DateObject(BaseModel):
    month: int
    year: int


class Experience(BaseModel):
    company: str
    title: str
    starts_at: DateObject
    ends_at: Optional[DateObject]


class Education(BaseModel):
    school: str
    degree_name: Optional[str]
    field_of_study: Optional[str]
    starts_at: DateObject
    ends_at: Optional[DateObject]


class LinkedinData(BaseModel):
    public_identifier: str
    full_name: str
    occupation: Optional[str]
    headline: Optional[str]
    summary: Optional[str]
    country_full_name: Optional[str]
    city: Optional[str]
    experiences: Optional[List[Experience]] = []
    education: Optional[List[Education]] = []
