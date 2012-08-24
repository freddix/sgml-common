Summary:	Common SGML catalog and DTD files
Name:		sgml-common
Version:	0.6.3
Release:	13
License:	distributable
##Copyright:	(C) International Organization for Standardization 1986
URL:		http://www.iso.ch/cate/3524030.html
Group:		Applications/Publishing/SGML
Source0:	ftp://ftp.kde.org/pub/kde/devel/docbook/SOURCES/%{name}-%{version}.tgz
# Source0-md5:	103c9828f24820df86e55e7862e28974
Patch0:		%{name}-chmod.patch
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libxml2-progs
Requires(pre,preun): /usr/bin/xmlcatalog
Requires:	coreutils
Requires:	grep
Requires:	libxml2-progs
Requires:	sed
Provides:	iso-entities
Provides:	iso-entities-8879.1986
Provides:	sgml-catalog
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		xml_catalog %{_datadir}/sgml/xml-iso-entities-8879.1986/catalog.xml

%description
sgml-common is a collection of entities and dtds that are useful for
SGML processing, but shouldn't need to be included in multiple
packages. It also includes an up-to-date Open Catalog file.

%prep
%setup -q
%patch0 -p1

%build
%{__autoconf}
%configure

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# directory commonly used by docbook-* packages
# and the second used by {,x}html-dtd* ones
install -d $RPM_BUILD_ROOT%{_datadir}/sgml/{docbook,html}

xmlcatalog --noout --create $RPM_BUILD_ROOT%{xml_catalog}
grep PUBLIC $RPM_BUILD_ROOT%{_datadir}/sgml/xml-iso-entities-8879.1986/catalog|sed 's/^/xmlcatalog --noout --add /;s/PUBLIC/public/;s=$= '$RPM_BUILD_ROOT'%{xml_catalog}=' |sh

rm -rf $RPM_BUILD_ROOT%{_prefix}/doc

%clean
rm -rf $RPM_BUILD_ROOT

%triggerpostun -- sgml-common < 0.5-9
if ! grep -qs /etc/sgml/sgml-iso-entities-8879.1986.cat /etc/sgml/catalog ; then
	/usr/bin/install-catalog --add /etc/sgml/sgml-iso-entities-8879.1986.cat /usr/share/sgml/sgml-iso-entities-8879.1986/catalog > /dev/null
fi

%post
if ! grep -qs /etc/sgml/sgml-iso-entities-8879.1986.cat /etc/sgml/catalog ; then
	/usr/bin/install-catalog --add /etc/sgml/sgml-iso-entities-8879.1986.cat /usr/share/sgml/sgml-iso-entities-8879.1986/catalog > /dev/null
fi
if ! grep -qs /etc/sgml/xml-iso-entities-8879.1986.cat /etc/sgml/catalog ; then
	/usr/bin/install-catalog --add /etc/sgml/xml-iso-entities-8879.1986.cat /usr/share/sgml/xml-iso-entities-8879.1986/catalog > /dev/null
fi
if ! grep -qs %{xml_catalog} /etc/xml/catalog ; then
	/usr/bin/xmlcatalog --noout --add nextCatalog "" %{xml_catalog} /etc/xml/catalog
fi

%preun
if [ "$1" = "0" ] ; then
	/usr/bin/install-catalog --remove /etc/sgml/sgml-iso-entities-8879.1986.cat /usr/share/sgml/sgml-iso-entities-8879.1986/catalog > /dev/null
	/usr/bin/install-catalog --remove /etc/sgml/xml-iso-entities-8879.1986.cat /usr/share/sgml/xml-iso-entities-8879.1986/catalog > /dev/null
	/usr/bin/xmlcatalog --noout --del %{xml_catalog} /etc/xml/catalog
fi

%files
%defattr(644,root,root,755)
%doc doc/HTML/*
%dir %{_sysconfdir}/sgml
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/sgml/sgml.conf
%attr(755,root,root) %{_bindir}/*
%dir %{_datadir}/sgml
%dir %{_datadir}/sgml/docbook
%dir %{_datadir}/sgml/html
%{_datadir}/sgml/sgml-iso-entities-8879.1986
%{_datadir}/sgml/xml-iso-entities-8879.1986
%{_datadir}/sgml/xml.dcl
%{_mandir}/*/*

