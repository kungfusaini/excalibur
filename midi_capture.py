#!/usr/bin/env python3
import mido
import sys

def main():
    print("Available MIDI inputs:")
    for port in mido.get_input_names():
        print(f"  - {port}")
    
    if len(sys.argv) > 1:
        port_name = sys.argv[1]
    else:
        port_name = mido.get_input_names()[0] if mido.get_input_names() else None
    
    if not port_name:
        print("No MIDI input devices found")
        return
    
    print(f"Listening to MIDI input: {port_name}")
    print("Press Ctrl+C to stop")
    
    try:
        with mido.open_input(port_name) as inport:
            for msg in inport:
                print(msg)
    except KeyboardInterrupt:
        print("\nStopped listening to MIDI input")

if __name__ == "__main__":
    main()