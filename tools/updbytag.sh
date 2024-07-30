#!/usr/bin/env bash
set -euxo pipefail

NAME=waybar
SPEC=${NAME}-git.spec
REPO="Alexays/Waybar"
GIT_URL="https://api.github.com/repos/${REPO}"

# Obter a versão antiga do .spec
oldTag="$(rpmspec -q --qf "%{version}\n" ${SPEC} | head -1 | sed 's/\^.*//')"

# Obter a nova versão da última tag no repositório
newTag="$(curl -s ${GIT_URL}/tags | jq -r '.[0].name' | sed 's/^v//')"

# Atualizar a versão no .spec se necessário
if rpmdev-vercmp "${oldTag}" "${newTag}"; then
	: # No change needed
elif [ $? -eq 12 ]; then
	perl -pe 's/(?<=bumpver\s)(\d+)/0/' -i ${SPEC}
	sed -i "/^Version:/s/${oldTag}/${newTag}/" ${SPEC}
else
	exit 1
fi

# Verificar se há diferenças e, se houver, atualizar o commit
if ! git diff --quiet; then
	perl -pe 's/(?<=bumpver\s)(\d+)/$1 + 1/ge' -i ${SPEC}
	git commit -am "up rev ${NAME}-git-${newTag}"
	git push
fi
