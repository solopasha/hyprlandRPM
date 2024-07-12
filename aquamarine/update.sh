#!/usr/bin/bash
set -euxo pipefail

ec=0

SPEC=aquamarine.spec
REPO=hyprwm/aquamarine
BRANCH=main

oldTag="$(rpmspec -q --qf "%{version}\n" --srpm $SPEC | sed 's/[\^,~].*//')"
newTag="$(curl "https://api.github.com/repos/$REPO/tags" | jq -r '.[0].name' | sed 's/^v//')"
if [[ $newTag == "null" ]]; then
    newTag="0.1.0"
fi

oldCommit="$(sed -n 's/.*\bcommit0\b \(.*\)/\1/p' $SPEC)"
newCommit="$(curl -s -H "Accept: application/vnd.github.VERSION.sha" "https://api.github.com/repos/$REPO/commits/$BRANCH")"

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
git commit -am "up rev ${SPEC%.*}-${newTag}+${newCommit:0:7}" && \
git push; }
