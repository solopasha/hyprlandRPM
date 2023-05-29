#!/usr/bin/bash
set -eux

ec=0

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

sed -i "s/$oldHyprlandCommit/$newHyprlandCommit/" hyprland-git.spec
sed -i "s/$oldWlrootsCommit/$newWlrootsCommit/" hyprland-git.spec
sed -i "s/$oldProtocolsCommit/$newProtocolsCommit/" hyprland-git.spec

rpmdev-vercmp $oldTag $newTag || ec=$?
case $ec in
    0) ;;
    12)
        perl -pe 's/(?<=bumpver\s)(\d+)/0/' -i hyprland-git.spec
        sed -i "/^Version:/s/$oldTag/$newTag/" hyprland-git.spec ;;
    *) exit 1
esac

git diff --quiet || \
{ perl -pe 's/(?<=bumpver\s)(\d+)/$1 + 1/ge' -i hyprland-git.spec && \
git commit -am "up rev hyprland-git-${newTag}+${newHyprlandCommit:0:7}" && \
git push; }
