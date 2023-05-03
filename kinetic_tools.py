import pygame
import numpy
from scipy.constants import pi

def load_image(image_path, scaling_factor: float=1)->tuple:
    image = zoom_image(pygame.image.load(image_path), scaling_factor=scaling_factor).convert_alpha()
    return image, image.get_rect()

def zoom_image(image: pygame.Surface, scaling_factor: float=1) -> pygame.Surface:
    current_width, current_height = image.get_size()
    new_size = (current_width*scaling_factor, current_height*scaling_factor)
    new_image = pygame.transform.scale(image, new_size)
    return new_image



class Particle(pygame.sprite.Sprite):

    def __init__(self, image_path: str, position: tuple=(100, 100), velocity: tuple=(100, 100), mass: float = 10, scaling_factor: float=1):
        super().__init__()
        self.image, self.rect = load_image(image_path, scaling_factor)
        self.rect.x, self.rect.y = position
        self.__width, self.__height = self.image.get_size()
        self.velocity_x, self.velocity_y = 0, 0
        self.__init_velocity_x, self.__init_velocity_y = velocity
        self.mass = mass

    def get_width(self):
        return self.__width
    
    def get_height(self):
        return self.__height

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    def move_surroundings(self, surroundings, dx, dy):
        surroundings.rect.x += dx
        surroundings.rect.y += dy

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))
    
    def update(self, dt, mode = None, surroundings = None):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.velocity_y -= self.__init_velocity_y
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.velocity_y += self.__init_velocity_y
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.velocity_x -= self.__init_velocity_x
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.velocity_x += self.__init_velocity_x

        dx = self.velocity_x*dt
        dy = self.velocity_y*dt
        
        if not mode:
            self.move(dx, dy)
        
        if mode=="fixed" and surroundings:
            self.move_surroundings(surroundings, dx, dy)
            pass


class ViscousFluid:
    def __init__(self, dynamic_viscosity = 1.4):
        self.__viscosity = dynamic_viscosity

    @property
    def viscosity(self):
        return self.__viscosity
    
    @viscosity.setter
    def viscosity(self, dynamic_viscosity):
        if dynamic_viscosity<=0:
            raise ValueError("Viscosity can't be less than or equal to zero.")
        self.__viscosity = dynamic_viscosity
    

    def damping(self, part: Particle, dt):
        part_width, part_height = part.image.get_size()
        radius = part_width/2

        attenuation_coefficient = 6*pi*self.viscosity*radius/part.mass

        dv_x = attenuation_coefficient*numpy.absolute(part.velocity_x)*dt
        dv_y = attenuation_coefficient*numpy.absolute(part.velocity_y)*dt

        if part.velocity_x>0:
            part.velocity_x -= dv_x
        if part.velocity_x<0:
            part.velocity_x += dv_x
        if numpy.absolute(part.velocity_x)<5:
            part.velocity_x = 0

        if part.velocity_y>0:
            part.velocity_y -= dv_y
        if part.velocity_y<0:
            part.velocity_y += dv_y
        if numpy.absolute(part.velocity_y)<5:
            part.velocity_y = 0

class Background(pygame.sprite.Sprite):
    def __init__(self, background_image_path, position=(100, 100), scaling_factor = 1):
        self.image, self.rect = load_image(background_image_path, scaling_factor)
        self.rect.x, self.rect.y = position
        self.width, self.height = self.image.get_size()

    def draw(self, screen, positions: tuple=None):
        current_pos = self.rect.x, self.rect.y
        if not positions:
            screen.blit(self.image, current_pos)
        else:
            screen.blit(self.image, positions)


def restrict_area(screen: pygame.Surface, part: Particle):
    margin = 12
    if part.rect.y > screen.get_height()-part.get_height()+margin or part.rect.y < -margin:
        part.velocity_y = -part.velocity_y
    if part.rect.x > screen.get_width()-part.get_width()+margin or part.rect.x<-margin:
        part.velocity_x = - part.velocity_x

    if part.rect.x < -margin:
        part.rect.x = -margin
    if part.rect.x > screen.get_width()-part.get_width()+margin:
        part.rect.x = screen.get_width()-part.get_width()+margin
    if part.rect.y < -margin:
        part.rect.y = -margin
    if part.rect.y > screen.get_height()-part.get_height()+margin:
        part.rect.y = screen.get_height()-part.get_height()+margin