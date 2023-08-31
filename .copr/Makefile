.PHONY: srpm
export specfile = $(notdir $(spec))

prepare:
	dnf install -y rpm-build rpmdevtools

srpm: prepare
	sed -e "/Name:/s/hyprland-git/$${specfile//.spec/}/" hyprland-git.spec > $(specfile)
ifneq ($(findstring git,$(specfile)),git)
	sed 's/%global bumpver/#%&/' \
		-i $(specfile)
endif
ifeq ($(specfile),hyprland-nvidia.spec)
	sed -e '1i Epoch: 1' \
		-i $(specfile)
endif
ifeq ($(specfile),hyprland-legacyrenderer.spec)
	sed -e '/legacyrenderer/s/0/1/' \
		-i $(specfile)
endif
	spectool -g ./$(specfile)
	rpmbuild -bs --define "_sourcedir ${PWD}" --define "_specdir ${PWD}" \
		--define "_builddir ${PWD}" --define "_srcrpmdir $(outdir)" --define \
		"_rpmdir ${PWD}" --define "_buildrootdir ${PWD}/.build" $(specfile)
