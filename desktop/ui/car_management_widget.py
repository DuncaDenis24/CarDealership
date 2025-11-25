import os
import sys
from pathlib import Path

# Add the project root to Python path if not already there
project_root = str(Path(__file__).parent.parent.absolute())
if project_root not in sys.path:
    sys.path.append(project_root)

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                            QLabel, QLineEdit, QGridLayout, QMessageBox, QFrame, 
                            QInputDialog, QScrollArea, QTableWidget, QTableWidgetItem, 
                            QHeaderView, QAbstractItemView, QDialog)
from PyQt5.QtGui import QPixmap, QIcon, QFont, QImage, QPainter, QColor
from PyQt5.QtCore import Qt, pyqtSignal, QSize, QUrl
from PyQt5.QtNetwork import QNetworkRequest, QNetworkAccessManager, QNetworkReply

from models.car import Car
from ui.car_dialog import CarDialog

class CarManagementWidget(QWidget):
    cars_updated = pyqtSignal()
    
    def __init__(self, car_service, parent=None):
        super().__init__(parent)
        self.car_service = car_service
        self.network_manager = QNetworkAccessManager(self)
        self.network_manager.finished.connect(self.handle_image_download)
        self.image_requests = {}
        self.init_ui()
        self.load_cars()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Search and Add Car row
        search_layout = QHBoxLayout()
        
        # Search bar
        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("Search cars...")
        self.search_edit.setClearButtonEnabled(True)
        self.search_edit.textChanged.connect(self.filter_cars)
        
        # Add Car button
        self.add_btn = QPushButton("Add Car")
        self.add_btn.setIcon(QIcon.fromTheme("list-add"))
        self.add_btn.setFixedSize(100, 30)
        self.add_btn.clicked.connect(self.add_car)
        
        search_layout.addWidget(QLabel("Search:"))
        search_layout.addWidget(self.search_edit)
        search_layout.addStretch()
        search_layout.addWidget(self.add_btn)
        
        # Scroll area for car cards
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        
        # Container widget for car cards
        self.cards_container = QWidget()
        self.cards_layout = QGridLayout(self.cards_container)
        self.cards_layout.setSpacing(20)
        self.cards_layout.setContentsMargins(20, 20, 20, 20)
        
        # Add a stretch to push cards to the top
        self.cards_layout.setRowStretch(100, 1)
        
        self.scroll_area.setWidget(self.cards_container)
        
        # Add to main layout
        layout.addLayout(search_layout)
        layout.addWidget(self.scroll_area)
        
        self.setLayout(layout)
    
    def create_car_card(self, car, row, col):
        # Create card frame
        card = QFrame()
        card.setFrameShape(QFrame.StyledPanel)
        card.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 8px;
                border: 1px solid #e0e0e0;
            }
            QFrame:hover {
                border: 1px solid #2196F3;
                background-color: #f5f9ff;
            }
        """)
        
        card_layout = QVBoxLayout(card)
        
        # Car name and model as title
        title = QLabel(f"<h3 style='margin: 0;'>{car.year} {car.name} {car.model}</h3>")
        title.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(title)
        
        # Car image
        image_label = QLabel()
        image_label.setObjectName("imageLabel")
        image_label.setAlignment(Qt.AlignCenter)
        
        # Store reference to the image label
        image_label.setProperty('car_id', getattr(car, 'id', 0))
        
        # Load and scale the image if available
        image_url = getattr(car, 'image_url', getattr(car, 'imageUrl', ''))
        if image_url:
            if image_url.startswith(('http://', 'https://')):
                # Use QNetworkAccessManager for web requests
                request = QNetworkRequest(QUrl(image_url))
                # Set a user agent to avoid 403 errors
                request.setHeader(QNetworkRequest.UserAgentHeader, "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
                
                # Store the request with the image label reference
                reply = self.network_manager.get(request)
                self.image_requests[reply] = (image_label, image_url)
                
                # Show placeholder while loading
                image_label.setText("Loading...")
            else:
                # For local files
                if os.path.exists(image_url):
                    pixmap = QPixmap(image_url)
                    if not pixmap.isNull():
                        pixmap = pixmap.scaled(240, 160, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                        image_label.setPixmap(pixmap)
                    else:
                        image_label.setText("Invalid Image")
                else:
                    image_label.setText("Image not found")
        else:
            image_label.setText("No Image")
        
        image_label.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(image_label)
        
        # Get the correct price values
        price_per_day = getattr(car, 'price_per_day', getattr(car, 'dailyRate', 0))
        purchase_price = getattr(car, 'price', price_per_day * 200)
        
        # Get status color and text
        status_color = '#4CAF50' if getattr(car, 'available', False) else '#F44336'
        status_text = 'Available' if getattr(car, 'available', False) else 'Not Available'
        
        # Create details text
        details_text = f"""
            <div style='margin: 5px 0;'>
                <p style='margin: 4px 0;'><b>Color:</b> {getattr(car, 'color', 'N/A')}</p>
                <p style='margin: 4px 0;'><b>Rental Price:</b> ${price_per_day:.2f}/day</p>
                <p style='margin: 4px 0;'><b>Purchase Price:</b> ${purchase_price:.2f}</p>
                <p style='margin: 4px 0;'><b>Status:</b> <span style='color: {status_color};'>{status_text}</span></p>
            </div>
        """
        # Create details label with all information
        details_label = QLabel(details_text)
        details_label.setWordWrap(True)
        card_layout.addWidget(details_label)
        
        # Action buttons
        btn_layout = QHBoxLayout()
        
        edit_btn = QPushButton("Edit")
        edit_btn.setIcon(QIcon.fromTheme("document-edit"))
        edit_btn.clicked.connect(lambda: self.edit_car(car))
        
        delete_btn = QPushButton("Delete")
        delete_btn.setIcon(QIcon.fromTheme("edit-delete"))
        delete_btn.clicked.connect(lambda: self.delete_car(car))
        
        btn_layout.addWidget(edit_btn)
        btn_layout.addWidget(delete_btn)
        
        # Add button layout to card layout
        card_layout.addLayout(btn_layout)
        
        # Add to grid
        self.cards_layout.addWidget(card, row, col)
        
        return card
        
    def handle_image_download(self, reply):
        """Handle the completion of an image download"""
        try:
            # Get the image label that requested this download
            image_label, image_url = self.image_requests.get(reply, (None, None))
            
            # Check if the label still exists and is valid
            if not image_label or not hasattr(image_label, 'setPixmap'):
                print(f"Image label no longer exists for URL: {image_url}")
                return
                
            if reply.error() == QNetworkReply.NoError:
                try:
                    # Read the image data
                    data = reply.readAll()
                    if data:
                        image = QImage()
                        if image.loadFromData(data):
                            pixmap = QPixmap.fromImage(image)
                            if not pixmap.isNull():
                                pixmap = pixmap.scaled(240, 160, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                                try:
                                    image_label.setPixmap(pixmap)
                                except RuntimeError:
                                    print("Failed to set pixmap - widget was deleted")
                                    return
                            else:
                                self.safe_set_text(image_label, "Invalid Image")
                        else:
                            self.safe_set_text(image_label, "Invalid Image Data")
                    else:
                        self.safe_set_text(image_label, "No Image Data")
                except Exception as e:
                    print(f"Error processing image: {e}")
                    self.safe_set_text(image_label, "Error")
            else:
                # Handle network error
                self.safe_set_text(image_label, "Load Failed")
        except Exception as e:
            print(f"Unexpected error in handle_image_download: {e}")
        finally:
            # Clean up
            if reply in self.image_requests:
                del self.image_requests[reply]
            reply.deleteLater()
    
    def safe_set_text(self, label, text):
        """Safely set text on a QLabel, handling the case where it might be deleted"""
        try:
            if label and hasattr(label, 'setText'):
                label.setText(text)
        except RuntimeError:
            # The C++ object has been deleted
            pass
    
    def filter_cars(self):
        try:
            search_text = self.search_edit.text().strip().lower()
            
            # Clear existing cards
            while self.cards_layout.count() > 0:
                item = self.cards_layout.takeAt(0)
                if item.widget():
                    item.widget().deleteLater()
            
            if not hasattr(self, 'all_cars') or not self.all_cars:
                return
            
            # Show matching cars
            row = col = 0
            for car in self.all_cars:
                if not search_text or any([
                    search_text in getattr(car, 'name', '').lower(),
                    search_text in getattr(car, 'model', '').lower(),
                    search_text in getattr(car, 'color', '').lower(),
                    search_text in str(getattr(car, 'year', '')),
                    search_text in str(getattr(car, 'license_plate', '')).lower(),
                    search_text in str(getattr(car, 'licensePlate', '')).lower()
                ]):
                    self.create_car_card(car, row, col)
                    col += 1
                    if col >= 3:  # 3 cards per row
                        col = 0
                        row += 1
        except Exception as e:
            QMessageBox.warning(self, "Search Error", f"Error filtering cars: {str(e)}")
    
    def load_cars(self):
        self.all_cars = self.car_service.get_all_cars()
        self.filter_cars()  # This will create and display the cards
    
    def get_selected_car(self):
        return None  # Not used in card-based UI
    
    def on_selection_changed(self):
        pass  # Not used in card-based UI
    
    def add_car(self):
        dialog = CarDialog()
        if dialog.exec_() == QDialog.Accepted:
            try:
                car = dialog.get_car_data()
                print("Car data before sending to API:", car.__dict__)  # Debug log
                
                result = self.car_service.create_car(car)
                
                if result:
                    print("Car created successfully:", result.__dict__)  # Debug log
                    self.load_cars()
                    self.cars_updated.emit()
                    QMessageBox.information(self, "Success", "Car added successfully!")
                else:
                    error_msg = "Failed to add car. Please check the console for more details."
                    print(error_msg)
                    QMessageBox.warning(self, "Error", error_msg)
                    
            except Exception as e:
                error_msg = f"An error occurred while adding the car: {str(e)}"
                print(error_msg)
                QMessageBox.critical(self, "Error", error_msg)
    
    def edit_car(self, car):
        dialog = CarDialog(car, self)
        if dialog.exec_() == QDialog.Accepted:
            updated_car = dialog.get_car_data()
            result = self.car_service.update_car(updated_car)
            if result:
                self.load_cars()
                self.cars_updated.emit()
                QMessageBox.information(self, "Success", "Car updated successfully!")
            else:
                QMessageBox.warning(self, "Error", "Failed to update car.")
    
    def delete_car(self, car):
        if not car or not car.id:
            return
            
        reply = QMessageBox.question(
            self, 
            "Confirm Delete",
            f"Are you sure you want to delete {car.name} {car.model}?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            if self.car_service.delete_car(car.id):
                self.load_cars()
                self.cars_updated.emit()
                QMessageBox.information(self, "Success", "Car deleted successfully!")
            else:
                QMessageBox.warning(self, "Error", "Failed to delete car.")
