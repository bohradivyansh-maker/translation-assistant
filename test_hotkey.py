"""
Debug Hotkey Test
Tests if hotkey detection is working
"""

import sys
sys.path.insert(0, 'src')

from pynput import keyboard
import time

print("="*60)
print("HOTKEY DEBUG TEST")
print("="*60)
print("\nPress Ctrl+Shift+T to test hotkey detection")
print("Press ESC to exit\n")

hotkey = {keyboard.Key.ctrl, keyboard.Key.shift, keyboard.KeyCode.from_char('t')}
current_keys = set()

def on_press(key):
    """Handle key press"""
    global current_keys
    current_keys.add(key)
    
    print(f"Key pressed: {key}")
    print(f"Current keys: {current_keys}")
    
    # Check if hotkey is pressed
    if hotkey.issubset(current_keys):
        print("\n" + "="*60)
        print("✅ HOTKEY DETECTED: Ctrl+Shift+T")
        print("="*60 + "\n")
    
    # Exit on ESC
    if key == keyboard.Key.esc:
        print("\nExiting...")
        return False

def on_release(key):
    """Handle key release"""
    global current_keys
    if key in current_keys:
        current_keys.remove(key)
    print(f"Key released: {key}")

# Start listener
print("Starting keyboard listener...")
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()

print("\nTest complete!")
