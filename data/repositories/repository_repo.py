"""
save(repo)
get_by_account(account_id)
get_by_repo_id(repo_id)
delete_by_account(account_id)
"""
from data.database import DataBase
from data.models import Repository
from typing import List

class RepoRepository :
    def __init__(self):
        self.db = DataBase()
        
    def save(self , repo : Repository) -> int :
        query = """
        INSERT INTO repositories (
            account_id,
            repo_id,
            name,
            full_name,
            is_private,
            main_language,
            updated_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        return self.db.execute(query , repo.to_insert_tuple())
    
    def get_by_account(self, account_id : int) -> List[Repository] :
        rows = self.db.fetch_all(
            "SELECT * FROM repositories WHERE account_id = ?",
            (account_id,)
        )
        return [Repository.from_row(r) for r in rows]
    
    def get_by_repo_id(self , repo_id : int) -> Repository | None :
        rows = self.db.fetch_all(
            "SELECT * FROM repositories WHERE repo_id = ? LIMIT 1",
            (repo_id,)
        )
        return Repository.from_row(rows[0]) if rows else None
    
    def delete_by_account_id(self , account_id : int) -> int :
        query = "DELETE FROM repositories WHERE account_id = ?"
        
        return self.db.execute(query , (account_id,))