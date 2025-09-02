#!/usr/bin/env python3
"""
Audio Trimmer Script
Extracts a clip from an audio file based on user-specified timestamps.
"""

import os
import sys
from pathlib import Path

try:
    from pydub import AudioSegment
except ImportError:
    print("Error: pydub is not installed.")
    print("Please install it using: pip install pydub")
    print("Note: You may also need ffmpeg installed on your system.")
    print("Visit https://ffmpeg.org/download.html for installation instructions.")
    sys.exit(1)


def parse_timestamp(timestamp_str):
    """
    Parse timestamp string in various formats and return milliseconds.
    Supported formats:
    - MM:SS (minutes:seconds)
    - HH:MM:SS (hours:minutes:seconds)
    - Seconds only (e.g., "90" for 90 seconds)
    - Milliseconds (e.g., "5000ms")
    """
    timestamp_str = timestamp_str.strip()
    
    # Check if it's in milliseconds
    if timestamp_str.endswith('ms'):
        return int(timestamp_str[:-2])
    
    # Check if it contains colons (time format)
    if ':' in timestamp_str:
        parts = timestamp_str.split(':')
        if len(parts) == 2:  # MM:SS
            minutes, seconds = map(float, parts)
            return int((minutes * 60 + seconds) * 1000)
        elif len(parts) == 3:  # HH:MM:SS
            hours, minutes, seconds = map(float, parts)
            return int((hours * 3600 + minutes * 60 + seconds) * 1000)
    else:
        # Assume it's seconds
        return int(float(timestamp_str) * 1000)


def format_duration(milliseconds):
    """Convert milliseconds to a readable format."""
    seconds = milliseconds / 1000
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = seconds % 60
    
    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{secs:05.2f}"
    else:
        return f"{minutes:02d}:{secs:05.2f}"


def trim_audio(input_file, start_time, end_time, output_file, output_format):
    """
    Trim audio file from start_time to end_time.
    Times should be in milliseconds.
    """
    try:
        # Load the audio file
        print(f"Loading audio file: {input_file}")
        audio = AudioSegment.from_file(input_file)
        
        # Get audio duration
        duration = len(audio)
        print(f"Audio duration: {format_duration(duration)}")
        
        # Validate timestamps
        if start_time < 0:
            start_time = 0
        if end_time > duration:
            end_time = duration
        
        if start_time >= end_time:
            raise ValueError("Start time must be before end time")
        
        # Extract the segment
        print(f"Extracting from {format_duration(start_time)} to {format_duration(end_time)}")
        trimmed_audio = audio[start_time:end_time]
        
        # Export the trimmed audio
        print(f"Saving trimmed audio to: {output_file}")
        trimmed_audio.export(output_file, format=output_format)
        
        print(f"✓ Successfully created trimmed audio file!")
        print(f"  Duration: {format_duration(len(trimmed_audio))}")
        
    except Exception as e:
        print(f"Error: {e}")
        return False
    
    return True


def main():
    print("=" * 50)
    print("Audio Trimmer Script")
    print("=" * 50)
    
    # Get input file
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    else:
        input_file = input("Enter the path to your audio file: ").strip()
    
    # Remove quotes if present
    input_file = input_file.strip('"').strip("'")
    
    # Check if file exists
    if not os.path.exists(input_file):
        print(f"Error: File '{input_file}' not found!")
        sys.exit(1)
    
    input_path = Path(input_file)
    
    # Display file info
    print(f"\nFile: {input_path.name}")
    print("-" * 50)
    
    # Load audio to get duration
    try:
        audio = AudioSegment.from_file(input_file)
        duration = len(audio)
        print(f"Total duration: {format_duration(duration)}")
    except Exception as e:
        print(f"Error loading audio file: {e}")
        sys.exit(1)
    
    print("\nTimestamp formats supported:")
    print("  - MM:SS (e.g., 1:30 for 1 minute 30 seconds)")
    print("  - HH:MM:SS (e.g., 0:01:30)")
    print("  - Seconds (e.g., 90 for 90 seconds)")
    print("  - Milliseconds (e.g., 5000ms)")
    
    # Get start timestamp
    print("\n" + "-" * 50)
    while True:
        start_input = input("Enter start timestamp (or press Enter for beginning): ").strip()
        if not start_input:
            start_ms = 0
            break
        try:
            start_ms = parse_timestamp(start_input)
            if start_ms < 0 or start_ms >= duration:
                print(f"Start time must be between 0 and {format_duration(duration)}")
                continue
            break
        except ValueError as e:
            print(f"Invalid timestamp format. Please try again.")
    
    # Get end timestamp
    while True:
        end_input = input("Enter end timestamp (or press Enter for end of file): ").strip()
        if not end_input:
            end_ms = duration
            break
        try:
            end_ms = parse_timestamp(end_input)
            if end_ms <= start_ms:
                print(f"End time must be after start time ({format_duration(start_ms)})")
                continue
            if end_ms > duration:
                print(f"End time cannot exceed file duration ({format_duration(duration)})")
                continue
            break
        except ValueError as e:
            print(f"Invalid timestamp format. Please try again.")
    
    # Generate output filename
    default_output = input_path.stem + "_trimmed" + input_path.suffix
    output_file = input(f"\nEnter output filename (or press Enter for '{default_output}'): ").strip()
    
    if not output_file:
        output_file = default_output
    
    # Ensure output has an extension
    output_path = Path(output_file)
    if not output_path.suffix:
        output_path = output_path.with_suffix(input_path.suffix)
        output_file = str(output_path)
    
    print("\n" + "=" * 50)
    print("Processing...")
    print("=" * 50)
    
    # Extract format from input file's suffix
    output_format = input_path.suffix[1:]
    
    # Perform the trim
    if trim_audio(input_file, start_ms, end_ms, output_file, output_format):
        print(f"\n✓ File saved as: {output_file}")
    else:
        print("\n✗ Failed to trim audio file")
        sys.exit(1)


if __name__ == "__main__":
    main()