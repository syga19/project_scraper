from pydantic import BaseModel


class Vacuum(BaseModel):
    title: str
    image_url: str
    price: str
    characteristics: str

class VacuumLink(BaseModel):
    url: str