from pydantic import BaseModel, Field, field_validator

class UserSubjectToolBase(BaseModel):
    user_id: str = Field(description="The authenticated user's ID. Always use the user ID provided in the system prompt.")
    subject: str = Field(description="The academic subject e.g. chemistry, physics, biology.")

    @field_validator('subject')
    @classmethod
    def lowercase_subject(cls, v: str) -> str:
        return cls.get_subject_key(v.lower())

    @staticmethod
    def get_subject_key(subject: str) -> str:
        subjects_map: dict[str, str] = {
            "english": "english",
            "biology": "biology",
            "chemistry": "chemistry",
            "physics": "physics",
            "history": "history",
            "mathematics": "mathematics",
            "geography": "geography",
            "literature": "englishlit",
            "economics": "economics",
            "government": "government",
            "commerce": "commerce",
            "accounting": "accounting",
            "insurance": "insurance",
            "civic education": "civiledu",
            "irk": "irk",
            "crk": "crk",
            "jamb novel": "novel",
        }
        return subjects_map.get(subject, subject)

class GetUserSubjectRank(UserSubjectToolBase):
    pass

class GetUserSubjectPoints(UserSubjectToolBase):
    pass

class GetUserSubjectStats(UserSubjectToolBase):
    pass
