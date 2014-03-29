Title: Asterisk Voip to Voip "Bridge" (Webcallback)
Date: 2010-10-29 06:35
Author: Tim White
Category: Technical
Tags: asterisk, bridge, callback, sip, sip to sip, voip, voip to voip, webcallback
Slug: asterisk-voip-to-voip-bridge-webcallback

Call it what you like. Sip to Sip, VoIP to VoIP, VoIP Bridge, Callback,
Webcallback. The idea is to have a server somewhere call two SIP(VoIP)
devices and connect the 2 calls together.

What's the point of it? Maybe you are stuck somewhere with a phone that
only accepts incoming calls, and you want to make cheap voip calls. Or
you are overseas, and it's cheaper to call from Australia to your
location that from your location to Australia. For example you may have
a payphone that accepts incoming calls but outgoing calls are expensive.
Or you just want to enjoy nice cheap VoIP rates but don't have any VoIP
hardware at your location, or poor dodgy internet, but have a mobile
phone or landline.

What ever the reason, being able to have a VoIP call that connects to
your location, then calls another party is a great thing!

Now before I go much further, if all you want is this ability to be
called, and then have your remote party called, [PennyTel][] has this
Webcallback feature built in. Mynetfone doesn't, but if you can make
outgoing calls you can use their ANI callback feature (you call a
special number, your caller ID needs to not be blocked, and then you
hangup after it rings, then it calls you back and lets you make your
VoIP call). So, if you aren't going to be using this much, and don't
need lots of customisation or special features, just signup for PennyTel
and start using their Webcallback feature. Remember, you pay the cost of
2 calls using this feature, not 1. First, the cost to your number, then
the cost to whom you are calling. So if both parties are mobile phones,
then it certainly might not be cheap anymore. How ever, if your number
is a landline in australia, and so is the party you are calling, then
it'll cost a total of \$0.16 to make your call (on their Freedom Untimed
plan). This is pretty cheap compared to most normal telco's.

Read on however, if you want the ability to use just about any VoIP
provider, and want to maybe use multiple VoIP providers and have heaps
of control over it all.

Asterisk, the VoIP/PBX mega funky software, will turn a normal server
into a PBX/VoIP Gateway etc etc. When I first looked to a solution to
this issue a few years ago, I looked at the task of setting up Asterisk
and found it daunting, so gave up. PennyTel Webcallback essentially
delivered what I needed so I left it alone until now. I now have
Asterisk setup as a simple VoIP system that allows me to make 2 calls
(using multiple VoIP providers if I want) and join them together.

Why is it better than PennyTel Webcallback?  
For me it's better because it can work out cheaper for me. PennyTel
callback is \$0.16 total (\$0.08 per each call to landline). However, if
I'm calling someone who is a MyNetFone customer, if  I was to call their
VoIP number from a MyNetFone VoIP account, the call would be free. And
if I'm on a MyNetFone monthly plan, then I could have a good number of
free landline calls each month. My optimal solution is currently
combining both MyNetFone and PennyTel. PennyTel to the normal landline,
\$0.08, and MyNetFone to the MyNetFone VoIP numbers, \$0.00. So it's a
total of \$0.08 for the whole call! So depending on your location, and
your destination number, and your VoIP provider plans, you can get your
calls cheaper than using PennyTel webcallback. And just the fact that
you can use this Callback method with just about any VoIP provider,
priceless!

So lets get onto the easy part, setting it all up. While at first this
can look daunting, in reality, it's very simple. This is all based on an
Ubuntu 10.04 box, using the CLI. Quick note before we start, what ever
machine you set this up on, needs to have enough bandwidth for 2 calls
at the same time. So if you are putting it on a home ADSL connection,
check you have enough up and down bandwidth for this. My server is
hosted out on the internet and has enough bandwidth. A big reason for me
setting this up is lack of a decent internet connection from my home to
be able to do normal VoIP.

    :::bash
    sudo apt-get install asterisk

Yes,this does pull in a far few bits of software, some of which isn't
needed and I've not even poked at yet, but this is what we do to get
Asterisk installed. Easy.

Now the setup. You need to edit /etc/asterisk/sip.conf to add your VoIP
providers. Some providers give you the Asterisk details on their site,
many others are just a google away, generally on
http://www.voip-info.org/

So drop down to the bottom of the [general] section in
/etc/asterisk/sip.conf and add in a register line for each VoIP
provider. Mine is in the following format. You can see that the username
is repeated a few times on the mynetfone one. It can be different for
other providers.

    :::ini
    register => username@sip01.mynetfone.com.au:password:username@sip01.mynetfone.com.au/username

    register => 888xxxxxxx:secret@sip.pennytel.com/888xxxxxxx

Now drop to the bottom of the /etc/asterisk/sip.conf file, and add in
your "trunks" for the VoIP providers. In my situation, I don't want
incoming calls (as then they need to be routed), so I just have the
outgoing trunks.

    :::ini
    [mynetfone-out]
    disallow=all
    allow=alaw
    allow=ulaw
    allow=ilbc
    allow=g729
    allow=gsm
    allow=g723
    authname=09xxxxxx
    canreinvite=no
    dtmfmode=rfc2833
    fromuser=09xxxxxx
    host=sip01.mynetfone.com.au
    insecure=very
    nat=no
    pedantic=no
    qualify=yes
    secret=password
    type=friend
    defaultuser=09xxxxxx

    [pennytel-out]
    type=friend
    host=sip.pennytel.com
    fromuser=888xxxxxxx
    defaultuser=888xxxxxxx
    secret=password
    canreinvite=no
    insecure=invite

Again, these can look different. A bit of googling around should help,
or if you work from the above you should be able to work out the
settings for your own provider. Note, username is no more in newer
Asterisk versions, it's now defaultuser, so you may need to change what
you find on the net.

Have a look in /etc/asterisk/manager.conf, you'll see you need to create
a file in /etc/asterisk/manager.d/ to add a user. You may wish to do
this so you can use the astman tool later, which helps with
disconnecting calls and monitoring things. (You can do this through the
asterisk cli, how ever it may be a bit harder).

The format of the file you create is as follows.
/etc/asterisk/manager.d/somename.conf

    :::ini
    [username]
    secret = password
    read = system,call,log,verbose,command,agent,user,config
    write = system,call.log,verbose,command,agent,user,config 

This username and password isn't related to your VPS at all, it's what
you'll use when logging in with Astman or other tools.

Now we get to the bit we've been waiting for, setting it up to connect 2
calls.  
Edit /etc/asterisk/extensions.conf. Comment out the include =\> demo
line from the [default] section. There is a section in the [default]
that should sort out Hangup/Busy detection and the likes, so the
extensions we are adding can be very simple, however, you can customise
these very easily to do more than just connect the 2 calls.

    :::ini
    [DialOutMyNetFone]
    exten => _0X.,1,Dial(SIP/mynetfone-out/${EXTEN})

    [DialOutPennyTel]
    exten => _0X.,1,Dial(SIP/pennytel-out/${EXTEN})

And we are done. Everything should be setup now. The default install of
Asterisk has autoloading on in /etc/asterisk/modules.conf so the rest
should just work.

After all those edits, restart asterisk.

    sudo /etc/init.d/asterisk restart

Now we create our call file.

    :::ini
    Channel: SIP/pennytel-out/YOURNUMBER
    Context: DialOutMyNetFone
    Extension: WHOTOCALLNUMBER
    Priority: 1
    Archive: Yes

Very simple file. The Channel line is what calls you, so replace
pennytel-out with the trunk you wish to use to call you. (It can be the
same as the trunk used later on, or different. In this example, it's
different as I want the cheap call to my landline, and the free call to
a mynetfone number). The Context is the extension name that we defined
in /etc/asterisk/extensions.conf, and the Extension is the number that
you wish to call. Both for YOURNUMBER and WHOTOCALLNUMBER you need to
know the format your VoIP provider uses. Some will allow just a
localised version, for example in australia I can just dial 075xxxxxx or
040 123 4567, and MyNetFone understands them. Some other VoIP providers
might need 6175xxxxxx instead. Dialing internation, some just need the
country code, others need a prefix like 0011, etc etc.

Now to actually place the call. There are a number of methods of doing
this, the end result needs to be a call file placed in the
/var/spool/asterisk/outgoing directory, owned by the asterisk user, and
placed in a way that asterisk can't start reading it before the file is
all there. For this reason, the mv command is recommended and I'll
demonstrate. (I first copy the file so I can keep a number of pre setup
files stored).

    cp preset1.call call123.call
    sudo chown asterisk call123.call
    sudo mv call123.call /var/spool/asterisk/outgoing/

As soon as the file hits that directory, asterisk reads it and executes
it. If everything goes right, within 10 seconds your phone should start
ringing. Pick it up, it'll then start ringing the other party, finally,
when they pickup you can start talking! Done.

Sometimes the hangup detection doesn't work properly. I've not yet
worked out why or how to fix it, I believe there are a number of things
to tweak regarding this. What I currently do is run 'astman localhost'
(from the machine running asterisk), login with the details we setup
earlier, and I can think select the call and press hangup if it doesn't
hangup correctly.

For more details about Call files, check out
<http://www.voip-info.org/wiki/view/Asterisk+auto-dial+out>

Of course, it's not always practical to ssh into your server just to
make a phone call. I'll leave the task of setting up other methods of
creating and moving the call files to the reader. Please though, don't
give your web server user full sudo access without a password! I'd
recommend ether a database with a cron runner script (running as the
asterisk user), or something similar.

Last things. Check your firewall. You'll need to open some RTP ports and
some SIP ports. A google will reveal more. Try to limit what you open
though, I've not given any instructions for securing asterisk in this
post, that also is for your further reading.

  [PennyTel]: http://pennytel.com.au
