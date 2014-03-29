Title: When did 'Linux' start moving away from it's simplicity?
Date: 2012-05-08 19:46
Author: Tim White
Category: Blog
Tags: accountservice, accountsservice, dbus, Gnome3, Linux, simplicity, unix
Slug: when-did-linux-start-moving-away-from-its-simplicity

Today I had the joy of trying to change a users desktop environment from
Gnome, to Cinnamon, via ssh. At first I thought it would be easy, change
the default desktop environment in lightdm.conf and restart. Fail. Ok,
so where is a users desktop environment preference stored? .dmrc, or at
least I thought so. I even logged in with a brand new user and confirmed
that it saved the users desktop preference in \~/.dmrc. Except, if I
changed .dmrc for a user, it just got overwritten with the old contents
at their next automatic login. (Remember, ssh, so can't use the gui to
change what was selected in the lightdm login screen).  
Wha?!!? Surely not a dconf/gconf setting somewhere. Search search
search. Still no luck. Eventually I discover a service called
"AccountsService" or something along that name. It stores the users
".dmrc" contents in /var/lib/AccountsService/users/ with a file for each
user, which believe it or not, can't be changed by the user! Arg! (And I
believe you need to kill accountsservice to be able to change the
contents of the file and have it actually honored, I tried just changing
it, but ended up changing it then rebooting to get it to work)

This is stupidity! Have a daemon, that one of it's tasks is to tell the
"display manager" what the users preferred desktop environment
preference is, that stores it in a place the user can't change, without
talking to the daemon! Oh, and write the contents of that file out to
.dmrc at login, but don't bother reading from that file.

Doing some more digging, AccountService is for querying and manipulating
user account information via D-Bus, essentially replacing the useradd,
usermod and userdel commands. I can't find a "homepage" for it, the
homepage listed is it's source code repo.
(<http://cgit.freedesktop.org/accountsservice/>)  (NB: Some more digging
finds this <http://www.freedesktop.org/wiki/Software/AccountsService> as
the homepage)  
I personally don't mind D-Bus, it services its purposes, but here is an
instance where it looks like someone has gone to the trouble of writing
a piece of code, to complicate some that use to be a simple stat/open of
a file, that the user was in total control of.

For the record, lightdm will work without AccountsService, and I believe
then it will honor \~/.dmrc  
Also, accountsservice isn't in Debian stable, but is in Debian testing,
and gdm3 and gnome depend on it. (So in other words Gnome3 depends on
it)

I just don't understand why we need to reinvent the wheel, take
something that is so simple (and fits in the Unix "philosophies" of
everything is a file, and that file formats should be simple text based)
and turn it into something that user no longer has control over, for
something that sets their preference!

Read
[http://blog.ngas.ch/archives/2011/12/13/the\_destructive\_desktop\_\_mdash\_linux\_in\_trouble/index.html][]for
some more thoughts on dbus.

  [http://blog.ngas.ch/archives/2011/12/13/the\_destructive\_desktop\_\_mdash\_linux\_in\_trouble/index.html]:
    http://blog.ngas.ch/archives/2011/12/13/the_destructive_desktop__mdash_linux_in_trouble/index.html%20
