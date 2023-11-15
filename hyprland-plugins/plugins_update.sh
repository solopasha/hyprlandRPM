#!/usr/bin/bash
set -euxo pipefail

SPEC=hyprland-plugins.spec

oldCommit="$(sed -n 's/.*\bcommit0\b \(.*\)/\1/p' $SPEC)"
newCommit="$(curl -s -H "Accept: application/vnd.github.VERSION.sha" "https://api.github.com/repos/hyprwm/hyprland-plugins/commits/main")"

sed -i "s/$oldCommit/$newCommit/" $SPEC

perl -pe 's/(?<=bumpver\s)(\d+)/$1 + 1/ge' -i $SPEC
