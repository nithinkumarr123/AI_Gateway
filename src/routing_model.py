import re
import math
from typing import Dict, Any

class RoutingModel:
    
    
    def __init__(self):
        self.force_capable_indicators = [
            'explain', 'analyze', 'evaluate', 'compare', 'contrast',
            'justify', 'synthesize', 'critique', 'deduce', 'infer',
            'discuss', 'elaborate', 'assess', 'examine', 'interpret',
            
            'theory of relativity', 'quantum computing', 'quantum',
            'relativity', 'black hole', 'gravity', 'physics',
            
            'algorithm', 'function', 'implementation', 'debug', 'optimize',
            'class', 'method', 'recursion', 'quicksort', 'sorting',
            'data structure', 'code', 'programming',
            
            'economic implications', 'microservices', 'architecture',
            'ethical implications', 'system of equations', 'matrix methods',
            'lesson plan', 'case study', 'universal basic income',
            'climate change', 'machine learning', 'deep learning',
            

            'design', 'create', 'build', 'develop', 'construct',
            'formulate', 'generate', 'produce', 'implement'
        ]
        
        self.force_fast_indicators = [

            'what is', 'who is', 'when did', 'where is', 'which is',
            'define briefly', 'list three', 'list', 'how many',
            'what year', 'what day', 'tell me',
            
            'hello', 'hi', 'hey', 'greetings', 'good morning', 'good day',
            
            '2+2', '3+3', '4+4', '5+5', '15*8', '10*10',
            
            'capital of', 'largest ocean', 'ceo of'
        ]
        
        self.complex_patterns = [
            r'\b(if|then|else|while|for|loop)\b.*\b(return|output)\b',
            r'\b(calculate|compute|solve|find)\b.*\b(equation|formula)\b',
            r'\b(compare|contrast)\b.*\b(and|vs|versus)\b',
            r'\b(implement|write|create|design)\b.*\b(system|architecture|function)\b',
            r'.*\b(advantages|disadvantages|pros|cons)\b',
            r'.*\b(implications|consequences|impact)\b',
            r'.{200,}', 
        ]
        
        self.simple_patterns = [
            r'^(what|who|when|where|why|how)\s+(is|are|was|were)\s+\w+\.?$',  
            r'^[A-Z][a-z]+\?$',  
            r'^hello|^hi|^hey',  
        ]
    
    def route(self, prompt: str) -> Dict[str, Any]:
        
        if not prompt or not isinstance(prompt, str):
            return {
                'model': 'fast',
                'reason': 'Invalid input - defaulting to fast model',
                'confidence': 0.0
            }
        
        prompt_lower = prompt.lower()
        token_count = len(prompt.split())
        char_count = len(prompt)

        for indicator in self.force_capable_indicators:
            if indicator in prompt_lower:
                return {
                    'model': 'capable',
                    'reason': f"Complex query detected: contains '{indicator}' - routing to capable model",
                    'confidence': 0.85,
                    'features': {
                        'trigger': indicator,
                        'token_count': token_count,
                        'char_count': char_count
                    }
                }

        for pattern in self.complex_patterns:
            if re.search(pattern, prompt_lower):
                return {
                    'model': 'capable',
                    'reason': f"Complex pattern detected - routing to capable model",
                    'confidence': 0.80,
                    'features': {
                        'pattern_match': pattern,
                        'token_count': token_count
                    }
                }
        

        if token_count < 15:
            for indicator in self.force_fast_indicators:
                if indicator in prompt_lower:
                    return {
                        'model': 'fast',
                        'reason': f"Simple query: '{indicator}' detected - routing to fast model",
                        'confidence': 0.90,
                        'features': {
                            'trigger': indicator,
                            'token_count': token_count
                        }
                    }
            

            for pattern in self.simple_patterns:
                if re.search(pattern, prompt_lower):
                    return {
                        'model': 'fast',
                        'reason': f"Simple pattern detected - routing to fast model",
                        'confidence': 0.85,
                        'features': {
                            'token_count': token_count
                        }
                    }
        

        if token_count >= 40:
            return {
                'model': 'capable',
                'reason': f"Long prompt ({token_count} words) - likely complex, routing to capable model",
                'confidence': 0.75,
                'features': {
                    'token_count': token_count,
                    'char_count': char_count
                }
            }
        
        if token_count <= 5:
            return {
                'model': 'fast',
                'reason': f"Very short prompt ({token_count} words) - routing to fast model",
                'confidence': 0.85,
                'features': {
                    'token_count': token_count
                }
            }
        
        if 6 <= token_count <= 15:
            question_words = ['what', 'who', 'when', 'where', 'why', 'how', 'which']
            if any(word in prompt_lower.split()[:3] for word in question_words):
                return {
                    'model': 'fast',
                    'reason': f"Medium prompt ({token_count} words) with question word - routing to fast model",
                    'confidence': 0.75,
                    'features': {
                        'token_count': token_count
                    }
                }

        complex_keywords = [
            'algorithm', 'function', 'implementation', 'analysis', 'design',
            'system', 'architecture', 'framework', 'methodology', 'process'
        ]
        
        for keyword in complex_keywords:
            if keyword in prompt_lower:
                return {
                    'model': 'capable',
                    'reason': f"Complex keyword '{keyword}' detected - routing to capable model",
                    'confidence': 0.70,
                    'features': {
                        'trigger': keyword,
                        'token_count': token_count
                    }
                }
        
        return {
            'model': 'fast',
            'reason': f"Default routing - prompt appears simple ({token_count} words)",
            'confidence': 0.65,
            'features': {
                'token_count': token_count,
                'char_count': char_count
            }
        }
    
    def get_info(self) -> Dict[str, Any]:
        return {
            'type': 'Rule-based routing model with multi-level rules',
            'force_capable_count': len(self.force_capable_indicators),
            'force_fast_count': len(self.force_fast_indicators),
            'complex_patterns_count': len(self.complex_patterns),
            'simple_patterns_count': len(self.simple_patterns),
            'description': 'Routes prompts based on keywords, patterns, and length'
        }
    
    def test_route(self, prompt: str) -> Dict[str, Any]:
        result = self.route(prompt)
        result['debug'] = {
            'prompt_length': len(prompt),
            'word_count': len(prompt.split()),
            'char_count': len(prompt)
        }
        return result


if __name__ == "__main__":
    model = RoutingModel()
    
    test_prompts = [
        "What is 2+2?",
        "What is the capital of France?",
        "Explain quantum computing",
        "Write a Python function for quicksort",
        "What is Python?",
        "Analyze the economic implications of AI",
        "Hello",
        "Compare and contrast machine learning and deep learning",
        "15 * 8",
        "Design a microservices architecture"
    ]
    
    print("="*70)
    print("ROUTING MODEL TEST")
    print("="*70)
    
    for prompt in test_prompts:
        result = model.route(prompt)
        print(f"\nPrompt: {prompt}")
        print(f"  → Model: {result['model'].upper()}")
        print(f"  → Reason: {result['reason']}")
        print(f"  → Confidence: {result['confidence']:.2f}")