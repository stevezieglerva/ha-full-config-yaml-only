#!/usr/bin/env python3

import sys
import re

def check_entities_in_config(file_path):
    """Check that the Alexa Cool Count entities are properly defined in the config."""
    with open(file_path, 'r') as f:
        content = f.read()
    
    required_strings = [
        "Alexa Cool Upstairs Count",
        "Alexa Cool Downstairs Count",
        "input_boolean.alexa_cool_upstairs",
        "input_boolean.alexa_cool_downstairs",
        "Today's Alexa Cool Commands"
    ]
    
    all_found = True
    for s in required_strings:
        if s not in content:
            print(f"❌ Missing required configuration: '{s}'")
            all_found = False
        else:
            print(f"✅ Found required configuration: '{s}'")
    
    return all_found

if __name__ == "__main__":
    config_file = "/Users/sziegler/Documents/GitHub/ha-full-config-yaml-only/configuration.yaml"
    
    # Check that required entities are defined
    if not check_entities_in_config(config_file):
        sys.exit(1)
    
    print("\n✅ All tests passed! The Alexa Cool Count feature appears to be correctly implemented.")
    sys.exit(0)