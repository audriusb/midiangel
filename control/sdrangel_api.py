import requests
import json

class SDRAngelAPI:
    def __init__(self, config):
        self.url = '{}://{}:{}/{}'.format(config['scheme'], config['hostname'], config['port'], config['path'])
        self.config = config

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

    def get_ch_freq(self, devset, ch):
        print('{}deviceset/{}/channel/{}/settings'.format(self.url, devset, ch))
        settings = requests.get('{}deviceset/{}/channel/{}/settings'.format(self.url, devset, ch)).json()
        try:
            return settings['{}Settings'.format(settings['channelType'])]['inputFrequencyOffset']
        except: return 0
    
    def change_ch_freq(self, step, devset, ch):

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

    def set_ch_freq(self, freq, devset, ch):
        settings = requests.get('{}deviceset/{}/channel/{}/settings'.format(self.url, devset, ch)).json()
        data = {
            'channelType': settings['channelType'],
            'direction': settings['direction'],
            '{}Settings'.format(settings['channelType']): { 
                'inputFrequencyOffset': freq
                }
        }
        result = requests.patch('{}deviceset/{}/channel/{}/settings'.format(self.url, devset, ch), json = data)

    def get_center_freq(self, devset):
        settings = requests.get('{}deviceset/{}/device/settings'.format(self.url, devset)).json()
        settings_name = [k for k in settings.keys() if k.lower().startswith(settings['deviceHwType'].lower())][0]
        if settings_name == "remoteInputSettings":
            url = '{}://{}:{}/{}'.format(self.config['scheme'], settings[settings_name]['apiAddress'], settings[settings_name]['apiPort'], self.config['path'])
            settings = requests.get('{}deviceset/{}/device/settings'.format(url, devset)).json()
            settings_name = [k for k in settings.keys() if k.lower().startswith(settings['deviceHwType'].lower())][0]
        return settings[settings_name]['centerFrequency']

    def change_center_freq(self, step, devset):
        settings = requests.get('{}deviceset/{}/device/settings'.format(self.url, devset)).json()
        settings_name = [k for k in settings.keys() if k.lower().startswith(settings['deviceHwType'].lower())][0]
        if settings_name == "remoteInputSettings":
            url = '{}://{}:{}/{}'.format(self.config['scheme'], settings[settings_name]['apiAddress'], settings[settings_name]['apiPort'], self.config['path'])
            settings = requests.get('{}deviceset/{}/device/settings'.format(url, devset)).json()
            settings_name = [k for k in settings.keys() if k.lower().startswith(settings['deviceHwType'].lower())][0]
        else:
            url = self.url
        current_freq = settings[settings_name]['centerFrequency']
        data = {
            'deviceHwType': settings['deviceHwType'],
            'direction': settings['direction'],
            settings_name: { 
                'centerFrequency': current_freq + step 
                }
        }
        result = requests.patch('{}deviceset/{}/device/settings'.format(url, devset), json = data)

    def set_center_freq(self, freq, devset):
        settings = requests.get('{}deviceset/{}/device/settings'.format(self.url, devset)).json()
        settings_name = [k for k in settings.keys() if k.lower().startswith(settings['deviceHwType'].lower())][0]
        if settings_name == "remoteInputSettings":
            url = '{}://{}:{}/{}'.format(self.config['scheme'], settings[settings_name]['apiAddress'], settings[settings_name]['apiPort'], self.config['path'])
            settings = requests.get('{}deviceset/{}/device/settings'.format(url, devset)).json()
            settings_name = [k for k in settings.keys() if k.lower().startswith(settings['deviceHwType'].lower())][0]
        else:
            url = self.url
        data = {
            'deviceHwType': settings['deviceHwType'],
            'direction': settings['direction'],
            settings_name: { 
                'centerFrequency': freq
                }
        }
        result = requests.patch('{}deviceset/{}/device/settings'.format(url, devset), json = data)


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

    def get_ch_mute(self, devset, ch):
        settings = requests.get('{}deviceset/{}/channel/{}/settings'.format(self.url, devset, ch)).json()
        try:
            is_mute = settings['{}Settings'.format(settings['channelType'])]['audioMute']
            if is_mute == 1:
                return 'on'
            else:
                return 'off'
        except: 
            return 'off'

    def set_ch_mute(self, devset, ch):
        settings = requests.get('{}deviceset/{}/channel/{}/settings'.format(self.url, devset, ch)).json()
        try:
            is_mute = settings['{}Settings'.format(settings['channelType'])]['audioMute']
            if is_mute == 0:
                next_state = 1
            else:
                next_state = 0
        except:
            return 'off'
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