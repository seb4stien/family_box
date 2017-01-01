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

    def drawMenu(self):
        borderColor = (255, 255, 255)
        lineColor = (64, 64, 64)
        subDividerColor = (128, 128, 128)
       
	boxSize = int((self.height - 2 * self.margin - (self.rows - 1) * self.margin)/self.rows)

        print("Box : %s" % boxSize)

        for col in range(self.cols):
            x = self.margin + boxSize * col + int(self.margin / 2) * col
            print("x = %s" % x)
            for row in range(self.rows):
                y = self.margin + row * boxSize + row * int(self.margin / 2)
                pygame.draw.rect(self.screen, borderColor, (x, y, boxSize, boxSize))

        pygame.display.update()
    
    def drawGraticule(self):
        "Renders an empty graticule"
        # The graticule is divided into 10 columns x 8 rows
        # Each cell is 50x40 pixels large, with 5 subdivisions per
        # cell, meaning 10x8 pixels each.  Subdivision lines are
        # displayed on the central X and Y axis
        # Active area = 10,30 to 510,350 (500x320 pixels)
        borderColor = (255, 255, 255)
        lineColor = (64, 64, 64)
        subDividerColor = (128, 128, 128)
        # Outer border: 2 pixels wide
        pygame.draw.rect(self.screen, borderColor, (8,28,504,324), 2)
        # Horizontal lines (40 pixels apart)
        for i in range(0, 7):
            y = 70+i*40
            pygame.draw.line(self.screen, lineColor, (10, y), (510, y))
        # Vertical lines (50 pixels apart)
        for i in range(0, 9):
            x = 60+i*50
            pygame.draw.line(self.screen, lineColor, (x, 30), (x, 350))
        # Vertical sub-divisions (8 pixels apart)
        for i in range(1, 40):
            y = 30+i*8
            pygame.draw.line(self.screen, subDividerColor, (258, y), (262, y))
        # Horizontal sub-divisions (10 pixels apart)
        for i in range(1, 50):
            x = 10+i*10
            pygame.draw.line(self.screen, subDividerColor, (x, 188), (x, 192))

    def test(self):
        "Test method to make sure the display is configured correctly"
        adcColor = (255, 255, 0)  # Yellow
        self.drawGraticule()
        # Get a font and use it render some text on a Surface.
        font = pygame.font.Font(None, 30)
        text_surface = font.render('pyScope (%s)' % "0.1", 
            True, (255, 255, 255))  # White text
        # Blit the text at 10, 0
        self.screen.blit(text_surface, (10, 0))
        # Render some text with a background color
        text_surface = font.render('Channel 0',
            True, (0, 0, 0), (255, 255, 0)) # Black text with yellow BG
        # Blit the text
        self.screen.blit(text_surface, (540, 30))
        # Update the display
        pygame.display.update()
        # Random adc data
        yLast = 260
        for x in range(10, 509):
            y = random.randrange(30, 350, 2) # Even number from 30 to 350
            pygame.draw.line(self.screen, adcColor, (x, yLast), (x+1, y))
            yLast = y
            pygame.display.update()

# Create an instance of the PyScope class
scope = gui()
scope.drawMenu()
# Wait 10 seconds
time.sleep(10)

