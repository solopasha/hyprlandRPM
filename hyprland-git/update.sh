#!/usr/bin/bash
set -euxo pipefail

ec=0
newRelease=0
curl_opts=(--connect-timeout 10 --retry 7 --retry-connrefused -Ss -X POST)

oldTag="$(rpmspec -q --qf "%{version}\n" hyprland-git.spec | head -1 | sed 's/\^.*//')"
newTag="$(curl "https://api.github.com/repos/hyprwm/Hyprland/tags" | jq -r '.[0].name' | sed 's/^v//')"

oldHyprlandCommit="$(sed -n 's/.*hyprland_commit \(.*\)/\1/p' hyprland-git.spec)"
newHyprlandCommit="$(curl -s -H "Accept: application/vnd.github.VERSION.sha" "https://api.github.com/repos/hyprwm/Hyprland/commits/main")"

oldCommitsCount="$(sed -n 's/.*commits_count \(.*\)/\1/p' hyprland-git.spec)"
newCommitsCount="$(curl -I -k \
                "https://api.github.com/repos/hyprwm/Hyprland/commits?per_page=1&sha=$newHyprlandCommit" | \
                sed -n '/^[Ll]ink:/ s/.*"next".*page=\([0-9]*\).*"last".*/\1/p')"

oldCommitDate="$(sed -n 's/.*commit_date \(.*\)/\1/p' hyprland-git.spec)"
newCommitDate="$(env TZ=Etc/GMT+12 date -d "$(curl -s "https://api.github.com/repos/hyprwm/Hyprland/commits?per_page=1&ref=$newHyprlandCommit" | \
                jq -r '.[].commit.author.date')" +"%a %b %d %T %Y")"

oldProtocolsCommit="$(sed -n 's/.*protocols_commit \(.*\)/\1/p' hyprland-git.spec)"
newProtocolsCommit="$(curl -L \
            -H "Accept: application/vnd.github+json" \
            -H "X-GitHub-Api-Version: 2022-11-28" \
            "https://api.github.com/repos/hyprwm/Hyprland/contents/subprojects/hyprland-protocols?ref=$newHyprlandCommit" | jq -r '.sha')"

oldUdis86Commit="$(sed -n 's/.*udis86_commit \(.*\)/\1/p' hyprland-git.spec)"
newUdis86Commit="$(curl -L \
            -H "Accept: application/vnd.github+json" \
            -H "X-GitHub-Api-Version: 2022-11-28" \
            "https://api.github.com/repos/hyprwm/Hyprland/contents/subprojects/udis86?ref=$newHyprlandCommit" | jq -r '.sha')"

sed -e "s/$oldHyprlandCommit/$newHyprlandCommit/" \
    -e "/%global commits_count/s/$oldCommitsCount/$newCommitsCount/" \
    -e "s/$oldCommitDate/$newCommitDate/" \
    -e "s/$oldProtocolsCommit/$newProtocolsCommit/" \
    -e "s/$oldUdis86Commit/$newUdis86Commit/" \
    -i hyprland-git.spec

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
pushd ../hyprland-plugins && \
bash plugins_update.sh;
popd && \
git commit -am "up rev hyprland-git-${newTag}+${newHyprlandCommit:0:7}" && \
git push && \
hyprlandGitBuildId=$(curl "${curl_opts[@]}" "https://copr.fedorainfracloud.org/webhooks/custom/77569/${COPR_WEBHOOK}/hyprland-git") && \
copr watch-build "${hyprlandGitBuildId}" && \
curl "${curl_opts[@]}" "https://copr.fedorainfracloud.org/webhooks/custom/77569/${COPR_WEBHOOK}/hyprland-plugins-git"; }

if [[ $newRelease == "1" ]]; then
    hyprlandBuildId=$(curl "${curl_opts[@]}" "https://copr.fedorainfracloud.org/webhooks/custom/77569/${COPR_WEBHOOK}/hyprland")
    copr watch-build "${hyprlandBuildId}"
    curl "${curl_opts[@]}" "https://copr.fedorainfracloud.org/webhooks/custom/77569/${COPR_WEBHOOK}/hyprland-plugins"
    git branch "$newTag"
    git push origin "$newTag"
fi
