<?php  

$link=mysqli_connect("ec2-52-79-206-60.ap-northeast-2.compute.amazonaws.com","root","1234", "eLearn" );  
if (!$link)  
{  
    echo "MySQL connect error : ";
    echo mysqli_connect_error();
    exit();  
}  

mysqli_set_charset($link,"utf8"); 


$sql="select * from users";

$result=mysqli_query($link,$sql);
$data = array();   
if($result){  
    
    while($row=mysqli_fetch_array($result)){
        array_push($data, 
            array('username'=>$row[0],
            'email'=>$row[1],
            'password'=>$row[2],
			'eLearnID'=>$row[3],
			'eLearnPW'=>$row[4]
        ));
    }

    echo "<pre>"; print_r($data); echo '</pre>';

}  
else{  
    echo "SQL ing error : "; 
    echo mysqli_error($link);
} 


 
mysqli_close($link);  
   
?>
