# *-* coding: utf-8 *-*

import os
import pygame
import time
import random
import platform
import logging

logging.basicConfig(level = logging.DEBUG)

class Gui:
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
        self.ratio = (self.width + .0) / self.height
        self.box_size = int((self.height - 2 * self.margin - (self.rows - 1) * self.margin / 2) / self.rows)

        self.state = 'home'

    def __del__(self):
        "Destructor to make sure pygame shuts down, etc."

		
    def drawBox(self, n, (x, y), text):
        
        borderColor = (255, 255, 255)
        lineColor = (64, 64, 64)

        box_bg = (255, 255, 255)
        box_fg = (0, 0, 120)

        fg = box_fg

        pygame.draw.rect(self.screen, borderColor, (x, y, self.box_size, self.box_size))

        index_font = pygame.font.Font(None, 50)
        index_surface = index_font.render(" %s " % n, True, box_bg, fg)  # Black text with yellow BG
        self.screen.blit(index_surface, (x, y))

        if '|' in text:
            text1, text2 = text.split('|')
        else:
            text1 = text
            text2 = None

        menu_font = pygame.font.Font(None, 40)
        menu_surface = menu_font.render("%s" % text1, True, fg, box_bg)
        self.screen.blit(menu_surface, (x + 10, y + int(self.box_size / 2) - 10))

        if text2:
            offset = menu_surface.get_size()[1]
            menu_surface = menu_font.render("%s" % text2, True, fg, box_bg)
            self.screen.blit(menu_surface, (x + 10, y + int(self.box_size / 2) - 10 + offset))


    def drawMenu(self, menu=[], selection=-1, error=False):

        self.screen.fill((0, 0, 0))

        self.drawBox(0, (20, self.height / 2 - self.box_size / 2), 'Accueil')

        if error:
            error_font = pygame.font.Font(None, 40)
            error_surface = error_font.render("Une erreur est survenue.", True, (244, 0, 0), (0, 0, 0))
            self.screen.blit(error_surface, (0, 0))

        n = 1
        for row in range(self.rows):
            for col in range(self.cols):
                if (n - 1) < len(menu):
                    x = (self.width - self.cols * self.box_size - (self.cols - 1) * self.margin / 2)/2 + self.box_size * col + int(self.margin/2) * col
                    y = self.margin + row * self.box_size + row * int(self.margin/2)

                    self.drawBox(n, (x, y), menu[n-1])

                n += 1

        pygame.display.update()
    
    def drawHome(self, error=False):
        gui.drawMenu(['Photos', 'Videos'], -1, error=error)

    def drawPicturesMenu(self):
        gui.drawMenu(['Toutes', '10|dernieres', '20|dernieres'], selection)




    def showPicture(self, picture_path):
        self.screen.fill((0, 0, 0))
        picture = pygame.image.load(picture_path)

        (width, height) = picture.get_size()

        picture_ratio = (width + .0) / height

        if picture_ratio > self.ratio:
            picture = pygame.transform.scale(picture, (self.width, int(self.width / picture_ratio)))
        else:
            picture = pygame.transform.scale(picture, (int(self.height * picture_ratio), self.height))

        (width, height) = picture.get_size()
        self.screen.blit(picture, ((self.width - width) / 2, (self.height - height) / 2))
        pygame.display.flip()

    def showSlideshow(self, n=None):
	logging.info("Slidshow")

        good_pictures = []

        for picture in os.listdir('data/pictures'):
            if '.' in picture:
                ext = picture.split('.')[-1].lower()

                if ext in ['jpg', 'jpeg', 'gif', 'png']:
                    good_pictures.append(
                        {'name': picture,
                         'mtime': os.path.getmtime('data/pictures/%s' % picture)}
                    )

	logging.debug("Raw pictures : %s" % good_pictures)
        good_pictures.sort(key = lambda p: p['mtime'])
        if n and n < len(good_pictures):
            good_pictures = good_pictures[0:n]

	logging.debug("Good pictures : %s" % good_pictures)
        for picture in good_pictures:
            self.showPicture('data/pictures/%s' % picture['name'])
            time.sleep(5)

        self.drawPicturesMenu()

gui = Gui()

gui.drawHome()

while True:
    selection = -1

    event = pygame.event.wait()
	
    if event.type == pygame.KEYDOWN:
	#print(event)
        if event.key >= 256:
            selection = event.key - 256
        else:
            try:
                selection = int(event.unicode)
            except:
                selection = event.unicode

        # Go back to main screen if error
        try:
            if gui.state == 'pictures':
                if selection == 1:
                    gui.showSlideshow()
                if selection == 2:
                    gui.showSlideshow(2)
                if selection == 3:
                    gui.showSlideshow(3)


            if gui.state == 'home':
                if selection == 1:
                    gui.state = 'pictures'
                    gui.drawPicturesMenu()

            error = False

        except:
            error = True

        if error:
            gui.state = 'home'
            gui.drawHome(error)

        if selection == 0:
            gui.state = 'home'
            gui.drawHome()

        if selection == 9:
            exit(0)

	
# time.sleep(5)

