from app.models.user import User
from app.db.connection import Neo4jConnection

db = Neo4jConnection()

def get_user_by_firebase_uid(uid: str) -> User | None:
    """
    Get a user by their Firebase UID.
    """
    try:
        query = """MATCH (u:User {uid: $uid}) RETURN u"""

        with db.get_session() as session:  # Gerenciando sessão corretamente
            result = session.run(query, uid=uid).single()

        if result:
            user_data = result["u"]
            return User(
                uid=user_data["uid"],
                email=user_data["email"],
                name=user_data.get("name"),
                photo_url=user_data.get("photo_url"),
            )

    except Exception as e:
        print(f"Error getting user by Firebase UID: {e}")
        raise e

    return None  # Retorna None se o usuário não for encontrado


def create_user(user: User) -> User:
    """
    Create a new user in the database.
    """

    try:
        query = """
                MERGE (u:User {uid: $uid})
                ON CREATE SET u.email = $email, u.name = $name, u.photo_url = $photo_url
                RETURN u
        """

        with db.get_session() as session:  # Usa `with` para garantir que a sessão seja fechada corretamente
            result = session.run(
                query,
                uid=user.uid,
                email=user.email,
                name=user.name,
                photo_url=user.photo_url,
            ).single()
        
        if result:
            user_data = result["u"]
            return User(
                uid=user_data["uid"],
                email=user_data["email"],
                name=user_data.get("name"),
                photo_url=user_data.get("photo_url"),
            )
        else:
            return None  # Caso nenhum usuário seja criado ou retornado

    except Exception as e:
        print(f"Error creating user: {e}")
        raise e

