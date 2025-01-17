"""Module for reading and writing csvs."""

import os
from typing import List
import logging
import pandas as pd
from pandas.errors import EmptyDataError
from app.calculator.calculation import Calculation

class FileManager:
    """Class for reading and writing csvs."""
    @staticmethod
    def read_from_csv(file_name: str) -> List[Calculation]:
        """Read data from a CSV file and return it as a list of Calculations."""
        try:
            df = pd.read_csv(file_name)
        except FileNotFoundError:
            logging.warning("File '%s' not found.", file_name)
            return []
        except EmptyDataError:
            logging.warning("File '%s' is empty.", file_name)
            return []

        calculations = []
        for _, row in df.iterrows():
            try:
                calc = Calculation.from_dict(row.to_dict())
                calculations.append(calc)
            except Exception as e:
                # Handle any parsing errors
                logging.error("Error parsing row %s: %s", row, e)
        return calculations

    @staticmethod
    def write_to_csv(file_name: str, calculations: List[Calculation]):
        """Write a list of Calculations to a CSV file using Pandas."""
        data = [calc.to_dict() for calc in calculations]
        df = pd.DataFrame(data)
        df.to_csv(file_name, index=False)
    
    @staticmethod
    def delete_csv_file(file_name: str):
        """
        Delete the specified CSV file.
        
        Args:
            file_name (str): The name of the CSV file to delete.
        """
        try:
            os.remove(file_name)
            logging.info("File '%s' has been deleted.", file_name)
        except FileNotFoundError:
            logging.warning("File '%s' does not exist.", file_name)
        except Exception as e:
            logging.error("Error deleting file '%s': %s", file_name, e)

