%define booking_repo base

Name:		codesearch
Version:	0.20120502
Release:	1%{?dist}
Summary:	Set of tools to aid developers in indexing and searching source code.

Group:		System Environment/Libraries
License:	BSD
URL:		http://code.google.com/p/codesearch
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

Source0:	%{name}-%{version}.tar.gz

BuildRequires:	go

%description
Google code search

%prep
%setup -n %{name}-%{version}

%build
%ifarch %ix86
	%global GOARCH 386
%endif
%ifarch	x86_64
	%global GOARCH amd64
%endif

GOROOT="%{_libdir}/go"
GOPATH=$GOROOT:$(pwd)
GOOS=linux
GOBIN="$GOROOT/bin"
GOARCH="%{GOARCH}"
export GOROOT GOBIN GOARCH GOOS GOPATH
sed -e 's@code.google.com/p/@@' -i index/write.go cmd/cindex/cindex.go cmd/cgrep/cgrep.go cmd/csearch/csearch.go regexp/match.go
mkdir -p src/codesearch
ln -s ../../index src/codesearch/
ln -s ../../regexp src/codesearch/
ln -s ../../sparse src/codesearch/
ln -s $(pwd)/cmd/cgrep %{_libdir}/go/src/cmd/cgrep
ln -s $(pwd)/cmd/cgrep %{_libdir}/go/src/cmd/cindex
ln -s $(pwd)/cmd/cgrep %{_libdir}/go/src/cmd/csearch

go install codesearch/sparse
go install codesearch/regexp
go install codesearch/index

go install cmd/cgrep
go install cmd/cindex
go install cmd/csearch

%install
mkdir -p $RPM_BUILD_ROOT/%{_bindir}
install -m755 %{_libdir}/go/bin/cgrep $RPM_BUILD_ROOT/%{_bindir}
install -m755 %{_libdir}/go/bin/cindex $RPM_BUILD_ROOT/%{_bindir}
install -m755 %{_libdir}/go/bin/csearch $RPM_BUILD_ROOT/%{_bindir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc
%{_bindir}/cgrep
%{_bindir}/cindex
%{_bindir}/csearch

%changelog
* Sun Sep 02 2012 Dennis Kaarsemaker <dennis.kaarsemaker@booking.com> 0.20120502
- Update to a newer hg checkout

* Thu Mar 8 2012 Dennis Kaarsemaker <dennis.kaarsemaker@booking.com> 201202222-r21
- Add more patches from Damian

* Sun Feb 26 2012 Dennis Kaarsemaker <dennis.kaarsemaker@booking.com> 201202222-1
- Initial version, after much swearing at go
