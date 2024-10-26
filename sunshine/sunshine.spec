%global build_timestamp %(date +"%Y%m%d")
%undefine _hardened_build

Name:           sunshine
Version:        2024.911.215654
Summary:        Sunshine is a self-hosted game stream host for Moonlight.
Release:        1%{?dist}
License:        GPLv3+
URL:            https://github.com/LizardByte/Sunshine
Source0:        sunshine.sysusers
Source1:        Linux-x86_64.tar.gz

Patch0:         legion-go-mod.patch
Patch1:         disable-version-check.patch
Patch2:         no-cmake-dirty-version.patch
Patch3:         update-message.patch

BuildRequires:  boost-devel
BuildRequires:  cmake
BuildRequires:  doxygen
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  libayatana-appindicator3-devel
BuildRequires:  libcap-devel
BuildRequires:  libcurl-devel
BuildRequires:  libdrm-devel
BuildRequires:  libevdev-devel
BuildRequires:  libgudev
BuildRequires:  libnotify-devel
BuildRequires:  libva-devel
BuildRequires:  libvdpau-devel
BuildRequires:  libX11-devel
BuildRequires:  libxcb-devel
BuildRequires:  libXcursor-devel
BuildRequires:  libXfixes-devel
BuildRequires:  libXi-devel
BuildRequires:  libXinerama-devel
BuildRequires:  libXrandr-devel
BuildRequires:  libXtst-devel
BuildRequires:  git
BuildRequires:  graphviz
BuildRequires:  mesa-libGL-devel
BuildRequires:  miniupnpc-devel
BuildRequires:  npm
BuildRequires:  numactl-devel
BuildRequires:  openssl-devel
BuildRequires:  opus-devel
BuildRequires:  pulseaudio-libs-devel
BuildRequires:  python3.11
BuildRequires:  rpm-build
BuildRequires:  systemd-udev
BuildRequires:  systemd-rpm-macros
%{?sysusers_requires_compat}
BuildRequires:  wget
BuildRequires:  which

# Conditional BuildRequires for cuda-gcc based on Fedora version and architecture
%if 0%{?fedora} >= 40 && "%{_target_cpu}" == "x86_64"
BuildRequires:  cuda-gcc-c++
%endif

Requires:  boost >= 1.81.0
Requires:  libcap >= 2.22
Requires:  libcurl >= 7.0
Requires:  libdrm > 2.4.97
Requires:  libevdev >= 1.5.6
Requires:  libopusenc >= 0.2.1
Requires:  libva >= 2.14.0
Requires:  libvdpau >= 1.5
Requires:  libwayland-client >= 1.20.0
Requires:  libX11 >= 1.7.3.1
Requires:  miniupnpc >= 2.2.4
Requires:  numactl-libs >= 2.0.14
Requires:  openssl >= 3.0.2
Requires:  pulseaudio-libs >= 10.0
Requires:  libayatana-appindicator3 >= 0.5.3

%description
Sunshine is a self-hosted game stream host for Moonlight. Offering low latency, cloud gaming server capabilities with support for AMD, Intel, and Nvidia GPUs for hardware encoding. Software encoding is also available. You can connect to Sunshine from any Moonlight client on a variety of devices. A web UI is provided to allow configuration, and client pairing, from your favorite web browser. Pair from the local server or any mobile device.

%prep
git clone --single-branch --branch master https://github.com/LizardByte/Sunshine
cd Sunshine
git fetch --tags
git checkout v%{version}
git submodule update --init --recursive
npm install

# patches
%autopatch -p1

#HACK: ffmpeg needs to be built with up-to-date libs, lets drop in our own built on Fedora for the build to replace the Ubuntu built versions
tar -xzf %{_sourcedir}/Linux-x86_64.tar.gz -C third-party/build-deps/ffmpeg/Linux-x86_64 --strip-components=1

%build
# we need to clear these flags to avoid linkage errors with cuda-gcc-c++
export CFLAGS=""
export CXXFLAGS=""
export FFLAGS=""
export FCFLAGS=""
export LDFLAGS=""

# Detect the architecture and Fedora version
ARCH=$(uname -m)
FEDORA_VERSION=%{fedora}

if [ "$ARCH" == "x86_64" ] && [ "$FEDORA_VERSION" -ge 40 ]; then
    # Set up CUDA environment variables
    export CUDA_VERSION="12.6.0"
    export CUDA_BUILD="560.28.03"
    export CUDA_RUNFILE="cuda_${CUDA_VERSION}_${CUDA_BUILD}_linux.run"
    export CUDA_INSTALL_PATH="%{_builddir}/cuda-$CUDA_VERSION"
    export CUDA_URL="https://developer.download.nvidia.com/compute/cuda/${CUDA_VERSION}/local_installers/${CUDA_RUNFILE}"
    export NVCC_PREPEND_FLAGS='-ccbin /usr/bin/cuda -allow-unsupported-compiler'

    # Install CUDA if not already installed
    if [ ! -d "${CUDA_INSTALL_PATH}" ]; then
        curl -o "./cuda.run" "${CUDA_URL}"
        chmod a+x ./cuda.run
        ./cuda.run --silent --toolkit --override --no-drm --no-man-page --no-opengl-libs --toolkitpath=${CUDA_INSTALL_PATH}
        rm ./cuda.run
    else
        echo "CUDA is already installed at ${CUDA_INSTALL_PATH}, skipping installation."
    fi

    # Update environment variables for CUDA
    export PATH=${CUDA_INSTALL_PATH}/bin:${PATH}
    export LD_LIBRARY_PATH=${CUDA_INSTALL_PATH}/lib64:${LD_LIBRARY_PATH}
    export PATH=/usr/bin/cuda:$PATH

    # Set up the build directory for Sunshine
    mkdir -p %{_builddir}/Sunshine/build
    cd %{_builddir}/Sunshine/build

    # Configure cmake to use CUDA
    cmake .. \
        -DCMAKE_BUILD_TYPE=Release \
        -DTESTS_ENABLE_PYTHON_TESTS=OFF \
        -DCMAKE_INTERPROCEDURAL_OPTIMIZATION=OFF \
        -DCMAKE_POSITION_INDEPENDENT_CODE=OFF \
        -DCMAKE_INSTALL_PREFIX=%{_prefix} \
        -DBUILD_DOCS=OFF \
        -DSUNSHINE_ENABLE_CUDA=ON \
        -DCMAKE_CUDA_COMPILER=${CUDA_INSTALL_PATH}/bin/nvcc \
        -DSUNSHINE_ASSETS_DIR=%{_datadir}/sunshine \
        -DSUNSHINE_EXECUTABLE_PATH=%{_bindir}/sunshine \
        -DSUNSHINE_ENABLE_WAYLAND=ON \
        -DSUNSHINE_ENABLE_X11=ON \
        -DSUNSHINE_ENABLE_DRM=ON
    %make_build

else
    # Set up the build directory for Sunshine
    mkdir -p %{_builddir}/Sunshine/build
    cd %{_builddir}/Sunshine/build

    # Configure cmake without CUDA
    cmake .. \
        -DCMAKE_BUILD_TYPE=Release \
        -DTESTS_ENABLE_PYTHON_TESTS=OFF \
        -DCMAKE_INTERPROCEDURAL_OPTIMIZATION=OFF \
        -DCMAKE_POSITION_INDEPENDENT_CODE=OFF \
        -DCMAKE_INSTALL_PREFIX=%{_prefix} \
        -DBUILD_DOCS=OFF \
        -DSUNSHINE_ENABLE_CUDA=OFF \
        -DSUNSHINE_ASSETS_DIR=%{_datadir}/sunshine \
        -DSUNSHINE_EXECUTABLE_PATH=%{_bindir}/sunshine \
        -DSUNSHINE_ENABLE_WAYLAND=ON \
        -DSUNSHINE_ENABLE_X11=ON \
        -DSUNSHINE_ENABLE_DRM=ON
    %make_build
fi

%install
install -p -D -m 0644 %{SOURCE0} %{buildroot}%{_sysusersdir}/sunshine.conf
cd %{_builddir}/Sunshine/build
%make_install

# Add modules-load configuration
install -D -m 0644 /dev/stdin %{buildroot}/usr/lib/modules-load.d/uhid.conf <<EOF
uhid
EOF

%pre
%sysusers_create_compat %{SOURCE0}

%post
# Ensure Sunshine can grab images from KMS
path_to_setcap=$(which setcap)
if [ -x "$path_to_setcap" ] ; then
  echo "$path_to_setcap cap_sys_admin+p /usr/bin/sunshine"
	$path_to_setcap cap_sys_admin+p $(readlink -f /usr/bin/sunshine)
fi

%preun
# Remove udev rule
rm -f %{_udevrulesdir}/99-uhid.rules

# Remove modules-load configuration
rm -f /usr/lib/modules-load.d/uhid.conf

%files
# Executables
%{_bindir}/sunshine
%{_bindir}/sunshine-*

# Systemd unit file for user services
%{_userunitdir}/sunshine.service

# Udev rules
%{_udevrulesdir}/60-sunshine.rules

# Modules-load configuration
%{_modulesloaddir}/uhid.conf

# Desktop entries
%{_datadir}/applications/sunshine.desktop
%{_datadir}/applications/sunshine_terminal.desktop

# Icons
%{_datadir}/icons/hicolor/scalable/apps/sunshine.svg
%{_datadir}/icons/hicolor/scalable/status/sunshine-locked.svg
%{_datadir}/icons/hicolor/scalable/status/sunshine-pausing.svg
%{_datadir}/icons/hicolor/scalable/status/sunshine-playing.svg
%{_datadir}/icons/hicolor/scalable/status/sunshine-tray.svg

# Metainfo
%{_datadir}/metainfo/sunshine.appdata.xml

# Main application assets and shaders
%{_datadir}/sunshine/apps.json
%{_datadir}/sunshine/box.png
%{_datadir}/sunshine/desktop-alt.png
%{_datadir}/sunshine/desktop.png
%{_datadir}/sunshine/steam.png
%dir %{_datadir}/sunshine/shaders
%dir %{_datadir}/sunshine/shaders/opengl
%{_datadir}/sunshine/shaders/opengl/*

# Web assets
%{_datadir}/sunshine/web/apps.html
%{_datadir}/sunshine/web/config.html
%{_datadir}/sunshine/web/index.html
%{_datadir}/sunshine/web/password.html
%{_datadir}/sunshine/web/pin.html
%{_datadir}/sunshine/web/troubleshooting.html
%{_datadir}/sunshine/web/welcome.html
%{_datadir}/sunshine/web/assets/*
%{_datadir}/sunshine/web/images/*
%{_sysusersdir}/sunshine.conf

%changelog
