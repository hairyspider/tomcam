<?php
class settings{
	public $temp=0;
	public $fan=0;
	public $moist=0;
	public $water=0;
}



if ($_SERVER["REQUEST_METHOD"] == "POST")
{
	if (!empty(trim($_POST["temp_action"]))){
		$temp_action = $_POST["temp_action"];
		#updateSetting("temp", $temp_action);
	}
	if (!empty(trim($_POST["fan_duration"]))){
		$fan_duration = $_POST["fan_duration"];
		#updateSetting("fan", $fan_duration);
	}
	if (!empty(trim($_POST["moist_action"]))){
		$moist_action = $_POST["moist_action"];
		#updateSetting("soil", $moist_action);
	}
	if (!empty(trim($_POST["water_duration"]))){
		$water_duration = $_POST["water_duration"];
		#updateSetting("water", $water_duration);
	}
	$a = new settings;
	$a->temp=$temp_action;
	$a->fan=$fan_duration;
	$a->moist=$moist_action;
	$a->water=$water_duration;
	
	$s = json_encode($a);
	
	file_put_contents("/opt/irrigation/settings.conf", $s );
	
	
	header("location: dashboard.html?done");
}

$s = file_get_contents("/opt/irrigation/settings.conf");


header('Access-Control-Allow-Origin: *');
echo $s;



?>
