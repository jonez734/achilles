<?php

define("SITEADMINEMAIL", "achilles <achilles@projects.zoidtechnologies.com>");

/**
 * define the base url for the site. THIS VALUE MUST BE TERMINATED WITH A "/"
 */
define("SITETITLE", "Project Achilles - What is the answer to life, the universe, and everything medicine?");
define("SITEURL", "http://achilles.zoidtechnologies.com/");
define("SITEKEYWORDS", "project achilles, monosodium glutamate, mono-sodium glutamate, msg, glutamate, disodium glutamate, truth in labeling, health, nutrition, consumer protection, food additives");
define("SITEDESCRIPTION", "Project Achilles studies the effects of monosodium glutamate on the human body");
define("SITETYPE", "website");
define("SKINURL", SITEURL . "skin/");
//define("SYSTEMDSN", "pgsql://apache@127.0.0.1/zoidweb3");
define("VHOSTDIR", "/srv/www/vhosts/achilles.zoidtechnologies.com/");
define("DOCUMENTROOT", VHOSTDIR . "html/");

define("IMAGESURL", "http://static.zoidtechnologies.com/");

define("SMARTYCOMPILEDTEMPLATESDIR", VHOSTDIR . "templates_c");
define("SMARTYPLUGINSDIR", VHOSTDIR . "smarty/");
define("SMARTYTEMPLATESDIR", VHOSTDIR."tmpl/");

define("LOGENTRYPREFIX", "achillesprod");

/*
 * @since 20190817
 * @since 20221104
 */
$includepath = get_include_path().":/srv/www/zoidweb4/php:/srv/www/bbsengine4/php";
if (set_include_path($includepath) === false)
{
    print("include path fail");
}
/**
 * @since 20200422
 * 3
 */
define("GOOGLEANALYTICSACCOUNT", "UA-23705021-1");

?>
