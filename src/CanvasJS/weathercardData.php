<?php
//Set header to app/json
header('Content-Type: application/json');

//Declare our connection values
$username = "root";
$password = "ECE435";
$hostname = "localhost"; 
$database = "weatherdata";

//Connect to our database, in this case weatherdata
$mysqli = new mysqli($hostname, $username, $password, $database);

//error check
if(!$mysqli){
	die("Connection failed: ".$mysqli->error);
}


//Our query to the database
$query = "SELECT * FROM weathercards";

//Execute our query
$result = $mysqli->query($query)
	or die("Query failed: ".$mysqli->error);

//Put the returned data into an array
$data = array();
foreach ($result as $row) {
	$data[] = $row;
}

//Our returned data is now stored in the $data array, so we can free the memory associated with $result
$result->close();

//Always close the connection as soon as possible
$mysqli->close();

//Print data in json format
print json_encode($data);

?>
