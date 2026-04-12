<?php

namespace {

define("ACHILLES_DSN", "pgsql:host=127.0.0.1;port=5432;dbname=achilles");

function achilles_db_connect()
{
  static $pdo = null;

  if ($pdo !== null)
  {
    return $pdo;
  }

  $options = [
    \PDO::ATTR_ERRMODE            => \PDO::ERRMODE_EXCEPTION,
    \PDO::ATTR_DEFAULT_FETCH_MODE => \PDO::FETCH_ASSOC,
    \PDO::ATTR_EMULATE_PREPARES   => false,
  ];

  $user = getenv('DB_USER') ?: 'bbsengine';
  $pass = getenv('DB_PASS') ?: '';

  try {
    $pdo = new \PDO(ACHILLES_DSN, $user, $pass, $options);
  } catch (\PDOException $e) {
    error_log('Achilles database connection error: ' . $e->getMessage());
    throw $e;
  }

  return $pdo;
}

function achilles_fooditem_select(?int $id = null): ?array
{
  $pdo = achilles_db_connect();

  if ($id !== null)
  {
    $sql = "SELECT * FROM achilles.fooditem WHERE id = :id";
    $stmt = $pdo->prepare($sql);
    $stmt->execute(['id' => $id]);
    $result = $stmt->fetch();
    return $result ?: null;
  }

  $sql = "SELECT * FROM achilles.fooditem ORDER BY dateposted DESC";
  $stmt = $pdo->query($sql);
  return $stmt->fetchAll();
}

function achilles_fooditem_insert(array $data): ?int
{
  $pdo = achilles_db_connect();

  $columns = [
    'upc', 'sku', 'lot', 'serial', 'name', 'title', 'description',
    'brandid', 'manufid', 'qsr', 'msgpresent', 'msgonlabel',
    'dsgpresent', 'dsgonlabel', 'frozen', 'wic', 'price',
    'quantity', 'producturl', 'datepurchased', 'dateposted',
    'postedbymoniker'
  ];

  $validColumns = [];
  $values = [];

  foreach ($columns as $col)
  {
    if (array_key_exists($col, $data))
    {
      $validColumns[] = $col;
      $values[$col] = $data[$col];
    }
  }

  if (empty($validColumns))
  {
    return null;
  }

  $sql = "INSERT INTO achilles.__fooditem(" . implode(', ', $validColumns) . ") VALUES (:" . implode(', :', $validColumns) . ") RETURNING id";

  try
  {
    $stmt = $pdo->prepare($sql);
    $stmt->execute($values);
    $result = $stmt->fetch();
    return $result['id'] ?? null;
  }
  catch (\Throwable $e)
  {
    error_log('achilles.fooditem_insert: ' . $e->getMessage());
    return null;
  }
}

function achilles_fooditem_update(int $id, array $data): bool
{
  $pdo = achilles_db_connect();

  $columns = [
    'upc', 'sku', 'lot', 'serial', 'name', 'title', 'description',
    'brandid', 'manufid', 'qsr', 'msgpresent', 'msgonlabel',
    'dsgpresent', 'dsgonlabel', 'frozen', 'wic', 'price',
    'quantity', 'producturl', 'datepurchased', 'datemodified',
    'modifiedbymoniker'
  ];

  $setParts = [];
  $values = [];

  foreach ($data as $key => $value)
  {
    if (in_array($key, $columns))
    {
      $setParts[] = "$key = :$key";
      $values[$key] = $value;
    }
  }

  if (empty($setParts))
  {
    return false;
  }

  $values['id'] = $id;

  $sql = "UPDATE achilles.__fooditem SET " . implode(', ', $setParts) . " WHERE id = :id";

  try
  {
    $stmt = $pdo->prepare($sql);
    $stmt->execute($values);
    return $stmt->rowCount() > 0;
  }
  catch (\Throwable $e)
  {
    error_log('achilles.fooditem_update: ' . $e->getMessage());
    return false;
  }
}

function achilles_fooditem_delete(int $id): bool
{
  $pdo = achilles_db_connect();

  $sql = "DELETE FROM achilles.__fooditem WHERE id = :id";

  try
  {
    $stmt = $pdo->prepare($sql);
    $stmt->execute(['id' => $id]);
    return $stmt->rowCount() > 0;
  }
  catch (\Throwable $e)
  {
    error_log('achilles.fooditem_delete: ' . $e->getMessage());
    return false;
  }
}

function achilles_fooditem_search(string $term): array
{
  $pdo = achilles_db_connect();

  $sql = "SELECT * FROM achilles.fooditem WHERE name ILIKE :term OR description ILIKE :term OR upc ILIKE :term ORDER BY name";
  $stmt = $pdo->prepare($sql);
  $stmt->execute(['term' => '%' . $term . '%']);
  return $stmt->fetchAll();
}

}

namespace {

require_once("config.php");
require_once("achilles.php");
require_once("engine.php");
require_once("session.php");
require_once("util.php");

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

    $id = \achilles_fooditem_insert($fooditem);

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

}