"""
Hotkey Handler Module
Manages global hotkey detection (Ctrl+Shift+T) and clipboard monitoring
Works across all Windows applications
"""

import logging
import threading
import time
from typing import Callable, Optional
from pynput import keyboard
import pyperclip
import pyautogui

logger = logging.getLogger(__name__)


class HotkeyHandler:
    """
    Handles global hotkey detection and clipboard monitoring
    """
    
    def __init__(self, hotkey_callback: Optional[Callable] = None):
        """
        Initialize hotkey handler
        
        Args:
            hotkey_callback: Function to call when hotkey is triggered
        """
        self.hotkey_callback = hotkey_callback
        self.listener = None
        self.is_running = False
        
        # Hotkey combination: Ctrl+Shift+T
        # Note: pynput may send Key.ctrl, Key.ctrl_l, or Key.ctrl_r
        self.current_keys = set()
        
        # Clipboard monitoring
        self.last_clipboard = ""
        self.clipboard_history = []
        self.max_history = 10
        
        logger.info("Hotkey handler initialized")
    
    def _is_hotkey_pressed(self):
        """Check if Ctrl+Shift+T hotkey is currently pressed"""
        # Check for Ctrl (left, right, or generic)
        has_ctrl = any(k == keyboard.Key.ctrl or k == keyboard.Key.ctrl_l or k == keyboard.Key.ctrl_r 
                      for k in self.current_keys)
        
        # Check for Shift (left, right, or generic)
        has_shift = any(k == keyboard.Key.shift or k == keyboard.Key.shift_l or k == keyboard.Key.shift_r 
                       for k in self.current_keys)
        
        # Check for T key - pynput sends KeyCode objects with .char attribute
        has_t = False
        for k in self.current_keys:
            if hasattr(k, 'char'):
                # KeyCode with char attribute - check for '\x14' (Ctrl+T), 't', or 'T'
                if k.char in ['\x14', 't', 'T']:
                    has_t = True
                    break
            elif k in ['\x14', 't', 'T']:
                # Direct string comparison fallback
                has_t = True
                break
        
        return has_ctrl and has_shift and has_t
    
    def on_press(self, key):
        """Handle key press event"""
        try:
            self.current_keys.add(key)
            
            # Check if hotkey combination is pressed
            if self._is_hotkey_pressed():
                self._trigger_hotkey()
                
        except Exception as e:
            logger.error(f"Key press error: {e}")
    
    def on_release(self, key):
        """Handle key release event"""
        try:
            if key in self.current_keys:
                self.current_keys.remove(key)
        except Exception as e:
            logger.error(f"Key release error: {e}")
    
    def _trigger_hotkey(self):
        """Execute hotkey callback"""
        logger.info("Hotkey triggered: Ctrl+Shift+T")
        
        if self.hotkey_callback:
            try:
                # Get selected text from clipboard
                selected_text = self.get_selected_text()
                
                # Get cursor position for popup placement
                cursor_pos = self.get_cursor_position()
                
                # Call the callback with text and position
                self.hotkey_callback(selected_text, cursor_pos)
                
            except Exception as e:
                logger.error(f"Hotkey callback error: {e}")
    
    def get_selected_text(self) -> str:
        """
        Get currently selected text by simulating Ctrl+C
        
        Returns:
            Selected text from clipboard
        """
        try:
            # Store current clipboard content
            original_clipboard = pyperclip.paste()
            
            # Clear clipboard
            pyperclip.copy("")
            
            # Small delay to ensure clipboard is cleared
            time.sleep(0.05)
            
            # Simulate Ctrl+C to copy selected text
            pyautogui.hotkey('ctrl', 'c')
            
            # Small delay to ensure copy operation completes
            time.sleep(0.1)
            
            # Get the new clipboard content
            selected_text = pyperclip.paste()
            
            # If nothing was selected, restore original clipboard
            if not selected_text or selected_text == "":
                pyperclip.copy(original_clipboard)
                logger.warning("No text selected")
                return ""
            
            # Store in history
            self._add_to_history(selected_text)
            
            logger.info(f"Selected text retrieved: {selected_text[:50]}...")
            return selected_text
            
        except Exception as e:
            logger.error(f"Error getting selected text: {e}")
            return ""
    
    def get_cursor_position(self) -> tuple:
        """
        Get current cursor position
        
        Returns:
            Tuple of (x, y) coordinates
        """
        try:
            position = pyautogui.position()
            logger.debug(f"Cursor position: {position}")
            return position
        except Exception as e:
            logger.error(f"Error getting cursor position: {e}")
            return (100, 100)  # Default position
    
    def _add_to_history(self, text: str):
        """Add text to clipboard history"""
        if text and text != self.last_clipboard:
            self.clipboard_history.append(text)
            
            # Maintain max history size
            if len(self.clipboard_history) > self.max_history:
                self.clipboard_history.pop(0)
            
            self.last_clipboard = text
    
    def get_clipboard_history(self) -> list:
        """Get clipboard history"""
        return self.clipboard_history.copy()
    
    def get_clipboard_context(self, num_items: int = 3) -> str:
        """
        Get context from clipboard history
        
        Args:
            num_items: Number of previous clipboard items to include
            
        Returns:
            Combined context string
        """
        if not self.clipboard_history:
            return ""
        
        # Get last N items (excluding the most recent one)
        context_items = self.clipboard_history[-(num_items + 1):-1]
        return " ".join(context_items)
    
    def start(self):
        """Start listening for hotkeys"""
        if self.is_running:
            logger.warning("Hotkey listener already running")
            return
        
        try:
            self.listener = keyboard.Listener(
                on_press=self.on_press,
                on_release=self.on_release
            )
            self.listener.start()
            self.is_running = True
            logger.info("Hotkey listener started (Ctrl+Shift+T)")
            
        except Exception as e:
            logger.error(f"Error starting hotkey listener: {e}")
            self.is_running = False
    
    def stop(self):
        """Stop listening for hotkeys"""
        if self.listener:
            self.listener.stop()
            self.is_running = False
            logger.info("Hotkey listener stopped")
    
    def set_callback(self, callback: Callable):
        """Set or update hotkey callback function"""
        self.hotkey_callback = callback
        logger.info("Hotkey callback updated")


class ClipboardMonitor:
    """
    Monitors clipboard for changes (optional feature)
    """
    
    def __init__(self, callback: Optional[Callable] = None):
        """
        Initialize clipboard monitor
        
        Args:
            callback: Function to call when clipboard changes
        """
        self.callback = callback
        self.is_monitoring = False
        self.last_content = ""
        self.monitor_thread = None
        
        logger.info("Clipboard monitor initialized")
    
    def _monitor_loop(self):
        """Main monitoring loop"""
        while self.is_monitoring:
            try:
                current_content = pyperclip.paste()
                
                if current_content != self.last_content:
                    self.last_content = current_content
                    
                    if self.callback and current_content:
                        self.callback(current_content)
                
                time.sleep(0.5)  # Check every 500ms
                
            except Exception as e:
                logger.error(f"Clipboard monitoring error: {e}")
                time.sleep(1)
    
    def start(self):
        """Start monitoring clipboard"""
        if self.is_monitoring:
            return
        
        self.is_monitoring = True
        self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.monitor_thread.start()
        logger.info("Clipboard monitoring started")
    
    def stop(self):
        """Stop monitoring clipboard"""
        self.is_monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=2)
        logger.info("Clipboard monitoring stopped")


# Example usage and testing
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    def test_callback(text, position):
        """Test callback function"""
        print(f"\n{'='*50}")
        print(f"Hotkey triggered!")
        print(f"Position: {position}")
        print(f"Selected text: {text}")
        print(f"{'='*50}\n")
    
    # Initialize handler
    handler = HotkeyHandler(hotkey_callback=test_callback)
    
    print("Hotkey handler test")
    print("Press Ctrl+Shift+T after selecting some text")
    print("Press Ctrl+C to exit")
    print("-" * 50)
    
    # Start listening
    handler.start()
    
    try:
        # Keep running
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping...")
        handler.stop()
