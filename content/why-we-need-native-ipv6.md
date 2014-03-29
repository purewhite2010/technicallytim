Title: Why we need native IPv6
Date: 2011-06-10 12:12
Author: Tim White
Category: Blog, Technical
Tags: ipv6, ping, sixxs
Slug: why-we-need-native-ipv6

We need native IPv6, or at least a decent PoP in Australia!

Currently our home network is IPv6 enabled via a Sixxs tunnel. If we
lived in NZ then our PoP would be in NZ. Unfortunately we can't use the
NZ PoP, so instead we use the London PoP! Eventually I'll get around to
pinging every PoP available to us and find the "closest" one, but for
now, letter the numbers do the talking.

I ping the same machine both via IPv6 and via IPv4. Lets see if you can
work out which is which.

    10 packets transmitted, 10 received, 0% packet loss
    rtt min/avg/max/mdev = 698.592/712.159/814.473/34.163 ms

    10 packets transmitted, 10 received, 0% packet loss
    rtt min/avg/max/mdev = 76.670/79.557/87.452/2.866 ms

The PoP has an average ping of 350ms just to get to the PoP! No wonder
it takes so long to get to the PoP and back to Australia! Hopefully
later in the year my hosting provider will have fixed the IPv6 transport
and I can setup my own local tunnel. Until then, slow IPv6 :(

<ins datetime="2011-06-10T02:48:46+00:00">Edit: So I finally got AARNet
IPv6 tunnel broker service working. A much better improvement. I'm
running both tunnels in parrallel so that if one dies the other is
working. Hopefully I'll see better IPv6 improvement now. Still, native
IPv6 would be better.
<http://michael-wheeler.org/2009/03/24/australian-ipv6-tunnel-broker/></ins>

    10 packets transmitted, 10 received, 0% packet loss
    rtt min/avg/max/mdev = 235.587/267.187/382.010/45.090 ms
