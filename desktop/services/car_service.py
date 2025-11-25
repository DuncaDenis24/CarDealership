import os
import sys
from pathlib import Path

# Add the project root to Python path if not already there
project_root = str(Path(__file__).parent.parent.absolute())
if project_root not in sys.path:
    sys.path.append(project_root)

import requests
from typing import List, Optional
from models.car import Car
from services.api_service import ApiService

class CarService:
    def __init__(self, base_url: str):
        self.base_url = f"{base_url}/api/cars"
        self.api_service = ApiService(base_url)
    
    def get_all_cars(self) -> List[Car]:
        """Get all cars from the API"""
        response = self.api_service.get("/api/cars")
        if response and response.status_code == 200:
            return [Car.from_dict(car_data) for car_data in response.json()]
        return []
    
    def get_car_by_id(self, car_id: int) -> Optional[Car]:
        """Get a single car by ID"""
        response = self.api_service.get(f"/api/cars/{car_id}")
        if response and response.status_code == 200:
            return Car.from_dict(response.json())
        return None
    
    def create_car(self, car: Car) -> Optional[Car]:
        """Create a new car"""
        try:
            car_data = car.to_dict()
            print(f"Sending car data to API: {car_data}")  # Debug log
            
            response = self.api_service.post("/api/cars", data=car_data)
            
            if response is None:
                print("Failed to get response from API")
                return None
                
            print(f"API Response Status: {response.status_code}")
            if response.status_code in (200, 201):  # Accept both 200 and 201 as success
                try:
                    car_data = response.json()
                    print(f"Successfully created car: {car_data}")
                    return Car.from_dict(car_data)
                except Exception as e:
                    print(f"Error parsing response: {str(e)}")
                    return None
            else:
                print(f"API Error: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            print(f"Error in create_car: {str(e)}")
            return None
    
    def update_car(self, car: Car) -> Optional[Car]:
        """Update an existing car"""
        if not car.id:
            return None
            
        response = self.api_service.put(f"/api/cars/{car.id}", data=car.to_dict())
        if response and response.status_code == 200:
            return Car.from_dict(response.json())
        return None
    
    def delete_car(self, car_id: int) -> bool:
        """Delete a car by ID"""
        try:
            print(f"Attempting to delete car with ID: {car_id}")
            response = self.api_service.delete(f"/api/cars/{car_id}")
            
            if response is None:
                print("No response received from server")
                return False
                
            print(f"Delete response status: {response.status_code}")
            # Consider both 200 (OK) and 204 (No Content) as success
            if response.status_code in (200, 204):
                print(f"Successfully deleted car with ID: {car_id}")
                return True
            else:
                print(f"Failed to delete car. Status: {response.status_code}, Response: {response.text}")
                return False
                
        except Exception as e:
            print(f"Error in delete_car: {str(e)}")
            return False
