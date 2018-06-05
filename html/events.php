<?php

header('Access-Control-Allow-Origin: *');

class ret
{
	public $requestTime = "now";

	public $data = [];
}

$db = new SQLite3("/home/pi/sensors.db");
$res = $db->query("select events.description as d, events.time as t, eventtype.type as n  from events inner join eventtype on eventtype.id = events.typeid where julianday()-julianday(time)<2 order by events.id desc;");
$data = new ret();

while ($row = $res->fetchArray(SQLITE3_ASSOC)) {
	$data->data[]=$row;
}


echo json_encode($data);


?>
