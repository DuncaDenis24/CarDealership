import requests
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, 
                            QTableWidgetItem, QPushButton, QHeaderView,
                            QMessageBox, QAbstractItemView, QApplication)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QColor

class PurchasesTab(QWidget):
    def __init__(self, api_service):
        super().__init__()
        self.api_service = api_service
        self.init_ui()
        self.load_purchases()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # Buttons
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)  # Add some spacing between buttons
        
        # Create buttons with icons and text
        self.refresh_btn = QPushButton("Refresh")
        self.complete_btn = QPushButton("✅ Complete")
        self.cancel_btn = QPushButton("Cancel")
        
        # Set fixed size for buttons
        for btn in [self.refresh_btn, self.complete_btn, self.cancel_btn]:
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
                QPushButton#cancel_btn {
                    background-color: #f44336;
                }
                QPushButton#cancel_btn:hover {
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
        self.complete_btn.setObjectName("complete_btn")
        self.cancel_btn.setObjectName("cancel_btn")
        
        # Set button tooltips
        self.refresh_btn.setToolTip("Refresh the purchases list")
        self.complete_btn.setToolTip("Mark the selected purchase as completed")
        self.cancel_btn.setToolTip("Cancel the selected purchase")
        
        # Disable action buttons by default (until a row is selected)
        self.complete_btn.setEnabled(False)
        self.cancel_btn.setEnabled(False)
        
        btn_layout.addWidget(self.refresh_btn)
        btn_layout.addWidget(self.complete_btn)
        btn_layout.addWidget(self.cancel_btn)
        
        # Table
        self.table = QTableWidget()
        # Show full purchase fields in a clear order to match backend model
        # Columns: ID, Customer, Email, Phone, Address, Car, Purchase Date, Payment Method, Status, Purchase Price
        self.table.setColumnCount(10)
        self.table.setHorizontalHeaderLabels([
            "ID", "Customer", "Email", "Phone", "Address", "Car", "Purchase Date", "Payment Method", "Status", "Purchase Price"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        
        # Connect selection change event
        self.table.itemSelectionChanged.connect(self.on_selection_changed)
        
        # Connect buttons
        self.refresh_btn.clicked.connect(self.load_purchases)
        self.complete_btn.clicked.connect(self.complete_purchase)
        self.cancel_btn.clicked.connect(self.cancel_purchase)
        
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
    
    def load_purchases(self):
        try:
            # Show loading state
            self.refresh_btn.setEnabled(False)
            self.refresh_btn.setText("Loading...")
            
            # Force UI update
            QApplication.processEvents()
            
            # Debug: Print the API URL being called
            print(f"Fetching purchases from: {self.api_service.base_url}/purchases")
            
            purchases = self.api_service.get_purchases()
            print(f"Received {len(purchases)} purchases from API")
            
            if not purchases:
                QMessageBox.information(self, "No Purchases", "No purchases found in the database.")
            
            self.table.setRowCount(len(purchases))
            
            for row, purchase in enumerate(purchases):
                try:
                    print(f"Processing purchase {row + 1}/{len(purchases)}: {purchase}")
                    print(f"Purchase data: {purchase.__dict__}")
                    
                    # ID
                    # Fill columns matching headers
                    self.table.setItem(row, 0, QTableWidgetItem(str(purchase.id)))
                    self.table.setItem(row, 1, QTableWidgetItem(purchase.customer_name))
                    self.table.setItem(row, 2, QTableWidgetItem(purchase.customer_email or ""))
                    # phone and address may be missing in API - default to empty string
                    self.table.setItem(row, 3, QTableWidgetItem(getattr(purchase, 'customer_phone', '') or ""))
                    self.table.setItem(row, 4, QTableWidgetItem(getattr(purchase, 'customer_address', '') or ""))
                    self.table.setItem(row, 5, QTableWidgetItem(purchase.car_name))
                    self.table.setItem(row, 6, QTableWidgetItem(purchase.purchase_date))

                    # Payment method
                    self.table.setItem(row, 7, QTableWidgetItem(str(purchase.payment_method) if getattr(purchase, 'payment_method', None) else ""))

                    # Status with color coding (column 8)
                    status_item = QTableWidgetItem(purchase.status)
                    if purchase.status == "COMPLETED":
                        status_item.setBackground(QColor(200, 255, 200))  # Light green
                    elif purchase.status == "CANCELLED":
                        status_item.setBackground(QColor(255, 200, 200))  # Light red
                    self.table.setItem(row, 8, status_item)

                    # Purchase price (column 9)
                    self.table.setItem(row, 9, QTableWidgetItem(f"${purchase.total_amount:.2f}"))
                    
                except Exception as e:
                    print(f"Error processing purchase {row + 1}: {str(e)}")
                    import traceback
                    traceback.print_exc()
            
            # Auto-resize rows to content
            self.table.resizeRowsToContents()
            
        except requests.exceptions.RequestException as e:
            error_msg = f"Network error while fetching purchases: {str(e)}\n"
            if hasattr(e, 'response') and e.response is not None:
                error_msg += f"Status Code: {e.response.status_code}\n"
                try:
                    error_msg += f"Response: {e.response.text}"
                except:
                    pass
            
            print(error_msg)
            QMessageBox.critical(self, "Network Error", error_msg)
            
        except Exception as e:
            error_msg = f"Failed to load purchases: {str(e)}\n"
            import traceback
            error_msg += traceback.format_exc()
            
            print(error_msg)
            QMessageBox.critical(self, "Error", f"An unexpected error occurred:\n{str(e)}")
            
        finally:
            # Reset button state
            self.refresh_btn.setEnabled(True)
            self.refresh_btn.setText("Refresh")
    
    def complete_purchase(self):
        """Mark the selected purchase as completed."""
        self._update_purchase_status("COMPLETED")
    
    def cancel_purchase(self):
        """Cancel the selected purchase."""
        self._update_purchase_status("CANCELLED")
    
    def on_selection_changed(self):
        """Enable/disable action buttons based on selection"""
        selected = self.table.selectedItems()
        has_selection = len(selected) > 0
        
        # Enable action buttons only if a row is selected
        self.complete_btn.setEnabled(has_selection)
        self.cancel_btn.setEnabled(has_selection)
        
        # If a row is selected, check if it's already in a final state
        if has_selection:
            row = selected[0].row()
            status = self.table.item(row, 8).text()  # Status is in column 8
            
            # Disable buttons if already in final state
            if status in ["COMPLETED", "CANCELLED"]:
                self.complete_btn.setEnabled(False)
                self.cancel_btn.setEnabled(False)
    
    def _update_purchase_status(self, status: str):
        """Update the status of the selected purchase"""
        selected = self.table.selectedItems()
        if not selected:
            QMessageBox.warning(self, "No Selection", "Please select a purchase to update.")
            return
        
        try:
            row = selected[0].row()
            purchase_id_item = self.table.item(row, 0)  # ID is in column 0
            
            if not purchase_id_item:
                QMessageBox.warning(self, "Error", "Could not determine purchase ID.")
                return
                
            purchase_id = purchase_id_item.text()
            if not purchase_id or purchase_id == '0':
                QMessageBox.warning(self, "Error", "Invalid purchase ID. Please refresh the list and try again.")
                return
                
            purchase_id = int(purchase_id)
            current_status = self.table.item(row, 8).text()  # Status is in column 8
            
            # Don't allow updating if already in a final state
            if current_status in ["COMPLETED", "CANCELLED"]:
                QMessageBox.warning(self, "Cannot Update", "This purchase has already been processed.")
                return
                
            # Show confirmation dialog
            action = "complete" if status == "COMPLETED" else "cancel"
            confirm = QMessageBox.question(
                self,
                "Confirm Action",
                f"Are you sure you want to {action} purchase #{purchase_id}?",
                QMessageBox.Yes | QMessageBox.No
            )
            
            if confirm == QMessageBox.Yes:
                # Disable buttons during update
                self.complete_btn.setEnabled(False)
                self.cancel_btn.setEnabled(False)
                
                # Show processing state
                processing_msg = QMessageBox(
                    QMessageBox.Information,
                    "Processing",
                    f"Updating purchase status to {status.lower()}...",
                    QMessageBox.NoButton,
                    self
                )
                processing_msg.setWindowModality(Qt.WindowModal)
                processing_msg.show()
                
                # Force UI update
                QApplication.processEvents()
                
                print(f"[UI] Attempting to update purchase {purchase_id} to status: {status}")
                
                # Perform the update
                success = self.api_service.update_purchase_status(purchase_id, status)
                
                if success:
                    print(f"[UI] Successfully updated purchase {purchase_id} to {status}")
                    # Close processing message and refresh data
                    processing_msg.close()
                    self.load_purchases()
                    QMessageBox.information(self, "Success", f"Purchase {action}d successfully!")
                else:
                    print(f"[UI] Failed to update purchase {purchase_id}")
                    processing_msg.close()
                    QMessageBox.warning(self, "Update Failed", 
                                     "Failed to update purchase status. "
                                     "Please check the console for more details and try again.")
                
        except ValueError as ve:
            QMessageBox.critical(self, "Error", f"Invalid purchase ID format: {str(ve)}")
        except Exception as e:
            error_msg = f"Failed to update purchase status: {str(e)}\n"
            import traceback
            error_msg += traceback.format_exc()
            print(error_msg)
            QMessageBox.critical(self, "Error", f"An unexpected error occurred:\n{str(e)}")
        finally:
            # Re-enable buttons
            self.on_selection_changed()