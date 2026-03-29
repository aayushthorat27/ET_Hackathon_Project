"""Outcome Caching for Token Optimization"""
from typing import Dict, Any, Tuple
from app.utils import hash_input


class OutcomeCache:
    """Cache successful agent outcomes to avoid redundant API calls"""

    def __init__(self):
        self.cache: Dict[str, Tuple[str, Dict[str, Any]]] = {}  # input_hash -> (agent_id, result)
        self.hits = 0
        self.misses = 0

    def get_cache_key(self, agent_id: str, input_data: Dict[str, Any]) -> str:
        """Generate cache key"""
        return f"{agent_id}:{hash_input(input_data)}"

    def get(self, agent_id: str, input_data: Dict[str, Any]) -> Dict[str, Any] | None:
        """Get cached result if available"""
        key = self.get_cache_key(agent_id, input_data)
        if key in self.cache:
            self.hits += 1
            return self.cache[key][1]
        self.misses += 1
        return None

    def set(self, agent_id: str, input_data: Dict[str, Any], result: Dict[str, Any]) -> None:
        """Cache a successful result"""
        key = self.get_cache_key(agent_id, input_data)
        self.cache[key] = (agent_id, result)

    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        total = self.hits + self.misses
        hit_rate = (self.hits / total * 100) if total > 0 else 0
        return {"hits": self.hits, "misses": self.misses, "hit_rate": hit_rate}

    def clear(self) -> None:
        """Clear cache"""
        self.cache.clear()


# Global cache instance
outcome_cache = OutcomeCache()
