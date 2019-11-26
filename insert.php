<?php
	error_reporting(E_ALL);
        ini_set('display_errors',1);

	include('dbcon.php');
	$android = strpos($_SERVER['HTTP_USER_AGENT'], "Android");

	if((($_SERVER['REQUEST_METHOD']=='POST')&&isset($_POST['submit'])) || $android){
		$u_id=$_POST['u_id'];
		$u_pw=$_POST['u_pw'];

		if(empty($u_id)){
			$errMSG = "enter the id";
		}
		else if(empty($u_pw)){
			$errMSG = "enter the password";
		}
		if(!isset($errMSG)){
                        try{
				$stmt = $con->prepare('INSERT INTO Login(u_id,u_pw) VALUES(:u_id, :u_pw)');
				$stmt->bindParam(':u_id',$u_id);
				$stmt->bindParam(':u_pw',$u_pw);
				if($stmt->execute()){
					$successMSG = "add new user";
				}
				else
				{
					$errMSG = "Error add new user";
				}
			}catch(PDOException $e){
				die("Database error: ".$e->getMessage());
			}
		}
	}
?>
<html>
	<body>
	<?php
	if(isset($errMSG)) echo $errMSG;
	if(isset($successMSG)) echo $successMSG;
	?>
		<form action="<?php $_PHP_SELF ?>" method="POST">
			ID: <input type = "text" name="u_id"/>
	          		PW: <input type = "text" name = "u_pw" />
			<input type="submit" name="submit" />
		</form>
	</body>
</html>
