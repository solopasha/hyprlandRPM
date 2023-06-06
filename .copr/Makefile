srpm:
		dnf install -y rpm-build rpmdevtools python3-specfile
		python3 nvidia.py > hyprland-nvidia.spec
		spectool -g ./hyprland-nvidia.spec
		rpmbuild -bs --define "_sourcedir ${PWD}" --define "_specdir ${PWD}" \
			--define "_builddir ${PWD}" --define "_srcrpmdir ${PWD}" --define \
			"_rpmdir ${PWD}" --define "_buildrootdir ${PWD}/.build" hyprland-nvidia.spec
		mv hyprland-nvidia*.src.rpm $$outdir
