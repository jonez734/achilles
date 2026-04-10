<?php

require_once("config.php");
require_once("achilles.php");
require_once("database.php");
require_once("engine.php");
require_once("session.php");
require_once("util.php");
require_once("page.php");

use achilles\database as achillesdb;

class fooditem
{
  function insert($values)
  {
    if (!\bbsengine6\util\csrfCheckRequest())
    {
      $remoteAddr = isset($_SERVER['REMOTE_ADDR']) ? $_SERVER['REMOTE_ADDR'] : 'unknown';
      $userAgent = isset($_SERVER['HTTP_USER_AGENT']) ? $_SERVER['HTTP_USER_AGENT'] : 'unknown';
      \bbsengine6\util\logentry("CSRF validation failed for fooditem.insert: ip={$remoteAddr}, user_agent={$userAgent}");
      \bbsengine6\page\error("Invalid security token. Please try again (code: fooditem.insert.csrf)");
      return false;
    }

    $fooditem = buildfooditemrecord($values);
    $fooditem["dateposted"] = date('Y-m-d H:i:s');
    $fooditem["postedbymoniker"] = \bbsengine6\member\lib\getcurrentmoniker();

    $id = \achilles\database\fooditemInsert($fooditem);

    if ($id === null)
    {
      \bbsengine6\page\error("Failed to insert fooditem");
      return false;
    }

    $page = array();
    $page["body"] = "<p style='color: white;'>Food item added successfully! ID: " . $id . "</p>";

    print \bbsengine6\util\encodejson(array("page" => $page));
    return;
  }

  function add()
  {
    \bbsengine6\setcurrentaction("add");

    $form = \bbsengine6\getquickform("achilles-fooditem-add");

    buildfooditemfieldset($form);

    $form->addElement("submit", "blah", ["value" => "add fooditem"]);

    if (accessfooditem("add") === false)
    {
      \bbsengine6\util\logentry("fooditem.add.12: accessfooditem check failed.");
      \bbsengine6\page\permissiondenied();
      return;
    }

    $currentmoniker = \bbsengine6\member\lib\getcurrentmoniker();

    $defaults = [];

    $form->addDataSource(new HTML_QuickForm2_DataSource_Array($defaults));

    $const = [];
    $const["mode"] = "add";
    $const["moniker"] = $currentmoniker;

    $form->addDataSource(new HTML_QuickForm2_DataSource_Array($const));

    $res = \bbsengine6\handleform($form, array($this, "insert"), "add fooditem");
    if ($res === true)
    {
      \bbsengine6\util\logentry("achilles.fooditem.add.102: handleform(...) returned true");
      return true;
    }

    $renderer = \bbsengine6\getquickformrenderer();
    $form->render($renderer);

    $res = \bbsengine6\displayform($renderer, "add fooditem");
    if (PEAR::isError($res))
    {
      \bbsengine6\util\logentry("achilles.fooditem.add.101: " . $res->toString());
    }
    return $res;
  }

  function main()
  {
    \bbsengine6\session\start();
    \bbsengine6\setcurrentsite("achilles");
    \bbsengine6\setcurrentpage("fooditem");

    $mode = isset($_REQUEST["mode"]) ? $_REQUEST["mode"] : null;

    switch ($mode)
    {
      case "add":
      {
        $res = $this->add();
        break;
      }
      default:
      {
        $res = PEAR::raiseError("invalid mode" . var_export($mode, true));
        break;
      }
    }

    return $res;
  }
};

$a = new fooditem();
$b = $a->main();
if (PEAR::isError($b))
{
  \bbsengine6\page\error($b->getMessage());
  \bbsengine6\util\logentry("fooditem.1000: " . $b->toString());
  exit;
}

?>
