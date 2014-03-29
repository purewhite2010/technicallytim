Title: Nginx, PHP-FPM, Wordpress, Super Cache
Date: 2011-10-24 11:37
Author: tim
Category: Blog, Technical
Tags: Nginx, php-fpm, secure, supercache, try_files, wordpress
Slug: nginx-php-fpm-wordpress-super-cache

So recently I've been exploring the alternative world of Nginx instead
of Apache, and PHP-FPM instead of mod\_php. There are plenty of
tutorials on the net for getting all of this setup, however not that
many are up to date anymore for the Super Cache stuff. Hopefully what I
present here will be a more up to date config, that is also mostly
secure compare to a good number of ones on the net (to do with passing
non PHP files to the php interpreter).

Firstly, my Nginx config for this very blog.

    :::nginx
    server {
      server_name www.tim.purewhite.id.au;
      rewrite ^/(.*) http://tim.purewhite.id.au/$1 permanent;
    }

    server {
        server_name tim.purewhite.id.au static.tim.purewhite.id.au;
        root /home/tim/domains/tim.purewhite.id.au/public_html;

        access_log /var/log/nginx/tim.purewhite.id.au_access_log;
        access_log  /var/log/nginx/default.access.log host_combined;
        #access_log  /var/log/nginx/uri.log host_combined_uri;
        error_log /var/log/nginx/tim.purewhite.id.au_error_log;

        index index.php;

        location / {

            if ($http_cookie ~ "comment_author_|wordpress|wp-postpass_") {
                rewrite ^/(.*) /loggedin$1 last;
            }
            try_files $uri
            /wordpress/wp-content/cache/supercache/$http_host/$uri/index.html
            $uri/
            /index.php;
        }

        location /loggedin {
            internal;
            rewrite ^/loggedin(.*) /$1 break;
            try_files $uri $uri/ /index.php;
        }


        location ^~ /code {
                proxy_set_header Host $host;
                proxy_set_header X-Forwarded-Server $host;
                proxy_set_header X-Forwarded-Host $host;
                proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_pass http://127.0.0.1:8080/code/;
        }

        location ~* \.(ico|css|js|gif|jpe?g|png)$ {
            expires 1w;
            break;
        }



        fastcgi_intercept_errors off;

        location ~ \.php {
            try_files $uri =404;
            include fastcgi_params;
            fastcgi_pass   127.0.0.1:9002;
        }

        include drop;
    }

The first thing to notice is line 1-4. This simply redirects everyone
from www.tim.purewhite.id.au to tim.purewhite.id.au. Simple as that.

Next we define the server and the root document path. Still very
standard. Then we define access logs, for various reason I'm logging to
more than one place, but that'll change once everything is finished.

Line 15 is boring, we just define the "index index.php" so that if you
access a directory it will load index.php or give you a 404 (which it
won't because of things further down).

Now for the fun. Lines 19-21. These catch a logged in user and send them
on an internal redirect down to lines 28-32. This is so we don't serve
cached content to logged in users. That little snippit is thanks to a
post at <http://permalink.gmane.org/gmane.comp.web.nginx.english/15664>.

However, there was a problem in the rest of the code. Thanks to a post
at
<http://wordpress.org/support/topic/lack-of-nginx-support-from-wp-super-cache>
I realised we needed to test if the cache was being used or not. So I
added the extra logging and discovered it wasn't. I quickly worked out
what the problem was. The code at lines 22 - 25 had the middle 2 lines
swapped around. So "\$uri/" was before the supercache line. What this
mean was that it would try if the \$uri was a directory, and to load a
directory it would try index.php (due to the index line) and so would
end up loading wordpress through index.php. However, if we try the
supercache line first, we find the cache file and so don't need to load
indexes.

And just like that, magic, it works! We use supercache files for normal
users, and if a cache file doesn't exist, we load wordpress like normal!

I'm also looking at how we run Nginx and PHP-FPM. I have heard of a few
ways, one being that root runs a Nginx as user nginx or nobody, and each
user runs their own Nginx which we proxy to from the main one. (And
users run their own PHP-FPM as well). This sounds like a lot of work,
very complicated, but yes, it gives you absolute security as only the
user can access his web docs and scripts, and everything runs as that
user. No one else's php process can load your config file to discover
your database passwords.

Another way of running it is with Nginx as a nginx/nobody/www-data user,
and each user run their own php-fpm but give the nginx/nobody/www-data
user read only access to the web directory. If done correctly, this can
actually be very secure. First, (as root) you chgrp all the files and
directories in the users doc root (htdocs, www, public\_html etc) to the
user nginx will run as. Ideally, you also only allow them read access
(so \`chmod g+rX,g-w -R public\_html\` will give them access to read,
but not write). You then set the gid bit on the directory; \`chmod g+s
public\_html\` (and do this for any directories that already exist
underneath). Now any files the user creates underneath the public\_html
dir will be readable to the nginx user, so nginx can serve static files.
Now running php-fpm as each user (I use php-fpm with a pool per user),
the php process can read all the files that user can, so only the users
own php process can read their config files with the password in it! And
it also means that files you upload (i.e. wordpress media files) will be
owned by the user, not by www-data or what ever the web user is. This is
SO much better than Apache and mod\_php, and easier than suExec with
mod\_php.

Once I have more of my domains moved to Nginx, I'll do a report on
memory and cpu usage.
