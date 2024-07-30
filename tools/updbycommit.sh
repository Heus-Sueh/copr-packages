#!/usr/bin/env bash
set -euxo pipefail

NAME=waybar
SPEC=${NAME}-git.spec
REPO="Alexays/Waybar"
GIT_URL="https://api.github.com/repos/${REPO}"
BRANCH=master

oldTag="$(rpmspec -q --qf "%{version}\n" ${SPEC} | head -1 | sed 's/\^.*//')"
newTag="$(curl -s ${GIT_URL}/tags | jq -r '.[0].name' | sed 's/^v//')"
oldCommit="$(sed -n 's/.*\bcommit0\b \(.*\)/\1/p' ${SPEC})"
newCommit="$(curl -s -H "Accept: application/vnd.github.VERSION.sha" ${GIT_URL}/commits/${BRANCH})"

sed -i "s/${oldCommit}/${newCommit}/" ${SPEC}

if rpmdev-vercmp "${oldTag}" "${newTag}"; then
	: # No change needed
elif [ $? -eq 12 ]; then
	perl -pe 's/(?<=bumpver\s)(\d+)/0/' -i ${SPEC}
	sed -i "/^Version:/s/${oldTag}/${newTag}/" ${SPEC}
else
	exit 1
fi

if ! git diff --quiet; then
	perl -pe 's/(?<=bumpver\s)(\d+)/$1 + 1/ge' -i ${SPEC}
	git commit -am "up rev ${NAME}-git-${newTag}+${newCommit:0:7}"
	git push
fi
