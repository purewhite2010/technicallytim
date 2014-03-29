Title: Wordpress to Pelican
Date: 2014-03-29
Author: Tim White
Category: Blog
Tags: wordpress, pelican
Slug: wordpress-to-pelican

It's been a while since I last blogged. Since then, I've started a full time job
as a Systems Administrator. This means I have less time for maintaining my own
servers. So I've finally taken the plunge migrating some of the more static
sites to static. For example this Technical blog will now be a static site. 
This doesn't mean it won't get updated, this just means that it's generated with
a static generator instead of being generated dynamically when someone views the
page. This results in lower server load, as it doesn't need PHP running, or a 
database. It results in faster page loads. It results in a more secure server as
it's just running a webserver and no web application.

I believe it results in blogs that are more focused on content than on the web
application that displays the content.

I've choosen to use [Pelican](https://github.com/getpelican/pelican), mostly
because I've enjoyed learning Python over the last year, and this gives me 
another excuse to play with some Python. I'm also more comfortable in Python than
some of the other options so this allows me to hack away on the code if I want to.

Regarding the current lack of comments on the blog. I'm still thinking of the best
way to handle that. I may just put a Google+ comments plugin on, as I really
don't like Disqus. I may also just not put dynamic comments on and use Github issues
for discussing posts as some others have done.
