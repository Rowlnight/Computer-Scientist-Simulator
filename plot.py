import pygame
import matplotlib

matplotlib.use("Agg")

import matplotlib.backends.backend_agg as agg
import pylab
import matplotlib.pyplot as plt
import matplotlib

class Plot(pygame.sprite.Sprite):
    def __init__(self, stocks_list):
        self.fig = pylab.figure(figsize=[6, 4], dpi=100)
        ax = self.fig.gca()
        ax.set_title('Акции банка', color='C0')
        ax.plot(stocks_list)
        canvas = agg.FigureCanvasAgg(self.fig)
        canvas.draw()
        renderer = canvas.get_renderer()
        raw_data = renderer.tostring_rgb()
        size = canvas.get_width_height()
        self.surf = pygame.image.fromstring(raw_data, size, "RGB")

    def reshow(self, stocks_list):
        plt.close()
        self.fig = pylab.figure(figsize=[6, 4], dpi=100)
        
        ax = self.fig.gca()
        ax.set_title('Акции банка', color='C0')
        ax.plot(stocks_list)
        ax.plot([0, 0, 0], color='white')
        ax.plot([36000, 36000, 36000], color='white')
        
        canvas = agg.FigureCanvasAgg(self.fig)
        canvas.draw()
        renderer = canvas.get_renderer()
        raw_data = renderer.tostring_rgb()
        size = canvas.get_width_height()
        self.surf = pygame.image.fromstring(raw_data, size, "RGB")
        
