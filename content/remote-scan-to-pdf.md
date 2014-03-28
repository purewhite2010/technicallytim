Title: Remote Scan to PDF
Date: 2011-04-20 16:42
Author: tim
Category: Blog, Coding, Technical
Tags: code, pdf, php, scan2pdf, scanner, scanning
Slug: remote-scan-to-pdf

I needed a simple and quick way for other users on the network to be
able to scan documents. So far, what I had been doing was running a
little bash script I found on the net, and scanning multiple pages into
a pdf. The problem was that I needed to run it, and teaching everyone
else to login via ssh and run it wasn't an option.

So I knocked together a little PHP application that did the basic things
the bash script does. It can even customise the settings (however that
is disabled atm due to a scanner problem). And to make it more natural,
I used jQuery and AJAX to run the jobs in the background without having
a script constantly reloading itself.

Warning, the script in it's current version has basically no security.
As there is a "readfile" part to dump the PDF to the browser, a user
could easily make it read any file the web server has access too. It
also has minimal error checking as generally things just work, and if
they don't, you start again.

So if you are looking for a simple solution for network access to your
scanner, and you don't want to go as far as phpsane, then here is the
code! <http://tim.purewhite.id.au/code/phpscan2pdf/files>
