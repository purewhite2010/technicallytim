Title: Wordpress Media in Google Cloud Storage
Date: 2015-10-05
Author: Tim White
Category: Blog
Tags: wordpress,google cloud storage,s3,media
Slug: wordpress-google-cloud-storage

One of the big challenges with Wordpress in the cloud, is the media we upload.
As soon as we upload media files, the Wordpress instance has data that isn't
stored in the database. This prevents us for example having a docker Wordpress
install that we can scale up as required, without some method for syncronising
the wp-content/uploads directory. [WP2Cloud](https://wordpress.org/plugins/wp2cloud-wordpress-to-cloud/)
solves this with the ClouSE storage engine, that attaches to MySQL. Without the Clouse storage
engine, the plugin is dead in the water. Which is really sad, because it
supports Amazon S3, and Google Cloud Storage.

Then there are a number of different plugins available that try to solve this
issue, some with Amazon S3 support, others with Google Drive support, and
others with OpenStack's Object Storage, Swift.

However, very little properly supports Google Cloud Storage, which is different 
from Google Drive. Why do I care about Google Cloud Storage? Firstly, it's
cheaper than Amazon S3. Secondly, I have a number of other business solutions
with Google, and sometimes keeping things together makes it easier. Lastly,
because no one seems to be doing, so lets try!

Initially, I thought I'd have to write an entire plugin myself. Thankfully,
some plugins are GPLed so I can look at the code and get an idea of what I need
for a basic plugin. And then, I stumbled upon the Golden Key.
[Migrating from Amazon S3 to Google Cloud Storage](https://cloud.google.com/storage/docs/migrating).
Google has done something that I had hoped, but hadn't found in my initial
searches. They support the Amazon S3 XML API!

The original [Amazon S3 for WordPress plugin by
tantan](https://wordpress.org/plugins/tantan-s3/) hadn't been updated since
2009. But it was forked, which was also then forked, and now we have
[WP Offload S3](https://wordpress.org/plugins/amazon-s3-and-cloudfront/) which
claims to be completely rewritten. Looking at the tantan-s3 code, it may have
been easier for me to start with that. However, the WP Offload S3 plugin uses
what I believe are official AWS PHP libraries. It's also a recently updaded
plugin.

After about 30 minutes playing around with S3, Google Cloud Storage, and the WP
Offload S3 plugin (and the associated [Amazon Web
Services](https://wordpress.org/plugins/amazon-web-services/) plugin), I was
able to get it uploading to Google Cloud Storage, over the S3 API! The main
battle was getting it to communicate with Google's endpoint, instead of
Amazon's endpoint. One of the big differences between Amazon and Google, is
that Amazon's endpoints are dependent on the region you are using. Google
appears to have a single endpoint, which they presumably route to your closest
Google datacentre.

2 Small Patches
[here](https://github.com/timwhite/wp-amazon-s3-and-cloudfront/commit/8b55698c8e937a585646d8ecd0682db088c8dc76)
and
[here](https://github.com/timwhite/wp-amazon-web-services/commit/56cc81e58894150e5e8e89a3f59e25458d956080)
and I now have an Amazon S3 plugin uploading to Google instead of Amazon!

And, as a bonus, if you've read this far, and you are applying this to an
existing site. You *can* upload existing media with the S3 plugin. All media
libraries have an entry in the wp_posts table with post_type set to attachment.
If you fetch all the ID's for the items you wish to upload, and have the handy
wp-cli.org tool installed, it's as simple as running the following tool for
each ID, in this case the media item ID is 7.
```php
wp eval 'do_action('wp_update_attachment_metadata', null, 7);'
```

For reference, those above patches are also here:
```diffc81e58894150e5e8e89a3f59e25458d956080 Mon Sep 17 00:00:00 2001
From: Tim White <tim@whiteitsolutions.com.au>
Date: Mon, 5 Oct 2015 13:23:28 +1000
Subject: [PATCH] Changes for using Google Cloud Storage instead of Amazon S3

---
 vendor/aws/Aws/Common/Client/ClientBuilder.php       | 2 +-
 vendor/aws/Aws/Common/Resources/public-endpoints.php | 3 +++
 vendor/aws/Aws/S3/Resources/s3-2006-03-01.php        | 7 ++++++-
 3 files changed, 10 insertions(+), 2 deletions(-)

diff --git a/vendor/aws/Aws/Common/Client/ClientBuilder.php
b/vendor/aws/Aws/Common/Client/ClientBuilder.php
index 34647e9..1e900ac 100644
--- a/vendor/aws/Aws/Common/Client/ClientBuilder.php
+++ b/vendor/aws/Aws/Common/Client/ClientBuilder.php
@@ -446,7 +446,7 @@ private function handleRegion(Collection $config)
                 'A region is required when using ' .
$description->getData('serviceFullName')
             );
         } elseif ($global && !$region) {
-            $config[Options::REGION] = 'us-east-1';
+            $config[Options::REGION] = 'global';
         }
     }
 
diff --git a/vendor/aws/Aws/Common/Resources/public-endpoints.php
b/vendor/aws/Aws/Common/Resources/public-endpoints.php
index d939f1f..122a02c 100644
--- a/vendor/aws/Aws/Common/Resources/public-endpoints.php
+++ b/vendor/aws/Aws/Common/Resources/public-endpoints.php
@@ -54,6 +54,9 @@
         'us-east-1/s3' => array(
             'endpoint' => 's3.amazonaws.com'
         ),
+        'global/s3' => array(
+            'endpoint' => 'storage.googleapis.com'
+        ),
         'us-west-1/s3' => array(
             'endpoint' => 's3-{region}.amazonaws.com'
         ),
diff --git a/vendor/aws/Aws/S3/Resources/s3-2006-03-01.php
b/vendor/aws/Aws/S3/Resources/s3-2006-03-01.php
index 5699058..d9af677 100644
--- a/vendor/aws/Aws/S3/Resources/s3-2006-03-01.php
+++ b/vendor/aws/Aws/S3/Resources/s3-2006-03-01.php
@@ -21,10 +21,15 @@
     'serviceAbbreviation' => 'Amazon S3',
     'serviceType' => 'rest-xml',
     'timestampFormat' => 'rfc822',
-    'globalEndpoint' => 's3.amazonaws.com',
+    'globalEndpoint' => 'storage.googleapis.com',
     'signatureVersion' => 's3',
     'namespace' => 'S3',
     'regions' => array(
+        'global' => array(
+            'http' => true,
+            'https' => true,
+            'hostname' => 'storage.googleapis.com',
+        ),
         'us-east-1' => array(
             'http' => true,
             'https' => true,
```

```diff
From 8b55698c8e937a585646d8ecd0682db088c8dc76 Mon Sep 17 00:00:00 2001
From: Tim White <tim@whiteitsolutions.com.au>
Date: Mon, 5 Oct 2015 13:12:25 +1000
Subject: [PATCH] Minor changes to make it work with Google Cloud Storage
 instead

---
 classes/amazon-s3-and-cloudfront.php | 8 ++++----
 view/domain-setting.php              | 4 ++--
 2 files changed, 6 insertions(+), 6 deletions(-)

diff --git a/classes/amazon-s3-and-cloudfront.php
b/classes/amazon-s3-and-cloudfront.php
index c0553d2..b3f62b2 100644
--- a/classes/amazon-s3-and-cloudfront.php
+++ b/classes/amazon-s3-and-cloudfront.php
@@ -55,7 +55,7 @@ class Amazon_S3_And_CloudFront extends AWS_Plugin_Base {
    const DEFAULT_ACL = 'public-read';
    const PRIVATE_ACL = 'private';
    const DEFAULT_EXPIRES = 900;
-   const DEFAULT_REGION = 'us-east-1';
+   const DEFAULT_REGION = 'global';
 
    const SETTINGS_KEY = 'tantan_wordpress_s3';
 
@@ -998,7 +998,7 @@ function get_file_prefix( $time = null, $post_id = null ) {
     * @return string
     */
    function get_s3_url_prefix( $region = '', $expires = null ) {
-       $prefix = 's3';
+       $prefix = 'storage';
 
        if ( '' !== $region ) {
            $delimiter = '-';
@@ -1046,10 +1046,10 @@ function get_s3_url_domain( $bucket, $region = '',
$expires = null, $args = arra
            $s3_domain = $bucket;
        }
        elseif ( 'path' === $args['domain'] || $this->use_ssl( $args['ssl'] ) )
{
-           $s3_domain = $prefix . '.amazonaws.com/' . $bucket;
+           $s3_domain = $prefix . '.googleapis.com/' . $bucket;
        }
        else {
-           $s3_domain = $bucket . '.' . $prefix . '.amazonaws.com';
+           $s3_domain = $bucket . '.' . $prefix . '.googleapis.com';
        }
 
        return $s3_domain;
diff --git a/view/domain-setting.php b/view/domain-setting.php
index 44019c3..266fef4 100644
--- a/view/domain-setting.php
+++ b/view/domain-setting.php
@@ -21,12 +21,12 @@
            <label class="subdomain-wrap <?php echo $subdomain_class; // xss
ok?>">
                <input type="radio" name="domain" value="subdomain" <?php
checked( $domain, 'subdomain' ); ?> <?php echo $subdomain_disabled; // xss ok
?>>
                <?php _e( 'Bucket name as subdomain',
'amazon-s3-and-cloudfront' ); ?>
-               <p>http://bucket-name.s3.amazon.com/&hellip;</p>
+               <p>http://bucket-name.storage.googleapis.com/&hellip;</p>
            </label>
            <label>
                <input type="radio" name="domain" value="path" <?php checked(
$domain, 'path' ); ?>>
                <?php _e( 'Bucket name in path', 'amazon-s3-and-cloudfront' );
?>
-               <p>http://s3.amazon.com/bucket-name/&hellip;</p>
+               <p>http://storage.googleapis.com/bucket-name/&hellip;</p>
            </label>
            <label>
                <input type="radio" name="domain" value="virtual-host" <?php
checked( $domain, 'virtual-host' ); ?>>
```
