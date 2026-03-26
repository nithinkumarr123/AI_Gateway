import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from src.routing_model import RoutingModel

def run_poc():
    print("=" * 80)
    print("AI GATEWAY - ROUTING MODEL POC")
    print("=" * 80)
    
    model = RoutingModel()
    
    with open('test_suite.json', 'r') as f:
        test_suite = json.load(f)
    
    total = len(test_suite)
    correct = 0
    false_positives = 0
    false_negatives = 0
    
    print(f"\nEvaluating {total} prompts...")
    print("-" * 80)
    
    results = []
    
    for i, test_case in enumerate(test_suite, 1):
        prompt = test_case['prompt']
        expected = test_case['expected_model']
        complexity_type = test_case['complexity_type']
        
        decision = model.route(prompt)
        predicted = decision['model']
        confidence = decision['confidence']
        features = decision.get('features', {})
        
        is_correct = (predicted == expected)
        if is_correct:
            correct += 1
        else:
            if predicted == 'fast' and expected == 'capable':
                false_negatives += 1
            elif predicted == 'capable' and expected == 'fast':
                false_positives += 1
        
        status = "✅" if is_correct else "❌"
        print(f"\n{status} Test {i}: {complexity_type.upper()}")
        print(f"  Prompt: {prompt[:80]}...")
        print(f"  Expected: {expected.upper()} | Predicted: {predicted.upper()} | Conf: {confidence:.3f}")
        if not is_correct:
            print(f"  Reason: {decision['reason'][:100]}")
        if features:
            print(f"  Features: {json.dumps(features)}")
    
    accuracy = (correct / total) * 100
    fp_rate = (false_positives / total) * 100
    fn_rate = (false_negatives / total) * 100
    
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Total prompts: {total}")
    print(f"Correct predictions: {correct}")
    print(f"Accuracy: {accuracy:.2f}%")
    print(f"False Positives (Simple → Capable): {false_positives} ({fp_rate:.2f}%)")
    print(f"False Negatives (Complex → Fast): {false_negatives} ({fn_rate:.2f}%)")

if __name__ == "__main__":
    run_poc()