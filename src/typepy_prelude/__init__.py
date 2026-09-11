from .option import Option, Some
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

from .option_box import OptionBox, box

__all__ = [
    "Option",
    "OptionBox",
    "Some",
    "and_then",
    "box",
    "expect",
    "filter",
    "is_none",
    "is_some",
    "map",
    "map_or",
    "map_or_else",
    "ok_or",
    "or_else",
    "unwrap",
    "unwrap_or",
    "unwrap_or_else",
]