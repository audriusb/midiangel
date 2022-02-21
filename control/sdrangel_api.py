import requests
import json

class SDRAngelAPI:
    def __init__(self, config):
        self.url = '{}://{}:{}/{}'.format(config['scheme'], config['hostname'], config['port'], config['path'])

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