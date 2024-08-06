import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

# Print sys.path to see the list of paths where Python looks for modules
print(sys.path)

from src.conf.config import Settings

def test_settings_loading():
    settings = Settings()
    assert settings.secret_key == "your_secret_key" 
    # Add more assertions to test different settings

# If you need to initialize and print settings for debug
if __name__ == "__main__":
    settings = Settings()
    print(settings.dict())
