<?php

/*
 * functions specific to project achilles
 */

function buildfooditemfieldset($form)
{
  $fieldset = $form->addElement("fieldset")->setLabel("Food Item");
  $fieldset->addText("name", "size=60")->setLabel("Name")->addRule("required", "'Name' is a required field");
  $fieldset->addElement("textarea", "description", "rows=15 cols=70")->setLabel("Description")->addRule("required", "'Description' is a required field");
  $fieldset->addText("brand", "size=60")->setLabel("Brand");
  $fieldset->addCheckbox("qsr")->setLabel("Quick Service Restaurant (Fast Food)?");
  $fieldset->addText("price", "size=10")->setLabel("Price");
  $fieldset->addCheckbox("msgpresent")->setLabel("MSG Present?");
  $fieldset->addCheckbox("msgonlabel")->setLabel("MSG clearly shown on label?");
  $fieldset->addText("datepurchased")->setLabel("Date Purchased");
  $fieldset->addText("locationpurchased")->setLabel("Location Purchased");
  $fieldset->addText("upc")->setLabel("UPC");
  $fieldset->addFile("upclabelimage", ["accept" => "image/*", "capture" => "camera"])->setLabel("photo of upc label");
  $fieldset->addElement("textarea", "ingredients", "rows=15 cols=70")->setLabel("Ingredients");
  $fieldset->addFile("ingredientsimage", ["accept" => "image/*", "capture" => "camera"])->setLabel("photo of ingredients list");
  $fieldset->addText("nutritionguideurl")->setLabel("Link to nutrition guide");
  $fieldset->addText("msgquantity")->setLabel("Quantity of MSG");
  return;
}

function buildfooditemrecord($values)
{
  $fooditem = array();
  $fooditem["name"] = $values["name"];
  $fooditem["description"] = $values["description"];
  $fooditem["brand"] = $values["brand"];
  $fooditem["qsr"] = isset($values["qsr"]) ? True : False;
  $fooditem["price"] = $values["price"];
  $fooditem["msgpresent"] = isset($values["msgpresent"]) ? True : False;
  $fooditem["msgonlabel"] = isset($values["msgonlabel"]) ? True : False;
  $fooditem["datepurchased"] = $values["datepurchased"];
  $fooditem["upc"] = $values["upc"];
  
  return $fooditem;
}

function accessfooditem($op, $fooditem=[])
{
  if ($op === "add")
  {
    if (flag("AUTHENTICATED") === true)
    {
      return true;
    }
  }
  return false;
}
?>
