<?php
include 'sqlite.php';

$db = connect();

$deviceId = "1";
$startTime = 1455746400;
$endTime = 1455919200;

$data = getData($deviceId, $startTime, $endTime);

$data = json_encode($data);
var_dump($data);
$db->close();

?>
