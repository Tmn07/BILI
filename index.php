<?php
	session_start();

	// echo 'post:' . $_POST['token'].'<br>';
	// echo 'sse:' . $_SESSION['token'] ;

	if(isset($_POST['num']) && $_POST['token'] == $_SESSION['token']) {
		// echo $_POST['num'];
		 
		// $_SESSION['token'] = rand(0,1000);
		$num = escapeshellarg($_POST['num']);
		// system("ls -al ~/PythonProjects/BILI/");
		$ret = system('python bilibili.py '.$num ." -p html.parser");
		// var_dump($arr);
		 // echo $resval;
		if ($ret) {
			// echo $resval;
			$filename = 'danmu.txt';
			// $res = file_get_contents('danmu.txt');
			$handle = fopen($filename, "r");//读取二进制文件时，需要将第二个参数设置成'rb'
    
		    //通过filesize获得文件大小，将整个文件一下子读到一个字符串中
		    $res = fread($handle, filesize ($filename));
		    fclose($handle);
			
		}
		$_SESSION['token'] = rand(0,1000);

	}

?>

<!DOCTYPE html>
<html>
<head>
	<title>惰怠的弹幕.</title>
	<meta charset="utf-8">
</head>
<script src="http://lib.sinaapp.com/js/jquery/1.9.1/jquery-1.9.1.min.js"></script>


<style type="text/css">
	.result{
	    margin: 20px;
	    width: 600px;
	    min-height: 200px;
	}
</style>

<body>
	<div class="main">
		<form action="" method="post">
			<label>AV_num:</label>
			<input type="text" name="num" />
			<input type="submit" class="submit" value="submit"/>
			<input type="hidden" name="token" value="<?php echo $_SESSION['token'];?>">
		</form>

	</div>
	<div class="result">
		<?php

		if (isset($res)) {
			?>
				<a type="button" href="danmu.txt" download="danmu.txt">下载 </a><br/>
			<?php
			$res = split("\n", $res);
			// var_dump($res);
			echo "弹幕内容\t发送位置\t发送时间 <br/>";
			for ($i=0; $i < count($res); $i++) { 
				echo $res[$i] . "<br/>";
			}

			// echo $res;
		}
		?>
	</div>
</body>
</html>