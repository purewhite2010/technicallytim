Title: Munin cgi graph timing out
Date: 2011-09-01 11:50
Author: Tim White
Category: Blog, Technical
Tags: ipcrm, ipcs, munin, munin-cgi-graph, semaphore, timeout
Slug: munin-cgi-graph-timing-out

A problem that has given lots of people problems, caused me issues
yesterday. I have munin using munin-cgi-graph to create the graphs on
demand due to me not often viewing the graphs. A few days ago I had a
server issue that caused apache to lock up (I think a process ran away
with my RAM which caused swapping and apache to lock up.) Once I apache
running again, I wanted to check the munin graphs to see what the system
looked like during the lockup (which killed a number of processes due to
out of memory conditions). However, the graphs wouldn't generate and the
cgi was timing out without sending any data.

`Timeout waiting for output from CGI script /usr/lib/cgi-bin/munin-cgi-graph Premature end of script headers: munin-cgi-graph`

I'm not alone ether.
<http://wiki.kartbuilding.net/index.php/Further_issues_upgrading_to_Lenny#munin_with_cgi>
and <http://forum.linode.com/viewtopic.php?t=5171%3E> both had issues.
More googling still didn't find an answer so I tried to debug the perl
cgi. After using CPAN to get Devel:Trace installed, I discovered the cgi
was sitting waiting for a semaphore flag that it uses to ensure no more
than a certain number of munin-graphs are running at once. This is
great, except when a crash has caused this semaphore to be stuck at the
maximum so no more munin-graph processes get started ever!

There are 2 solutions. The first is simple, reboot. The second is also
simple, clear the semaphore flags manually. `ipcs` is the command to
show the flags and `ipcrm` is the command for removing the semaphores.
Check the man pages for information on the correct syntax.
