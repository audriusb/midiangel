import datetime
import configparser
import signal, sys

from control import SDRController, MIDIControl, midi_translate

from threading import Thread
from queue import Queue
from time import sleep

config = configparser.ConfigParser()
config.read('config.ini')

event_flush_count = 10
event_flush_timeout_ms = 100

last_event_flush_t = datetime.datetime.now()
last_event_flush_count = 0
event_api_buff = Queue()

midi = MIDIControl(config['MidiController']['controller_name'])
sdr_controller = SDRController(
        config['sdrangel'],
        midi
    )

def freq_step(speed='slow', direction='up'):
    step = 10
    if speed == 'fast':
        step = 100
    if direction == 'down':
        step = 0 - step
    return step

def parse_buffered_events(events):
    
    freq = 0
    for event in list(filter(lambda event: event['type'] == 'changeChFreq' , events)):
        freq += freq_step(event['options']['speed'], event['value'])
    if freq != 0:
        sdr_controller.change_channel_freq(freq)

    skew_count = 0
    skew = 0
    for event in list(filter(lambda event: event['type'] == 'slideFreq' , events)):
        skew += event['value']
        skew_count += 1
    if skew_count != 0:
        sdr_controller.skew_freq_display(event['value'])

def parse_event(event):
    if event['type'] == 'triggerRxDev':
        sdr_controller.change_device_state('rx')
    if event['type'] == 'triggerTxDev':
        sdr_controller.change_device_state('tx')
    if event['type'] == 'changeCenterFreq':
        sdr_controller.change_center_freq(10000, event['value'])
    if event['type'] == 'selectRxChan':
        sdr_controller.select_channel(rx=event['value'])
    if event['type'] == 'selectTxChan':
        sdr_controller.select_channel(tx=event['value'])
    if event['type'] == 'changeRxVolume':
        sdr_controller.change_channel_volume('rx', event['value'])
    if event['type'] == 'changeTxVolume':
        sdr_controller.change_channel_volume('tx', event['value'])
    
    if event['type'] == 'muteRxChan':
        sdr_controller.mute_channel('rx')
    if event['type'] == 'muteTxChan':
        sdr_controller.mute_channel('tx')



def listen_events(th_name, event_api_buff, last_event_flush_count, midi):
    print('Listening to MIDI device: ' + config['MidiController']['controller_name'])
    while True:
        event = midi_translate(midi.client.event_input())
        print('Got event: ' + repr(event))
        if event['buffered'] == True:
            event_api_buff.put(event)
            last_event_flush_count += 1
        else:
            parse_event(event)

def flush_events(th_name, event_api_buff, last_event_flush_t, last_event_flush_count):
    while True:
        now = datetime.datetime.now()
        t_diff = datetime.datetime.now() - last_event_flush_t
        t_diff_ms = (t_diff.seconds * 1000) + (t_diff.microseconds // 1000)
        if t_diff_ms > event_flush_timeout_ms or last_event_flush_count > event_flush_count :
            last_event_flush_t = datetime.datetime.now()
            last_event_flush_count = 0
            events = []
            while not event_api_buff.empty():
                events.append(event_api_buff.get())
            if len(events) > 0:
                parse_buffered_events(events)
        sleep(0.01)

def signal_handler(signal, frame):
    print('Exiting...')
    midi.reset_all()
    print('Bye')
    sys.exit()

thread_listen = Thread( target=listen_events, args=('listen', event_api_buff, last_event_flush_count, midi) )
thread_parse = Thread( target=flush_events, args=('parse', event_api_buff, last_event_flush_t, last_event_flush_count ) )

signal.signal(signal.SIGINT, signal_handler)

thread_listen.daemon = True
thread_parse.daemon = True
thread_listen.start()
thread_parse.start()
thread_listen.join()
thread_parse.join()