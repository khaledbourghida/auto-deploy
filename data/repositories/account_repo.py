from data.database import DataBase
from data.models import Account
from typing import List

class AccountRepository :
    def __init__(self):
        self.db = DataBase()
        
    def create(self, account : Account) -> int :
        query = """
        INSERT INTO accounts (
            platform_id,
            username,
            email,
            avatar_url,
            is_active,
            created_at
        ) VALUES (?, ?, ?, ?, ?, ?)
        """
        
        return self.db.execute(query , account.to_insert_tuple())
    
    def get_by_id(self , id : int) -> Account | None :
        rows = self.db.fetch_all(
            "SELECT * FROM accounts WHERE id = ? LIMIT 1",
            (id,)
        )
        
        return Account.from_row(rows[0]) if rows else None
    
    def get_by_platform(self , platform_id : int) -> List[Account] :
        rows = self.db.fetch_all(
            "SELECT * FROM accounts WHERE platform_id = ?",
            (platform_id,)
        )
        
        return [Account.from_row(r) for r in rows]
    
    def get_active(self, platform_id : int) -> Account | None :
        rows = self.db.fetch_all(
            "SELECT * FROM accounts WHERE platform_id = ? AND is_active = 1 LIMIT 1",
            (platform_id,)
        )
        
        return Account.from_row(rows[0]) if rows else None
    
    def set_active(self , account_id : int) -> int :
        query = """
        UPDATE accounts SET is_active = 1 WHERE id = ?
        """
        
        return self.db.execute(query , (account_id,))
    
    def deactivate_all(self, platform_id : int) -> int :
        query = """
        UPDATE accounts SET is_active = 0 WHERE platform_id = ?
        """
        
        return self.db.execute(query , (platform_id,))
    
    def delete(self , account_id : int) -> int :
        query = """
        DELETE FROM accounts WHERE id = ?
        """
        
        return self.db.execute(query , (account_id,))