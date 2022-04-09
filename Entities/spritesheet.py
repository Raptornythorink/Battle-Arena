
import pygame


class SpriteSheet:
    '''
    Represents a spritesheet based on an image.
    '''
    def __init__(self, image):
        self.sheet = image

    def get_image(self, pos, frame, width, height, scale, colour):
        '''
        Allows to select a specific frame in a spritesheet.

        :param pos: coordinates of the top-left corner of the first frame
        :param frame: the index number of the frame
        :param width: the width of each frame in pixels
        :param height: the height of each frame in pixels
        :param scale: factor used to rescale the image
        :param colour: the colour (rgb or rgba) corresponding to transparent:

        :returns: the selected image as a pygame surface
        '''
        image = pygame.Surface((width, height)).convert_alpha()
        image.blit(self.sheet, pos, ((frame * width), 0, width, height))
        image = pygame.transform.scale(image, (width * scale, height * scale))
        image.set_colorkey(colour)
        return image
