%global go_import_path	code.google.com/p/codesearch
%global go_source	_build/src/%{go_import_path}
%global rev	24df7a1a1bd03971c9dbc5408723b32527d62b94
%global shortrev	%(r=%{rev}; echo ${r:0:12})
%global snapshot	20131031
# We are using gccgo: stripped binaries are not presently supported.
%global __strip	/bin/true
# For now, the debuginfo macro fails due to no build ID note on golang
# binaries, so disable the debug package.
%global debug_package	%{nil}

Name:	codesearch
Version:	0.%{snapshot}
Release:	1%{?dist}
Summary:	The Google codesearch tool and its libraries.
Group:		Applications/File
License:	BSD
URL:		http://code.google.com/p/codesearch
Source0:	https://codesearch.googlecode.com/archive/%{rev}.tar.gz
BuildRequires:	gcc
BuildRequires:	golang >= 1.2-7
ExclusiveArch:	%{go_arches}

%description
Google code search

%package	-n golang-googlecode-codesearch-devel
Version:	0
Release:	0.4.hg%{shortrev}%{?dist}
Summary:	Go libraries which support the Google codesearch tool
Group:	System Environment/Libraries
Provides:	golang(%{go_import_path}) = %{version}-%{release}
Provides:	golang(%{go_import_path}/index) = %{version}-%{release}
Provides:	golang(%{go_import_path}/regexp) = %{version}-%{release}
Provides:	golang(%{go_import_path}/sparse) = %{version}-%{release}
Requires:	golang
%if 0%{?fedora} >= 19
BuildArch:	noarch
%else
ExclusiveArch:	%{go_arches}
%endif
%description -n golang-googlecode-codesearch-devel
%{summary}

These libraries implement the tokenization of input files
into trigraphs, building a cross-reference index fo trigraghs
and a regular expression matcher that employs the trigraph index.

%prep
%setup -q -n codesearch-%{shortrev}

%build
# Set up temporary build gopath, and put our directory there.
mkdir -p $(dirname %{go_source})
ln -s $(pwd) %{go_source}
export GOPATH=$(pwd)/_build:%{gopath}
for tool in cgrep cindex csearch; do
  go build -o $tool cmd/$tool/${tool}.go
done

%install
install -d %{buildroot}/%{_bindir}
for tool in cgrep cindex csearch; do
  install -p -m755 ./${tool} %{buildroot}/%{_bindir}
done
install -d %{buildroot}/%{gopath}/src/%{go_import_path}
for d in index regexp sparse; do
   cp -avp $d %{buildroot}/%{gopath}/src/%{go_import_path}/
done

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_bindir}/cgrep
%{_bindir}/cindex
%{_bindir}/csearch

%files -n golang-googlecode-codesearch-devel
%defattr(-,root,root,-)
%doc AUTHORS CONTRIBUTORS LICENSE README
%dir %attr(755,root,root) %{gopath}/src/%{go_import_path}
%dir %attr(755,root,root) %{gopath}/src/%{go_import_path}/index
%dir %attr(755,root,root) %{gopath}/src/%{go_import_path}/regexp
%dir %attr(755,root,root) %{gopath}/src/%{go_import_path}/sparse
%{gopath}/src/%{go_import_path}/index/*.go
%{gopath}/src/%{go_import_path}/regexp/*.go
%{gopath}/src/%{go_import_path}/sparse/*.go

%changelog
* Tue Dec 23 2014 Gary Funck <gary@intrepid.com>
- Update spec file to conform to conventions described here:
  http://fedoraproject.org/wiki/PackagingDrafts/Go

* Tue Dec 23 2014 Gary Funck <gary@intrepid.com>
- Update to hg checkout dated 2013-10-31.

* Sun Sep 02 2012 Dennis Kaarsemaker <dennis.kaarsemaker@booking.com> 0.20120502
- Update to a newer hg checkout

* Thu Mar 8 2012 Dennis Kaarsemaker <dennis.kaarsemaker@booking.com> 201202222-r21
- Add more patches from Damian

* Sun Feb 26 2012 Dennis Kaarsemaker <dennis.kaarsemaker@booking.com> 201202222-1
- Initial version, after much swearing at go
