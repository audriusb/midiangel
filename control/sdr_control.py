from .midi_control import MIDIControl
from .sdrangel_api import SDRAngelAPI

sdr_client_type = {
    'sdrangel': SDRAngelAPI
}

class SDRController:
    
    def __init__(self, sdr_type, rx_only, config, midi):
        self.active_rx_device = 0
        self.active_tx_device = 0
        self.rx_only = rx_only
        self.sdr_client = sdr_client_type[sdr_type](config)
        self.midi_client = midi
        self.select_device_sets()
        self.select_channel(rx="0")
        if not rx_only:
            self.select_channel(tx="0")

    def change_channel_freq(self, step):
        # try:
        self.sdr_client.set_ch_freq(step, self.active_rx_device_set, self.active_rx_channel)
        if not self.rx_only:
            self.sdr_client.set_ch_freq(step, self.active_tx_device_set, self.active_tx_channel)
        # except Exception as e:
            # print('Error changing frequency. Could be channel not available on selected device')
            # print(repr(e))
            # return

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
        if tx:
            if not self.sdr_client.check_channel('tx', self.active_tx_device_set, tx ) or int(tx) > 4:
                self.midi_client.channel_blink(3, 'right', int(tx)+1 )
            else:
                self.active_tx_channel = tx
                self.midi_client.channel_dim_all('right')
                self.midi_client.channel_on('right', int(rx)+1 )

    def change_center_freq(self, step, direction):
        change = step
        if direction == 'down':
            change = 0 - step
        self.sdr_client.set_center_freq(change, self.active_rx_device_set)
        if not self.rx_only:
            self.sdr_client.set_center_freq(change, self.active_tx_device_set)
