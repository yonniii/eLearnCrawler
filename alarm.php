<?php
        error_reporting(E_ALL);
        ini_set('display_errors',1);

        include('dbcon.php');

        $android = strpos($_SERVER['HTTP_USER_AGENT'], "Android");

        if((($_SERVER['REQUEST_METHOD']=='POST')&&isset($_POST['submit'])) || $android){
                $time=$_POST['time'];
         $id=$_POST['id'];
                if(empty($time)){
                        $errMSG = "enter the time";
                }
         else if(empty($id)){
          $errMSG = "enter the time";
         }
                if(!isset($errMSG)){
                        try{
                                $stmt = $con->prepare('INSERT INTO alarm(time,id) VALUES(:time,:id)');
                                $stmt->bindParam(':time',$time);
           $stmt->bindParam(':id',$id);
                                if($stmt->execute())
                                {
                                        $successMSG = "add new time";
                                }
                                else
                                {
                                        $errMSG = "Error add new time";
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
                        TIME: <input type = "text" name="time"/>
          ID:<input type="text" name="id"/>
                        <input type="submit" name="submit" />
                </form> 
        </body>
</html>
