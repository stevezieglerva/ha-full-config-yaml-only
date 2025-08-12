#!/usr/bin/env python3
import re
import sys

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
        with open(file_path, 'r') as file:
            content = file.readlines()
        
        all_matched = True
        for pair in key_value_pairs:
            key = pair['key']
            value = pair['value']
            
            pattern = f"^{re.escape(key)}\s*{re.escape(value)}.*$"
            
            found = False
            for line in content:
                line = line.strip()
                if re.match(pattern, line):
                    print(f"PASS: '{key} {value}' is correctly formatted on a single line")
                    found = True
                    break
            
            if not found:
                print(f"ERROR: '{key} {value}' was not found on a single line in {file_path}")
                all_matched = False
        
        return all_matched
    
    except Exception as e:
        print(f"Error testing file {file_path}: {str(e)}")
        return False

if __name__ == "__main__":
    file_path = "/Users/sziegler/Documents/GitHub/ha-full-config-yaml-only/configuration.yaml"
    
    # Key-value pairs to check
    key_value_pairs = [
        {"key": "automation:", "value": "!include automations.yaml"},
        {"key": "script:", "value": "!include scripts.yaml"},
        {"key": "scene:", "value": "!include scenes.yaml"}
    ]
    
    success = test_yaml_key_value_inline(file_path, key_value_pairs)
    
    if success:
        print("\nAll keys have values on the same line!")
        sys.exit(0)
    else:
        print("\nSome keys do not have values on the same line.")
        sys.exit(1)