<?php

require_once('/srv/www/bbsengine6/php/bootstrap.php');
require_once('util.php');
\bbsengine6\util\add_include_paths(['/srv/www/zoid6/php/', '/srv/www/bbsengine6/php/', '/srv/www/smarty/']);

// Define configuration constants in config namespace (required by bbsengine6)
// Using backslash prefix makes them accessible via defined('\config\CONSTANT')
define("config\SITENAME", "achilles");
define("config\SITEADMINEMAIL", "achilles <achilles@projects.zoidtechnologies.com>");
define("config\SITETITLE", "Project Achilles - A study of the affects of flavor enhancers on health");
define("config\SITEURL", "/achilles/");
define("config\SITEKEYWORDS", "project achilles, monosodium glutamate, mono-sodium glutamate, msg, glutamate, disodium glutamate, truth in labeling, health, nutrition, consumer protection, food additives");
define("config\SITEDESCRIPTION", "Project Achilles studies the affects of flavor enhancers on health");
define("config\VHOSTDIR", "/srv/www/vhosts/zoidtechnologies.com/");
define("config\DOCUMENTROOT", \config\VHOSTDIR . "html/achilles/");
define("config\SKINDIR", \config\DOCUMENTROOT . "skin/");
define("config\SKINURL", \config\SITEURL . "skin/");
define("config\JSURL", "/achilles/skin/js/");

// @since 2026-09-24 — load zoid6config.php first (which transitively
// loads bbsengine6config.php, defining config\SHAREDTMPLDIR) before
// the SMARTY* defines that reference \config\SHAREDTMPLDIR.
require_once('zoid6config.php');

// SMARTYTEMPLATESDIR - 2-element array (bbsengine6/skin/tmpl/ is
// auto-appended by bbsengine6config.php as the engine fallback).
// Search order: 1) Site-specific templates 2) shared zoid6 templates
define("config\SMARTYTEMPLATESDIR", [
    0 => \config\SKINDIR . "tmpl/",
    1 => \config\SHAREDTMPLDIR,
]);

// SMARTYCOMPILEDTEMPLATESDIR - compiled template cache directory
define("config\SMARTYCOMPILEDTEMPLATESDIR", \config\VHOSTDIR . "templates_c");

// SMARTYPLUGINSDIR - plugin directories for custom Smarty functions and modifiers
define("config\SMARTYPLUGINSDIR", [
    0 => \config\VHOSTDIR . "smarty/",
    1 => "/srv/www/zoid6/smarty/"
]);

define("config\LOGENTRYPREFIX", "zoid6achilles");
define("config\ENGINEURL", "/engine/");
define("config\ENGINESKINURL", "/engine/skin/");
define("config\SHAREDSKINURL", "/shared/skin/");
define("config\GOOGLEANALYTICSACCOUNT", "UA-23705021-1");
define("config\SECTIONTEMPLATEDIR", \config\SKINDIR . "tmpl/sections/");

// Create global aliases for non-SMARTY constants
// (SMARTY* aliases are created by zoid6config.php)
define("SITEURL", \config\SITEURL);
define("VHOSTDIR", \config\VHOSTDIR);
define("DOCUMENTROOT", \config\DOCUMENTROOT);
define("SKINDIR", \config\SKINDIR);
define("SKINURL", \config\SKINURL);
define("JSURL", \config\JSURL);
define("ENGINEURL", \config\ENGINEURL);
define("ENGINESKINURL", \config\ENGINESKINURL);
define("SHAREDSKINURL", \config\SHAREDSKINURL);
define("STATICSKINURL", \config\SHAREDSKINURL); // Alias for backward compat
define("LOGENTRYPREFIX", \config\LOGENTRYPREFIX);
define("SECTIONTEMPLATEDIR", \config\SECTIONTEMPLATEDIR);

?>
