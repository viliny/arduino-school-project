<?php

function connect()
{
	if(file_exists('monitor.db'))
	{
		$db = new sqlite3('monitor.db');
		$db->busyTimeOut(10000);
		return $db;
	}else
	{
		$db = new sqlite3('monitor.db');
		$db->busyTimeOut(10000);
		$db->query("CREATE TABLE Device(deviceId TEXT , lastUpdate NUMERAL , deviceName TEXT, error NUMERAL)");
		$db->query("CREATE TABLE Data(deviceId TEXT , humidity NUMERAL , temp NUMERAL, lidSwitchOpen NUMERAL, waterLevelLow NUMERAL, batteryStatus TEXT, measureTime NUMERAL)");
		$db->query("CREATE TABLE Settings(email TEXT UNIQUE, name TEXT, lang TEXT, humidityTrshld NUMERAL, tempTrshld NUMERAL, lidSwitchTrshldTime NUMERAL)");
		return $db;
	}
}

function addNewDevice($deviceId,$deviceName)
{
	$db = connect();
	$db->query("INSERT INTO Device VALUES('".$deviceId."','".time()."','".$deviceName."',0)");
	$db->close();
}

function deleteDevice($deviceId)
{
	$db = connect();
	$db->query("DELETE FROM Device WHERE deviceId = '".$deviceId."'");
	$db->close();
}

function getLatestData($deviceId)
{
	$db = connect();
	$result = $db->query("SELECT * FROM Data WHERE deviceId = '".$deviceId."' ORDER BY measureTime DESC LIMIT 1;");
	$data = $result->fetchArray(SQLITE3_ASSOC);
	$db->close();
	return $data;
}

function deleteData($deviceId, $startTime, $endTime)
{
	$db = connect();
	$db->query("DELETE FROM Data WHERE deviceId = '".$deviceId."' AND measureTime > " . $startTime ." AND measureTime < " . $endTime);
	$db->close();
	return $data;
}

function getDevices()
{
	$rows = array();
	$db = connect();
	$results = $db->query("SELECT * FROM Device");
	while($row = $results->fetchArray(SQLITE3_ASSOC))
		array_push($rows, $row);
	$db->close();
	return $rows;
}

function getData($deviceId, $startTime, $endTime)
{
	$rows = array();
	$db = connect();
	$results = $db->query("SELECT * FROM Data WHERE deviceId = '".$deviceId."' AND measureTime > ".$startTime." AND measureTime < " . $endTime);
	while($row = $results->fetchArray(SQLITE3_ASSOC))
	{
		array_push($rows, $row);
	}
	$db->close();
	return $rows;
}

function getSettings()
{
	$db = connect();
	$result = $db->query("SELECT * FROM Settings");
	$data = $result->fetchArray(SQLITE3_ASSOC);
	$db->close();
	return $data;
}

function setSettings($email,$name,$humidityTrshld,$tempTrshld,$lidSwitchTrshldTime)
{
	$db = connect();
	$db->query("DELETE FROM Settings");
	$db->query("INSERT INTO Settings VALUES('$email','$name','fi','$humidityTrshld','$tempTrshld','$lidSwitchTrshldTime')");
	$db->close();
}
?>
