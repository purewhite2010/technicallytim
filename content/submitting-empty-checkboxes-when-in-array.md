Title: Submitting Empty Checkboxes when in Array
Date: 2012-09-11 15:20
Author: Tim White
Category: Blog, Coding
Tags: array, checkboxes, empty, HTML, submit
Slug: submitting-empty-checkboxes-when-in-array

In HTML, we often use a nice feature for POSTing a form, or submitting a
form, where we have lots of items the "same". In the Grase Hotspot
project, we have groups for example, and we can dynamically add and
delete groups, but need a complete form for each group with it's
settings. So we use an "array" to submit the values. Simple put, we have
a number of \<inputs\> with the same name, but with square brackets on
the end. i.e. \<input type="text" name="groupprice[]"/\>, and we have
multiples of these. Thanks to page ordering, we can have a number of
different arrays as well, and can associate all the group values
together thanks to their positions in each array.

However, this breaks when we are submitting checkboxes, because
unchecked checkboxes won't submit. When unchecked, they are a form
element that isn't successful, and only successful form elements are
submitted. That's fine, except we are relying on the array behaviour to
match elements together, and when a checkbox isn't submitted, it doesn't
even take up an array position, it's just absent, which means all
following checkboxes on the page are now in the wrong spot in the array
and not matched with the other arrays.

So normally when we submit input fields and some items have been left
blank, they still consume a spot in the array, like so.

    :::php
    array(4) {
    [0]=>
    string(6) "Item 1"
    [1]=>
    string(0) ""
    [2]=>
    string(0) ""
    [3]=>
    string(6) "Item 4"
    }

However, the checkboxes (which have a value on On normally when
checked), would appear like so (with Item numbers instead of "On" for
clarity)

    :::php
    array(2) {
    [0]=>
    string(6) "Item 1"
    [1]=>
    string(6) "Item 4"
    }

There are solutions out there, however none work very well for dynamic
adding and creating "groups" of data, including checkboxes. Given that
the dynamic creation and deletion of those groups is with Javascript,
I've turned to a small javascript snippit to get it working. Hopefully
I'll find a nice way to have it fallback when javascript is disabled.

I found the solution I'm using at <http://www.dwright.us/?p=472> however
couldn't get it working well. A bit of fiddling and working on the
solution in the comments and I came up with the following snippit that
works nicely for me.

    :::js
    $(document).ready(function(){
        // do when submit is pressed
        $('form').submit(function() {

            $('input:checkbox:not(:checked)').each(function() {
                    console.log($(this).attr('name'));
                    $(this).before($('<input>')
                    .attr('class', '_temp')
                    .attr('type', 'hidden')
                    .attr('name', $(this).attr('name')));
                    // .val('off'));
            });  
        });

    });

One of the main things I changed (once I made it work) was not having it
set the "extra" inputs to the value of "Off", but leaving them as an
empty value. This is because in my code I run the incoming arrays
through array\_filter which removes all the empty ones (and maintains
the array indexes so the order and position is still there).
