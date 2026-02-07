from PySide6.QtWidgets import (
    QApplication
)

from PySide6.QtCore import QStandardPaths
import os
import sys


def get_loc():
    # Get writable app data location
    app_data_dir = QStandardPaths.writableLocation(
        QStandardPaths.AppDataLocation
    )

    # Create directory if not exists
    os.makedirs(app_data_dir, exist_ok=True)

    return app_data_dir
