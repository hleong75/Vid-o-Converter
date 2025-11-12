#!/usr/bin/env python3
"""
Graphical User Interface for Video Converter
"""

import sys
import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
import threading
from typing import List, Optional

from .converter import VideoConverter
from .presets import get_presets_by_category, get_preset


class VideoConverterGUI:
    """Main GUI application"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Video Converter Pro")
        self.root.geometry("900x700")
        self.root.resizable(True, True)
        
        self.converter = VideoConverter()
        self.input_files: List[str] = []
        self.is_converting = False
        
        self._setup_ui()
        self._setup_styles()
    
    def _setup_styles(self):
        """Setup custom styles"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure colors
        style.configure('Title.TLabel', font=('Arial', 16, 'bold'))
        style.configure('Section.TLabel', font=('Arial', 11, 'bold'))
        style.configure('Action.TButton', font=('Arial', 10), padding=10)
    
    def _setup_ui(self):
        """Setup the user interface"""
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(3, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="Video Converter Pro", style='Title.TLabel')
        title_label.grid(row=0, column=0, pady=(0, 20))
        
        # Input section
        self._create_input_section(main_frame)
        
        # Preset section
        self._create_preset_section(main_frame)
        
        # Advanced options section
        self._create_advanced_section(main_frame)
        
        # Output section
        self._create_output_section(main_frame)
        
        # Progress section
        self._create_progress_section(main_frame)
        
        # Action buttons
        self._create_action_buttons(main_frame)
    
    def _create_input_section(self, parent):
        """Create input file selection section"""
        input_frame = ttk.LabelFrame(parent, text="Input Files", padding="10")
        input_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        input_frame.columnconfigure(0, weight=1)
        
        # File list
        list_frame = ttk.Frame(input_frame)
        list_frame.grid(row=0, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        list_frame.columnconfigure(0, weight=1)
        
        self.file_listbox = tk.Listbox(list_frame, height=5, selectmode=tk.EXTENDED)
        self.file_listbox.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.file_listbox.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.file_listbox.config(yscrollcommand=scrollbar.set)
        
        # Buttons
        btn_frame = ttk.Frame(input_frame)
        btn_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E))
        
        ttk.Button(btn_frame, text="Add Files", command=self._add_files).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(btn_frame, text="Add Folder", command=self._add_folder).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(btn_frame, text="Remove Selected", command=self._remove_files).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(btn_frame, text="Clear All", command=self._clear_files).pack(side=tk.LEFT)
    
    def _create_preset_section(self, parent):
        """Create preset selection section"""
        preset_frame = ttk.LabelFrame(parent, text="Conversion Preset", padding="10")
        preset_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        preset_frame.columnconfigure(1, weight=1)
        
        ttk.Label(preset_frame, text="Preset:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        
        # Preset selection
        self.preset_var = tk.StringVar()
        self.preset_combo = ttk.Combobox(preset_frame, textvariable=self.preset_var, state='readonly')
        self.preset_combo.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 10))
        self.preset_combo.bind('<<ComboboxSelected>>', self._on_preset_selected)
        
        # Load presets
        self._load_presets()
        
        # Description
        ttk.Label(preset_frame, text="Description:").grid(row=1, column=0, sticky=(tk.W, tk.N), padx=(0, 10), pady=(10, 0))
        
        self.preset_desc = tk.Text(preset_frame, height=3, wrap=tk.WORD, state=tk.DISABLED)
        self.preset_desc.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=(10, 0))
    
    def _create_advanced_section(self, parent):
        """Create advanced options section"""
        advanced_frame = ttk.LabelFrame(parent, text="Advanced Options (Optional)", padding="10")
        advanced_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        advanced_frame.columnconfigure(1, weight=1)
        advanced_frame.columnconfigure(3, weight=1)
        
        # Video codec
        ttk.Label(advanced_frame, text="Video Codec:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        self.video_codec_var = tk.StringVar()
        video_codec_combo = ttk.Combobox(advanced_frame, textvariable=self.video_codec_var, width=15)
        video_codec_combo['values'] = ('', 'libx264', 'libx265', 'libvpx-vp9', 'libaom-av1', 'copy')
        video_codec_combo.grid(row=0, column=1, sticky=tk.W, padx=(0, 20))
        
        # Audio codec
        ttk.Label(advanced_frame, text="Audio Codec:").grid(row=0, column=2, sticky=tk.W, padx=(0, 10))
        self.audio_codec_var = tk.StringVar()
        audio_codec_combo = ttk.Combobox(advanced_frame, textvariable=self.audio_codec_var, width=15)
        audio_codec_combo['values'] = ('', 'aac', 'libmp3lame', 'libopus', 'flac', 'copy')
        audio_codec_combo.grid(row=0, column=3, sticky=tk.W)
        
        # Resolution
        ttk.Label(advanced_frame, text="Resolution:").grid(row=1, column=0, sticky=tk.W, padx=(0, 10), pady=(10, 0))
        self.resolution_var = tk.StringVar()
        resolution_combo = ttk.Combobox(advanced_frame, textvariable=self.resolution_var, width=15)
        resolution_combo['values'] = ('', '1920x1080', '1280x720', '854x480', '640x360', '320x240')
        resolution_combo.grid(row=1, column=1, sticky=tk.W, padx=(0, 20), pady=(10, 0))
        
        # CRF
        ttk.Label(advanced_frame, text="Quality (CRF):").grid(row=1, column=2, sticky=tk.W, padx=(0, 10), pady=(10, 0))
        self.crf_var = tk.StringVar()
        crf_spin = ttk.Spinbox(advanced_frame, from_=0, to=51, textvariable=self.crf_var, width=13)
        crf_spin.grid(row=1, column=3, sticky=tk.W, pady=(10, 0))
        
        # Trim options
        ttk.Label(advanced_frame, text="Start Time:").grid(row=2, column=0, sticky=tk.W, padx=(0, 10), pady=(10, 0))
        self.start_time_var = tk.StringVar()
        ttk.Entry(advanced_frame, textvariable=self.start_time_var, width=17).grid(row=2, column=1, sticky=tk.W, padx=(0, 20), pady=(10, 0))
        
        ttk.Label(advanced_frame, text="Duration:").grid(row=2, column=2, sticky=tk.W, padx=(0, 10), pady=(10, 0))
        self.duration_var = tk.StringVar()
        ttk.Entry(advanced_frame, textvariable=self.duration_var, width=15).grid(row=2, column=3, sticky=tk.W, pady=(10, 0))
    
    def _create_output_section(self, parent):
        """Create output directory section"""
        output_frame = ttk.LabelFrame(parent, text="Output", padding="10")
        output_frame.grid(row=4, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        output_frame.columnconfigure(1, weight=1)
        
        ttk.Label(output_frame, text="Output Directory:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        
        self.output_dir_var = tk.StringVar(value=str(Path.home() / "Videos" / "Converted"))
        ttk.Entry(output_frame, textvariable=self.output_dir_var).grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 10))
        
        ttk.Button(output_frame, text="Browse", command=self._browse_output_dir).grid(row=0, column=2)
    
    def _create_progress_section(self, parent):
        """Create progress section"""
        progress_frame = ttk.LabelFrame(parent, text="Progress", padding="10")
        progress_frame.grid(row=5, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        progress_frame.columnconfigure(0, weight=1)
        
        # Status label
        self.status_label = ttk.Label(progress_frame, text="Ready")
        self.status_label.grid(row=0, column=0, sticky=tk.W, pady=(0, 10))
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_var, maximum=100)
        self.progress_bar.grid(row=1, column=0, sticky=(tk.W, tk.E))
    
    def _create_action_buttons(self, parent):
        """Create action buttons"""
        button_frame = ttk.Frame(parent)
        button_frame.grid(row=6, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
        
        self.convert_btn = ttk.Button(
            button_frame, 
            text="Convert", 
            command=self._start_conversion,
            style='Action.TButton'
        )
        self.convert_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(button_frame, text="Cancel", command=self._cancel_conversion).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="Exit", command=self.root.quit).pack(side=tk.LEFT)
    
    def _load_presets(self):
        """Load presets into combo box"""
        presets = get_presets_by_category()
        preset_names = []
        
        for category, preset_list in presets.items():
            for preset in preset_list:
                preset_names.append(preset.name)
        
        self.preset_combo['values'] = preset_names
        if preset_names:
            self.preset_combo.current(0)
            self._on_preset_selected(None)
    
    def _on_preset_selected(self, event):
        """Handle preset selection"""
        preset_name = self.preset_var.get()
        
        # Find preset by name
        presets = get_presets_by_category()
        for category, preset_list in presets.items():
            for preset in preset_list:
                if preset.name == preset_name:
                    self.preset_desc.config(state=tk.NORMAL)
                    self.preset_desc.delete(1.0, tk.END)
                    self.preset_desc.insert(1.0, preset.description)
                    self.preset_desc.config(state=tk.DISABLED)
                    return
    
    def _add_files(self):
        """Add files to conversion list"""
        files = filedialog.askopenfilenames(
            title="Select Video Files",
            filetypes=[
                ("Video Files", "*.mp4 *.avi *.mkv *.mov *.wmv *.flv *.webm *.m4v"),
                ("All Files", "*.*")
            ]
        )
        
        for file in files:
            if file not in self.input_files:
                self.input_files.append(file)
                self.file_listbox.insert(tk.END, Path(file).name)
    
    def _add_folder(self):
        """Add all videos from a folder"""
        folder = filedialog.askdirectory(title="Select Folder")
        if not folder:
            return
        
        video_extensions = ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm', '.m4v']
        for file_path in Path(folder).iterdir():
            if file_path.is_file() and file_path.suffix.lower() in video_extensions:
                file_str = str(file_path)
                if file_str not in self.input_files:
                    self.input_files.append(file_str)
                    self.file_listbox.insert(tk.END, file_path.name)
    
    def _remove_files(self):
        """Remove selected files from list"""
        selection = self.file_listbox.curselection()
        for index in reversed(selection):
            self.file_listbox.delete(index)
            del self.input_files[index]
    
    def _clear_files(self):
        """Clear all files"""
        self.file_listbox.delete(0, tk.END)
        self.input_files.clear()
    
    def _browse_output_dir(self):
        """Browse for output directory"""
        directory = filedialog.askdirectory(title="Select Output Directory")
        if directory:
            self.output_dir_var.set(directory)
    
    def _start_conversion(self):
        """Start video conversion"""
        if not self.input_files:
            messagebox.showwarning("No Files", "Please add files to convert")
            return
        
        if self.is_converting:
            messagebox.showwarning("Busy", "Conversion is already in progress")
            return
        
        # Create output directory
        output_dir = self.output_dir_var.get()
        try:
            os.makedirs(output_dir, exist_ok=True)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create output directory: {e}")
            return
        
        # Start conversion in background thread
        self.is_converting = True
        self.convert_btn.config(state=tk.DISABLED)
        
        thread = threading.Thread(target=self._conversion_worker)
        thread.daemon = True
        thread.start()
    
    def _conversion_worker(self):
        """Worker thread for video conversion"""
        output_dir = self.output_dir_var.get()
        total_files = len(self.input_files)
        successful = 0
        failed = 0
        
        for i, input_file in enumerate(self.input_files, 1):
            try:
                # Update status
                self.root.after(0, self._update_status, f"Converting {i}/{total_files}: {Path(input_file).name}")
                
                # Determine output file
                input_path = Path(input_file)
                preset_name = self.preset_var.get()
                
                # Get preset to determine extension
                ext = 'mp4'
                if preset_name:
                    presets = get_presets_by_category()
                    for category, preset_list in presets.items():
                        for preset in preset_list:
                            if preset.name == preset_name:
                                if preset.container:
                                    ext = preset.container
                                break
                
                output_file = os.path.join(output_dir, f"{input_path.stem}.{ext}")
                
                # Progress callback
                def progress_callback(progress):
                    # Update for current file
                    file_progress = ((i - 1) / total_files + progress / total_files) * 100
                    self.root.after(0, self._update_progress, file_progress)
                
                # Convert using preset or advanced options
                if preset_name:
                    # Find and use preset
                    for category, preset_list in presets.items():
                        for preset in preset_list:
                            if preset.name == preset_name:
                                success = self.converter.convert_with_preset(
                                    input_file=input_file,
                                    output_file=output_file,
                                    preset_params=preset.to_ffmpeg_params(),
                                    progress_callback=progress_callback
                                )
                                break
                else:
                    # Use advanced options
                    success = self.converter.convert(
                        input_file=input_file,
                        output_file=output_file,
                        video_codec=self.video_codec_var.get() or None,
                        audio_codec=self.audio_codec_var.get() or None,
                        resolution=self.resolution_var.get() or None,
                        crf=int(self.crf_var.get()) if self.crf_var.get() else None,
                        start_time=self.start_time_var.get() or None,
                        duration=self.duration_var.get() or None,
                        progress_callback=progress_callback
                    )
                
                if success:
                    successful += 1
                else:
                    failed += 1
                    
            except Exception as e:
                failed += 1
                print(f"Error converting {input_file}: {e}")
        
        # Conversion complete
        self.root.after(0, self._conversion_complete, successful, failed, total_files)
    
    def _update_status(self, status: str):
        """Update status label"""
        self.status_label.config(text=status)
    
    def _update_progress(self, progress: float):
        """Update progress bar"""
        self.progress_var.set(progress)
    
    def _conversion_complete(self, successful: int, failed: int, total: int):
        """Handle conversion completion"""
        self.is_converting = False
        self.convert_btn.config(state=tk.NORMAL)
        self.progress_var.set(0)
        self.status_label.config(text="Ready")
        
        messagebox.showinfo(
            "Conversion Complete",
            f"Conversion complete!\n\nSuccessful: {successful}\nFailed: {failed}\nTotal: {total}"
        )
    
    def _cancel_conversion(self):
        """Cancel conversion"""
        if self.is_converting:
            # Note: This is a simplified cancellation - in a real app you'd need to properly
            # terminate the FFmpeg process
            messagebox.showinfo("Cancel", "Conversion cancellation not yet implemented")


def main():
    """Main entry point for GUI"""
    try:
        root = tk.Tk()
        app = VideoConverterGUI(root)
        root.mainloop()
    except Exception as e:
        print(f"Error starting GUI: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
