Name:           matugen
Version:        2.4.0
Release:        %autorelease
Summary:        Material you color generation tool with templates

License:        GPL-2.0
URL:            https://github.com/InioX/matugen
Source:         %{url}/releases/download/v%{version}/%{name}-%{version}-x86_64.tar.gz

%global _description %{expand:
%{summary}.}

%define _debugsource_template %{nil}

%description %{_description}

%prep
%autosetup -c

%build

%install
mkdir -p %{buildroot}%{_bindir}
install -Dpm755 %{name} %{buildroot}/%{_bindir}/%{name}

%files
%license LICENSE
%{_bindir}/%{name}

%changelog
%autochangelog
