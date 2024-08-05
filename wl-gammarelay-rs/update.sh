#!/usr/bin/bash
set -euxo pipefail

ec=0

SPEC=wl-gammarelay-rs.spec

oldTag="$(rpmspec -q --qf "%{version}\n" $SPEC | head -1 | sed 's/\^.*//')"
newTag="$(curl "https://api.github.com/repos/MaxVerevkin/wl-gammarelay-rs/tags" | jq -r '.[0].name' | sed 's/^v//')"

oldCommit="$(sed -n 's/.*\bcommit0\b \(.*\)/\1/p' $SPEC)"
newCommit="$(curl -s -H "Accept: application/vnd.github.VERSION.sha" "https://api.github.com/repos/MaxVerevkin/wl-gammarelay-rs/commits/main")"

sed -i "s/$oldCommit/$newCommit/" $SPEC

rpmdev-vercmp "$oldTag" "$newTag" || ec=$?
case $ec in
    0) ;;
    12)
        perl -pe 's/(?<=bumpver\s)(\d+)/0/' -i $SPEC
        sed -i "/^Version:/s/$oldTag/$newTag/" $SPEC ;;
    *) exit 1
esac

git diff --quiet || \
{ perl -pe 's/(?<=bumpver\s)(\d+)/$1 + 1/ge' -i $SPEC && \
git commit -am "up rev wl-gammarelay-rs-${newTag}+${newCommit:0:7}" && \
git push && \
copr-cli build-package solopasha/hyprland --name wl-gammarelay-rs --nowait --enable-net on; }
