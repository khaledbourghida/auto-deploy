from data.database import DataBase
from data.models import Platform
from typing import List

class PlatformRepository:
    def __init__(self):
        self.db = DataBase()

    def create(self, platform: Platform) -> int:
        query = """
        INSERT INTO platforms (
            name,
            display_name,
            subtitle,
            bgcolor,
            icon,
            desc,
            base_url,
            is_connected,
            created_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        return self.db.execute(query, platform.to_insert_tuple())

    def get_by_name(self, name: str) -> Platform | None:
        rows = self.db.fetch_all(
            "SELECT * FROM platforms WHERE name = ? LIMIT 1",
            (name,)
        )
        return Platform.from_row(rows[0]) if rows else None

    def get_by_id(self, id: int) -> Platform | None:
        rows = self.db.fetch_all(
            "SELECT * FROM platforms WHERE id = ? LIMIT 1",
            (id,)
        )
        return Platform.from_row(rows[0]) if rows else None

    def get_all(self) -> List[Platform]:
        rows = self.db.fetch_all("SELECT * FROM platforms")
        return [Platform.from_row(r) for r in rows]
    
    def get_id_by_name(self , name : str) -> int | None :
        rows = self.db.fetch_all(
            "SELECT id FROM platforms WHERE name = ? LIMIT 1",
            (name,)
        )
        
        return rows[0]["id"] if rows else None

    def exists(self, name: str) -> bool:
        rows = self.db.fetch_all(
            "SELECT 1 FROM platforms WHERE name = ? LIMIT 1",
            (name,)
        )
        return bool(rows)
    
    def make_connected(self, id : int) -> int :
        query = """
        UPDATE platforms SET is_connected = 1 WHERE id = ?
        """
        
        return self.db.execute(query , (id,))
    
    def make_unconnected(self , id : int) -> int :
        query = """
        UPDATE platforms SET is_connected = 0 WHERE id = ?
        """
        
        return self.db.execute(query , (id,))