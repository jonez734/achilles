<?php

require_once("config.php");
require_once("engine.php");
require_once("session.php");
require_once("database.php");

class index
{
  function gethealthlinks()
  {
    $sql = "select id, broken, lastmodified from vulcan.link, vulcan.map_link_sig where vulcan.map_link_sig.linkid = vulcan.link.id and vulcan.map_link_sig.siglabelpath ~ 'top.achilles' order by vulcan.link.broken asc, lastmodified desc";

    $pdo = \bbsengine6\database\connect(SYSTEMDSN);
    $dat = [];
    $stmt = $pdo->prepare($sql);
    try {
      $stmt->execute($dat);
    } catch (Exception $e) {
      return [];
    }
    return $stmt->fetch();

    $dbh = \bbsengine6\database\connect(SYSTEMDSN);
    if (PEAR::isError($dbh))
    {
      logentry("index.200: " . $dbh->toString());
      return null;
    }
//    $sql = "select id from vulcan.link where sigpath ~ 'top.achilles' order by lastmodified desc";
    $sql = "select id, broken, lastmodified from vulcan.link, vulcan.map_link_sig where vulcan.map_link_sig.linkid = vulcan.link.id and vulcan.map_link_sig.siglabelpath ~ 'top.achilles' order by vulcan.link.broken asc, lastmodified desc";
    $res = $dbh->getAll($sql, array("integer"));
    if (PEAR::isError($res))
    {
      logentry("index.202: " . $res->toString());
      return null;
    }

    $healthlinks = [];
    $count = 0;
    foreach ($res as $rec)
    {
      $id = isset($rec["id"]) ? intval($rec["id"]) : null;
      $link = getlinkbyid($id);
      if (PEAR::isError($link))
      {
        logentry("index.204: " . $link->toString());
        continue;
      }
      if (accesslink("view", $link) === True)
      {
/*
        if ($count == 5)
        {
          break;
        }
*/
        $healthlinks[] = $link;
        $count++;
      }
    }
    return $healthlinks;
  }

  function main()
  {
    \bbsengine6\session\start();
    
    \bbsengine6\setcurrentsite("achilles");
    \bbsengine6\setcurrentpage("index");
    \bbsengine6\setcurrentaction("view");
    \bbsengine6\setreturnto(\bbsengine6\getcurrenturi());
//    \bbsengine6\clearpageprotocol();

    $title = "achilles - a project to study manufactured free glutamic acid (aka monosodium glutamate (MSG)";

//    $page = \bbsengine6\getpage($title);
    $healthlinks = $this->gethealthlinks();

//    $tmpl = getsmarty();
//    $tmpl->assign("healthlinks", $healthlinks);

    $data = [];

    $metadata = [];
/*
    $metadata["og:description"] = "Project Achilles studies the effects of manufactured free glutamic acid (aka mono-sodium glutamate and MSG) on the human immune system";
    $metadata["og:title"] = $title;
    $metadata["og:type"] = "website";
    $metadata["og:url"] = 'http:'.ACHILLESURL;
    $metadata["keywords"] = "project achilles, manufactured free glutamic acid, monosodium glutamate, msg, nutrition, health, diet";
    $metadata["Generator"] = "PEAR HTML_Page2 via bbsengine4";
*/
    $data["healthlinks"] = $healthlinks;
    $data["metadata"] = $metadata;
    $data["pagetemplate"] = "index.tmpl"; // achilles-page.tmpl";

    $sidebar = [];
    if (\bbsengine6\flag("ADMIN"))
    {
      $sidebar[] = ["name" => "add link", "title" => "add link to achilles sig", "url" => TEOSURL."achilles/add-link", "desc" => "add link to achilles sig"];
    }
    $data["sidebar"] = $sidebar;

    \bbsengine6\displaypage($data);
    return;
  }
};

//print("foo!");

$a = new index();
$b = $a->main();
if (PEAR::isError($b))
{
  logentry("index.100: " . $b->toString());
  displayerrorpage($b->getMessage());
  exit;
}
?>
