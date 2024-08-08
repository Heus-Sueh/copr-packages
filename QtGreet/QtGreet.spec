# Macros
%global github_url https://github.com
%global github_tags /archive/refs/tags/%{version}
%global gitlab_url https://gitlab.com
%global gitlab_tags /-/archive/v%{version}/%{name}-v%{version}.tar.gz
#=================================================================================#
Name: QtGreet
Version: 2.0.2
Release: 1%{?dist}
Summary: Qt based greeter for greetd, to be run under wayfire or similar wlr-based compositors.
License: GPLv3
URL: %{gitlab_url}/marcusbritanicus/QtGreet
Source: %url/%{gitlab_tags}

BuildRequires:  cmake
BuildRequires:  extra-cmake-modules
BuildRequires:  gcc-c++

BuildRequires:  cmake(Qt5Core)
BuildRequires:  cmake(Qt5DBus)
BuildRequires:  cmake(Qt5Gui)
BuildRequires:  cmake(Qt5Widgets)
BuildRequires:  cmake(Qt5WaylandClient)
BuildRequires:  pkgconfig(json-c)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  qt5-qtbase-private-devel

Requires:       greetd >= 0.6
Provides:       greetd-greeter = 0.6
Provides:       greetd-%{name} = %{version}-%{release}

%description
%{summary}.


%prep
%autosetup -n QtGreet-v%{version}-%{commit}


%build
%cmake
%cmake_build


%install
%cmake_install

install -D -m 0644 -pv -t %{buildroot}%{_sysconfdir}/%{name} \
    configs/config.ini configs/wayfire.ini
install -D -m 0644 -pv -t %{buildroot}%{_datadir}/%{name}/backgrounds \
    backgrounds/*


%check
%ctest


%files
%license LICENSE 
%doc README.md
%dir %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/config.ini
%config(noreplace) %{_sysconfdir}/%{name}/wayfire.ini
%{_bindir}/%{name}
%{_datadir}/%{name}


%changelog
%autochangelog
