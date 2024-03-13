#!/usr/bin/bash
set -euxo pipefail

ec=0

SPEC=aylurs-gtk-shell-git.spec
REPO=Aylur/ags
BRANCH=main

oldTag="$(rpmspec -q --qf "%{version}\n" --srpm $SPEC | sed 's/[\^,~].*//')"
newTag="$(curl "https://api.github.com/repos/$REPO/tags" | jq -r '.[0].name' | sed 's/^v//')"

oldCommit="$(sed -n 's/.*\bags_commit\b \(.*\)/\1/p' $SPEC)"
newCommit="$(curl -s -H "Accept: application/vnd.github.VERSION.sha" "https://api.github.com/repos/$REPO/commits/$BRANCH")"

oldGvcCommit="$(sed -n 's/.*gvc_commit \(.*\)/\1/p' $SPEC)"
newGvcCommit="$(curl -L \
            -H "Accept: application/vnd.github+json" \
            -H "X-GitHub-Api-Version: 2022-11-28" \
            "https://api.github.com/repos/$REPO/contents/subprojects/gvc" | jq -r '.sha')"

sed -e "s/$oldCommit/$newCommit/" \
    -e "s/$oldGvcCommit/$newGvcCommit/" \
    -i $SPEC

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
git push && \
copr-cli build-package solopasha/hyprland --name ${SPEC%.*} --nowait --enable-net on; }
