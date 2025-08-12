#!/usr/bin/env python3
import re
import sys
import os

def test_yaml_key_value_inline(file_path, key_value_pairs):
    """
    Test that specified YAML keys have values on the same line.
    
    Args:
        file_path: Path to the YAML file to check
        key_value_pairs: List of dictionaries with 'key' and 'value' fields
    
    Returns:
        True if all patterns match, False otherwise
    """
    try:
        if not os.path.exists(file_path):
            print(f"ERROR: File not found: {file_path}")
            return False
            
        with open(file_path, 'r') as file:
            content = file.readlines()
        
        all_matched = True
        for pair in key_value_pairs:
            key = pair['key']
            value = pair['value']
            
            # Pattern to match key and value on the same line
            pattern = f"^\s*{re.escape(key)}\s*{re.escape(value)}.*$"
            
            found = False
            line_num = 0
            for i, line in enumerate(content):
                line_num = i + 1
                line = line.strip()
                if re.match(pattern, line):
                    print(f"PASS: '{key} {value}' is correctly formatted on a single line (line {line_num})")
                    found = True
                    break
            
            if not found:
                print(f"ERROR: '{key} {value}' was not found on a single line in {file_path}")
                
                # Search for the key by itself to provide more diagnostics
                key_pattern = f"^\s*{re.escape(key)}.*$"
                for i, line in enumerate(content):
                    line_num = i + 1
                    line = line.strip()
                    if re.match(key_pattern, line):
                        print(f"  Found key '{key}' on line {line_num}: '{line}'")
                        
                all_matched = False
        
        return all_matched
    
    except Exception as e:
        print(f"Error testing file {file_path}: {str(e)}")
        return False

if __name__ == "__main__":
    # Allow specifying file path as command-line argument
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
    else:
        file_path = "/Users/sziegler/Documents/GitHub/ha-full-config-yaml-only/configuration.yaml"
    
    print(f"Testing file: {file_path}")
    
    # Key-value pairs to check
    key_value_pairs = [
        {"key": "automation:", "value": "!include automations.yaml"},
        {"key": "script:", "value": "!include scripts.yaml"},
        {"key": "scene:", "value": "!include scenes.yaml"}
    ]
    
    success = test_yaml_key_value_inline(file_path, key_value_pairs)
    
    if success:
        print("\nALL TESTS PASSED: All keys have values on the same line!")
        sys.exit(0)
    else:
        print("\nTEST FAILED: Some keys do not have values on the same line.")
        sys.exit(1)