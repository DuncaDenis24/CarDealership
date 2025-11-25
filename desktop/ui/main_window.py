import os
import sys
from pathlib import Path
from PyQt5.QtWidgets import QMainWindow, QTabWidget, QMessageBox

# Add the project root to Python path if not already there
project_root = str(Path(__file__).parent.parent.absolute())
if project_root not in sys.path:
    sys.path.append(project_root)

# Now import local modules
from ui.tabs.rentals_tab import RentalsTab
from ui.tabs.purchases_tab import PurchasesTab
from ui.car_management_widget import CarManagementWidget
from services.api_service import ApiService
from services.car_service import CarService

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Car Rental Admin")
        self.setGeometry(100, 100, 1200, 800)
        
        # Initialize API service
        self.api_service = ApiService()
        
        # Create tabs
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)
        
        # Initialize services
        self.car_service = CarService(self.api_service.base_url)
        
        # Add tabs
        self.rentals_tab = RentalsTab(self.api_service)
        self.purchases_tab = PurchasesTab(self.api_service)
        self.car_management_tab = CarManagementWidget(self.car_service)
        
        self.car_management_tab.cars_updated.connect(self.on_cars_updated)
        
        # Add tabs to the tab widget
        self.tabs.addTab(self.rentals_tab, "Rentals")
        self.tabs.addTab(self.purchases_tab, "Purchases")
        self.tabs.addTab(self.car_management_tab, "Car Management")
        
        # Connect tab change signal to refresh cars when switching to Car Management tab
        self.tabs.currentChanged.connect(self.on_tab_changed)
        
    def on_tab_changed(self, index):
        """Handle tab changes and refresh data when switching to the Car Management tab"""
        current_tab = self.tabs.widget(index)
        if current_tab == self.car_management_tab:
            try:
                self.car_management_tab.load_cars()
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Failed to refresh car list: {str(e)}")
    
    def on_cars_updated(self):
        """Handle car updates by refreshing the rentals and purchases tabs"""
        try:
            # Refresh the current tab if it's the car management tab
            current_tab = self.tabs.currentWidget()
            if current_tab == self.car_management_tab:
                self.car_management_tab.load_cars()
                
            # Also refresh rentals and purchases tabs
            if hasattr(self.rentals_tab, 'load_rentals'):
                self.rentals_tab.load_rentals()
            if hasattr(self.purchases_tab, 'load_purchases'):
                self.purchases_tab.load_purchases()
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to refresh data: {str(e)}")