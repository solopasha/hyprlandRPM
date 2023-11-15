.PHONY: prepare goprep srpm
specfile = $(notdir $(spec))

prepare:
	dnf install --nodocs -y rpm-build rpmdevtools

goprep:
	dnf install --nodocs -y golang git-core
	go env -w GOPROXY=https://proxy.golang.org,direct
	go env -w GOSUMDB=sum.golang.org

hyprland-plugins-git.spec:
	mv hyprland-plugins.spec hyprland-plugins-git.spec
	sed -e '/%global build_for/s/release/git/' -i $(specfile)

hyprland%spec:
	sed -e "/Name:/s/hyprland-git/$(basename $(specfile))/" hyprland-git.spec > $(specfile)
    ifneq ($(findstring git,$(specfile)),git)
		sed 's/%global bumpver/#%&/' -i $(specfile)
    endif

    ifeq ($(specfile),hyprland-nvidia.spec)
		sed -e '1i Epoch: 1' -i $(specfile)
    endif

    ifeq ($(specfile),hyprland-legacyrenderer.spec)
		sed -e '/legacyrenderer/s/0/1/' -i $(specfile)
    endif

kitty.spec: goprep
	bash bundle_go_deps_for_rpm.sh kitty.spec

srpm: prepare $(specfile)
	spectool -g ./$(specfile)
	rpmbuild -bs --define "_sourcedir ${PWD}" --define "_specdir ${PWD}" \
		--define "_builddir ${PWD}" --define "_srcrpmdir $(outdir)" --define \
		"_rpmdir ${PWD}" --define "_buildrootdir ${PWD}/.build" $(specfile)
