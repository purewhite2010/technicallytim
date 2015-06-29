Title: Coova Chilli & FreeRadius Reply-Message
Date: 2011-04-03 01:45
Author: Tim White
Category: Coding, Technical
Tags: Access-Reject, CoovaChili, FreeRadius, Hotspot, Reply-Message
Slug: coova-chilli-freeradius-reply-message

I was going to post this on the Grase Hotspot site, but will post it
here in depth and just the basics on the hotspot site.

Previously I researched this problem and found very little, it would
seem since my last search more material has become available that has
assisted. In particular
<http://freeradius.1045715.n5.nabble.com/RESOLVED-customize-Post-Auth-Type-REJECT-td2779460.html>
  
The basic problem is this. Using CoovaChilli, when a login failed for
some reason, we usually didn't get an error message. If your data quota
had been used up, then maybe you'd get "Your maximum never usage time
has been reached" which for most people was confusing. An expired
account may give you the error "Password Has Expired". However, any
other reason for a login failure and you'd usually not get a message.

At first, you may want to blame Coova Chilli. After all, it is the piece
of software sending back the login failed status, and if using the JSON
interface, it would send back the login failure message. However, good
CoovaChilli is just relaying the message it gets from the Radius server.
So we next turn our attention to FreeRadius.

The first place you may be tempted to look is in
/etc/freeradius/modules/expiration

    :::ini
    expiration {
            #
            # The Reply-Message which will be sent back in case the
            # account has expired. Dynamic substitution is supported
            #
            reply-message = "Password Has Expired\r\n" 
            #reply-message = "Your account has expired, %{User-Name}\r\n"
    }


This file gives you false hope. You see the option reply-message and
think, if the expiration has a reply-message, then surely I can just
drop a similar thing in at other places. However, what you don't realise
is that the reply-message is an option for the expiration module.
Internally the module has settings it understands, and other modules
won't understand those same settings! There is no setting for the sql
modules, or the sections that handle counting remaining quota. Putting
this reply-message option in other places will just cause FreeRadius to
fail to start.

By now, if you have read the link above, you may have some better
understanding of what to do. A good place to start reading for better
understanding of how freeradius reads it's config files is `man unlang`.
unlang is the "language" used by the config files, and reading it and
some of the accompanying documents with freeradius will enlighten you to
how things work.

I'll give you a large block of finished code, so you can start to
understand where all this fits together. This is an exceprt of
/etc/freeradius/sites-available/default with comments stripped out.
Please don't just copy and paste this, it's to give better understanding
of where the parts go, as many examples don't give you the context of
the changes needed.

    :::ini
    authorize {
        preprocess
        chap
        mschap
        suffix
        eap {
            ok = return
        }
        sql{
            notfound = 1
            reject = 2
        }
        if(notfound){
            update reply {
                Reply-Message := "Login Failed. Please check your Username and Password"
            }
            reject
        }
        
        if(reject){
            update reply {
                Reply-Message := "Login Failed. Please check your Username and Password"
            }
            reject
        }   


        expiration{
            userlock = 1
        }
        if(userlock){
                update reply {
                        Reply-Message := "Your account has expired, %{User-Name}"
                }
                reject
        }
        
        logintime

        noresetBytecounter{
            reject = 1
        }
        if(reject){
                update reply {
                        Reply-Message := "You have reached your bandwidth limit"
                }
                reject
        }

        
        noresetcounter{
            reject = 1
        }
        if(reject){
                update reply {
                        Reply-Message := "You have reached your time limit"
                }
                reject
        }

        pap
    }

    post-auth {
        sql
        exec
        Post-Auth-Type REJECT {
            update reply { # Fallback error message
                Reply-Message = "Login Failed. Please check your username and password"
            }
            attr_filter.access_reject
        }
    }

I'll start with the part that will help explain the best.

    :::ini
    noresetBytecounter{
        reject = 1
    }
    if(reject){
            update reply {
                    Reply-Message := "You have reached your bandwidth limit"
            }
            reject
    }

When I first saw this code, I thought it was setting a variable reject
to the value of 1. However it's not quite like that. See all modules
have return codes. For example, an ok code, or a reject or fail code.
However, that code is more than just a code, it also has an action with
it. For example, a reject code has the action, reject. Rather simple.
What the reject action does, is stop processing this section and return
a reject. What the 'reject = 1' does, is says that if this module
returns a reject, we set the action to a 1, which is setting it's
priority to 1, so that we can process more modules and get their error
codes too, and give them priorities, so the highest priority code wins.
This would let us do complex things for example, letting us exceed our
bandwidth limit as long as our time limit is also exceeded. Given that
we can have priorities from 1 to 99999 we can actually do really complex
things.

So what this first bit of code is doing then, is preventing a reject
from being sent straight away, so we can do more processing. And the
next bit of processing we do is test for that reject. (You may think
that this test could catch an earlier reject, but only if an earlier
reject also had it's priority set to something otherwise it's default
action would have been to return a reject straight away.) If this reject
exists, then the module noresetBytecounter must have triggered it. So we
update the reply package that FreeRadius is going to return, and set the
Reply-Message to an appropriate error message given then module that
caused the failure. We then send that reject without processing more
modules with the "reject" line. We could do other things like
sending an 'return' which would clear the reject and return an ok.

Most of the rest of that big piece of code is similar pieces of code,
although some have different codes, like userlock. The other important
piece of code sets a default message for Access-Reject.

    :::ini
    post-auth {
        sql
        exec
        Post-Auth-Type REJECT {
                    update reply { # Fallback error message
                        Reply-Message = "Login Failed. Please check your username and password"
                    }
            attr_filter.access_reject
        }
    }


It's rather easy to see what is happening here. In the post-auth section
(same file as the rest of the stuff), we match the Reject packets. We
then update the reply, with a generic error message. Because of the
operators (= .vs. :=) it will only add this Reply-Message if there is no
other Reply-Message already set in the Access-Reject. We used := before
to replace any Reply-Message already existing, so for example we could
override the cryptic message sthe the sql\_counter module sends back. We
could also use += if we want to "Append" Reply-Messages, allowing
multiple messages to be sent back. The "attr\_filter.access\_reject"
line is nothing to worry about, it just filters the return Access-Reject
packet to ensure only allowed attributes are sent back. As Reply-Message
is allowed, it isn't stripped out.

Hopefully that gives better understanding to what code is needed to
change/set the Reply-Message in Access-Reject packets. It could also be
used to send back messages with Access-Accept packets. The great thing
is that there are a good number of return codes, which allow you to make
some really complex changes to how the data flows. If you have read the
link at the start, you should by now start to realise how powerful
unlang is. Not only can you check return codes, you can also check parts
of the packet that have been "constructed". You can also change much
more than the Reply-Message, you can change if it's access is accepted
or rejected, what bandwidth controls are sent back, etc etc! For
example, and ISP can allow login even with incorrect password, yet move
that client to a different ip range that is setup for redirection to an
internal portal to assist with resetting the password.
(<http://www.easyzonecorp.net/network/view.php?ID=1042>). Or the link
from the start, they are using it so that when a datalimit is reached,
FreeRadius sends back a slower speed, i.e. throttling them once their
quota is used without disconnecting them! When you realise what power
RADIUS has, you understand why it's used by isp's and the like!

Keywords to assist people in finding this information. Radius,
FreeRadius, Access-Reject, Reply-Message, CoovaChilli, ChilliSpot,
Hotspot, sql reply-message reject

<ins>
The original version of this document had "ok = reject" lines instead of reject
lines. This happened to work due a bug in Freeradius that has since been fixed.
The correct line is just a plain reject in the if statements.
</ins>

  [http://freeradius.1045715.n5.nabble.com/RESOLVED-customize-Post-Auth-Type-REJECT-td2779460.html  
 ]: http://freeradius.1045715.n5.nabble.com/RESOLVED-customize-Post-Auth-Type-REJECT-td2779460.html
