Title: Belkin? Rtkit?
Date: 2011-11-05 12:10
Author: tim
Category: Blog, Technical
Tags: backwards ip, belkin, reverse ip, rtkit
Slug: belkin-rtkit

While attempting to remotely debug a linux machine today, I was first
encountering a strange problem. Any process that took more than about
1/2 second to complete, would freeze. top, ps, lsmod, tail -f, the list
goes on. For example, trying to run dmesg and display it's output would
freeze, but dmesg into a file, and it would complete!

After much digging, I eventually found that rtkit (rtkit-daemon) is
constantly trying to make pulseaudio operate at realtime. In reality, we
don't need our audio to operate in realtime as most modern computers can
keep up with video playback just fine. For the few people we actually
want near real time audio (say, people recording multitrack stuff), then
they can enable it themselves. Disabling rtkit (actually, uninstalling
it as it appears to be started in dbus stuff), seems to have solved that
problem.

The next problem was a strange DNS response. A dns request through the
Belkin modem, to this server (purewhite.id.au) would return 10.45.41.175
instead of 175.41.45.10. I know what reverse DNS is, but this is reverse
IP! Belkin is returning the ip in reverse!! (Or backwards if you
desire). A quick check reveals that this relatively new modem, hasn't
got any new firmware for it (and it's firmware is over 1 year old).
Apparently, someone else had this problem and belkin told them to just
hard code the ip's in your hosts file for the hosts that are being
returned wrong! I believe it was also a Belkin modem that would return
strange results when you did an AAAA request (ipv6).  
So if you have a Belkin, maybe force your computer to use your ISP's
DNS servers directly, rather than the routers. (Or take it back to the
shop, because after all, it is faulty)
