from rx import Observable, Observer
from grove.adc import ADC
import signal
import sys

class GroveLightSensor:

    def __init__(self, channel):
        self.channel = channel
        self.adc = ADC()

    @property
    def light(self):
        value = self.adc.read(self.channel)
        return value

disposer = None

def handler(signal, frame):
    if disposer != None:
        disposer.dispose()
    sys.exit(0)

def main():
    pin = 0
    sensor = GroveLightSensor(pin)
    disposer = Observable.interval(1000) \
        .map(lambda _: sensor.light) \
        .map(lambda value: value > 200) \
        .distinct_until_changed() \
        .filter(lambda value: value) \
        .subscribe(lambda _: print("Should Notify"))
    signal.signal(signal.SIGINT, handler)
    while True:
        pass

if __name__ == "__main__":
    main()
