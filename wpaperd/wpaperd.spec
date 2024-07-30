Name:           wpaperd
Version:        1.0.1
Release:        1
Summary:        Wallpaper daemon for Wayland

License:        GPL-3.0
URL:            https://github.com/danyspin97/wpaperd
Source0:        %{url}/archive/refs/tags/%{version}.tar.gz

BuildRequires:  cargo
BuildRequires:  scdoc
BuildRequires:  git
BuildRequires:  wayland-devel
BuildRequires:  libwayland-client 
BuildRequires:  libwayland-egl
BuildRequires:  egl-wayland-devel
BuildRequires:  egl-wayland
BuildRequires:  mesa-libEGL-devel
Requires:       wayland
Requires:       mesa

%global _description %{expand:
Wallpaper daemon for Wayland.}

%description %{_description}

%prep
%autosetup -Sgit

%build
export RUSTUP_TOOLCHAIN=stable
export CARGO_TARGET_DIR=target
cargo build --release
scdoc <man/wpaperd-output.5.scd >target/release/wpaperd-output.5

%install
install -Dpm0755 target/release/wpaperd %{buildroot}/%{_bindir}/wpaperd
install -Dpm0755 target/release/wpaperctl %{buildroot}/%{_bindir}/wpaperctl
install -Dpm0644 target/release/wpaperd-output.5 %{buildroot}/%{_mandir}/man5/wpaperd-output.5

%files
%{_bindir}/wpaperd
%{_bindir}/wpaperctl
%{_mandir}/man5/wpaperd-output.5.gz

%changelog
%autochangelog
