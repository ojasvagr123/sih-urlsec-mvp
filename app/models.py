from typing import Optional, Dict, Any
from sqlmodel import SQLModel, Field, Column, JSON


class Event(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    timestamp: str
    src_ip: str
    dst_ip: Optional[str] = None
    method: Optional[str] = None
    url: Optional[str] = None

    # JSON columns
    params: Optional[Dict[str, Any]] = Field(default=None, sa_column=Column(JSON))
    headers: Optional[Dict[str, Any]] = Field(default=None, sa_column=Column(JSON))

    body: Optional[str] = None
    body_snippet: Optional[str] = None
    attack_type: Optional[str] = None
    attack_confidence: Optional[float] = 0.0
    is_success: Optional[bool] = False
    honeypot_correlated: Optional[bool] = False
    honeypot_session: Optional[str] = None


class CowrieEvent(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    timestamp: str
    src_ip: str
    event: str
    username: Optional[str] = None
    password: Optional[str] = None
    session: Optional[str] = None
