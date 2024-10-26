%define repo https://github.com/savedra1/clipse
%global debug_package %{nil}

Name:           clipse
Version:        1.0.9
Release:        1%{?dist}
Summary:        A configurable, TUI-based clipboard manager application written in Go

License:        MIT
URL:            %{repo}
Source0:        %{repo}/archive/refs/tags/v%{version}.tar.gz

BuildRequires:  golang git
Requires:	golang

%description
A configurable, TUI-based clipboard manager application written in Go

%prep
%setup -q

%build
go mod tidy
go build -ldflags="-linkmode=external" -o %{name}

%install
# move the built binary to the user accessible binary store
mkdir -p %{buildroot}/%{_bindir}
install -m 0755 %{name} %{buildroot}%{_bindir}/%{name}

%files
%license LICENSE
%{_bindir}/%{name}

%changelog
%autochangelog
