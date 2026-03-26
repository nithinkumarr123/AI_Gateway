from difflib import SequenceMatcher
from typing import Optional, Dict, Any, Tuple
from collections import OrderedDict
import hashlib
import time

class CacheLayer:
    def __init__(self, similarity_threshold: float = 0.85, max_size: int = 1000):
        self.cache = OrderedDict()
        self.similarity_threshold = similarity_threshold
        self.max_size = max_size
        self.hits = 0
        self.misses = 0
        
    def _calculate_similarity(self, text1: str, text2: str) -> float:
        return SequenceMatcher(None, text1.lower(), text2.lower()).ratio()
    
    def _get_cache_key(self, prompt: str) -> str:
        return hashlib.md5(prompt.lower().encode()).hexdigest()
    
    def get(self, prompt: str) -> Tuple[Optional[Dict[str, Any]], float]:
        exact_key = self._get_cache_key(prompt)
        if exact_key in self.cache:
            self.hits += 1
            self.cache.move_to_end(exact_key)
            return self.cache[exact_key], 1.0
        
        best_match = None
        best_similarity = 0
        
        for key, data in self.cache.items():
            original_prompt = data.get('original_prompt', '')
            if original_prompt:
                similarity = self._calculate_similarity(prompt, original_prompt)
                if similarity > best_similarity and similarity >= self.similarity_threshold:
                    best_similarity = similarity
                    best_match = data
        
        if best_match:
            self.hits += 1
            return best_match, best_similarity
        
        self.misses += 1
        return None, 0
    
    def set(self, prompt: str, data: Dict[str, Any]) -> None:
        cache_key = self._get_cache_key(prompt)
        data_with_original = {
            **data,
            'original_prompt': prompt,
            'timestamp': time.time()
        }
        self.cache[cache_key] = data_with_original
        self.cache.move_to_end(cache_key)
        
        if len(self.cache) > self.max_size:
            self.cache.popitem(last=False)
    
    def get_stats(self):
        total = self.hits + self.misses
        hit_rate = self.hits / total if total > 0 else 0
        return {
            'size': len(self.cache),
            'hits': self.hits,
            'misses': self.misses,
            'hit_rate': hit_rate,
            'threshold': self.similarity_threshold
        }