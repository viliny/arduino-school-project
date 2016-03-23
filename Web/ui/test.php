<?php

include "sqlite.php";

$db = connect();

$db->query("INSERT INTO Log VALUES('erxcror' , 'testi' , 'testi1', 1, 5)");
$db->query("INSERT INTO Log VALUES('error' , 'yhteyshäiriö' , 'testi1', 1, 6)");
$db->query("INSERT INTO Log VALUES('alert' , 'homo' , 'testi1', 1, 4)");
$db->query("INSERT INTO Log VALUES('errzxcor' , 'yhteyshäihomoriö' , 'testi1', 1, 2)");
$db->query("INSERT INTO Log VALUES('errzxcor' , 'yhteyshäiriö' , 'testi1', 1, 3)");
$db->query("INSERT INTO Log VALUES('error' , 'yhteysasdasdhäiriö' , 'testi1', 1, 1)");
$db->close();
?>
