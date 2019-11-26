<?php
	error_reporting(E_ALL);\
	ini_set('display_errors',1);
	
	include('dbcon.php');
	$stmt = $con->prepare('select * from reports');
	$stmt->execute();
	if ($stmt->rowCount() > 0)
	{
		$data = array();
		
		while($row=$stmt->fetch(PDO::FETCH_ASSOC))
		{
			extract($row);
			array_push($data,
				array(
				'stdnt_no'=>$stdnt_no,
					'id'=>$id,
				'title'=>$title,
				'start_time'=>$start_time,
				'end_time'=>$end_time,
				'type'=>$type,
				'subject'=>$subject,
				'report_no'=>$report_no,
				'is_submit'=>$is_submit,
				'is_include'=>$is_include,
				'is_press'=>$is_progress,
				'updated_time'=>$updated_time));
		}
	        header('Content-Type: application/json; charset=utf8');
	        $json = json_encode(array("reports"=>$data), JSON_PRETTY_PRINT+JSON_UNESCAPED_UNICODE);
	        echo $json;
	}
?>

