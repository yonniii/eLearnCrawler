<?php 

    error_reporting(E_ALL); 
    ini_set('display_errors',1); 

    include('dbcon.php');
        

    $stmt = $con->prepare('select * from eLearn.users');
    $stmt->execute();

    if ($stmt->rowCount() > 0)
    {
        $data = array(); 

        while($row=$stmt->fetch(PDO::FETCH_ASSOC))
        {
            extract($row);
    
            array_push($data, 
                array('username'=>$username,
                'email'=>$email,
                'password'=>$password,
	   'eLearnID'=>$eLearnID,
	   'eLearnPW'=>$eLearnPW
            ));
        }

        header('Content-Type: application/json; charset=utf8');
        $json = json_encode(array("root"=>$data), JSON_PRETTY_PRINT+JSON_UNESCAPED_UNICODE);
        echo $json;
    }

?>
