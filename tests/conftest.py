import sys
import os

# Add stubs path first (for external deps like litellm, openai, gepa)
stubs_path = os.path.join(os.path.dirname(__file__), '..', 'ai_earth', 'lego', 'stubs')
sys.path.insert(0, stubs_path)

# Add lego path (for real extracted packages: evoagentx, dspy)
lego_path = os.path.join(os.path.dirname(__file__), '..', 'ai_earth', 'lego')
sys.path.insert(0, lego_path)
