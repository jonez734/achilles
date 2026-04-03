<?php
require_once("config.php");
require_once("zoid6.php");
require_once("engine.php");

$smarty = \bbsengine6\getsmarty();

$name = $_GET['name'] ?? '';
// Security: allow only alphanumeric, underscores, and hyphens
$name = preg_replace('/[^a-zA-Z0-9_-]/', '', $name); 

$templatePath = "sections/${name}.tmpl";


// Check if the file exists within the smarty template directory
if (empty($name) || !$smarty->templateExists($templatePath)) 
{
    http_response_code(404);
    echo "Section content not found.";
    exit;
}

// Render only the partial template, not the whole page
$smarty->display($templatePath);
?>
