Name:           apx
Version:        2.4.3
Release:        1%{?dist}
Summary:        Package manager with support for multiple sources
License:        GPL-3.0-only
URL:            https://github.com/Vanilla-OS/apx
Source0:        %{name}-%{version}.tar.gz::%{url}/archive/refs/tags/v%{version}.tar.gz

BuildRequires:  go
Requires:       distrobox
Requires:       glibc

%description
apx is a package manager with support for multiple sources.

%prep
%setup -q
mkdir -p build/
sed -i 's|share/apx|bin|' config/apx.json
sed -i 's|bin/distrobox|bin|' config/apx.json

%build
go build -o build \
  -ldflags "-s -w -linkmode=external -X main.Version=v%{version} -extldflags \"$LDFLAGS\""

for shell in bash fish zsh; do
  ./build/apx completion $shell >build/%{name}.$shell
done

%check
[[ "$(./build/apx --version)" == "apx version v%{version}" ]]

%install
install -Dm755 build/%{name} %{buildroot}/%{_bindir}/%{name}
install -Dm644 config/apx.json %{buildroot}/%{_sysconfdir}/apx/apx.json
install -Dm644 man/man1/apx.1 %{buildroot}/%{_mandir}/man1/apx.1
install -Dm644 build/%{name}.bash %{buildroot}/%{_datadir}/bash-completion/completions/%{name}
install -Dm644 build/%{name}.fish %{buildroot}/%{_datadir}/fish/vendor_completions.d/%{name}.fish
install -Dm644 build/%{name}.zsh %{buildroot}/%{_datadir}/zsh/site-functions/_%{name}

%files
%{_bindir}/%{name}
%{_sysconfdir}/apx/apx.json
%{_mandir}/man1/apx.1*
%{_datadir}/bash-completion/completions/%{name}
%{_datadir}/fish/vendor_completions.d/%{name}.fish
%{_datadir}/zsh/site-functions/_%{name}

%changelog
