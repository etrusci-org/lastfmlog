import os
import json

from .core import Core
from .cliparser import CLIParser




confFile = os.path.abspath(os.path.join(os.path.dirname(__file__), 'conf.json'))
with open(confFile) as f:
    conf = json.load(f)

bannerFile = os.path.abspath(os.path.join(os.path.dirname(__file__), 'banner.ascii'))
with open(bannerFile) as f:
    banner = f.read()




__all__ = [
    'Core',
    'CLIParser',
    'conf',
    'banner',
]
