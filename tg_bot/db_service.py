import contextlib


class DbService:
    def __init__(self, session_maker):
        self._session_maker = session_maker

    @contextlib.contextmanager
    def _get_session(self):
        db_session = self._session_maker()
        yield db_session
        db_session.close()

    @contextlib.contextmanager
    def create(self, model_obj):
        with self._get_session() as db_session:
            db_session.add(model_obj)
            db_session.commit()
            db_session.refresh(model_obj)
            yield model_obj

    @contextlib.contextmanager
    def get(self, model_cls):
        with self._get_session() as db_session:
            return db_session.query(model_cls).all()
