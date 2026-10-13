from data.database import DataBase
from data.models import Token
from datetime import datetime

class TokenRepository :
    def __init__(self):
        self.db = DataBase()
        
    def save(self, token : Token) -> int :
        query = """
        INSERT INTO tokens (
            account_id,
            token_encrypted,
            token_type,
            expires_at,
            scopes,
            created_at
        ) VALUES (?, ?, ?, ?, ?, ?)
        """
        
        return self.db.execute(query , token.to_insert_tuple())
    
    def get_by_account(self , account_id : int) -> Token | None :
        rows = self.db.fetch_all(
            "SELECT * FROM tokens WHERE account_id = ? LIMIT 1",
            (account_id,)
        )
        
        return Token.from_row(rows[0]) if rows else None
    
    def delete(self , account_id : int) -> int :
        query = """
        DELETE FROM tokens WHERE account_id = ?
        """
        
        return self.db.execute(query , (account_id,))
    
    
    def has_valid_token(self, account_id: int) -> bool:
        rows = self.db.fetch_all(
            """
            SELECT expires_at FROM tokens
            WHERE account_id = ?
            LIMIT 1
            """,
            (account_id,)
        )

        if not rows:
            return False

        expires_at = rows[0]["expires_at"]
        if expires_at is None:
            return True

        return datetime.fromisoformat(expires_at) > datetime.utcnow()
    
    def update(self, token: Token) -> int:
        query = """
        UPDATE tokens SET
            token_encrypted = ?,
            expires_at = ?
        WHERE id = ?
        """
        return self.db.execute(query, (token.token_encrypted, token.expires_at, token.id))