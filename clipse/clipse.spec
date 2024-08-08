Name:           clipse
Version:        1.9.0
Release:        %autorelease
Summary:        Configurable TUI clipboard manager for Unix 

License:        GPL-2.0
URL:            https://github.com/savedra1/clipse
Source:         %{url}/releases/download/v%{version}/%{name}-%{version}-amd64.tar.gz

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
%changelog CHANGELOG
%{_bindir}/%{name}

%changelog
%autochangelog
