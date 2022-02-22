from alsa_midi.event import ControlChangeEvent, NoteOnEvent, NoteOffEvent
import alsaaudio

def midi_translate(event):

    if type(event) is ControlChangeEvent:
        params = (event.channel, event.param, event.value)
        param_no_val = (event.channel, event.param)
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

        # Channel volume changes
        if param_no_val == (0, 9):
            vol = 1
            if int(event.value) > 64:
                vol = round((10000/63) * (int(event.value) - 64), 8)
            if int(event.value) < 64:
                vol = round(1 - (0.9/64) * abs((int(event.value) - 64)),8)
            return {"buffered": False, "type": "changeRxVolume", "value": vol}
        if param_no_val == (1, 9):
            vol = 1
            if int(event.value) > 64:
                vol = 1 + round((2/63) * (int(event.value) - 64),2)
            if int(event.value) < 64:
                vol = round((1/64) * int(event.value),2)
            return {"buffered": False, "type": "changeTxVolume", "value": vol}
        
        # Alsa system audio control
        if param_no_val == (15, 10):
            mixer = alsaaudio.Mixer()
            mixer.setvolume(round(event.value/127 * 100))
            return {"buffered": False, "type": "NoSDRAction"}

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

        # Mute buttons
        if params == (0, 27, 127):
            return {"buffered": False, "type": "muteRxChan"}
        if params == (1, 27, 127):
            return {"buffered": False, "type": "muteTxChan"}
        
        
        print('Undefined NoteOnEvent: '+repr(event))

    
    if type(event) is NoteOffEvent:
        params = (event.channel, event.note, event.velocity)
        if params == (0, 27, 0):
            return {"buffered": False, "type": "muteRxChan"}
        if params == (1, 27, 0):
            return {"buffered": False, "type": "muteTxChan"}

    return {"buffered": False, "type": "NotImplemented", "value": "None","options": {}}      


