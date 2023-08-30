import os
from specfile import Specfile

specfile = Specfile('hyprland-git.spec')

specfile.add_patch('nvidia.patch')
specfile.name = os.getenv('specfile').removesuffix('.spec')

print(specfile)
