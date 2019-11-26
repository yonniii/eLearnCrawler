<?php 
	error_reporting(E_ALL);
	ini_set('display_errors',1);
	include('dbcon.php');
	
	$stmt = $con->prepare('select * from notices');
        $stmt->execute();

        if ($stmt->rowCount() > 0)
	{
		$data = array(); 
		while($row=$stmt->fetch(PDO::FETCH_ASSOC))
		{
			extract($row);
			
			array_push($data, 
				array('type'=>$type,
				'title'=>$title,
				'url'=>$url,
				'writter'=>$writter,
				'date'=>$date,
				'updated_time'=>$updated_time,
				));
		}
		header('Content-Type: application/json; charset=utf8');
		$json = json_encode(array("notices"=>$data), JSON_PRETTY_PRINT+JSON_UNESCAPED_UNICODE);
		echo $json;
	}
?>
