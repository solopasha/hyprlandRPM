#!/usr/bin/bash
set -euxo pipefail

ec=0

SPEC=eww-git.spec

oldTag="$(rpmspec -q --qf "%{version}\n" $SPEC | head -1 | sed 's/\^.*//')"
newTag="$(curl "https://api.github.com/repos/elkowar/eww/tags" | jq -r '.[0].name' | sed 's/^v//')"

oldCommit="$(sed -n 's/.*\bcommit0\b \(.*\)/\1/p' $SPEC)"
newCommit="$(curl -s -H "Accept: application/vnd.github.VERSION.sha" "https://api.github.com/repos/elkowar/eww/commits/master")"


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
git commit -am "up rev eww-git-${newTag}+${newCommit:0:7}" && \
git push; }
