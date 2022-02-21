from alsa_midi.event import ControlChangeEvent, NoteOnEvent, NoteOffEvent

def midi_translate(event):

    if type(event) is ControlChangeEvent:
        params = (event.channel, event.param, event.value)
        # Channel freqency changes
        if params == (0, 6, 1):
            return {"buffered": True, "type": "changeChFreq", "value": "up", "options": {"speed": "slow"}}
        if params == (0, 6, 127):
            return {"buffered": True, "type": "changeChFreq", "value": "down", "options": {"speed": "slow"}}
        if params == (1, 6, 1):
            return {"buffered": True, "type": "changeChFreq", "value": "up", "options": {"speed": "fast"}}
        if params == (1, 6, 127):
            return {"buffered": True, "type": "changeChFreq", "value": "down", "options": {"speed": "fast"}}

        # Center Frequency changes
        if params == (15, 0, 127):
            return {"buffered": False, "type": "changeCenterFreq", "value": "down"}
        if params == (15, 0, 1):
            return {"buffered": False, "type": "changeCenterFreq", "value": "up"}

        print('Undefined ControlChangeEvent: '+repr(event))


    if type(event) is NoteOnEvent:
        params = (event.channel, event.note, event.velocity)

        # RX (Left) Channel selectors
        if params == (4, 1, 127):
            return {"buffered": False, "type": "selectRxChan", "value": "0"}
        if params == (4, 2, 127):
            return {"buffered": False, "type": "selectRxChan", "value": "1"}
        if params == (4, 3, 127):
            return {"buffered": False, "type": "selectRxChan", "value": "2"}
        if params == (4, 4, 127):
            return {"buffered": False, "type": "selectRxChan", "value": "3"}
        
        # TX (Right) Channel selectors
        if params == (5, 1, 127):
            return {"buffered": False, "type": "selectTxChan", "value": "0"}
        if params == (5, 2, 127):
            return {"buffered": False, "type": "selectTxChan", "value": "1"}
        if params == (6, 3, 127):
            return {"buffered": False, "type": "selectTxChan", "value": "2"}
        if params == (7, 4, 127):
            return {"buffered": False, "type": "selectTxChan", "value": "3"}
        print('Undefined NoteOnEvent: '+repr(event))

    # TBD
    # if type(event) is NoteOffEvent:

    return {"buffered": False, "type": "NotImplemented", "value": "None","options": {}}        
