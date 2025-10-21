"""
Language Selector Popup
Quick language selection before translation
"""

import tkinter as tk
from tkinter import ttk
from typing import Optional, Callable
import logging

logger = logging.getLogger(__name__)


class LanguageSelector:
    """
    Quick popup to select target language
    """
    
    # Popular languages (with English first!)
    LANGUAGES = {
        'en': '🇬🇧 English',
        'es': '🇪🇸 Spanish',
        'fr': '🇫🇷 French',
        'de': '🇩🇪 German',
        'hi': '🇮🇳 Hindi',
        'ja': '🇯🇵 Japanese',
        'zh-cn': '🇨🇳 Chinese',
        'ar': '🇸🇦 Arabic',
        'pt': '🇵🇹 Portuguese',
        'ru': '🇷🇺 Russian',
        'it': '🇮🇹 Italian',
        'ko': '🇰🇷 Korean',
        'tr': '🇹🇷 Turkish',
        'nl': '🇳🇱 Dutch',
        'pl': '🇵🇱 Polish',
        'vi': '🇻🇳 Vietnamese'
    }
    
    def __init__(self, default_lang: str = 'es'):
        """
        Initialize language selector
        
        Args:
            default_lang: Default language code
        """
        self.default_lang = default_lang
        self.selected_lang = default_lang
        self.root = None
        
    def show(self, position: tuple = (100, 100), callback: Optional[Callable] = None):
        """
        Show language selector popup
        
        Args:
            position: (x, y) position to display
            callback: Function to call with selected language
        """
        try:
            # Create popup window
            self.root = tk.Tk()
            self.root.title("Select Language")
            self.root.overrideredirect(True)
            self.root.attributes('-topmost', True)
            self.root.configure(bg='#2b2b2b')
            
            # Position near cursor
            x, y = position
            x += 20
            y += 20
            self.root.geometry(f"+{x}+{y}")
            
            # Main frame
            main_frame = tk.Frame(self.root, bg='#2b2b2b', padx=15, pady=15)
            main_frame.pack(fill='both', expand=True)
            
            # Title
            title = tk.Label(
                main_frame,
                text="🌐 Select Target Language",
                bg='#2b2b2b',
                fg='#ffffff',
                font=('Segoe UI', 12, 'bold')
            )
            title.pack(pady=(0, 10))
            
            # Language buttons frame (2 columns)
            buttons_frame = tk.Frame(main_frame, bg='#2b2b2b')
            buttons_frame.pack(fill='both', expand=True)
            
            # Create buttons for each language
            row = 0
            col = 0
            for lang_code, lang_name in self.LANGUAGES.items():
                btn = tk.Button(
                    buttons_frame,
                    text=lang_name,
                    bg='#3c3c3c' if lang_code != self.default_lang else '#0078d4',
                    fg='#ffffff',
                    font=('Segoe UI', 10),
                    width=18,
                    height=1,
                    bd=0,
                    relief='flat',
                    cursor='hand2',
                    command=lambda lc=lang_code: self._on_select(lc, callback)
                )
                btn.grid(row=row, column=col, padx=3, pady=3, sticky='ew')
                
                # Hover effects
                btn.bind('<Enter>', lambda e, b=btn, lc=lang_code: 
                        b.configure(bg='#0078d4' if lc != self.default_lang else '#005a9e'))
                btn.bind('<Leave>', lambda e, b=btn, lc=lang_code: 
                        b.configure(bg='#3c3c3c' if lc != self.default_lang else '#0078d4'))
                
                col += 1
                if col > 1:  # 2 columns
                    col = 0
                    row += 1
            
            # Bottom info
            info = tk.Label(
                main_frame,
                text="Or press ESC to use default language",
                bg='#2b2b2b',
                fg='#888888',
                font=('Segoe UI', 8)
            )
            info.pack(pady=(10, 0))
            
            # Keyboard shortcuts
            self.root.bind('<Escape>', lambda e: self._on_select(self.default_lang, callback))
            self.root.bind('<Return>', lambda e: self._on_select(self.default_lang, callback))
            
            # Auto-close after 10 seconds
            self.root.after(10000, lambda: self._on_select(self.default_lang, callback))
            
            # Start event loop
            self.root.mainloop()
            
        except Exception as e:
            logger.error(f"Error showing language selector: {e}")
            if callback:
                callback(self.default_lang)
    
    def _on_select(self, lang_code: str, callback: Optional[Callable]):
        """Handle language selection"""
        self.selected_lang = lang_code
        logger.info(f"Language selected: {lang_code}")
        
        # Close window
        if self.root:
            self.root.destroy()
            self.root = None
        
        # Call callback with selected language
        if callback:
            callback(lang_code)
    
    def close(self):
        """Close the selector"""
        if self.root:
            try:
                self.root.destroy()
            except:
                pass
            self.root = None


def show_language_selector(position: tuple = (100, 100), default_lang: str = 'es', callback: Optional[Callable] = None):
    """
    Quick function to show language selector
    
    Args:
        position: (x, y) position
        default_lang: Default language code
        callback: Function to call with selected language
    """
    selector = LanguageSelector(default_lang)
    selector.show(position, callback)


# Test code
if __name__ == "__main__":
    def on_lang_selected(lang):
        print(f"Selected language: {lang}")
    
    show_language_selector(callback=on_lang_selected)
