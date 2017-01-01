# *-* coding: utf-8 *-*

import os
import pygame
import time
import random
import platform

class gui:
    screen = None;
    
    def __init__(self):
        "Ininitializes a new pygame screen using the framebuffer"
        # Based on "Python GUI in Linux frame buffer"
        # http://www.karoltomala.com/blog/?p=679
	# and https://learn.adafruit.com/pi-video-output-using-pygame/pointing-pygame-to-the-framebuffer
        disp_no = os.getenv("DISPLAY")

        if platform.system() == 'Windows':
            os.environ['SDL_VIDEODRIVER'] = 'windib'

        if disp_no:
            print "I'm running under X display = {0}".format(disp_no)
        
        # Check which frame buffer drivers are available
        # Start with fbcon since directfb hangs with composite output
        drivers = ['fbcon', 'directfb', 'svgalib']
        found = False
        for driver in drivers:
            # Make sure that SDL_VIDEODRIVER is set
            if not os.getenv('SDL_VIDEODRIVER'):
                os.putenv('SDL_VIDEODRIVER', driver)
            try:
                pygame.display.init()
            except pygame.error:
                print 'Driver: {0} failed.'.format(driver)
                continue
            found = True
            break
    
        if not found:
            raise Exception('No suitable video driver found!')
        
        size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
        self.width = size[0]
        self.height = size[1]
        print "Framebuffer size: %d x %d" % (self.width, self.height)

        self.screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
        # Clear the screen to start
        self.screen.fill((0, 0, 0))        
        # Initialise font support
        pygame.font.init()
        # Render the screen
        pygame.display.update()
	# Hide mouse
        pygame.mouse.set_visible(False)


        self.cols = 3
        self.rows = 3
        self.margin = 100


    def __del__(self):
        "Destructor to make sure pygame shuts down, etc."

    def drawMenu(self, menu=[], selection=-1):
        borderColor = (255, 255, 255)
        lineColor = (64, 64, 64)
        subDividerColor = (128, 128, 128)
       
        boxSize = int((self.height - 2 * self.margin - (self.rows - 1) * self.margin/2)/self.rows)

		
        box_bg = (255, 255, 255)
        box_fg = (0, 0, 120)

		
        n = 1
        for row in range(self.rows):
            for col in range(self.cols):
                if (n - 1) < len(menu):
                    x = (self.width - self.cols * boxSize - (self.cols - 1) * self.margin / 2)/2 + boxSize * col + int(self.margin/2) * col
                    y = self.margin + row * boxSize + row * int(self.margin/2)
                    pygame.draw.rect(self.screen, borderColor, (x, y, boxSize, boxSize))
							
							
                    if str(n) == selection:
                        fg = (255, 0, 0)
                    else:
                        fg = box_fg
							
                    index_font = pygame.font.Font(None, 50)
                    index_surface = index_font.render(" %s " % n, True, box_bg, fg) # Black text with yellow BG
                    self.screen.blit(index_surface, (x, y))
					
                    menu_font = pygame.font.Font(None, 40)
                    menu_surface = menu_font.render("%s" % menu[n-1], True, fg, box_bg)
                    self.screen.blit(menu_surface, (x + 10, y + int(boxSize / 2) - 10))
				
                n += 1

        pygame.display.update()
    

# Create an instance of the PyScope class
scope = gui()
# Wait 10 seconds

selection = -1

while True:
    
    scope.drawMenu(['Photos', 'Vidéos'], selection)

    event = pygame.event.wait()
	
    if event.type == pygame.KEYDOWN:
        if chr(event.key) == 'q':
	        exit(0)
        else:
            print(chr(event.key))
            selection = chr(event.key)
		
	
# time.sleep(5)

