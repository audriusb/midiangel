import requests
import json

class SDRAngelAPI:
    def __init__(self, config):
        self.url = '{}://{}:{}/{}'.format(config['scheme'], config['hostname'], config['port'], config['path'])

    def get_deviceset_state(self, devset):
        state = requests.get('{}deviceset/{}/device/run'.format(self.url, devset)).json()['state']
        if state == 'running':
            return 'on'
        elif state == 'idle':
            return 'off'
        return 'fail'

    def set_deviceset_state(self, devset, state):
        if state == 'on':
            response = requests.post('{}deviceset/{}/device/run'.format(self.url, devset))
        elif state == 'off':
            response = requests.delete('{}deviceset/{}/device/run'.format(self.url, devset))

    def check_channel(self, direction, devset, ch):
        try:
            settings = requests.get('{}deviceset/{}/channel/{}/settings'.format(self.url, devset, ch)).json()
            if settings['direction'] == 0 and direction == 'rx':
                return True
            elif settings['direction'] == 1 and direction == 'tx':
                return True
            return False
        except:
            return False

    def set_ch_freq(self, step, devset, ch):
        settings = requests.get('{}deviceset/{}/channel/{}/settings'.format(self.url, devset, ch)).json()
        current_freq = settings['{}Settings'.format(settings['channelType'])]['inputFrequencyOffset']
        data = {
            'channelType': settings['channelType'],
            'direction': settings['direction'],
            '{}Settings'.format(settings['channelType']): { 
                'inputFrequencyOffset': current_freq + step 
                }
        }
        result = requests.patch('{}deviceset/{}/channel/{}/settings'.format(self.url, devset, ch), json = data)

    def set_center_freq(self, step, devset):
        settings = requests.get('{}deviceset/{}/device/settings'.format(self.url, devset)).json()
        settings_name = {k.lower(): k for k in settings.keys()}['{}Settings'.format(settings['deviceHwType']).lower()]
        current_freq = settings[settings_name]['centerFrequency']
        data = {
            'deviceHwType': settings['deviceHwType'],
            'direction': settings['direction'],
            settings_name: { 
                'centerFrequency': current_freq + step 
                }
        }
        result = requests.patch('{}deviceset/{}/device/settings'.format(self.url, devset), json = data)


    def set_ch_vol(self, vol, devset, ch):
        settings = requests.get('{}deviceset/{}/channel/{}/settings'.format(self.url, devset, ch)).json()
        if settings['direction'] == 0:
            vol_setting_name = 'volume'
        else:
            vol_setting_name = 'volumeFactor'
        data = {
            'channelType': settings['channelType'],
            'direction': settings['direction'],
            '{}Settings'.format(settings['channelType']): { 
                vol_setting_name: vol 
                }
        }
        result = requests.patch('{}deviceset/{}/channel/{}/settings'.format(self.url, devset, ch), json = data)

    def set_ch_mute(self, devset, ch):
        settings = requests.get('{}deviceset/{}/channel/{}/settings'.format(self.url, devset, ch)).json()
        is_mute = settings['{}Settings'.format(settings['channelType'])]['audioMute']
        if is_mute == 0:
            next_state = 1
        else:
            next_state = 0
        data = {
            'channelType': settings['channelType'],
            'direction': settings['direction'],
            '{}Settings'.format(settings['channelType']): { 
                'audioMute': next_state
                }
        }
        result = requests.patch('{}deviceset/{}/channel/{}/settings'.format(self.url, devset, ch), json = data)
        if next_state == 1:
            return 'on'
        else:
            return 'off'