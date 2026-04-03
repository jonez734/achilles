<?php

require_once("PEAR.php");

require_once("config.php");
require_once("zoid6.php");
require_once("engine.php");
require_once("session.php");

function getsection($sectiontemplate)
{
    $res = null;

//    logentry("bed.getvar.100: var=".var_export($var, true));

    $tmpl = getsmarty();
    $data = [];
    $data["fragment"] = $tmpl->fetch($sectiontemplate);
    return $data;
}

\bbsengine6\session\start();

function getsectiontemplates($directory = "skin/tmpl/sections") 
{
  $files = glob($directory . '/*.tmpl'); // Get all .tmpl files in the directory
  return $files;
}

$section = isset($_REQUEST["section"]) ? $_REQUEST["section"] : null;
$res = getsection($section);
if (PEAR::isError($res))
{
    logentry("achilles.bed.100: var=".var_export($var, true)." ". $res->toString());
    $res = ["fragment" => "<b>error</b>"];
//    print encodejson($res);
//    exit(1);
}

$encoded = \bbsengine6\encodejson($res);
if (isset($_REQUEST["callback"]))
{
  header('Content-type: text/javascript'); // text/plain
//              logentry("bed.php.100: callback exists");
  $output = $_REQUEST["callback"]."({$encoded})";
  print $output;
//              logentry("bed.php.120: output=".var_export($output, true));
}
else
{
  header("Content-type: application/json");
  logentry("bed.php.110: using json (no callback)");
  print $encoded;
}
?>
