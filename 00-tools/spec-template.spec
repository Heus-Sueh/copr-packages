# Macros
%global github_url https://github.com
%global github_tags /archive/refs/tags/%{version}
%global gitlab_url https://gitlab.com
%global gitlab_tags /-/archive/v%{version}/%{name}-v%{version}.tar.gz
#==================================================================================#
Name:           
Version:        
Release:        1
Summary:        
License:        GPL-3.0
URL:            %{github_url}/
Source:         %{url}/%{github_tags}.tar.gz

BuildRequires:  
Requires:

%global _description %{expand:
%{summary}.}

%description %{_description}

%prep

%build

%install
install -Dpm0755 target %{buildroot}/%{_bindir}/

%files
%{_bindir}/
%{_mandir}/
%license LICENSE

%changelog
%autochangelog
