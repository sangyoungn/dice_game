import board
import digitalio
import random
import time

class LED:
    '''
    Class LED
    Abtracts LED control over digital output port
    '''
    def __init__(self, port):
        self.port = digitalio.DigitalInOut(port)
        self.port.direction = digitalio.Direction.OUTPUT
        
    def on(self):
        self.port.value = True
        
    def off(self):
        self.port.value = False
        
        
class SWITCH:
    '''
    Class SWITCH
    Abstracts switch input over digital input port
    '''
    def __init__(self, port):
        self.port = digitalio.DigitalInOut(port)
        self.port.direction = digitalio.Direction.INPUT
        
    def value(self):
        return self.port.value
    
class DICE:
    '''
    Class DICE
    Represents each dice number with 7 LEDs
    '''
    def __init__(self, leds: list):
        '''
        Requires list comprised with 7 LEDs
        [D1, D2, D3, D4, D5, D6, D6]
        '''
        self.led_list = leds
        
    def decode(self, num):
        '''
        Coverts to the LED representation from a number
        '''
        decode = [ [False, False, False, True, False, False, False], \
                   [True, False, False, False, False, False, True], \
                   [True, False, False, True, False, False, True], \
                   [True, False, True, False, True, False, True], \
                   [True, False, True, True, True, False, True], \
                   [True, True, True, False, True, True, True] ]
        
        led_idx = 0
        for led in self.led_list:
            # Look up the state of each LED for a given number
            if decode[num-1][led_idx] == True:
                led.on()
            else:
                led.off()
            led_idx += 1
            
    def all_off(self):
        '''
        Method to turn off all LEDs
        '''
        for led in self.led_list:
            led.off()

class Dice_Game:
    '''
    Class Dice_Game
    Abstracts the rolling dice
    '''
    def __init__(self, dice:DICE):
        '''
        Requires a DICE class
        '''
        self.dice = dice
        
    def roll(self):
        
        # Random number determining how many time the dice will be rolling
        iter = random.randint(30, 50) 
        previous_number = 0 # Need to remember previously generated random number
        for i in range(iter):
            random_number = random.randint(1,6) # Generate a random number between 1 and 6
            while random_number == previous_number or random_number + previous_number == 7:
                # Cannot be same as previous generated number
                # A real dice roll shouldn't show the numbers on opposite sides in sequence.
                random_number = random.randint(1,6)
            self.dice.decode(random_number)

            # The delay between two consecutive numbers will increase exponentially.
            delay = 0.1 * ( 0.5 / 0.1 ) ** ( i / iter )
            # Added a random jitter
            delay = delay + random.uniform(0, 0.05)
            time.sleep(delay)
            previous_number = random_number # Store the number for reference in the next iteration.
        
        time.sleep(0.5)
        # Show the final number 3 times.
        for i in range(3):
            self.dice.all_off()
            time.sleep(0.5)
            self.dice.decode(random_number)
            time.sleep(0.5)
            
        self.dice.decode(random_number)

def dice_game_main():
    # List of LEDs
    leds = [ LED(board.PB4), LED(board.PC1), LED(board.PC2), LED(board.PD5), LED(board.PB5), LED(board.PD4), LED(board.PC3) ]

    # Switch instance
    switch = SWITCH(board.PC0)
    
    # Create a DICE instance with the list of LEDs
    dice = DICE(leds)

    # Create a Dice_Game instance with dice
    dice_game = Dice_Game(dice)

    while True:
        # Infinite Loop
        while switch.value():
            # Wait until the switch is pressed
            pass
        demo_number = 1
        while not switch.value():
            # Wait until the switch is released
            # While waiting, repeatedly show the dice numbers in turn.
            dice.decode(demo_number)
            demo_number += 1
            if demo_number > 6:
                demo_number = 1
            time.sleep(0.5)
           
        dice_game.roll()

if __name__ == '__main__':
    dice_game_main()