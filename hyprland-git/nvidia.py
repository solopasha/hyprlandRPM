from specfile import Specfile

specfile = Specfile('hyprland-git.spec')

specfile.add_patch('nvidia.patch')
specfile.name = 'hyprland-nvidia-git'

print(specfile)
