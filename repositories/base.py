from abc import ABC, abstractmethod

class BaseRespository[T](ABC):
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