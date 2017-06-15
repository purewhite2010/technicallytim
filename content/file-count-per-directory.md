Title: File count for subdirectories
Date: 2017-06-15 09:55
Author: Tim White
Category: Technical
Tags: du, file count, bash
Slug: file-count-per-directory

Sometimes Google takes awhile to find the thing you are looking for. I currently have the need to find the recursive file count for all the directories in a directory. And then sort them.

There are lots of stackoverflow questions and answers to this, but most of them rely on the find command, fancy loops, etc. I found a nice elegant one liner that uses du, cut, sort and uniq. This works perfectly for me, is super quick, and much nicer to use IMHO

So here is that answer, so I can easily find it next time, and so hopefully others can find it too!

https://stackoverflow.com/a/39622947/682931
   :::bash
   du -a | cut -d/ -f2 | sort | uniq -c | sort -nr
