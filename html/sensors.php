<?php

header('Access-Control-Allow-Origin: *');

class ret
{
	public $requestTime = "now";

	public $data = [];
}

$db = new SQLite3("/home/pi/sensors.db");
$res = $db->query("select round(temperature,1) as t, round(pressure,0) as p, round(moisture, 1) as m, time from sensors where julianday()-julianday(time)<2;");
$data = new ret();

while ($row = $res->fetchArray(SQLITE3_ASSOC)) {

	$data->data[]=$row;
}


echo json_encode($data);


?>
