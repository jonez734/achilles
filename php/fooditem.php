<?php

require_once("config.php");
require_once("achilles.php");
require_once("zoidweb4.php");
require_once("bbsengine4.php");

class fooditem
{
  function insert($values)
  {
    $fooditem = buildfooditemrecord($values);
    
    $page = array();
    $page["body"] = "<pre style='color: white;'>".var_export($fooditem, True)."</pre>";
    
    print encodejson(array("page" => $page));
    return;
  }

  function add()
  {
    setcurrentaction("add");

    $form = getquickform("achilles-fooditem-add");

    buildfooditemfieldset($form);

    $form->addElement("submit", "blah", ["value" => "add fooditem"]);

    if (accessfooditem("add") === False)
    {
      logentry("fooditem.add.12: accessfooditem check failed.");
      displaypermissiondenied();
      return;
    }

    $currentmemberid = getcurrentmemberid();

    $defaults = [];
    
    /*
    if (flag("ADMIN") === True)
    {
      $defaults["approved"] = True;
      $defaults["dateapproved"] = "now()";
      $defaults["approvedbyid"] = $currentmemberid;
    }
    */
    $form->addDataSource(new HTML_QuickForm2_DataSource_Array($defaults));

    $const = [];
    $const["mode"] = "add";
    $const["memberid"] = $currentmemberid;

    $form->addDataSource(new HTML_QuickForm2_DataSource_Array($const));
    
    $res = handleform($form, array($this, "insert"), "add fooditem");
    if ($res === True)
    {
      logentry("achilles.fooditem.add.102: handleform(...) returned True");
      return True;
    }

    $renderer = getquickformrenderer();
    $form->render($renderer);

    $res = displayform($renderer, "add fooditem");
    if (PEAR::isError($res))
    {
      logentry("achilles.fooditem.add.101: " . $res->toString());
    }
    return $res;
  }

  function main()
  {
    startsession();
    
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
        $res = PEAR::raiseError("invalid mode" . var_export($mode, True));
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
  displayerrorpage($b->getMessage());
  logentry("fooditem.1000: " . $b->toString());
  exit;
}

?>
