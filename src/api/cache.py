from django.core.cache import cache


def cache_key_for_collect_list(page: int = 1) -> str:
    """Ключ кеша для списка сборов."""
    return f'collect_list_page_{page}'


def cache_key_for_collect_detail(collect_id: int) -> str:
    """Ключ кеша для детальной информации о сборе."""
    return f'collect_detail_{collect_id}'


def cache_collect_list(page: int = 1, data=None):
    """Кэширует список сборов."""
    return cache.set(cache_key_for_collect_list(page), data, timeout=600)


def cache_collect_detail(collect_id: int, data=None):
    """Кэширует детальную информацию о сборе."""
    return cache.set(
        cache_key_for_collect_detail(collect_id), data, timeout=600
    )


def invalidate_collect_list_cache(page: int = 1):
    """Удаляет кэш списка сборов."""
    return cache.delete(cache_key_for_collect_list(page))


def invalidate_collect_detail_cache(collect_id: int):
    """Удаляет кэш детальной информации о сборе."""
    return cache.delete(cache_key_for_collect_detail(collect_id))
