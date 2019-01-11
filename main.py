from rx import Observable
from grove.adc import ADC
import signal
import sys
from urllib3 import PoolManager
from argparse import ArgumentParser


class GroveLightSensor:

    def __init__(self, channel):
        self.channel = channel
        self.adc = ADC()

    @property
    def light(self):
        value = self.adc.read(self.channel)
        return value


class Notifier:

    def __init__(self, iftttkey):
        self.iftttkey = iftttkey

    def notice(self):
        url = "https://maker.ifttt.com/trigger/\
comming/with/key/{}".format(self.iftttkey)
        http = PoolManager()
        request = http.request(
            'POST',
            url)
        print("Request Status {}".format(request.status))
        request


disposer = None
threshold = 200


def handler(signal, frame):
    if disposer is not None:
        disposer.dispose()
    sys.exit(0)


def main():
    psr = ArgumentParser()
    psr.add_argument('-k', '--key', required=True, help='IFTTT webhook key')
    args = psr.parse_args()
    pin = 0
    sensor = GroveLightSensor(pin)
    notifier = Notifier(args.key)
    global disposer
    disposer = Observable.interval(1000) \
        .map(lambda _: sensor.light) \
        .do_action(lambda value: print("Sensor Value {}".format(value))) \
        .map(lambda value: value > threshold) \
        .distinct_until_changed() \
        .filter(lambda value: value) \
        .map(lambda _: notifier.notice()) \
        .subscribe()
    signal.signal(signal.SIGINT, handler)
    while True:
        pass


if __name__ == "__main__":
    main()
