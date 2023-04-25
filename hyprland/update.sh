#!/usr/bin/bash
set -eux

modified=0

oldHyprlandCommit="$(sed -n 's/.*hyprland_commit \(.*\)/\1/p' hyprland.spec)"
newHyprlandCommit="$(curl -s -H "Accept: application/vnd.github.VERSION.sha" "https://api.github.com/repos/hyprwm/Hyprland/commits/main")"

oldWlrootsCommit="$(sed -n 's/.*wlroots_commit \(.*\)/\1/p' hyprland.spec)"
newWlrootsCommit="$(curl -L \
            -H "Accept: application/vnd.github+json" \
            -H "X-GitHub-Api-Version: 2022-11-28" \
            https://api.github.com/repos/hyprwm/Hyprland/contents/subprojects/wlroots | jq -r '.sha')"

if [[ $oldHyprlandCommit != "$newHyprlandCommit" ]]; then
    modified+=1
    sed -i "s/$oldHyprlandCommit/$newHyprlandCommit/" hyprland.spec
fi

if [[ $oldWlrootsCommit != "$newWlrootsCommit" ]]; then
    modified+=1
    sed -i "s/$oldWlrootsCommit/$newWlrootsCommit/" hyprland.spec
fi

if [[ $modified -ge 1 ]]; then
    perl -pe 's/(?<=bumpver\s)(\d+)/$1 + 1/ge' -i hyprland.spec
fi

git --no-pager diff
git commit -am "up rev"
