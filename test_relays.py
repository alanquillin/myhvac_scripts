#!/usr/bin/python

import getopt
import RPi.GPIO as GPIO
import sys
import time

OKBLUE = '\033[94m'
OKGREEN = '\033[92m'
FAIL = '\033[91m'
ENDC = '\033[0m'


def colorize(msg, color):
    return color + msg + ENDC


class Channel(object):
    def __init__(self, name, out_pin, lb_pin, fb_pin):
        self.name = name
        self.out_pin = out_pin
        self.loopback_pin = lb_pin
        self.feedback_pin = fb_pin

    def init(self):
        GPIO.setup(self.out_pin, GPIO.OUT)
        GPIO.setup(self.loopback_pin, GPIO.IN)
        GPIO.setup(self.feedback_pin, GPIO.IN)

    def on(self):
        GPIO.output(self.out_pin, GPIO.HIGH)

    def off(self):
        GPIO.output(self.out_pin, GPIO.LOW)

    def is_lb_on(self):
        return self.lb_val == 1

    def is_fb_on(self):
        return self.fb_val == 1

    @property
    def lb_val(self):
        return GPIO.input(self.loopback_pin)

    @property
    def fb_val(self):
        return GPIO.input(self.feedback_pin)

    @staticmethod
    def get_result_str(t, t_val='True', f_val='False'):
        return colorize(t_val, OKGREEN) if t else colorize(f_val, FAIL)
    
    def test(self):
        prepend_char = 53 - len(self.name)
        print('**********************************************************************')
        print('****  TESTING: %s  %s' % (self.name, ''.join('*' for _ in range(prepend_char))))
        print('**********************************************************************')

        print('Turning on:')
        self.on()
        time.sleep(.25)
        print('\tLoopback On: %s, Val: %s' % (self.get_result_str(self.is_lb_on()), self.lb_val))
        print('\tFeedback On: %s, Val: %s' % (self.get_result_str(self.is_fb_on()), self.fb_val))
        
        print('\nTurning off:')
        self.off()
        time.sleep(.25)
        print('\tLoopback Off: %s, Val: %s' % (self.get_result_str(not self.is_lb_on()), self.lb_val))
        print('\tFeedback Off: %s, Val: %s' % (self.get_result_str(not self.is_fb_on()), self.fb_val))
        print('\n')


BOARD_WHITE = Channel("White", 32, 31, 22)
BOARD_GREEN = Channel("Green", 36, 33, 18)
BOARD_YELLOW = Channel("Yellow", 38, 35, 16)
BOARD_AUX = Channel("Aux", 40, 37, 12)

BOARD_CHANNELS = [BOARD_WHITE, BOARD_GREEN, BOARD_YELLOW, BOARD_AUX]

BCM_WHITE = Channel("White", 12, 6, 25)
BCM_GREEN = Channel("Green", 16, 13, 24)
BCM_YELLOW = Channel("Yellow", 20, 19, 23)
BCM_AUX = Channel("Aux", 21, 26, 18)

BCM_CHANNELS = [BCM_WHITE, BCM_GREEN, BCM_YELLOW, BCM_AUX]


def init_all(channels=None):
    if not channels:
        channels = BOARD_CHANNELS
    for channel in channels:
        channel.init()


def all_on(channels=None):
    if not channels:
        channels = BOARD_CHANNELS
    for channel in channels:
        channel.on()


def all_off(channels=None):
    if not channels:
        channels = BOARD_CHANNELS
    for channel in channels:
        channel.off()


def print_status(channels=None):
    if not channels:
        channels = BOARD_CHANNELS
    for channel in channels:
        channel.print_status()


def main(mode=None, channels=None):
    if not mode:
        mode = GPIO.BOARD

    if not channels:
        channels = BOARD_CHANNELS

    print('\nRunning tests with GPIO in %s mode...\n' % ('BCM' if mode == GPIO.BCM else 'BOARD'))

    print('Testing with the following channel configurations:')
    for channel in channels:
        print('\t%s:\tOut pin: %s, LB pin: %s, FB pin: %s' % (channel.name, channel.out_pin, channel.loopback_pin, channel.feedback_pin))

    print('')

    GPIO.setwarnings(False)
    GPIO.setmode(mode)

    for channel in channels:
        channel.init()
        channel.test()

    print('**********************************************************************')
    print('****  TESTING: ALL  %s' % (''.join('*' for _ in range(50))))
    print('**********************************************************************')

    print('Turning all channels on:')
    all_on(channels)
    time.sleep(.25)

    for channel in channels:
        print('\t%s:\tLoopback On: %s, Val: %s' % (channel.name, channel.get_result_str(channel.is_lb_on()), channel.lb_val))
        print('\t\tFeedback On: %s, Val: %s' % (channel.get_result_str(channel.is_lb_on()), channel.fb_val))

    print('\nTurning all channels off:')
    all_off(channels)
    time.sleep(.25)

    for channel in channels:
        print('\t%s:\tLoopback Off: %s, Val: %s' % (channel.name, channel.get_result_str(not channel.is_lb_on()), channel.lb_val))
        print('\t\tFeedback Off: %s, Val: %s' % (channel.get_result_str(not channel.is_lb_on()), channel.fb_val))


def cleanup():
    GPIO.cleanup()


def print_help_and_exit(exit_status=None):
    print ('test_relays.py -m [BOARD (default), BCM]')

    if exit_status:
        sys.exit(exit_status)
    else:
        sys.exit()


if __name__ == "__main__":
    argv = sys.argv[1:]
    mode = GPIO.BOARD
    channels = BOARD_CHANNELS

    try:
        opts, _ = getopt.getopt(argv, "hm:", ["help", "mode="])
    except getopt.GetoptError:
        print_help_and_exit(2)

    for opt, arg in opts:
        if opt in ('-h', '--help'):
            print_help_and_exit()
        elif opt in ("-m", "--mode"):
            if arg.lower() not in ['board', 'bcm']:
                print_help_and_exit(2)

            if arg.lower() == 'bcm':
                mode = GPIO.BCM
                channels = BCM_CHANNELS

    main(mode, channels)
    cleanup()

