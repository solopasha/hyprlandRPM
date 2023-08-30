.PHONY: srpm
specfile = $(notdir $(spec))

prepare:
	dnf install -y rpm-build rpmdevtools python3-specfile

srpm: prepare
	export SPECFILE=$(specfile)
ifeq ($(specfile),hyprland.spec)
	sed -e '/Name:/s/hyprland-git/$${specfile//.spec/}/' \
		-e '/%global bumpver/s/[[:digit:]]\+/0/' \
		hyprland-git.spec > $(specfile)
endif
ifeq ($(specfile),hyprland-nvidia.spec)
	python3 nvidia.py > $(specfile)
	sed -e '1i Epoch: 1' \
		-e'/hyprland-portals.conf/d' \
		-e '/%global bumpver/s/[[:digit:]]\+/0/' \
		-i $(specfile)
endif
ifeq ($(specfile),hyprland-legacyrenderer.spec)
	sed -e '/legacyrenderer/s/0/1/' \
		-e '/Name:/s/hyprland-git/$${specfile//.spec/}/' \
		-e '/%global bumpver/s/[[:digit:]]\+/0/' \
		hyprland-git.spec > $(specfile)
endif
ifeq ($(specfile),hyprland-nvidia-git.spec)
	python3 nvidia.py > $(specfile)
endif
	spectool -g ./$(specfile)
	rpmbuild -bs --define "_sourcedir ${PWD}" --define "_specdir ${PWD}" \
		--define "_builddir ${PWD}" --define "_srcrpmdir $(outdir)" --define \
		"_rpmdir ${PWD}" --define "_buildrootdir ${PWD}/.build" $(specfile)
