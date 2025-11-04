"""Módulo simples de estrelas para o simulador.

Fornece:
- init_stars(cfg, screen, sun, planet_radii) -> list de dicts de estrela
- update_stars(stars, cfg, now) -> atualiza e remove estrelas expiradas

As estrelas são representadas por turtles pequenas; cada estrela tem um tempo de vida
curto (padrão 0.5s) e surge aleatoriamente pela tela.
"""
import random
import time
import math
import turtle
from typing import List, Dict


def _random_point_avoid_orbits(cx, cy, planet_radii, margin, max_range):
    # escolhe uma distância radial que não esteja muito perto das órbitas
    if not planet_radii:
        r = random.uniform(0, max_range)
    else:
        radii = sorted(planet_radii)
        choices = []
        for i in range(len(radii)-1):
            inner = radii[i] + margin
            outer = radii[i+1] - margin
            if outer > inner:
                choices.append((inner, outer))
        # area outside largest orbit
        choices.append((radii[-1] + margin, max_range))
        rng = random.choice(choices)
        r = random.uniform(rng[0], max(rng[1], rng[0]+1))

    angle = random.random() * 2 * math.pi
    x = cx + r * math.cos(angle)
    y = cy + r * math.sin(angle)
    return x, y


def random_light_color():
    """Gera uma cor clara/pastel em hex (ex: #f2f7ff)."""
    r = random.randint(180, 255)
    g = random.randint(180, 255)
    b = random.randint(180, 255)
    return f'#{r:02x}{g:02x}{b:02x}'


def random_vivid_color():
    """Gera uma cor mais viva (tons saturados) em hex."""
    r = random.randint(100, 255)
    g = random.randint(100, 255)
    b = random.randint(100, 255)
    return f'#{r:02x}{g:02x}{b:02x}'


def init_stars(cfg: Dict, screen, sun, planet_radii: List[float]):
    """Cria um container e popula com algumas estrelas iniciais."""
    stars = []
    count = cfg.get('stars', {}).get('count', 0) if cfg.get('stars') else 0
    if count <= 0:
        count = 120

    # tentar usar o tamanho real do canvas para preencher horizontal e vertical
    try:
        canvas = screen.getcanvas()
        width = canvas.winfo_width()
        height = canvas.winfo_height()
        if width <= 1 or height <= 1:
            width = cfg.get('screen', {}).get('width', 800)
            height = cfg.get('screen', {}).get('height', 600)
    except Exception:
        width = cfg.get('screen', {}).get('width', 800)
        height = cfg.get('screen', {}).get('height', 600)
    max_x = width // 2
    max_y = height // 2
    cx, cy = sun.xcor(), sun.ycor()

    lifetime = cfg.get('stars', {}).get('lifetime', 0.5) if cfg.get('stars') else 0.5

    # construir paleta: combinar tons pastel e cores vivas
    palette = []
    # permitir configuração externa
    if cfg.get('stars') and cfg.get('stars').get('colors'):
        palette = list(cfg.get('stars').get('colors'))
    else:
        # gerar uma base de cores pastel e vivas
        for _ in range(8):
            palette.append(random_light_color())
        for _ in range(6):
            palette.append(random_vivid_color())

    for _ in range(count):
        # posicionamento por toda a tela: usar largura e altura completas
        x = random.uniform(-max_x, max_x)
        y = random.uniform(-max_y, max_y)
        t = turtle.Turtle()
        t.hideturtle()
        t.penup()
        t.goto(x, y)
        t.shape('circle')
        t.shapesize(0.08)
        color = random.choice(palette)
        t.color(color)
        t.showturtle()
        stars.append({'t': t, 'born': time.time(), 'life': lifetime, 'color': color})

    return stars


def update_stars(stars: List[Dict], cfg: Dict, now: float):
    """Atualiza o estado das estrelas: remove expiradas e ocasionalmente cria novas.

    Opcionalmente recebe um objeto `screen` dentro de `cfg['__screen_obj__']` ou pode
    ser chamado com o parâmetro screen passado diretamente (compatível com chamadas
    anteriores)."""
    spawn_chance = cfg.get('stars', {}).get('spawn_chance', 0.2) if cfg.get('stars') else 0.2
    max_new = cfg.get('stars', {}).get('max_new_per_frame', 6) if cfg.get('stars') else 6

    alive = []
    for s in stars:
        t = s['t']
        age = now - s['born']
        frac = age / max(s['life'], 1e-9)
        if frac >= 1.0:
            try:
                t.clear()
                t.hideturtle()
                t.goto(10000, 10000)
            except Exception:
                pass
            continue
        # triangular fade
        if frac < 0.5:
            size = 0.08 + frac * (0.3 - 0.08) * 2
        else:
            size = 0.3 - (frac - 0.5) * (0.3 - 0.08) * 2
        try:
            t.shapesize(max(0.04, size))
        except Exception:
            pass
        alive.append(s)

    # spawn novas estrelas por toda a tela (usar tamanho real do canvas se possível)
    spawned = 0
    # obter dimensão do canvas (se caller colocou o objeto screen dentro de cfg)
    try:
        screen_obj = cfg.get('__screen_obj__') if cfg.get('__screen_obj__') else None
        if screen_obj:
            canvas = screen_obj.getcanvas()
            width = canvas.winfo_width()
            height = canvas.winfo_height()
            if width <= 1 or height <= 1:
                width = cfg.get('screen', {}).get('width', 800)
                height = cfg.get('screen', {}).get('height', 600)
        else:
            width = cfg.get('screen', {}).get('width', 800)
            height = cfg.get('screen', {}).get('height', 600)
    except Exception:
        width = cfg.get('screen', {}).get('width', 800)
        height = cfg.get('screen', {}).get('height', 600)
    max_x = width // 2
    max_y = height // 2
    # construir paleta local (igual à usada em init_stars)
    palette = []
    if cfg.get('stars') and cfg.get('stars').get('colors'):
        palette = list(cfg.get('stars').get('colors'))
    else:
        for _ in range(8):
            palette.append(random_light_color())
        for _ in range(6):
            palette.append(random_vivid_color())

    for _ in range(max_new):
        if random.random() < spawn_chance:
            x = random.uniform(-max_x, max_x)
            y = random.uniform(-max_y, max_y)
            t = turtle.Turtle()
            t.hideturtle()
            t.penup()
            t.goto(x, y)
            t.shape('circle')
            t.shapesize(0.06)
            color = random.choice(palette)
            t.color(color)
            t.showturtle()
            alive.append({'t': t, 'born': now, 'life': 0.6, 'color': color})
            spawned += 1
            if spawned >= max_new:
                break

    stars.clear()
    stars.extend(alive)
