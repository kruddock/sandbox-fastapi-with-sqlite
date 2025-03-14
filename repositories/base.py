import contextlib
from abc import ABC, abstractmethod
from sqlalchemy import Engine
from sqlmodel import Session

class BaseRespository[T](ABC):
    def __init__(self, engine: Engine):
        super().__init__()
        self.engine = engine
        
    @contextlib.contextmanager
    def get_session(self):
        with Session(self.engine) as session:
            yield session 
        
    @abstractmethod
    def collection(self) -> list[T]:
        raise NotImplementedError
    
    @abstractmethod
    def add(self, **kwargs: object) -> T:
        raise NotImplementedError
    
    @abstractmethod
    def show(self, id: int) -> T | None:
        raise NotImplementedError
    
    @abstractmethod
    def update(self, id: int, **kwargs: object) -> T | None:
        raise NotImplementedError
    
    @abstractmethod
    def remove(self, id: int) ->  T | None:
        raise NotImplementedError