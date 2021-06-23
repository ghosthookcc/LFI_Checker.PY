<?php

include_once("cgi-bin/processfiles.php");

$program = new fileinfo;
$returnvalue = $program->iterdir("200");
$urls = $program->getUrls("urls.txt");

$fileNames = $returnvalue[0];
$fileExtensions = $returnvalue[1];
$fileSizes = $returnvalue[2];
$fileContent = $returnvalue[3];

$length = sizeof($fileNames);

?>

<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<meta http-equiv="origin-trial" content="Avk9PfkdFizUZbCY55oIEHe1156lSiyX5bQdCZzavJ8UWwRin0pAwceyAlrVxOId7YZMT+csGF44p2PBOBl0iAsAAABUeyJvcmlnaW4iOiJodHRwOi8vbG9jYWxob3N0Ojc3NzciLCJmZWF0dXJlIjoiTmF0aXZlRmlsZVN5c3RlbTIiLCJleHBpcnkiOjE1OTY5Nzc3NTB9">

	<link href="css/style.css" rel="stylesheet" type="text/css">

	<script src="js/js_test/qunit.js"></script>

</head>
<body>

<!--
<br>

<a href='{r.url}'>((({params[param]}))) :: {url+params[param]}</a><br>
-->

<div id="mainContainer">

	<?php

	/*
	foreach($urls as $url)
	{
		echo $url;
	}
	*/

	?>

</div>


<footer>

	<div id="filesContainer">

		<?php addElement($length,
										 $fileNames,
										 $fileExtensions,
										 $fileSizes,
									 	 $fileContent);
    ?>

	</div>

</footer>

<script type="text/javascript" src="https://code.jquery.com/jquery-3.5.1.min.js"></script>
<script src="js/fso.min.js"></script>
<script src="js/urlmanager.js"></script>

</body>
</html>
