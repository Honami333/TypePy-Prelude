"""Option[T] — аналог Rust Option<T>.
 
Использование:
    x: Option[int] = Some(5)
    y: Option[int] = None
 
    match x:
        case Some(value):
            ...
        case None:
            ...
"""
 
from __future__ import annotations
 
from dataclasses import dataclass
from collections.abc import Callable
 
from result import Err, Ok, Result
 
 
@dataclass(frozen=True, slots=True)
class Some[T]:
    """Обёртка над значением, когда оно есть."""
 
    value: T

type Option[T] = Some[T] | None
 
 
def is_some[T](opt: Option[T]) -> bool:
    """Есть ли значение."""
    return opt is not None
 
 
def is_none[T](opt: Option[T]) -> bool:
    """Значения нет."""
    return opt is None
 
 
def unwrap[T](opt: Option[T]) -> T:
    """Достать значение. Падает с ValueError, если None."""
    match opt:
        case Some(value):
            return value
        case None:
            raise ValueError("unwrap() вызван на None")
 
 
def expect[T](opt: Option[T], msg: str) -> T:
    """То же что unwrap, но с собственным текстом ошибки."""
    match opt:
        case Some(value):
            return value
        case None:
            raise ValueError(msg)
 
 
def unwrap_or[T](opt: Option[T], default: T) -> T:
    """Достать значение либо вернуть default, если None."""
    match opt:
        case Some(value):
            return value
        case None:
            return default
 
 
def unwrap_or_else[T](opt: Option[T], f: Callable[[], T]) -> T:
    """Достать значение либо вычислить запасное через f(), если None."""
    match opt:
        case Some(value):
            return value
        case None:
            return f()
 
 
def map[T, U](opt: Option[T], f: Callable[[T], U]) -> Option[U]:
    """Применить f к значению внутри, если оно есть. None остаётся None."""
    match opt:
        case Some(value):
            return Some(f(value))
        case None:
            return None
 
 
def map_or[T, U](opt: Option[T], default: U, f: Callable[[T], U]) -> U:
    """Как map, но сразу разворачивает результат, с default вместо None."""
    match opt:
        case Some(value):
            return f(value)
        case None:
            return default
 
 
def map_or_else[T, U](
    opt: Option[T], default_f: Callable[[], U], f: Callable[[T], U]
) -> U:
    """Как map_or, но default тоже вычисляется лениво через default_f()."""
    match opt:
        case Some(value):
            return f(value)
        case None:
            return default_f()
 
 
def and_then[T, U](opt: Option[T], f: Callable[[T], Option[U]]) -> Option[U]:
    """Цепочка операций, каждая из которых сама может вернуть None."""
    match opt:
        case Some(value):
            return f(value)
        case None:
            return None
 
 
def or_else[T](opt: Option[T], f: Callable[[], Option[T]]) -> Option[T]:
    """Если opt — None, попробовать запасной вариант через f()."""
    match opt:
        case Some(_):
            return opt
        case None:
            return f()
 
 
def filter[T](opt: Option[T], predicate: Callable[[T], bool]) -> Option[T]:
    """Оставить значение, только если оно проходит проверку predicate."""
    match opt:
        case Some(value) if predicate(value):
            return opt
        case _:
            return None
 
 
def ok_or[T, E](opt: Option[T], err: E) -> Result[T, E]:
    """Превратить Option в Result: Some -> Ok, None -> Err(err)."""
    match opt:
        case Some(value):
            return Ok(value)
        case None:
            return Err(err)