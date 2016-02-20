<?php
include 'sqlite.php';

$db = connect();



for($i = 1; $i<5; $i++)
{
	$measure = time() - 7200;
	
	for($j = 0; $j<100; $j++)
	{
		$measure += (60 * 5);
		$humidity = rand(75, 85);
		$temp = rand(19, 23);
		$result = $db->query("INSERT INTO Data VALUES('".$i."','".$humidity."','". $temp ."','0','0','verkkovirta','" . $measure . "');");
		echo("DEBU|| Laite: ". $i .", Rivi: " .$j. ", Kosteus: " . $humidity . ", Lämpötila: " . $temp . ", aikaleima: " . $measure . "\n");
	}
}

$db->close();

?>
