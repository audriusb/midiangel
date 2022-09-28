import Hamlib

class RigControl:

    def __init__(self, config):
        self.enabled = config['enabled']
        if self.enabled:
            self.rig = Hamlib.Rig(Hamlib.__dict__[config['model_number']])
            self.rig.set_conf("rig_pathname", config['device'])
            self.rig.set_conf('serial_speed', config['baud_rate'])
            self.rig.set_conf("retry", "5")
            self.rig.open()

    def set_freq(self, freq):
        if self.enabled:
            self.rig.set_freq(Hamlib.RIG_VFO_A, freq)

    def change_freq(self, step):
        if self.enabled:
            self.set_freq(self.get_freq() + step)

    def get_freq(self):
        if self.enabled:
            return self.rig.get_freq()

    def close(self):
        if self.enabled:
            self.rig.close()
