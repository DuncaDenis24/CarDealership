from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, 
                            QTableWidgetItem, QPushButton, QHeaderView,
                            QMessageBox, QAbstractItemView, QApplication)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QColor

class RentalsTab(QWidget):
    def __init__(self, api_service):
        super().__init__()
        self.api_service = api_service
        self.init_ui()
        self.load_rentals()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # Buttons
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)  # Add some spacing between buttons
        
        # Create buttons with icons and text
        self.refresh_btn = QPushButton("Refresh")
        self.approve_btn = QPushButton("✅ Approve")
        self.reject_btn = QPushButton("Reject")
        
        # Set fixed size for buttons
        for btn in [self.refresh_btn, self.approve_btn, self.reject_btn]:
            btn.setMinimumWidth(120)
            btn.setMinimumHeight(40)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #4CAF50;
                    color: white;
                    border: none;
                    border-radius: 4px;
                    padding: 8px 16px;
                    font-size: 14px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #45a049;
                }
                QPushButton:disabled {
                    background-color: #cccccc;
                    color: #666666;
                }
                QPushButton#reject_btn {
                    background-color: #f44336;
                }
                QPushButton#reject_btn:hover {
                    background-color: #d32f2f;
                }
                QPushButton#refresh_btn {
                    background-color: #2196F3;
                }
                QPushButton#refresh_btn:hover {
                    background-color: #0b7dda;
                }
            """)
        
        # Set object names for styling
        self.refresh_btn.setObjectName("refresh_btn")
        self.approve_btn.setObjectName("approve_btn")
        self.reject_btn.setObjectName("reject_btn")
        
        # Set button tooltips
        self.refresh_btn.setToolTip("Refresh the rentals list")
        self.approve_btn.setToolTip("Approve the selected rental")
        self.reject_btn.setToolTip("Reject the selected rental")
        
        # Disable action buttons by default (until a row is selected)
        self.approve_btn.setEnabled(False)
        self.reject_btn.setEnabled(False)
        
        btn_layout.addWidget(self.refresh_btn)
        btn_layout.addWidget(self.approve_btn)
        btn_layout.addWidget(self.reject_btn)
        
        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "ID", "Customer", "Car", "Period", "Status", "Total Price"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        # Connect selection change event
        self.table.itemSelectionChanged.connect(self.on_selection_changed)
        
        # Connect buttons
        self.refresh_btn.clicked.connect(self.load_rentals)
        self.approve_btn.clicked.connect(self.approve_rental)
        self.reject_btn.clicked.connect(self.reject_rental)
        
        # Create a container widget for the buttons
        button_container = QWidget()
        button_container.setLayout(btn_layout)
        
        # Add some margin around the buttons
        button_container.setStyleSheet("""
            QWidget {
                background-color: #f5f5f5;
                padding: 10px;
                border-bottom: 1px solid #e0e0e0;
            }
        """)
        
        # Add widgets to main layout with stretch factors
        layout.addWidget(button_container, 0)  # Buttons at the top, don't stretch
        layout.addWidget(self.table, 1)        # Table takes remaining space
        
        # Set layout margins and spacing
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
    
    def load_rentals(self):
        try:
            # Show loading state
            self.refresh_btn.setEnabled(False)
            self.refresh_btn.setText("Loading...")
            
            # Force UI update
            QApplication.processEvents()
            
            rentals = self.api_service.get_rentals()
            self.table.setRowCount(len(rentals))
            
            for row, rental in enumerate(rentals):
                self.table.setItem(row, 0, QTableWidgetItem(str(rental.id)))
                self.table.setItem(row, 1, QTableWidgetItem(rental.customer_name))
                self.table.setItem(row, 2, QTableWidgetItem(rental.car_name))
                self.table.setItem(row, 3, QTableWidgetItem(rental.formatted_date))
                
                # Status with color coding
                status_item = QTableWidgetItem(rental.status)
                if rental.status == "APPROVED":
                    status_item.setBackground(QColor(200, 255, 200))  # Light green
                elif rental.status == "REJECTED":
                    status_item.setBackground(QColor(255, 200, 200))  # Light red
                self.table.setItem(row, 4, status_item)
                
                self.table.setItem(row, 5, QTableWidgetItem(f"${rental.total_price:.2f}"))
                
            # Auto-resize rows to content
            self.table.resizeRowsToContents()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load rentals: {str(e)}")
        finally:
            # Reset button state
            self.refresh_btn.setEnabled(True)
            self.refresh_btn.setText("Refresh")
    
    def approve_rental(self):
        self._update_rental_status("APPROVED")
    
    def reject_rental(self):
        self._update_rental_status("REJECTED")
    
    def on_selection_changed(self):
        """Enable/disable action buttons based on selection and rental status"""
        # Disable all buttons by default
        self.approve_btn.setEnabled(False)
        self.reject_btn.setEnabled(False)
        
        # Get selected items
        selected = self.table.selectedItems()
        if not selected:
            return
            
        # Get the status of the selected rental
        row = selected[0].row()
        status_item = self.table.item(row, 4)  # Status is in column 4
        
        # Only enable buttons if status is PENDING
        if status_item and status_item.text() == "PENDING":
            self.approve_btn.setEnabled(True)
            self.reject_btn.setEnabled(True)
    
    def _update_rental_status(self, status: str):
        """Update the status of the selected rental"""
        selected = self.table.selectedItems()
        if not selected:
            QMessageBox.warning(self, "No Selection", "Please select a rental to update.")
            return
        
        try:
            row = selected[0].row()
            rental_id = int(self.table.item(row, 0).text())
            current_status = self.table.item(row, 4).text()
            
            # Don't allow updating if already in a final state
            if current_status in ["APPROVED", "REJECTED"]:
                QMessageBox.warning(self, "Cannot Update", "This rental has already been processed.")
                return
                
            # Show confirmation dialog
            confirm = QMessageBox.question(
                self,
                "Confirm Action",
                f"Are you sure you want to {status.lower()} this rental?",
                QMessageBox.Yes | QMessageBox.No
            )
            
            if confirm == QMessageBox.Yes:
                # Disable buttons during update
                self.approve_btn.setEnabled(False)
                self.reject_btn.setEnabled(False)
                
                # Show processing state
                processing_msg = QMessageBox(
                    QMessageBox.Information,
                    "Processing",
                    f"Updating rental status to {status}...",
                    QMessageBox.NoButton,
                    self
                )
                processing_msg.setWindowModality(Qt.WindowModal)
                processing_msg.show()
                
                # Force UI update
                QApplication.processEvents()
                
                # Perform the update
                if self.api_service.update_rental_status(rental_id, status):
                    # Close processing message and refresh data
                    processing_msg.close()
                    self.load_rentals()
                    QMessageBox.information(self, "Success", f"Rental {status.lower()}d successfully!")
                else:
                    processing_msg.close()
                    QMessageBox.warning(self, "Update Failed", "Failed to update rental status. Please try again.")
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to update rental status: {str(e)}")
        finally:
            # Re-enable buttons
            self.on_selection_changed()