from recipe import Recipe
from quantities import units as u
import json

#unitNames = [u.symbol for _, u in units.__dict__.items() if isinstance(u, type(units.deg))] + [u for u, f in u.__dict__.items() if isinstance(f, type(units.deg))]
un = [bar for bar, foo in u.__dict__.items() if isinstance(foo, type(u.m))]