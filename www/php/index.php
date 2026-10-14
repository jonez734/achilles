<?php

require_once('/srv/www/bbsengine6/php/bootstrap.php');

require_once("config.php");

require_once("engine.php");
require_once("session.php");
require_once("database.php");

require_once("zoid6.php");
require_once("libvulcan.php");

class index
{
  function gethealthlinks()
  {
    return [];

    /* disabled 2026-10-13: vulcan.healthlinks query — dead code, never reached.
       preserved here so the SQL can be re-enabled once the vulcan link map
       is available. the function is hardcoded to return [] for now.
    $sql = "select elle.url from vulcan.link as elle, vulcan.map_link_sig as m where m.url = elle.url and m.path ~ 'top.achilles' order by elle.broken asc, lastmodified desc";

    $pdo = \bbsengine6\database\connect(\SYSTEMDSN);
    $dat = [];

    $stmt = $pdo->prepare($sql);
//    try {
      $stmt->execute($dat);
//    } catch (Exception $e) {
//      return null;
//    }
    if ($stmt->rowCount() == 0)
    {
      return [];
    }
    $res = $stmt->fetchAll();
    $healthlinks = [];
    foreach ($res as $rec)
    {
      $link = \vulcan\lib\getlinkbyurl($rec["url"]);
      $healthlinks[] = $link;
      if (\vulcan\lib\access("view", $link) === true)
      {
        $healthlinks[] = $link;
      }
    }
    return $healthlinks;
    */
  }

  function getsectionnames(): array
  {
      $directory = SECTIONTEMPLATEDIR;
      \bbsengine6\util\logentry("achilles.160: directory=".var_export($directory, true));
      $sections  = [];

      // Get all *.tmpl files
      foreach (glob($directory . "/*.tmpl") as $file) {
          $basename = basename($file);            // e.g. "metrics.tmpl"
          $name     = preg_replace('/\.tmpl$/', '', $basename);  // "metrics"
          $sections[] = $name;
      }

      sort($sections); // optional, but keeps things predictable

      return $sections;
  }

  function main(): void
  {
    \bbsengine6\session\start();
    
    \bbsengine6\setcurrentsite(defined('\config\SITENAME') ? \config\SITENAME : "NEEDINFO");
    \bbsengine6\setcurrentpage("index");
    \bbsengine6\setcurrentaction("view");
    \bbsengine6\setreturnto(\bbsengine6\getcurrenturi());

    $title = "achilles - a project to study manufactured free glutamic acid (aka monosodium glutamate (MSG)";

    $healthlinks = $this->gethealthlinks();

    $data = [];

    $data["healthlinks"] = $healthlinks;
    $data["pagetemplate"] = "index.tmpl"; // achilles-page.tmpl";

    $tmplpath = \bbsengine6\template\extra()[0] . "/index.tmpl";
    $data["lastmodified"] = file_exists($tmplpath) ? filemtime($tmplpath) : false;

    $choices = [];
    if (\bbsengine6\member\lib\checkflag("SYSOP"))
    {
      $choices[] = ["name" => "add link", "title" => "add link to achilles sig", "url" => TEOSURL."achilles/add-link", "desc" => "add link to achilles sig"];
    }
    $data["choices"] = \zoid6\buildchoices($choices);

    $sectionnames = $this->getsectionnames();
    \bbsengine6\util\logentry("achilles.120: sectionnames=".var_export($sectionnames, true));

    $sections = [];
    foreach ($sectionnames as $name) {
      $tmplpath = SECTIONTEMPLATEDIR . $name . ".tmpl";
      $open = false;
      if (file_exists($tmplpath)) {
        $tmplsrc = file_get_contents($tmplpath);
        if ($tmplsrc !== false && preg_match('/data-state\s*=\s*"open"/i', $tmplsrc) === 1) {
          $open = true;
        }
      }
      $sections[$name] = [
        'open' => $open,
        'lastmodified' => file_exists($tmplpath) ? filemtime($tmplpath) : false,
      ];
    }
//    \bbsengine6\util\logentry("----> achilles.100: sections=".var_export($sections, true));

    $data["sections"] = $sections;

    \bbsengine6\displaypage($data, "index.tmpl");
    \bbsengine6\util\logentry("achilles.100: ".var_export($data, true));
    return;
  }
};

//print("foo!");

$a = new index();
$a->main();
?>
