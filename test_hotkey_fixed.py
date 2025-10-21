"""
Simple Test - Verifies Ctrl+Shift+T Detection
"""

import sys
sys.path.insert(0, 'src')

from pynput import keyboard

print("="*60)
print("HOTKEY DETECTION TEST (FIXED VERSION)")
print("="*60)
print("\n✓ Fixed: Now detects Ctrl+Shift+T properly!")
print("\nInstructions:")
print("  1. Press Ctrl+Shift+T")
print("  2. Watch for '✅ HOTKEY DETECTED'")
print("  3. Press ESC to exit\n")
print("-"*60)

current_keys = set()
detected_count = 0

def check_hotkey_pressed():
    """Check if Ctrl+Shift+T is currently pressed"""
    # Check for Ctrl (left or right or generic)
    has_ctrl = any(k == keyboard.Key.ctrl or k == keyboard.Key.ctrl_l or k == keyboard.Key.ctrl_r for k in current_keys)
    
    # Check for Shift (left or right or generic)  
    has_shift = any(k == keyboard.Key.shift or k == keyboard.Key.shift_l or k == keyboard.Key.shift_r for k in current_keys)
    
    # Check for T key - multiple ways
    has_t = False
    for k in current_keys:
        if hasattr(k, 'char'):
            if k.char in ['\x14', 't', 'T']:
                has_t = True
                break
        elif k in ['\x14', 't', 'T']:
            has_t = True
            break
    
    return has_ctrl and has_shift and has_t

def on_press(key):
    global current_keys, detected_count
    current_keys.add(key)
    
    # Check components
    has_ctrl = any(k == keyboard.Key.ctrl or k == keyboard.Key.ctrl_l or k == keyboard.Key.ctrl_r for k in current_keys)
    has_shift = any(k == keyboard.Key.shift or k == keyboard.Key.shift_l or k == keyboard.Key.shift_r for k in current_keys)
    
    # Check for T - try different approaches
    has_t = False
    for k in current_keys:
        # Check if it's a KeyCode with char
        if hasattr(k, 'char') and k.char == '\x14':
            has_t = True
            break
        # Check if it's the string itself
        if k == '\x14':
            has_t = True
            break
        # Check if it's a KeyCode for 't' or 'T'
        if hasattr(k, 'char') and k.char in ['t', 'T']:
            has_t = True
            break
    
    # Print status for debugging
    if has_ctrl and has_shift and repr(key) in ["'\\x14'", "'t'", "'T'"]:
        print(f"\n[Ctrl+Shift+T!  has_t={has_t}, key={repr(key)}, type={type(key)}]")
        if hasattr(key, 'char'):
            print(f"  key.char={repr(key.char)}")
    
    # Check if hotkey is pressed
    if check_hotkey_pressed():
        detected_count += 1
        print(f"\n{'='*60}")
        print(f"✅ HOTKEY DETECTED #{detected_count}: Ctrl+Shift+T")
        print(f"   Keys pressed: {current_keys}")
        print(f"{'='*60}\n")
    
    if key == keyboard.Key.esc:
        print("\n" + "-"*60)
        print(f"Test complete! Detected {detected_count} time(s)")
        print("-"*60)
        return False

def on_release(key):
    global current_keys
    if key in current_keys:
        current_keys.remove(key)

print("Listening for keystrokes...")
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
