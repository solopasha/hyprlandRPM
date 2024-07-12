#!/usr/bin/bash
set -euxo pipefail

ec=0
newRelease=0

SPEC=hyprland-aquamarine-git.spec
REPO=hyprwm/Hyprland

oldTag="$(rpmspec -q --qf "%{version}\n" $SPEC | head -1 | sed 's/\^.*//')"
newTag="$(curl "https://api.github.com/repos/$REPO/tags" | jq -r '.[0].name' | sed 's/^v//')"

oldHyprlandCommit="$(sed -n 's/.*hyprland_commit \(.*\)/\1/p' $SPEC)"
newHyprlandCommit="$(curl -s "https://api.github.com/repos/$REPO/git/refs/pull/6608/head" | jq -r '.object.sha')"

oldCommitsCount="$(sed -n 's/.*commits_count \(.*\)/\1/p' $SPEC)"
newCommitsCount="$(curl -I -k \
                "https://api.github.com/repos/$REPO/commits?per_page=1&sha=$newHyprlandCommit" | \
                sed -n '/^[Ll]ink:/ s/.*"next".*page=\([0-9]*\).*"last".*/\1/p')"

oldCommitDate="$(sed -n 's/.*commit_date \(.*\)/\1/p' $SPEC)"
newCommitDate="$(env TZ=Etc/GMT+12 date -d "$(curl -s "https://api.github.com/repos/$REPO/commits?per_page=1&ref=$newHyprlandCommit" | \
                jq -r '.[].commit.author.date')" +"%a %b %d %T %Y")"

oldProtocolsCommit="$(sed -n 's/.*protocols_commit \(.*\)/\1/p' $SPEC)"
newProtocolsCommit="$(curl -L \
            -H "Accept: application/vnd.github+json" \
            -H "X-GitHub-Api-Version: 2022-11-28" \
            "https://api.github.com/repos/$REPO/contents/subprojects/hyprland-protocols?ref=$newHyprlandCommit" | jq -r '.sha')"

oldUdis86Commit="$(sed -n 's/.*udis86_commit \(.*\)/\1/p' $SPEC)"
newUdis86Commit="$(curl -L \
            -H "Accept: application/vnd.github+json" \
            -H "X-GitHub-Api-Version: 2022-11-28" \
            "https://api.github.com/repos/$REPO/contents/subprojects/udis86?ref=$newHyprlandCommit" | jq -r '.sha')"

sed -e "s/$oldHyprlandCommit/$newHyprlandCommit/" \
    -e "/%global commits_count/s/$oldCommitsCount/$newCommitsCount/" \
    -e "s/$oldCommitDate/$newCommitDate/" \
    -e "s/$oldProtocolsCommit/$newProtocolsCommit/" \
    -e "s/$oldUdis86Commit/$newUdis86Commit/" \
    -i $SPEC

# rpmdev-vercmp $oldTag $newTag || ec=$?
# case $ec in
#     0) ;;
#     12)
#         perl -pe 's/(?<=bumpver\s)(\d+)/0/' -i $SPEC
#         sed -i "/^Version:/s/$oldTag/$newTag/" $SPEC
#         newRelease=1 ;;
#     *) exit 1
# esac

git diff --quiet || \
{ perl -pe 's/(?<=bumpver\s)(\d+)/$1 + 1/ge' -i $SPEC && \
git commit -am "up rev ${SPEC%.*}-${newHyprlandCommit:0:7}" && \
git push; }
