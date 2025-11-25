from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Car:
    id: Optional[int] = None
    name: str = ""
    model: str = ""
    year: int = datetime.now().year
    color: str = ""
    license_plate: str = ""
    price_per_day: float = 0.0
    price: float = 0.0  # Purchase price
    available: bool = True
    for_sale: bool = False  # Explicitly add for_sale field
    for_rent: bool = False  # Explicitly add for_rent field
    image_url: str = ""
    description: str = ""
    car_type: str = "SEDAN"  # Default car type
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "model": self.model,
            "year": self.year,
            "color": self.color,
            "licensePlate": self.license_plate,
            "pricePerDay": self.price_per_day,
            "dailyRate": self.price_per_day,  # For backward compatibility
            "price": self.price,
            "available": self.available,
            "imageUrl": self.image_url,
            "image_url": self.image_url,  # For backward compatibility
            "description": self.description,
            "forSale": getattr(self, 'for_sale', self.price > 0),  # Default to True if price > 0
            "forRent": getattr(self, 'for_rent', self.price_per_day > 0),  # Default to True if price_per_day > 0
            "type": getattr(self, 'car_type', 'SEDAN')  # Default to 'SEDAN' if not set
        }
        
    @classmethod
    def from_dict(cls, data: dict):
        # Handle both pricePerDay and dailyRate fields
        price_per_day = data.get("pricePerDay")
        if price_per_day is None:
            price_per_day = data.get("dailyRate", 0.0)
            
        # Handle price field
        price = data.get("price")
        if price is None:
            price = float(price_per_day) * 200 if price_per_day else 0.0
            
        return cls(
            id=data.get("id"),
            name=data.get("name", ""),
            model=data.get("model", ""),
            year=data.get("year", datetime.now().year),
            color=data.get("color", ""),
            license_plate=data.get("licensePlate", ""),
            price_per_day=float(price_per_day) if price_per_day is not None else 0.0,
            price=float(price) if price is not None else 0.0,
            available=bool(data.get("available", True)),
            for_sale=bool(data.get("forSale", float(price) > 0 if price is not None else False)),
            for_rent=bool(data.get("forRent", float(price_per_day) > 0 if price_per_day is not None else False)),
            image_url=data.get("imageUrl", data.get("image_url", "")),
            description=data.get("description", ""),
            car_type=data.get("type", "SEDAN")
        )
    
    def __str__(self):
        return f"{self.year} {self.name} {self.model} - {self.color}"
