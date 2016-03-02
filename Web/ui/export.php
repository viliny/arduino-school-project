<?php
// output headers so that the file is downloaded rather than displayed
header('Content-Type: text/csv; charset=utf-8');
header('Content-Disposition: attachment; filename=data.csv');

include 'sqlite.php';

$startTime = strtotime($_REQUEST['startTime']);
$endTime = strtotime($_REQUEST['endTime']);
$deviceId = $_REQUEST['deviceId'];
$data = getData($deviceId,$startTime,$endTime);
deleteData($deviceId,$startTime,$endTime);


// create a file pointer connected to the output stream
$output = fopen('php://output', 'w');

fputcsv($output, array("id","humidity","temperature","kansi auki(0=kiinni, 1=auki)","veden korkeus(0=ok, 1=matala)","virransyötön status","aikaleima"));

// loop over the rows, outputting them
foreach($data as $key=>$value)
{
	fputcsv($output, $value);
}


?>
