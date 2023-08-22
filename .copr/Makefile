.PHONY: srpm
specfile = $(notdir $(spec))

srpm:
	dnf install -y rpm-build rpmdevtools python3-specfile
ifeq ($(specfile),hyprland-nvidia.spec)
	python3 nvidia.py > $(specfile)
endif
ifeq ($(specfile),hyprland-legacyrenderer.spec)
	sed '/legacyrenderer/s/0/1/;/Name:/s/hyprland/hyprland-legacyrenderer/' hyprland.spec > hyprland-legacyrenderer.spec
endif
	spectool -g ./$(specfile)
	rpmbuild -bs --define "_sourcedir ${PWD}" --define "_specdir ${PWD}" \
		--define "_builddir ${PWD}" --define "_srcrpmdir ${PWD}" --define \
		"_rpmdir ${PWD}" --define "_buildrootdir ${PWD}/.build" $(specfile)
	mv hyprland*.src.rpm $(outdir)
