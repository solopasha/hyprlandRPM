#!/usr/bin/bash
set -euxo pipefail

ec=0
newRelease=0

oldTag="$(rpmspec -q --qf "%{version}\n" hyprland-git.spec | head -1 | sed 's/\^.*//')"
newTag="$(curl "https://api.github.com/repos/hyprwm/Hyprland/tags" | jq -r '.[0].name' | sed 's/^v//')"

oldHyprlandCommit="$(sed -n 's/.*hyprland_commit \(.*\)/\1/p' hyprland-git.spec)"
newHyprlandCommit="$(curl -s -H "Accept: application/vnd.github.VERSION.sha" "https://api.github.com/repos/hyprwm/Hyprland/commits/main")"

oldWlrootsCommit="$(sed -n 's/.*wlroots_commit \(.*\)/\1/p' hyprland-git.spec)"
newWlrootsCommit="$(curl -L \
            -H "Accept: application/vnd.github+json" \
            -H "X-GitHub-Api-Version: 2022-11-28" \
            https://api.github.com/repos/hyprwm/Hyprland/contents/subprojects/wlroots | jq -r '.sha')"

oldProtocolsCommit="$(sed -n 's/.*protocols_commit \(.*\)/\1/p' hyprland-git.spec)"
newProtocolsCommit="$(curl -L \
            -H "Accept: application/vnd.github+json" \
            -H "X-GitHub-Api-Version: 2022-11-28" \
            https://api.github.com/repos/hyprwm/Hyprland/contents/subprojects/hyprland-protocols | jq -r '.sha')"

oldUdis86Commit="$(sed -n 's/.*udis86_commit \(.*\)/\1/p' hyprland-git.spec)"
newUdis86Commit="$(curl -L \
            -H "Accept: application/vnd.github+json" \
            -H "X-GitHub-Api-Version: 2022-11-28" \
            https://api.github.com/repos/hyprwm/Hyprland/contents/subprojects/udis86 | jq -r '.sha')"

sed -e "s/$oldHyprlandCommit/$newHyprlandCommit/" \
    -e "s/$oldWlrootsCommit/$newWlrootsCommit/" \
    -e "s/$oldProtocolsCommit/$newProtocolsCommit/" \
    -e "s/$oldUdis86Commit/$newUdis86Commit/" -i hyprland-git.spec

rpmdev-vercmp $oldTag $newTag || ec=$?
case $ec in
    0) ;;
    12)
        perl -pe 's/(?<=bumpver\s)(\d+)/0/' -i hyprland-git.spec
        sed -i "/^Version:/s/$oldTag/$newTag/" hyprland-git.spec
        newRelease=1 ;;
    *) exit 1
esac

git diff --quiet || \
{ perl -pe 's/(?<=bumpver\s)(\d+)/$1 + 1/ge' -i hyprland-git.spec && \
bash ../hyprland-plugins/plugins_update.sh;
git commit -am "up rev hyprland-git-${newTag}+${newHyprlandCommit:0:7}" && \
git push && \
hyprlandGitBuildId=$(copr-cli build-package solopasha/hyprland --nowait --name hyprland-git | sed -n 's/.*builds: \(.*\)/\1'/p) && \
copr-cli build-package solopasha/hyprland --nowait --name hyprland-plugins-git --after-build-id "$hyprlandGitBuildId" && \
copr-cli build-package solopasha/hyprland --nowait --name hyprland-nvidia-git; }

if [[ $newRelease == "1" ]]; then
    hyprlandBuildId=$(copr-cli build-package solopasha/hyprland --nowait --name hyprland | sed -n 's/.*builds: \(.*\)/\1'/p)
    parallel copr-cli build-package solopasha/hyprland --nowait --name ::: hyprland{-nvidia,-legacyrenderer}
    copr-cli build-package solopasha/hyprland --nowait --name hyprland-plugins --after-build-id "$hyprlandBuildId"
fi
