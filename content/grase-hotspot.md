Title: GRASE Hotspot
Date: 2010-12-14 21:55
Author: Tim White
Category: Coding, Technical
Tags: CoovaChilli, FreeRadius, GRASE, GRASE Hotspot, Hotspot
Slug: grase-hotspot

3 years in the making, and finally I am releasing the code for the GRASE
Hotspot. I've always planned on releasing the code, but had a lot things
I wanted done before the code was released, in particular making it easy
to install, and modular, as well as more secure than it previously was
(in particular the remote access).

For those that don't know much about the hotspot system I've been
working on, it's a simple captive portal system, that allows an
organisation/company to provide controlled internet access to users.
When a user tries to use a computer on the network (wireless or wired),
the first time they attempt to access a website, it redirects them to a
login screen. After a sucessful login they can then use the internet
until their time or data allowance is exhausted. The main part of the
GRASE Hotspot is the admin interface I have written. This provides a
simple interface for adding and managing users, as well as monitoring
usage and websites visited.

The rest of the Hotspot system is what we call glue layers. This is the
process of connecting individual components together, in this case,
CoovaChilli, FreeRadius, MySQL, Squid and a few other components. Most
of the Hotspot solutions I researched required a lot of manual work
gluing the components together. All this hard work is taken care of
using the GRASE Hotspot.

Currently the best way to get started using the system, is to download
the grase-repo deb package from
<http://hotspot.purewhite.id.au/apt/pool/main/g/grase-repo/> which will
setup the apt repository. Then head over to
<http://hotspot.purewhite.id.au/wiki/Documentation/Packages> to get an
idea of some of the other packages that can be installed to get started.
More information will appear over time at the main wiki page.

Some old screenshots (will be updated soon) and support forums are over
at [SourceForge.][]

  [SourceForge.]: http://sf.net/projects/grase/
