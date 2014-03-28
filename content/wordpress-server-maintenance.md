Title: Wordpress Server Maintenance
Date: 2013-04-25 14:00
Author: tim
Category: Blog, Coding
Tags: security, updates, wordpress, wp-cli
Slug: wordpress-server-maintenance

Wow. Somehow I missed when this amazing tool was released. [wp-cli][].
Just wow.

I have a bunch of scripts I use to keep all the Wordpress installs up to
date on my server, it finds all the installs, then it downloads the
latest version, checks each install for the installed version and
updates them by extracting the files correctly, ensuring user
permissions etc. However, that only keeps the core updated, I still need
to rely on all my customers to keep their plugins updated. This is ok,
except when a plugin has a security issue and needs to be updated ASAP.
Recently, we had just that situation with the WP-Super-Cache plugin. So
I modified my scripts, and now they update that particular plugin. But
it would be a pain to write a script that updated every plugin, so I'm
stuck logging into a number of sites I maintain, updating all the
plugins regularly, and then hoping for the sites that the customer
maintains, they do the same.

Enter, [wp-cli][]. The tool I've been dreaming of for a long time.
Simply install, then using the basic structure of my script (the part
that finds all installs, verifies they are valid installs, and executes
commands as the user who owns the install), I can now run any of the
awesome [wp-cli][] commands on all the sites I host! Server maintenance
just got a whole lot easier (as long as no plugin updates break things)

For the really lazy, here is my code for updating all plugins, using the
wp-cli scripts. It uses sudo, so make sure you know what you are doing.
You may also have to tweak how locate finds things, as by default it
won't show you files you can't access.

~~~~ {lang="bash"}
#!/bin/bash

# Just find all installs and try and run tools in them
# find wp-config.php files
SAVEIFS=$IFS
IFS=$(echo -en "\n\b")
installs=$(locate -r wp-config.php$)

for conffile in $installs
do
# goto root wp dir as user
    wpdir=$(dirname "$conffile");
    pushd $wpdir > /dev/null || exit
    
    echo "Checking $wpdir..."
    
    ## Check we actually have a wordpress install
    
    if [[ ! -f "wp-includes/version.php" || ! -f $conffile ]]
        then echo "$wpdir doesn't appear to be a wordpress install, skipping..."
        continue
    fi
    
    # Get username for tool
    username=$(stat -c %U $conffile)
    
    # run tool commands
    sudo -u $username -- wp plugin update-all
    
    popd > /dev/null
done
~~~~

  [wp-cli]: http://wp-cli.org/ "wp-cli"
