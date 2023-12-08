import sqlite3
from typing import Optional

class DeviceControl:
    """
    A class to manage the usage of mobile devices in testing scenarios.

    This class creates and manages an SQLite database to track the usage status of mobile devices, 
    functioning as a semaphore system. It offers functionalities to add new devices, update their usage status, 
    and check whether a device is currently in use.

    Attributes:
        conn (sqlite3.Connection): Connection to the SQLite database.
        cursor (sqlite3.Cursor): Cursor to execute database operations.
    """

    def __init__(self, db_path: str = 'devices.db') -> None:
        """
        Initializes the database connection and creates the table if it doesn't exist.

        Args:
            db_path (str): Path to the SQLite database file.
        """
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS devices (
                device_id TEXT PRIMARY KEY,
                in_use BOOLEAN NOT NULL CHECK (in_use IN (0, 1))
            )
        ''')
        self.conn.commit()

    def add_device(self, device_id: str) -> None:
        """
        Adds a new device to the database with a default status of not in use.

        Args:
            device_id (str): Unique identifier for the device.
        """
        self.cursor.execute('''
            INSERT OR IGNORE INTO devices (device_id, in_use) VALUES (?, 0)
        ''', (device_id,))
        self.conn.commit()

    def set_device_status(self, device_id: str, in_use: bool) -> None:
        """
        Updates the usage status of a specified device.

        Args:
            device_id (str): Unique identifier for the device.
            in_use (bool): True if the device is in use, False otherwise.
        """
        self.cursor.execute('''
            UPDATE devices SET in_use = ? WHERE device_id = ?
        ''', (int(in_use), device_id))
        self.conn.commit()

    def is_device_in_use(self, device_id: str) -> bool:
        """
        Checks if a specified device is currently in use. Adds the device to the database with a default status
        of not in use if it does not exist.

        Args:
            device_id (str): Unique identifier for the device.

        Returns:
            bool: True if the device is in use, False otherwise.
        """
        self.cursor.execute('''
            SELECT in_use FROM devices WHERE device_id = ?
        ''', (device_id,))
        result = self.cursor.fetchone()

        if result is None:
            self.add_device(device_id)
            return False
        else:
            return bool(result[0])

    def __del__(self) -> None:
        """
        Closes the database connection when the instance is destroyed.
        """
        self.conn.close()
