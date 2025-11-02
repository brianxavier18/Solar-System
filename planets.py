import turtle
from math import cos, sin


class Planet(turtle.Turtle):
    """Representa um planeta que orbita ao redor do sol (um turtle)."""

    def __init__(self, name: str, radius: float, color: str, speed_kmh: float, shape: str = 'circle', shapesize: float = 0.5):
        """radius: pixels on screen; speed_kmh: linear orbital speed in km/h"""
        super().__init__(shape=shape)
        self.name = name
        self.radius = radius
        self.color(color)
        self.penup()
        self.shapesize(shapesize)
        self.angle = 0.0
        # store linear speed in km/h; conversion to angular speed happens in step
        self.speed_kmh = speed_kmh
        # writer for persistent label (created later when label settings are provided)
        self._label_writer = None
        self._label_color = 'white'
        self._label_font = ("Arial", 8, "normal")

    def move(self, sun):
        """Posiciona o planeta de acordo com o ângulo atual em relação ao sol."""
        x = self.radius * cos(self.angle)
        y = self.radius * sin(self.angle)
        self.goto(sun.xcor() + x, sun.ycor() + y)

    def step(self, dt_seconds: float, km_per_pixel: float, speed_multiplier: float = 1.0):
        """Avança o ângulo do planeta usando:
        - dt_seconds: tempo decorrido neste frame (s)
        - km_per_pixel: escala (quantos km correspondem a 1 pixel)
        - speed_multiplier: multiplicador global de velocidade

        Cálculo:
        1) radius_pixels * km_per_pixel -> radius_km
        2) linear_speed_pixels_per_hour = speed_kmh / km_per_pixel
        3) angular_speed_rad_per_hour = linear_speed_pixels_per_hour / radius_pixels
        4) delta_angle = angular_speed * (dt_seconds / 3600) * speed_multiplier
        """
        if self.radius <= 0:
            return
        # linear speed in pixels per hour
        linear_pixels_per_hour = (self.speed_kmh / max(km_per_pixel, 1e-9))
        # avoid division by zero
        angular_speed_rad_per_hour = linear_pixels_per_hour / self.radius
        delta = angular_speed_rad_per_hour * (dt_seconds / 3600.0) * speed_multiplier
        self.angle += delta

    def label(self):
        """Cria ou atualiza o writer persistente para esse planeta e posiciona o texto."""
        if self._label_writer is None:
            self._label_writer = turtle.Turtle()
            self._label_writer.hideturtle()
            self._label_writer.penup()
        # move writer and rewrite
        self._label_writer.clear()
        self._label_writer.color(self._label_color)
        self._label_writer.goto(self.xcor() + 8, self.ycor() + 8)
        self._label_writer.write(self.name, font=tuple(self._label_font))
        return self._label_writer

    def set_label_style(self, color: str = 'white', font=('Arial', 8, 'normal')):
        self._label_color = color
        self._label_font = font


def create_planets_from_config(cfg):
    """Cria e retorna uma lista de Planet a partir da configuração JSON."""
    planets = []
    pd = cfg.get('planet_design', {})
    shape = pd.get('shape', 'circle')
    shapesize = pd.get('shapesize', 0.5)
    for p in cfg.get('planets', []):
        planets.append(Planet(p['name'], p['radius'], p['color'], p.get('speed_kmh', 0), shape=shape, shapesize=shapesize))
    return planets
