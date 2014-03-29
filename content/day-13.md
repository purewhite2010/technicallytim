Title: Day 13
Date: 2011-08-29 13:03
Author: Tim White
Category: Blog, Coding, projectX
Tags: GPS, iOS, iPhone, XCode
Slug: day-13

I think today is Day 13.

So finally I've had a chance to sit down and nut this out. First things
first, getting hello world to run on the iPhone. Finally I worked out
how to self sign a certificate, and get Xcode to build it, then using a
custom script I found on the net, sign the code so the iPhone will run
it. Yay! Hello World runs on the iPhone!

Next step. Get a GPS app running on the iPhone. After following a pretty
good tutorial from
http://www.vellios.com/2010/08/16/core-location-gps-tutorial/ I finally
got a GPS test app running. (After making some changes so it would run
on iOS 3.1). However, this is the end of the good news. So far, as I
suspected, the iPhone 3GS isn't performing well on the GPS. Accuracy of
1km isn't good enough, that can be achieved with just network location!
We need down to about 10m. I'm thinking maybe I will need to upgrade to
a newer iOS to see if it's an issue with the hardware or the software.
However I want this app to run on iOS 3.1, so am hesitant to do any
upgrades.

The last of the good news is that the Objective-C is starting to make
some sense to me, and I'll now work on learning the major differences,
and some more subtle ones, between Objective-C, C++ and
C.<small></small>
