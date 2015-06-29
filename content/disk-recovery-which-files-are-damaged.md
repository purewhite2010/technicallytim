Title: Disk recovery - Which files are damaged?
Date: 2011-04-19 09:40
Author: Tim White
Category: Blog, Technical
Tags: damaged, fat32, recovery, sector
Slug: disk-recovery-which-files-are-damaged

<ins datetime="2011-08-11T21:49:04+00:00">First, getting an image of the
damaged hard drive.

    $ ddrescue -n /dev/inputdevice rescued.img rescued.log

    $ ddrescue -r 1 /dev/inputdevice rescued.img rescued.log

The first ddrescue command tries to fly through the disk as quickly as
possible, skipping over sections when an error occurs. This allows me to
recover most of the good data as quickly as possible. The second command
(which is only needed if you had errors found with the first command)
will then retry the bad sections of disk, splitting the error sections
into smaller and smaller parts until you eventually have individual
blocks that are damaged. It is here that ddrescue really works hard to
recover your data, and this part can take just as long as the first
part.</ins>

So you have successfully used ddrescue to recover everything you can off
a failing hard drive. Now you have a big image file, maybe 500Gb, with
sectors that could be recovered, and those that couldn't. But how do you
find which files belong to the broken sectors? I recently had this
problem with a FAT32 filesystem. After lots and lots of googling, I
still didn't have a decent answer. Windows has a tool called DiskView,
however it doesn't appear to work on disk images. There is also a Hex
viewer around that apparently will tell you which files belong to the
sector you are viewing, but I had no luck with that ether.

Eventually I stumbled across a toolset I should have used from the
start. The Sleuth Kit. I also stumbled across a paper someone had
written doing some forensics with The Sleuth Kit which pointed me to the
right tools, although some had changed names.

However, let me first point you to a fairly simple way that is hidden in
the ddrescue info pages. While at first it sounds like this method
should be the long hard way, it actually works out to be the easiest
way.

It is suggested in the ddrescue info pages that you md5sum all the files
in the image, then using ddrescue in fill mode you write some data (that
isn't all zero's) to the sections that couldn't be recovered, and then
md5sum all the files again and compare. Seeing as I had already copied
all the files off the image, it was actually even simplier than that. I
wrote the random data to the damaged sections (in this case "BADSECTOR"
over and over again) and then did a diff between the files on the image
and the files I had already copied off the image. It did take awhile to
do the diff, but 4hrs to compare 180Gb of files with 180Gb of files,
over a network isn't that bad. I'm sure it would have been a lot quicker
had all the files resided on the local machine on  a nice RAID array.

So a simplified example

copy all files off rescued image (loop mount) to another location

    $ echo -n "BAD SECTOR " > tmpfile
    $ ddrescue --fill=- tmpfile rescue.img rescue.log

    $ diff -r /mnt/loop/ /mnt/server/rescuedfiles/ > damagedfiles

You'll then have a list of files that differ between the 2 versions,
which are the ones with damaged sectors. Also, the ddrescue doesn't
damage the logfile so you can then reverse it using /dev/zero to restore
the image to it's original recovery state. This won't work with sparse
files.

    $ ddrescue --fill=- /dev/zero rescue.img rescue.log

<ins datetime="2011-08-11T21:54:00+00:00">Or, if you haven't copied the
files off, then the way suggested in the ddrescue manual looks like
this. (After getting your disk image)


    # mount -o loop rescued.img /mnt/loop

    $ find /mnt/loop -type f -print0 | xargs -0 md5sum > prefill.md5

    $ echo -n "BAD SECTOR " > tmpfile
    $ ddrescue --fill=- tmpfile rescue.img rescue.log

    ## You may need to unmount and remount the loop file to prevent any caching interferring.
    # umount /mnt/loop
    # mount -o loop rescued.img /mnt/loop

    $ find /mnt/loop -type f -print0 | xargs -0 md5sum > postfill.md5

    $ diff prefill.md5 postfill.md5


</ins>

<ins datetime="2011-08-11T21:42:04+00:00">**This is all you need when
trying to work out which files are damaged. The following is another
method for really peaking into the file system that may be more useful
for deeper analysis**</ins>

However, if you do want to find out which files are in the damaged
sectors, then continue as it is possible.

First, check that the sector is actually used. This used to be the dstat
command, but it has since been renamed to blkstat. So we take a sector
number from the logfile that couldn't be recovered.

    $ cat rescue.log |grep -|head
    0x0178F200  0x0000D400  -
    0x017A0000  0x00000200  -
    0x2BC488F400  0x00011600  -
    0x2BEEFF0A00  0x00020000  -
    0x5AC5FB0A00  0x00020000  -
    0x5AC6050A00  0x00020000  -
    0x5AC60E0A00  0x00020000  -
    0x5AC6180A00  0x00020000  -
    0x5AC6220A00  0x00020000  -
    0x5AC62B0A00  0x00020000  -

We then convert it to a sector number. I know the sector size is 512
bytes in this case, but you will need to verify it for your drive. If in
doubt, do the conversion, open a hexeditor, jump to that location, use
the previous ddrescue command to fill in the badsectors with some known
next, and confirm that the known text is at the address you are
viewing.  
I've picked sector 0x2BEEFF0A00 to analyise. So I convert it to decimal
and dived by 512 (the sector size). I can do this all at once if I know
that 512 in hex is 200.

    $ echo "ibase=16; 2BEEFF0A00/200"|bc
    368541573

Or do it the long way

    $ echo "ibase=16; 2BEEFF0A00"|bc
    188693285376
    $ echo "188693285376/512"|bc
    368541573

Ether way, I now know that the sector number is 368541573. Using blkstat
(formerly dstat) I can verify that the sector is used or not.

    $ blkstat rescued.img 368541573
    Sector: 368541573
    Allocated
    Cluster: 5754738


Now a little warning, if you get a sector that looks like this.

    $ blkstat rescued.img 48249
    Sector: 48249
    Allocated (Meta)

Then you are probably looking at a sector in a directory listing. The
next tool we are going to use, ifind, may take a very long time to
process that sector for almost no gain. I would leave these sectors
until you have processed the others. I believe this one for me actually
is in one of the FAT's, which just told me that the FAT was probably
damaged. What I can do is work with the damaged FAT initially, then
switch over to the other FAT and see what is different. (Which I won't
cover in this post) <ins datetime="2011-04-18T23:52:56+00:00">On further
investigation, it turns out this sector was in an unused part of the
FAT, so had caused no damage to the FAT. Damage to the fat could prevent
you from even seeing some of the files, so hopefully when you have
damage to the FAT your 2nd FAT will still be good.</ins>

Our next step is to use ifind to find the inode associated with the
sector. This can take some time and lots of CPU.

    $ time ifind rescued.img -d 368541573
    5892375559

    real    2m52.314s
    user    1m15.280s
    sys 0m2.170s

This finally gives us the inode associated with that file.

    $ istat rescued.img 5892375559|head -12
    Directory Entry: 5892375559
    Allocated
    File Attributes: File, Archive
    Size: 21346140
    Name: MICROS~1

    Directory Entry Times:
    Written:    Wed Aug 25 22:16:38 2010
    Accessed:   Wed Apr 13 00:00:00 2011
    Created:    Wed Aug 25 22:16:39 2010

    Sectors:

The listing then goes on to show all sectors that the file uses. If we
grep the listing, we can confirm that the sector 5892375559 is in that
file. Unfortunately, we are stuck with the 8.3 filename and not the
complete filename. Thankfully another tool will come to our rescue. If
you are looking for a good number of files that are affected (i.e. more
than 1 or 2 sectors) you'll want to run this command without the grep,
and save the contents to a file so you can just grep over that file each
time as it takes a long time to recursively list all the files in a big
filesystem.

    $ fls -rFp bunsom.img |grep 5892375559
    r/r 5892375559: Microsoft Office 2011/Office/Microsoft Chart Converter.app/Contents/MacOS/Microsoft Chart Converter

So finally we can see that the inode 5892375559, which contains our
damaged sector, belongs to this file from the Microsoft Office Chart
Converter App. (Yes, it does look a little strange this file but that's
because it's a OS X App file).

We can now repeat this for all damaged sectors. However, I'd be first
getting a list of all sectors (remember that the second column in the
ddrescue log is size of the damaged area, use that to work out who many
sectors in a row are damaged). I'd then check the file we have just
found (use the istat tool) to see if any of the other damaged sectors
are also in that file.

*keywords to assist others finding it: data recovery, damaged sector,
file at sector, file belong to sector, sector contents, damaged files,
fat32, sector explore, sector view*

## Comments
Leave a comment by adding to the [issue on
Github](https://github.com/timwhite/technicallytim/issues/1)

Comment from [amichair](https://github.com/amichair):
> Thanks for the article, it's been very helpful!

> A few updates that might save time for the next person to need it:

> * instead of the hex calculations and using bc, one can simply use 'ddrescuelog
-l- ddrescue.log'. This outputs all the bad ('-') sector numbers in decimal,
i.e. it does both the division by sector size and conversion to decimal, and in
addition it outputs all the sectors and not just the first one of each series
of bad blocks (you mention this in the last paragraph but with no example of
how to do this). So this one command takes care of a lot of stuff in one fell
swoop.

> * in some larger disks nowadays the sector size is 4096 rather than 512. Thus
calculating the 'data unit' used in the sleuthkit tools might require an
additional division by 8 (after division by 512).

> * the version of sleuthkit in Ubuntu (up to 13.10, and it looks like it won't
change by the 14.04 release this week) is a couple years old, and as it turns
out, does not support ext4. While this is platform-specific (though pretty
common platform), the important note is that blkstat works ok, but then ifind
says 'inode not found', which is a bit perplexing considering it is marked as
'Allocated'. So the filesystem auto-detection fails silently. Only if one
specifies '-f ext4' explicitly does he find out that ext4 is not supported. I
had to download and build the latest sleuthkit myself for it to work with ext4
properly.

> Thanks once again for this great tutorial!
