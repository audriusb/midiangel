from time import sleep
from alsa_midi import SequencerClient
from alsa_midi import WRITE_PORT, PortType
from alsa_midi.event import ControlChangeEvent, NoteOnEvent, NoteOffEvent

class MIDIControl:
    def __init__(self, dev_name):
        self.client = SequencerClient('midi_cli')
        ports = self.client.list_ports()
        self.midi_port = list(filter(lambda port: port.client_name == dev_name , ports))[0]
        print('Found MIDI port: ' + repr(self.midi_port))
        self.port = self.client.create_port('inout')
        self.port.connect_to(self.midi_port)
        self.port.connect_from(self.midi_port)

    def channel_off(self, side, number):
        if side == 'left':
            ch = 4
        elif side == 'right':
            ch = 5
        self.client.event_output(NoteOnEvent(note=number, channel=ch, velocity=0), port=self.port)
        self.client.drain_output()


    def channel_on(self, side, number):
        if side == 'left':
            ch = 4
        elif side == 'right':
            ch = 5
        self.client.event_output(NoteOnEvent(note=number, channel=ch, velocity=127), port=self.port)
        self.client.drain_output()


    def channel_dimm(self, side, number):
        if side == 'left':
            ch = 4
        elif side == 'right':
            ch = 5
        self.client.event_output(NoteOnEvent(note=number, channel=ch, velocity=1), port=self.port)
        self.client.drain_output()


    def channel_dim_all(self, side):
        if side == 'left':
            ch = 4
        elif side == 'right':
            ch = 5
        self.client.event_output(NoteOnEvent(note=1, channel=ch, velocity=1), port=self.port)
        self.client.event_output(NoteOnEvent(note=2, channel=ch, velocity=1), port=self.port)
        self.client.event_output(NoteOnEvent(note=3, channel=ch, velocity=1), port=self.port)
        self.client.event_output(NoteOnEvent(note=4, channel=ch, velocity=1), port=self.port)
        self.client.drain_output()


    def channel_blink(self, times, side, number):
        if side == 'left':
            ch = 4
        elif side == 'right':
            ch = 5
        for cnt in range(times):
            self.client.event_output(NoteOnEvent(note=number, channel=ch, velocity=127), port=self.port)
            self.client.drain_output()
            sleep(0.2)
            self.client.event_output(NoteOnEvent(note=number, channel=ch, velocity=0), port=self.port)
            self.client.drain_output()
            sleep(0.2)
        self.client.event_output(NoteOnEvent(note=number, channel=ch, velocity=1), port=self.port)
        self.client.drain_output()

    def reset_all(self):
        self.client.event_output(NoteOnEvent(note=1, channel=0, velocity=1), port=self.port)
        self.client.event_output(NoteOnEvent(note=2, channel=0, velocity=1), port=self.port)
        self.client.event_output(NoteOnEvent(note=2, channel=0, velocity=1), port=self.port)
        self.client.event_output(NoteOnEvent(note=1, channel=4, velocity=1), port=self.port)
        self.client.event_output(NoteOnEvent(note=2, channel=4, velocity=1), port=self.port)
        self.client.event_output(NoteOnEvent(note=3, channel=4, velocity=1), port=self.port)
        self.client.event_output(NoteOnEvent(note=4, channel=4, velocity=1), port=self.port)
        self.client.event_output(NoteOnEvent(note=27, channel=0, velocity=0), port=self.port)
        self.client.event_output(NoteOnEvent(note=4, channel=0, velocity=0), port=self.port)
        self.client.event_output(NoteOnEvent(note=2, channel=1, velocity=1), port=self.port)
        self.client.event_output(NoteOnEvent(note=1, channel=1, velocity=1), port=self.port)
        self.client.event_output(NoteOnEvent(note=0, channel=1, velocity=1), port=self.port)
        self.client.event_output(NoteOnEvent(note=1, channel=5, velocity=1), port=self.port)
        self.client.event_output(NoteOnEvent(note=2, channel=5, velocity=1), port=self.port)
        self.client.event_output(NoteOnEvent(note=3, channel=5, velocity=1), port=self.port)
        self.client.event_output(NoteOnEvent(note=4, channel=5, velocity=1), port=self.port)
        self.client.event_output(NoteOnEvent(note=27, channel=1, velocity=0), port=self.port)
        self.client.drain_output()

    
