<?php

namespace achilles\database;

define("ACHILLES_DSN", "pgsql:host=127.0.0.1;port=5432;dbname=achilles");

function connect()
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

function fooditemSelect(?int $id = null): ?array
{
  $pdo = connect();

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

function fooditemInsert(array $data): ?int
{
  $pdo = connect();

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
    error_log('achilles.database.fooditemInsert: ' . $e->getMessage());
    return null;
  }
}

function fooditemUpdate(int $id, array $data): bool
{
  $pdo = connect();

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
    error_log('achilles.database.fooditemUpdate: ' . $e->getMessage());
    return false;
  }
}

function fooditemDelete(int $id): bool
{
  $pdo = connect();

  $sql = "DELETE FROM achilles.__fooditem WHERE id = :id";

  try
  {
    $stmt = $pdo->prepare($sql);
    $stmt->execute(['id' => $id]);
    return $stmt->rowCount() > 0;
  }
  catch (\Throwable $e)
  {
    error_log('achilles.database.fooditemDelete: ' . $e->getMessage());
    return false;
  }
}

function fooditemSearch(string $term): array
{
  $pdo = connect();

  $sql = "SELECT * FROM achilles.fooditem WHERE name ILIKE :term OR description ILIKE :term OR upc ILIKE :term ORDER BY name";
  $stmt = $pdo->prepare($sql);
  $stmt->execute(['term' => '%' . $term . '%']);
  return $stmt->fetchAll();
}