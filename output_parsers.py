from pydantic import BaseModel, Field
from typing import Optional, List
from langchain_core.output_parsers import PydanticOutputParser


class Summary(BaseModel):

    summary: str = Field(description="Summary of the Linkedin profile")
    facts: List[str] = Field(description="Interesting Facts about the Linkedin profile")

    def to_dict(self):
        return {
            "summary": self.summary,
            "facts": self.facts
        }
    

summary_parser = PydanticOutputParser(pydantic_object=Summary)