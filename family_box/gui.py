# *-* coding: utf-8 *-*

import os
import pygame
import time
import subprocess
import random
import platform
import logging

import sys
import traceback

base_dir = os.path.dirname(__file__)


if platform.system() == 'Windows':
    logging.basicConfig(level=logging.DEBUG, filename="family_pi.log")

    os.environ['SDL_VIDEODRIVER'] = 'windib'
    class OMXPlayer(file):
        def __init__(self, file):
            logging.info("Fake player : %s" % file)
            self._is_playing = True
            time.sleep(5)
            self._is_playing = False
            logging.info("Fake player : stop")

        def is_playing(self):
            return self._is_playing

else:
    logging.basicConfig(level=logging.DEBUG, filename="/tmp/family_pi.log")
    from omxplayer import OMXPlayer

data_dir = os.getenv('FAMILY_BOX_DATA')
if not data_dir:
    data_dir = os.path.join(base_dir, 'data')

def get_selection(event):
    if event.key >= 256:
        selection = event.key - 256
    else:
        try:
            selection = int(event.unicode)
        except:
            selection = event.unicode

    if selection in range(10):
        return selection
    else:
        return None

class Gui:
    screen = None;
    
    def __init__(self):
        "Ininitializes a new pygame screen using the framebuffer"
        # Based on "Python GUI in Linux frame buffer"
        # http://www.karoltomala.com/blog/?p=679
	# and https://learn.adafruit.com/pi-video-output-using-pygame/pointing-pygame-to-the-framebuffer
        disp_no = os.getenv("DISPLAY")

        if disp_no:
            logging.info("I'm running under X display = {0}".format(disp_no))
        
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
                logging.error('Driver: {0} failed.'.format(driver))
                continue
            found = True
            break
    
        if not found:
            raise Exception('No suitable video driver found!')
        
        size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
        self.width = size[0]
        self.height = size[1]
        logging.info("Framebuffer size: %d x %d" % (self.width, self.height))

        self.screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
        #self.screen = pygame.display.set_mode((1000, 800))
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

    def clear(self):
        self.screen.fill((0, 0, 0))

    def drawTopMenu(self, text, color=(0, 0, 230)):
        menu_font = pygame.font.Font(None, 40)
        menu_surface = menu_font.render(text, True, color, (0, 0, 0))
        self.screen.blit(menu_surface, (0, 0))

		
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

    def drawExplorerMenu(self, title, path):
        self.clear()

        self.drawTopMenu(title)

        self.drawBox(0, (20, self.height / 2 - self.box_size / 2), 'Accueil')

        font_size = 40
        entry_font = pygame.font.Font(None, font_size)

        n = 1
        self.current_choices = []
        for file in os.listdir(os.path.join(data_dir, path)):
            self.current_choices.append(os.path.join(path, file))
            entry_surface = entry_font.render(str(n) + " - " + file, True, (150, 150, 250), (0, 0, 0))
            self.screen.blit(entry_surface, (self.box_size + 100, font_size + font_size * n))
            n += 1

        pygame.display.update()


    def drawMenu(self, title, menu=[], selection=-1, error=False):

        self.clear()

        self.drawTopMenu(title)

        self.drawBox(0, (20, self.height / 2 - self.box_size / 2), 'Accueil')

        if error:
            self.drawTopMenu("Une erreur est survenue", color=(244, 0, 0))

        n = 1
        for row in range(self.rows):
            for col in range(self.cols):
                if (n - 1) < len(menu):
                    x = (self.width - self.cols * self.box_size - (self.cols - 1) * self.margin / 2)/2 + self.box_size * col + int(self.margin/2) * col
                    y = self.margin + row * self.box_size + row * int(self.margin/2)

                    if menu[n-1]:
                        self.drawBox(n, (x, self.height - y - self.box_size), menu[n-1])

                n += 1

        pygame.display.update()
    
    def drawHome(self, error=False):
        gui.drawMenu('Accueil', ['Photos', 'Videos', 'Films',
                       None, None, None,
                       None, None, None], -1, error=error)

    def drawPicturesMenu(self):
        gui.drawMenu('Photos', ['Ordre|normal', 'Ordre|inverse'])

    def drawVideosMenu(self):
        gui.current_path = 'Videos'
        gui.drawExplorerMenu('Videos', 'Videos')

    def drawMoviesMenu(self):
        gui.current_path = 'Films'
        gui.drawExplorerMenu('Films', 'Films')


    def showPicture(self, picture_path, current, nb):
        self.clear()

        picture = pygame.image.load(picture_path)

        (width, height) = picture.get_size()

        picture_ratio = (width + .0) / height

        if picture_ratio > self.ratio:
            picture = pygame.transform.scale(picture, (self.width, int(self.width / picture_ratio)))
        else:
            picture = pygame.transform.scale(picture, (int(self.height * picture_ratio), self.height))

        (width, height) = picture.get_size()
        self.screen.blit(picture, ((self.width - width) / 2, (self.height - height) / 2))

        if current == 0:
            title = "Appuyer sur 0 pour quitter ou 6 pour la photo suivante"
        elif current == nb - 1:
            title = "Appuyer sur 0 pour quitter, 4 pour la photo precedente"
        else:
            title = "Appuyer sur 0 pour quitter, 4 pour la photo precedente ou 6 pour la photo suivante"

        self.drawTopMenu("Photo %d sur %d : " % (current + 1, nb) + title)
        pygame.display.flip()


    def showSlideshow(self, n=None, reverse=False):
        logging.info("Slideshow")

        good_pictures = []

        for picture in os.listdir(os.path.join(data_dir, 'Photos')):
            if '.' in picture:
                ext = picture.split('.')[-1].lower()

                if ext in ['jpg', 'jpeg', 'gif', 'png']:
                    good_pictures.append(
                        {'name': picture,
                         'mtime': os.path.getmtime(os.path.join(data_dir, 'Photos', picture))}
                    )

        logging.debug("Raw pictures : %s" % good_pictures)
        good_pictures.sort(key = lambda p: p['mtime'])
        if n and n < len(good_pictures):
            good_pictures = good_pictures[0:n]

        if reverse:
            good_pictures.reverse()

        logging.debug("Good pictures : %s" % good_pictures)
        stopped = False

        nb_pictures = len(good_pictures)
        current_picture = 0

        while True:
            self.showPicture(os.path.join(data_dir, 'Photos', good_pictures[current_picture]['name']),
                             current_picture,
                             nb_pictures)

            while True:
                event = pygame.event.wait()

                if event.type == pygame.KEYDOWN:
                    selection = get_selection(event)
                    if selection == 0:
                        stopped = True
                        break

                    if selection == 4:
                        current_picture = max(current_picture - 1, 0)
                        break

                    if selection == 6:
                        current_picture = min(current_picture + 1, nb_pictures - 1)
                        break

                if stopped:
                    break

            if stopped:
                break

        self.drawPicturesMenu()

gui = Gui()

gui.drawHome()

while True:
    selection = -1

    event = pygame.event.wait()
	
    if event.type == pygame.KEYDOWN:
        selection = get_selection(event)
        if selection is None:
            continue
        logging.debug("Selection : %s" % selection)

        if selection == 0:
            gui.state = 'home'
            gui.drawHome()

        # Go back to main screen if error
        try:
            if gui.state == 'explorer':
                new_path = gui.current_choices[selection - 1]
                if os.path.isfile(os.path.join(data_dir, new_path)):
                    gui.drawTopMenu("Appuyer sur : 0 pour arreter, 4 pour reculer, 5 pour pause, 6 pour accelerer")
                    pygame.display.flip()

                    player = OMXPlayer(os.path.join(data_dir, new_path))
                    time.sleep(2)
                    status = "play"
                    while player.playback_status() in ['Playing', 'Paused']:
                        logging.debug("Playing")
                        event = pygame.event.poll()
                        if event != pygame.NOEVENT and event.type == pygame.KEYDOWN:
                            sel = get_selection(event)
                        else:
                            sel = None
                        sleep = 1
                        if sel == 0:
                            player.stop()
                        if sel == 5:
                            if status == "play":
                                status = "pause"
                                player.pause()
                            else:
                                status = "play"
                                player.play()
                        if sel == 4:
                            pos = player.position()
                            player.set_position(pos - 60)
                            sleep = 0
                        if sel == 6:
                            pos = player.position()
                            player.set_position(pos + 60)
                            sleep = 0
                        time.sleep(sleep)

                    # kill omxplayer to be sure :)
                    if platform.system() != 'Windows':
                        time.sleep(2)
                        subprocess.call(os.path.dirname(base_dir) + "/bin/kill-omxplayer")

                    parent = new_path.split(os.path.sep)[:-1]
                    if len(parent) > 1:
                        new_path = os.path.sep.join(parent)
                    else:
                        new_path = parent[0]
                    gui.drawExplorerMenu(new_path, new_path)
                else:
                    gui.drawExplorerMenu(new_path, new_path)

            if gui.state == 'pictures':
                if selection == 1:
                    gui.showSlideshow()
                if selection == 2:
                    gui.showSlideshow(reverse = True)

            if gui.state == 'home':
                if selection == 1:
                    gui.state = 'pictures'
                    gui.drawPicturesMenu()

                if selection == 2:
                    gui.state = 'explorer'
                    gui.drawVideosMenu()

                if selection == 3:
                    gui.state = 'explorer'
                    gui.drawMoviesMenu()

            error = False

        except:
            error = True
            #exc_type, exc_value, exc_traceback = sys.exc_info()
            #traceback.print_exc(exc_traceback)
            logging.exception("Got exception in main loop")


        if error:
            gui.state = 'home'
            gui.drawHome(error)

        if selection == 9:
            exit(0)


        while pygame.event.get():
            pass

	
# time.sleep(5)

