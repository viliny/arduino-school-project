<?php
include 'sqlite.php';

$db = connect();

$startTime = 1457075283;

for($i = 1; $i<5; $i++)
{
	echo("kirjoitetaan laitteelle " . $i . "\n");
	for($j = 0; $j<1000; $j++)
	{
		$db->query("INSERT INTO Data VALUES('".$i."' , " . rand(70,90) . " , " . rand(18,25) . "," . rand(0,1) . ", " . rand(0,1) . ", '" . rand(0,99) . "', " . $startTime . ")");
		$db->query("INSERT INTO Log VALUES('INFO' , 'Data haettu onnistuneesti' , '".$i."', '0', ".$startTime.")");
		$startTime += 60 * 5;
		echo("Kirjoitettiin rivi: " . $j . "\n");
	}
}

$db->close();

?>
