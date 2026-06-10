import sys
import os

# Add lego first for real code (evoagentx, dspy, mem0)
lego_path = os.path.join(os.path.dirname(__file__), '..', 'ai_earth', 'lego')
sys.path.insert(0, lego_path)

# Stubs at END — only used for packages NOT already installed
stubs_path = os.path.join(os.path.dirname(__file__), '..', 'ai_earth', 'lego', 'stubs')
sys.path.append(stubs_path)
