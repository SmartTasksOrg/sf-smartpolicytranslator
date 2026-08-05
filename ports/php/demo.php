<?php
require __DIR__ . "/src/SptClient.php";
use SmartTasks\Spt\SptClient;
[$ds, $out] = [$argv[1], $argv[2]];
@mkdir($out, 0777, true);
$c = new SptClient(getenv("SPT_URL") ?: "http://localhost:8000");
foreach (glob("$ds/*.txt") as $f) {
    $res = $c->translate(file_get_contents($f));
    $name = basename($f, ".txt");
    file_put_contents("$out/$name.policy.json", json_encode($res, JSON_PRETTY_PRINT));
    echo "  $name: " . $res["iaiso_policy"]["enforcement_mode"] . "\n";
}
