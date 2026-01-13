from abc import ABC, abstractmethod

class DatabaseInterface(ABC):
    @abstractmethod
    def execute_query(self, query: str, params: tuple = ()) -> list:
        """Execute a query against the database."""
        pass