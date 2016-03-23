<?php
//ui:n ajax funkkarit tänne kiitos

include 'sqlite.php';

switch($_REQUEST['mode']) {
	case "updateDevices":
		$rows = getDevices();
		$json = json_encode($rows);
		echo($json);
	break;
	
	case "updateDevice":
		$data = json_encode(getLatestData($_REQUEST['id']));
		echo($data);
	break;
	
	case "getSettings":
		$data = getSettings();
		$json = json_encode($data);
		echo($json);
	break;
	case "addNewDevice":
		addNewDevice($_REQUEST['deviceId'],$_REQUEST['deviceName']);
	break;
	case "deleteDevice":
		deleteDevice($_REQUEST['deviceId']);
	break;
	case "setSettings":
		setSettings($_REQUEST['email'],$_REQUEST['name'],$_REQUEST['humidityTrshld'],$_REQUEST['tempTrshld'],$_REQUEST['lidSwitchTrshldTime']);
	break;
	case "getChart":
		
		$startTime = $_REQUEST['startTime'];
		$endTime = $_REQUEST['endTime'];
		$startTime = strtotime($startTime);
		$endTime = strtotime($endTime);
		$deviceId = $_REQUEST['deviceId'];
		
		$output = getData($deviceId,$startTime,$endTime);
		$output = json_encode($output);
		echo($output);
	break;
	case "updateLog":
		$output = updateLog($_REQUEST['filters'],$_REQUEST['orderBy'], $_REQUEST['isAsc']);
		$output = json_encode($output);
		echo($output);
	break;
}

?>
