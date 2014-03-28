Title: What it takes to keep things running. (How to reduce comment/wiki spam)
Date: 2011-04-05 22:13
Author: tim
Category: Blog
Tags: password, project honey pot, pwdhash, security, spam
Slug: what-it-takes-to-keep-things-running-how-to-reduce-commentwiki-spam

I recently pushed out a new version of the [GRASE Hotspot][]. I spent
lots of time working on rewriting the splash/welcome page, and login
forms so that they would work even with javascript disabled, and allow
you to force it into the non javascript version if you are having
problems (so browsers like Safari can be used). However, recently I've
spent a lot of time just doing maintenance.

The maintenance started when again I spent lots of time cleaning up spam
on the wiki, this was after enabling ReCAPTCHA. I decided it wasn't
practical to keep cleaning up the wiki, and seeing as I was the only one
contributing to it, it made more sense migrating it to a Wordpress site.
After the migration was done, I quickly started getting comment spam on
the new site!! Thankfully, Akismet blocks comment spam, but the volume
of spam coming in was enormous! A peek into the server logs showed that
the same ip's that were publishing spam in the wiki, would try to get
post to the missing wiki, find it missing and discover the wordpress
site and immediately try to post comment spam! It was time to reduce the
load on the server if possible.

After some research, I implemented some basic .htaccess rules that would
block some of the spam even getting processed. But why couldn't I find a
simple DNSBL for Apache? Turns out the right googling will find
libapache2-mod-spamhaus, which does what we need. But unlike email spam,
it seems comment/wiki spammers aren't in the DNSBL's as much as email
spammers. Thankfully, libapache2-mod-spamhaus was now dropping about
half the spamming connections.

Some more research turned up [Project Honey Pot][] which is aimed more
at the comment spammers and address harvesters. A quick check of the ip
database they maintain revealed that most of the remaining comment
spammer ips that were hitting my site were in their database!
Unfortunately, the mod\_httpbl module for Apache isn't in a nice
repository anywhere, and hasn't been touched for awhile, so setup wasn't
as easy. I found [Repel][] which is a simple Python program that you use
with mod\_rewrite (and RewriteMap's). It's not so easy to setup, mainly
due to the instructions being a little unclear, but also because the
rewrite rules that use Repel can be very tricky. The documentation was
good for just blocking, however I figured if I was going to use Project
Honey Pot, I should contribute too, so I setup a honeypot on the site
and then had fun and games with rewrite rules. Eventually though, I got
it all setup. Now if you are thinking of setting this up yourself, it's
probably a lot easier using the [Wordpress Plugin][] which I've since
setup on another site I assist with. While this will block the spammers,
or direct them to a honeypot, it may have slightly more load than Repel.
This is because Repel is a little python program, that apache already
has running, and just passes the ipaddress to and waits for a reply. The
wordpress plugin solution requires Apache to fire up PHP, which then
fires up Wordpress, which then loads the plugin which finally gets the
ipaddress, does the DNS lookup and then goes from there. I've done no
testing, but logically Repel would appear to use less resources, but you
are welcome to prove me wrong.

On top of all that maintenance, I also had some mail servers receiving
spam, which should have been blocked. Some more tweaks and changes, and
another influx of spam is now not getting past the gate.

 

Lastly, some advice. Password advice. In particular because I heard an
"expert" on the ABC radio recently giving some poor advice. Get yourself
a strong password, with letters and numbers, maybe some capital letters
as well as lowercase, and decent length, at least 8 characters long. Now
use that password for one place, and only one place, maybe your email
account. Now find another one, just as strong, use that for your next
account, maybe facebook. Reusing passwords is a big No No, as an
important CEO recently discovered.  
I can hear you already, moaning and groaning. It's so hard to remember
one really strong password, how can you remember more than one? Well
this is the easy part. You use a formula. I've started using
[PwdHash][], developed by Standford University. It simply takes the
domain name of the site you are generating the password, and your master
password, and creates you a "hash" that you use as your password for
that site. So for example, if my master password was
'thecatsatonthemat', my facebook password would be
'F58VFRH8eUejfcIs9UA'. This will let you create strong unique passwords
for each account, then if one of your accounts is broken into and the
password somehow discovered, your other accounts are safe. Of course, if
your email account gets broken into, a lot of other accounts are not
safe as the hacker can then just reset your passwords by using the "Lost
Password" feature many sites provide.

If you do decide to use PwdHash, you can install a firefox extension
that assist, or you can use it directly on the site (as it uses
Javascript, your password never leaves the computer, you can even save
the page and use it offline). I found a little python script that does
it for me, which I have on my server and my machine, so I can create my
pwdhash's even when I don't have a browser handy. Of course, there is
nothing preventing you having multiple master passwords ether, just to
make it even more secure!

  [GRASE Hotspot]: http://hotspot.purewhite.id.au/
  [Project Honey Pot]: %20http://www.projecthoneypot.org?rf=93412
    "Project Honey Pot"
  [Repel]: http://repel.in-progress.com/
  [Wordpress Plugin]: http://wordpress.org/extend/plugins/httpbl/
    "Wordpress Http:bl Plugin"
  [PwdHash]: https://www.pwdhash.com/ "PwdHash"
