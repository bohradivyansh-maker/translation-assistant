"""
System Tray Icon Handler
Provides easy way to exit the application
"""

import logging
from pynput import keyboard
import threading
import tkinter as tk
from tkinter import Menu
import os
import sys

logger = logging.getLogger(__name__)


class SystemTrayIcon:
    """
    System tray icon with menu for easy app control
    """
    
    def __init__(self, on_exit_callback):
        """
        Initialize system tray icon
        
        Args:
            on_exit_callback: Function to call when user wants to exit
        """
        self.on_exit_callback = on_exit_callback
        self.root = None
        self.icon_window = None
        self.exit_listener = None
        self.is_running = True
        
        # Start exit hotkey listener (Ctrl+Shift+Q)
        self._start_exit_hotkey()
        
        logger.info("System tray initialized with exit hotkey Ctrl+Shift+Q")
    
    def _start_exit_hotkey(self):
        """Start listening for Ctrl+Shift+Q to exit"""
        self.current_keys = set()
        
        def on_press(key):
            try:
                self.current_keys.add(key)
                if self._is_exit_hotkey():
                    logger.info("Exit hotkey detected (Ctrl+Shift+Q)")
                    self.exit_application()
            except Exception as e:
                logger.error(f"Error in exit hotkey handler: {e}")
        
        def on_release(key):
            try:
                self.current_keys.discard(key)
            except Exception as e:
                pass
        
        self.exit_listener = keyboard.Listener(
            on_press=on_press,
            on_release=on_release
        )
        self.exit_listener.start()
    
    def _is_exit_hotkey(self):
        """Check if Ctrl+Shift+Q is pressed"""
        try:
            # Check for Ctrl
            has_ctrl = any(
                k == keyboard.Key.ctrl or k == keyboard.Key.ctrl_l or k == keyboard.Key.ctrl_r
                for k in self.current_keys
            )
            
            # Check for Shift
            has_shift = any(
                k == keyboard.Key.shift or k == keyboard.Key.shift_l or k == keyboard.Key.shift_r
                for k in self.current_keys
            )
            
            # Check for Q (both uppercase and lowercase, and control character)
            has_q = any(
                (hasattr(k, 'char') and k.char in ['q', 'Q', '\x11'])
                for k in self.current_keys
            )
            
            return has_ctrl and has_shift and has_q
            
        except Exception as e:
            logger.error(f"Error checking exit hotkey: {e}")
            return False
    
    def show_status_window(self):
        """Show a small status window indicating the app is running"""
        try:
            self.root = tk.Tk()
            self.root.title("Translation Assistant")
            
            # Make window small and unobtrusive
            window_width = 350
            window_height = 120
            
            # Position in bottom-right corner
            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()
            x = screen_width - window_width - 20
            y = screen_height - window_height - 70
            
            self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
            self.root.configure(bg='#2b2b2b')
            
            # Make it stay on top initially, then allow hiding
            self.root.attributes('-topmost', False)
            
            # Add icon and status
            status_frame = tk.Frame(self.root, bg='#2b2b2b')
            status_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)
            
            # Status indicator
            status_label = tk.Label(
                status_frame,
                text="🟢 Translation Assistant Running",
                font=('Segoe UI', 11, 'bold'),
                bg='#2b2b2b',
                fg='#4CAF50'
            )
            status_label.pack(pady=(0, 8))
            
            # Instructions
            instructions = tk.Label(
                status_frame,
                text="Press Ctrl+Shift+T to translate\nPress Ctrl+Shift+Q to exit",
                font=('Segoe UI', 9),
                bg='#2b2b2b',
                fg='#e0e0e0',
                justify=tk.CENTER
            )
            instructions.pack(pady=(0, 8))
            
            # Button frame
            button_frame = tk.Frame(status_frame, bg='#2b2b2b')
            button_frame.pack()
            
            # Minimize button
            minimize_btn = tk.Button(
                button_frame,
                text="Minimize",
                command=self.root.iconify,
                bg='#3c3c3c',
                fg='white',
                font=('Segoe UI', 9),
                relief=tk.FLAT,
                padx=15,
                pady=3,
                cursor='hand2'
            )
            minimize_btn.pack(side=tk.LEFT, padx=5)
            
            # Exit button
            exit_btn = tk.Button(
                button_frame,
                text="Exit App",
                command=self.exit_application,
                bg='#c62828',
                fg='white',
                font=('Segoe UI', 9, 'bold'),
                relief=tk.FLAT,
                padx=15,
                pady=3,
                cursor='hand2'
            )
            exit_btn.pack(side=tk.LEFT, padx=5)
            
            # Hover effects
            def on_enter_minimize(e):
                minimize_btn.config(bg='#4c4c4c')
            def on_leave_minimize(e):
                minimize_btn.config(bg='#3c3c3c')
            
            def on_enter_exit(e):
                exit_btn.config(bg='#d32f2f')
            def on_leave_exit(e):
                exit_btn.config(bg='#c62828')
            
            minimize_btn.bind('<Enter>', on_enter_minimize)
            minimize_btn.bind('<Leave>', on_leave_minimize)
            exit_btn.bind('<Enter>', on_enter_exit)
            exit_btn.bind('<Leave>', on_leave_exit)
            
            # Handle window close button
            self.root.protocol("WM_DELETE_WINDOW", self.root.iconify)
            
            logger.info("Status window displayed")
            
            # Start the GUI loop
            self.root.mainloop()
            
        except Exception as e:
            logger.error(f"Error showing status window: {e}", exc_info=True)
    
    def exit_application(self):
        """Exit the application gracefully"""
        try:
            logger.info("Exiting application...")
            self.is_running = False
            
            # Stop exit hotkey listener
            if self.exit_listener:
                self.exit_listener.stop()
            
            # Close status window
            if self.root:
                self.root.quit()
                self.root.destroy()
            
            # Call the exit callback
            if self.on_exit_callback:
                self.on_exit_callback()
            
            # Force exit
            os._exit(0)
            
        except Exception as e:
            logger.error(f"Error during exit: {e}")
            os._exit(0)
    
    def run(self):
        """Run the system tray in main thread"""
        try:
            self.show_status_window()
        except Exception as e:
            logger.error(f"Error running system tray: {e}", exc_info=True)
