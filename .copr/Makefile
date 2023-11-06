.PHONY: srpm prepare
export specfile = $(notdir $(spec))

prepare:
	dnf install --nodocs -y rpm-build rpmdevtools

srpm: prepare
ifeq ($(findstring kitty.spec,$(specfile)),kitty.spec)
	dnf install --nodocs -y golang git-core
	go env -w GOPROXY=https://proxy.golang.org,direct
	go env -w GOSUMDB=sum.golang.org
	bash bundle_go_deps_for_rpm.sh kitty.spec
endif

ifeq ($(findstring hyprland,$(specfile)),hyprland)
	sed -e "/Name:/s/hyprland-git/$${specfile//.spec/}/" hyprland-git.spec > $(specfile)

    ifneq ($(findstring git,$(specfile)),git)
		sed 's/%global bumpver/#%&/' -i $(specfile)
    endif

    ifeq ($(specfile),hyprland-nvidia.spec)
		sed -e '1i Epoch: 1' -i $(specfile)
    endif

    ifeq ($(specfile),hyprland-legacyrenderer.spec)
		sed -e '/legacyrenderer/s/0/1/' -i $(specfile)
    endif
endif
	spectool -g ./$(specfile)
	rpmbuild -bs --define "_sourcedir ${PWD}" --define "_specdir ${PWD}" \
		--define "_builddir ${PWD}" --define "_srcrpmdir $(outdir)" --define \
		"_rpmdir ${PWD}" --define "_buildrootdir ${PWD}/.build" $(specfile)
