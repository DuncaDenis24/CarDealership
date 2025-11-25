# models/rental.py
from dataclasses import dataclass, field
from typing import Dict, Any, Optional
import json

@dataclass
class Rental:
    id: int = 0
    customer_name: str = ""
    customer_email: str = ""
    customerName: str = field(init=False, repr=False)
    customerEmail: str = field(init=False, repr=False)
    car: Dict[str, Any] = field(default_factory=dict)
    start_date: str = ""
    end_date: str = ""
    startDate: str = field(init=False, repr=False)
    endDate: str = field(init=False, repr=False)
    status: str = "PENDING"
    total_price: float = 0.0
    totalPrice: float = field(init=False, repr=False)
    created_at: str = ""
    createdAt: str = field(init=False, repr=False)
    
    def __post_init__(self):
        """Handle both snake_case and camelCase field names."""
        # Handle camelCase to snake_case
        if hasattr(self, 'customerName'):
            self.customer_name = getattr(self, 'customerName', self.customer_name)
        if hasattr(self, 'customerEmail'):
            self.customer_email = getattr(self, 'customerEmail', self.customer_email)
        if hasattr(self, 'startDate'):
            self.start_date = getattr(self, 'startDate', self.start_date)
        if hasattr(self, 'endDate'):
            self.end_date = getattr(self, 'endDate', self.end_date)
        if hasattr(self, 'totalPrice'):
            self.total_price = float(getattr(self, 'totalPrice', self.total_price))
        if hasattr(self, 'createdAt'):
            self.created_at = getattr(self, 'createdAt', self.created_at)
    
    @property
    def car_name(self) -> str:
        if not self.car:
            return ""
        if isinstance(self.car, dict):
            name = self.car.get('name', '')
            model = self.car.get('model', '')
        else:
            name = getattr(self.car, 'name', '')
            model = getattr(self.car, 'model', '')
        return f"{name} {model}".strip()
    
    @property
    def formatted_date(self) -> str:
        return f"{self.start_date} to {self.end_date}"
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Rental':
        """Create a Rental instance from a dictionary."""
        return cls(**{
            'id': data.get('id', 0),
            'customer_name': data.get('customerName', data.get('customer_name', '')),
            'customer_email': data.get('customerEmail', data.get('customer_email', '')),
            'car': data.get('car', {}),
            'start_date': data.get('startDate', data.get('start_date', '')),
            'end_date': data.get('endDate', data.get('end_date', '')),
            'status': data.get('status', 'PENDING'),
            'total_price': float(data.get('totalPrice', data.get('total_price', 0.0))),
            'created_at': data.get('createdAt', data.get('created_at', ''))
        })
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary with camelCase keys for JSON serialization."""
        return {
            'id': self.id,
            'customerName': self.customer_name,
            'customerEmail': self.customer_email,
            'car': self.car,
            'startDate': self.start_date,
            'endDate': self.end_date,
            'status': self.status,
            'totalPrice': self.total_price,
            'createdAt': self.created_at
        }
    
    def __str__(self) -> str:
        return f"Rental(id={self.id}, customer='{self.customer_name}', car='{self.car_name}', status='{self.status}')"