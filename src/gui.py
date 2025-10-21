"""
GUI Module
Creates popup translation window using Tkinter
Displays near cursor with translation results and controls
"""

import logging
import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional, Callable, Dict
import pyperclip

logger = logging.getLogger(__name__)


class TranslationPopup:
    """
    Popup window for displaying translation results
    """
    
    def __init__(
        self,
        on_copy: Optional[Callable] = None,
        on_speak: Optional[Callable] = None,
        on_save: Optional[Callable] = None
    ):
        """
        Initialize translation popup
        
        Args:
            on_copy: Callback when copy button clicked
            on_speak: Callback when speak button clicked
            on_save: Callback when save to dictionary button clicked
        """
        self.on_copy = on_copy
        self.on_speak = on_speak
        self.on_save = on_save
        
        self.root = None
        self.is_visible = False
        
        logger.info("Translation popup initialized")
    
    def show(
        self,
        original_text: str,
        translated_text: str,
        source_lang: str,
        target_lang: str,
        position: tuple = (100, 100),
        metadata: Optional[Dict] = None
    ):
        """
        Show translation popup
        
        Args:
            original_text: Original text
            translated_text: Translated text
            source_lang: Source language code
            target_lang: Target language code
            position: (x, y) position to display popup
            metadata: Additional metadata to display
        """
        try:
            # Close existing window if any
            self.close()
            
            # Create new window
            self.root = tk.Tk()
            self.root.title("Translation Assistant")
            
            # Window configuration
            self.root.overrideredirect(True)  # Remove title bar
            self.root.attributes('-topmost', True)  # Always on top
            self.root.configure(bg='#2b2b2b')
            
            # Set position near cursor
            x, y = position
            # Offset to avoid cursor
            x += 20
            y += 20
            
            # Main frame
            main_frame = tk.Frame(self.root, bg='#2b2b2b', padx=10, pady=10)
            main_frame.pack(fill='both', expand=True)
            
            # Title bar (for dragging)
            title_frame = tk.Frame(main_frame, bg='#1e1e1e', height=30)
            title_frame.pack(fill='x', pady=(0, 10))
            
            title_label = tk.Label(
                title_frame,
                text=f"  🌐 Translation: {source_lang.upper()} → {target_lang.upper()}",
                bg='#1e1e1e',
                fg='#ffffff',
                font=('Segoe UI', 10, 'bold'),
                anchor='w'
            )
            title_label.pack(side='left', fill='x', expand=True, pady=5)
            
            # Close button
            close_btn = tk.Button(
                title_frame,
                text="✕",
                command=self.close,
                bg='#1e1e1e',
                fg='#ffffff',
                font=('Segoe UI', 12),
                relief='flat',
                cursor='hand2',
                width=3
            )
            close_btn.pack(side='right', padx=5)
            
            # Make title bar draggable
            title_frame.bind('<Button-1>', self._start_drag)
            title_frame.bind('<B1-Motion>', self._on_drag)
            title_label.bind('<Button-1>', self._start_drag)
            title_label.bind('<B1-Motion>', self._on_drag)
            
            # Original text section
            original_label = tk.Label(
                main_frame,
                text="Original:",
                bg='#2b2b2b',
                fg='#888888',
                font=('Segoe UI', 9),
                anchor='w'
            )
            original_label.pack(fill='x', pady=(0, 5))
            
            original_frame = tk.Frame(main_frame, bg='#1e1e1e', relief='solid', borderwidth=1)
            original_frame.pack(fill='x', pady=(0, 10))
            
            original_text_widget = tk.Text(
                original_frame,
                bg='#1e1e1e',
                fg='#cccccc',
                font=('Segoe UI', 10),
                wrap='word',
                height=3,
                relief='flat',
                padx=10,
                pady=8
            )
            original_text_widget.pack(fill='both', expand=True)
            original_text_widget.insert('1.0', original_text)
            original_text_widget.config(state='disabled')
            
            # Translation section
            translation_label = tk.Label(
                main_frame,
                text="Translation:",
                bg='#2b2b2b',
                fg='#888888',
                font=('Segoe UI', 9),
                anchor='w'
            )
            translation_label.pack(fill='x', pady=(0, 5))
            
            translation_frame = tk.Frame(main_frame, bg='#1e1e1e', relief='solid', borderwidth=1)
            translation_frame.pack(fill='x', pady=(0, 10))
            
            translation_text_widget = tk.Text(
                translation_frame,
                bg='#1e1e1e',
                fg='#4ec9b0',
                font=('Segoe UI', 11, 'bold'),
                wrap='word',
                height=3,
                relief='flat',
                padx=10,
                pady=8
            )
            translation_text_widget.pack(fill='both', expand=True)
            translation_text_widget.insert('1.0', translated_text)
            translation_text_widget.config(state='disabled')
            
            # Metadata section (if provided)
            if metadata:
                self._add_metadata_section(main_frame, metadata)
            
            # Button frame
            button_frame = tk.Frame(main_frame, bg='#2b2b2b')
            button_frame.pack(fill='x', pady=(10, 0))
            
            # Copy button
            copy_btn = tk.Button(
                button_frame,
                text="📋 Copy",
                command=lambda: self._on_copy_click(translated_text),
                bg='#0e639c',
                fg='#ffffff',
                font=('Segoe UI', 10),
                relief='flat',
                cursor='hand2',
                padx=15,
                pady=8
            )
            copy_btn.pack(side='left', padx=(0, 5))
            
            # Speak button
            speak_btn = tk.Button(
                button_frame,
                text="🔊 Speak",
                command=lambda: self._on_speak_click(translated_text, target_lang),
                bg='#0e639c',
                fg='#ffffff',
                font=('Segoe UI', 10),
                relief='flat',
                cursor='hand2',
                padx=15,
                pady=8
            )
            speak_btn.pack(side='left', padx=(0, 5))
            
            # Save button
            save_btn = tk.Button(
                button_frame,
                text="💾 Save",
                command=lambda: self._on_save_click(original_text, translated_text, source_lang, target_lang),
                bg='#0e639c',
                fg='#ffffff',
                font=('Segoe UI', 10),
                relief='flat',
                cursor='hand2',
                padx=15,
                pady=8
            )
            save_btn.pack(side='left', padx=(0, 5))
            
            # Update window size
            self.root.update_idletasks()
            width = self.root.winfo_reqwidth()
            height = self.root.winfo_reqheight()
            
            # Ensure window fits on screen
            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()
            
            if x + width > screen_width:
                x = screen_width - width - 20
            if y + height > screen_height:
                y = screen_height - height - 20
            
            self.root.geometry(f"{width}x{height}+{x}+{y}")
            
            # Bind escape key to close
            self.root.bind('<Escape>', lambda e: self.close())
            
            # Focus on window
            self.root.focus_force()
            
            self.is_visible = True
            logger.info(f"Popup shown at ({x}, {y})")
            
            # Start main loop
            self.root.mainloop()
            
        except Exception as e:
            logger.error(f"Error showing popup: {e}")
            if self.root:
                self.root.destroy()
    
    def _add_metadata_section(self, parent, metadata: Dict):
        """Add metadata information section"""
        try:
            metadata_frame = tk.Frame(parent, bg='#2b2b2b')
            metadata_frame.pack(fill='x', pady=(5, 5))
            
            info_text = []
            
            if 'domain' in metadata:
                info_text.append(f"Domain: {metadata['domain'].title()}")
            
            if 'confidence' in metadata:
                conf = metadata['confidence']
                info_text.append(f"Confidence: {conf:.1%}")
            
            if 'entities' in metadata and metadata['entities']:
                entity_count = len(metadata['entities'])
                info_text.append(f"Entities preserved: {entity_count}")
            
            if info_text:
                info_label = tk.Label(
                    metadata_frame,
                    text=" | ".join(info_text),
                    bg='#2b2b2b',
                    fg='#888888',
                    font=('Segoe UI', 8)
                )
                info_label.pack()
                
        except Exception as e:
            logger.error(f"Error adding metadata: {e}")
    
    def _start_drag(self, event):
        """Start window drag"""
        self._drag_start_x = event.x
        self._drag_start_y = event.y
    
    def _on_drag(self, event):
        """Handle window dragging"""
        if self.root:
            x = self.root.winfo_x() + event.x - self._drag_start_x
            y = self.root.winfo_y() + event.y - self._drag_start_y
            self.root.geometry(f"+{x}+{y}")
    
    def _on_copy_click(self, text: str):
        """Handle copy button click"""
        try:
            pyperclip.copy(text)
            logger.info("Text copied to clipboard")
            
            if self.on_copy:
                self.on_copy(text)
            
            # Show brief confirmation
            messagebox.showinfo("Copied", "Translation copied to clipboard!", parent=self.root)
            
        except Exception as e:
            logger.error(f"Error copying text: {e}")
    
    def _on_speak_click(self, text: str, lang: str):
        """Handle speak button click"""
        try:
            logger.info(f"Speak requested: {text[:30]}...")
            
            if self.on_speak:
                self.on_speak(text, lang)
            
        except Exception as e:
            logger.error(f"Error in speak callback: {e}")
    
    def _on_save_click(self, original: str, translation: str, source_lang: str, target_lang: str):
        """Handle save button click"""
        try:
            logger.info("Save to dictionary requested")
            
            if self.on_save:
                self.on_save(original, translation, source_lang, target_lang)
            
            messagebox.showinfo("Saved", "Added to user dictionary!", parent=self.root)
            
        except Exception as e:
            logger.error(f"Error in save callback: {e}")
    
    def close(self):
        """Close popup window"""
        if self.root:
            try:
                self.root.quit()
                self.root.destroy()
                self.root = None
                self.is_visible = False
                logger.info("Popup closed")
            except Exception as e:
                logger.error(f"Error closing popup: {e}")


# Example usage and testing
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    def on_copy_handler(text):
        print(f"Copy clicked: {text}")
    
    def on_speak_handler(text, lang):
        print(f"Speak clicked: {text} (lang: {lang})")
    
    def on_save_handler(original, translation, source_lang, target_lang):
        print(f"Save clicked: {original} -> {translation}")
    
    # Create popup
    popup = TranslationPopup(
        on_copy=on_copy_handler,
        on_speak=on_speak_handler,
        on_save=on_save_handler
    )
    
    # Show popup with test data
    popup.show(
        original_text="Hello, how are you today?",
        translated_text="Hola, ¿cómo estás hoy?",
        source_lang="en",
        target_lang="es",
        position=(200, 200),
        metadata={
            'domain': 'casual',
            'confidence': 0.95,
            'entities': ['John']
        }
    )
