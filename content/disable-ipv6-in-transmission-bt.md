Title: Disable IPv6 in Transmission BT
Date: 2011-06-10 15:59
Author: tim
Category: Blog, Technical
Tags: ipv6, torrent, transmission, tunnel
Slug: disable-ipv6-in-transmission-bt

After finally getting my IPv6 working nicely, it was time to prevent
Transmission from using IPv6 as  I don't want lots of torrent traffic
going through the tunnel when it's faster through IPv4 (until a time I
can get Native IPv6). Apparently this is an "invalid" feature request
according to some of the developers.
(<http://trac.transmissionbt.com/ticket/4197>)

Had the developer actually stopped to consider it, maybe read some
relevant parts of the source code, they would have quickly discovered
that you can already disable it! They could document it as a feature
without having to touch a line of code, and mark the feature request as
completed!

It's a rather simple fix. There are checks for the IPv6 address not
being a link local address, or a 6to4, or Teredo tunnel[1]. So we just
make Transmission bind to a link local address and hey presto, no IPv6
for Transmission!

Simply add the following line to the settings.json file.

    "bind-address-ipv6": "fe80::"

 

[1] You'd think given that they already prevent Teredo tunnels from
being used, that the feature request would actually make sense for those
wishing to disable IPv6 due to TUNNEL's!
