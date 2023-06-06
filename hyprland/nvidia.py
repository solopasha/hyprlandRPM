from specfile import Specfile

specfile = Specfile('hyprland.spec')

specfile.add_patch('nvidia.patch')
specfile.name = 'hyprland-nvidia'

print(specfile)
