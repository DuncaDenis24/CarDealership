# services/api_service.py
from __future__ import annotations

import json
import os
import sys
import requests
from typing import List, Optional, Dict, Any, TYPE_CHECKING

# Add the project root to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(project_root)

# Now we can use absolute imports
from desktop.models.purchase import Purchase

if TYPE_CHECKING:
    from desktop.models.rental import Rental

class ApiService:
    def __init__(self, base_url: str = "http://localhost:8080"):
        # Ensure base_url doesn't end with /api to avoid double /api in paths
        self.base_url = base_url.rstrip('/')
        if self.base_url.endswith('/api'):
            self.base_url = self.base_url[:-4]
        self.session = requests.Session()
        
    def _make_request(self, method: str, endpoint: str, **kwargs):
        """Helper method to make HTTP requests with error handling."""
        url = f"{self.base_url}{endpoint}"
        try:
            print(f"Making {method} request to {url}")  # Debug log
            if 'json' in kwargs:
                print(f"Request data: {kwargs['json']}")  # Debug log
                
            response = self.session.request(method, url, **kwargs)
            
            # Log response status and content for debugging
            print(f"Response status: {response.status_code}")
            if response.status_code >= 400:  # Log error responses
                print(f"Error response: {response.text}")
                
            response.raise_for_status()
            return response
            
        except requests.exceptions.HTTPError as e:
            error_msg = f"HTTP Error: {e.response.status_code} - {e.response.text}"
            print(f"API request failed: {error_msg}")
            return e.response  # Return the response even on error
            
        except requests.exceptions.RequestException as e:
            error_msg = f"Request failed: {str(e)}"
            print(f"API request failed: {error_msg}")
            return None
    
    # Generic HTTP methods
    def get(self, endpoint: str, **kwargs):
        return self._make_request('GET', endpoint, **kwargs)
        
    def post(self, endpoint: str, data=None, **kwargs):
        if data is not None:
            kwargs['json'] = data
        return self._make_request('POST', endpoint, **kwargs)
        
    def put(self, endpoint: str, data=None, **kwargs):
        if data is not None:
            kwargs['json'] = data
        return self._make_request('PUT', endpoint, **kwargs)
        
    def delete(self, endpoint: str, **kwargs):
        return self._make_request('DELETE', endpoint, **kwargs)
        
    def get_rentals(self) -> List[Rental]:
        """Fetch all rentals from the API."""
        from desktop.models.rental import Rental
        response = self.get("/api/rentals")
        if response and response.status_code == 200:
            return [Rental.from_dict(rental) for rental in response.json()]
        return []
    
    def update_rental_status(self, rental_id: int, status: str) -> bool:
        """Update the status of a rental."""
        try:
            print(f"[API] Updating rental {rental_id} status to {status}")
            
            # Simple PUT request to update status
            url = f"{self.base_url}/api/rentals/{rental_id}/status"
            print(f"[API] Sending status update to: {url}")
            
            response = self.session.put(
                url,
                json={"status": status},
                headers={"Content-Type": "application/json"}
            )
            
            print(f"[API] Status code: {response.status_code}")
            print(f"[API] Response: {response.text}")
            
            return response.status_code == 200
            
        except Exception as e:
            print(f"[API] Error: {str(e)}")
            return False
    
    def get_purchases(self) -> List[Purchase]:
        """Fetch all purchases from the API."""
        try:
            response = self.session.get(f"{self.base_url}/api/purchases")
            response.raise_for_status()
            
            data = response.json()
            
            # Handle different response formats
            purchases_data = []
            
            if isinstance(data, list):
                purchases_data = data
            elif isinstance(data, dict) and '_embedded' in data and 'purchases' in data['_embedded']:
                purchases_data = data['_embedded']['purchases']
            elif isinstance(data, dict) and 'content' in data:
                purchases_data = data['content']
            elif isinstance(data, dict) and 'id' in data:
                purchases_data = [data]
            else:
                return []
            
            if not isinstance(purchases_data, list):
                return []
            
            # Process and validate each purchase
            valid_purchases = []
            for purchase in purchases_data:
                try:
                    if isinstance(purchase, str):
                        purchase = json.loads(purchase)
                    
                    if not isinstance(purchase, dict):
                        continue
                        
                    # Try to extract ID from _links.self.href if not present
                    if 'id' not in purchase and '_links' in purchase and 'self' in purchase['_links']:
                        href = purchase['_links']['self'].get('href', '')
                        if href:
                            purchase_id = href.split('/')[-1]
                            if purchase_id.isdigit():
                                purchase['id'] = int(purchase_id)
                    
                    valid_purchases.append(purchase)
                    
                except (json.JSONDecodeError, Exception):
                    continue
            
            # Create Purchase objects from the valid purchases
            return [Purchase.from_dict(p, self) for p in valid_purchases]
            
        except requests.exceptions.RequestException:
            return []
            
        except Exception:
            return []
    
    def update_purchase_status(self, purchase_id: int, status: str) -> bool:
        """
        Update the status of a purchase.
        
        Args:
            purchase_id: The ID of the purchase to update
            status: The new status (e.g., 'PENDING', 'COMPLETED', 'CANCELLED')
            
        Returns:
            bool: True if the update was successful, False otherwise
        """
        if not purchase_id or purchase_id <= 0:
            print(f"[API] Error: Invalid purchase ID: {purchase_id}")
            return False
            
        if not status or status not in ["PENDING", "COMPLETED", "CANCELLED"]:
            print(f"[API] Error: Invalid status: {status}")
            return False
            
        try:
            print(f"[API] Updating purchase {purchase_id} status to {status}")
            
            # First try with /api/purchases/{id}/status endpoint
            url = f"{self.base_url}/api/purchases/{purchase_id}/status"
            print(f"[API] Sending status update to: {url}")
            
            response = self.session.put(
                url,
                json={"status": status},
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            
            print(f"[API] Status code: {response.status_code}")
            print(f"[API] Response: {response.text}")
            
            if response.status_code == 200:
                return True
                
            # If the first attempt failed, try the full update endpoint as fallback
            print(f"[API] First attempt failed, trying full update endpoint...")
            url = f"{self.base_url}/api/purchases/{purchase_id}"
            
            # First get the current purchase data
            purchase_data = self.get_purchase(purchase_id)
            if not purchase_data:
                print(f"[API] Error: Could not retrieve purchase {purchase_id}")
                return False
                
            # Update the status
            purchase_data['status'] = status
            
            # Send the update
            response = self.session.put(
                url,
                json=purchase_data,
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            
            print(f"[API] Full update status code: {response.status_code}")
            print(f"[API] Full update response: {response.text}")
            
            return response.status_code == 200
            
        except requests.exceptions.RequestException as re:
            print(f"[API] Request error: {str(re)}")
            if hasattr(re, 'response') and re.response is not None:
                print(f"[API] Response status: {re.response.status_code}")
                print(f"[API] Response text: {re.response.text}")
            return False
            
        except Exception as e:
            print(f"[API] Unexpected error: {str(e)}")
            import traceback
            traceback.print_exc()
            return False
    
    def get_car(self, car_id: int) -> Optional[Dict[str, Any]]:
        """Fetch car details by ID from the API."""
        try:
            response = self.session.get(
                f"{self.base_url}/api/cars/{car_id}",
                timeout=10
            )
            if response.status_code == 200:
                return response.json()
            return None
        except Exception as e:
            print(f"Error fetching car details: {e}")
            return None
            
    # Rental methods
    def get_rental(self, rental_id: int) -> Optional[Dict[str, Any]]:
        """Fetch a single rental by ID from the API."""
        try:
            response = self.get(f"/api/rentals/{rental_id}")
            if response and response.status_code == 200:
                return response.json()
            return None
        except Exception as e:
            print(f"Error fetching rental {rental_id}: {e}")
            return None
            
    def create_rental(self, rental_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Create a new rental."""
        try:
            response = self.post("/api/rentals", data=rental_data)
            if response and response.status_code == 201:
                return response.json()
            return None
        except Exception as e:
            print(f"Error creating rental: {e}")
            return None
            
    def update_rental(self, rental_id: int, rental_data: Dict[str, Any]) -> bool:
        """Update an existing rental."""
        try:
            response = self.put(f"/api/rentals/{rental_id}", data=rental_data)
            return response is not None and response.status_code == 200
        except Exception as e:
            print(f"Error updating rental {rental_id}: {e}")
            return False
            
    def delete_rental(self, rental_id: int) -> bool:
        """Delete a rental by ID."""
        try:
            response = self.delete(f"/api/rentals/{rental_id}")
            return response is not None and response.status_code == 204
        except Exception as e:
            print(f"Error deleting rental {rental_id}: {e}")
            return False
            
    # Purchase methods
    def get_purchase(self, purchase_id: int) -> Optional[Dict[str, Any]]:
        """Fetch a single purchase by ID from the API."""
        try:
            response = self.get(f"/api/purchases/{purchase_id}")
            if response and response.status_code == 200:
                return response.json()
            return None
        except Exception as e:
            print(f"Error fetching purchase {purchase_id}: {e}")
            return None
            
    def create_purchase(self, purchase_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Create a new purchase."""
        try:
            response = self.post("/api/purchases", data=purchase_data)
            if response and response.status_code == 201:
                return response.json()
            return None
        except Exception as e:
            print(f"Error creating purchase: {e}")
            return None
            
    def update_purchase(self, purchase_id: int, purchase_data: Dict[str, Any]) -> bool:
        """Update an existing purchase."""
        try:
            response = self.put(f"/api/purchases/{purchase_id}", data=purchase_data)
            return response is not None and response.status_code == 200
        except Exception as e:
            print(f"Error updating purchase {purchase_id}: {e}")
            return False
            
    def delete_purchase(self, purchase_id: int) -> bool:
        """Delete a purchase by ID."""
        try:
            response = self.delete(f"/api/purchases/{purchase_id}")
            return response is not None and response.status_code == 204
        except Exception as e:
            print(f"Error deleting purchase {purchase_id}: {e}")
            return False