from __future__ import annotations

from dataclasses import dataclass
from collections.abc import Callable

from .option import Option
# Проверки
from .option import is_some, is_none
# Извлечение значения
from .option import unwrap, expect, unwrap_or, unwrap_or_else
# Трансформации
from .option import map, map_or, map_or_else
# Цепочки и фильтрация
from .option import and_then, or_else, filter
# Конвертация в Result
from .option import ok_or
from result import Result


@dataclass(frozen=True, slots=True)
class OptionBox[T]:
    """Обёртка вокруг Option[T] только ради удобных цепочек .map()/.and_then().

    Сама по себе нигде не хранится и не передаётся в сигнатурах —
    в остальном коде везде остаётся честный Some[T] | None.
    Использование: box(opt).map(f).and_then(g).unpack()
    """

    _inner: Option[T]

    def unpack(self) -> Option[T]:
        """Достать обратно обычный Option[T] — конец цепочки."""
        return self._inner

    def map[U](self, f: Callable[[T], U]) -> OptionBox[U]:
        """Применить f к значению внутри, если оно есть. None остаётся None."""
        return OptionBox(map(self._inner, f))

    def map_or[U](self, default: U, f: Callable[[T], U]) -> U:
        """Как map, но сразу разворачивает результат, с default вместо None."""
        return map_or(self._inner, default, f)

    def map_or_else[U](
        self, default_f: Callable[[], U], f: Callable[[T], U]
    ) -> U:
        """Как map_or, но default тоже вычисляется лениво через default_f()."""
        return map_or_else(self._inner, default_f, f)

    def and_then[U](self, f: Callable[[T], Option[U]]) -> OptionBox[U]:
        """Цепочка операций, каждая из которых сама может вернуть None."""
        return OptionBox(and_then(self._inner, f))

    def or_else(self, f: Callable[[], Option[T]]) -> OptionBox[T]:
        """Если opt — None, попробовать запасной вариант через f()."""
        return OptionBox(or_else(self._inner, f))

    def filter(self, predicate: Callable[[T], bool]) -> OptionBox[T]:
        """Оставить значение, только если оно проходит проверку predicate."""
        return OptionBox(filter(self._inner, predicate))

    def unwrap(self) -> T:
        """Достать значение. Падает с ValueError, если None."""
        return unwrap(self._inner)

    def expect(self, msg: str) -> T:
        """То же что unwrap, но с собственным текстом ошибки."""
        return expect(self._inner, msg)

    def unwrap_or(self, default: T) -> T:
        """Достать значение либо вернуть default, если None."""
        return unwrap_or(self._inner, default)

    def unwrap_or_else(self, f: Callable[[], T]) -> T:
        """Достать значение либо вычислить запасное через f(), если None."""
        return unwrap_or_else(self._inner, f)

    def is_some(self) -> bool:
        """Есть ли значение."""
        return is_some(self._inner)

    def is_none(self) -> bool:
        """Значения нет."""
        return is_none(self._inner)

    def ok_or[E](self, err: E) -> Result[T, E]:
        """Превратить Option в Result: Some -> Ok, None -> Err(err)."""
        return ok_or(self._inner, err)


def box[T](opt: Option[T]) -> OptionBox[T]:
    """Обернуть Option[T] для цепочки методов."""
    return OptionBox(opt)