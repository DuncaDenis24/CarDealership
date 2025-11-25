import sys
import os
from pathlib import Path
from PyQt5.QtWidgets import QApplication

# Add the project root (parent of desktop) to Python path
project_root = str(Path(__file__).parent.parent.absolute())
if project_root not in sys.path:
    sys.path.append(project_root)

# Import local modules
from ui.main_window import MainWindow

def load_stylesheet(app):
    """Load and apply the stylesheet."""
    # Try multiple possible paths
    possible_paths = [
        os.path.join(os.path.dirname(__file__), 'ui', 'styles', 'main_style.qss'),  # From desktop/
        os.path.join(os.path.dirname(__file__), 'styles', 'main_style.qss'),  # From desktop/ui/
        'main_style.qss'  # Current directory
    ]
    
    for path in possible_paths:
        try:
            if os.path.exists(path):
                with open(path, 'r', encoding='utf-8') as f:
                    stylesheet = f.read()
                    app.setStyleSheet(stylesheet)
                    return True
        except Exception as e:
            print(f"Error loading stylesheet from {path}: {e}")
    
    print("Failed to load stylesheet from any path")
    return False

def main():
    # Create the application
    app = QApplication(sys.argv)
    
    # Load and apply stylesheet
    load_stylesheet(app)
    
    # Create and show the main window
    window = MainWindow()
    window.show()
    
    # Run the application
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()