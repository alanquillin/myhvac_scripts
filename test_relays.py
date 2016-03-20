import RPi.GPIO as GPIO
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

    def get_result_str(self, t, t_val='True', f_val='False'):
        if t:
            return colorize(t_val, OKGREEN)
        
        return colorize(f_val, FAIL)
    
    def print_status(self):
        print('%s Status:' % colorize(self.name, OKBLUE))
        lb_status = GPIO.input(self.loopback_pin) == 1
        fb_status = GPIO.input(self.feedback_pin) == 1
        print('\tLoopback: %s' % self.get_result_str(lb_status, 'On', 'Off'))
        print('\tFeedback: %s' % self.get_result_str(fb_status, 'On', 'Off'))
    
    def test(self):
        prepend_char = 53 - len(self.name)
        print('**********************************************************************')
        print('****  TESTING: %s  %s' % (self.name, ''.join('*' for _ in range(prepend_char))))
        print('**********************************************************************')

        print('Turning on:')
        self.on()
        time.sleep(.25)
        lb_val = GPIO.input(self.loopback_pin)
        fb_val = GPIO.input(self.feedback_pin)
        lb_status = lb_val == 1
        fb_status = fb_val == 1
        print('\tLoopback On: %s, Val: %s' % (self.get_result_str(lb_status), lb_val))
        print('\tFeedback On: %s, Val: %s' % (self.get_result_str(fb_status), fb_val))
        
        print('Turning off:')
        self.off()
        time.sleep(.25)
        lb_val = GPIO.input(self.loopback_pin)
        fb_val = GPIO.input(self.feedback_pin)
        lb_status = lb_val == 0
        fb_status = fb_val == 0
	print('\tLoopback Off: %s, Val: %s' % (self.get_result_str(lb_status), lb_val))
        print('\tFeedback Off: %s, Val: %s' % (self.get_result_str(fb_status), fb_val))
        print('\n')

WHITE = Channel("White", 32, 31, 22)
GREEN = Channel("Green", 36, 33, 18) 
YELLOW = Channel("Yellow", 38, 35, 16)
AUX = Channel("Aux", 40, 37, 12)

CHANNELS = [WHITE, GREEN, YELLOW, AUX]

def init_all(channels=None):
    if not channels:
        channels = CHANNELS
    for channel in channels:
        channel.init()

def all_on(channels=None):
    if not channels:
	channels = CHANNELS
    for channel in channels:
        channel.on()

def all_off(channels=None):
    if not channels:
        channels = CHANNELS
    for channel in channels:
        channel.off()

def print_status(channels=None):
    if not channels:
        channels = CHANNELS
    for channel in channels:
        channel.print_status()

def main():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)

    for channel in CHANNELS:
        channel.init()
        channel.test()

def cleanup():
    GPIO.cleanup()

if __name__ == "__main__":
    main()
    cleanup()

