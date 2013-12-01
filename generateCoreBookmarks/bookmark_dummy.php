<?php

$file = 'http:// ';
if (function_exists('curl_version'))
{
	$curl = curl_init();
	curl_setopt($curl, CURLOPT_URL, $file);
	curl_setopt($curl, CURLOPT_RETURNTRANSFER, 1);
	$content = curl_exec($curl);
	curl_close($curl);
}
else if (file_get_contents(__FILE__) && ini_get('allow_url_fopen'))
{
	$content = file_get_contents($file);
}
else
{
	echo 'Neither cURL nor allow_url_fopen are active. Please activate one of them to use this script!';
}
?>