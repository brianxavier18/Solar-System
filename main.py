import json
import time
import turtle
from pathlib import Path

from display import setup_screen, create_sun, draw_orbits
from planets import create_planets_from_config


ROOT = Path(__file__).parent


def load_config(path: Path):
    # Default configuration embedded in Python
    DEFAULT_CONFIG = {
        "screen": {
            "bgcolor": "black",
            "tracer": 0,
            "sleep": 0.01,
            "title": "Solar System",
            "width": 800,
            "height": 600,
            "sun_color": "yellow"
        },
        "scale": {
            "km_per_pixel": 1
        },
        "labels": {
            "color": "white",
            "font": ["Arial", 8, "normal"]
        },
        "planets": [
            { "name": "Mercury", "radius": 40,  "color": "grey",     "speed_kmh": 172332, "label_color": "white" },
            { "name": "Venus",   "radius": 80,  "color": "orange",   "speed_kmh": 126072, "label_color": "white" },
            { "name": "Earth",   "radius": 100, "color": "blue",     "speed_kmh": 107208, "label_color": "white" },
            { "name": "Mars",    "radius": 150, "color": "red",      "speed_kmh": 86677,  "label_color": "white" },
            { "name": "Jupiter", "radius": 180, "color": "brown",    "speed_kmh": 47052,  "label_color": "white" },
            { "name": "Saturn",  "radius": 230, "color": "pink",     "speed_kmh": 34884,  "label_color": "white" },
            { "name": "Uranus",  "radius": 250, "color": "lightblue","speed_kmh": 24480,  "label_color": "white" },
            { "name": "Neptune", "radius": 280, "color": "black",    "speed_kmh": 19548,  "label_color": "white" }
        ]
    }

    # helper: deep merge src into dst
    def deep_merge(dst, src):
        for k, v in src.items():
            if isinstance(v, dict) and isinstance(dst.get(k), dict):
                deep_merge(dst[k], v)
            else:
                dst[k] = v

    # try to load external config and merge over defaults
    try:
        if not path.exists():
            # create a config.json from defaults for user convenience
            try:
                with path.open('w', encoding='utf-8') as f:
                    json.dump(DEFAULT_CONFIG, f, indent=2, ensure_ascii=False)
            except Exception:
                pass

        with path.open('r', encoding='utf-8') as f:
            external = json.load(f)
    except Exception:
        return DEFAULT_CONFIG

    merged = DEFAULT_CONFIG.copy()
    deep_merge(merged, external)
    return merged


def main():
    cfg = load_config(ROOT / 'config.json')
    screen = setup_screen(cfg)
    sun_color = cfg.get('screen', {}).get('sun_color', 'yellow')
    sun = create_sun(color=sun_color)

    # optional: draw orbit guides
    draw_orbits(screen, cfg.get('planets', []))

    planets = create_planets_from_config(cfg)
    # armazenar writers para labels
    writers = [None] * len(planets)
    # apply label styles from config
    # always use the global label color (ignore per-planet label_color)
    global_label_color = cfg.get('labels', {}).get('color', 'white')
    global_label_font = cfg.get('labels', {}).get('font', ["Arial", 8, "normal"])
    for idx, _ in enumerate(planets):
        planets[idx].set_label_style(color=global_label_color, font=tuple(global_label_font))

    # controle de execução
    paused = {'value': False}
    speed_multiplier = {'value': 1.0}

    def toggle_pause():
        paused['value'] = not paused['value']

    def increase_speed():
        speed_multiplier['value'] *= 1.5

    def decrease_speed():
        speed_multiplier['value'] /= 1.5

    # keybindings
    screen.listen()
    screen.onkey(toggle_pause, 'space')
    screen.onkey(increase_speed, '+')
    screen.onkey(increase_speed, '=')  # tecla = também (sem shift)
    screen.onkey(decrease_speed, '-')

    try:
        last_time = time.time()
        km_per_pixel = cfg.get('scale', {}).get('km_per_pixel', 1000)
        sleep_time = cfg.get('screen', {}).get('sleep', 0.01)

        while True:
            now = time.time()
            dt = now - last_time
            last_time = now

            if not paused['value']:
                for idx, p in enumerate(planets):
                    p.move(sun)
                    p.step(dt_seconds=dt, km_per_pixel=km_per_pixel, speed_multiplier=speed_multiplier['value'])

                    # update label: remove previous writer and write again
                    if writers[idx] is not None:
                        try:
                            writers[idx].clear()
                            writers[idx].hideturtle()
                        except Exception:
                            pass
                    writers[idx] = p.label()

            # optional: show current speed multiplier in window title
            screen.title(f"Solar System — speed x{speed_multiplier['value']:.2f}")

            screen.update()
            time.sleep(sleep_time)
    except turtle.Terminator:
        pass


if __name__ == '__main__':
    main()
