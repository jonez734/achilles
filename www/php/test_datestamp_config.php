<?php
/**
 * test_datestamp_config.php — Verifies the achilles vhost config
 * pins DATEFORMAT using the current expanded strftime vocabulary
 * (the full Python strftime token set supported by the
 * token-aware walker in bbsengine6/smarty/modifier.datestamp.php
 * and zoid6/smarty/modifier.datestamp.php). See
 * bbsengine6/handbook/specs/datestamp.md for the full spec.
 *
 * The achilles vhost is a zoid6-using site. zoid6.php (loaded
 * by index.php AFTER config.php) defines a bare `DATEFORMAT`
 * constant with a different value. To avoid that conflict,
 * achilles config-prod.php pins `\config\DATEFORMAT` (the
 * namespaced form the zoid6 modifier reads first). This test
 * verifies the config-prod.php define:
 *
 *   1. Exists in achilles/www/config-prod.php as a
 *      `define("config\\DATEFORMAT", ...)` line.
 *   2. Uses only strftime tokens that the bbsengine6 and zoid6
 *      token-aware walkers both support (the "current expansion"
 *      vocabulary).
 *   3. When fed into the canonical walker (loaded from the repo
 *      source, not the deployed /srv/www/ copy, so the test
 *      passes regardless of deploy state), produces output that
 *      contains no literal `%X` artifacts (the symptom of the
 *      OLD strftime→date str_replace modifier that didn't know
 *      `%b`, `%a`, `%l`, etc.).
 *
 * Usage:
 *   php test_datestamp_config.php
 */

declare(strict_types=1);

const REPO_ROOT          = "/home/opencode/data/work";
const ACHILLES_ROOT      = REPO_ROOT . "/achilles";
const ACHILLES_CONFIG    = ACHILLES_ROOT . "/www/config-prod.php";
const BBS_MODIFIER_SRC   = REPO_ROOT . "/bbsengine6/smarty/modifier.datestamp.php";
const ZOID6_MODIFIER_SRC = REPO_ROOT . "/zoid6/smarty/modifier.datestamp.php";

// Tokens both modifiers support (the "current expansion" set).
// Mirrors $strftimeToDate in both walker implementations, plus
// the inline-handled %j and %O and the literal %%.
const SUPPORTED_TOKENS = [
    "%Y", "%y", "%m", "%b", "%B",
    "%d", "%H", "%I", "%l",
    "%M", "%S", "%p", "%P",
    "%Z", "%z", "%:z",
    "%a", "%A",
    "%%", "%j", "%O",
];

$passed = 0;
$failed = 0;

function test_pass(string $name, string $detail = ""): void {
    global $passed;
    $passed++;
    echo "  \u{2713} PASS: $name" . ($detail !== "" ? ": $detail" : "") . "\n";
}

function test_fail(string $name, string $detail = ""): never {
    global $failed;
    $failed++;
    echo "  \u{2717} FAIL: $name" . ($detail !== "" ? " \u{2014} $detail" : "") . "\n";
    exit(1);
}

function check(bool $cond, string $name, string $detail = ""): void {
    if ($cond) {
        test_pass($name, $detail);
    } else {
        test_fail($name, $detail);
    }
}

echo "=== achilles |datestamp config Tests ===\n\n";

// =============================================================================
// 1. config-prod.php pins config\DATEFORMAT.
// =============================================================================

echo "--- 1. achilles config pins \\config\\DATEFORMAT ---\n\n";

check(file_exists(ACHILLES_CONFIG), "achilles config-prod.php exists", ACHILLES_CONFIG);

$configSrc = file_get_contents(ACHILLES_CONFIG);

// Match `define("config\\DATEFORMAT", "...")`. The PHP source has
// the backslashes literally doubled (escaped), so the regex
// needs to match two literal backslashes: PCRE `\\\\` = PHP
// single-quoted string `'\\\\\\\\'` (8 backslashes total).
$configHasDateformat = (bool)preg_match(
    '/define\(\s*"config\\\\\\\\DATEFORMAT"\s*,\s*"([^"]*)"\s*\)/',
    $configSrc,
    $matches
);

if (!$configHasDateformat) {
    test_fail("config\\DATEFORMAT define present", "no `define(\"config\\\\DATEFORMAT\", ...)` line found in " . ACHILLES_CONFIG);
}

$configDateformat = $matches[1];
test_pass("config\\DATEFORMAT define present", "[$configDateformat]");

// =============================================================================
// 2. The format uses only currently-supported strftime tokens.
// =============================================================================

echo "\n--- 2. \\config\\DATEFORMAT uses only currently-supported strftime tokens ---\n\n";

// Walk the format string and extract every %X sequence (including
// multi-character ones like %:z). %% is treated as a single
// literal token.
preg_match_all('/%(?::?[A-Za-z%])/', $configDateformat, $tokenMatches);
$usedTokens = array_unique($tokenMatches[0]);

$unsupported = [];
foreach ($usedTokens as $tok) {
    if (!in_array($tok, SUPPORTED_TOKENS, true)) {
        $unsupported[] = $tok;
    }
}

if (!empty($unsupported)) {
    test_fail(
        "all tokens in \\config\\DATEFORMAT are currently supported",
        "unsupported tokens: " . implode(", ", $unsupported)
    );
}

test_pass(
    "all tokens in \\config\\DATEFORMAT are currently supported",
    "tokens used: " . implode(" ", $usedTokens)
);

// =============================================================================
// 3. The walker (loaded from the repo source) renders the format
//    without leaving any literal %X artifacts. This catches the
//    "2026-%b-13 %Tuesday:28AM EDT (%am)" symptom of the OLD
//    strftime->date str_replace modifier that didn't know %b,
//    %a, %l, etc.
// =============================================================================

echo "\n--- 3. bbsengine6 walker renders achilles DATEFORMAT cleanly ---\n\n";

// Stub the require_once("config.php") line so the loaded modifier
// doesn't try to load a real vhost config (which would define
// \config\DATEFORMAT and bypass our pin). The modifier delegates
// to \bbsengine6\util\datestamp (the canonical PHP date/time
// formatter in bbsengine6/php/util.php), so we load util.php
// first to make that function available.
require_once(__DIR__ . "/../../../bbsengine6/php/util.php");
$bbsSource = file_get_contents(BBS_MODIFIER_SRC);
$bbsSource = preg_replace('/require_once\("config\.php"\);/', '// stubbed', $bbsSource);

// Pin both forms before eval so the walker reads whichever form
// it checks first.
define("config\\DATEFORMAT", $configDateformat);
define("DATEFORMAT", $configDateformat);

eval("?>" . $bbsSource);

$ts = strtotime('2026-10-13 14:30:00 America/New_York');
$actual = smarty_modifier_datestamp($ts);

// No literal %X (where X is alpha) should appear in the rendered
// output. The OLD str_replace modifier would render "%b" and "%a"
// literally; the walker translates them.
if (preg_match('/%[a-z]/', $actual)) {
    test_fail(
        "bbsengine6 walker output has no literal %X artifacts",
        "got [$actual]"
    );
}

test_pass(
    "bbsengine6 walker output has no literal %X artifacts",
    "[$actual]"
);

// Sanity check the rendered output contains the year, day, and
// day name (the canonical parts of the achilles format).
check(strpos($actual, "2026") !== false, "output contains year 2026", "[$actual]");
check(strpos($actual, "13") !== false,   "output contains day 13",   "[$actual]");
check(strpos($actual, "(Tue)") !== false || strpos($actual, "(Tuesday)") !== false,
      "output contains day name", "[$actual]");

// =============================================================================
// 4. The zoid6 walker (loaded from the repo source) renders the
//    format cleanly with the same input. Both modifiers must
//    agree for the "achilles should not shadow zoid6" rule to
//    hold.
// =============================================================================

echo "\n--- 4. zoid6 walker renders achilles DATEFORMAT cleanly ---\n\n";

$zoid6Source = file_get_contents(ZOID6_MODIFIER_SRC);
$zoid6Source = preg_replace('/require_once\("config\.php"\);/', '// stubbed', $zoid6Source);
// util.php is already loaded above (for the bbsengine6 modifier);
// the zoid6 modifier delegates to the same \bbsengine6\util\datestamp().

// The bbsengine6 modifier already defined
// smarty_modifier_datestamp() above. Rename the zoid6 modifier's
// copy so we can load both in the same PHP process and exercise
// the achilles->zoid6->bbsengine6 chain end-to-end. The walker
// logic is identical between bbsengine6 and zoid6 today (the
// "achilles should not shadow zoid6" rule), so this rename is the
// only difference.
$zoid6Source = str_replace(
    'function smarty_modifier_datestamp',
    'function zoid6_smarty_modifier_datestamp',
    $zoid6Source
);

eval("?>" . $zoid6Source);

/** @var callable $zoid6Callable */
$zoid6Callable = 'zoid6_smarty_modifier_datestamp';
$actualZoid6 = $zoid6Callable($ts);

if (preg_match('/%[a-z]/', $actualZoid6)) {
    test_fail(
        "zoid6 walker output has no literal %X artifacts",
        "got [$actualZoid6]"
    );
}

test_pass(
    "zoid6 walker output has no literal %X artifacts",
    "[$actualZoid6]"
);

check(strpos($actualZoid6, "2026") !== false, "zoid6 walker output contains year 2026", "[$actualZoid6]");
check(strpos($actualZoid6, "13") !== false,   "zoid6 walker output contains day 13",   "[$actualZoid6]");

// =============================================================================
// 5. Both walkers produce identical output for the same input.
//    This pins the achilles->zoid6->bbsengine6 chain to a single
//    canonical rendering (no shadowing drift).
// =============================================================================

echo "\n--- 5. bbsengine6 and zoid6 walkers agree on achilles DATEFORMAT ---\n\n";

check(
    $actual === $actualZoid6,
    "bbsengine6 walker output matches zoid6 walker output",
    "bbs=[$actual] zoid6=[$actualZoid6]"
);

echo "\n=== Test Results ===\n";
echo "Passed: $passed\n";
echo "Failed: $failed\n";

if ($failed > 0) {
    exit(1);
}

echo "\n\u{2713} All achilles |datestamp config tests passed!\n";
exit(0);