import turtle
from typing import Tuple


def setup_screen(cfg) -> turtle.Screen:
    screen = turtle.Screen()
    screen.bgcolor(cfg.get('screen', {}).get('bgcolor', 'black'))
    screen.tracer(cfg.get('screen', {}).get('tracer', 0))
    # set title and size if provided
    title = cfg.get('screen', {}).get('title')
    if title:
        screen.title(title)
    width = cfg.get('screen', {}).get('width')
    height = cfg.get('screen', {}).get('height')
    if width and height:
        try:
            screen.setup(width=width, height=height)
        except Exception:
            # some turtle implementations may not support setup; ignore
            pass
    return screen


def create_sun(color: str = 'yellow') -> turtle.Turtle:
    sun = turtle.Turtle()
    sun.shape('circle')
    sun.color(color)
    sun.shapesize(2)
    sun.penup()
    return sun


def draw_orbits(screen, planets_cfg):
    """Desenha círculos guia para as órbitas (opcional)."""
    drawer = turtle.Turtle()
    drawer.hideturtle()
    drawer.color('white')
    drawer.penup()
    drawer.speed('fastest')
    drawer.pensize(1)
    for p in planets_cfg:
        radius = p['radius']
        drawer.goto(0, -radius)
        drawer.pendown()
        drawer.circle(radius)
        drawer.penup()

    # não removemos os círculos — deixamos as órbitas visíveis
