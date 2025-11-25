# models/purchase.py
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Any, Optional, Union, TYPE_CHECKING
import json

if TYPE_CHECKING:
    from services.api_service import ApiService  # only for type hints
@dataclass
class Purchase:
    id: int = 0
    customer_name: str = ""
    customer_email: str = ""
    customer_phone: str = ""
    customer_address: str = ""
    car: Dict[str, Any] = field(default_factory=dict)
    purchase_date: str = ""
    status: str = "PENDING"
    payment_method: str = ""
    purchase_price: float = 0.0
    total_amount: float = 0.0
    created_at: str = ""
    
    # Add camelCase fields for API compatibility
    customerName: str = field(init=False, repr=False)
    customerEmail: str = field(init=False, repr=False)
    customerPhone: str = field(init=False, repr=False)
    customerAddress: str = field(init=False, repr=False)
    purchaseDate: str = field(init=False, repr=False)
    paymentMethod: str = field(init=False, repr=False)
    purchasePrice: float = field(init=False, repr=False)
    totalAmount: float = field(init=False, repr=False)
    createdAt: str = field(init=False, repr=False)
    carId: int = field(init=False, repr=False, default=0)
    _car: Dict[str, Any] = field(init=False, repr=False, default_factory=dict)
    _api_service: Optional[ApiService] = field(init=False, repr=False, default=None)
    
    @property
    def car_name(self) -> str:
        """Get the car name from the car dictionary."""
        if not self.car:
            # If no car data but we have a car_id, try to fetch it
            if self.car_id and self._api_service:
                self._fetch_car_details()
            return ""
        
        if isinstance(self.car, dict):
            name = self.car.get('name', '')
            model = self.car.get('model', '')
        else:
            name = getattr(self.car, 'name', '')
            model = getattr(self.car, 'model', '')
        
        result = f"{name} {model}".strip()
        
        # If still empty and we have a car_id, try to fetch
        if not result and self.car_id and self._api_service:
            self._fetch_car_details()
            # Retry getting name and model after fetching
            if self._car:
                if isinstance(self._car, dict):
                    name = self._car.get('name', '')
                    model = self._car.get('model', '')
                else:
                    name = getattr(self._car, 'name', '')
                    model = getattr(self._car, 'model', '')
                result = f"{name} {model}".strip()
        
        return result
    
    def __post_init__(self):
        """Handle both snake_case and camelCase field names."""
        # Initialize all fields with empty/default values if not already set
        if not hasattr(self, 'customer_name'): self.customer_name = ""
        if not hasattr(self, 'customer_email'): self.customer_email = ""
        if not hasattr(self, 'customer_phone'): self.customer_phone = ""
        if not hasattr(self, 'customer_address'): self.customer_address = ""
        if not hasattr(self, 'purchase_date'): self.purchase_date = ""
        if not hasattr(self, 'payment_method'): self.payment_method = ""
        if not hasattr(self, 'purchase_price'): self.purchase_price = 0.0
        if not hasattr(self, 'total_amount'): self.total_amount = 0.0
        if not hasattr(self, 'created_at'): self.created_at = ""
        if not hasattr(self, 'car_id'): self.car_id = 0

        # Handle camelCase to snake case
        if hasattr(self, 'customerName'):
            self.customer_name = getattr(self, 'customerName')
        if hasattr(self, 'customerEmail'):
            self.customer_email = getattr(self, 'customerEmail')
        if hasattr(self, 'customerPhone'):
            self.customer_phone = getattr(self, 'customerPhone')
        if hasattr(self, 'customerAddress'):
            self.customer_address = getattr(self, 'customerAddress')
        if hasattr(self, 'purchaseDate'):
            self.purchase_date = getattr(self, 'purchaseDate')
        if hasattr(self, 'paymentMethod'):
            self.payment_method = getattr(self, 'paymentMethod')
        if hasattr(self, 'purchasePrice'):
            self.purchase_price = float(getattr(self, 'purchasePrice'))
        if hasattr(self, 'totalAmount'):
            self.total_amount = float(getattr(self, 'totalAmount'))
        if hasattr(self, 'createdAt'):
            self.created_at = getattr(self, 'createdAt')
        if hasattr(self, 'carId'):
            self.car_id = getattr(self, 'carId')
            
        # If total_amount is not set but purchase_price is, use purchase_price
        if not self.total_amount and self.purchase_price:
            self.total_amount = self.purchase_price
            
        # If we have a car_id but no car data, try to get it from the car field
        if (self.car_id and (not hasattr(self, 'car') or not self.car) and 
            hasattr(self, '_api_service') and self._api_service):
            self._fetch_car_details()
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any], api_service: Optional[ApiService] = None) -> 'Purchase':
        """Create a Purchase object from a dictionary."""
        instance = cls()
        
        if api_service:
            instance._api_service = api_service
        
        field_mapping = {
            'id': 'id',
            'customerName': 'customer_name',
            'customerEmail': 'customer_email',
            'customerPhone': 'customer_phone',
            'customerAddress': 'customer_address',
            'purchaseDate': 'purchase_date',
            'paymentMethod': 'payment_method',
            'purchasePrice': 'purchase_price',
            'totalAmount': 'total_amount',
            'createdAt': 'created_at',
            'carId': 'car_id',
            'status': 'status'
        }
        
        for key, value in data.items():
            if value is None:
                continue
                
            if key == 'car' and value:
                if isinstance(value, dict) and 'id' in value:
                    instance.car = value
                    instance.car_id = value['id']
                elif isinstance(value, int):
                    instance.car_id = value
                continue
                
            if key in field_mapping:
                target_field = field_mapping[key]
                if key == 'id' and value is not None:
                    try:
                        value = int(value) if str(value).strip() else 0
                    except (ValueError, TypeError):
                        value = 0
                setattr(instance, target_field, value)
            else:
                setattr(instance, key, value)
                
        if hasattr(instance, 'car') and instance.car and 'id' in instance.car and not instance.car_id:
            instance.car_id = instance.car['id']
        
        # If we have a car_id but no car data, and we have an API service, fetch the car details
        if instance.car_id and (not hasattr(instance, '_car') or not instance._car) and api_service:
            instance._fetch_car_details()
        
        # Format payment method if it exists
        if hasattr(instance, 'payment_method') and instance.payment_method:
            instance.payment_method = str(instance.payment_method).replace('_', ' ').title()
        
        # Call post_init to handle field mapping
        instance.__post_init__()
        
        return instance
    
    def set_api_service(self, api_service: ApiService):
        """Set the API service for fetching car details."""
        self._api_service = api_service
        if self.car_id and not self._car:
            self._fetch_car_details()
    
    def _fetch_car_details(self):
        """Fetch car details from the API using the car ID."""
        if not self.car_id or not self._api_service:
            return
            
        try:
            car_data = self._api_service.get_car(self.car_id)
            if car_data:
                self._car = car_data
        except Exception as e:
            print(f"Error fetching car details: {e}")
    
    def __str__(self) -> str:
        return f"Purchase(id={self.id}, customer='{self.customer_name}', car='{self.car_name}', amount=${self.total_amount:.2f}, status='{self.status}')"