from sqlalchemy import create_engine
import sqlalchemy.orm as orm
from os.path import exists

SqlAlchemyBase = orm.declarative_base()

__factory = None


def global_init(db_file: str):
    global __factory

    if __factory:
        return

    if not db_file or not db_file.strip():
        raise Exception("Database file isn't specified!")

    db_exists = exists(db_file.strip())
    connection_string = f'sqlite:///{db_file.strip()}?check_same_thread=False'
    print(f"Connecting to the database at {connection_string}")

    engine = create_engine(connection_string, echo=False)
    __factory = orm.sessionmaker(bind=engine)

    from data.__all_models import User, Deck, Card

    SqlAlchemyBase.metadata.create_all(engine)
    if not db_exists:
        db_session = create_session()
        admin = User(username="admin")
        admin.set_password("lol")
        db_session.add(admin)

        deck = Deck(
            user_created_id=1,
            name="Test deck"
        )
        db_session.add(deck)

        card1 = Card(
            deck_id=1,
            position=1,
            front="Kartica",
            back="die Karte"
        )

        card2 = Card(
            deck_id=1,
            position=2,
            front="Glas",
            back="die Stimme"
        )

        db_session.add(card1)
        db_session.add(card2)

        db_session.commit()


def create_session():
    global __factory
    return __factory()
