Title: Handbrake Encoding Cluster
Date: 2010-09-09 18:18
Author: tim
Category: Coding, Technical
Tags: bzr, cluster, code, distributed, encode, encoding, gearman, handbrake, handbrakecli, script, transcode
Slug: handbrake-encoding-cluster

Recently I've been given the task of putting a DVD collection on to the
computer (for backup purposes, so that the originals can be locked away
and not damaged by little hands). Having used [Handbrake][] before to
convert DVD's to H.264 videos, I figured I'd be able to use it again.
But for such a large task, it makes sense to have many computers doing
the encoding. Unlike dvd::rip, Handbrake doesn't have a distributed
cluster feature.

I found a possible solution in the Handbrake Forums, using ppss and some
scripts. <http://forum.handbrake.fr/viewtopic.php?f=6&t=17504>

Unfortunately, I wasn't able to get PPSS working how I wanted (or at
all). However, it did provide me with a transcode bash script that
assisted with getting the HandbrakeCLI options right, in particular
splitting TV episodes into individual episodes.

I continued looking for ways to do this, knowing I'd previously used
some clustering script many years ago, and finally found [gearman][].  
At first glace, gearman seems to be perfect, except digging deeper you
discover it's designed to be called from within applications and not so
much as a command line "queue". Thankfully I discovered a [post][]
explaining how to make gearman more command line friendly using xargs.
(Which also helped me finally understand how xargs work!) So with a bit
of scripting I had myself a number of small shell scripts, a gearmand
server, and a working cluster.

Firstly, I setup some NFS mounts on all the computers involved.

~~~~ {escaped="true" lang="bash"}
$ mkdir /mnt/DVD_rip
$ mkdir /mnt/DVD_encode
~~~~

For me, I had 2 mounts as I wanted the DVD\_rip folder to be on a local
computer, and the DVD\_encode folder to be on a server that all the
finished files needed to be on.

I then created a simple [bash script][] for ripping the disks (with
error handling). I can run this script in the /mnt/DVD\_rip folder, give
it one argument (the DVD name) and it'll rip the disk and attempt to
retry any sectors that have errors. The 'lsdvd' is so that css keys are
loaded so you can read encrypted DVD's. You can also stop and restart
the ripping process at any time without loosing what has been ripped
successfully. NB: It doesn't remove the CSS encryption so you will need
libdvdcss on all computers doing encoding.

~~~~ {escaped="true" lang="bash"}
lsdvd /dev/sr0 > /dev/null & ddrescue -r 1 /dev/sr0 "$1.iso" "$1.log"
~~~~

My next script ([submitjob.sh][]) is another 1 liner, it submits the job
to gearmand. It simply takes the name of the file to encode (iso or a
video file) and optionally an attribute that ether tells our transcoding
script to encode all the titles (split episodes) or which title to
encode. Without this attribute it will scan for the longest title and
only encode that.

My next script ([startworker.sh][]) starts the gearman worker processes.
I run it on each machine in the cluster that I want processing videos. I
usually run it in a screen session as when it's encoding it outputs some
information through this script, the rest goes into log files. NB: The
script has the hostname of the gearmand server in it as does the
[submitjob.sh][] script.

Our last script ([transcode2mkv.sh][]) is the actually transcoding
script. This is what the gearman worker calls to do the encoding. I got
this script from the method that uses PPSS at
<http://forum.handbrake.fr/viewtopic.php?f=6&t=17504>. I then modified
it to encode to mkv files instead of mp4, and I changed some of the
default encoding options, as well as how it handled the titles (i.e.
selecting all, or individual ones), and how it handled selection of
audio and subtitle tracks (it selected them all, I wanted it to just
select the English audio, and all the subtitles). I also added logging
so that it would update a cluster log when it started and stopped
encoding (with timestamps), and to log the progress output to one
logfile, and the verbose information to another logfile (so I could
easily tail the logfile to get the current progress).  
Initially for doing TV episodes, this script would select all the
titles and encode each one to it's own file. I changed it to just select
the 4 I wanted, and then later changed it so I could select individual
titles. The reason I changed to selecting individual titles was that
some of my encoding machines are faster than others, this way I didn't
have 3 machines sitting idle while one machine was still on the first
title of the disk, instead they each took a title and the disk was
processed a lot quicker.

All the files can be found at
<http://tim.purewhite.id.au/code/handbrake-cluster> or checked out with
bzr.

~~~~ {escaped="true" lang="bash"}
bzr branch http://tim.purewhite.id.au/code/handbrake-cluster/
~~~~

  [Handbrake]: http://handbrake.fr
  [gearman]: http://gearman.org/
  [post]: http://stefaanlippens.net/gearman_setting_worker_process_arguments_through_xargs
  [bash script]: http://tim.purewhite.id.au/code/handbrake-cluster/rip
  [submitjob.sh]: http://tim.purewhite.id.au/code/handbrake-cluster/submitjob.sh
  [startworker.sh]: http://tim.purewhite.id.au/code/handbrake-cluster/startworker.sh
  [transcode2mkv.sh]: http://tim.purewhite.id.au/code/handbrake-cluster/transcode2mkv.sh
