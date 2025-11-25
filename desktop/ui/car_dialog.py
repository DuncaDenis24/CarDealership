import os
import sys
from pathlib import Path
from datetime import datetime

# Add the project root to Python path if not already there
project_root = str(Path(__file__).parent.parent.absolute())
if project_root not in sys.path:
    sys.path.append(project_root)

from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                            QLineEdit, QSpinBox, QDoubleSpinBox, 
                            QCheckBox, QPushButton, QFileDialog, 
                            QMessageBox, QComboBox, QGroupBox, QFormLayout)
from PyQt5.QtCore import Qt, QSize, QUrl
from PyQt5.QtGui import QIcon, QPixmap, QImage
from PyQt5.QtNetwork import QNetworkRequest, QNetworkAccessManager, QNetworkReply

from models.car import Car

class CarDialog(QDialog):
    def __init__(self, car: Car = None, parent=None):
        super().__init__(parent)
        self.car = car if car else Car()
        self.setWindowTitle("Add New Car" if not car else "Edit Car")
        self.setModal(True)
        self.network_manager = QNetworkAccessManager(self)
        self.network_manager.finished.connect(self.handle_image_download)
        self.init_ui()
        self.load_car_data()
    
    def init_ui(self):
        main_layout = QHBoxLayout()
        
        # Left side - Image preview
        left_layout = QVBoxLayout()
        self.image_preview = QLabel()
        self.image_preview.setFixedSize(300, 200)
        self.image_preview.setAlignment(Qt.AlignCenter)
        self.image_preview.setStyleSheet("""
            QLabel {
                background-color: #f5f5f5;
                border: 1px solid #ddd;
                border-radius: 4px;
            }
        """)
        left_layout.addWidget(QLabel("Image Preview:"))
        left_layout.addWidget(self.image_preview)
        
        # Image URL
        self.image_edit = QLineEdit()
        self.image_edit.setPlaceholderText("Image URL or local path")
        self.browse_btn = QPushButton("Browse...")
        self.browse_btn.clicked.connect(self.browse_image)
        
        # Connect signal after all UI is set up
        self.image_edit.textChanged.connect(self.update_image_preview)
        
        image_layout = QHBoxLayout()
        image_layout.addWidget(self.image_edit)
        image_layout.addWidget(self.browse_btn)
        left_layout.addLayout(image_layout)
        left_layout.addStretch()
        
        # Right side - Form
        form_layout = QFormLayout()
        form_layout.setSpacing(10)
        
        # Basic Info Group
        basic_group = QGroupBox("Car Information")
        basic_layout = QFormLayout()
        
        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("e.g., Toyota")
        basic_layout.addRow("Brand/Name*:", self.name_edit)
        
        self.model_edit = QLineEdit()
        self.model_edit.setPlaceholderText("e.g., Corolla")
        basic_layout.addRow("Model*:", self.model_edit)
        
        self.license_edit = QLineEdit()
        self.license_edit.setPlaceholderText("e.g., B123ABC")
        basic_layout.addRow("License Plate:", self.license_edit)
        
        self.year_spin = QSpinBox()
        self.year_spin.setRange(1900, 2100)
        self.year_spin.setValue(datetime.now().year)
        basic_layout.addRow("Year*:", self.year_spin)
        
        self.color_edit = QLineEdit()
        self.color_edit.setPlaceholderText("e.g., Red")
        basic_layout.addRow("Color*:", self.color_edit)
        
        # Map between display text and backend format
        self.car_type_mapping = {
            'Sedan': 'SEDAN',
            'SUV': 'SUV',
            'Hatchback': 'HATCHBACK',
            'Pickup Truck': 'PICKUP',
            'Convertible': 'CONVERTIBLE'
        }
        
        self.type_combo = QComboBox()
        self.type_combo.addItems(self.car_type_mapping.keys())
        basic_layout.addRow("Type*:", self.type_combo)
        
        basic_group.setLayout(basic_layout)
        
        # Pricing Group
        price_group = QGroupBox("Pricing & Availability")
        price_layout = QFormLayout()
        
        self.price_spin = QDoubleSpinBox()
        self.price_spin.setRange(0, 10000)
        self.price_spin.setPrefix("$")
        self.price_spin.setDecimals(2)
        self.price_spin.setValue(50.0)
        price_layout.addRow("Daily Rate*:", self.price_spin)
        
        self.sale_price_spin = QDoubleSpinBox()
        self.sale_price_spin.setRange(0, 1000000)
        self.sale_price_spin.setPrefix("$")
        self.sale_price_spin.setDecimals(2)
        price_layout.addRow("Sale Price:", self.sale_price_spin)
        
        self.for_rent_check = QCheckBox("Available for rent")
        self.for_rent_check.setChecked(True)
        price_layout.addRow("", self.for_rent_check)
        
        self.for_sale_check = QCheckBox("Available for sale")
        price_layout.addRow("", self.for_sale_check)
        
        self.available_check = QCheckBox("Currently available")
        self.available_check.setChecked(True)
        price_layout.addRow("", self.available_check)
        
        price_group.setLayout(price_layout)
        
        # Add groups to form
        form_layout.addRow(basic_group)
        form_layout.addRow(price_group)
        
        # Buttons
        btn_layout = QHBoxLayout()
        self.save_btn = QPushButton("Save")
        self.save_btn.clicked.connect(self.accept)
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.clicked.connect(self.reject)
        
        btn_layout.addStretch()
        btn_layout.addWidget(self.save_btn)
        btn_layout.addWidget(self.cancel_btn)
        
        # Create right layout with form and buttons
        right_layout = QVBoxLayout()
        right_layout.addLayout(form_layout)
        right_layout.addStretch()
        right_layout.addLayout(btn_layout)
        
        # Set main layout with left and right sections
        main_layout = QHBoxLayout()
        main_layout.addLayout(left_layout, 1)
        main_layout.addLayout(right_layout, 2)
        
        self.setLayout(main_layout)
        self.setMinimumSize(800, 500)
    
    def browse_image(self):
        """Open a file dialog to select an image file."""
        file_name, _ = QFileDialog.getOpenFileName(
            self, 
            "Select Car Image", 
            "", 
            "Images (*.png *.jpg *.jpeg)"
        )
        if file_name:
            self.image_edit.setText(file_name)
    
    def update_image_preview(self):
        """Update the image preview based on the current image path or URL."""
        if not hasattr(self, 'image_edit') or not hasattr(self, 'image_preview'):
            return
            
        image_source = self.image_edit.text().strip()
        if not image_source:
            self.set_placeholder_image()
            return
            
        if image_source.startswith(('http://', 'https://')):
            # Handle web URL
            self.image_preview.setText("Loading...")
            request = QNetworkRequest(QUrl(image_source))
            request.setHeader(QNetworkRequest.UserAgentHeader, "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
            self.network_manager.get(request)
        else:
            # Handle local file path
            if os.path.exists(image_source):
                try:
                    pixmap = QPixmap(image_source)
                    if not pixmap.isNull():
                        self.set_preview_pixmap(pixmap)
                        return
                except Exception as e:
                    print(f"Error loading image: {e}")
            self.set_placeholder_image()
    
    def set_preview_pixmap(self, pixmap):
        """Set the preview pixmap with proper scaling."""
        pixmap = pixmap.scaled(300, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.image_preview.setPixmap(pixmap)
        self.image_preview.setStyleSheet("""
            QLabel {
                background-color: transparent;
                border: 1px solid #ddd;
                border-radius: 4px;
            }
        """)
    
    def set_placeholder_image(self):
        """Set the placeholder image when no image is available."""
        self.image_preview.setText("No image\npreview\navailable")
        self.image_preview.setStyleSheet("""
            QLabel {
                background-color: #f5f5f5;
                border: 1px solid #ddd;
                border-radius: 4px;
                color: #888;
                font-style: italic;
            }
        """)
        self.image_preview.setAlignment(Qt.AlignCenter)
    
    def handle_image_download(self, reply):
        """Handle the completion of an image download."""
        if reply.error() == QNetworkReply.NoError:
            try:
                data = reply.readAll()
                image = QImage()
                if image.loadFromData(data):
                    pixmap = QPixmap.fromImage(image)
                    self.set_preview_pixmap(pixmap)
                    return
            except Exception as e:
                print(f"Error processing downloaded image: {e}")
        
        # If we get here, there was an error
        self.set_placeholder_image()
        reply.deleteLater()
    
    def load_car_data(self):
        """Load car data into the form fields."""
        if not self.car:
            return

        # Always load basic fields
        self.name_edit.setText(self.car.name)
        self.model_edit.setText(self.car.model)
        self.year_spin.setValue(self.car.year)
        self.color_edit.setText(self.car.color)

        # Handle price_per_day and price
        price_per_day = getattr(self.car, 'price_per_day', 0)
        price = getattr(self.car, 'price', 0)

        self.price_spin.setValue(price_per_day)
        self.sale_price_spin.setValue(price)

        # Handle availability and sale status
        self.available_check.setChecked(getattr(self.car, 'available', False))

        # Handle for_sale status - check if price > 0 or for_sale is explicitly True
        has_price = getattr(self.car, 'price', 0) > 0
        is_for_sale = getattr(self.car, 'for_sale', has_price)
        self.for_sale_check.setChecked(is_for_sale)

        # If for_sale is True but price is 0, set a default price
        if is_for_sale and getattr(self.car, 'price', 0) <= 0:
            self.sale_price_spin.setValue(self.price_spin.value() * 200)

        # Handle for_rent status
        if hasattr(self.car, 'for_rent'):
            self.for_rent_check.setChecked(self.car.for_rent)

        # Handle image URL
        image_url = getattr(self.car, 'image_url', getattr(self.car, 'imageUrl', ''))
        if image_url:
            self.image_edit.setText(image_url)
            
        # Set additional fields if they exist
        if hasattr(self.car, 'license_plate'):
            self.license_edit.setText(self.car.license_plate)

        if hasattr(self.car, 'car_type'):
            # Convert backend type to display text
            display_type = next((k for k, v in self.car_type_mapping.items() if v == self.car.car_type), None)
            if display_type:
                index = self.type_combo.findText(display_type, Qt.MatchFixedString)
                if index >= 0:
                    self.type_combo.setCurrentIndex(index)

        # Update image preview
        self.update_image_preview()
    
    def get_car_data(self):
        """Get the car data from the form fields and update the car object."""
        if not hasattr(self, 'car') or not self.car:
            self.car = Car()

        # Basic info
        self.car.name = self.name_edit.text().strip()
        self.car.model = self.model_edit.text().strip()
        self.car.year = self.year_spin.value()
        self.car.color = self.color_edit.text().strip()
        
        # Handle prices
        self.car.price_per_day = self.price_spin.value()
        sale_price = self.sale_price_spin.value()
        self.car.price = sale_price

        # Handle availability
        self.car.available = self.available_check.isChecked()

        # Handle additional fields
        if hasattr(self.car, 'license_plate'):
            self.car.license_plate = self.license_edit.text().strip()
            
        if hasattr(self.car, 'car_type'):
            # Convert display text to backend type
            display_type = self.type_combo.currentText()
            self.car.car_type = self.car_type_mapping.get(display_type, 'SEDAN')
        
        # Handle for_rent and for_sale status
        self.car.for_rent = self.for_rent_check.isChecked()
        self.car.for_sale = self.for_sale_check.isChecked()
        
        # If for_rent is true but price_per_day is 0, set a default price
        if self.car.for_rent and self.car.price_per_day <= 0:
            self.car.price_per_day = 50.0  # Default daily rate
            self.price_spin.setValue(50.0)
            
        # If for_sale is true but price is 0, set a default price
        if self.car.for_sale and self.car.price <= 0:
            default_price = self.price_spin.value() * 200
            self.car.price = default_price
            self.sale_price_spin.setValue(default_price)

        # Handle image URL
        self.car.image_url = self.image_edit.text().strip()
        
        # Clear description if it exists
        if hasattr(self.car, 'description'):
            self.car.description = ""
            
        return self.car
