from sqlmodel import SQLModel, Field
import datetime
import uuid


class PasswordChange(SQLModel, table=True):
    __tablename__ = "password_change"
    id: uuid.UUID = Field(primary_key=True, default_factory=uuid.uuid4)
    email: str
    password_key: str
    timestamp: datetime.datetime
