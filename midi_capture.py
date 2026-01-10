import mido

# Using the exact name from your aconnect output
# Mido usually needs the full string including the port number
input_name = 'TriplePlay Express:TriplePlay Express TP Guitar 24:0'

print(f"Opening {input_name}...")

try:
    with mido.open_input(input_name) as inport:
        print("Listening for MIDI... (Press Ctrl+C to stop)")
        for msg in inport:
            print(msg)
except IOError:
    print("Could not find the MIDI port. Let's list available names:")
    print(mido.get_input_names())
