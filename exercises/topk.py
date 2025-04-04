# Prelude
# This takes a list of strings representing SKUs and returns the top k SKUs based on their frequency.

from collections import Counter
from typing import Dict, List


def top_k(sku_list: List[str], k: int) -> List[str]:
    """
    Returns the top k SKUs based on their frequency.
    """
    if not sku_list:
        return []

    sku_count = Counter(sku_list)
    top_skus = [sku for sku, _ in sku_count.most_common(k)]
    return top_skus


def top_k_sorted(sku_list: List[str], k) -> List[str]:
    """
    Returns the top k SKUs based on their frequency.
    """
    sku_count = Counter(sku_list)
    sku_list = sorted(sku_count, key=lambda x: sku_count[x])
    return sku_list[-k:]


def frequencies(list: List[str]) -> Dict[str, int]:
    """
    Returns a dictionary of the frequency of each SKU.
    """
    freq_dict = {}
    for item in list:
        if item in freq_dict:
            freq_dict[item] += 1
        else:
            freq_dict[item] = 1
    return freq_dict


def sort_by_freq(freq_dict: Dict[str, int]) -> List[str]:
    """
    Returns a list of SKUs sorted by frequency.
    """
    return sorted(freq_dict, key=lambda x: freq_dict[x], reverse=True)


def top_k_freq(sku_list: List[str], k: int) -> List[str]:
    """
    Returns the top k SKUs based on their frequency.
    """
    freq_dict = frequencies(sku_list)
    sorted_skus = sort_by_freq(freq_dict)
    return sorted_skus[:k]
