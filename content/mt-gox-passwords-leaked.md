Title: Mt Gox Passwords Leaked
Date: 2011-06-20 14:37
Author: tim
Category: Blog, Technical
Tags: bitcoin, crack, database, leaked, mt gox, password
Slug: mt-gox-passwords-leaked

For the second time in a week, I've heard of a websites user database
being leaked. In the first case it was from a site I've never used. The
second though was a site I signed up to a few months back.  
One of the biggest problems with this leaked database is that the
hashing function used isn't that strong when the hacker has rainbow
tables to use to crack the database.  
The first side effect of this for me was to go and change some of my
passwords as a precautionary measure. The second side effect, and the
more annoying one, is that I used a private email address for this
particular account instead of using one of my "junk" gmail addresses. So
now my private email address is in the hands of every hacker who is
trying to crack that database. And already we are receiving "spam" to
those addresses in that database. Most of it so far is users ether
letting you know the Mt Gox database has been hacked, or users/owners of
other Bitcoin exchanges sending you "advertising" so you'll come start
using their exchange. I've email gotten an email advertising online
storage from a company that accepts Bitcoins as payments. And they
haven't bothered to try and keep the email addresses slightly private,
1500 other people also have my address, and I have theirs, as no Bcc was
used. (Of course, spam filtering will quickly filter that particular
email out).  
Interested to see how bad the compromise was, and if it'll affect me,
I've also downloaded the user database now. A quick look shows that my
password is hashed with the less secure method and a quick bit of code
later I can confirm the password I used to make that hash. Luckily for
me, I use pwdhash to generate a unique password for each site I use.
This means that an attacker who has cracked my hashed password in the Mt
Gox password, still only has a password that can be used for one site,
Mt Gox. If they had enough time and power, then maybe they could work
backwards and eventually find the password I used to generate my pwdhash
passwords, but by the time they did this, I'd have changed all those
passwords anyway.  
Having only been using pwdhashing for a little while now, it was good
to discover that it has already protected me from an attack. A number of
user who had simple passwords that have been cracked already, have also
had other accounts attacked as they used the same password in multiple
places.

 

An interesting side note is how much the Mt Gox Bitcoin exchange has
grown in a very short space of time. A discussion taking place in a
forum noted that your position in the database is related to when you
signed up. Working from knowing when you signed up shows how many people
signed up after you. It seems to have had exponential growth in the last
few weeks, which is good for Bitcoin in general, but bad once you
realise how this will look to all those new users. Looking at my
position in the database, I can see I was a very early adopter.

 
