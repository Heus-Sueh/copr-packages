#!/usr/bin/env bash
set -euox pipefail

NAME=example
SPEC=${NAME}.spec
REPO="user/project"
GIT_URL="https://api.github.com/repos/${REPO}"
BRANCH=master

# Get the old version from the .spec file
oldTag="$(rpmspec -q --qf "%{version}\n" ${SPEC} | head -1 | sed 's/\^.*//')"

# Get the new version from the latest tag in the repository
newTag="$(curl -s ${GIT_URL}/tags | jq -r '.[0].name' | sed 's/^v//')"

# Update the version in the .spec file if necessary
if rpmdev-vercmp "${oldTag}" "${newTag}"; then
	: # No change needed
elif [ $? -eq 12 ]; then
	# Increment version in the spec file
	perl -pe 's/(?<=bumpver\s)(\d+)/0/' -i ${SPEC}
	sed -i "/^Version:/s/${oldTag}/${newTag}/" ${SPEC}
else
	exit 1
fi

# Check for differences and update the commit if there are any
if ! git diff --quiet; then
	# Increment the version in the spec file
	perl -pe 's/(?<=bumpver\s)(\d+)/$1 + 1/ge' -i ${SPEC}
	git commit -am "up rev ${NAME}-git-${newTag}"
	git push
fi
