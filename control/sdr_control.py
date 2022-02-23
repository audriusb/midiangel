from collections import defaultdict

from .midi_control import MIDIControl
from .sdrangel_api import SDRAngelAPI

class SDRController:
    
    def __init__(self, config, midi):
        self.rx_only = config.getboolean('rx_only')
        self.sdr_client = SDRAngelAPI(config)
        self.midi_client = midi
        self.select_device_sets()
        self.device_states = defaultdict(dict)
        self.check_device_states()
        self.select_channel(rx='0')
        if not self.rx_only:
            self.select_channel(tx='0')

    # For safety reasons update existing state
    def check_device_states(self):
        self.device_states[self.active_rx_device_set] =  self.sdr_client.get_deviceset_state(self.active_rx_device_set)
        if self.device_states[self.active_rx_device_set] == 'on':
            self.midi_client.play_on('left')
        elif self.device_states[self.active_rx_device_set] == 'off':
            self.midi_client.play_dimm('left')
        if not self.rx_only:
            self.device_states[self.active_tx_device_set] =  self.sdr_client.get_deviceset_state(self.active_tx_device_set)
            if self.device_states[self.active_tx_device_set] == 'on':
                self.midi_client.play_on('right')
            elif self.device_states[self.active_tx_device_set] == 'off':
                self.midi_client.play_dimm('right')
        else:
            self.midi_client.play_off('right')

    def change_device_state(self, side):
        if side == 'rx':
            if self.device_states[self.active_rx_device_set] == 'off':
                self.sdr_client.set_deviceset_state(self.active_rx_device_set, 'on')
            else:
                self.sdr_client.set_deviceset_state(self.active_rx_device_set, 'off')
        if side == 'tx' and not self.rx_only:
            if self.device_states[self.active_tx_device_set] == 'off':
                self.sdr_client.set_deviceset_state(self.active_tx_device_set, 'on')
            else:
                self.sdr_client.set_deviceset_state(self.active_tx_device_set, 'off')
        self.check_device_states()

    def change_channel_freq(self, step):
        self.sdr_client.set_ch_freq(step, self.active_rx_device_set, self.active_rx_channel)
        if not self.rx_only:
            self.sdr_client.set_ch_freq(step, self.active_tx_device_set, self.active_tx_channel)

    def select_device_sets(self, rx=0, tx=1):
        self.active_rx_device_set = rx
        self.active_tx_device_set = tx
        if self.rx_only:
            self.midi_client.channel_off('right', 1)
            self.midi_client.channel_off('right', 2)
            self.midi_client.channel_off('right', 3)
            self.midi_client.channel_off('right', 4)


    def select_channel(self, rx=None, tx=None):
        if rx:

            if not self.sdr_client.check_channel('rx', self.active_rx_device_set, rx ) or int(rx) > 4:
                self.midi_client.channel_blink(3, 'left', int(rx)+1 )
            else:
                self.active_rx_channel = rx
                self.midi_client.channel_dim_all('left')
                self.midi_client.channel_on('left', int(rx)+1 )
                self.midi_client.mute_change(
                   'left',
                    self.sdr_client.get_ch_mute(self.active_rx_device_set, self.active_rx_channel)
                )
        if tx:
            if not self.sdr_client.check_channel('tx', self.active_tx_device_set, tx ) or int(tx) > 4:
                self.midi_client.channel_blink(3, 'right', int(tx)+1 )
            else:
                self.active_tx_channel = tx
                self.midi_client.channel_dim_all('right')
                self.midi_client.channel_on('right', int(rx)+1 )
                self.midi_client.mute_change(
                   'right',
                    self.sdr_client.get_ch_mute(self.active_rx_device_set, self.active_rx_channel)
                )

    def change_center_freq(self, step, direction):
        change = step
        if direction == 'down':
            change = 0 - step
        self.sdr_client.set_center_freq(change, self.active_rx_device_set)
        if not self.rx_only:
            self.sdr_client.set_center_freq(change, self.active_tx_device_set)

    def change_channel_volume(self, side, vol):
        if side == 'rx':
            self.sdr_client.set_ch_vol(vol, self.active_rx_device_set, self.active_rx_channel)
        if side == 'tx' and not self.rx_only:
            self.sdr_client.set_ch_vol(vol, self.active_tx_device_set, self.active_tx_channel)

    def mute_channel(self, side):
        if side == 'rx':
            self.midi_client.mute_change(
                'left',
                self.sdr_client.set_ch_mute(self.active_rx_device_set, self.active_rx_channel)
            )
        if side == 'tx' and not self.rx_only:
            self.midi_client.mute_change(
                'right',
                self.sdr_client.set_ch_mute(self.active_tx_device_set, self.active_tx_channel)
            )
