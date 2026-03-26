import requests
import json
import time

print("="*70)
print("AI GATEWAY - Test Cases")
print("="*70)

test_suite = [
    ("Simple Math", "What is 15 * 8?", "fast"),
    ("Simple Factual", "What is the capital of France?", "fast"),
    ("Complex Science", "Explain quantum computing", "capable"),
    ("Complex Physics", "Explain the theory of relativity", "capable"),
    ("Code Implementation", "Write a Python function for quicksort", "capable"),
    ("Simple Definition", "What is Python?", "fast"),
    ("Complex Analysis", "Analyze the economic implications of AI", "capable"),
    ("Greeting", "Hello", "fast"),
]

correct = 0
print("\n ROUTING ACCURACY TEST")
print("-"*70)

for i, (name, prompt, expected) in enumerate(test_suite, 1):
    try:
        print(f"\n[{i}/{len(test_suite)}] Testing: {name}")

        if i > 1:
            time.sleep(0.5)
        
        response = requests.post(
            "http://127.0.0.1:8000/chat",
            json={"prompt": prompt},
            timeout=10  # Increased timeout
        )
        
        if response.status_code == 200:
            result = response.json()
            model_used = result['model_used']
            
            if model_used == expected:
                correct += 1
                status = "✅"
            else:
                status = "❌"
            
            print(f"{status} {name:25} → {model_used.upper():8} (Expected: {expected.upper()})")
            print(f"   Reason: {result['routing_reason'][:70]}...")
            print(f"   Cache: {'HIT' if result['cache_hit'] else 'MISS'}")
        else:
            print(f" {name:25} → Error: Status {response.status_code}")
            
    except requests.exceptions.Timeout:
        print(f"  {name:25} → Timeout, retrying...")
        try:
            time.sleep(1)
            response = requests.post(
                "http://127.0.0.1:8000/chat",
                json={"prompt": prompt},
                timeout=10
            )
            result = response.json()
            model_used = result['model_used']
            if model_used == expected:
                correct += 1
                print(f" {name:25} → {model_used.upper()} (Retry successful)")
        except:
            print(f" {name:25} → Failed after retry")
            
    except Exception as e:
        print(f" {name:25} → Error: {str(e)[:50]}")

accuracy = (correct / len(test_suite)) * 100
print("\n" + "="*70)
print(f"FINAL ACCURACY: {correct}/{len(test_suite)} ({accuracy:.0f}%)")
print("="*70)

print("\n CACHE PERFORMANCE")
print("-"*70)
try:
    health = requests.get("http://127.0.0.1:8000/health", timeout=5).json()
    cache = health['cache']
    print(f"Cache Size: {cache['size']} entries")
    print(f"Cache Hits: {cache['hits']}")
    print(f"Cache Misses: {cache['misses']}")
    print(f"Hit Rate: {cache['hit_rate']*100:.1f}%")
except:
    print("Unable to fetch cache stats")


print("\n RECENT ACTIVITY")
print("-"*70)
try:
    logs = requests.get("http://127.0.0.1:8000/logs?limit=8", timeout=5).json()
    for log in logs[:8]:
        timestamp = log['timestamp'].split('T')[1][:8]
        model = log['model_used'].upper()
        cache = "📀" if log['cache_hit'] else "💾"
        prompt = log['prompt_snippet'][:50]
        print(f"{timestamp} | {cache} | {model:8} | {prompt}...")
except:
    print("Unable to fetch logs")

print("\n" + "="*70)
print("Test Case COMPLETED ")
print("="*70)