import array, time
from machine import Pin
from color_map import * #To design pattern
import rp2

class neopixel_pio:
    # pin_data          : Pin of the neopixel
    # nb_leds           : Number of led(s)
    # leds_brightness   : Led's brightness (0 to 1)
    def __init__(self, pin_data, nb_leds, leds_brightness=0.02):
        self.pin = pin_data
        self.num_leds = nb_leds
        self.brightness = leds_brightness

        @rp2.asm_pio(sideset_init=rp2.PIO.OUT_LOW, out_shiftdir=rp2.PIO.SHIFT_LEFT, autopull=True, pull_thresh=24)
        def ws2812():
            T1 = 2
            T2 = 5
            T3 = 3
            wrap_target()
            label("bitloop")
            out(x, 1)               .side(0)    [T3 - 1]
            jmp(not_x, "do_zero")   .side(1)    [T1 - 1]
            jmp("bitloop")          .side(1)    [T2 - 1]
            label("do_zero")
            nop()                   .side(0)    [T2 - 1]
            wrap()
        
        # Create the StateMachine with the ws2812 program, outputting on selected pin.
        self.sm = rp2.StateMachine(0, ws2812, freq=8_000_000, sideset_base=Pin(self.pin))
        
        # Start the StateMachine, it will wait for data on its FIFO.
        self.sm.active(1)

    # 24 bit data for each neopixel in the GRB order
    def pixel_set_and_dim(self,color, brightness):
        self.green=int(color[1]*brightness)
        self.red=int(color[0]*brightness)
        self.blue=int(color[2]*brightness)
        self.result= (self.green<<16)+(self.red<<8)+self.blue
        return self.result

    # Creates an array with the 24 bits value of GRB (Green, Red, Blue) for all pixels and sends it to the PIO
    def draw_ring(self,pattern,num_leds):
        # Creates an array, type of elements: unsigned integer,
        # initialized with a zeroed list of num_leds size
        # Array type, see : https://docs.python.org/3/library/array.html
        self.ar = array.array("I",[0]*num_leds)
        for i, color in enumerate(pattern):
            self.ar[i]=pixel_set_and_dim(color,self.brightness)

        self.sm.put(ar, 8) # pushes a word of data to the state machine
        # second parameter indicates a shift value for each pushed data (from ar).
        # data is coded with 32 bits, so the value pushes the 24 bits at the right position.
    
    #Function to clear neopixel        
    def shutdown(self):
        self.ring=[BLACK]*self.num_leds # complete ring
        self.draw_ring(self.ring, self.num_leds)

    #Function to simulate a flash
    #   Delay       : Delay in ms of pattern1 displaying
    #   pattern1    : First pattern to be displayed
    #   pattern2    : Second pattern to be displayed
    def neopixel_flashed_display(self, delay, pattern1, pattern2):
        self.draw_ring(pattern1, self.num_leds)
        time.sleep_ms(delay)
        self.draw_ring(pattern2, self.num_leds)

    #Function for an animated display
    #   counter     : Incremented counter for pattern selection (One in 2 number)  
    #   pattern1    : First pattern to be displayed
    #   pattern2    : Second pattern to be displayed
    def neopixel_alternate_display(self, counter, pattern1, pattern2):
        if (counter % 2) == 0:
            self.draw_ring(pattern1, self.num_leds)
        else:
            self.draw_ring(pattern2, self.num_leds)

    
#if __name__ == "__main__":
 








    