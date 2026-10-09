import mido
import sys

# --- CONFIGURATION ---
# The script will look for these names in your MIDI list
GUITAR_SEARCH_TERM = "TriplePlay Express"
ENGINE_SEARCH_TERM = "USB MIDI Interface"
# ---------------------

def find_port_name(partial_name, port_list):
    """Finds the full MIDI port name from a partial string."""
    for name in port_list:
        if partial_name in name:
            return name
    return None

def main():
    # 1. Detect Ports
    input_names = mido.get_input_names()
    output_names = mido.get_output_names()

    in_port = find_port_name(GUITAR_SEARCH_TERM, input_names)
    out_port = find_port_name(ENGINE_SEARCH_TERM, output_names)

    if not in_port:
        print(f"Error: Could not find Guitar input containing '{GUITAR_SEARCH_TERM}'")
        print("Available inputs:", input_names)
        return

    if not out_port:
        print(f"Error: Could not find MiniEngine output containing '{ENGINE_SEARCH_TERM}'")
        print("Available outputs:", output_names)
        return

    print(f"Connecting: {in_port} ---> {out_port}")

    try:
        # 2. Open both ports
        with mido.open_input(in_port) as inport, mido.open_output(out_port) as outport:
            print("System Active. Play your guitar! (Press Ctrl+C to stop)")
            
            for msg in inport:
                # 3. Process and Filter
                # We only want to forward actual performance data (notes, bends, etc.)
                if msg.type in ['note_on', 'note_off', 'pitchwheel', 'control_change']:
                    
                    # FORCE every message to MIDI Channel 1 (Internal index 0)
                    # This prevents the MiniEngine from switching to Channel 8
                    msg.channel = 0
                    
                    # Send to MiniEngine
                    outport.send(msg)
                    
                    # 4. Print for debugging in your terminal
                    if msg.type == 'note_on':
                        print(f" [NOTE ON]  Note: {msg.note} | Vel: {msg.velocity}")
                    elif msg.type == 'note_off':
                        print(f" [NOTE OFF] Note: {msg.note}")
                    else:
                        print(f" [EXTRA]    {msg}")

    except KeyboardInterrupt:
        print("\nStopping MIDI router...")
    except Exception as e:
        print(f"\nAn error occurred: {e}")

if __name__ == "__main__":
    main()
